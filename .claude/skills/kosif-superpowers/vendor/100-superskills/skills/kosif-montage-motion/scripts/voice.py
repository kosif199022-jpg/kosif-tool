"""KOSIF voice — offline narration with the voices Windows already has (OneCore: e.g. "Microsoft Naayf" ar-SA, David,
Zira, Mark). Nothing leaves the machine. A timed script becomes one voice track plus line timings for captions.

    python voice.py --list
    python voice.py out.wav --text "كل إطار برنامج" [--voice Naayf] [--rate -5%]
    python voice.py out.wav --script lines.json [--seconds 15]        lines.json: [{"t": 0.6, "text": "...", "rate": "-5%"}, ...]

Writes out.wav (48 kHz stereo) and out.json ([{t, end, text}] — captions and the mux's ducking read it).
In a composition: <audio id="voice" src="assets/voice.wav" data-start="0" data-role="voice" ...> — the studio mux ducks the
other clips under it (sidechain) and normalises the mix to −14 LUFS.
"""
from __future__ import annotations
import sys as _sys
for _s in (_sys.stdout, _sys.stderr):
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="replace")   # Windows consoles default to a legacy code page

import argparse
import json
import subprocess
import tempfile
import wave
from pathlib import Path
from xml.sax.saxutils import escape

import numpy as np

SR = 48000
PS = r"""
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Runtime.WindowsRuntime
$asTask = ([System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object { $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1' })[0]
function Await($op, $type) { $t = $asTask.MakeGenericMethod($type).Invoke($null, @($op)); $t.Wait(-1) | Out-Null; $t.Result }
[Windows.Media.SpeechSynthesis.SpeechSynthesizer, Windows.Media.SpeechSynthesis, ContentType = WindowsRuntime] | Out-Null
$all = [Windows.Media.SpeechSynthesis.SpeechSynthesizer]::AllVoices
if ($args[0] -eq '--list') { $all | ForEach-Object { $_.DisplayName + '|' + $_.Language + '|' + $_.Gender }; exit 0 }
$ssml = [System.IO.File]::ReadAllText($args[0], [System.Text.Encoding]::UTF8)
$s = New-Object Windows.Media.SpeechSynthesis.SpeechSynthesizer
$v = $all | Where-Object { $_.DisplayName -like ('*' + $args[2] + '*') } | Select-Object -First 1
if ($v) { $s.Voice = $v }
$stream = Await ($s.SynthesizeSsmlToStreamAsync($ssml)) ([Windows.Media.SpeechSynthesis.SpeechSynthesisStream])
$in = [System.IO.WindowsRuntimeStreamExtensions]::AsStreamForRead($stream)
$fs = [System.IO.File]::Create($args[1]); $in.CopyTo($fs); $fs.Close()
"""


def _ps(args: list[str]) -> str:
    script = Path(tempfile.mkdtemp(prefix="kosif_voice_")) / "say.ps1"
    script.write_text(PS, encoding="utf-8-sig")
    r = subprocess.run(["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(script), *args],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        raise RuntimeError((r.stderr or r.stdout)[-600:])
    return r.stdout


def voices() -> list[dict]:
    out = []
    for line in _ps(["--list"]).splitlines():
        parts = line.strip().split("|")
        if len(parts) >= 2:
            out.append({"name": parts[0], "lang": parts[1], "gender": parts[2] if len(parts) > 2 else ""})
    return out


def _lang_of(voice: str) -> str:
    for v in voices():
        if voice.lower() in v["name"].lower():
            return v["lang"]
    return "ar-SA"


def _read_wav(path: Path) -> np.ndarray:
    with wave.open(str(path)) as w:
        sr, ch, sw, n = w.getframerate(), w.getnchannels(), w.getsampwidth(), w.getnframes()
        x = np.frombuffer(w.readframes(n), {2: np.int16, 4: np.int32, 1: np.uint8}[sw]).astype(np.float32)
    x = (x - 128) / 128 if sw == 1 else x / float(np.iinfo({2: np.int16, 4: np.int32}[sw]).max)
    if ch > 1:
        x = x.reshape(-1, ch).mean(1)
    if sr != SR:                                              # linear resample to 48 kHz
        t = np.linspace(0, len(x) / sr, int(len(x) * SR / sr), endpoint=False)
        x = np.interp(t, np.arange(len(x)) / sr, x).astype(np.float32)
    return x


def say(text: str, voice: str = "Naayf", rate: str = "-4%", pitch: str = "+0%", lang: str | None = None) -> np.ndarray:
    lang = lang or _lang_of(voice)
    ssml = (f"<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='{lang}'>"
            f"<prosody rate='{rate}' pitch='{pitch}'>{escape(text)}</prosody></speak>")
    tmp = Path(tempfile.mkdtemp(prefix="kosif_voice_"))
    (tmp / "s.xml").write_text(ssml, encoding="utf-8")
    _ps([str(tmp / "s.xml"), str(tmp / "o.wav"), voice])
    x = _read_wav(tmp / "o.wav")
    nz = np.flatnonzero(np.abs(x) > 0.004)                  # trim the synthesiser's leading and trailing silence
    if len(nz):
        x = x[max(0, nz[0] - int(0.02 * SR)): nz[-1] + int(0.08 * SR)]
    return x


def track(lines: list[dict], voice: str = "Naayf", seconds: float | None = None) -> tuple[np.ndarray, list[dict]]:
    clips, timing = [], []
    for ln in lines:
        x = say(ln["text"], ln.get("voice", voice), ln.get("rate", "-4%"), ln.get("pitch", "+0%"))
        clips.append((float(ln["t"]), x))
        timing.append({"t": float(ln["t"]), "end": round(float(ln["t"]) + len(x) / SR, 3), "text": ln["text"]})
    total = seconds or (max(e["end"] for e in timing) + 0.5 if timing else 1.0)
    out = np.zeros(int(total * SR), np.float32)
    for t0, x in clips:
        i = int(t0 * SR)
        x = x[: max(0, len(out) - i)]
        out[i:i + len(x)] += x
    peak = np.abs(out).max() or 1.0
    out = out / peak * 0.89
    return out, timing


def write(path: Path, mono: np.ndarray):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    st = np.stack([mono, mono], 1)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(st, -1, 1) * 32767).astype(np.int16).tobytes())


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("out", nargs="?")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--text"); ap.add_argument("--script"); ap.add_argument("--voice", default="Naayf")
    ap.add_argument("--rate", default="-4%"); ap.add_argument("--seconds", type=float)
    a = ap.parse_args()
    if a.list:
        for v in voices():
            print(f"{v['name']:28s} {v['lang']:8s} {v['gender']}")
        return
    if not a.out:
        ap.error("out.wav is required")
    lines = json.loads(Path(a.script).read_text(encoding="utf-8")) if a.script else [{"t": 0.0, "text": a.text or "", "rate": a.rate}]
    mono, timing = track(lines, a.voice, a.seconds)
    write(Path(a.out), mono)
    Path(a.out).with_suffix(".json").write_text(json.dumps(timing, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({"file": a.out, "seconds": round(len(mono) / SR, 2), "lines": len(timing), "voice": a.voice}, ensure_ascii=False))


if __name__ == "__main__":
    main()
