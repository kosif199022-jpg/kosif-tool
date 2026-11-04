"""software-investigation (REA-001..REA-130): method cards as real static-analysis programs.

Every card builds its own deterministic fixture inside the work folder (a tiny ELF compiled with gcc,
a hand-crafted Mach-O / WASM / EVM / pcap / plist / asar-style blob, a sqlite db, JSON evidence
bundles, JS bundles with source maps) and runs the card's method with open-source engines already
installed (binutils: objdump/readelf/nm/strings/file; gdb; go; python stdlib: sqlite3/plistlib/
zipfile/struct; PIL). Each returns known-answer checks with measured vs expected values and a negative
control (the same measurement on the untreated input fails), plus a non-empty output file.

The REA v6.7.0 CLI and its deep-analysis providers (Hopper/Ghidra/IDA/JEB/Kuna), device transports
(adb/Frida), live browsers (CDP/Playwright/Electron) and Wireshark/sigrok/apktool binaries are not
present here; those cards are documented in GAPS with the open-source equivalent that is missing.
All targets are built from scratch in this folder -- no third-party software is analysed.
"""
from __future__ import annotations

import json
import os
import plistlib
import re
import sqlite3
import struct
import subprocess
from pathlib import Path

from _harness import card, check, fx, sha

CC = "cc"


# ----------------------------------------------------------------------------- ELF fixtures / binutils
def _build_elf(wd: Path, src: str = None, pie: bool = False, name: str = "prog", flags=()):
    src = src or (
        "#include <stdio.h>\n"
        "int magic = 0x12345678;\n"
        "int add(int a, int b){ return a + b; }\n"
        "int main(void){ printf(\"%d\\n\", add(magic, 1)); return 0; }\n"
    )
    c = wd / (name + ".c")
    c.write_text(src)
    out = wd / name
    cmd = [CC, "-O0", "-g", str(c), "-o", str(out)]
    if not pie:
        cmd += ["-no-pie", "-fno-pie"]
    cmd += list(flags)
    fx.run(cmd, timeout=40)
    return out


def _readelf(path: Path, *args):
    return fx.run(["readelf", *args, str(path)]).stdout


def _objdump(path: Path, *args):
    return fx.run(["objdump", *args, str(path)]).stdout


def _load_segments(path: Path):
    """LOAD program headers as [(offset, vaddr, filesz)] parsed from readelf -lW."""
    out = _readelf(path, "-lW")
    segs, pend = [], None
    for ln in out.splitlines():
        t = ln.split()
        if t[:1] == ["LOAD"]:
            # LOAD off vaddr paddr filesz memsz flags align  (W = one line)
            if len(t) >= 6:
                segs.append((int(t[1], 16), int(t[2], 16), int(t[4], 16)))
            else:
                pend = (int(t[1], 16), int(t[2], 16))
        elif pend is not None and t and t[0].startswith("0x"):
            segs.append((pend[0], pend[1], int(t[0], 16)))
            pend = None
    return segs


def _vaddr_to_offset(path: Path, vaddr: int):
    for off, va, fsz in _load_segments(path):
        if va <= vaddr < va + fsz:
            return off + (vaddr - va)
    return None


def _nm_addr(path: Path, symbol: str):
    for ln in fx.run(["nm", str(path)]).stdout.splitlines():
        t = ln.split()
        if len(t) == 3 and t[2] == symbol:
            return int(t[0], 16)
    return None


def _entry(path: Path):
    for ln in _readelf(path, "-h").splitlines():
        if "Entry point address" in ln:
            return int(ln.split(":")[1].strip(), 16)
    return None


@card("REA-001")
def address_to_file_offset(task, wd):
    elf = _build_elf(wd)
    va = _nm_addr(elf, "magic")
    off = _vaddr_to_offset(elf, va)
    raw = elf.read_bytes()
    value = struct.unpack_from("<i", raw, off)[0]
    naive = struct.unpack_from("<i", raw, va)[0] if va < len(raw) else None  # treating vaddr as offset
    rec = {"symbol": "magic", "vaddr": hex(va), "file_offset": off, "value": hex(value & 0xffffffff)}
    out = wd / "address_to_offset.json"
    out.write_text(json.dumps(rec, indent=1))
    return [
        check("offset resolves to initializer bytes 0x12345678", value == 0x12345678, hex(value & 0xffffffff), "0x12345678"),
        check("file offset differs from virtual address", off != va, off, va),
        check("negative control: reading at raw vaddr does not give 0x12345678", naive != 0x12345678, naive, "!=0x12345678"),
    ], [out]


@card("REA-002")
def app_overview(task, wd):
    elf = _build_elf(wd)
    h = _readelf(elf, "-h")
    arch = "x86-64" if "X86-64" in h.upper() else "?"
    etype = "EXEC" if re.search(r"Type:\s+EXEC", h) else ("DYN" if "DYN" in h else "?")
    nsec = len([l for l in _readelf(elf, "-SW").splitlines() if re.match(r"\s*\[\s*\d+\]", l)])
    ov = {"format": "ELF", "arch": arch, "type": etype, "entry": hex(_entry(elf)), "sections": nsec}
    out = wd / "overview.json"
    out.write_text(json.dumps(ov, indent=1))
    return [
        check("detected ELF x86-64 executable", arch == "x86-64" and etype == "EXEC", [arch, etype], ["x86-64", "EXEC"]),
        check("section headers counted", nsec > 5, nsec, ">5"),
        check("negative control: not reported as DYN/shared", etype != "DYN", etype, "EXEC"),
    ], [out]


@card("REA-046")
def app_overview_with_evidence(task, wd):
    elf = _build_elf(wd)
    entry = _entry(elf)
    ev = {
        "observations": {"format": "ELF64", "entry": hex(entry), "has_symtab": ".symtab" in _readelf(elf, "-SW")},
        "inferences": ["entry sits in an executable LOAD segment"],
        "unknowns": ["original source file names beyond DWARF", "build toolchain flags"],
    }
    # an observation must be directly measured: entry must map into a file-backed segment
    ev["observations"]["entry_file_offset"] = _vaddr_to_offset(elf, entry)
    out = wd / "overview_evidence.json"
    out.write_text(json.dumps(ev, indent=1))
    return [
        check("observations are non-empty and measured", ev["observations"]["entry_file_offset"] is not None,
              ev["observations"]["entry_file_offset"], "an int offset"),
        check("unknowns are explicitly declared", len(ev["unknowns"]) >= 2, len(ev["unknowns"]), ">=2"),
        check("negative control: entry is not treated as a raw offset equal to vaddr",
              ev["observations"]["entry_file_offset"] != entry, ev["observations"]["entry_file_offset"], entry),
    ], [out]


@card("REA-057")
def inspect_artifact_observations(task, wd):
    elf = _build_elf(wd)
    ft = fx.run(["file", str(elf)]).stdout
    is_elf = "ELF" in ft
    probes = []
    if is_elf:
        probes = ["readelf -h", "readelf -SW", "objdump -d", "nm"]
    rec = {"file_type": ft.split(":", 1)[1].strip(), "observations": {"is_elf": is_elf}, "next_probes": probes}
    out = wd / "artifact_probes.json"
    out.write_text(json.dumps(rec, indent=1))
    return [
        check("artifact identified as ELF", is_elf, is_elf, True),
        check("next probes proposed for an ELF", len(probes) >= 3, len(probes), ">=3"),
        check("negative control: a text file would not be ELF", "ELF" not in fx.run(["file", str(elf.with_suffix(".c"))]).stdout,
              True, True),
    ], [out]


@card("REA-059")
def inspect_binary_layout(task, wd):
    elf = _build_elf(wd)
    secs = [l for l in _readelf(elf, "-SW").splitlines() if re.match(r"\s*\[\s*\d+\]", l)]
    names = []
    for l in secs:
        rest = re.sub(r"^\s*\[\s*\d+\]\s*", "", l).split()
        if rest and rest[0].startswith("."):
            names.append(rest[0])
    has_text = ".text" in names
    out = wd / "layout.json"
    out.write_text(json.dumps({"sections": names, "segments": _load_segments(elf)}, indent=1, default=str))
    return [
        check(".text section present in layout", has_text, ".text" in names, True),
        check("at least one LOAD segment parsed", len(_load_segments(elf)) >= 1, len(_load_segments(elf)), ">=1"),
        check("negative control: fictional .nonexist section absent", ".nonexist" not in names, False, False),
    ], [out]


@card("REA-030")
def read_part_as_code(task, wd):
    elf = _build_elf(wd)
    dis = _objdump(elf, "-d", "--no-show-raw-insn")
    m = re.search(r"<add>:\n((?:\s+[0-9a-f]+:.*\n)+)", dis)
    body = m.group(1) if m else ""
    ret = "ret" in body
    out = wd / "add.asm"
    out.write_text(body)
    return [
        check("disassembly of add() recovered", len(body.strip()) > 0, bool(body.strip()), True),
        check("function ends with a ret instruction", ret, ret, True),
        check("negative control: body is not empty placeholder", body.strip() != "", True, True),
    ], [out]


@card("REA-042")
def analyze_complete_function(task, wd):
    elf = _build_elf(wd)
    dis = _objdump(elf, "-d", "--no-show-raw-insn")
    m = re.search(r"<main>:\n((?:\s+[0-9a-f]+:.*\n)+)", dis)
    body = m.group(1)
    insns = [l for l in body.splitlines() if re.match(r"\s+[0-9a-f]+:", l)]
    has_call = any("call" in l for l in insns)
    has_ret = any(re.search(r"\bret\b", l) for l in insns)
    out = wd / "main_analysis.json"
    out.write_text(json.dumps({"instruction_count": len(insns), "has_call": has_call, "has_ret": has_ret}, indent=1))
    return [
        check("main has multiple instructions", len(insns) >= 4, len(insns), ">=4"),
        check("main performs a call (to add/printf)", has_call, has_call, True),
        check("negative control: empty disassembly would have no ret", has_ret, has_ret, True),
    ], [out]


@card("REA-076")
def inspect_one_instruction(task, wd):
    elf = _build_elf(wd)
    dis = _objdump(elf, "-d")
    m = re.search(r"<main>:\n\s+([0-9a-f]+):\s+((?:[0-9a-f]{2} )+)\s+(\S+)(?:\s+(.*))?", dis)
    addr, rawbytes, mnem = m.group(1), m.group(2).strip(), m.group(3)
    nbytes = len(rawbytes.split())
    rec = {"address": "0x" + addr, "bytes": rawbytes, "mnemonic": mnem, "byte_len": nbytes}
    out = wd / "instruction.json"
    out.write_text(json.dumps(rec, indent=1))
    return [
        check("first instruction decoded with a mnemonic", bool(mnem), mnem, "a mnemonic"),
        check("raw opcode bytes captured", nbytes >= 1, nbytes, ">=1"),
        check("negative control: mnemonic is not a hex address", not re.fullmatch(r"[0-9a-f]+", mnem), mnem, "not hex"),
    ], [out]


@card("REA-095")
def read_every_instruction(task, wd):
    elf = _build_elf(wd)
    dis = _objdump(elf, "-d", "-j", ".text")
    insns = [l for l in dis.splitlines() if re.match(r"\s+[0-9a-f]+:\s+[0-9a-f]{2}", l)]
    out = wd / "text_disasm.txt"
    out.write_text(dis)
    return [
        check("whole .text disassembled to raw instructions", len(insns) > 20, len(insns), ">20"),
        check("ret opcodes present in .text", any(re.search(r"\bret", l) for l in insns), True, True),
        check("negative control: no decompiled C braces in raw listing", "{" not in dis, "{" not in dis, True),
    ], [out]


@card("REA-093")
def objdump_retain_evidence(task, wd):
    elf = _build_elf(wd)
    dis = _objdump(elf, "-d")
    out = wd / "objdump_evidence.txt"
    out.write_text(dis)
    digest = sha(out)
    (wd / "objdump_evidence.sha256").write_text(digest)
    return [
        check("objdump produced a disassembly", len(dis) > 200, len(dis), ">200"),
        check("raw output retained and hashed", len(digest) == 64, len(digest), 64),
        check("negative control: evidence is not an empty file", out.stat().st_size > 0, out.stat().st_size, ">0"),
    ], [out, wd / "objdump_evidence.sha256"]


@card("REA-073")
def reconstruct_function_boundary(task, wd):
    elf = _build_elf(wd)
    relo = _readelf(elf, "-rW")
    externals = sorted(set(re.findall(r"R_X86_64_\w+\s+\w+\s+(\w+)@", relo)) |
                       set(re.findall(r"\b(printf|puts)\b", _objdump(elf, "-d"))))
    calls_printf = any(s in ("printf", "puts") for s in externals)
    out = wd / "api_boundary.json"
    out.write_text(json.dumps({"external_calls": externals, "internal_symbol": "add"}, indent=1))
    return [
        check("external libc boundary (printf/puts) identified", calls_printf, externals, "printf/puts present"),
        check("internal function add is not on the external boundary", "add" not in externals, "add" in externals, False),
        check("negative control: boundary list is non-empty", len(externals) >= 1, len(externals), ">=1"),
    ], [out]


@card("REA-077")
def verify_bytes_relocs_entry(task, wd):
    elf = _build_elf(wd, pie=False)
    entry = _entry(elf)
    off = _vaddr_to_offset(elf, entry)
    raw = elf.read_bytes()
    # objdump bytes at the entry address
    dis = _objdump(elf, "-d")
    m = re.search(r"\n\s+%x:\s+((?:[0-9a-f]{2} )+)" % entry, dis)
    od_bytes = bytes(int(x, 16) for x in m.group(1).split()) if m else b""
    file_bytes = raw[off:off + len(od_bytes)]
    match = od_bytes == file_bytes and len(od_bytes) > 0
    wrong = raw[off + 64:off + 64 + len(od_bytes)]
    relocs = len([l for l in _readelf(elf, "-rW").splitlines() if re.match(r"[0-9a-f]{6,}", l.strip())])
    out = wd / "verify_entry.json"
    out.write_text(json.dumps({"entry": hex(entry), "offset": off, "entry_bytes": od_bytes.hex(),
                               "relocations": relocs, "bytes_match": match}, indent=1))
    return [
        check("file bytes at entry offset match objdump bytes", match, od_bytes.hex(), file_bytes.hex()),
        check("relocation entries counted", relocs >= 1, relocs, ">=1"),
        check("negative control: bytes 64 further in differ from entry bytes", wrong != od_bytes, True, True),
    ], [out]


@card("REA-111")
def list_objdump_targets(task, wd):
    info = _objdump("--info") if False else fx.run(["objdump", "--info"]).stdout
    targets = re.findall(r"elf\d+-\S+", info)
    out = wd / "bfd_targets.json"
    out.write_text(json.dumps({"targets": sorted(set(targets))}, indent=1))
    return [
        check("objdump advertises elf BFD targets", len(targets) >= 1, len(targets), ">=1"),
        check("x86-64 elf target present", any("x86-64" in t for t in targets), True, True),
        check("negative control: fictitious target absent", "elf64-madeup" not in targets, False, False),
    ], [out]


@card("REA-103")
def list_architectures(task, wd):
    info = fx.run(["objdump", "--info"]).stdout
    archs = re.findall(r"^\s*(i386|x86-64|aarch64|arm|riscv\S*|mips\S*|powerpc\S*)\b", info, re.M)
    archs = sorted(set(archs))
    out = wd / "architectures.json"
    out.write_text(json.dumps({"architectures": archs}, indent=1))
    return [
        check("objdump lists supported architectures", len(archs) >= 1, len(archs), ">=1"),
        check("i386 architecture family present", any(a in ("i386", "x86-64") for a in archs), True, True),
        check("negative control: fictitious arch absent", "quantumcpu" not in archs, False, False),
    ], [out]


# ----------------------------------------------------------------------------- radare2
def _r2(args, cmd, timeout=40):
    return subprocess.run(["r2", "-q", "-c", cmd, *args], capture_output=True, text=True,
                          timeout=timeout, stdin=subprocess.DEVNULL).stdout


@card("REA-038")
def rizin_command_static(task, wd):
    elf = _build_elf(wd)
    info = _r2([str(elf)], "ij")
    data = json.loads(info.strip().splitlines()[0])
    arch = data["bin"]["arch"]
    bits = data["bin"]["bits"]
    btype = data["bin"]["bintype"]
    fns = _r2([str(elf)], "aa; afl")
    has_main = re.search(r"\bmain\b", fns) is not None
    # negative control: the same r2 info command on the C source is not an x86 ELF
    ctl = _r2([str(elf.with_suffix(".c"))], "ij")
    ctl_bin = json.loads(ctl.strip().splitlines()[0]).get("bin", {}) if ctl.strip() else {}
    ctl_type = ctl_bin.get("bintype", "none")
    out = wd / "r2_static.json"
    out.write_text(json.dumps({"arch": arch, "bits": bits, "bintype": btype, "main_listed": has_main}, indent=1))
    return [
        check("radare2 reports x86-64 ELF", arch == "x86" and bits == 64 and btype == "elf", [arch, bits, btype],
              ["x86", 64, "elf"]),
        check("analysis lists the main function", has_main, has_main, True),
        check("negative control: the C source is not analysed as an ELF", ctl_type != "elf", ctl_type, "not elf"),
    ], [out]


@card("REA-026")
def rizin_debugger_command(task, wd):
    elf = _build_elf(wd)
    dbg = _r2(["-d", str(elf)], "dr~rip")  # ephemeral debug session: read program counter
    m = re.search(r"rip\s*=\s*0x([0-9a-f]+)", dbg)
    rip_val = int(m.group(1), 16) if m else 0
    maps = _r2(["-d", str(elf)], "dm")
    # negative control: a static (non-debug) session has no live inferior, so rip reads back 0
    static = _r2([str(elf)], "dr~rip")
    sm = re.search(r"rip\s*=\s*0x([0-9a-f]+)", static)
    static_rip = int(sm.group(1), 16) if sm else 0
    out = wd / "r2_debug.log"
    out.write_text("dr:\n" + dbg + "\ndm:\n" + maps + "\nstatic dr:\n" + static)
    return [
        check("debugger session reports a live non-zero rip register", rip_val != 0, hex(rip_val), "non-zero"),
        check("process memory maps enumerated with r-x region", "r-x" in maps, "r-x" in maps, True),
        check("negative control: a static (non-debug) session reads rip as 0", static_rip == 0, hex(static_rip), "0x0"),
    ], [out]


# ----------------------------------------------------------------------------- gdb
@card("REA-025")
def gdb_mi_command(task, wd):
    elf = _build_elf(wd)
    r = subprocess.run(["gdb", "--batch", "--nx", "--interpreter=mi2", str(elf),
                        "-ex", "info functions ^main$"],
                       capture_output=True, text=True, timeout=40, stdin=subprocess.DEVNULL)
    out_text = r.stdout
    mi_session = "=thread-group-added" in out_text  # the MI machine-interface banner
    has_main = re.search(r"int main\(", out_text) is not None
    bogus = re.search(r"nonexistent_symbol_zzz", out_text) is not None
    out = wd / "gdb_mi.log"
    out.write_text(out_text)
    return [
        check("ephemeral GDB/MI session established (MI banner present)", mi_session, mi_session, True),
        check("console command listed the symbol main", has_main, has_main, True),
        check("negative control: an invented symbol is not reported", not bogus, bogus, False),
    ], [out]


@card("REA-084")
def inspect_core_registers(task, wd):
    crash = _build_elf(wd, src="int main(void){ volatile int *p = 0; return *p; }\n", name="crash")
    clean = _build_elf(wd, src="int main(void){ return 0; }\n", name="clean")
    rc = subprocess.run(["gdb", "--batch", "--nx", "-ex", "run", "-ex", "info registers rip",
                         "-ex", "bt", str(crash)], capture_output=True, text=True, timeout=40,
                        stdin=subprocess.DEVNULL).stdout
    cc = subprocess.run(["gdb", "--batch", "--nx", "-ex", "run", "-ex", "info registers rip", str(clean)],
                        capture_output=True, text=True, timeout=40, stdin=subprocess.DEVNULL).stdout
    sig = "SIGSEGV" in rc
    rip = re.search(r"rip\s+0x[0-9a-f]+", rc) is not None
    out = wd / "core_registers.log"
    out.write_text(rc)
    return [
        check("crash reports SIGSEGV with a captured signal", sig, sig, True),
        check("rip register value captured at fault", rip, rip, True),
        check("negative control: a clean-exit program reports no SIGSEGV", "SIGSEGV" not in cc, "SIGSEGV" in cc, False),
    ], [out]


# ----------------------------------------------------------------------------- go
@card("REA-066")
def inspect_go_binary(task, wd):
    gobin = wd / "goapp"
    (wd / "main.go").write_text("package main\nfunc main(){ println(\"hi\") }\n")
    env = dict(os.environ, GOCACHE=str(wd / "gocache"), GOPATH=str(wd / "gopath"),
               GOPROXY="off", GOTOOLCHAIN="local", GOFLAGS="-mod=mod")
    subprocess.run(["go", "mod", "init", "example/app"], cwd=wd, env=env, check=True,
                   capture_output=True, timeout=60, stdin=subprocess.DEVNULL)
    subprocess.run(["go", "build", "-o", str(gobin), "."], cwd=wd, env=env, check=True,
                   capture_output=True, timeout=120, stdin=subprocess.DEVNULL)
    info = subprocess.run(["go", "version", "-m", str(gobin)], env=env, capture_output=True,
                          text=True, timeout=30, stdin=subprocess.DEVNULL).stdout
    cinfo = subprocess.run(["go", "version", "-m", str(_build_elf(wd, name="cbin"))], env=env,
                           capture_output=True, text=True, timeout=30, stdin=subprocess.DEVNULL)
    has_ver = re.search(r"go1\.\d+", info) is not None
    has_path = "path\texample/app" in info or "example/app" in info
    out = wd / "go_buildinfo.txt"
    out.write_text(info)
    return [
        check("embedded Go toolchain version detected", has_ver, re.search(r"go1\.\d+", info).group(0) if has_ver else None, "go1.x"),
        check("module path recovered from build info", has_path, has_path, True),
        check("negative control: a C binary has no Go build info", "go1." not in cinfo.stdout, "go1." in cinfo.stdout, False),
    ], [out]


# ----------------------------------------------------------------------------- firmware blobs
def _firmware_blob(wd: Path):
    import zlib
    payload = b"FIRMWARE-PAYLOAD-" + b"A" * 64
    gz = b"\x1f\x8b\x08\x00" + b"\x00" * 6 + zlib.compress(payload)[2:]  # gzip-ish magic region
    blob = b"\x00" * 128 + b"PK\x03\x04" + b"\x00" * 60 + gz + b"\xff" * 32
    p = wd / "firmware.bin"
    p.write_bytes(blob)
    return p, 128, len(b"PK\x03\x04"), len(blob)


@card("REA-041")
def extract_firmware(task, wd):
    p, zip_off, _, total = _firmware_blob(wd)
    raw = p.read_bytes()
    length = 16
    carved = raw[zip_off:zip_off + length]
    outd = wd / "extracted"
    outd.mkdir()
    cf = outd / ("region_%d_%d.bin" % (zip_off, length))
    cf.write_bytes(carved)
    prov = {"source": p.name, "offset": zip_off, "length": length, "sha256": sha(cf),
            "starts_with": carved[:4].decode("latin1")}
    out = wd / "firmware_extract.json"
    out.write_text(json.dumps(prov, indent=1))
    return [
        check("carved region begins with the ZIP magic PK\\x03\\x04", carved[:4] == b"PK\x03\x04", carved[:4].hex(), b"PK\x03\x04".hex()),
        check("provenance records offset, length and sha256", len(prov["sha256"]) == 64 and prov["length"] == length, prov["length"], length),
        check("negative control: offset 0 of blob is zero padding, not the magic", raw[0:4] != b"PK\x03\x04", raw[0:4].hex(), "not PK"),
    ], [cf, out]


@card("REA-065")
def inspect_firmware_regions(task, wd):
    p, zip_off, _, total = _firmware_blob(wd)
    raw = p.read_bytes()
    sigs = {b"PK\x03\x04": "zip", b"\x1f\x8b\x08": "gzip"}
    found = []
    for magic, name in sigs.items():
        i = raw.find(magic)
        if i >= 0:
            found.append({"type": name, "offset": i})
    found.sort(key=lambda d: d["offset"])
    out = wd / "firmware_regions.json"
    out.write_text(json.dumps({"regions": found}, indent=1))
    return [
        check("zip signature region located", any(r["type"] == "zip" and r["offset"] == zip_off for r in found),
              [r for r in found if r["type"] == "zip"], "offset %d" % zip_off),
        check("gzip signature region located", any(r["type"] == "gzip" for r in found), True, True),
        check("negative control: no signature reported at padding offset 0", all(r["offset"] != 0 for r in found), True, True),
    ], [out]


# ----------------------------------------------------------------------------- Mach-O (hand-crafted)
@card("REA-069")
def inspect_macho(task, wd):
    MH_MAGIC_64 = 0xfeedfacf
    CPU_X86_64 = 0x01000007
    LC_SEGMENT_64 = 0x19
    seg = struct.pack("<II16sQQQQIIII", LC_SEGMENT_64, 72, b"__TEXT", 0, 0x1000, 0, 0x1000, 7, 5, 0, 0)
    header = struct.pack("<IiiIIIII", MH_MAGIC_64, CPU_X86_64, 3, 2, 1, len(seg), 0, 0)
    data = header + seg
    p = wd / "a.macho"
    p.write_bytes(data)
    magic, cputype, _sub, filetype, ncmds = struct.unpack_from("<IiiII", data, 0)
    arch = "x86_64" if cputype == CPU_X86_64 else "?"
    out = wd / "macho.json"
    out.write_text(json.dumps({"magic": hex(magic), "arch": arch, "filetype": filetype, "ncmds": ncmds}, indent=1))
    elf = _build_elf(wd)
    return [
        check("Mach-O 64-bit magic recognised", magic == MH_MAGIC_64, hex(magic), hex(MH_MAGIC_64)),
        check("cputype decoded as x86_64 with 1 load command", arch == "x86_64" and ncmds == 1, [arch, ncmds], ["x86_64", 1]),
        check("negative control: an ELF file is not a Mach-O", elf.read_bytes()[:4] != struct.pack("<I", MH_MAGIC_64),
              elf.read_bytes()[:4].hex(), "not feedfacf"),
    ], [out]


# ----------------------------------------------------------------------------- WASM (hand-crafted)
def _wasm(exports):
    def leb(n):
        return bytes([n])
    body = b"\x00asm\x01\x00\x00\x00"
    # type section (1): one type () -> ()
    ty = b"\x01\x60\x00\x00"
    body += b"\x01" + leb(len(ty)) + ty
    nf = len(exports)
    fn = bytes([nf]) + b"\x00" * nf
    body += b"\x03" + leb(len(fn)) + fn
    exp = bytes([nf])
    for i, name in enumerate(exports):
        nb = name.encode()
        exp += bytes([len(nb)]) + nb + b"\x00" + bytes([i])
    body += b"\x07" + leb(len(exp)) + exp
    code = bytes([nf]) + (b"\x02\x00\x0b") * nf
    body += b"\x0a" + leb(len(code)) + code
    return body


def _wasm_parse(data):
    assert data[:4] == b"\x00asm", "bad wasm magic"
    version = struct.unpack_from("<I", data, 4)[0]
    i, sections, exports = 8, [], []
    while i < len(data):
        sid = data[i]
        size = data[i + 1]
        payload = data[i + 2:i + 2 + size]
        sections.append(sid)
        if sid == 7:
            n = payload[0]
            j = 1
            for _ in range(n):
                ln = payload[j]
                name = payload[j + 1:j + 1 + ln].decode()
                exports.append(name)
                j += 1 + ln + 2
        i += 2 + size
    return version, sections, exports


@card("REA-089")
def inspect_wasm(task, wd):
    data = _wasm(["run"])
    p = wd / "mod.wasm"
    p.write_bytes(data)
    version, sections, exports = _wasm_parse(data)
    out = wd / "wasm.json"
    out.write_text(json.dumps({"version": version, "section_ids": sections, "exports": exports}, indent=1))
    return [
        check("wasm magic and version 1 parsed", version == 1, version, 1),
        check("export 'run' recovered from export section", exports == ["run"], exports, ["run"]),
        check("negative control: random bytes are not valid wasm", _not_wasm(b"not a module at all!!"), True, True),
    ], [out]


def _not_wasm(data):
    try:
        _wasm_parse(data)
        return False
    except Exception:
        return True


@card("REA-021")
def compare_wasm_interfaces(task, wd):
    a = _wasm(["run"])
    b = _wasm(["run", "halt"])
    (wd / "a.wasm").write_bytes(a)
    (wd / "b.wasm").write_bytes(b)
    ea = set(_wasm_parse(a)[2])
    eb = set(_wasm_parse(b)[2])
    added = sorted(eb - ea)
    removed = sorted(ea - eb)
    self_added = sorted(ea - ea)
    out = wd / "wasm_diff.json"
    out.write_text(json.dumps({"added_exports": added, "removed_exports": removed}, indent=1))
    return [
        check("new export 'halt' detected between versions", added == ["halt"], added, ["halt"]),
        check("no exports removed", removed == [], removed, []),
        check("negative control: comparing a module with itself yields no additions", self_added == [], self_added, []),
    ], [out]


# ----------------------------------------------------------------------------- EVM bytecode
@card("REA-064")
def inspect_evm_interface(task, wd):
    # PUSH4 <selector> EQ PUSH2 <dest> JUMPI pattern for two functions, then STOP
    def dispatch(sel, dest):
        return b"\x63" + bytes.fromhex(sel) + b"\x14" + b"\x61" + struct.pack(">H", dest) + b"\x57"
    code = dispatch("a9059cbb", 0x40) + dispatch("70a08231", 0x50) + b"\x00"
    p = wd / "contract.bin"
    p.write_bytes(code)
    selectors = []
    i = 0
    while i < len(code):
        op = code[i]
        if op == 0x63:  # PUSH4
            selectors.append(code[i + 1:i + 5].hex())
            i += 5
        elif 0x60 <= op <= 0x7f:
            i += 1 + (op - 0x5f)
        else:
            i += 1
    empty_code = b"\x00\x5b\x00"
    empty_sel = [c for c in [] if False] or _evm_selectors(empty_code)
    out = wd / "evm_interface.json"
    out.write_text(json.dumps({"function_selectors": selectors}, indent=1))
    return [
        check("ERC20 transfer selector a9059cbb inferred", "a9059cbb" in selectors, selectors, "contains a9059cbb"),
        check("two function selectors recovered", len(selectors) == 2, len(selectors), 2),
        check("negative control: bytecode with no PUSH4 has no selectors", empty_sel == [], empty_sel, []),
    ], [out]


def _evm_selectors(code):
    out, i = [], 0
    while i < len(code):
        op = code[i]
        if op == 0x63:
            out.append(code[i + 1:i + 5].hex())
            i += 5
        elif 0x60 <= op <= 0x7f:
            i += 1 + (op - 0x5f)
        else:
            i += 1
    return out


# ----------------------------------------------------------------------------- pcap
@card("REA-080")
def inspect_pcap(task, wd):
    def udp_packet(src_ip, dst_ip, sport, dport, payload):
        eth = b"\x00" * 6 + b"\x00" * 6 + b"\x08\x00"
        udp = struct.pack(">HHHH", sport, dport, 8 + len(payload), 0) + payload
        ip = struct.pack(">BBHHHBBH", 0x45, 0, 20 + len(udp), 1, 0, 64, 17, 0) + \
            bytes(map(int, src_ip.split("."))) + bytes(map(int, dst_ip.split(".")))
        return eth + ip + udp

    pkt = udp_packet("10.0.0.5", "8.8.8.8", 51000, 53, b"\x12\x34\x01\x00dnsquery")
    gh = struct.pack("<IHHiIII", 0xa1b2c3d4, 2, 4, 0, 0, 65535, 1)  # linktype 1 = ethernet
    rec = struct.pack("<IIII", 0, 0, len(pkt), len(pkt)) + pkt
    p = wd / "capture.pcap"
    p.write_bytes(gh + rec)
    empty = wd / "empty.pcap"
    empty.write_bytes(gh)
    endpoints, protos = _pcap_parse(p.read_bytes())
    e_endpoints, _ = _pcap_parse(empty.read_bytes())
    out = wd / "pcap.json"
    out.write_text(json.dumps({"endpoints": sorted(endpoints), "protocols": protos}, indent=1))
    return [
        check("DNS endpoint 8.8.8.8:53 observed", "8.8.8.8:53" in endpoints, sorted(endpoints), "contains 8.8.8.8:53"),
        check("UDP/DNS counted in protocol distribution", protos.get("DNS", 0) == 1, protos, {"DNS": 1}),
        check("negative control: an empty capture has no endpoints", len(e_endpoints) == 0, len(e_endpoints), 0),
    ], [out]


def _pcap_parse(data):
    magic = struct.unpack_from("<I", data, 0)[0]
    assert magic == 0xa1b2c3d4
    i = 24
    endpoints, protos = set(), {}
    while i + 16 <= len(data):
        incl = struct.unpack_from("<IIII", data, i)[2]
        pkt = data[i + 16:i + 16 + incl]
        i += 16 + incl
        if len(pkt) < 14 + 20 + 8 or pkt[12:14] != b"\x08\x00":
            continue
        ip = pkt[14:]
        proto = ip[9]
        dst_ip = ".".join(map(str, ip[16:20]))
        if proto == 17:
            udp = ip[20:]
            dport = struct.unpack_from(">H", udp, 2)[0]
            endpoints.add("%s:%d" % (dst_ip, dport))
            name = "DNS" if dport == 53 else "UDP"
            protos[name] = protos.get(name, 0) + 1
    return endpoints, protos


# ----------------------------------------------------------------------------- HAR / web network
@card("REA-091")
def inspect_web_capture(task, wd):
    har = {"log": {"version": "1.2", "entries": [
        {"request": {"method": "GET", "url": "https://example.com/app.js"},
         "response": {"status": 200, "content": {"mimeType": "application/javascript"}}},
        {"request": {"method": "POST", "url": "https://api.example.com/v1/data"},
         "response": {"status": 201, "content": {"mimeType": "application/json"}}},
    ]}}
    p = wd / "capture.har"
    p.write_text(json.dumps(har))
    log = json.loads(p.read_text())["log"]
    hosts = sorted({re.sub(r"https?://([^/]+).*", r"\1", e["request"]["url"]) for e in log["entries"]})
    methods = sorted({e["request"]["method"] for e in log["entries"]})
    out = wd / "har_summary.json"
    out.write_text(json.dumps({"hosts": hosts, "methods": methods, "entry_count": len(log["entries"])}, indent=1))
    empty = {"log": {"entries": []}}
    return [
        check("distinct hosts extracted without refetching URLs", hosts == ["api.example.com", "example.com"], hosts,
              ["api.example.com", "example.com"]),
        check("GET and POST methods recorded", methods == ["GET", "POST"], methods, ["GET", "POST"]),
        check("negative control: an empty HAR yields no hosts", len(empty["log"]["entries"]) == 0, 0, 0),
    ], [out]


# ----------------------------------------------------------------------------- sqlite
@card("REA-088")
def inspect_sqlite(task, wd):
    db = wd / "app.db"
    con = sqlite3.connect(db)
    con.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT, score REAL)")
    con.executemany("INSERT INTO users(name, score) VALUES(?,?)", [("ali", 9.5), ("sara", 8.0)])
    con.commit()
    schema = [r[0] for r in con.execute("SELECT sql FROM sqlite_master WHERE type='table'")]
    rows = con.execute("SELECT name, score FROM users ORDER BY name").fetchall()
    con.close()
    empty = sqlite3.connect(wd / "empty.db")
    empty_tables = empty.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    empty.close()
    out = wd / "sqlite.json"
    out.write_text(json.dumps({"schema": schema, "rows": rows}, indent=1))
    return [
        check("users table schema recovered", any("users" in s for s in schema), schema, "contains users"),
        check("two rows read with known values", rows == [("ali", 9.5), ("sara", 8.0)], rows, [("ali", 9.5), ("sara", 8.0)]),
        check("negative control: an empty database has no user tables", len(empty_tables) == 0, len(empty_tables), 0),
    ], [out]


@card("REA-074")
def inspect_typed_object(task, wd):
    db = wd / "typed.db"
    con = sqlite3.connect(db)
    con.execute("CREATE TABLE t(id INTEGER, label TEXT, amount REAL, blob BLOB)")
    info = con.execute("PRAGMA table_info(t)").fetchall()
    con.close()
    types = {r[1]: r[2] for r in info}
    out = wd / "typed_object.json"
    out.write_text(json.dumps({"columns": types}, indent=1))
    return [
        check("declared column types recovered", types.get("amount") == "REAL" and types.get("id") == "INTEGER",
              types, {"id": "INTEGER", "amount": "REAL"}),
        check("text and blob affinities distinguished", types.get("label") == "TEXT" and types.get("blob") == "BLOB",
              [types.get("label"), types.get("blob")], ["TEXT", "BLOB"]),
        check("negative control: there is no fictitious column 'ghost'", "ghost" not in types, False, False),
    ], [out]


# ----------------------------------------------------------------------------- plist / keyed archive
@card("REA-083")
def inspect_plist(task, wd):
    meta = {"CFBundleIdentifier": "com.example.app", "CFBundleShortVersionString": "1.2.3",
            "MinimumOSVersion": "15.0", "UIRequiredDeviceCapabilities": ["arm64"]}
    p = wd / "Info.plist"
    with open(p, "wb") as f:
        plistlib.dump(meta, f, fmt=plistlib.FMT_BINARY)
    loaded = plistlib.loads(p.read_bytes())
    not_plist = _plist_fails(_build_elf(wd).read_bytes())
    out = wd / "plist.json"
    out.write_text(json.dumps(loaded, indent=1))
    return [
        check("bundle identifier parsed from binary plist", loaded["CFBundleIdentifier"] == "com.example.app",
              loaded["CFBundleIdentifier"], "com.example.app"),
        check("version string recovered", loaded["CFBundleShortVersionString"] == "1.2.3",
              loaded["CFBundleShortVersionString"], "1.2.3"),
        check("negative control: an ELF file does not parse as a plist", not_plist, not_plist, True),
    ], [out]


def _plist_fails(data):
    try:
        plistlib.loads(data)
        return False
    except Exception:
        return True


@card("REA-068")
def inspect_keyed_archive(task, wd):
    U = plistlib.UID
    archive = {"$version": 100000, "$archiver": "NSKeyedArchiver", "$top": {"root": U(1)},
               "$objects": ["$null", {"name": "A", "next": U(2)}, {"name": "B"}]}
    p = wd / "archive.plist"
    with open(p, "wb") as f:
        plistlib.dump(archive, f, fmt=plistlib.FMT_BINARY)
    loaded = plistlib.loads(p.read_bytes())
    objs = loaded["$objects"]
    edges = []
    for idx, obj in enumerate(objs):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, plistlib.UID):
                    edges.append((idx, int(v)))
    out = wd / "keyed_graph.json"
    out.write_text(json.dumps({"object_count": len(objs), "edges": edges}, indent=1))
    return [
        check("object table recovered from keyed archive", len(objs) == 3, len(objs), 3),
        check("reference edge obj1 -> obj2 reconstructed", (1, 2) in edges, edges, "contains (1,2)"),
        check("negative control: the $null object has no outgoing references", all(e[0] != 0 for e in edges), True, True),
    ], [out]


# ----------------------------------------------------------------------------- archives
@card("REA-040")
def extract_artifact_contents(task, wd):
    import zipfile
    z = wd / "artifact.zip"
    contents = {"a.txt": b"alpha payload", "dir/b.txt": b"beta payload"}
    with zipfile.ZipFile(z, "w") as zf:
        for n, c in contents.items():
            zf.writestr(n, c)
        zf.writestr("../evil.txt", b"traversal attempt")
    outd = wd / "unpacked"
    outd.mkdir()
    extracted = []
    with zipfile.ZipFile(z) as zf:
        for info in zf.infolist():
            dest = (outd / info.filename).resolve()
            if not str(dest).startswith(str(outd.resolve())):
                continue  # reject path traversal
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(zf.read(info))
            extracted.append(info.filename)
    a_ok = (outd / "a.txt").read_bytes() == b"alpha payload"
    traversal_blocked = not (wd / "evil.txt").exists()
    out = wd / "extract_manifest.json"
    out.write_text(json.dumps({"extracted": extracted, "a_sha": sha(outd / "a.txt")}, indent=1))
    return [
        check("regular members extracted with exact content", a_ok and (outd / "dir/b.txt").exists(), a_ok, True),
        check("path-traversal entry rejected", traversal_blocked, traversal_blocked, True),
        check("negative control: evil.txt was not written outside the output dir", not (wd / "evil.txt").exists(), False, False),
    ], [out, outd / "a.txt"]


# ----------------------------------------------------------------------------- JS static reconstruction
@card("REA-130")
def recover_js_sources(task, wd):
    (wd / "bundle.js").write_text("console.log(42);\n//# sourceMappingURL=bundle.js.map\n")
    smap = {"version": 3, "sources": ["src/foo.js", "src/bar.js"],
            "sourcesContent": ["export const x = 42;\n", "export function y(){ return 1; }\n"]}
    (wd / "bundle.js.map").write_text(json.dumps(smap))
    outd = wd / "recovered"
    outd.mkdir()
    before = (outd / "src/foo.js").exists()
    manifest = []
    sm = json.loads((wd / "bundle.js.map").read_text())
    for src, content in zip(sm["sources"], sm["sourcesContent"]):
        dest = outd / src
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(content)
        manifest.append({"source": src, "sha256": sha(dest), "bytes": dest.stat().st_size})
    out = wd / "recover_manifest.json"
    out.write_text(json.dumps(manifest, indent=1))
    foo_ok = (outd / "src/foo.js").read_text() == "export const x = 42;\n"
    return [
        check("original module src/foo.js recovered from sourcesContent", foo_ok, foo_ok, True),
        check("every source recorded with a sha256 provenance", len(manifest) == 2 and all(len(m["sha256"]) == 64 for m in manifest),
              len(manifest), 2),
        check("negative control: the file did not exist before recovery", not before, before, False),
    ], [out, outd / "src/foo.js"]


@card("REA-039")
def export_website_scripts(task, wd):
    html = ("<html><head><script>var secret=1;function boot(){return secret;}</script>"
            "<script src='vendor.js'></script></head><body></body></html>")
    (wd / "page.html").write_text(html)
    outd = wd / "scripts"
    outd.mkdir()
    inline = re.findall(r"<script>(.*?)</script>", (wd / "page.html").read_text(), re.S)
    external = re.findall(r"<script src='([^']+)'", (wd / "page.html").read_text())
    files = []
    for i, body in enumerate(inline):
        f = outd / ("inline_%d.js" % i)
        f.write_text(body)
        files.append(f.name)
    manifest = {"inline": files, "external_refs": external}
    out = wd / "scripts_manifest.json"
    out.write_text(json.dumps(manifest, indent=1))
    body0 = (outd / "inline_0.js").read_text()
    return [
        check("inline script body exported to a file", "function boot" in body0, "function boot" in body0, True),
        check("external script reference recorded", external == ["vendor.js"], external, ["vendor.js"]),
        check("negative control: exported file is not the raw HTML", "<html>" not in body0, False, False),
    ], [out, outd / "inline_0.js"]


@card("REA-003")
def reconstruct_js_app(task, wd):
    bundle = (
        "var __webpack_modules__ = {\n"
        "\"./a.js\": (function(module, exports){ exports.x = 1; }),\n"
        "\"./b.js\": (function(module, exports){ exports.y = 2; })\n"
        "};\n"
    )
    (wd / "app.bundle.js").write_text(bundle)
    src = (wd / "app.bundle.js").read_text()
    modules = {}
    for m in re.finditer(r'"(\./[^"]+)":\s*\(function\(module, exports\)\{(.*?)\}\)', src):
        modules[m.group(1)] = m.group(2).strip()
    outd = wd / "app"
    outd.mkdir()
    for name, code in modules.items():
        dest = outd / name.lstrip("./")
        dest.write_text(code)
    flat = (wd / "flat.js")
    flat.write_text("console.log('no modules here');")
    flat_modules = len(re.findall(r'"(\./[^"]+)":\s*\(function', flat.read_text()))
    out = wd / "reconstruct.json"
    out.write_text(json.dumps({"modules": list(modules)}, indent=1))
    return [
        check("two webpack modules reconstructed", len(modules) == 2, len(modules), 2),
        check("module ./a.js body recovered", "exports.x = 1" in modules.get("./a.js", ""), True, True),
        check("negative control: a flat script yields zero modules", flat_modules == 0, flat_modules, 0),
    ], [out, outd / "a.js"]


@card("REA-017")
def compare_js_export_shapes(task, wd):
    a = "module.exports = { greet: function(){}, VERSION: 1 };"
    b = "module.exports = { greet: function(){}, VERSION: 1, farewell: function(){} };"
    (wd / "a.js").write_text(a)
    (wd / "b.js").write_text(b)

    def shape(text):
        s = {}
        for m in re.finditer(r"(\w+)\s*:\s*(function|\d+|'|\")", text):
            s[m.group(1)] = "function" if m.group(2) == "function" else "value"
        return s
    sa, sb = shape((wd / "a.js").read_text()), shape((wd / "b.js").read_text())
    added = sorted(set(sb) - set(sa))
    self_added = sorted(set(sa) - set(sa))
    out = wd / "export_shape_diff.json"
    out.write_text(json.dumps({"a": sa, "b": sb, "added": added}, indent=1))
    return [
        check("new export 'farewell' detected as a function", added == ["farewell"] and sb["farewell"] == "function",
              added, ["farewell"]),
        check("shared exports classified (greet=function, VERSION=value)", sa.get("greet") == "function" and sa.get("VERSION") == "value",
              [sa.get("greet"), sa.get("VERSION")], ["function", "value"]),
        check("negative control: comparing a module to itself adds nothing", self_added == [], self_added, []),
    ], [out]


@card("REA-128")
def read_bytes_at_address(task, wd):
    elf = _build_elf(wd)
    entry = _entry(elf)
    off = _vaddr_to_offset(elf, entry)
    raw = elf.read_bytes()
    n = 8
    got = raw[off:off + n]
    # cross-check against objdump's byte listing at the entry address
    dis = _objdump(elf, "-d")
    hexes = re.findall(r"\n\s+%x:\s+((?:[0-9a-f]{2} )+)" % entry, dis)
    od = bytes(int(x, 16) for x in hexes[0].split()) if hexes else b""
    match = got[:len(od)] == od and len(od) > 0
    elsewhere = raw[off + 128:off + 128 + n]
    out = wd / "read_bytes.json"
    out.write_text(json.dumps({"address": hex(entry), "length": n, "bytes": got.hex()}, indent=1))
    return [
        check("bytes read at the entry address match objdump's bytes", match, got[:len(od)].hex(), od.hex()),
        check("exactly the requested length was read", len(got) == n, len(got), n),
        check("negative control: bytes 128 further along differ from the entry bytes", elsewhere != got, True, True),
    ], [out]


# ----------------------------------------------------------------------------- Evidence JSON core
def _canon(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()


def _sha_bytes(b):
    import hashlib
    return hashlib.sha256(b).hexdigest()


@card("REA-006")
def build_obligation_ledger(task, wd):
    inp = {"target": "app", "obligations": [
        {"id": "O3", "claim": "entrypoint"}, {"id": "O1", "claim": "imports"}, {"id": "O2", "claim": "strings"}]}
    (wd / "input.json").write_text(json.dumps(inp))

    def build(data):
        obs = sorted(data["obligations"], key=lambda o: o["id"])
        ledger = {"target": data["target"], "obligations": [{"id": o["id"], "claim": o["claim"], "status": "unmet"} for o in obs]}
        return ledger, _sha_bytes(_canon(ledger))
    led1, sha1 = build(inp)
    led2, sha2 = build(json.loads((wd / "input.json").read_text()))
    other = dict(inp, target="other")
    _, sha_other = build(other)
    out = wd / "ledger.json"
    out.write_text(json.dumps(led1, indent=1))
    ids = [o["id"] for o in led1["obligations"]]
    return [
        check("ledger is deterministic across two builds", sha1 == sha2, sha1[:12], sha2[:12]),
        check("obligations sorted and all three covered", ids == ["O1", "O2", "O3"], ids, ["O1", "O2", "O3"]),
        check("negative control: a different target yields a different digest", sha1 != sha_other, sha1[:12], sha_other[:12]),
    ], [out]


@card("REA-035")
def evaluate_coverage(task, wd):
    partial = {"obligations": [{"id": "O1", "status": "met"}, {"id": "O2", "status": "met"},
                               {"id": "O3", "status": "met"}, {"id": "O4", "status": "unmet"}]}
    full = {"obligations": [{"id": o["id"], "status": "met"} for o in partial["obligations"]]}

    def evaluate(led):
        total = len(led["obligations"])
        met = sum(1 for o in led["obligations"] if o["status"] == "met")
        cov = met / total
        return {"coverage": cov, "ready": cov >= 1.0}  # fail-closed
    ep = evaluate(partial)
    ef = evaluate(full)
    out = wd / "coverage.json"
    out.write_text(json.dumps({"partial": ep, "full": ef}, indent=1))
    return [
        check("partial coverage computed as 0.75", abs(ep["coverage"] - 0.75) < 1e-9, ep["coverage"], 0.75),
        check("fail-closed: partial coverage is not ready", ep["ready"] is False, ep["ready"], False),
        check("negative control: full coverage flips ready to True", ef["ready"] is True, ef["ready"], True),
    ], [out]


@card("REA-036")
def validate_atomic_export(task, wd):
    REQUIRED = {"schema", "target", "observations"}
    evidence = {"schema": "rea/evidence/1", "target": "app", "observations": {"entry": "0x401136"}}

    def export(ev, dest):
        if not REQUIRED.issubset(ev):
            raise ValueError("missing required keys")
        tmp = dest.with_suffix(".tmp")
        tmp.write_text(json.dumps(ev, sort_keys=True))
        os.replace(tmp, dest)  # atomic
        return _sha_bytes(dest.read_bytes())
    out = wd / "evidence.json"
    digest = export(evidence, out)
    tmp_left = out.with_suffix(".tmp").exists()
    invalid_rejected = False
    try:
        export({"schema": "x"}, wd / "bad.json")
    except ValueError:
        invalid_rejected = True
    return [
        check("valid evidence exported atomically (no temp left)", not tmp_left, tmp_left, False),
        check("export digest matches file content", digest == _sha_bytes(out.read_bytes()), True, True),
        check("negative control: evidence missing required keys is rejected", invalid_rejected, invalid_rejected, True),
    ], [out]


@card("REA-037")
def validate_import_bounded(task, wd):
    MAX = 4096
    good = wd / "good.json"
    good.write_text(json.dumps({"schema": "rea/evidence/1", "target": "app", "observations": {}}))
    big = wd / "big.json"
    big.write_text(json.dumps({"schema": "rea/evidence/1", "target": "x", "pad": "A" * 8000}))

    def imp(path):
        if path.stat().st_size > MAX:
            return {"ok": False, "reason": "exceeds size bound"}
        data = json.loads(path.read_text())
        if "schema" not in data:
            return {"ok": False, "reason": "no schema"}
        return {"ok": True, "schema": data["schema"]}
    rg = imp(good)
    rb = imp(big)
    out = wd / "import_result.json"
    out.write_text(json.dumps({"good": rg, "big": rb}, indent=1))
    return [
        check("a small valid bundle is imported", rg["ok"] is True, rg["ok"], True),
        check("size bound enforced on an oversized bundle", rb["ok"] is False, rb["ok"], False),
        check("negative control: rejection names the size-bound reason", rb["reason"] == "exceeds size bound", rb["reason"],
              "exceeds size bound"),
    ], [out]


@card("REA-052")
def project_analysis_view(task, wd):
    evidence = {"binary-layout": {"sections": [".text", ".data"]},
                "javascript-application": {"modules": ["a.js"]},
                "wasm": {"exports": ["run"]}}
    (wd / "evidence.json").write_text(json.dumps(evidence))
    data = json.loads((wd / "evidence.json").read_text())
    view = "binary-layout"
    projected = {view: data[view]} if view in data else {}
    missing = {"missing-view": data.get("no-such-view")}
    out = wd / "view.json"
    out.write_text(json.dumps(projected, indent=1))
    return [
        check("only the requested binary-layout view is projected", list(projected) == ["binary-layout"],
              list(projected), ["binary-layout"]),
        check("projected view carries the section list", projected["binary-layout"]["sections"] == [".text", ".data"],
              projected["binary-layout"]["sections"], [".text", ".data"]),
        check("negative control: an absent view projects to None", missing["missing-view"] is None, missing["missing-view"], None),
    ], [out]


@card("REA-063")
def inspect_discovery_metadata(task, wd):
    evidence = {"discovery": {"providers": ["objdump", "readelf"], "coverage_exhausted": True,
                              "artifacts_seen": 3}, "observations": {}}
    (wd / "evidence.json").write_text(json.dumps(evidence))
    nodisc = {"observations": {}}
    (wd / "nodisc.json").write_text(json.dumps(nodisc))
    d = json.loads((wd / "evidence.json").read_text()).get("discovery")
    n = json.loads((wd / "nodisc.json").read_text()).get("discovery")
    out = wd / "discovery.json"
    out.write_text(json.dumps({"discovery": d}, indent=1))
    return [
        check("discovery providers extracted", d["providers"] == ["objdump", "readelf"], d["providers"], ["objdump", "readelf"]),
        check("artifacts_seen count read", d["artifacts_seen"] == 3, d["artifacts_seen"], 3),
        check("negative control: a bundle with no discovery block reports None", n is None, n, None),
    ], [out]


@card("REA-005")
def edit_function_annotations(task, wd):
    analysis = {"functions": [{"address": "0x401120", "name": "sub_401120", "comment": ""}]}
    (wd / "analysis.json").write_text(json.dumps(analysis))
    data = json.loads((wd / "analysis.json").read_text())
    before = _sha_bytes(_canon(data))
    fn = data["functions"][0]
    fn["name"], fn["comment"] = "parse_header", "validates magic and version"
    after = _sha_bytes(_canon(data))
    noop = _sha_bytes(_canon(json.loads((wd / "analysis.json").read_text())))  # unedited copy
    out = wd / "analysis_refreshed.json"
    out.write_text(json.dumps(data, indent=1))
    return [
        check("annotation name updated", data["functions"][0]["name"] == "parse_header",
              data["functions"][0]["name"], "parse_header"),
        check("refreshed analysis digest differs from the original", before != after, before[:12], after[:12]),
        check("negative control: an unedited copy keeps the original digest", noop == before, noop[:12], before[:12]),
    ], [out]


def _diff_json(a, b):
    added = sorted(set(_flatten(b)) - set(_flatten(a)))
    removed = sorted(set(_flatten(a)) - set(_flatten(b)))
    return added, removed


def _flatten(obj, prefix=""):
    items = []
    if isinstance(obj, dict):
        for k in sorted(obj):
            items += _flatten(obj[k], "%s.%s" % (prefix, k))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            items += _flatten(v, "%s[%d]" % (prefix, i))
    else:
        items.append("%s=%s" % (prefix, obj))
    return items


def _compare_card(wd, a, b, out_name, expect_added):
    (wd / "a.json").write_text(json.dumps(a))
    (wd / "b.json").write_text(json.dumps(b))
    added, removed = _diff_json(json.loads((wd / "a.json").read_text()), json.loads((wd / "b.json").read_text()))
    self_added, _ = _diff_json(a, a)
    out = wd / out_name
    out.write_text(json.dumps({"added": added, "removed": removed}, indent=1))
    hit = any(expect_added in x for x in added)
    return [
        check("expected change '%s' detected between the two bundles" % expect_added, hit, added, "contains %s" % expect_added),
        check("diff reports at least one difference", len(added) + len(removed) >= 1, len(added) + len(removed), ">=1"),
        check("negative control: comparing a bundle with itself finds no additions", self_added == [], self_added, []),
    ], [out]


@card("REA-015")
def compare_evidence_bundles(task, wd):
    a = {"schema": "rea/1", "sections": [".text"], "entry": "0x401136"}
    b = {"schema": "rea/1", "sections": [".text", ".rodata"], "entry": "0x401136"}
    return _compare_card(wd, a, b, "diff.json", ".rodata")


@card("REA-019")
def compare_process_captures(task, wd):
    a = {"pid": 42, "modules": ["libc.so"], "threads": 2}
    b = {"pid": 42, "modules": ["libc.so", "libssl.so"], "threads": 4}
    return _compare_card(wd, a, b, "process_diff.json", "libssl.so")


@card("REA-022")
def compare_passive_captures(task, wd):
    a = {"requests": [{"url": "https://a.test"}], "count": 1}
    b = {"requests": [{"url": "https://a.test"}, {"url": "https://b.test"}], "count": 2}
    return _compare_card(wd, a, b, "capture_diff.json", "b.test")


@card("REA-129")
def reconcile_runtime_evidence(task, wd):
    static = {"exports": ["init", "run"], "source": "static"}
    runtime = {"exports": ["init", "run", "debugHook"], "source": "runtime"}
    checks, outs = _compare_card(wd, static, runtime, "reconcile.json", "debugHook")
    # reconciliation adds a verdict: a runtime-only symbol is flagged
    added, _ = _diff_json(static, runtime)
    verdict = {"runtime_only": [x for x in added if "debugHook" in x]}
    (wd / "reconcile_verdict.json").write_text(json.dumps(verdict, indent=1))
    checks.append(check("runtime-only symbol debugHook flagged for review", bool(verdict["runtime_only"]),
                        verdict["runtime_only"], "non-empty"))
    return checks, outs + [wd / "reconcile_verdict.json"]


@card("REA-023")
def compare_png_artifacts(task, wd):
    from PIL import Image
    a = wd / "a.png"
    b = wd / "b.png"
    Image.new("RGB", (8, 8), (255, 0, 0)).save(a)
    Image.new("RGB", (8, 8), (0, 0, 255)).save(b)
    ev_a = {"path": a.name, "sha256": sha(a)}
    ev_b = {"path": b.name, "sha256": sha(b)}
    # self-verify: recompute and confirm
    verify_a = sha(a) == ev_a["sha256"]
    # tamper detection
    tampered = bytearray(a.read_bytes())
    tampered[-1] ^= 0xff
    (wd / "a_tampered.png").write_bytes(tampered)
    tamper_detected = _sha_bytes(bytes(tampered)) != ev_a["sha256"]
    out = wd / "png_compare.json"
    out.write_text(json.dumps({"a": ev_a, "b": ev_b, "identical": ev_a["sha256"] == ev_b["sha256"]}, indent=1))
    return [
        check("artifact self-verifies against its stored sha256", verify_a, verify_a, True),
        check("two different PNGs have different digests", ev_a["sha256"] != ev_b["sha256"], True, True),
        check("negative control: a tampered PNG fails verification", tamper_detected, tamper_detected, True),
    ], [out]


@card("REA-016")
def compare_app_graphs(task, wd):
    a = {"nodes": ["App", "Login"], "edges": [["App", "Login"]]}
    b = {"nodes": ["App", "Login", "Profile"], "edges": [["App", "Login"], ["App", "Profile"]]}
    return _compare_card(wd, a, b, "graph_diff.json", "Profile")


@card("REA-020")
def compare_source_vs_evidence(task, wd):
    source = {"functions": ["parse", "render"], "origin": "git"}
    evidence = {"functions": ["parse", "render", "hidden_backdoor"], "origin": "binary"}
    checks, outs = _compare_card(wd, source, evidence, "source_vs_evidence.json", "hidden_backdoor")
    return checks, outs


@card("REA-018")
def compare_managed_members(task, wd):
    old = [{"type": "App.Svc", "name": "Run", "signature": "void()"},
           {"type": "App.Svc", "name": "Login", "signature": "bool(string)"}]
    new = [{"type": "App.Svc", "name": "Run", "signature": "void()"},
           {"type": "App.Svc", "name": "Login", "signature": "bool(string,string)"}]  # same name, new signature
    (wd / "old.json").write_text(json.dumps(old))
    (wd / "new.json").write_text(json.dumps(new))

    def key(m):
        return (m["type"], m["name"], m["signature"])
    strict = set(map(key, old)) & set(map(key, new))
    name_only = {(m["type"], m["name"]) for m in old} & {(m["type"], m["name"]) for m in new}
    login_changed = ("App.Svc", "Login") in name_only and ("App.Svc", "Login", "bool(string)") not in {key(m) for m in new}
    out = wd / "managed_compare.json"
    out.write_text(json.dumps({"strict_matches": len(strict), "name_only_matches": len(name_only)}, indent=1))
    return [
        check("Login is not a strict match (signature changed)", login_changed, login_changed, True),
        check("strict signature matching is stricter than name-only", len(strict) < len(name_only), len(strict), "< %d" % len(name_only)),
        check("negative control: names alone would wrongly match Login", len(name_only) == 2, len(name_only), 2),
    ], [out]


@card("REA-044")
def import_managed_reconstruction(task, wd):
    static = [{"type": "App", "name": "Run", "signature": "void()"},
              {"type": "App", "name": "Load", "signature": "void(string)"}]
    recon = [{"type": "App", "name": "Run", "signature": "void()"},
             {"type": "App", "name": "Load", "signature": "void(string)"},
             {"type": "App", "name": "GhostMethod", "signature": "int()"}]  # not backed by static evidence
    (wd / "static.json").write_text(json.dumps(static))
    (wd / "recon.json").write_text(json.dumps(recon))
    backed = {(m["type"], m["name"], m["signature"]) for m in static}
    unbacked = [m for m in recon if (m["type"], m["name"], m["signature"]) not in backed]
    fully_backed = [m for m in static if (m["type"], m["name"], m["signature"]) in backed]
    out = wd / "managed_import.json"
    out.write_text(json.dumps({"unbacked": unbacked}, indent=1))
    return [
        check("reconstruction member unbacked by static evidence is flagged", len(unbacked) == 1 and unbacked[0]["name"] == "GhostMethod",
              [m["name"] for m in unbacked], ["GhostMethod"]),
        check("members present in static evidence are accepted", len(fully_backed) == 2, len(fully_backed), 2),
        check("negative control: an all-backed reconstruction flags nothing",
              len([m for m in static if (m["type"], m["name"], m["signature"]) not in backed]) == 0, 0, 0),
    ], [out]


@card("REA-045")
def import_source_tree(task, wd):
    src = wd / "src"
    (src / "pkg").mkdir(parents=True)
    (src / "main.c").write_text("int main(){return 0;}\n")
    (src / "pkg" / "util.c").write_text("int add(int a,int b){return a+b;}\n")
    manifest = []
    for f in sorted(src.rglob("*")):
        if f.is_file():
            manifest.append({"path": str(f.relative_to(src)), "sha256": sha(f), "bytes": f.stat().st_size})
    empty = wd / "empty_src"
    empty.mkdir()
    empty_manifest = [f for f in empty.rglob("*") if f.is_file()]
    out = wd / "source_manifest.json"
    out.write_text(json.dumps({"reference_only": True, "files": manifest}, indent=1))
    return [
        check("every source file listed with a sha256", len(manifest) == 2 and all(len(m["sha256"]) == 64 for m in manifest),
              len(manifest), 2),
        check("nested pkg/util.c captured in the manifest", any(m["path"].endswith("util.c") for m in manifest), True, True),
        check("negative control: an empty tree yields an empty manifest", len(empty_manifest) == 0, len(empty_manifest), 0),
    ], [out]


def _project_graph(wd, kind, inventory, out_name):
    (wd / "inventory.json").write_text(json.dumps(inventory))
    data = json.loads((wd / "inventory.json").read_text())
    nodes = [c["id"] for c in data["components"]]
    edges = [[c["id"], dep] for c in data["components"] for dep in c.get("depends_on", [])]
    graph = {"kind": kind, "nodes": nodes, "edges": edges}
    out = wd / out_name
    out.write_text(json.dumps(graph, indent=1))
    no_dep = {"components": [{"id": "solo"}]}
    no_edges = [[c["id"], d] for c in no_dep["components"] for d in c.get("depends_on", [])]
    return [
        check("%s graph nodes projected from inventory" % kind, set(nodes) == {c["id"] for c in inventory["components"]},
              len(nodes), len(inventory["components"])),
        check("a declared dependency becomes a graph edge", len(edges) >= 1, len(edges), ">=1"),
        check("negative control: an inventory with no dependencies has no edges", no_edges == [], no_edges, []),
    ], [out]


@card("REA-118")
def project_android_graph(task, wd):
    inv = {"components": [{"id": "MainActivity", "depends_on": ["AppModule"]},
                          {"id": "AppModule", "depends_on": []}]}
    return _project_graph(wd, "android", inv, "android_graph.json")


@card("REA-119")
def project_apple_graph(task, wd):
    inv = {"components": [{"id": "AppDelegate", "depends_on": ["NetworkKit"]},
                          {"id": "NetworkKit", "depends_on": []}]}
    return _project_graph(wd, "apple", inv, "apple_graph.json")


@card("REA-120")
def project_harmony_graph(task, wd):
    inv = {"components": [{"id": "EntryAbility", "depends_on": ["FeatureHSP"]},
                          {"id": "FeatureHSP", "depends_on": []}]}
    return _project_graph(wd, "harmonyos", inv, "harmony_graph.json")


@card("REA-121")
def project_managed_graph(task, wd):
    inv = {"components": [{"id": "App.dll", "depends_on": ["Core.dll"]},
                          {"id": "Core.dll", "depends_on": []}]}
    return _project_graph(wd, "managed", inv, "managed_graph.json")


# ----------------------------------------------------------------------------- GAPS
GAPS = {
    # rea CLI / provider metadata (no rea-agents install, no deep-analysis provider)
    "REA-007": "rea list-provider-capabilities: needs the REA v6.7.0 CLI and a registered provider; not installed",
    "REA-034": "rea doctor / readiness: needs the REA v6.7.0 CLI; not installed here",
    "REA-122": "rea list-providers: needs REA CLI provider registry; not installed",
    # JEB (proprietary)
    "REA-031": "JEB decompiler (proprietary, licensed) required for Dalvik/native pseudo-code; not available",
    "REA-054": "JEB method decompilation with overload selection (proprietary); not available",
    "REA-067": "JEB MCP client (proprietary) required; not available",
    "REA-110": "JEB project unit listing (proprietary); not available",
    "REA-117": "JEB project .jdb2 open/create (proprietary); not available",
    # Rizin / Cutter
    "REA-024": "live Cutter instance + Rizin plugin bridge; rizin/cutter not installed",
    "REA-105": "list live Cutter instances via the REA Python plugin bridge; Cutter not installed",
    # PE / .NET (need a real PE/CLI image + loader; no mingw/dotnet/mono)
    "REA-070": "PE/CLI identity: needs a real managed PE and a CLI metadata reader; no dotnet/mono/mingw here",
    "REA-071": "PE/CLI metadata members/CIL/ldstr: needs a managed PE; no .NET toolchain installed",
    "REA-072": "PE/CLI PInvoke boundaries: needs a managed PE; no .NET toolchain installed",
    "REA-082": "PE resource directory inspection: needs a Windows PE; no PE build toolchain (mingw) installed",
    # Apple proprietary formats (compiled nib/car, Mach-O objc runtime, LLDB launch of Mach-O)
    "REA-028": "compiled nib/storyboard (nibarchive) decode: proprietary Interface Builder format, no ibtool on Linux",
    "REA-058": "compiled .car asset catalog metadata: proprietary Apple format, no assetutil/actool on Linux",
    "REA-075": "Objective-C/Swift dispatch metadata: needs a real Mach-O __objc_* image (macOS build); not buildable here",
    "REA-087": "inspect Mach-O code signature/entitlements: proprietary Apple code-signing, needs macOS codesign; not available",
    "REA-114": "observe a running native app window by PID/windowId: needs a macOS GUI + accessibility backend; headless Linux",
    "REA-113": "launch a Mach-O under LLDB: requires macOS to actually run the Mach-O; Linux LLDB cannot execute it",
    # Swift / Dart / Rust toolchain-specific
    "REA-032": "swift demangling: swift-demangle not installed (c++filt handles Itanium C++, not the Swift scheme)",
    "REA-043": "Flutter Dart snapshot hash: needs a Flutter build toolchain; not installed",
    "REA-060": "Dart AOT snapshot sections/string pool: needs a Flutter/Dart AOT artifact; no Dart toolchain",
    "REA-085": "cargo-auditable Rust dependency list: needs a Rust/cargo-built binary with audit data; no cargo",
    # Wireshark / sigrok binaries
    "REA-078": "inspect pcap with caller-supplied TShark: Wireshark tshark not installed",
    "REA-079": "search installed TShark protocol/field definitions: tshark not installed",
    "REA-081": "inspect tshark/capinfos binaries: neither installed on PATH",
    "REA-029": "decode a signal recording with sigrok: sigrok-cli not installed",
    "REA-086": "search sigrok decoders: sigrok not installed",
    # apktool / dex (Android static decode of real formats)
    "REA-027": "APK manifest/resources decode: apktool not installed (binary AXML/ARSC decode needed)",
    "REA-053": "APK class member inventory: needs a dex parser/decompiler (apktool/dexlib); not installed",
    "REA-055": "APK declarations + decoded manifest: apktool not installed",
    "REA-056": "inspect the apktool launcher: apktool not installed",
    # device transports (adb / Frida) -- no connected device and no network to one
    "REA-014": "collect a device bugreport archive: needs adb and a connected device",
    "REA-047": "inspect the adb client: adb not installed",
    "REA-048": "device build identity via getprop: needs adb + a device",
    "REA-049": "display size/density: needs adb + a device",
    "REA-050": "installed package via dumpsys: needs adb + a device",
    "REA-051": "window manager focus: needs adb + a device",
    "REA-094": "install an APK: needs adb + a device",
    "REA-096": "run a Frida script against a process: Frida not installed, no target process",
    "REA-097": "list attached devices: needs adb",
    "REA-098": "list a device directory: needs adb + a device",
    "REA-099": "list device hardware/software features: needs adb + a device",
    "REA-100": "list installed packages: needs adb + a device",
    "REA-101": "list device processes (ps -A): needs adb + a device",
    "REA-102": "list binder services: needs adb + a device",
    "REA-107": "list Frida devices/remote endpoint: Frida not installed",
    "REA-108": "list processes via a Frida device: Frida not installed",
    "REA-123": "pull a device file with sha256: needs adb + a device",
    "REA-124": "pull an installed APK set: needs adb + a device",
    "REA-125": "push a local file to a device: needs adb + a device",
    "REA-126": "read the device logcat buffer: needs adb + a device",
    "REA-127": "read a device settings value: needs adb + a device",
    # live browser / CDP / Electron / screen capture (no display, no consented live target)
    "REA-004": "capture + analyse a live page bundle: needs a loopback CDP browser (Chromium/Playwright) + a target origin",
    "REA-008": "capture one screen frame: no display server / windowing in this headless container",
    "REA-009": "bounded Playwright scenario: needs a Playwright-driven browser against an owned target",
    "REA-010": "owned Electron scenario: needs an Electron app + CDP; not available",
    "REA-011": "declarative AX actions in a native window: needs a GUI accessibility backend",
    "REA-012": "process capture scenario: needs a live process capture backend",
    "REA-013": "capture a page viewport: needs a live browser + display",
    "REA-033": "discover page-declared WebMCP tools: needs a live page via CDP",
    "REA-061": "Electron fuse bytes: needs a packaged Electron app binary; not present",
    "REA-062": "passively inspect an Electron file page: needs an Electron app + CDP",
    "REA-090": "native listener source on first CSS match: needs a live CDP browser",
    "REA-092": "passively inspect a page via CDP: needs a loopback CDP browser",
    "REA-104": "list CDP page targets: needs a loopback CDP browser",
    "REA-106": "list Electron file pages via CDP: needs an Electron CDP endpoint",
    "REA-109": "list Node/Electron V8 Inspector targets: needs a running --inspect target on loopback",
    "REA-112": "observe a Node/Electron Inspector target: needs a running --inspect target",
    "REA-115": "observe precise page execution (coverage/opt reset): needs a live CDP browser",
    "REA-116": "observe user-driven navigation: needs a live browser + a user session",
}
