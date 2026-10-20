#!/usr/bin/env python3
"""KOSIF Blender Cinema: cinematic Cycles renders from one command, built on the capabilities read out of Blender 5.2.2
on this laptop (REA overview of the install + the live bpy API: 2,499 operators, 4,023 types, 274 geometry nodes,
the node-group compositor, 4 sky models, 7 panoramic lenses, AgX/Filmic/Khronos PBR Neutral, OpenImageDenoise).

    python scripts/blender_cinema.py doctor                    # finds Blender (or the bpy module) and its version
    python scripts/blender_cinema.py presets                   # the cinematic looks and what each sets
    python scripts/blender_cinema.py inventory -o blender.json # live capability inventory from Blender itself
    python scripts/blender_cinema.py render --preset neon-night -o shot.png
    python scripts/blender_cinema.py render --preset product-hero --model chair.glb --quality final -o hero.png
    python scripts/blender_cinema.py render --preset golden-hour --frames 72 --move orbit -o turntable.mp4
    python scripts/blender_cinema.py render --preset anamorphic-epic --save-blend epic.blend -o epic.png

What a preset sets (all of it real Blender settings, editable in the saved .blend):
  path tracing  Cycles, adaptive sampling, light tree, path guiding on CPU, clamped indirect light, OpenImageDenoise
  lens          focal length, sensor 36 mm, depth of field with f-stop, blade count and anamorphic aperture ratio,
                autofocus on the subject, 180° shutter motion blur for animation
  light         area/spot/sun rigs in Kelvin, physical sky (multiple scattering), volumetric fog and god rays
  film          AgX view transform with a look, exposure, then the compositor: bloom or anamorphic streaks,
                lens dispersion (chromatic aberration), lift/gamma/gain grade, vignette
  camera move   orbit, dolly-in, crane-up, vertigo (dolly zoom), handheld

Blender is found from KOSIF_BLENDER, PATH, ~/KOSIF-Tools/Blender*/…/blender(.exe), Program Files, /Applications or
/usr/bin; when no executable exists the `bpy` module (pip install bpy) runs the same code. Every result prints one JSON
line {"op","output","metrics","verified"}; "verified" means the file was rendered and measured (size, not blank).
"""
import argparse
import glob
import json
import math
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time

try:
    import bpy  # noqa: F401  (present inside Blender or with `pip install bpy`)
    HAVE_BPY = True
except ImportError:
    HAVE_BPY = False

HERE = Path(__file__).resolve()

PRESETS = {
    "product-hero": {
        "ar": "منتج بطل على خلفية استوديو منحنية بثلاث إضاءات ناعمة",
        "lens": 85, "fstop": 2.8, "blades": 0, "ratio": 1.0, "look": "AgX - Punchy", "exposure": 0.0,
        "set": "cyclorama", "world": [0.02, 0.02, 0.025], "material": "glossy-paint",
        "lights": [{"type": "AREA", "k": 5600, "w": 900, "size": 3, "at": [-3.5, -3.0, 4.0]},
                   {"type": "AREA", "k": 6500, "w": 250, "size": 4, "at": [4.0, -2.5, 2.0]},
                   {"type": "SPOT", "k": 4800, "w": 1500, "spot": 40, "at": [0.5, 4.5, 3.5]}],
        "cam": [0.0, -10.0, 2.0], "finish": {"glare": "Bloom", "glare_strength": 0.25, "dispersion": 0.0, "vignette": 0.25,
                                            "grade": [[1.0, 1.0, 1.02], [1.0, 1.0, 1.0], [1.02, 1.0, 0.98]]},
    },
    "golden-hour": {
        "ar": "ساعة ذهبية: سماء فيزيائية وشمس منخفضة وضباب جوي",
        "lens": 35, "fstop": 4.0, "blades": 7, "ratio": 1.0, "look": "AgX - Base Contrast", "exposure": -0.3,
        "set": "ground", "sky": {"elevation": 5.0, "rotation": 200.0}, "mist": 0.01, "material": "brushed-gold",
        "lights": [{"type": "SUN", "k": 3600, "w": 3.5, "angle": 1.2, "elev": 5.0, "rot": 200.0}],
        "cam": [3.5, -6.5, 1.0], "finish": {"glare": "Fog Glow", "glare_strength": 0.35, "dispersion": 0.004, "vignette": 0.3,
                                            "grade": [[1.0, 0.98, 1.03], [1.0, 1.0, 1.0], [1.06, 1.0, 0.9]]},
    },
    "noir-volumetric": {
        "ar": "نوار: شعاع ضوء صلب عبر ستائر وضباب حجمي بالأبيض والأسود",
        "lens": 50, "fstop": 2.0, "blades": 6, "ratio": 1.0, "look": "AgX - High Contrast", "exposure": 0.2,
        "set": "room", "world": [0.0, 0.0, 0.0], "fog": 0.035, "blinds": True, "material": "satin-black",
        "lights": [{"type": "SPOT", "k": 5200, "w": 9000, "spot": 22, "blend": 0.08, "at": [-6.0, 3.0, 6.0]},
                   {"type": "AREA", "k": 7000, "w": 60, "size": 6, "at": [3.0, -4.0, 3.0]}],
        "cam": [2.5, -6.0, 1.4], "finish": {"glare": "Bloom", "glare_strength": 0.2, "dispersion": 0.0, "vignette": 0.45,
                                            "saturation": 0.0, "grade": [[0.98, 0.98, 0.98], [1.0, 1.0, 1.0], [1.05, 1.05, 1.05]]},
    },
    "neon-night": {
        "ar": "نيون ليلي: أنابيب مضيئة وأرض مبتلة عاكسة وضباب وانحراف لوني",
        "lens": 24, "fstop": 1.8, "blades": 8, "ratio": 1.0, "look": "AgX - Punchy", "exposure": 0.0,
        "set": "wet-floor", "world": [0.002, 0.003, 0.01], "fog": 0.012, "neon": True, "material": "glossy-paint",
        "lights": [{"type": "AREA", "k": 8000, "w": 220, "size": 5, "at": [0.0, -3.5, 4.5]},
                   {"type": "SPOT", "k": 9000, "w": 900, "spot": 35, "at": [1.5, 4.0, 3.0]}], "cam": [2.8, -5.5, 1.1],
        "finish": {"glare": "Bloom", "glare_strength": 0.7, "dispersion": 0.025, "vignette": 0.35,
                   "grade": [[0.98, 1.0, 1.04], [1.0, 1.0, 1.0], [1.04, 0.98, 1.04]]},
    },
    "anamorphic-epic": {
        "ar": "ملحمي أنامورفيك 2.39:1: بوكيه بيضاوي وتوهج خطي أفقي وتدرج تيل وبرتقالي",
        "lens": 50, "fstop": 2.8, "blades": 0, "ratio": 2.0, "look": "AgX - Medium High Contrast", "exposure": 0.0,
        "aspect": 2.39, "set": "ground-dark", "world": [0.004, 0.006, 0.01], "bokeh_lights": True, "material": "brushed-gold",
        "lights": [{"type": "AREA", "k": 3200, "w": 1200, "size": 2, "at": [0.0, 5.0, 2.5]},
                   {"type": "AREA", "k": 7500, "w": 300, "size": 5, "at": [-4.0, -3.0, 3.0]}],
        "cam": [0.0, -6.0, 1.2], "finish": {"glare": "Streaks", "streaks": 2, "glare_strength": 0.3, "glare_threshold": 2.0, "dispersion": 0.01,
                                            "vignette": 0.3, "grade": [[0.96, 1.0, 1.06], [1.0, 1.0, 1.0], [1.08, 1.0, 0.9]]},
    },
}
QUALITY = {"draft": {"samples": 24, "pct": 50}, "preview": {"samples": 96, "pct": 100}, "final": {"samples": 512, "pct": 100}}
MOVES = ["none", "orbit", "dolly-in", "crane-up", "vertigo", "handheld"]


# ====================================================================== outside Blender
def find_blender():
    env = os.environ.get("KOSIF_BLENDER")
    if env and Path(env).exists():
        return env
    for name in ("blender", "blender.exe"):
        p = shutil.which(name)
        if p:
            return p
    home = Path.home()
    pats = [str(home / "KOSIF-Tools" / "Blender*" / "**" / "blender.exe"), str(home / "KOSIF-Tools" / "Blender*" / "**" / "blender"),
            r"C:\Program Files\Blender Foundation\*\blender.exe", "/Applications/Blender.app/Contents/MacOS/Blender",
            "/usr/bin/blender", "/snap/bin/blender", str(home / "blender*" / "blender")]
    for pat in pats:
        hits = sorted(glob.glob(pat, recursive=True), reverse=True)
        hits = [h for h in hits if Path(h).name.lower() in ("blender.exe", "blender")]
        if hits:
            return hits[0]
    return None


def bpy_python():
    """A Python interpreter that can import bpy (KOSIF_BPY_PYTHON, or this one)."""
    env = os.environ.get("KOSIF_BPY_PYTHON")
    cands = [env] if env else []
    cands.append(sys.executable)
    for py in cands:
        if py and subprocess.run([py, "-c", "import bpy"], capture_output=True).returncode == 0:
            return py
    return None


def run_inside(job):
    """Run this file inside Blender (executable, or bpy module) with a job; return the receipt."""
    tmp = Path(tempfile.mkdtemp(prefix="kosif-blender-"))
    jp = tmp / "job.json"
    job["receipt"] = str(tmp / "receipt.json")
    jp.write_text(json.dumps(job, ensure_ascii=False), encoding="utf-8")
    exe = find_blender()
    if exe:
        cmd = [exe, "-b", "--factory-startup", "--python", str(HERE), "--", "--job", str(jp)]
        runner = "blender"
    else:
        py = bpy_python()
        if not py:
            raise RuntimeError("Blender not found: set KOSIF_BLENDER to blender(.exe), put it on PATH, "
                               "or `pip install bpy` (Blender as a Python module)")
        cmd, runner = [py, str(HERE), "--job", str(jp)], "bpy-module"
    t0 = time.time()
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    rp = Path(job["receipt"])
    if not rp.exists():
        tail = "\n".join((proc.stdout + proc.stderr).splitlines()[-25:])
        raise RuntimeError(f"Blender run failed (exit {proc.returncode}):\n{tail}")
    rec = json.loads(rp.read_text(encoding="utf-8"))
    rec["runner"], rec["blender"], rec["wall_seconds"] = runner, exe, round(time.time() - t0, 1)
    shutil.rmtree(tmp, ignore_errors=True)
    return rec


def measure_png(path):
    """Size and brightness statistics of a rendered PNG (pure stdlib decode is overkill: use Pillow when present)."""
    try:
        from PIL import Image, ImageStat
        im = Image.open(path).convert("RGB")
        st = ImageStat.Stat(im)
        return {"size": list(im.size), "mean": [round(v, 1) for v in st.mean], "std": [round(v, 1) for v in st.stddev]}
    except ImportError:
        data = Path(path).read_bytes()
        return {"bytes": len(data), "png": data.startswith(b"\x89PNG")}


def encode_mp4(frames_dir, fps, out):
    ff = shutil.which("ffmpeg")
    if not ff:
        return None
    cmd = [ff, "-y", "-loglevel", "error", "-framerate", str(fps), "-i", str(Path(frames_dir) / "frame_%04d.png"),
           "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "16", "-movflags", "+faststart", str(out)]
    return str(out) if subprocess.run(cmd).returncode == 0 else None


def cli(argv=None):
    ap = argparse.ArgumentParser(prog="blender_cinema.py", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("doctor")
    sub.add_parser("presets")
    iv = sub.add_parser("inventory")
    iv.add_argument("-o", "--out", required=True)
    r = sub.add_parser("render")
    r.add_argument("--preset", default="product-hero", choices=sorted(PRESETS))
    r.add_argument("--model", help=".glb .gltf .fbx .obj .stl .ply .usd/.usdz .abc or .blend (objects appended)")
    r.add_argument("--res", default="1920x1080", help="WxH before --quality scaling; anamorphic-epic keeps 2.39:1")
    r.add_argument("--quality", default="draft", choices=sorted(QUALITY))
    r.add_argument("--samples", type=int)
    r.add_argument("--frames", type=int, default=1)
    r.add_argument("--fps", type=int, default=24)
    r.add_argument("--move", default="none", choices=MOVES)
    r.add_argument("--device", default="auto", choices=["auto", "cpu", "gpu"])
    r.add_argument("--lens", type=float)
    r.add_argument("--fstop", type=float)
    r.add_argument("--seed", type=int, default=7)
    r.add_argument("--save-blend")
    r.add_argument("-o", "--out", required=True)
    a = ap.parse_args(argv)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if a.cmd == "presets":
        for k, v in PRESETS.items():
            print(f"{k:16} lens {v['lens']}mm f/{v['fstop']}  {v['look']:28} {v['ar']}")
        return 0
    if a.cmd == "doctor":
        exe = find_blender()
        ver = None
        if exe:
            out = subprocess.run([exe, "-b", "--factory-startup", "-v"], capture_output=True, text=True, errors="replace").stdout
            ver = next((ln.strip() for ln in out.splitlines() if ln.startswith("Blender")), None)
        py = None if exe else bpy_python()
        print(json.dumps({"status": "doctor", "blender": exe, "version": ver, "bpy_python": py, "ffmpeg": shutil.which("ffmpeg"),
                          "ready": bool(exe or py), "install": None if (exe or py) else
                          "download Blender from blender.org (portable zip is fine) and set KOSIF_BLENDER, or pip install bpy"},
                         ensure_ascii=False))
        return 0
    if a.cmd == "inventory":
        rec = run_inside({"cmd": "inventory", "out": str(Path(a.out).resolve())})
        print(json.dumps({"op": "inventory", "output": a.out, "metrics": rec.get("summary", {}), "verified": Path(a.out).exists()},
                         ensure_ascii=False))
        return 0
    out = Path(a.out).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    W, H = (int(v) for v in a.res.lower().split("x"))
    animated = a.frames > 1
    frames_dir = Path(tempfile.mkdtemp(prefix="kosif-frames-")) if animated else None
    job = {"cmd": "render", "preset": a.preset, "model": str(Path(a.model).resolve()) if a.model else None,
           "w": W, "h": H, "quality": a.quality, "samples": a.samples, "frames": a.frames, "fps": a.fps, "move": a.move,
           "device": a.device, "lens": a.lens, "fstop": a.fstop, "seed": a.seed,
           "save_blend": str(Path(a.save_blend).resolve()) if a.save_blend else None,
           "still": None if animated else str(out if out.suffix.lower() == ".png" else out.with_suffix(".png")),
           "frames_dir": str(frames_dir) if animated else None}
    t0 = time.time()
    try:
        rec = run_inside(job)
    except Exception as exc:
        print(json.dumps({"op": "render", "status": "error", "error": str(exc)[-1500:]}, ensure_ascii=False))
        return 1
    metrics = {k: rec.get(k) for k in ("preset", "engine", "device", "samples", "resolution", "view_transform", "look",
                                       "render_seconds", "runner", "warnings")}
    if animated:
        mp4 = encode_mp4(frames_dir, a.fps, out) if out.suffix.lower() == ".mp4" else None
        frames = sorted(frames_dir.glob("frame_*.png"))
        metrics.update(frames=len(frames), first_frame=measure_png(frames[0]) if frames else None)
        if not mp4:
            dest = out if out.suffix == "" else out.with_suffix("")
            dest.mkdir(parents=True, exist_ok=True)
            for fr in frames:
                shutil.copy2(fr, dest / fr.name)
            output = str(dest)
        else:
            output = mp4
        shutil.rmtree(frames_dir, ignore_errors=True)
        ok = len(frames) == a.frames and metrics["first_frame"] and max(metrics["first_frame"].get("std", [0])) > 2
    else:
        output = job["still"]
        metrics["image"] = measure_png(output) if Path(output).exists() else None
        ok = bool(metrics["image"]) and max(metrics["image"].get("std", [0])) > 2
    if a.save_blend:
        metrics["blend"] = a.save_blend if Path(a.save_blend).exists() else None
    metrics["total_seconds"] = round(time.time() - t0, 1)
    print(json.dumps({"op": "render", "output": output, "metrics": metrics, "verified": bool(ok)}, ensure_ascii=False, default=str))
    return 0 if ok else 1


# ====================================================================== inside Blender
def kelvin_rgb(k):
    """Approximate blackbody colour (Tanner Helland fit), linear-ish 0..1."""
    t = k / 100.0
    r = 255 if t <= 66 else 329.698727446 * ((t - 60) ** -0.1332047592)
    g = 99.4708025861 * math.log(t) - 161.1195681661 if t <= 66 else 288.1221695283 * ((t - 60) ** -0.0755148492)
    b = 255 if t >= 66 else (0 if t <= 19 else 138.5177312231 * math.log(t - 10) - 305.0447927307)
    srgb = [min(255, max(0, c)) / 255 for c in (r, g, b)]
    return [((c + 0.055) / 1.055) ** 2.4 if c > 0.04045 else c / 12.92 for c in srgb]


def inside(job):
    import bpy
    import bmesh
    from mathutils import Vector
    warnings = []
    if job["cmd"] == "inventory":
        return inventory(job)
    P = PRESETS[job["preset"]]
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    cy = sc.cycles

    # ---- device
    dev = "CPU"
    if job["device"] != "cpu":
        try:
            prefs = bpy.context.preferences.addons["cycles"].preferences
            for t in ("OPTIX", "CUDA", "HIP", "ONEAPI", "METAL"):
                try:
                    prefs.compute_device_type = t
                except TypeError:
                    continue
                prefs.refresh_devices()
                gpus = [d for d in prefs.devices if d.type == t]
                if gpus:
                    for d in prefs.devices:
                        d.use = d.type == t
                    cy.device, dev = "GPU", t
                    break
        except Exception as e:  # noqa: BLE001
            warnings.append(f"gpu probe: {e}")
    if dev == "CPU":
        cy.device = "CPU"

    # ---- sampling, light paths, denoise
    q = QUALITY[job["quality"]]
    cy.samples = job["samples"] or q["samples"]
    cy.use_adaptive_sampling = True
    cy.adaptive_threshold = 0.01 if job["quality"] == "final" else 0.05
    cy.use_denoising = True
    try:
        cy.denoiser = "OPENIMAGEDENOISE"
    except TypeError:
        warnings.append("OpenImageDenoise unavailable")
    cy.use_light_tree = True
    if dev == "CPU":
        cy.use_guiding = True
    cy.sample_clamp_indirect = 10.0
    cy.caustics_reflective = cy.caustics_refractive = False
    cy.max_bounces, cy.volume_bounces = 12, 2
    cy.seed = job["seed"]
    W, H = job["w"], job["h"]
    if P.get("aspect"):
        H = int(round(W / P["aspect"])) // 2 * 2
    sc.render.resolution_x, sc.render.resolution_y = W, H
    sc.render.resolution_percentage = q["pct"]
    sc.render.film_transparent = False

    # ---- colour management
    vs = sc.view_settings
    vs.view_transform = "AgX"
    for look in (P["look"], P["look"].replace("AgX - ", "")):
        try:
            vs.look = look
            break
        except TypeError:
            continue
    else:
        warnings.append(f"look {P['look']} not available")
    vs.exposure = P["exposure"]

    # ---- world
    world = bpy.data.worlds.new("KOSIF World")
    sc.world = world
    wt = world.node_tree
    bg = wt.nodes.get("Background") or wt.nodes.new("ShaderNodeBackground")
    wout = wt.nodes.get("World Output") or wt.nodes.new("ShaderNodeOutputWorld")
    if P.get("sky"):
        sky = wt.nodes.new("ShaderNodeTexSky")
        sky.sky_type = "MULTIPLE_SCATTERING"
        sky.sun_elevation = math.radians(P["sky"]["elevation"])
        sky.sun_rotation = math.radians(P["sky"]["rotation"])
        sky.sun_disc = True
        wt.links.new(sky.outputs[0], bg.inputs["Color"])
        bg.inputs["Strength"].default_value = 0.35
    else:
        bg.inputs["Color"].default_value = (*P["world"], 1)
        bg.inputs["Strength"].default_value = 1.0
    wt.links.new(bg.outputs[0], wout.inputs["Surface"])

    # ---- materials
    def material(name, kind):
        m = bpy.data.materials.new(name)
        nt = m.node_tree
        b = nt.nodes["Principled BSDF"]
        I = b.inputs
        presets = {
            "glossy-paint": dict(color=(0.55, 0.03, 0.04), metallic=0.0, rough=0.18, coat=1.0),
            "brushed-gold": dict(color=(1.0, 0.71, 0.29), metallic=1.0, rough=0.28, coat=0.0, aniso=0.6),
            "satin-black": dict(color=(0.02, 0.02, 0.02), metallic=0.0, rough=0.35, coat=0.6),
            "chrome": dict(color=(0.95, 0.95, 0.97), metallic=1.0, rough=0.06, coat=0.0),
            "studio-grey": dict(color=(0.18, 0.18, 0.19), metallic=0.0, rough=0.6, coat=0.0),
            "wet-asphalt": dict(color=(0.015, 0.015, 0.018), metallic=0.0, rough=0.07, coat=0.0),
            "ground": dict(color=(0.16, 0.12, 0.07), metallic=0.0, rough=0.9, coat=0.0),
            "matte-dark": dict(color=(0.01, 0.01, 0.012), metallic=0.0, rough=0.25, coat=0.0),
        }
        s = presets[kind]
        I["Base Color"].default_value = (*s["color"], 1)
        I["Metallic"].default_value = s["metallic"]
        I["Roughness"].default_value = s["rough"]
        I["Coat Weight"].default_value = s["coat"]
        if s.get("aniso"):
            I["Anisotropic"].default_value = s["aniso"]
        if kind == "wet-asphalt":    # puddles: roughness varies with a noise texture
            nz = nt.nodes.new("ShaderNodeTexNoise")
            nz.inputs["Scale"].default_value = 3.0
            ramp = nt.nodes.new("ShaderNodeMapRange")
            ramp.inputs["To Min"].default_value, ramp.inputs["To Max"].default_value = 0.02, 0.35
            nt.links.new(nz.outputs["Fac"], ramp.inputs["Value"])
            nt.links.new(ramp.outputs["Result"], I["Roughness"])
        return m

    def emissive(name, rgb, strength):
        m = bpy.data.materials.new(name)
        nt = m.node_tree
        b = nt.nodes["Principled BSDF"]
        b.inputs["Base Color"].default_value = (*rgb, 1)
        b.inputs["Emission Color"].default_value = (*rgb, 1)
        b.inputs["Emission Strength"].default_value = strength
        return m

    def assign(obj, mat):
        obj.data.materials.clear()
        obj.data.materials.append(mat)

    # ---- set
    def cyclorama(width=24, depth=14, height=10, radius=3.0, mat=None):
        me = bpy.data.meshes.new("Cyclorama")
        bm = bmesh.new()
        prof = [(-depth, 0.0)]
        for i in range(13):
            a = math.pi / 2 * i / 12
            prof.append((depth * 0.5 - radius + radius * math.sin(a), radius - radius * math.cos(a)))
        prof.append((depth * 0.5, height))
        rows = []
        for x in (-width / 2, width / 2):
            rows.append([bm.verts.new((x, y, z)) for (y, z) in prof])
        for i in range(len(prof) - 1):
            bm.faces.new((rows[0][i], rows[1][i], rows[1][i + 1], rows[0][i + 1]))
        bm.to_mesh(me)
        bm.free()
        ob = bpy.data.objects.new("Cyclorama", me)
        sc.collection.objects.link(ob)
        for poly in me.polygons:
            poly.use_smooth = True
        if mat:
            assign(ob, mat)
        return ob

    def plane(size, mat, z=0.0, name="Floor"):
        bpy.ops.mesh.primitive_plane_add(size=size, location=(0, 0, z))
        ob = bpy.context.active_object
        ob.name = name
        assign(ob, mat)
        return ob

    st = P["set"]
    if st == "cyclorama":
        cyclorama(mat=material("Backdrop", "studio-grey"))
    elif st == "ground":
        plane(400, material("Ground", "ground"))
    elif st == "wet-floor":
        plane(60, material("Wet floor", "wet-asphalt"))
    elif st == "ground-dark":
        plane(80, material("Dark floor", "matte-dark"))
    elif st == "room":
        plane(40, material("Floor", "satin-black"))
        bpy.ops.mesh.primitive_plane_add(size=40, location=(0, 8, 0), rotation=(math.radians(90), 0, 0))
        assign(bpy.context.active_object, material("Wall", "studio-grey"))

    # ---- subject
    subject_objs = []
    model = job.get("model")
    if model:
        ext = Path(model).suffix.lower()
        before = set(bpy.data.objects)
        try:
            if ext in (".glb", ".gltf"):
                bpy.ops.import_scene.gltf(filepath=model)
            elif ext == ".fbx":
                bpy.ops.import_scene.fbx(filepath=model)
            elif ext == ".obj":
                bpy.ops.wm.obj_import(filepath=model)
            elif ext == ".stl":
                bpy.ops.wm.stl_import(filepath=model)
            elif ext == ".ply":
                bpy.ops.wm.ply_import(filepath=model)
            elif ext in (".usd", ".usda", ".usdc", ".usdz"):
                bpy.ops.wm.usd_import(filepath=model)
            elif ext == ".abc":
                bpy.ops.wm.alembic_import(filepath=model)
            elif ext == ".blend":
                with bpy.data.libraries.load(model, link=False) as (src, dst):
                    dst.objects = list(src.objects)
                for ob in dst.objects:
                    if ob and ob.type not in ("CAMERA", "LIGHT"):
                        sc.collection.objects.link(ob)
            else:
                raise ValueError(f"unsupported model type {ext}")
        except Exception as e:  # noqa: BLE001
            warnings.append(f"model import failed: {e}")
        subject_objs = [o for o in bpy.data.objects if o not in before and o.type == "MESH"]
        for o in [o for o in bpy.data.objects if o not in before and o.type in ("CAMERA", "LIGHT")]:
            bpy.data.objects.remove(o)
    if not subject_objs:
        bpy.ops.mesh.primitive_monkey_add(size=2, location=(0, 0, 1))
        hero = bpy.context.active_object
        hero.name = "Hero"
        hero.rotation_euler = (math.radians(-12), 0, math.radians(18))
        mod = hero.modifiers.new("Subdivision", "SUBSURF")
        mod.levels = mod.render_levels = 2
        for poly in hero.data.polygons:
            poly.use_smooth = True
        assign(hero, material("Hero", P["material"]))
        subject_objs = [hero]
    # normalise: fit the subject in a 2 m box standing on the floor at the origin
    bpy.context.view_layer.update()
    pts = [o.matrix_world @ Vector(c) for o in subject_objs for c in o.bound_box]
    mn = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
    mx = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
    size = max((mx - mn).x, (mx - mn).y, (mx - mn).z, 1e-6)
    root = bpy.data.objects.new("Subject", None)
    sc.collection.objects.link(root)
    for o in subject_objs:
        if o.parent is None or o.parent not in subject_objs:
            o.parent = root
    s = 2.0 / size
    root.scale = (s, s, s)
    centre = (mn + mx) / 2
    root.location = (-centre.x * s, -centre.y * s, -mn.z * s)
    bpy.context.view_layer.update()
    target = bpy.data.objects.new("Focus", None)
    sc.collection.objects.link(target)
    front = (mn.y - centre.y) * s                   # focus halfway to the front face, where the eye looks first
    target.location = (0, front * 0.5, ((mx.z - mn.z) * s) * 0.5)

    # ---- lights
    def light(spec, i):
        ld = bpy.data.lights.new(f"Light {i}", spec["type"])
        ld.energy = spec["w"]
        try:
            ld.use_temperature = True
            ld.temperature = spec["k"]
        except AttributeError:
            ld.color = kelvin_rgb(spec["k"])
        ob = bpy.data.objects.new(f"Light {i}", ld)
        sc.collection.objects.link(ob)
        if spec["type"] == "SUN":
            el, rot = math.radians(spec["elev"]), math.radians(spec["rot"])
            ob.rotation_euler = (math.pi / 2 - el, 0, rot + math.pi)
            ld.angle = math.radians(spec.get("angle", 0.5))
        else:
            ob.location = spec["at"]
            tr = ob.constraints.new("TRACK_TO")
            tr.target, tr.track_axis, tr.up_axis = target, "TRACK_NEGATIVE_Z", "UP_Y"
            if spec["type"] == "AREA":
                ld.shape, ld.size = "DISK", spec["size"]
            if spec["type"] == "SPOT":
                ld.spot_size = math.radians(spec["spot"])
                ld.spot_blend = spec.get("blend", 0.25)
                ld.shadow_soft_size = 0.05
        return ob

    for i, spec in enumerate(P["lights"]):
        light(spec, i)
    if P.get("neon"):
        for j, (rgb, loc, rot) in enumerate([((1.0, 0.05, 0.6), (-2.2, 2.0, 1.4), (math.radians(90), 0, math.radians(-20))),
                                             ((0.0, 0.8, 1.0), (2.4, 1.6, 1.0), (0, math.radians(90), math.radians(30))),
                                             ((0.6, 0.1, 1.0), (0.0, 3.5, 2.6), (0, math.radians(90), 0))]):
            bpy.ops.mesh.primitive_torus_add(major_radius=0.9 if j == 0 else 1.2, minor_radius=0.035, location=loc, rotation=rot)
            assign(bpy.context.active_object, emissive(f"Neon {j}", rgb, 40))
    if P.get("bokeh_lights"):
        import random
        rnd = random.Random(job["seed"])
        for j in range(40):
            bpy.ops.mesh.primitive_uv_sphere_add(radius=0.05, location=(rnd.uniform(-9, 9), rnd.uniform(9, 22), rnd.uniform(0.3, 5)))
            warm = rnd.random() < 0.6
            assign(bpy.context.active_object, emissive(f"Bokeh {j}", (1.0, 0.55, 0.2) if warm else (0.3, 0.6, 1.0), rnd.uniform(30, 90)))
    if P.get("blinds"):
        slat = material("Blinds", "satin-black")
        for j in range(9):
            bpy.ops.mesh.primitive_cube_add(size=1, location=(-3.6, 1.8, 3.1 + j * 0.28 - 1.1))
            ob = bpy.context.active_object
            ob.scale = (0.05, 3.0, 0.07)
            ob.rotation_euler = (0, math.radians(-35), math.radians(-25))
            assign(ob, slat)
    if P.get("fog") or P.get("mist"):      # a bounded domain: a world volume is infinite and would swallow the sky
        big = bool(P.get("mist"))
        bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 6 if big else 4))
        dom = bpy.context.active_object
        dom.name, dom.scale = "Fog", ((80, 80, 12) if big else (24, 24, 8))
        fm = bpy.data.materials.new("Fog")
        nt = fm.node_tree
        for n in list(nt.nodes):
            if n.type == "BSDF_PRINCIPLED":
                nt.nodes.remove(n)
        vol = nt.nodes.new("ShaderNodeVolumePrincipled")
        vol.inputs["Density"].default_value = P.get("fog") or P["mist"]
        vol.inputs["Anisotropy"].default_value = 0.45
        if big:
            vol.inputs["Color"].default_value = (1.0, 0.85, 0.68, 1)
        nt.links.new(vol.outputs[0], nt.nodes["Material Output"].inputs["Volume"])
        assign(dom, fm)
        dom.visible_shadow = True

    # ---- camera
    cd = bpy.data.cameras.new("Camera")
    cd.lens = job.get("lens") or P["lens"]
    cd.sensor_width = 36
    cd.dof.use_dof = True
    cd.dof.focus_object = target
    cd.dof.aperture_fstop = job.get("fstop") or P["fstop"]
    cd.dof.aperture_blades = P["blades"]
    cd.dof.aperture_ratio = P["ratio"]
    cam = bpy.data.objects.new("Camera", cd)
    sc.collection.objects.link(cam)
    sc.camera = cam
    cam.location = P["cam"]
    tr = cam.constraints.new("TRACK_TO")
    tr.target, tr.track_axis, tr.up_axis = target, "TRACK_NEGATIVE_Z", "UP_Y"

    # ---- camera move
    n = job["frames"]
    sc.frame_start, sc.frame_end = 1, n
    sc.render.fps = job["fps"]
    if n > 1:
        sc.render.use_motion_blur = True
        sc.render.motion_blur_shutter = 0.5          # 180° shutter
        mv = job["move"]
        base = Vector(P["cam"])
        if mv == "orbit":
            rig = bpy.data.objects.new("Orbit", None)
            sc.collection.objects.link(rig)
            cam.parent = rig
            rig.rotation_euler = (0, 0, 0)
            rig.keyframe_insert("rotation_euler", index=2, frame=1)
            rig.rotation_euler[2] = math.radians(360 * (n - 1) / n)
            rig.keyframe_insert("rotation_euler", index=2, frame=n)
            curves = rig.animation_data.action
            linear_keys(curves)
        elif mv in ("dolly-in", "vertigo"):
            cam.location = base
            cam.keyframe_insert("location", frame=1)
            near = base.lerp(Vector((0, 0, 1)), 0.45)
            cam.location = near
            cam.keyframe_insert("location", frame=n)
            if mv == "vertigo":     # dolly zoom: focal length grows as the camera closes in, subject size stays put
                d0, d1 = (base - Vector((0, 0, 1))).length, (near - Vector((0, 0, 1))).length
                cd.lens = P["lens"] * 0.6
                cd.keyframe_insert("lens", frame=n)
                cd.lens = P["lens"] * 0.6 * d0 / d1
                cd.keyframe_insert("lens", frame=1)
        elif mv == "crane-up":
            cam.location = (base.x, base.y, 0.4)
            cam.keyframe_insert("location", frame=1)
            cam.location = (base.x, base.y * 0.85, 4.5)
            cam.keyframe_insert("location", frame=n)
        elif mv == "handheld":
            cam.constraints.remove(tr)
            cam.rotation_euler = (math.radians(80), 0, math.atan2(-base.x, base.y) + math.pi)
            cam.keyframe_insert("rotation_euler", frame=1)
            cam.keyframe_insert("rotation_euler", frame=n)
            add_noise(cam)

    # ---- compositor finishing (5.x node-group compositor)
    try:
        finish(sc, P["finish"])
        sc.render.use_compositing = True
    except Exception as e:  # noqa: BLE001
        warnings.append(f"compositor: {e}")

    # ---- render
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_depth = "8"
    t0 = time.time()
    if n > 1:
        sc.render.filepath = str(Path(job["frames_dir"]) / "frame_")
        sc.render.use_file_extension = True
        bpy.ops.render.render(animation=True)
        # Blender names frames frame_0001.png …
    else:
        sc.render.filepath = job["still"]
        bpy.ops.render.render(write_still=True)
    secs = round(time.time() - t0, 1)
    if job.get("save_blend"):
        bpy.ops.wm.save_as_mainfile(filepath=job["save_blend"], compress=True)
    return {"preset": job["preset"], "engine": sc.render.engine, "device": dev, "samples": cy.samples,
            "resolution": [sc.render.resolution_x * sc.render.resolution_percentage // 100,
                           sc.render.resolution_y * sc.render.resolution_percentage // 100],
            "view_transform": vs.view_transform, "look": vs.look, "render_seconds": secs, "warnings": warnings,
            "version": bpy.app.version_string}


def linear_keys(action):
    try:
        for fc in action.fcurves:
            for kp in fc.keyframe_points:
                kp.interpolation = "LINEAR"
    except AttributeError:    # 5.x layered actions
        for layer in action.layers:
            for strip in layer.strips:
                for bag in strip.channelbags:
                    for fc in bag.fcurves:
                        for kp in fc.keyframe_points:
                            kp.interpolation = "LINEAR"


def add_noise(ob):
    def fcurves(action):
        try:
            return list(action.fcurves)
        except AttributeError:
            return [fc for layer in action.layers for strip in layer.strips for bag in strip.channelbags for fc in bag.fcurves]
    for fc in fcurves(ob.animation_data.action):
        m = fc.modifiers.new("NOISE")
        m.scale, m.strength, m.phase = 18.0, 0.035, 7.0 * fc.array_index


def finish(sc, F):
    import bpy
    tree = bpy.data.node_groups.new("KOSIF Film Finish", "CompositorNodeTree")
    tree.interface.new_socket("Image", in_out="OUTPUT", socket_type="NodeSocketColor")
    N, L = tree.nodes, tree.links
    rl = N.new("CompositorNodeRLayers")
    cur = rl.outputs["Image"]
    if F.get("glare"):
        g = N.new("CompositorNodeGlare")
        g.inputs["Type"].default_value = F["glare"]
        g.inputs["Quality"].default_value = "High"
        g.inputs["Threshold"].default_value = F.get("glare_threshold", 0.8)
        g.inputs["Strength"].default_value = F.get("glare_strength", 0.3)
        if F["glare"] == "Streaks":
            g.inputs["Streaks"].default_value = F.get("streaks", 2)
            g.inputs["Streaks Angle"].default_value = 0.0
        L.new(cur, g.inputs["Image"])
        cur = g.outputs["Image"]
    if F.get("dispersion"):
        ld = N.new("CompositorNodeLensdist")
        ld.inputs["Dispersion"].default_value = F["dispersion"]
        ld.inputs["Distortion"].default_value = 0.0
        L.new(cur, ld.inputs["Image"])
        cur = ld.outputs["Image"]
    if F.get("grade"):
        cb = N.new("CompositorNodeColorBalance")
        lift, gamma, gain = F["grade"]
        # colour inputs follow the scalar inputs of the same name
        def colour_input(name):
            return [s for s in cb.inputs if s.name == name and s.type == "RGBA"][0]
        colour_input("Lift").default_value = (*lift, 1)
        colour_input("Gamma").default_value = (*gamma, 1)
        colour_input("Gain").default_value = (*gain, 1)
        L.new(cur, cb.inputs["Image"])
        cur = cb.outputs["Image"]
    if F.get("saturation") is not None:
        hs = N.new("CompositorNodeHueSat")
        hs.inputs["Saturation"].default_value = F["saturation"]
        L.new(cur, hs.inputs["Image"])
        cur = hs.outputs["Image"]
    if F.get("vignette"):
        em = N.new("CompositorNodeEllipseMask")
        em.inputs["Size"].default_value = (0.92, 0.92)
        bl = N.new("CompositorNodeBlur")
        bl.inputs["Size"].default_value = (220, 220)
        L.new(em.outputs["Mask"], bl.inputs["Image"])
        mix = N.new("ShaderNodeMix")
        mix.data_type, mix.blend_type = "RGBA", "MULTIPLY"
        rgba = [s for s in mix.inputs if s.type == "RGBA"]
        mix.inputs[0].default_value = F["vignette"]
        L.new(cur, rgba[0])
        L.new(bl.outputs["Image"], rgba[1])
        cur = [s for s in mix.outputs if s.type == "RGBA"][0]
    go = N.new("NodeGroupOutput")
    L.new(cur, go.inputs[0])
    sc.compositing_node_group = tree


def inventory(job):
    import bpy
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    pfx = lambda p: sorted(t for t in dir(bpy.types) if t.startswith(p))
    cam = bpy.data.cameras.new("C")
    w = bpy.data.worlds.new("W")
    sky = w.node_tree.nodes.new("ShaderNodeTexSky")
    enum = lambda o, p: [i.identifier for i in o.bl_rna.properties[p].enum_items]
    ops = {k: sorted(x for x in dir(getattr(bpy.ops, k)) if not x.startswith("_")) for k in dir(bpy.ops) if not k.startswith("_")}
    data = {
        "schema": "kosif.blender.inventory.v1", "version": bpy.app.version_string,
        "build_hash": bpy.app.build_hash.decode("ascii", "replace"),
        "operators_total": sum(map(len, ops.values())), "operators": ops,
        "types_total": len([t for t in dir(bpy.types) if not t.startswith("_")]),
        "shader_nodes": pfx("ShaderNode"), "compositor_nodes": pfx("CompositorNode"), "geometry_nodes": pfx("GeometryNode"),
        "texture_nodes": pfx("TextureNode"), "sky_types": enum(sky, "sky_type"), "camera_types": enum(cam, "type"),
        "panorama_types": enum(cam, "panorama_type"), "light_types": ["POINT", "SUN", "SPOT", "AREA"],
        "image_formats": enum(sc.render.image_settings, "file_format"), "ffmpeg_codecs": enum(sc.render.ffmpeg, "codec"),
        "ffmpeg_containers": enum(sc.render.ffmpeg, "format"),
        "cycles_settings": sorted(p.identifier for p in sc.cycles.bl_rna.properties),
        "addons_core": sorted(m.__name__ for m in __import__("addon_utils").modules()),
        "compositor_api": "scene.compositing_node_group (node-group compositor)" if hasattr(sc, "compositing_node_group") else "scene.node_tree",
        "limitations": "Registration and settings are not feature coverage; only render receipts prove a feature ran here.",
    }
    try:
        prefs = bpy.context.preferences.addons["cycles"].preferences
        prefs.refresh_devices()
        data["devices"] = [[d.name, d.type] for d in prefs.devices]
    except Exception as e:  # noqa: BLE001
        data["devices"] = str(e)
    Path(job["out"]).write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    return {"summary": {k: (len(v) if isinstance(v, (list, dict)) else v) for k, v in data.items()
                        if k not in ("schema", "limitations", "build_hash")}}


def inner_main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]
    job_path = Path(argv[argv.index("--job") + 1])
    job = json.loads(job_path.read_text(encoding="utf-8"))
    try:
        rec = inside(job)
    except Exception as exc:  # noqa: BLE001
        import traceback
        rec = {"error": f"{type(exc).__name__}: {exc}", "trace": traceback.format_exc()[-3000:]}
    Path(job["receipt"]).write_text(json.dumps(rec, ensure_ascii=False, default=str), encoding="utf-8")
    if "error" in rec:
        print(rec["trace"], file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    if "--job" in sys.argv and HAVE_BPY:
        inner_main()
    else:
        sys.exit(cli())
