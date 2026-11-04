"""software-investigation (REA v6.7.0) chunk 02: REA-131..REA-258 as real programs.

REA's deep-analysis commands need external engines that are NOT present in this checkout
(Ghidra/Hopper/IDA, jadx + an adb-authorised Android device, Frida, Rizin/GDB live debug,
macOS/Hopper, a .NET/CLI toolchain, pwntools). ``rea doctor`` here reports every provider
missing. Those cards are honest GAPS below.

For the cards whose *method* is a static binary/file measurement, this module does that method
for real on fixtures it builds inside the work folder, with installed open-source engines and the
repo's own KOSIF scripts:
  * the real ``rea`` CLI where it runs engine-free: ``rea inspect-with-objdump`` (GNU objdump
    provider) and the KOSIF ``rea_bridge.py run artifact`` path;
  * GNU objdump / readelf / nm / strings / file on a tiny ELF this module compiles with gcc;
  * the CPython ``marshal``/``importlib`` headers for .pyc; Shannon entropy in pure Python;
  * the repo's ``installer_triage.py`` (pure stdlib) on self-built PE / Electron-asar fixtures.
Every runner builds its own target (never third-party software), is static-only, returns
known-answer checks plus a negative control on the untreated input, and writes an output file.

No engine installed beyond the base image; no network; no secrets (fake tokens built at runtime).
"""
from __future__ import annotations

import hashlib
import json
import marshal
import math
import re
import struct
import subprocess
from importlib.util import MAGIC_NUMBER
from pathlib import Path

from _harness import card, check, fx

REPO = Path(__file__).resolve().parents[4]
SCRIPTS = REPO / ".claude/skills/kosif-superpowers/scripts"
TRIAGE = SCRIPTS / "installer_triage.py"
BRIDGE = SCRIPTS / "rea_bridge.py"

GAPS: dict = {}


# --------------------------------------------------------------------------- fixtures / helpers
_C_SRC = (
    '#include <stdio.h>\n'
    'int helper(int x){return x*3+1;}\n'
    'int main(){const char *s="MAGIC_TOKEN_ABC";printf("%s %d\\n",s,helper(7));return 0;}\n'
)


def _cc(wd: Path) -> Path:
    """Compile a tiny ELF (with a build-id note) to analyse statically. gcc is in the base image."""
    src = wd / "t.c"
    src.write_text(_C_SRC, encoding="utf-8")
    out = wd / "t.bin"
    fx.run(["gcc", "-O0", "-g", "-Wl,--build-id", str(src), "-o", str(out)], timeout=30)
    return out


def _so(wd: Path) -> Path:
    """Compile a shared object with one exported (GLOBAL) and one static (local) function."""
    src = wd / "lib.c"
    src.write_text("int exported_add(int a,int b){return a+b;}\n"
                   "static int hidden_impl(int x){return x+1;}\n"
                   "int exported_use(int x){return hidden_impl(x);}\n", encoding="utf-8")
    out = wd / "libt.so"
    fx.run(["gcc", "-shared", "-fPIC", "-O0", str(src), "-o", str(out)], timeout=30)
    return out


def _objdump_d(binary: Path) -> str:
    return fx.run(["objdump", "-d", str(binary)]).stdout


def _func_body(disasm: str, name: str) -> list:
    """Lines of the disassembly for function <name>, up to the next label."""
    lines = disasm.splitlines()
    out, inside = [], False
    for ln in lines:
        if re.match(r"^[0-9a-f]+ <%s>:" % re.escape(name), ln):
            inside = True
            continue
        if inside:
            if re.match(r"^[0-9a-f]+ <.+>:", ln):
                break
            if ln.strip():
                out.append(ln)
    return out


def _jw(path: Path, obj) -> Path:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=1), encoding="utf-8")
    return path


# =========================================================================== REAL RUNNERS
@card("REA-132")
def resolve_native_call_site(task, wd):
    """REA-132 resolve-native-call-targets: resolve one static native call site to its callee.
    objdump disassembly; the call in main resolves to <helper>, a data-load (lea) line does not."""
    binary = _cc(wd)
    body = _func_body(_objdump_d(binary), "main")
    call_lines = [ln for ln in body if re.search(r"\bcall\b", ln)]
    lea_lines = [ln for ln in body if re.search(r"\blea\b", ln)]
    targets = []
    for ln in call_lines:
        m = re.search(r"call\s+[0-9a-f]+\s*<([^>+]+)", ln)
        if m:
            targets.append(m.group(1))
    out = _jw(wd / "call_sites.json", {"function": "main", "call_sites": targets, "lea_count": len(lea_lines)})
    return [
        check("the call site in main resolves to callee <helper>", "helper" in targets, targets, "helper in list"),
        check("negative control: a data-load (lea) line carries no resolved call target",
              all("call" not in ln for ln in lea_lines) and bool(lea_lines), len(lea_lines), ">0 lea, 0 call"),
    ], [out]


@card("REA-133")
def search_strings_and_procedures(task, wd):
    """REA-133 search: search every analysed string or procedure name.
    strings(1) for literals + nm(1)/objdump symbols for procedure names; a known-absent token misses."""
    binary = _cc(wd)
    literals = fx.run(["strings", "-a", str(binary)]).stdout.splitlines()
    syms = fx.run(["nm", str(binary)]).stdout.splitlines()
    proc_names = {m.group(1) for m in (re.search(r"\s[Tt]\s(\S+)$", s) for s in syms) if m}
    hit_literal = any("MAGIC_TOKEN_ABC" in s for s in literals)
    hit_proc = "helper" in proc_names
    absent = any("ZZZ_NO_SUCH_TOKEN" in s for s in literals) or "ZZZ_NO_SUCH_TOKEN" in proc_names
    out = _jw(wd / "search.json", {"query_literal": "MAGIC_TOKEN_ABC", "literal_found": hit_literal,
                                   "query_procedure": "helper", "procedure_found": hit_proc,
                                   "procedures": sorted(proc_names)})
    return [
        check("the string literal MAGIC_TOKEN_ABC is found", hit_literal, hit_literal, True),
        check("the procedure name 'helper' is found in the symbol table", hit_proc, hit_proc, True),
        check("negative control: an absent token ZZZ_NO_SUCH_TOKEN is not matched", not absent, absent, False),
    ], [out]


@card("REA-135")
def search_bytes_masked(task, wd):
    """REA-135 search-bytes: find masked byte patterns. 'M A ?? I C' matches MAGIC in .rodata;
    an all-literal pattern that is not present returns zero hits (negative control)."""
    binary = _cc(wd)
    data = binary.read_bytes()

    def masked_find(pattern):
        toks = pattern.split()
        plen = len(toks)
        want = [(None if t == "??" else int(t, 16)) for t in toks]
        hits = []
        for i in range(len(data) - plen + 1):
            if all(w is None or data[i + k] == w for k, w in enumerate(want)):
                hits.append(i)
        return hits

    masked = masked_find("4d 41 ?? 49 43")      # M A ?? I C  -> MAGIC
    absent = masked_find("de ad be ef ca fe")   # not present
    ok_masked = len(masked) >= 1 and data[masked[0]:masked[0] + 5] == b"MAGIC"
    out = _jw(wd / "byte_hits.json", {"pattern": "4d 41 ?? 49 43", "offsets": masked[:8],
                                      "absent_pattern": "de ad be ef ca fe", "absent_hits": len(absent)})
    return [
        check("masked pattern M A ?? I C matches MAGIC at >=1 offset", ok_masked, len(masked), ">=1"),
        check("negative control: an absent exact pattern returns zero hits", len(absent) == 0, len(absent), 0),
    ], [out]


@card("REA-153")
def xrefs_to_address(task, wd):
    """REA-153 xrefs: list bounded references to an analysed address.
    objdump shows every call targeting <helper>; a never-called local symbol has no callers."""
    binary = _cc(wd)
    disasm = _objdump_d(binary)
    callers_helper = [ln.strip() for ln in disasm.splitlines() if re.search(r"call\s+[0-9a-f]+\s*<helper>", ln)]
    callers_main = [ln.strip() for ln in disasm.splitlines() if re.search(r"call\s+[0-9a-f]+\s*<main>", ln)]
    out = _jw(wd / "xrefs.json", {"symbol": "helper", "xrefs": callers_helper,
                                  "symbol_main": "main", "xrefs_main": callers_main})
    return [
        check("at least one call-site references <helper>", len(callers_helper) >= 1, len(callers_helper), ">=1"),
        check("negative control: <main> has no in-binary callers", len(callers_main) == 0, len(callers_main), 0),
    ], [out]


@card("REA-192")
def binary_overview(task, wd):
    """REA-192 binary_overview: overview of a native binary, run through the real engine-free
    `rea inspect-with-objdump` (GNU objdump provider). The Evidence digest must match the file."""
    binary = _cc(wd)
    art = wd / "overview.json"
    done = fx.run(["rea", "inspect-with-objdump", str(binary), "file_headers", "--json"], timeout=30)
    ev = json.loads(done.stdout)
    art.write_text(json.dumps(ev, ensure_ascii=False, indent=1), encoding="utf-8")
    want_sha = hashlib.sha256(binary.read_bytes()).hexdigest()
    got_sha = ev.get("subject", {}).get("digest", {}).get("sha256")
    provider = ev.get("provider", {}).get("id")
    ftype = fx.run(["file", str(binary)]).stdout
    return [
        check("rea returned Evidence whose subject digest == the binary's sha256", got_sha == want_sha, got_sha, want_sha),
        check("the overview came from the GNU objdump provider", provider == "gnu.objdump", provider, "gnu.objdump"),
        check("negative control: the compiled fixture is a real ELF (not empty/text)", "ELF" in ftype, ftype.strip()[:40], "ELF ..."),
    ], [art]


@card("REA-246")
def byte_entropy(task, wd):
    """REA-246 inspect_byte_entropy: Shannon byte-entropy profile.
    A zero-filled block measures ~0 bits; a pseudo-random block measures near 8 bits/byte."""
    import os
    low = bytes(4096)                              # all zeros -> entropy 0
    high = os.urandom(4096)                        # ~8 bits/byte
    (wd / "low.bin").write_bytes(low)
    (wd / "high.bin").write_bytes(high)

    def entropy(buf):
        if not buf:
            return 0.0
        counts = [0] * 256
        for b in buf:
            counts[b] += 1
        n = len(buf)
        return -sum((c / n) * math.log2(c / n) for c in counts if c)

    e_low, e_high = entropy(low), entropy(high)
    out = _jw(wd / "entropy.json", {"zero_block_bits": round(e_low, 4), "random_block_bits": round(e_high, 4)})
    return [
        check("a zero-filled block has entropy ~0 bits/byte", e_low < 0.01, round(e_low, 4), "<0.01"),
        check("a random block has entropy > 7.8 bits/byte", e_high > 7.8, round(e_high, 4), ">7.8"),
        check("negative control: the two measures are not equal (method separates them)", abs(e_high - e_low) > 7.0,
              round(e_high - e_low, 4), ">7.0"),
    ], [out]


@card("REA-248")
def elf_notes(task, wd):
    """REA-248 inspect_elf_notes: GNU build-id and ABI-tag notes. readelf -n on our fixture
    (linked with --build-id) shows a build-id; a raw data file has no ELF notes."""
    binary = _cc(wd)
    notes = fx.run(["readelf", "-n", str(binary)]).stdout
    m = re.search(r"Build ID:\s*([0-9a-f]+)", notes)
    build_id = m.group(1) if m else None
    has_abi = "NT_GNU_ABI_TAG" in notes or "ABI: " in notes
    raw = wd / "raw.dat"
    raw.write_bytes(b"not an elf" * 100)
    raw_has = subprocess.run(["readelf", "-n", str(raw)], capture_output=True, text=True).returncode == 0 \
        and "Build ID" in subprocess.run(["readelf", "-n", str(raw)], capture_output=True, text=True).stdout
    out = _jw(wd / "elf_notes.json", {"build_id": build_id, "has_abi_tag": has_abi})
    return [
        check("the ELF carries a GNU build-id note", bool(build_id) and len(build_id) >= 16, build_id, "hex >=16 chars"),
        check("the ELF carries an ABI-tag note", has_abi, has_abi, True),
        check("negative control: a raw data file exposes no build-id note", not raw_has, raw_has, False),
    ], [out]


@card("REA-253")
def native_exports(task, wd):
    """REA-253 inspect_native_exports: the ELF export (dynamic symbol) table.
    readelf --dyn-syms lists GLOBAL FUNC exports; a static function is not exported."""
    so = _so(wd)
    dyn = fx.run(["readelf", "--dyn-syms", str(so)]).stdout
    exported = set(re.findall(r"GLOBAL\s+DEFAULT\s+\d+\s+(\w+)", dyn))
    out = _jw(wd / "exports.json", {"exports": sorted(exported)})
    return [
        check("exported_add is in the dynamic export table", "exported_add" in exported, "exported_add" in exported, True),
        check("exported_use is in the dynamic export table", "exported_use" in exported, "exported_use" in exported, True),
        check("negative control: the static function hidden_impl is NOT exported",
              "hidden_impl" not in exported, "hidden_impl" in exported, False),
    ], [out]


@card("REA-255")
def python_pyc(task, wd):
    """REA-255 inspect_python_pyc: CPython .pyc header and code objects, without executing it.
    Parse the 16-byte header (magic/flags/fields) and marshal the code object; read its co_consts."""
    src = wd / "mod.py"
    src.write_text("K = 1337\n\ndef f(x):\n    return x + K\n", encoding="utf-8")
    code = compile(src.read_text(), "mod.py", "exec")
    blob = marshal.dumps(code)
    pyc = wd / "mod.pyc"
    pyc.write_bytes(MAGIC_NUMBER + b"\x00\x00\x00\x00" + b"\x00" * 8 + blob)

    raw = pyc.read_bytes()
    magic = raw[:4]
    body = marshal.loads(raw[16:])            # parse, never exec
    consts = body.co_consts
    has_k = 1337 in consts
    names = set(body.co_names) | {c.co_name for c in consts if hasattr(c, "co_name")}
    out = _jw(wd / "pyc.json", {"magic": magic.hex(), "magic_matches_runtime": magic == MAGIC_NUMBER,
                                "co_names": sorted(body.co_names), "nested_fns": sorted(n for n in names if n == "f"),
                                "const_1337_present": has_k})
    return [
        check("the .pyc magic matches this CPython's marshal magic", magic == MAGIC_NUMBER, magic.hex(), MAGIC_NUMBER.hex()),
        check("the marshalled code object exposes the constant 1337", has_k, has_k, True),
        check("the nested function 'f' is recovered from the code objects", "f" in names, "f" in names, True),
        check("negative control: an unrelated constant 9999 is absent", 9999 not in consts, 9999 in consts, False),
    ], [out]


# --------------------------------------------------------------- KOSIF installer-triage (REA 236-241)
@card("REA-236")
def installer_scan(task, wd):
    """REA-236 installer_triage scan: identify an installer/PE without executing it.
    A self-built unsigned PE is classified format=pe with an 'unsigned' finding; an asar is not PE."""
    pe = _build_fake_pe(wd / "setup.exe")
    res = json.loads(fx.run(["python3", "-I", str(TRIAGE), "scan", str(pe)]).stdout)
    art = res["artifacts"][0]
    findings = {f["value"] for f in art.get("findings", [])}
    asar = _build_asar(wd / "app.asar")
    res2 = json.loads(fx.run(["python3", "-I", str(TRIAGE), "scan", str(asar)]).stdout)
    out = _jw(wd / "scan.json", {"pe": {"format": art["format"], "findings": sorted(findings),
                                        "signed": art["pe"]["authenticode_slot"]["present"]},
                                 "asar_format": res2["artifacts"][0]["format"]})
    return [
        check("the self-built installer is classified as a PE", art["format"] == "pe", art["format"], "pe"),
        check("its unsigned state is reported (no Authenticode slot)",
              "unsigned" in findings and not art["pe"]["authenticode_slot"]["present"], sorted(findings), "unsigned"),
        check("negative control: an Electron asar is NOT classified as a PE",
              res2["artifacts"][0]["format"] != "pe", res2["artifacts"][0]["format"], "asar"),
    ], [out]


@card("REA-238")
def installer_asar(task, wd):
    """REA-238 installer_triage asar: list an Electron archive and read package.json, without executing it."""
    asar = _build_asar(wd / "app.asar")
    res = json.loads(fx.run(["python3", "-I", str(TRIAGE), "asar", str(asar)]).stdout)
    pkg = res.get("package") or {}
    out = _jw(wd / "asar_list.json", res)
    return [
        check("the asar lists its two packaged files", res.get("files") == 2, res.get("files"), 2),
        check("package.json is parsed: name == demo", pkg.get("name") == "demo", pkg.get("name"), "demo"),
        check("the declared main is main.js", pkg.get("main") == "main.js", pkg.get("main"), "main.js"),
        check("negative control: a truncated header is rejected as invalid",
              json.loads(fx.run(["python3", "-I", str(TRIAGE), "asar", str(_bad_asar(wd / "bad.asar"))]).stdout)
              .get("status") == "invalid_asar", True, "invalid_asar"),
    ], [out]


@card("REA-239")
def installer_fingerprint(task, wd):
    """REA-239 installer_triage fingerprint: count Electron capability anchors in the main bundle."""
    asar = _build_asar(wd / "app.asar")
    res = json.loads(fx.run(["python3", "-I", str(TRIAGE), "fingerprint", str(asar)]).stdout)
    feats = {f["feature"] for f in res.get("features", [])}
    out = _jw(wd / "fingerprint.json", res)
    empty = _build_asar(wd / "empty.asar", main_js=b"module.exports={};\n")
    res2 = json.loads(fx.run(["python3", "-I", str(TRIAGE), "fingerprint", str(empty)]).stdout)
    return [
        check("screen-capture capability detected (desktopCapturer anchor)", "screen-capture" in feats, sorted(feats), "has screen-capture"),
        check("auto-update capability detected (autoUpdater anchor)", "auto-update" in feats, sorted(feats), "has auto-update"),
        check("notifications capability detected (Notification anchor)", "notifications" in feats, sorted(feats), "has notifications"),
        check("negative control: a bundle with no anchors yields zero features",
              len(res2.get("features", [])) == 0, len(res2.get("features", [])), 0),
    ], [out]


@card("REA-240")
def installer_route(task, wd):
    """REA-240 installer_triage route: map each unpacked artifact to the REA command that fits it."""
    unp = wd / "unpacked"
    unp.mkdir()
    _build_asar(unp / "app.asar")
    res = json.loads(fx.run(["python3", "-I", str(TRIAGE), "route", str(unp)]).stdout)
    plan = res.get("plan", [])
    asar_plan = [p for p in plan if p.get("kind") == "electron-asar"]
    cmds = [" ".join(map(str, c)) for p in asar_plan for c in p.get("commands", [])]
    empty = wd / "empty_dir"
    empty.mkdir()
    res2 = json.loads(fx.run(["python3", "-I", str(TRIAGE), "route", str(empty)]).stdout)
    out = _jw(wd / "route.json", res)
    return [
        check("the asar is routed as an electron-asar artifact", len(asar_plan) == 1, len(asar_plan), 1),
        check("the route includes rea analyze-javascript-application",
              any("analyze-javascript-application" in c for c in cmds), True, "present"),
        check("negative control: an empty directory produces no routing plan",
              len(res2.get("plan", [])) == 0, len(res2.get("plan", [])), 0),
    ], [out]


@card("REA-241")
def rea_bridge_run(task, wd):
    """REA-241 rea_bridge.py run: drive the real REA CLI through the KOSIF bridge (no cmd.exe shell).
    `run artifact` executes engine-free and writes Evidence whose digest matches the target; a
    missing target fails closed."""
    binary = _cc(wd)
    out_ev = wd / "bridge_artifact.json"
    done = fx.run(["python3", "-I", str(BRIDGE), "run", "artifact", str(binary),
                   "--authorized", "--output", str(out_ev)], timeout=60)
    res = json.loads(done.stdout)
    ev = json.loads(out_ev.read_text()) if out_ev.exists() else {}
    want_sha = hashlib.sha256(binary.read_bytes()).hexdigest()
    got_sha = ev.get("subject", {}).get("digest", {}).get("sha256")
    missing = subprocess.run(["python3", "-I", str(BRIDGE), "run", "artifact", str(wd / "nope.bin"),
                              "--authorized", "--output", str(wd / "none.json")],
                             capture_output=True, text=True)
    try:
        miss_status = json.loads(missing.stdout).get("status")
    except ValueError:
        miss_status = "error"
    status_log = _jw(wd / "bridge_status.json", {"status": res.get("status"), "exit_code": res.get("exit_code"),
                                                 "result_sha256": res.get("result_sha256"),
                                                 "missing_target_status": miss_status})
    return [
        check("the bridge ran REA and reported executed_not_verified",
              res.get("status") == "executed_not_verified", res.get("status"), "executed_not_verified"),
        check("REA exited 0 through the bridge", res.get("exit_code") == 0, res.get("exit_code"), 0),
        check("the Evidence subject digest matches the analysed binary", got_sha == want_sha, got_sha, want_sha),
        check("negative control: a missing target does NOT report executed_not_verified (fails closed)",
              miss_status != "executed_not_verified", miss_status, "not executed_not_verified"),
    ], [out_ev, status_log]


# --------------------------------------------------------------- fixture builders for triage cards
def _build_fake_pe(path: Path) -> Path:
    """A minimal unsigned PE32+ stub (MZ + PE\\0\\0, no security directory). Never executed."""
    mz = bytearray(0x40)
    mz[0:2] = b"MZ"
    struct.pack_into("<I", mz, 0x3c, 0x40)                 # e_lfanew -> 0x40
    coff = struct.pack("<HHIIIHH", 0x8664, 0, 0, 0, 0, 0xF0, 0x22)
    opt = bytearray(0xF0)
    struct.pack_into("<H", opt, 0, 0x20b)                  # PE32+ magic
    data = bytes(mz) + b"PE\0\0" + coff + bytes(opt)
    data += b"ProductVersion\x001.2.3\x00" + b"\0" * 1024
    path.write_bytes(data)
    return path


def _asar_bytes(files: dict, blobs: dict) -> bytes:
    content = b""
    hdr = {"files": {}}
    for name, blob in blobs.items():
        hdr["files"][name] = {"size": len(blob), "offset": str(len(content))}
        content += blob
    j = json.dumps(hdr).encode()
    pad = (-len(j)) % 4
    head = struct.pack("<4I", 4, 8 + len(j) + pad, 4 + len(j) + pad, len(j))
    return head + j + b"\0" * pad + content


def _build_asar(path: Path, main_js: bytes = None) -> Path:
    if main_js is None:
        main_js = (b"const {app,desktopCapturer}=require('electron');"
                   b"require('child_process');autoUpdater.checkForUpdates();new Notification('x');")
    pkg = json.dumps({"name": "demo", "version": "1.0.0", "main": "main.js"}).encode()
    path.write_bytes(_asar_bytes(None, {"package.json": pkg, "main.js": main_js}))
    return path


def _bad_asar(path: Path) -> Path:
    path.write_bytes(b"\x04\x00\x00")                      # < 16 bytes -> not an asar
    return path


# =========================================================================== HONEST GAPS
# Every card below needs an engine / platform / service this checkout does not have.
# ``rea doctor`` here reports Ghidra, Hopper, IDA, jadx, Kuna, Frida, Rizin and pwntools all missing,
# and there is no adb-authorised Android device, no macOS host, no .NET/CLI toolchain and no network.
_ANDROID = "needs an adb-authorised Android device and/or a jadx-headless-mcp 0.7.1 JAR (engine:android); none present"
_GHIDRA = "needs a deep-analysis provider (Ghidra/Hopper/IDA) for the native analysis graph; rea doctor reports none"
_WAKARU = "needs the wakaru JavaScript-application provider plus a captured Application Graph Evidence JSON; not available"
_MACOS = "macOS/Hopper Mach-O target (os:macos); this host is Linux with no Hopper"
_FRIDA = "needs a live Frida session attached to a running process (engine:frida); dynamic, not static, and absent"
_RIZIN = "needs a live Rizin/GDB debug session (engine:rizin) attached to a running inferior; absent"
_MCP = "an MCP tool that only runs inside a live REA stdio server bound to an analysis provider (Ghidra); no engine here"
_MANAGED = "needs a built .NET/CLI (PE/CLI) assembly and a managed-metadata reader; no .NET toolchain in this image"
_PROMPT = "an MCP prompt: a template invoked by a connected LLM client against a live REA server, not a runnable program"
_SKILL = "a documentation skill: its method is 'read SKILL.md and apply judgement', with no deterministic measurable output"
_SELFMGMT = "REA self-management (installs/removes/updates agent config or needs the network); not an analysis with output"

GAPS.update({
    "REA-131": _ANDROID,
    "REA-134": _ANDROID,
    "REA-137": _ANDROID,
    "REA-138": _ANDROID,
    "REA-139": _ANDROID,
    "REA-141": _ANDROID,
    "REA-150": _ANDROID,
    "REA-136": _SELFMGMT,
    "REA-149": _SELFMGMT,
    "REA-151": _SELFMGMT,
    "REA-140": _GHIDRA + " (reliable data-literal xrefs need the decompiler graph; call xrefs are covered by REA-153)",
    "REA-142": _WAKARU,
    "REA-143": _MACOS,
    "REA-144": _WAKARU,
    "REA-145": _MACOS,
    "REA-146": _GHIDRA + " (bounded def-use needs the decompiler's data-flow; call deps alone would under-serve the card)",
    "REA-147": _WAKARU,
    "REA-148": _WAKARU,
    "REA-152": _MANAGED,
    "REA-237": "installer_triage unpack needs a 7-Zip binary (7z/7za/7zz); only zip/unzip are present in this image",
})
# REA MCP tools 154..229, 246..257 (minus the engine-free ones implemented above)
for _n in list(range(154, 230)) + list(range(246, 258)):
    _k = "REA-%d" % _n
    if _k in {"REA-192", "REA-246", "REA-248", "REA-253", "REA-255"}:
        continue  # implemented above with an installed open-source equivalent
    GAPS.setdefault(_k, _MCP)
# refine the MCP gaps that name a specific engine
for _n in range(196, 202):
    GAPS["REA-%d" % _n] = _FRIDA
for _n in range(202, 210):
    GAPS["REA-%d" % _n] = _RIZIN
# MCP prompts 230..235
for _n in range(230, 236):
    GAPS["REA-%d" % _n] = _PROMPT
# REA upstream agent skills (docs) 242..245 and 258
for _n in (242, 243, 244, 245, 258):
    GAPS["REA-%d" % _n] = _SKILL
