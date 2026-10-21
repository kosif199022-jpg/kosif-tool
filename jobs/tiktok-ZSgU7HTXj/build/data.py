"""Builds film/data.js: lyrics (cleaned), who sings, gestures, the boss's reactions, stickers and zoom punches."""
import json, pathlib, sys
J = pathlib.Path(__file__).resolve().parents[1]
audio = json.load(open(J / "build" / "audio.json"))
lyr = json.load(open(J / "build" / "lyrics.json"))          # [{s, e, who, text}] cleaned by hand
words_src = json.load(open(J / "source" / lyr["words_file"]))
INTRO_END = lyr["intro_end"]

phrases = []
for k, p in enumerate(lyr["phrases"]):
    toks = p["text"].split()
    ws = [w for w in words_src if w["s"] >= p["s"] - .05 and w["s"] < p["e"] - .05]
    # spread the cleaned words over the recognised word times (same count -> 1:1, else even split)
    if len(ws) == len(toks):
        tw = [{"w": t, "s": w["s"], "e": w["e"]} for t, w in zip(toks, ws)]
    else:
        d = (p["e"] - p["s"]) / len(toks)
        tw = [{"w": t, "s": round(p["s"] + i * d, 3), "e": round(p["s"] + (i + 1) * d, 3)} for i, t in enumerate(toks)]
    phrases.append({"s": p["s"], "e": p["e"], "who": p["who"], "tilt": (-.03 if k % 2 else .03), "words": tw})

# gestures for the kid: point on "انت", temple on "فاكر", wag on "مافي", open palm otherwise; bottle where he holds one
gestures = []
for ph in phrases:
    if ph["who"] != "kid": continue
    txt = " ".join(w["w"] for w in ph["words"])
    kind = "temple" if "فاكر" in txt else "wag" if "مافي" in txt else "point" if "انت" in txt or "إنت" in txt else "open"
    gestures.append({"s": ph["s"], "e": ph["e"] - .1, "kind": kind})
for a, b in lyr.get("bottle", []):
    gestures = [g for g in gestures if g["e"] <= a or g["s"] >= b] + [{"s": a, "e": b, "kind": "bottle"}]
gestures.sort(key=lambda g: g["s"])

json.dump({"duration": lyr["duration"], "introEnd": INTRO_END, "rms": audio["rms"], "beats": audio["beats"],
           "phrases": phrases, "gestures": gestures, "boss": lyr["boss"], "stickers": lyr["stickers"], "punches": lyr["punches"]},
          open(J / "film" / "data.json", "w"), ensure_ascii=False)
(J / "film" / "data.js").write_text("window.DATA=" + (J / "film" / "data.json").read_text() + ";\n")
print(len(phrases), "phrases,", len(gestures), "gestures", file=sys.stderr)
