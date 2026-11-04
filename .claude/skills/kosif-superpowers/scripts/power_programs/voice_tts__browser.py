"""Wave-2 browser program for voice-tts: VOICE-52, MediaRecorder capture and download.

A Web Audio oscillator (440 Hz) feeds a MediaStream; createAudioRecorder(stream).stop() resolves
a Blob (audio/webm by default), downloadAudioBlob(blob,'kosif-response.webm') triggers the file
download and revokes the object URL after 1000 ms. The saved file is converted to WAV with ffmpeg
and its pitch is measured: the known answer is 440 Hz.
"""
from __future__ import annotations

import wave
from pathlib import Path

import numpy as np

from ._browser_common import browser, ff, page, probe

REC = """<!doctype html><html><body><script>
function createAudioRecorder(stream,mime){const chunks=[];const rec=new MediaRecorder(stream,mime?{mimeType:mime}:undefined);rec.ondataavailable=e=>chunks.push(e.data);
return {start(){rec.start(100)},stop(){return new Promise(r=>{rec.onstop=()=>r(new Blob(chunks,{type:rec.mimeType||'audio/webm'}));rec.stop()})},mime:()=>rec.mimeType}}
function downloadAudioBlob(blob,name){const url=URL.createObjectURL(blob);const a=document.createElement('a');a.href=url;a.download=name;a.id='dl';a.textContent='dl';
document.body.appendChild(a);window.__url=url;setTimeout(()=>{URL.revokeObjectURL(url);window.__revoked=performance.now()},1000);window.__made=performance.now();return a}
window.go=async()=>{const ac=new AudioContext();const o=ac.createOscillator();o.frequency.value=440;const d=ac.createMediaStreamDestination();o.connect(d);o.start();
const r=createAudioRecorder(d.stream);r.start();await new Promise(x=>setTimeout(x,1200));const blob=await r.stop();o.stop();
downloadAudioBlob(blob,'kosif-response.webm');return {type:blob.type,size:blob.size}};
window.alive=async()=>{try{await (await fetch(window.__url)).blob();return true}catch(e){return false}};</script></body></html>"""


def pitch(wav: Path) -> float:
    with wave.open(str(wav)) as w:
        sr = w.getframerate()
        x = np.frombuffer(w.readframes(w.getnframes()), "<i2").astype(float)
    x = x[int(0.2 * sr):]
    spec = np.abs(np.fft.rfft(x * np.hanning(len(x))))
    return float(np.argmax(spec) * sr / len(x))


def voice_52(work: Path):
    """MediaRecorder capture + download: record a 440 Hz MediaStream to a Blob, download kosif-response.webm, revoke after 1000 ms."""
    page(work, "rec.html", REC)
    (work / "dl").mkdir()
    r = browser(work, {"launch": {"args": ["--autoplay-policy=no-user-gesture-required"]}, "steps": [
        {"op": "goto", "url": "/rec.html"}, {"op": "eval", "js": "window.go()", "as": "blob"},
        {"op": "eval", "js": "window.alive()", "as": "before"},
        {"op": "download", "selector": "#dl", "dir": str(work / "dl"), "as": "file"},
        {"op": "eval", "js": "new Promise(r=>setTimeout(r,1100))"},
        {"op": "eval", "js": "window.alive()", "as": "after"},
        {"op": "eval", "js": "window.__revoked-window.__made", "as": "delay"}]})
    v = r["values"]
    f = Path(v["file"]["path"])
    ff("-i", str(f), "-ac", "1", "-ar", "16000", str(work / "response.wav"))
    hz = pitch(work / "response.wav")
    dur = float(probe(work / "response.wav")["format"]["duration"])
    return [("default mime is audio/webm", v["blob"]["type"].startswith("audio/webm"), v["blob"]["type"]),
            ("download saved as kosif-response.webm", v["file"]["name"] == "kosif-response.webm" and v["file"]["bytes"] == v["blob"]["size"], str(v["file"])),
            ("object URL alive before 1000 ms", v["before"] is True, str(v["before"])),
            ("object URL revoked after 1000 ms", v["after"] is False and v["delay"] is not None and 995 <= v["delay"] < 1300, f"{v['after']} {v['delay']} ms"),
            ("converted WAV holds the 1.2 s recording", 0.9 < dur < 1.6, f"{dur:.2f} s"),
            ("recorded pitch is 440 Hz", abs(hz - 440) < 5, f"{hz:.1f} Hz")]


PROGRAMS = {"VOICE-52": voice_52}
