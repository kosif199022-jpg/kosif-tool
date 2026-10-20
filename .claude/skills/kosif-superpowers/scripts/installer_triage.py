#!/usr/bin/env python3
"""KOSIF Superpowers: read-only triage of Windows installers and desktop apps before REA.

REA's artifact graph treats an NSIS/Inno/UPX installer as one opaque PE with no
children, so it never reaches the app inside. This tool closes that gap:

  scan <file|dir>            identify installer family, packer, Electron, .NET, signature slot, version strings,
                             payloads hidden in PE resources (MSI/CAB/EXE), encrypted RAR, Adobe offline packages
  unpack <file> --to <new>   extract the payload with 7-Zip (innoextract for Inno Setup) into an ABSENT folder
                             (never runs the target)
  asar <app.asar> [entry]    list an Electron archive / print one small text entry (package.json)
  fingerprint <app.asar>     count Electron capability anchors in the main bundle (feature evidence)
  route <dir>                map every unpacked artifact to the REA command that fits it

Pure standard library. Nothing here executes target code, contacts the network or installs anything.
`unpack` needs --authorized and a 7-Zip binary (7z/7za/7zz on PATH or SEVEN_ZIP).
Results are evidence of *structure*, never of runtime behaviour: verified is always false.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import struct
import subprocess
import sys

SOURCE = "https://github.com/morluto/rea"
CHUNK = 1 << 20
MAX_SCAN_BYTES = 4 << 20          # signatures are searched in the first 4 MiB of the overlay
MAX_ASAR_HEADER = 64 << 20
MAX_TEXT_ENTRY = 2 << 20
MAX_FINGERPRINT_BYTES = 64 << 20

SIG = {
    "nsis": b"\xef\xbe\xad\xdeNullsoftInst",
    "inno": b"Inno Setup Setup Data (",
    "inno_ldr": b"rDlPtS\xcd\xe6\xd7{\x0b*",
    "sevenzip": b"7z\xbc\xaf\x27\x1c",
    "zip": b"PK\x03\x04",
    "msi_ole": b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1",
    "cab": b"MSCF\x00\x00\x00\x00",
    "electron_fuse": b"dL7pKGdnNz796PbbjQWNKmHXBZaB9tsX",
    "squirrel": b"SquirrelTemp",
    "wixburn": b".wixburn",
    "installshield": b"InstallShield",
    "inno_zlb": b"zlb\x1a",                 # Inno Setup compressed block at the start of its overlay
    "rar4": b"Rar!\x1a\x07\x00",
    "rar5": b"Rar!\x1a\x07\x01\x00",
    "mz": b"MZ",
}
MIN_EMBEDDED = 1 << 20                      # resources this large are payloads, not icons or dialogs
RT_NAMES = {1: "CURSOR", 2: "BITMAP", 3: "ICON", 4: "MENU", 5: "DIALOG", 6: "STRING", 10: "RCDATA",
            12: "GROUP_CURSOR", 14: "GROUP_ICON", 16: "VERSION", 24: "MANIFEST"}
MACHINES = {0x14C: "x86", 0x8664: "x86_64", 0xAA64: "arm64", 0x1C4: "arm"}

# Electron/Chromium capability anchors → (feature id, Arabic, English). Counted, never executed.
ELECTRON_ANCHORS = {
    "desktopCapturer": ("screen-capture", "تسجيل الشاشة/النوافذ", "screen and window capture"),
    "getDisplayMedia": ("screen-capture", "تسجيل الشاشة/النوافذ", "screen and window capture"),
    "getUserMedia": ("camera-mic", "الكاميرا والميكروفون", "camera and microphone input"),
    "MediaRecorder": ("recording", "تسجيل الوسائط", "media recording"),
    "autoUpdater": ("auto-update", "التحديث التلقائي", "auto update"),
    "electron-updater": ("auto-update", "التحديث التلقائي", "auto update"),
    "Tray": ("tray", "أيقونة شريط المهام", "system tray"),
    "Notification": ("notifications", "إشعارات النظام", "system notifications"),
    "setAsDefaultProtocolClient": ("deep-link", "روابط عميقة بمخطط خاص", "custom URL scheme deep links"),
    "protocol.handle": ("custom-protocol", "بروتوكول داخلي", "custom in-app protocol"),
    "safeStorage": ("secure-storage", "تخزين مشفر للأسرار", "OS-encrypted secret storage"),
    "crashReporter": ("crash-reporting", "تقارير الأعطال", "crash reporting"),
    "sentry": ("crash-reporting", "تقارير الأعطال", "crash reporting"),
    "nativeTheme": ("dark-mode", "الوضع الداكن حسب النظام", "follows OS dark mode"),
    "showSaveDialog": ("file-dialogs", "حوارات حفظ وفتح", "save/open dialogs"),
    "showOpenDialog": ("file-dialogs", "حوارات حفظ وفتح", "save/open dialogs"),
    "addWordToSpellCheckerDictionary": ("spellcheck", "تدقيق إملائي", "spell checking"),
    "printToPDF": ("print-pdf", "طباعة وتصدير PDF", "print and PDF export"),
    "powerSaveBlocker": ("keep-awake", "منع السكون أثناء العمل", "keep the machine awake"),
    "globalShortcut": ("global-shortcuts", "اختصارات عامة", "global shortcuts"),
    "MessageChannelMain": ("message-port", "قناة MessagePort بين العمليات", "MessagePort bridge"),
    "requestMessagePort": ("message-port", "قناة MessagePort بين العمليات", "MessagePort bridge"),
    "contextBridge": ("context-bridge", "جسر آمن للواجهة", "context-isolated bridge"),
    "utilityProcess": ("utility-process", "عمليات مساعدة", "utility processes"),
    "offline": ("offline", "عمل بلا إنترنت", "offline mode"),
    "webRequest": ("network-policy", "تحكم في طلبات الشبكة", "network request policy"),
}


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(CHUNK), b""):
            h.update(block)
    return h.hexdigest()


def parse_pe(data_head, size):
    """Minimal PE header parse from the first bytes of a file. Returns None when not PE."""
    if len(data_head) < 0x40 or data_head[:2] != b"MZ":
        return None
    e_lfanew = struct.unpack_from("<I", data_head, 0x3C)[0]
    if e_lfanew + 24 > len(data_head) or data_head[e_lfanew:e_lfanew + 4] != b"PE\0\0":
        return None
    machine, nsec, timestamp, _, _, opt_size, characteristics = struct.unpack_from("<HHIIIHH", data_head, e_lfanew + 4)
    opt = e_lfanew + 24
    magic = struct.unpack_from("<H", data_head, opt)[0] if opt + 2 <= len(data_head) else 0
    pe32plus = magic == 0x20B
    dd_off = opt + (112 if pe32plus else 96)
    dirs = []
    for i in range(16):
        o = dd_off + i * 8
        if o + 8 > len(data_head):
            break
        dirs.append(struct.unpack_from("<II", data_head, o))
    sections, end_of_image = [], 0
    sec_off = opt + opt_size
    for i in range(nsec):
        o = sec_off + i * 40
        if o + 40 > len(data_head):
            break
        name = data_head[o:o + 8].rstrip(b"\0").decode("latin-1")
        vsize, va, rsize, rptr = struct.unpack_from("<IIII", data_head, o + 8)
        sections.append({"name": name, "virtual_size": vsize, "virtual_address": va, "raw_size": rsize, "raw_offset": rptr})
        end_of_image = max(end_of_image, rptr + rsize)
    sec_dir = dirs[4] if len(dirs) > 4 else (0, 0)   # security directory: file offset, not RVA
    if sec_dir[0] and sec_dir[0] >= end_of_image:
        overlay_end = sec_dir[0]
    else:
        overlay_end = size
    return {
        "machine": MACHINES.get(machine, hex(machine)),
        "pe32plus": pe32plus,
        "timestamp": timestamp,
        "characteristics": characteristics,
        "is_dll": bool(characteristics & 0x2000),
        "sections": sections,
        "managed_cli": bool(len(dirs) > 14 and dirs[14][0]),
        "authenticode_slot": {"present": bool(sec_dir[0]), "offset": sec_dir[0], "bytes": sec_dir[1]},
        "overlay": {"offset": end_of_image, "bytes": max(0, overlay_end - end_of_image)},
    }


def version_strings(blob):
    """Read StringFileInfo values (UTF-16LE key\\0\\0value) without a resource parser."""
    out = {}
    for key in ("CompanyName", "FileDescription", "FileVersion", "ProductName", "ProductVersion", "OriginalFilename", "LegalCopyright"):
        k = key.encode("utf-16-le") + b"\0\0"
        i = blob.find(k)
        if i < 0:
            continue
        j = i + len(k)
        while j < len(blob) - 1 and blob[j:j + 2] == b"\0\0":
            j += 2
        end = blob.find(b"\0\0", j)
        while end > 0 and (end - j) % 2:
            end = blob.find(b"\0\0", end + 1)
        if end > j:
            val = blob[j:end].decode("utf-16-le", "replace").strip()
            # an empty value is followed by the next String header (binary lengths): reject control chars
            if 0 < len(val) < 200 and all(ord(ch) >= 0x20 for ch in val):
                out[key] = val
    return out


def magic_family(b):
    for fam in ("msi_ole", "cab", "sevenzip", "zip", "rar5", "rar4"):
        if b.startswith(SIG[fam]):
            return fam
    return "pe" if b.startswith(SIG["mz"]) else None


def read_vint(b, i):
    """RAR5 variable-length integer: 7 bits per byte, high bit = more."""
    val, shift = 0, 0
    while i < len(b):
        val |= (b[i] & 0x7F) << shift
        i += 1
        if not b[i - 1] & 0x80:
            return val, i
        shift += 7
    return None, i


def rar_info(head):
    """Is the archive's file list itself encrypted? (Then even listing needs the password.)"""
    if head.startswith(SIG["rar5"]):
        _, i = read_vint(head, 12)          # skip CRC32, read header size
        htype, _ = read_vint(head, i)
        return {"version": 5, "headers_encrypted": htype == 4}
    if head.startswith(SIG["rar4"]) and len(head) >= 12:
        htype, flags = head[9], struct.unpack_from("<H", head, 10)[0]
        return {"version": 4, "headers_encrypted": htype == 0x73 and bool(flags & 0x0080)}
    return None


def pe_resource_payloads(f, pe, limit=4096):
    """Walk the PE resource tree (type → name → language) and report entries of MIN_EMBEDDED bytes or more,
    with the container format their first bytes show. Some installers (DxO PhotoLab) keep the whole MSI and
    CAB as resources, so the overlay is empty and REA's PE readers stop at their size budget."""
    rsrc = next((s for s in pe["sections"] if s["name"] == ".rsrc"), None)
    if not rsrc or not rsrc["raw_size"]:
        return []
    base, va, end = rsrc["raw_offset"], rsrc["virtual_address"], rsrc["raw_offset"] + rsrc["raw_size"]
    found, seen = [], [0]

    def rd(off, n):
        if off < base or off + n > end:
            return b""
        f.seek(off)
        return f.read(n)

    def label(raw, level):
        if raw & 0x80000000:
            s = rd(base + (raw & 0x7FFFFFFF), 2)
            if len(s) < 2:
                return "?"
            n = struct.unpack("<H", s)[0]
            return rd(base + (raw & 0x7FFFFFFF) + 2, 2 * n).decode("utf-16-le", "replace")
        return RT_NAMES.get(raw, str(raw)) if level == 0 else str(raw)

    def walk(off, level, parts):
        hdr = rd(base + off, 16)
        if len(hdr) < 16:
            return
        count = sum(struct.unpack_from("<HH", hdr, 12))
        for k in range(count):
            seen[0] += 1
            if seen[0] > limit:
                return
            e = rd(base + off + 16 + 8 * k, 8)
            if len(e) < 8:
                return
            raw_name, ptr = struct.unpack("<II", e)
            name = label(raw_name, level)
            if ptr & 0x80000000 and level < 2:
                walk(ptr & 0x7FFFFFFF, level + 1, parts + [name])
            elif not ptr & 0x80000000:
                data = rd(base + ptr, 16)
                if len(data) < 16:
                    continue
                rva, size = struct.unpack_from("<II", data)
                if size < MIN_EMBEDDED:
                    continue
                off_file = rva - va + base
                fam = magic_family(rd(off_file, 8)) if base <= off_file < end else None
                rtype, rname = (parts + ["?", "?"])[:2]
                found.append({"resource": "\\".join([".rsrc", name, rtype, rname]), "bytes": size,
                              "offset": off_file, "container": fam or "unknown"})
    walk(0, 0, [])
    return found


def classify(path):
    path = Path(path)
    size = path.stat().st_size
    try:
        f = open(path, "rb")
    except OSError as error:
        # Windows Defender denies reads of quarantined files with EINVAL (Errno 22); report, never work around
        blocked = getattr(error, "errno", None) == 22 or getattr(error, "winerror", None) == 225
        return {"name": path.name, "bytes": size, "format": "unreadable",
                "findings": [{"kind": "blocked", "value": "antivirus" if blocked else "os-error",
                              "basis": str(error),
                              "meaning": "the OS refused to open it (antivirus detection): leave it alone and tell the owner"
                              if blocked else "could not be opened"}], "routes": [], "verified": False}
    with f:
        head = f.read(min(size, 1 << 16))
        pe = parse_pe(head, size)
        result = {"name": path.name, "bytes": size, "sha256": sha256_file(path), "format": "pe" if pe else "other"}
        findings, routes = [], []
        if not pe:
            for fam in ("sevenzip", "zip", "msi_ole", "cab"):
                if head.startswith(SIG[fam]):
                    result["format"] = fam
            rar = rar_info(head)
            if rar:
                result["format"] = "rar"
                result["rar"] = rar
                if rar["headers_encrypted"]:
                    findings.append({"kind": "container", "value": "rar-encrypted",
                                     "basis": f"RAR{rar['version']} archive with encrypted headers",
                                     "meaning": "even the file list needs the password: ask the owner for it; never guess or crack it"})
            if path.suffix.lower() == ".asar" and len(head) >= 16:
                result["format"] = "asar"
            return finalize(result, findings, routes, path)
        result["pe"] = pe
        names = [s["name"] for s in pe["sections"]]
        # resource section (for version info) — read at most 2 MiB of it
        rsrc = next((s for s in pe["sections"] if s["name"] == ".rsrc"), None)
        blob = b""
        if rsrc and rsrc["raw_size"]:
            f.seek(rsrc["raw_offset"])
            blob = f.read(min(rsrc["raw_size"], 2 << 20))
        result["version_info"] = version_strings(blob)
        ov = pe["overlay"]
        f.seek(ov["offset"])
        overlay_head = f.read(min(ov["bytes"], MAX_SCAN_BYTES))
        f.seek(0)
        front = f.read(2 << 20)     # Inno keeps "Inno Setup Setup Data" in its loader, not in the overlay
        embedded = pe_resource_payloads(f, pe)
        # whole-file signatures for Electron fuse need a streaming search on large binaries
        electron = stream_find(f, SIG["electron_fuse"], size)
    if any(n.upper().startswith("UPX") for n in names):
        findings.append({"kind": "packer", "value": "upx", "basis": "section names " + ",".join(names),
                         "meaning": "UPX-compressed: REA's PE readers may reject overlapping section bytes; unpack with `upx -d` on a COPY before deep inspection"})
    for fam, label in (("nsis", "NSIS installer"), ("inno", "Inno Setup installer"), ("inno_ldr", "Inno Setup installer")):
        if SIG[fam] in overlay_head or (fam == "inno_ldr" and SIG[fam] in head):
            findings.append({"kind": "installer", "value": fam.replace("_ldr", ""), "basis": f"{label} signature in overlay/header"})
            break
    else:
        if overlay_head.startswith(SIG["inno_zlb"]) and b"Inno Setup" in front:
            findings.append({"kind": "installer", "value": "inno", "basis": "Inno Setup loader string + zlb block at overlay start",
                             "meaning": "7-Zip cannot open Inno data; list it with `innoextract -l` (Capture One 21, FontLab 7 were built this way)"})
    for e in embedded:
        if e["container"] in ("msi_ole", "cab", "sevenzip", "zip", "pe"):
            findings.append({"kind": "embedded", "value": e["container"], "resource": e["resource"], "bytes": e["bytes"],
                             "basis": f"{e['bytes']} bytes of {e['container']} inside PE resource {e['resource']}"})
    for fam, label in (("sevenzip", "7z SFX"), ("zip", "ZIP SFX"), ("msi_ole", "embedded MSI/OLE"), ("cab", "embedded CAB")):
        if overlay_head.startswith(SIG[fam]) or (fam in ("sevenzip",) and SIG[fam] in overlay_head[:4096]):
            findings.append({"kind": "container", "value": fam, "basis": f"{label} signature at overlay start"})
    if SIG["wixburn"] in head:
        findings.append({"kind": "installer", "value": "wix-burn", "basis": ".wixburn section"})
    if SIG["squirrel"] in head + overlay_head:
        findings.append({"kind": "installer", "value": "squirrel", "basis": "SquirrelTemp marker"})
    if electron:
        findings.append({"kind": "runtime", "value": "electron", "basis": f"Electron fuse sentinel at offset {electron}"})
    if pe["managed_cli"]:
        findings.append({"kind": "runtime", "value": "dotnet", "basis": "CLI data directory present"})
    if not pe["authenticode_slot"]["present"]:
        findings.append({"kind": "signature", "value": "unsigned", "basis": "no security directory"})
    if ov["bytes"] > 1 << 20 and not any(x["kind"] in ("installer", "container", "embedded") for x in findings):
        findings.append({"kind": "overlay", "value": "unknown-payload", "basis": f"{ov['bytes']} bytes after the last section"})
    vi = " ".join(result["version_info"].values()).lower()
    if "creative cloud" in vi or "adobe installer" in vi:
        findings.append({"kind": "installer", "value": "bootstrapper", "basis": "version info names a downloader/setup stub"})
    return finalize(result, findings, routes, path)


def stream_find(f, needle, size, cap=512 << 20):
    f.seek(0)
    pos, tail = 0, b""
    while pos < min(size, cap):
        block = f.read(CHUNK * 8)
        if not block:
            break
        buf = tail + block
        i = buf.find(needle)
        if i >= 0:
            return pos - len(tail) + i
        tail = buf[-len(needle):]
        pos += len(block)
    return None


def finalize(result, findings, routes, path):
    kinds = {(x["kind"], x["value"]) for x in findings}
    fmt = result["format"]
    if ("installer", "nsis") in kinds:
        routes.append({"step": "unpack", "command": f"installer_triage.py unpack {path.name} --to <absent-dir> --authorized", "why": "NSIS payload ($PLUGINSDIR, app-*.7z) is invisible to REA until extracted"})
    elif ("installer", "inno") in kinds:
        routes.append({"step": "list", "command": f"innoextract -l {path.name}", "why": "file list of the Inno payload without extracting (feature evidence from names)"})
        routes.append({"step": "unpack", "command": f"installer_triage.py unpack {path.name} --to <absent-dir> --authorized", "why": "uses innoextract when present; 7-Zip cannot read Inno data"})
    elif ("container", "rar-encrypted") in kinds:
        routes.append({"step": "note", "why": "password-protected RAR: ask the owner for the password; do not guess, brute-force or use cracking tools"})
    elif any(k in ("container", "embedded") for k, _ in kinds):
        routes.append({"step": "unpack", "command": f"installer_triage.py unpack {path.name} --to <absent-dir> --authorized", "why": "self-extracting archive or payload stored in PE resources"})
    if fmt == "msi_ole":
        routes.append({"step": "list", "command": f"7z l {path.name}", "why": "MSI file table (REA has no MSI reader: inspect-artifact answers unsupported_target)"})
        routes.append({"step": "unpack", "command": f"installer_triage.py unpack {path.name} --to <absent-dir> --authorized", "why": "then `route` sends .NET assemblies to inspect-managed-artifact"})
    if any(k == "embedded" for k, _ in kinds) and result["bytes"] > 64 << 20:
        routes.append({"step": "note", "why": "REA inspect-pe-resources stops at 64 MiB per file (resource_constraint): extract the large resources first, then scan each"})
    if ("installer", "bootstrapper") in kinds or (fmt == "pe" and not findings and result["bytes"] < 8 << 20):
        routes.append({"step": "note", "why": "small signed setup stub: the product is downloaded at install time, so its features cannot be read from this file; analyse the installed program folder instead"})
    if ("runtime", "electron") in kinds:
        routes.append({"step": "rea", "command": ["rea", "inspect-electron-fuses", str(path), "--json"]})
        routes.append({"step": "rea", "command": ["rea", "analyze-javascript-application", "<resources/app.asar>", "--source-path", "<main>", "--source-path", "<preload>", "--json"], "why": "scope to main+preload first; a full minified bundle can exceed REA's 300 s per-file timeout"})
    if ("runtime", "dotnet") in kinds:
        routes.append({"step": "rea", "command": ["rea", "inspect-managed-artifact", str(path), "--json"]})
    if fmt == "pe" and not any(k == "packer" for k, _ in kinds):
        routes.append({"step": "rea", "command": ["rea", "inspect-pe-resources", str(path), "--json"]})
    if fmt == "asar":
        routes.append({"step": "rea", "command": ["rea", "analyze-javascript-application", str(path), "--json"]})
    if fmt in ("zip", "sevenzip"):
        routes.append({"step": "rea", "command": ["rea", "inspect-artifact", str(path), "--json"]})
    if fmt == "pe":
        routes.append({"step": "rea", "command": ["rea", "inspect-artifact", str(path), "--json"], "why": "evidence receipt + REA's own next probes"})
    result["findings"] = findings
    result["routes"] = routes
    result["analysis_executed"] = False
    result["verified"] = False
    return result


def adobe_package(root):
    """Adobe offline (HyperDrive) layout: products/driver.xml names the product and its SAP-code dependencies."""
    drv = Path(root) / "products" / "driver.xml"
    if not drv.is_file() or drv.stat().st_size > 1 << 20:
        return None
    text = drv.read_text(encoding="utf-8", errors="replace")
    pick = lambda tag, s: (re.search(rf"<{tag}>([^<]*)</{tag}>", s) or [None, None])[1]
    product = text.split("<Dependencies>")[0]
    deps = [{"sap": pick("SAPCode", d), "base_version": pick("BaseVersion", d)}
            for d in re.findall(r"<Dependency>(.*?)</Dependency>", text, flags=re.S)]
    langs = sorted({m for m in re.findall(r"-([a-z]{2}_[A-Z]{2})\.zip$", "\n".join(x.name for x in (Path(root) / "products").rglob("*.zip")), flags=re.M)})
    return {"kind": "adobe-offline-package", "product": pick("Name", product), "sap": pick("SAPCode", product),
            "version": pick("CodexVersion", product), "platform": pick("Platform", product), "dependencies": deps,
            "languages": langs, "route": "each products/<SAP>/*.zip is a plain ZIP: unpack the -mul and en_US ones, then `route`"}


def scan(target):
    p = Path(target)
    if p.is_dir():
        items = [x for x in sorted(p.iterdir()) if x.is_file() and x.suffix.lower() in (".exe", ".msi", ".dll", ".asar", ".zip", ".7z", ".rar")]
        res = {"status": "scanned", "target": str(p.resolve()), "artifacts": [classify(x) for x in items],
               "analysis_executed": False, "verified": False, "source": SOURCE}
        pkg = adobe_package(p)
        if pkg:
            res["package"] = pkg
        return res
    if not p.is_file():
        return {"status": "target_missing", "analysis_executed": False, "verified": False}
    return {"status": "scanned", "artifacts": [classify(p)], "analysis_executed": False, "verified": False, "source": SOURCE}


def seven_zip():
    env = os.environ.get("SEVEN_ZIP")
    if env and Path(env).is_file():
        return env
    for name in ("7z", "7za", "7zz"):
        hit = shutil.which(name)
        if hit:
            return hit
    for guess in (r"C:\Program Files\7-Zip\7z.exe", r"C:\Program Files (x86)\7-Zip\7z.exe"):
        if Path(guess).is_file():
            return guess
    return None


def unpack(target, dest, authorized, depth=2):
    src = Path(target)
    if not src.is_file():
        return {"status": "target_missing", "analysis_executed": False, "verified": False}
    if not authorized:
        return {"status": "authorization_required", "analysis_executed": False, "verified": False,
                "why": "extraction writes the target's files to disk; confirm you have the right to inspect it"}
    out = Path(dest)
    if out.exists() or out.is_symlink():
        return {"status": "unsafe_or_existing_output", "analysis_executed": False, "verified": False}
    if not out.parent.is_dir():
        return {"status": "output_parent_missing", "analysis_executed": False, "verified": False}
    tool = seven_zip()
    if not tool:
        return {"status": "seven_zip_missing", "install": "winget install 7zip.7zip | apt install 7zip | brew install sevenzip",
                "analysis_executed": False, "verified": False}
    info = classify(src)
    fam = next((x["value"] for x in info["findings"] if x["kind"] == "installer"), None)
    if any(x["value"] == "rar-encrypted" for x in info["findings"]):
        return {"status": "password_required", "analysis_executed": False, "verified": False,
                "why": "the archive's file list is encrypted; ask the owner for the password (never guess it)"}
    log = []
    if fam == "inno":
        inno = shutil.which("innoextract")
        if not inno:
            return {"status": "innoextract_missing", "install": "scoop install innoextract | apt install innoextract | brew install innoextract",
                    "analysis_executed": False, "verified": False}
        ok = run_tool([inno, "-s", "-d", str(out), str(src)], src, log)
    else:
        ok = extract(tool, src, out, "Nsis" if fam == "nsis" else None, log)
    if not ok:
        return {"status": "extraction_failed", "log": log, "analysis_executed": False, "verified": False}
    # second level: payload archives inside the installer ($PLUGINSDIR/app-64.7z, res.zip, *.nupkg) and
    # extension-less PE resources whose bytes are an MSI, CAB or 7z (DxO keeps its MSI as .rsrc/1033/BIN/5100)
    if depth > 1:
        for inner in sorted(out.rglob("*")):
            if not inner.is_file() or inner.stat().st_size == 0:
                continue
            nested = inner.suffix.lower() in (".7z", ".zip", ".nupkg", ".msi", ".cab")
            if not nested and inner.stat().st_size >= MIN_EMBEDDED and ".rsrc" in inner.parts:
                with open(inner, "rb") as h:
                    nested = magic_family(h.read(8)) in ("msi_ole", "cab", "sevenzip", "zip")
            target_dir = inner.with_name(inner.name + ".d")
            if nested and not target_dir.exists():
                extract(tool, inner, target_dir, None, log)
    manifest = []
    for f in sorted(out.rglob("*")):
        if f.is_file():
            manifest.append({"path": f.relative_to(out).as_posix(), "bytes": f.stat().st_size})
    return {"status": "extracted_not_executed", "target": src.name, "target_sha256": info["sha256"], "installer": fam,
            "output": str(out.resolve()), "files": len(manifest), "bytes": sum(m["bytes"] for m in manifest),
            "notable": notable(out), "log": log, "analysis_executed": False, "verified": False,
            "next": "run `installer_triage.py route <output>` and follow the REA commands it lists"}


def extract(tool, src, out, fmt, log):
    cmd = [tool, "x", "-y", "-bd", "-o" + str(out)]   # stdin is closed, so an encrypted archive fails instead of prompting
    if fmt:
        cmd.append("-t" + fmt)
    cmd.append(str(src))
    return run_tool(cmd, src, log)


def run_tool(cmd, src, log):
    try:
        proc = subprocess.run(cmd, capture_output=True, stdin=subprocess.DEVNULL, timeout=1800, check=False)
    except (OSError, subprocess.TimeoutExpired) as exc:
        log.append({"archive": src.name, "status": type(exc).__name__})
        return False
    log.append({"archive": src.name, "exit_code": proc.returncode})
    return proc.returncode == 0


def notable(root):
    root = Path(root)
    hits = {"asar": [], "electron_exe": [], "managed": [], "archives": [], "downloader_plugins": [], "languages": 0, "rtl": False}
    for f in root.rglob("*"):
        if not f.is_file():
            continue
        rel = f.relative_to(root).as_posix()
        low = rel.lower()
        if low.endswith(".asar"):
            hits["asar"].append(rel)
        elif low.endswith(".exe") and (f.parent / "resources").is_dir() and any((f.parent / "resources").glob("*.asar")):
            hits["electron_exe"].append(rel)
        elif low.endswith((".zip", ".7z", ".nupkg")):
            hits["archives"].append(rel)
        elif low.endswith(".dll") and ("download" in low or "bgworker" in low or "inetc" in low or "nsisdl" in low):
            hits["downloader_plugins"].append(rel)   # online installer: the product arrives at install time
        if "/locales/" in "/" + low or "/lang/" in "/" + low:
            hits["languages"] += 1
        if low.endswith((".rtl.css", ".rtl.html")) or "/ar." in low or low.endswith(("ar.pak", "ar-sa.json")):
            hits["rtl"] = True
    return hits


def read_asar(path):
    with open(path, "rb") as f:
        head = f.read(16)
        if len(head) < 16:
            raise ValueError("not an asar archive")
        size = struct.unpack_from("<I", head, 12)[0]
        if size <= 0 or size > MAX_ASAR_HEADER:
            raise ValueError("asar header size out of bounds")
        header = json.loads(f.read(size).decode("utf-8"))
        base = 8 + struct.unpack_from("<I", head, 4)[0]
    files = {}

    def walk(node, prefix):
        for name, val in node.get("files", {}).items():
            q = prefix + "/" + name
            if "files" in val:
                walk(val, q)
            else:
                files[q.lstrip("/")] = val
    walk(header, "")
    return files, base


def asar_entry(path, entry, limit=MAX_TEXT_ENTRY):
    files, base = read_asar(path)
    meta = files.get(entry.lstrip("/"))
    if not meta or meta.get("unpacked") or "offset" not in meta:
        return None
    size = int(meta.get("size", 0))
    with open(path, "rb") as f:
        f.seek(base + int(meta["offset"]))
        return f.read(min(size, limit))


def asar_list(path, entry=None):
    try:
        files, _ = read_asar(path)
    except (OSError, ValueError) as exc:
        return {"status": "invalid_asar", "error": str(exc)[:200], "analysis_executed": False, "verified": False}
    if entry:
        data = asar_entry(path, entry)
        if data is None:
            return {"status": "entry_missing", "entry": entry}
        text = data.decode("utf-8", "replace")
        return {"status": "entry", "entry": entry, "bytes": len(data), "text": text, "analysis_executed": False, "verified": False}
    biggest = sorted(files.items(), key=lambda kv: -int(kv[1].get("size", 0)))[:25]
    pkg = None
    raw = asar_entry(path, "package.json")
    if raw:
        try:
            j = json.loads(raw)
            pkg = {k: j.get(k) for k in ("name", "productName", "version", "main", "author") if j.get(k) is not None}
        except ValueError:
            pkg = None
    return {"status": "listed", "files": len(files), "bytes": sum(int(v.get("size", 0)) for v in files.values()),
            "package": pkg, "largest": [{"path": k, "bytes": int(v.get("size", 0))} for k, v in biggest],
            "renderers": sorted({k.split("/")[2] for k in files if k.startswith("dist/renderer/") and k.count("/") >= 3}),
            "analysis_executed": False, "verified": False}


def fingerprint(path):
    """Electron capability anchors in package.json + main + preload. Counts are evidence of code presence only."""
    try:
        files, _ = read_asar(path)
    except (OSError, ValueError) as exc:
        return {"status": "invalid_asar", "error": str(exc)[:200]}
    raw = asar_entry(path, "package.json") or b"{}"
    try:
        pkg = json.loads(raw)
    except ValueError:
        pkg = {}
    main = (pkg.get("main") or "index.js").lstrip("./")
    candidates = [main] + [k for k in files if k.endswith("preload.js")]
    text = b""
    for c in candidates:
        blob = asar_entry(path, c, MAX_FINGERPRINT_BYTES)
        if blob:
            text += blob + b"\n"
    s = text.decode("utf-8", "replace")
    features = {}
    for anchor, (fid, ar, en) in ELECTRON_ANCHORS.items():
        n = len(re.findall(r"\b" + re.escape(anchor) + r"\b", s, flags=re.I if anchor in ("offline", "sentry") else 0))
        if n:
            f = features.setdefault(fid, {"feature": fid, "ar": ar, "en": en, "anchors": {}})
            f["anchors"][anchor] = n
    assoc = []
    fa = pkg.get("packageFileAssociations") or pkg.get("fileAssociations") or (pkg.get("build") or {}).get("fileAssociations")
    if isinstance(fa, dict):
        fa = next(iter(fa.values()), [])
    for item in fa or []:
        if isinstance(item, dict):
            ext = item.get("ext") or item.get("A")
            if isinstance(ext, list):
                assoc += ext
            elif ext:
                assoc.append(ext)
    windows = sorted({k.split("/")[2] for k in files if k.startswith("dist/renderer/") and k.count("/") >= 3})
    pages = sorted({re.sub(r"\.(rtl|ltr)$", "", Path(k).stem.split("index.", 1)[-1]) for k in files
                    if k.endswith(".html") and "/renderer/" in k and "stats" not in k and "toc" not in k})
    rtl = any(k.endswith((".rtl.css", ".rtl.html")) for k in files)
    return {"status": "fingerprinted", "package": {k: pkg.get(k) for k in ("name", "version", "main") if pkg.get(k)},
            "scanned": candidates, "scanned_bytes": len(text), "features": sorted(features.values(), key=lambda x: x["feature"]),
            "file_associations": sorted(set(assoc)), "renderer_windows": windows, "renderer_pages": pages, "rtl_ui": rtl,
            "limitations": ["anchor counts show code presence in the bundle, not that a feature is reachable or enabled",
                            "minified aliases can hide APIs; absence of an anchor is not absence of the feature"],
            "analysis_executed": False, "verified": False}


def route(root):
    root = Path(root)
    if not root.is_dir():
        return {"status": "target_missing"}
    plan = []
    for f in sorted(root.rglob("*")):
        if not f.is_file():
            continue
        low = f.name.lower()
        if low.endswith(".asar"):
            fp = asar_list(f)
            main = (fp.get("package") or {}).get("main", "index.js")
            plan.append({"artifact": f.relative_to(root).as_posix(), "kind": "electron-asar",
                         "commands": [["installer_triage.py", "fingerprint", str(f)],
                                      ["rea", "analyze-javascript-application", str(f), "--source-path", main, "--json"],
                                      ["rea", "trace-application-feature", "<evidence.json>", "--seed", "<feature word>", "--json"]]})
        elif low.endswith(".exe") and f.stat().st_size > 1 << 20:
            c = classify(f)
            plan.append({"artifact": f.relative_to(root).as_posix(), "kind": "pe",
                         "findings": c["findings"], "commands": [r["command"] for r in c["routes"] if r["step"] == "rea"]})
        elif low.endswith(".dll"):
            with open(f, "rb") as h:
                head = h.read(1 << 16)
            pe = parse_pe(head, f.stat().st_size)
            if pe and pe["managed_cli"]:
                plan.append({"artifact": f.relative_to(root).as_posix(), "kind": "dotnet",
                             "commands": [["rea", "inspect-managed-members", str(f), "--json"]]})
        elif low.endswith(".msi"):
            plan.append({"artifact": f.relative_to(root).as_posix(), "kind": "msi",
                         "commands": [["7z", "l", str(f)], ["installer_triage.py", "unpack", str(f), "--to", "<absent-dir>", "--authorized"]]})
        elif low.endswith((".zip", ".nupkg")):
            plan.append({"artifact": f.relative_to(root).as_posix(), "kind": "archive",
                         "commands": [["rea", "inspect-artifact", str(f), "--json"]]})
        elif low.endswith((".db", ".sqlite", ".sqlite3")):
            plan.append({"artifact": f.relative_to(root).as_posix(), "kind": "sqlite",
                         "commands": [["rea", "inspect-sqlite-database", str(f), "--json"]]})
    return {"status": "routed", "root": str(root.resolve()), "artifacts": len(plan), "plan": plan[:200],
            "analysis_executed": False, "verified": False, "source": SOURCE}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="action", required=True)
    s = sub.add_parser("scan"); s.add_argument("target")
    u = sub.add_parser("unpack"); u.add_argument("target"); u.add_argument("--to", required=True); u.add_argument("--authorized", action="store_true")
    a = sub.add_parser("asar"); a.add_argument("target"); a.add_argument("entry", nargs="?")
    fp = sub.add_parser("fingerprint"); fp.add_argument("target")
    r = sub.add_parser("route"); r.add_argument("target")
    args = ap.parse_args()
    if args.action == "scan":
        res = scan(args.target)
    elif args.action == "unpack":
        res = unpack(args.target, args.to, args.authorized)
    elif args.action == "asar":
        res = asar_list(args.target, args.entry)
    elif args.action == "fingerprint":
        res = fingerprint(args.target)
    else:
        res = route(args.target)
    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(res, ensure_ascii=False, indent=2))
    return 0 if res.get("status") not in ("extraction_failed",) else 1


if __name__ == "__main__":
    sys.exit(main())
