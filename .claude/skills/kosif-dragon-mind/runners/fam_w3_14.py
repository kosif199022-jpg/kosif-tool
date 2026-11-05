"""Wave 3, chunk 14: mixed-family power cards (atlas data/docs, agents, mind, strategy, web, checks, code, footage,
products, retro look, KOSIF tools) as real programs with known-answer checks and negative controls.

Engines used (all local, nothing is spent, nothing leaves the work folder):
duckdb (python), mongomock, chromadb (explicit embeddings, no model download), hypothesis, pandera (pandas + polars),
ortools CP-SAT, PuLP (HiGHS), MuJoCo, quantstats, genanki, rembg with the 4.6 MB u2netp model (~/.u2net/u2netp.onnx),
python-docx, librosa, numpy/PIL, ffmpeg/ffprobe, tmux (private socket inside the work folder), Mermaid CLI (mmdc) with the
system Chrome, Playwright + Chromium, GSAP, the HyperFrames CLI (media-treatment, add, snapshot), the Slidev parser and
KaTeX from @slidev/cli, node `docx`, the reference MCP filesystem server via the python `mcp` client, the Claude Code CLI
(`claude plugin ...` inside a private HOME), and the repo's own programs: skill_intelligence.py, fusionforge.py,
mimic/mm_analyze.py, the kosif-montage-motion studio_import.py / reel.py, tools/kosif.py scaffold, tools/render_html.cjs
and tools/a-shell/Cinema_C_V34_Studio_iPhone.sh.

Installed for this module into the user environment (small, the real engines the cards name):
  pip install mongomock genanki mujoco quantstats
  npm i -g @modelcontextprotocol/server-filesystem
  curl -L -o ~/.u2net/u2netp.onnx https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2netp.onnx  (4.6 MB)
"""
import json
import math
import os
import re
import shutil
import sqlite3
import subprocess
import sys
import threading
import time
import zipfile
from pathlib import Path

from _harness import card, check, fx, sha

REPO = Path(__file__).resolve().parents[4]
SP = REPO / ".claude/skills/kosif-superpowers"
SPS = SP / "scripts"
MM = SP / "vendor/100-superskills/skills/kosif-montage-motion/scripts"
NM = Path("/opt/node22/lib/node_modules")
NODE = shutil.which("node") or "/opt/node22/bin/node"
CHROME = next((p for p in ("/usr/bin/google-chrome", "/usr/bin/chromium", "/usr/bin/chromium-browser") if Path(p).exists()), None)
HF = shutil.which("hyperframes") or "/opt/node22/bin/hyperframes"
FONT = next((p for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                         "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf") if Path(p).exists()), None)

GAPS = {
    "ADATA-41": "Milvus/Zilliz administration (databases, users, roles, privileges, cloud ACL/projects) needs a running "
                "Milvus server or a Zilliz Cloud account; Milvus Lite has no databases, users or roles, so nothing honest "
                "can run here",
    "AGENT-34": "installing ECC pulls a third-party harness (hundreds of skills/hooks) from npm/GitHub into the user's "
                "Claude Code configuration; it needs the user's consent and writes outside the work folder, and a fresh "
                "download per run would not fit the 15 s budget",
    "AGENT-36": "llama.cpp needs a GGUF model of 0.5-5 GB and the model host (huggingface.co) is blocked by the proxy here (403)",
    "AMIND-56": "the card's core is fetching and reading real arXiv papers; export.arxiv.org does not resolve from this "
                "container (no network for that host)",
    "ASTRAT-55": "Google Classroom through the gws CLI is a live Google service that needs the user's OAuth sign-in",
    "AWEB-01": "a third-party YouTube proxy API with its own key (live service); nothing to run offline",
    "FOOT-57": "Basma AutoEdit needs the Basma app with its AI keys and stock APIs (Pexels/Pixabay keys blocked here)",
    "TOOL-84": "the Remotion starter renders, but a cold Remotion webpack bundle + Chrome still took 27.8 s here "
               "(measured 2026-11-04), over the 15 s runner budget; a warm cache would sit outside the work folder",
}


# ----------------------------------------------------------------------------------------------- helpers


def _np():
    import numpy as np
    return np


def jw(path, obj):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(obj, ensure_ascii=False, indent=1), encoding="utf-8")
    return Path(path)


def tw(path, text):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(text, encoding="utf-8")
    return Path(path)


def sh(cmd, cwd=None, env=None, timeout=60, input=None, ok=(0,)):
    done = subprocess.run([str(c) for c in cmd], capture_output=True, text=True, timeout=timeout, cwd=str(cwd) if cwd else None,
                          env=env, input=input, stdin=None if input is not None else subprocess.DEVNULL)
    if ok is not None and done.returncode not in ok:
        raise RuntimeError("command failed (%d): %s" % (done.returncode, (done.stderr or done.stdout)[-600:]))
    return done


def node_env(**extra):
    e = dict(os.environ)
    e["NODE_PATH"] = str(NM)
    e["PATH"] = str(Path(NODE).parent) + ":" + e.get("PATH", "/usr/bin:/bin")
    if CHROME:
        e.setdefault("CHROME_PATH", CHROME)
        e.setdefault("PUPPETEER_EXECUTABLE_PATH", CHROME)
    e.update({k: str(v) for k, v in extra.items()})
    return e


def node_js(wd, name, js, timeout=60, args=()):
    src = tw(Path(wd) / (name + ".cjs"), js)
    done = sh([NODE, src, *args], cwd=wd, env=node_env(), timeout=timeout)
    return json.loads(done.stdout.strip().splitlines()[-1])


def py_env(wd):
    e = dict(os.environ)
    e["TMPDIR"] = str(Path(wd) / "tmp")
    (Path(wd) / "tmp").mkdir(exist_ok=True)
    return e


def load_png(path):
    from PIL import Image
    return _np().asarray(Image.open(path).convert("RGB")).astype(float)


def save_png(arr, path):
    from PIL import Image
    Image.fromarray(_np().clip(arr, 0, 255).round().astype("uint8")).save(path)
    return Path(path)


def write_video(path, frames, fps=30):
    np = _np()
    frames = list(frames)
    h, w = frames[0].shape[:2]
    p = subprocess.Popen(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
                          "-s", "%dx%d" % (w, h), "-r", str(fps), "-i", "-", "-c:v", "libx264rgb", "-qp", "0",
                          "-preset", "ultrafast", str(path)], stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    for f in frames:
        p.stdin.write(np.clip(f, 0, 255).round().astype("uint8").tobytes())
    p.stdin.close()
    if p.wait():
        raise RuntimeError("ffmpeg encode failed: %s" % p.stderr.read().decode(errors="replace")[-300:])
    return Path(path)


def read_video(path):
    np = _np()
    st = [s for s in fx.probe(path)["streams"] if s.get("codec_type") == "video"][0]
    w, h = int(st["width"]), int(st["height"])
    out = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                         capture_output=True, timeout=120, stdin=subprocess.DEVNULL).stdout
    return np.frombuffer(out, dtype=np.uint8).reshape(-1, h, w, 3).astype(float)


def lufs(path):
    """Integrated loudness (EBU R128) of a file's first audio stream, by ffmpeg ebur128."""
    done = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-map", "0:a:0", "-af", "ebur128", "-f", "null", "-"],
                          capture_output=True, text=True, timeout=60, stdin=subprocess.DEVNULL)
    m = re.findall(r"I:\s+(-?[\d.]+) LUFS", done.stderr)
    return float(m[-1]) if m else None


def vstream(path):
    return [s for s in fx.probe(path)["streams"] if s.get("codec_type") == "video"][0]


def duration(path):
    return float(fx.probe(path)["format"]["duration"])


class _Serve:
    """Serve a folder on 127.0.0.1 in a thread (local fixtures only)."""

    def __init__(self, root):
        import functools
        import http.server
        h = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(root))
        h.log_message = lambda *a, **k: None
        self.srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), h)
        self.url = "http://127.0.0.1:%d" % self.srv.server_address[1]
        threading.Thread(target=self.srv.serve_forever, daemon=True).start()

    def close(self):
        self.srv.shutdown()
        self.srv.server_close()


def three_shot_clip(path, size="180x320", sec=1.0, audio=None):
    """Three visually distinct shots (testsrc2 / mandelbrot / smptebars) joined by hard cuts at sec and 2*sec."""
    w, h = size.split("x")
    args = ["-f", "lavfi", "-i", "testsrc2=s=%s:r=30:d=%s" % (size, sec), "-f", "lavfi", "-i", "mandelbrot=s=%s:r=30" % size,
            "-f", "lavfi", "-i", "smptebars=s=%s:r=30:d=%s" % (size, sec)]
    fc = "[1]trim=duration=%s,setpts=PTS-STARTPTS[m];[0][m][2]concat=n=3:v=1[v]" % sec
    maps = ["-map", "[v]"]
    if audio:
        args += ["-i", str(audio)]
        maps += ["-map", "3:a", "-c:a", "aac", "-shortest"]
    fx.ffmpeg(*args, "-filter_complex", fc, *maps, "-pix_fmt", "yuv420p", "-c:v", "libx264", "-crf", "16", str(path))
    return Path(path)


# ================================================================================ ADATA: lakehouse, DuckDB, MongoDB

_ORDERS = ("order_id,ts,amount,country\n1,2026-01-01 10:00:00,10.00,EG\n2,2026-01-01 11:00:00,20.00,SA\n"
           "2,2026-01-01 11:00:00,20.00,SA\n3,2026-01-02 09:00:00,5.50,EG\n4,2026-01-02 09:30:00,n/a,SA\n"
           "5,2026-01-02 12:00:00,7.25,SA\n")


def choose_ingestion(src, freshness_min):
    """Match the ingestion method to the source, backward from the freshness SLO (ADATA-33 step 3)."""
    if src["kind"] == "operational-db" and (src.get("cdc") or freshness_min < 15):
        return "mirroring"
    if src["kind"] == "jdbc":
        return "jdbc-import"
    if src.get("transforms") == "complex" or src.get("orchestration"):
        return "pipeline"
    if src.get("lowcode"):
        return "dataflow"
    if src["kind"] in ("files", "object-store"):
        return "copy-job"
    return "pipeline"


@card("ADATA-33")
def medallion_lakehouse(task, wd):
    """Medallion design backward from the stated query + freshness SLO: bronze keeps raw rows with lineage, silver
    types, de-duplicates and quarantines, gold serves exactly the stated query; ingestion method per source by rule;
    every layer written as Parquet; trade-offs documented. Engine: DuckDB."""
    import duckdb
    raw = tw(wd / "landing" / "orders_2026-01.csv", _ORDERS)
    slo = {"queries": ["daily revenue per country"], "freshness_minutes": 60}
    con = duckdb.connect(str(wd / "lake.duckdb"))
    for s in ("bronze", "silver", "gold"):
        con.execute("CREATE SCHEMA %s" % s)
    con.execute("CREATE TABLE bronze.orders AS SELECT *, TIMESTAMP '2026-01-03 00:00:00' AS _ingested_at, ? AS _source "
                "FROM read_csv(?, all_varchar=true, header=true)", [raw.name, str(raw)])
    con.execute("CREATE TABLE silver.quarantine AS SELECT *, 'amount not numeric' AS reason FROM bronze.orders "
                "WHERE TRY_CAST(amount AS DECIMAL(12,2)) IS NULL")
    con.execute("CREATE TABLE silver.orders AS SELECT CAST(order_id AS INT) order_id, CAST(ts AS TIMESTAMP) ts, "
                "CAST(amount AS DECIMAL(12,2)) amount, country FROM (SELECT *, row_number() OVER (PARTITION BY order_id "
                "ORDER BY _ingested_at DESC) rn FROM bronze.orders WHERE TRY_CAST(amount AS DECIMAL(12,2)) IS NOT NULL) WHERE rn = 1")
    con.execute("CREATE TABLE gold.daily_revenue AS SELECT CAST(ts AS DATE) AS day, country, SUM(amount) AS revenue, "
                "COUNT(*) AS orders FROM silver.orders GROUP BY ALL ORDER BY ALL")
    for t in ("bronze.orders", "silver.orders", "gold.daily_revenue"):
        con.execute("COPY %s TO '%s' (FORMAT parquet)" % (t, wd / (t.replace(".", "_") + ".parquet")))
    n_b = con.execute("SELECT count(*) FROM bronze.orders").fetchone()[0]
    n_s = con.execute("SELECT count(*) FROM silver.orders").fetchone()[0]
    n_q = con.execute("SELECT count(*) FROM silver.quarantine").fetchone()[0]
    gold = [(str(d), c, float(r)) for d, c, r, _ in con.execute("SELECT * FROM gold.daily_revenue").fetchall()]
    total = float(con.execute("SELECT SUM(revenue) FROM gold.daily_revenue").fetchone()[0])
    naive = float(con.execute("SELECT SUM(TRY_CAST(amount AS DECIMAL(12,2))) FROM bronze.orders").fetchone()[0])
    pq = con.execute("SELECT count(*) FROM read_parquet('%s')" % (wd / "gold_daily_revenue.parquet")).fetchone()[0]
    con.close()
    sources = {"pos_db": {"kind": "operational-db", "cdc": True}, "partner_csv": {"kind": "files"},
               "crm_saas": {"kind": "saas", "lowcode": True}, "legacy_erp": {"kind": "jdbc"},
               "clickstream": {"kind": "object-store", "transforms": "complex"}}
    picks = {k: choose_ingestion(v, slo["freshness_minutes"]) for k, v in sources.items()}
    want_picks = {"pos_db": "mirroring", "partner_csv": "copy-job", "crm_saas": "dataflow", "legacy_erp": "jdbc-import",
                  "clickstream": "pipeline"}
    design = tw(wd / "design.md", "# Medallion design\n\nQuery: %s; freshness SLO %d min.\n\n| layer | earns its place because |\n|---|---|\n"
                "| bronze | raw replay + lineage (_source, _ingested_at) |\n| silver | typed, de-duplicated by order_id, bad rows quarantined |\n"
                "| gold | serves exactly the stated query |\n\nIngestion: %s\n\nTables: Parquet here; in production managed Delta/Iceberg "
                "with compaction. Trade-off: mirroring is freshest but costs a CDC slot; copy jobs are cheapest for files.\n"
                % (slo["queries"][0], slo["freshness_minutes"], json.dumps(picks)))
    want_gold = [("2026-01-01", "EG", 10.0), ("2026-01-01", "SA", 20.0), ("2026-01-02", "EG", 5.5), ("2026-01-02", "SA", 7.25)]
    return [
        check("bronze keeps every raw row", n_b == 6, n_b, 6),
        check("silver: duplicate removed and bad amount quarantined", (n_s, n_q) == (4, 1), [n_s, n_q], [4, 1]),
        check("gold answers the stated query exactly", gold == want_gold, gold, want_gold),
        check("gold revenue total", abs(total - 42.75) < 1e-9, total, 42.75),
        check("ingestion method per source matches the rules", picks == want_picks, picks, want_picks),
        check("gold Parquet reads back", pq == 4, pq, 4),
        check("negative control: revenue straight from bronze is wrong (duplicates counted)", abs(naive - 42.75) > 1, naive, "!= 42.75"),
    ], [design, wd / "gold_daily_revenue.parquet", wd / "lake.duckdb"]


@card("ADATA-39")
def duckdb_attach_query(task, wd):
    """DuckDB: resolve + check the db path, validate with PRAGMA version, list duckdb_tables()/columns/row counts,
    persist a state.sql (ATTACH + view + macro) and reuse it in a fresh session, and query CSV, Parquet and JSON files."""
    import duckdb
    csv = tw(wd / "clips.csv", "id,name,seconds,fps\n1,intro,8,30\n2,body,42,30\n3,outro,12,29\n4,teaser,15,60\n")
    tw(wd / "events.json", "".join(json.dumps({"clip": i % 4 + 1, "views": 10 * i}) + "\n" for i in range(1, 9)))
    db = (wd / "analytics.duckdb").resolve()
    cli = shutil.which("duckdb")
    con = duckdb.connect(str(db))
    ver = con.execute("PRAGMA version").fetchone()[0]
    con.execute("CREATE TABLE clips AS SELECT * FROM read_csv(?)", [str(csv)])
    con.execute("COPY clips TO '%s' (FORMAT parquet)" % (wd / "clips.parquet"))
    tables = con.execute("SELECT table_name, estimated_size FROM duckdb_tables()").fetchall()
    cols = con.execute("SELECT column_name, data_type FROM duckdb_columns() WHERE table_name = 'clips' ORDER BY column_index").fetchall()
    rows = con.execute("SELECT count(*) FROM clips").fetchone()[0]
    con.close()
    state = tw(wd / "state.sql", "ATTACH '%s' AS a (READ_ONLY);\nCREATE OR REPLACE TEMP VIEW long_clips AS SELECT * FROM a.clips WHERE seconds > 10;\n"
                                 "CREATE OR REPLACE TEMP MACRO fps_ok(f) AS f IN (24, 25, 30, 60);\n" % db)
    c2 = duckdb.connect()
    c2.execute(state.read_text())
    n_long = c2.execute("SELECT count(*) FROM long_clips").fetchone()[0]
    bad_fps = c2.execute("SELECT list(name) FROM a.clips WHERE NOT fps_ok(fps)").fetchone()[0]
    pq_sum = c2.execute("SELECT sum(seconds) FROM read_parquet(?)", [str(wd / "clips.parquet")]).fetchone()[0]
    js = c2.execute("SELECT c.name, sum(e.views) v FROM read_json_auto(?) e JOIN a.clips c ON c.id = e.clip GROUP BY 1 ORDER BY 2 DESC",
                    [str(wd / "events.json")]).fetchall()
    c2.close()
    c3 = duckdb.connect()
    try:
        c3.execute("SELECT count(*) FROM long_clips")
        fresh_failed = False
    except duckdb.Error:
        fresh_failed = True
    c3.close()
    rep = jw(wd / "duckdb_report.json", {"version": ver, "cli_on_path": bool(cli), "tables": tables, "columns": cols, "rows": rows,
                                         "long_clips": n_long, "bad_fps": bad_fps, "parquet_seconds": pq_sum, "views_by_clip": js})
    return [
        check("db path resolved and exists", db.is_file(), str(db), "exists"),
        check("PRAGMA version answers", str(ver).startswith("v"), ver, "v*"),
        check("duckdb_tables lists clips with 4 rows", [t[0] for t in tables] == ["clips"] and rows == 4, [tables, rows], "clips, 4"),
        check("columns and types", cols == [("id", "BIGINT"), ("name", "VARCHAR"), ("seconds", "BIGINT"), ("fps", "BIGINT")], cols, "id,name,seconds,fps"),
        check("state.sql reused: view over the attached db", n_long == 3, n_long, 3),
        check("state.sql macro flags the 29 fps clip", bad_fps == ["outro"], bad_fps, ["outro"]),
        check("read_parquet sum of seconds", pq_sum == 77, pq_sum, 77),
        check("read_json join: views per clip", js[0] == ("intro", 120), js, "intro 120 first"),
        check("negative control: a fresh session without state.sql has no view", fresh_failed, fresh_failed, True),
    ], [rep, state, db]


def _mongo_fixture():
    import datetime as dt
    cities = ["Cairo", "Riyadh", "Dubai"]
    base = dt.datetime(2026, 1, 1)
    return [{"_id": i, "city": cities[i % 3], "total": (i * 37) % 250, "created": base + dt.timedelta(days=i),
             "items": [{"sku": "S%d" % (i % 5), "qty": 1 + i % 3}] * (1 + i % 4), "customer_id": 1000 + i % 7} for i in range(60)]


_SYN = {"date": "created", "newest": "created", "revenue": "total", "amount": "total"}


def nl_to_mongo(request, schema):
    """Translate a request of the supported shapes into a read-only find or aggregation, validating every field."""
    r = request.lower().strip()
    m = re.match(r"orders in (\w+) with (\w+) over (\d+),? (newest|oldest) first", r)
    if m:
        city, field, n, order = m.groups()
        field = _SYN.get(field, field)
        used = ["city", field, "created"]
        missing = [f for f in used if f not in schema]
        if missing:
            return {"error": "unknown field(s): %s" % missing}
        return {"kind": "find", "filter": {"city": city.capitalize(), field: {"$gt": int(n)}},
                "sort": [("created", -1 if order == "newest" else 1)], "limit": 10, "fields": used}
    m = re.match(r"(?:sum|total) of (\w+) per (\w+)", r)
    if m:
        f, g = (_SYN.get(x, x) for x in m.groups())
        missing = [x for x in (f, g) if x not in schema]
        if missing:
            return {"error": "unknown field(s): %s" % missing}
        return {"kind": "aggregate", "pipeline": [{"$group": {"_id": "$" + g, "sum": {"$sum": "$" + f}}}, {"$sort": {"_id": 1}}],
                "fields": [f, g]}
    return {"error": "unsupported request shape"}


@card("ADATA-42")
def nl_to_mongodb(task, wd):
    """List dbs/collections, read indexes, sample the schema (sampleSize 50) and 4 docs, validate every field, emit a
    read-only find (or an aggregation only for grouping), check the index covers it, and advise embed vs reference.
    Engine: mongomock (an in-memory MongoDB API)."""
    import mongomock
    docs = _mongo_fixture()
    cl = mongomock.MongoClient()
    col = cl["shop"]["orders"]
    col.insert_many(docs)
    col.create_index([("city", 1), ("created", -1)], name="city_created")
    dbs, colls = cl.list_database_names(), cl["shop"].list_collection_names()
    idx = col.index_information()
    sample = list(col.find({}).limit(50))
    schema = {}
    for d in sample:
        for k, v in d.items():
            schema.setdefault(k, set()).add(type(v).__name__)
    head4 = list(col.find({}, limit=4))
    q1 = nl_to_mongo("orders in Cairo with total over 100, newest first", schema)
    got1 = [d["_id"] for d in col.find(q1["filter"]).sort(q1["sort"]).limit(q1["limit"])]
    want1 = sorted([d["_id"] for d in docs if d["city"] == "Cairo" and d["total"] > 100], key=lambda i: -i)[:10]
    keys = [k for k, _ in idx["city_created"]["key"]]
    uses_index = keys[:1] == ["city"] and "created" in keys
    q2 = nl_to_mongo("total of revenue per city", schema)
    got2 = {d["_id"]: d["sum"] for d in col.aggregate(q2["pipeline"])}
    want2 = {}
    for d in docs:
        want2[d["city"]] = want2.get(d["city"], 0) + d["total"]
    read_only = not any(k in json.dumps(q2["pipeline"]) for k in ("$out", "$merge"))
    max_items = max(len(d["items"]) for d in sample)
    advice = {"items": "embed (bounded array, max %d, read with the order)" % max_items if max_items <= 20 else "reference",
              "customer_id": "reference (shared across orders)"}
    bad = nl_to_mongo("orders in Cairo with price over 100, newest first", schema)
    rep = jw(wd / "mongo_plan.json", {"dbs": dbs, "collections": colls, "indexes": {k: v["key"] for k, v in idx.items()},
                                      "schema": {k: sorted(v) for k, v in schema.items()}, "q1": {k: v for k, v in q1.items()},
                                      "q1_ids": got1, "q2": q2, "q2_result": got2, "advice": advice, "rejected": bad}, )
    return [
        check("database and collection listed", "shop" in dbs and colls == ["orders"], [dbs, colls], "shop/orders"),
        check("schema sampled from 50 docs has every field", len(sample) == 50 and set(schema) == {"_id", "city", "total", "created", "items", "customer_id"},
              sorted(schema), "6 fields"),
        check("4-doc preview", len(head4) == 4, len(head4), 4),
        check("request 1 became a find (no aggregation needed)", q1.get("kind") == "find", q1.get("kind"), "find"),
        check("find returns the known Cairo orders, newest first", got1 == want1, got1, want1),
        check("the compound index city_created serves filter + sort", uses_index, keys, ["city", "created"]),
        check("grouping request became an aggregation with known sums", q2.get("kind") == "aggregate" and got2 == want2, got2, want2),
        check("pipeline is read-only (no $out/$merge)", read_only, read_only, True),
        check("embed-vs-reference advice from measured array size", advice["items"].startswith("embed"), advice, "embed items"),
        check("negative control: an unknown field (price) is rejected", "error" in bad, bad, "error"),
    ], [rep]


# ================================================================================ ADOCS: diagrams, plans, docs, articles, decks

def _pp(wd):
    return jw(wd / "puppeteer.json", {"executablePath": CHROME, "args": ["--no-sandbox"]})


def _balance(src):
    """Fix the commonest Mermaid parse error: a node label left unclosed on its line."""
    out = []
    for line in src.splitlines():
        for o, c in (("[", "]"), ("(", ")"), ("{", "}")):
            line += c * max(0, line.count(o) - line.count(c))
        out.append(line)
    return "\n".join(out) + "\n"


@card("ADOCS-21")
def mermaid_render_loop(task, wd):
    """Write .mmd, render with mmdc, on a parse error fix the syntax and rerun until it compiles; embed the fenced
    block in Markdown next to the versioned source."""
    src = "flowchart LR\n  U[User] -->|uploads clip| A[API\n  A -->|queues job| W[Render worker]\n  W -->|writes mp4| S[(Storage)]\n"
    pp = _pp(wd)
    attempts = []
    cur = src
    for i in range(3):
        f = tw(wd / ("diagram_v%d.mmd" % i), cur)
        out = wd / "diagram.svg"
        done = subprocess.run(["mmdc", "-i", str(f), "-o", str(out), "-p", str(pp), "-q"], capture_output=True, text=True,
                              timeout=60, stdin=subprocess.DEVNULL, env=node_env())
        err = (done.stderr or "")
        attempts.append({"try": i, "rc": done.returncode, "parse_error": "Parse error" in err or "Expecting" in err})
        if done.returncode == 0 and out.exists():
            break
        cur = _balance(cur)
    svg = (wd / "diagram.svg").read_text(encoding="utf-8") if (wd / "diagram.svg").exists() else ""
    labels = ["uploads clip", "queues job", "writes mp4", "Render worker", "Storage"]
    md = tw(wd / "README.md", "# Render flow\n\n```mermaid\n%s```\n" % cur)
    return [
        check("first render failed with a parse error", attempts[0]["rc"] != 0 and attempts[0]["parse_error"], attempts[0], "rc!=0, parse error"),
        check("fixed source compiled within 3 tries", attempts[-1]["rc"] == 0 and len(attempts) <= 3, attempts, "last rc 0"),
        check("SVG holds every node and edge label", all(l in svg for l in labels), [l in svg for l in labels], True),
        check("Markdown embeds the fenced mermaid block of the fixed source", ("```mermaid\n" + cur) in md.read_text(encoding="utf-8"), True, True),
        check("negative control: the original source is still unbalanced", _balance(src) != src, True, True),
    ], [wd / "diagram.svg", md]


_PLAN = """# Plan: upload-to-render service

## TL;DR
Users upload a clip, we render it in the background and send a link when it is ready.

## Summary
Today renders run on the web server and block it. We move them to a worker. The page stays fast. Nothing changes for users except speed.

## Inventory
- Components: upload page, API, render worker, storage
- Schema: jobs(id, status, file, created)
- Endpoints: POST /jobs, GET /jobs/{id}

## Architecture
```mermaid
flowchart LR
  U[User] -->|uploads clip| A[API]
  A -->|queues job| W[Render worker]
  W -->|writes mp4| S[(Storage)]
  A -->|sends link| U
```

## Key changes
- A job table records every render.
- A worker renders one job at a time.
- The user gets a link by email when the job is done.
"""

_JARGON = ("idempotent", "sharding", "k8s", "rpc", "refactor", "orm")


def plan_lint(md):
    f = []
    heads = re.findall(r"^##\s+(.+)$", md, re.M)
    for need in ("TL;DR", "Summary", "Inventory", "Architecture", "Key changes"):
        if need not in heads:
            f.append("missing section " + need)
    tl = re.search(r"## TL;DR\n(.+?)\n\n", md, re.S)
    if tl and len(tl.group(1).split()) > 40:
        f.append("TL;DR over 40 words")
    prose = re.sub(r"```.*?```", "", md, flags=re.S)
    for s in re.split(r"(?<=[.!?])\s+|\n", prose):
        if len(s.split()) > 25:
            f.append("sentence over 25 words")
    for j in _JARGON:
        if re.search(r"\b%s\b" % j, prose, re.I):
            f.append("jargon: " + j)
    if "```mermaid" not in md:
        f.append("no mermaid architecture")
    return f


_COMMENT_SERVER = r"""
const http=require('http'),fs=require('fs'),path=require('path');const root=process.argv[2];const store=path.join(root,'comments.json');
fs.writeFileSync(store,'[]');
const srv=http.createServer((req,res)=>{ if(req.url==='/api/comments'&&req.method==='POST'){let b='';req.on('data',d=>b+=d);req.on('end',()=>{
  const all=JSON.parse(fs.readFileSync(store,'utf8'));all.push(JSON.parse(b));fs.writeFileSync(store,JSON.stringify(all));res.end('{"ok":true}');});return;}
 if(req.url==='/api/comments'){res.setHeader('content-type','application/json');res.end(fs.readFileSync(store));return;}
 const f=path.join(root,req.url==='/'?'plan.html':decodeURIComponent(req.url.slice(1)));
 if(!f.startsWith(root)||!fs.existsSync(f)){res.statusCode=404;res.end();return;} res.end(fs.readFileSync(f));});
srv.listen(0,'127.0.0.1',()=>{console.log('PORT '+srv.address().port);});
"""


@card("ADOCS-24")
def visual_plan_review(task, wd):
    """Write the plan as Markdown (TL;DR, summary, inventory, mermaid architecture, key changes) for a non-developer,
    lint it, render the diagram (mmdc) and the page (pandoc), serve it with a local node server and collect comments."""
    import urllib.request
    op = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    md = tw(wd / "plan.md", _PLAN)
    findings = plan_lint(_PLAN)
    mmd = tw(wd / "arch.mmd", re.search(r"```mermaid\n(.*?)```", _PLAN, re.S).group(1))
    sh(["mmdc", "-i", mmd, "-o", wd / "arch.svg", "-p", _pp(wd), "-q"], env=node_env(), timeout=60)
    page_md = tw(wd / "plan_page.md", re.sub(r"```mermaid\n.*?```", "![architecture](arch.svg)", _PLAN, flags=re.S))
    sh(["pandoc", page_md, "-s", "--metadata", "title=Plan", "-o", wd / "plan.html"], timeout=60)
    html = (wd / "plan.html").read_text(encoding="utf-8")
    tw(wd / "server.cjs", _COMMENT_SERVER)
    p = subprocess.Popen([NODE, str(wd / "server.cjs"), str(wd)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    try:
        port = int(p.stdout.readline().split()[1])
        base = "http://127.0.0.1:%d" % port
        page = op.open(base + "/", timeout=5).read().decode()
        svg_ok = b"<svg" in op.open(base + "/arch.svg", timeout=5).read()
        for c in ({"section": "Key changes", "text": "Who gets the email?"}, {"section": "TL;DR", "text": "Clear."}):
            op.open(urllib.request.Request(base + "/api/comments", data=json.dumps(c).encode(), method="POST"), timeout=5).read()
        comments = json.loads(op.open(base + "/api/comments", timeout=5).read())
    finally:
        p.terminate()
        p.wait(timeout=5)
    bad = "# Plan\n\n## Summary\nWe refactor the ORM layer and make the RPC calls idempotent so the sharding change that the platform team proposed last quarter can finally land without downtime for anyone.\n"
    return [
        check("plan passes lint (sections, short sentences, no jargon, diagram)", findings == [], findings, []),
        check("architecture diagram rendered with its labels", all(l in (wd / "arch.svg").read_text() for l in ("queues job", "sends link")), True, True),
        check("rendered page has every section and the diagram", all(s in html for s in ("TL;DR", "Key changes", "arch.svg")), True, True),
        check("served page and SVG reachable on localhost", "Key changes" in page and svg_ok, [len(page), svg_ok], True),
        check("comments collected and read back", [c["section"] for c in comments] == ["Key changes", "TL;DR"], comments, 2),
        check("negative control: an engineer-speak draft fails lint", len(plan_lint(bad)) >= 4, plan_lint(bad), ">= 4 findings"),
    ], [md, wd / "plan.html", wd / "comments.json"]


@card("ADOCS-31")
def version_correct_docs(task, wd):
    """Answer an API question from the docs of the INSTALLED version: read the version from the lockfile, confirm the
    installed package matches, read the signature/docstring of that version, cite the source, record the gotcha."""
    import importlib.metadata as md
    import inspect
    import pandas as pd
    inst = md.version("pandas")
    lock = tw(wd / "requirements.lock", "numpy==%s\npandas==%s\n" % (md.version("numpy"), inst))
    locked = dict(l.split("==") for l in lock.read_text().split())
    question = "Which keyword sets the line terminator in DataFrame.to_csv?"
    params = list(inspect.signature(pd.DataFrame.to_csv).parameters)
    answer = "lineterminator" if "lineterminator" in params else ("line_terminator" if "line_terminator" in params else None)
    src = inspect.getsourcefile(inspect.unwrap(pd.DataFrame.to_csv)) or ""
    url = "https://pandas.pydata.org/pandas-docs/version/%s/reference/api/pandas.DataFrame.to_csv.html" % inst
    df = pd.DataFrame({"a": [1, 2]})
    out = df.to_csv(index=False, **{answer: "\r\n"})
    try:
        df.to_csv(index=False, line_terminator="\r\n")
        memory_ok = True
    except TypeError:
        memory_ok = False
    rules = tw(wd / "rules" / "pandas.md", "# pandas %s gotchas\n- to_csv uses `%s` (source: %s; %s)\n- `line_terminator` was removed in 2.0\n"
               % (inst, answer, src.split("site-packages/")[-1] if src else "?", url))
    mismatch = {"pandas": "1.5.3"}
    stale = mismatch["pandas"] != inst
    ans = jw(wd / "answer.json", {"question": question, "locked": locked["pandas"], "installed": inst, "answer": answer, "cite": url,
                                  "source_file": src})
    return [
        check("lockfile version equals the installed package", locked["pandas"] == inst, [locked["pandas"], inst], "equal"),
        check("answer read from the installed signature", answer == "lineterminator" and int(inst.split(".")[0]) >= 2, [answer, inst], "lineterminator (pandas>=2)"),
        check("the answer works on this version (CRLF written)", out == "a\r\n1\r\n2\r\n", repr(out), "a\\r\\n1\\r\\n2\\r\\n"),
        check("citation names the version-pinned docs URL and source file", inst in url and src.endswith("generic.py") or src.endswith("frame.py"), [url, src[-40:]], "versioned"),
        check("gotcha recorded in a rule file", "line_terminator" in rules.read_text(), True, True),
        check("a lockfile pinned to another version is flagged stale", stale, ["1.5.3", inst], "mismatch"),
        check("negative control: the from-memory keyword fails on the installed version", not memory_ok, memory_ok, False),
    ], [ans, rules]


_SESSION = [
    {"kind": "prompt", "text": "اعمل لي ريلز من الصوت ده بترجمة عربية"},
    {"kind": "output", "text": "Transcribed 41 words, built a 9:16 timeline."},
    {"kind": "dead_end", "text": "Burned captions with the default font", "why": "Arabic letters came out disconnected"},
    {"kind": "prompt", "text": "the letters look broken, fix the font"},
    {"kind": "output", "text": "Switched to a shaping-aware renderer with Cairo font; letters joined."},
    {"kind": "dead_end", "text": "Cut on every detected onset", "why": "too many cuts; the edit felt nervous"},
    {"kind": "prompt", "text": "fewer cuts, only on the strong beats"},
    {"kind": "output", "text": "Cut on downbeats only: 12 cuts in 30 s, -14 LUFS, delivered."},
]


def _timeline_svg(steps):
    w = 120 * len(steps) + 20
    parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="80" role="img" aria-label="session timeline">' % w]
    for i, s in enumerate(steps):
        col = "#c0392b" if s["kind"] == "dead_end" else ("#2c7be5" if s["kind"] == "prompt" else "#2e9e5b")
        parts.append('<rect class="step %s" x="%d" y="20" width="100" height="40" rx="8" fill="%s"/>' % (s["kind"], 10 + 120 * i, col))
    parts.append("</svg>")
    return "".join(parts)


def session_article(steps):
    prompts = [s["text"] for s in steps if s["kind"] == "prompt"]
    dead = [s for s in steps if s["kind"] == "dead_end"]
    lines = ["# How we built an Arabic reel in three prompts", "", "## What we set out to do", prompts[0], "",
             "## The real prompts"] + ["> %s" % p for p in prompts] + ["", "## Wrong turns (and why)"]
    lines += ["- **%s**: %s." % (d["text"], d["why"]) for d in dead]
    lines += ["", "## What I learned", "Each wrong turn taught a rule: shape Arabic before burning it, and cut on strong beats only.",
              "", "## Timeline", _timeline_svg(steps), "", "## Result", [s["text"] for s in steps if s["kind"] == "output"][-1], ""]
    return "\n".join(lines)


@card("ADOCS-40")
def teaching_article(task, wd):
    """Turn a working session (real prompts, outputs and dead ends) into a walkthrough with the prompts verbatim, the
    wrong turns with their reasons, a reflective tone, a diagram, and rendered HTML (pandoc)."""
    log = wd / "session.jsonl"
    log.write_text("".join(json.dumps(s, ensure_ascii=False) + "\n" for s in _SESSION), encoding="utf-8")
    steps = [json.loads(l) for l in log.read_text(encoding="utf-8").splitlines()]
    art = tw(wd / "article.md", session_article(steps))
    sh(["pandoc", art, "-s", "--metadata", "title=Walkthrough", "-o", wd / "article.html"], timeout=60)
    html = (wd / "article.html").read_text(encoding="utf-8")
    text = art.read_text(encoding="utf-8")
    prompts = [s["text"] for s in steps if s["kind"] == "prompt"]
    dead = [s for s in steps if s["kind"] == "dead_end"]
    polished = "# Arabic reel\n\n" + steps[-1]["text"] + "\n"
    return [
        check("every real prompt quoted verbatim", all(("> " + p) in text for p in prompts), len(prompts), 3),
        check("every dead end with its reason", all(d["text"] in text and d["why"] in text for d in dead), len(dead), 2),
        check("diagram: one box per step, red boxes = dead ends", html.count('class="step') == len(steps) and html.count("step dead_end") == 2,
              [html.count('class="step'), html.count("step dead_end")], [8, 2]),
        check("reflective, educational section present", "## What I learned" in text, True, True),
        check("rendered HTML carries the headings", all(h in html for h in ("The real prompts", "Wrong turns")), True, True),
        check("negative control: a polished summary hides the wrong turns", not any(d["why"] in polished for d in dead), True, True),
    ], [art, wd / "article.html"]


_ELI5 = [
    ("A box with labelled drawers", "A hash map is a cabinet. Each drawer has a number.", "drawers"),
    ("The name picks the drawer", "A recipe turns the name into a drawer number. Same name, same drawer.", "arrow"),
    ("Two names, one drawer", "Sometimes two names land together. The drawer keeps a short list.", "list"),
]


def eli5_html(ideas):
    secs = []
    for i, (title, text, kind) in enumerate(ideas):
        if kind == "drawers":
            body = "".join('<rect x="%d" y="20" width="50" height="60" fill="#f4c542" stroke="#333"/><text x="%d" y="55">%d</text>' % (10 + 60 * k, 30 + 60 * k, k) for k in range(4))
        elif kind == "arrow":
            body = '<text x="10" y="55">"ali"</text><line x1="70" y1="50" x2="170" y2="50" stroke="#333" stroke-width="4"/><rect x="180" y="20" width="50" height="60" fill="#f4c542" stroke="#333"/>'
        else:
            body = '<rect x="10" y="20" width="50" height="60" fill="#f4c542" stroke="#333"/><circle cx="100" cy="35" r="12" fill="#2c7be5"/><circle cx="100" cy="70" r="12" fill="#e5532c"/>'
        secs.append('<section class="idea"><h2>%s</h2><svg viewBox="0 0 260 100" width="260" height="100">%s</svg><p>%s</p></section>' % (title, body, text))
    return ("<!doctype html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width'><title>ELI5</title>"
            "<style>body{font:18px sans-serif;margin:16px;background:#fff}section{margin:24px 0}</style></head><body>%s</body></html>" % "".join(secs))


@card("ADOCS-41")
def eli5_visual(task, wd):
    """Zero-knowledge explainer: one idea per diagram, minimal text, concrete analogy, one self-contained HTML; the
    page is opened in Chromium (Playwright) and measured: SVGs per section, words per section, painted pixels."""
    page = tw(wd / "eli5.html", eli5_html(_ELI5))
    wall = tw(wd / "draft_wall.html", "<!doctype html><html><body><section class='idea'><h2>Hash maps</h2><p>%s</p></section></body></html>"
              % ("A hash map stores key value pairs using a hash function that maps keys to bucket indices with collision handling " * 3))
    js = """const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const out={};
for (const f of %s){const p=await b.newPage({viewport:{width:390,height:900}});await p.goto('file://'+f);
out[f]=await p.$$eval('section.idea',ss=>ss.map(s=>({svgs:s.querySelectorAll('svg').length,shapes:s.querySelectorAll('svg *').length,
words:s.innerText.split(/\\s+/).filter(Boolean).length})));out[f+'#ext']=await p.$$eval('[src],link[href]',e=>e.length);
await p.screenshot({path:f+'.png',fullPage:true});}await b.close();console.log(JSON.stringify(out));})();""" % json.dumps([str(page), str(wall)])
    res = node_js(wd, "measure", js)
    good, bad = res[str(page)], res[str(wall)]
    np = _np()
    shot = load_png(str(page) + ".png")
    painted = float((np.abs(shot - 255).max(axis=-1) > 30).mean())
    return [
        check("three ideas, exactly one diagram each", [s["svgs"] for s in good] == [1, 1, 1], [s["svgs"] for s in good], [1, 1, 1]),
        check("every diagram draws shapes", all(s["shapes"] >= 3 for s in good), [s["shapes"] for s in good], ">= 3"),
        check("minimal text: <= 25 words per idea", all(s["words"] <= 25 for s in good), [s["words"] for s in good], "<= 25"),
        check("self-contained (no external src/href)", res[str(page) + "#ext"] == 0, res[str(page) + "#ext"], 0),
        check("rendered page paints diagrams (non-white pixels)", painted > 0.03, painted, "> 0.03"),
        check("negative control: a text-wall draft has no diagram and too many words", bad[0]["svgs"] == 0 and bad[0]["words"] > 25, bad, "0 svg, > 25 words"),
    ], [page, Path(str(page) + ".png")]


_DECK = """---
theme: none
title: Shipping reels faster
aspectRatio: 16/9
---

# Shipping reels faster

<!-- Welcome everyone; this is the presenter note. -->

---
layout: two-cols
---

# Before

Manual cuts

::right::

# After

Cuts on the beat

---

# Code, step by step

```ts {1|2-3|all}
const bpm = 128
const beat = 60 / bpm
cut(at(beat * 4))
```

<v-click>Every cut lands on a beat.</v-click>

<v-click>No more nudging by hand.</v-click>

---
layout: fact
---

# The maths

$t_n = n \\cdot \\frac{60}{BPM}$
"""


@card("ADOCS-48")
def slidev_deck(task, wd):
    """Slidev deck from one Markdown file, parsed by Slidev's own parser (@slidev/parser): first frontmatter configures
    the deck, --- separates slides, HTML comments are presenter notes, layouts (two-cols with ::right::, fact), code
    line-range steps {1|2-3|all}, v-click reveals; LaTeX rendered with KaTeX. (A full `slidev build` takes ~18 s here,
    so the export step itself is not run.)"""
    deck = tw(wd / "slides.md", _DECK)
    flat = tw(wd / "flat.md", _DECK.replace("\n---\n", "\n\n"))
    parser = NM / "@slidev/cli/node_modules/@slidev/parser/dist/core.mjs"
    katex = NM / "@slidev/cli/node_modules/katex"
    js = """import {parse} from %s; import fs from 'fs'; import {createRequire} from 'module'; const require=createRequire(import.meta.url);
const katex=require(%s); const out={};
for (const f of [%s,%s]){const r=await parse(fs.readFileSync(f,'utf8'),f); out[f]=r.slides.map(s=>({fm:s.frontmatter,note:s.note||null,content:s.content}));}
out.tex=katex.renderToString(String.raw`t_n = n \\cdot \\frac{60}{BPM}`); console.log(JSON.stringify(out));""" % (
        json.dumps(str(parser)), json.dumps(str(katex)), json.dumps(str(deck)), json.dumps(str(flat)))
    src = tw(wd / "parse.mjs", js)
    res = json.loads(sh([NODE, src], cwd=wd, env=node_env(), timeout=40).stdout.strip().splitlines()[-1])
    slides = res[str(deck)]
    code = re.search(r"```ts \{([^}]*)\}", slides[2]["content"]).group(1)
    steps = code.split("|")
    clicks = len(steps) - 1 + slides[2]["content"].count("<v-click>")
    html = tw(wd / "slide4_math.html", "<!doctype html><html><head><meta charset='utf-8'><link rel='stylesheet' href='%s/dist/katex.min.css'></head><body>%s</body></html>"
              % (katex.as_uri(), res["tex"]))
    out = jw(wd / "deck_parsed.json", {"slides": slides, "code_steps": steps, "clicks_slide3": clicks})
    return [
        check("deck config read from the first frontmatter", slides[0]["fm"].get("title") == "Shipping reels faster" and slides[0]["fm"].get("aspectRatio") == "16/9",
              slides[0]["fm"], "title + 16/9"),
        check("four slides separated by ---", len(slides) == 4, len(slides), 4),
        check("presenter note parsed from the HTML comment", (slides[0]["note"] or "").startswith("Welcome everyone"), slides[0]["note"], "Welcome..."),
        check("layouts: two-cols with a ::right:: slot, then fact", slides[1]["fm"].get("layout") == "two-cols" and "::right::" in slides[1]["content"]
              and slides[3]["fm"].get("layout") == "fact", [slides[1]["fm"], slides[3]["fm"]], "two-cols, fact"),
        check("code reveals in 3 steps {1|2-3|all} + 2 v-clicks = 4 clicks", steps == ["1", "2-3", "all"] and clicks == 4, [steps, clicks], 4),
        check("LaTeX rendered by KaTeX (MathML + frac)", "katex" in res["tex"] and "mfrac" in res["tex"], len(res["tex"]), "katex html"),
        check("negative control: without --- separators the parser sees one slide", len(res[str(flat)]) == 1, len(res[str(flat)]), 1),
    ], [out, html, deck]


# ================================================================================ AGENT: schedules, plugins, vector store, MCP

def _cron_field(spec, lo, hi):
    vals = set()
    for part in spec.split(","):
        step = 1
        if "/" in part:
            part, s = part.split("/")
            step = int(s)
        if part == "*":
            a, b = lo, hi
        elif "-" in part:
            a, b = map(int, part.split("-"))
        else:
            a = b = int(part)
        vals.update(range(a, b + 1, step))
    return vals


def cron_next(expr, start, n=3):
    """Next n run times of a 5-field cron (optionally prefixed CRON_TZ=Zone), as UTC datetimes."""
    import datetime as dt
    from zoneinfo import ZoneInfo
    tz = ZoneInfo("UTC")
    if expr.startswith("CRON_TZ="):
        z, expr = expr.split(None, 1)
        tz = ZoneInfo(z.split("=", 1)[1])
    mi, hr, dom, mon, dow = expr.split()
    M, Hh, D, Mo = _cron_field(mi, 0, 59), _cron_field(hr, 0, 23), _cron_field(dom, 1, 31), _cron_field(mon, 1, 12)
    W = {d % 7 for d in _cron_field(dow, 0, 7)}
    t = start.astimezone(tz).replace(second=0, microsecond=0) + dt.timedelta(minutes=1)
    out = []
    for _ in range(60 * 24 * 40):
        if t.minute in M and t.hour in Hh and t.day in D and t.month in Mo and ((t.weekday() + 1) % 7) in W:
            out.append(t.astimezone(ZoneInfo("UTC")))
            if len(out) == n:
                break
        t += dt.timedelta(minutes=1)
    return out


_CONTEXT_WORDS = ("as above", "this session", "the previous", "continue", "same as before", "that file")


def trigger_issues(spec, now):
    iss = []
    expr = spec["cron"]
    runs = cron_next(expr, now, 30)
    gaps = [(b - a).total_seconds() / 60 for a, b in zip(runs, runs[1:])]
    if gaps and min(gaps) < 60:
        iss.append("runs more often than hourly (%d min)" % min(gaps))
    minute = expr.split()[-5]
    if minute in ("0", "30", "*") or minute.startswith("*/"):
        iss.append("minute not jittered away from :00/:30")
    if spec["mode"] == "fresh":
        p = spec["prompt"].lower()
        if any(w in p for w in _CONTEXT_WORDS) or len(p.split()) < 12:
            iss.append("fresh-session prompt is not standalone")
    return iss


@card("AGENT-17")
def scheduled_routines(task, wd):
    """Build trigger specs the way the card says (5-field cron, at least hourly, minute jittered off :00/:30,
    CRON_TZ= for local time, a standalone prompt for a fresh session, three modes + a one-shot send_later), validate
    them and compute the next runs. Nothing is created: creating a trigger is the user's explicit request."""
    import datetime as dt
    from zoneinfo import ZoneInfo
    now = dt.datetime(2026, 11, 4, 10, 0, tzinfo=ZoneInfo("Africa/Cairo"))
    specs = {
        "weekday_digest": {"mode": "fresh", "cron": "CRON_TZ=Africa/Cairo 17 9 * * 1-5",
                           "prompt": "Open the kosif-tool repository, run python3 tools/validate.py and post a one-paragraph summary of failures to this project."},
        "resume_check": {"mode": "resume", "cron": "43 */2 * * *", "prompt": "check the render queue"},
        "wake_other": {"mode": "wake", "cron": "CRON_TZ=Asia/Riyadh 7 20 * * 0", "prompt": "weekly review"},
    }
    issues = {k: trigger_issues(v, now) for k, v in specs.items()}
    nxt = [t.isoformat() for t in cron_next(specs["weekday_digest"]["cron"], now, 3)]
    want = ["2026-11-05T07:17:00+00:00", "2026-11-06T07:17:00+00:00", "2026-11-09T07:17:00+00:00"]
    later = {"tool": "send_later", "deliver_at": (now + dt.timedelta(hours=2)).astimezone(ZoneInfo("UTC")).isoformat(), "message": "render finished? check out/job"}
    bad = {"every5": {"mode": "resume", "cron": "*/5 * * * *", "prompt": "x"},
           "on_the_hour": {"mode": "resume", "cron": "0 9 * * *", "prompt": "x"},
           "context_prompt": {"mode": "fresh", "cron": "11 8 * * *", "prompt": "continue as above"}}
    bad_issues = {k: trigger_issues(v, now) for k, v in bad.items()}
    out = jw(wd / "triggers.json", {"triggers": specs, "issues": issues, "next_runs_utc": nxt, "send_later": later, "rejected": bad_issues})
    return [
        check("all three trigger specs pass the rules", all(v == [] for v in issues.values()), issues, "no issues"),
        check("CRON_TZ=Africa/Cairo 09:17 Mon-Fri -> next runs in UTC (EET, UTC+2)", nxt == want, nxt, want),
        check("one-shot send_later due in 2 h (UTC)", later["deliver_at"] == "2026-11-04T10:00:00+00:00", later["deliver_at"], "2026-11-04T10:00:00+00:00"),
        check("three modes covered", sorted(v["mode"] for v in specs.values()) == ["fresh", "resume", "wake"], True, True),
        check("negative control: */5, :00 and a context-bound fresh prompt are rejected", all(bad_issues[k] for k in bad), bad_issues, "each rejected"),
    ], [out]


@card("AGENT-24")
def plugins_marketplace(task, wd):
    """A plugin (skills + hooks) in a local marketplace, validated and installed with the real Claude Code CLI in two
    commands (`plugin marketplace add`, `plugin install name@marketplace`) inside a private HOME, then checked with
    `plugin list`; an invalid manifest is refused."""
    claude = shutil.which("claude")
    if not claude:
        raise RuntimeError("claude CLI not on PATH")
    mk = wd / "mk"
    jw(mk / ".claude-plugin/marketplace.json", {"name": "local-mk", "owner": {"name": "KOSIF"}, "description": "local test marketplace",
                                                "plugins": [{"name": "reel-helper", "source": "./plugins/reel-helper", "description": "reel helper"}]})
    pl = mk / "plugins/reel-helper"
    jw(pl / ".claude-plugin/plugin.json", {"name": "reel-helper", "version": "0.1.0", "description": "Checks reels", "author": {"name": "KOSIF"}})
    tw(pl / "skills/reel-check/SKILL.md", "---\nname: reel-check\ndescription: Check a reel is 1080x1920 at 30 fps\n---\nRun ffprobe and compare.\n")
    jw(pl / "hooks/hooks.json", {"hooks": {"PostToolUse": [{"matcher": "Bash", "hooks": [{"type": "command", "command": "true"}]}]}})
    bad = wd / "bad-plugin"
    jw(bad / ".claude-plugin/plugin.json", {"name": "Bad Name!", "version": "x"})
    home = wd / "home"
    home.mkdir()
    env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HOME": str(home), "NO_COLOR": "1"}
    v = sh([claude, "plugin", "validate", mk], env=env, ok=None, timeout=60)
    vb = sh([claude, "plugin", "validate", bad], env=env, ok=None, timeout=60)
    a = sh([claude, "plugin", "marketplace", "add", mk], env=env, ok=None, timeout=60)
    i = sh([claude, "plugin", "install", "reel-helper@local-mk"], env=env, ok=None, timeout=60)
    ls = sh([claude, "plugin", "list"], env=env, ok=None, timeout=60)
    settings = json.loads((home / ".claude/settings.json").read_text()) if (home / ".claude/settings.json").exists() else {}
    log = tw(wd / "plugin_log.txt", "\n".join("$ %s\n%s%s" % (n, d.stdout, d.stderr) for n, d in
                                              (("validate", v), ("validate bad", vb), ("add", a), ("install", i), ("list", ls))))
    enabled = settings.get("enabledPlugins", {})
    return [
        check("marketplace validates", v.returncode == 0, v.returncode, 0),
        check("marketplace added", a.returncode == 0 and "local-mk" in a.stdout, a.stdout.strip()[-80:], "added"),
        check("plugin installed from name@marketplace", i.returncode == 0 and "reel-helper@local-mk" in i.stdout, i.stdout.strip()[-80:], "installed"),
        check("plugin list shows it once, enabled", ls.stdout.count("reel-helper@local-mk") == 1 and "enabled" in ls.stdout, ls.stdout.count("reel-helper@local-mk"), 1),
        check("enabled in the private HOME settings only (one install method)", list(enabled) == ["reel-helper@local-mk"], enabled, {"reel-helper@local-mk": True}),
        check("negative control: an invalid manifest fails validation", vb.returncode != 0, vb.returncode, "!= 0"),
    ], [log]


def _embed(text, vocab):
    w = re.findall(r"\w+", text.lower())
    v = [float(w.count(t)) for t in vocab]
    n = math.sqrt(sum(x * x for x in v)) or 1.0
    return [x / n for x in v]


@card("AGENT-37")
def chroma_rag(task, wd):
    """Index documents into a persistent Chroma collection (embeddings computed here, no model download), answer a
    semantic query by nearest neighbours with metadata filters, and reopen the store from disk."""
    import chromadb
    from chromadb.config import Settings
    docs = {"r1": "beat synced reel montage with cuts on the beat", "r2": "vertical reel montage cut to music beat",
            "d1": "duckdb query parquet files with sql", "d2": "pandas dataframe schema contract",
            "a1": "arabic typography kashida and shaping", "a2": "arabic captions font shaping for subtitles"}
    vocab = sorted({w for t in docs.values() for w in re.findall(r"\w+", t.lower())})
    cl = chromadb.PersistentClient(path=str(wd / "chroma"), settings=Settings(anonymized_telemetry=False))
    col = cl.get_or_create_collection("kb_docs", embedding_function=None, metadata={"hnsw:space": "cosine"})
    col.add(ids=list(docs), documents=list(docs.values()), embeddings=[_embed(t, vocab) for t in docs.values()],
            metadatas=[{"topic": k[0]} for k in docs])
    q = col.query(query_embeddings=[_embed("montage reel on the beat", vocab)], n_results=2)
    qa = col.query(query_embeddings=[_embed("arabic font shaping", vocab)], n_results=2, where={"topic": "a"})
    del cl
    cl2 = chromadb.PersistentClient(path=str(wd / "chroma"), settings=Settings(anonymized_telemetry=False))
    n = cl2.get_collection("kb_docs", embedding_function=None).count()
    qn = cl2.get_collection("kb_docs", embedding_function=None).query(query_embeddings=[_embed("sql parquet", vocab)], n_results=1)
    out = jw(wd / "rag.json", {"q_reel": q["ids"][0], "q_arabic": qa["ids"][0], "q_sql": qn["ids"][0], "count_after_reopen": n})
    files = [p for p in (wd / "chroma").rglob("*") if p.is_file()]
    return [
        check("reel query returns the two reel documents", sorted(q["ids"][0]) == ["r1", "r2"], q["ids"][0], ["r1", "r2"]),
        check("metadata-filtered query returns the Arabic documents", sorted(qa["ids"][0]) == ["a1", "a2"], qa["ids"][0], ["a1", "a2"]),
        check("store persisted: 6 vectors after reopening", n == 6, n, 6),
        check("negative control: the same search with an SQL query does not return a reel document", qn["ids"][0] == ["d1"], qn["ids"][0], ["d1"]),
    ], [out, max(files, key=lambda p: p.stat().st_size)]


@card("AGENT-38")
def mcp_reference_servers(task, wd):
    """Wire the reference MCP filesystem server (@modelcontextprotocol/server-filesystem, stdio) into an agent as tools
    with the python MCP client: list tools, list a directory, read a file, and confirm access outside the allowed root
    is refused."""
    import asyncio
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
    server = NM / "@modelcontextprotocol/server-filesystem/dist/index.js"
    root = (wd / "allowed").resolve()
    tw(root / "notes.txt", "beat grid 128 bpm\n")
    tw(root / "plan.md", "# plan\n")
    tw(wd / "outside.txt", "secret\n")

    async def go():
        params = StdioServerParameters(command=NODE, args=[str(server), str(root)], env={"PATH": os.environ.get("PATH", "")})
        with open(wd / "server_stderr.txt", "w") as err:
            async with stdio_client(params, errlog=err) as (r, w):
                async with ClientSession(r, w) as s:
                    await s.initialize()
                    tools = [t.name for t in (await s.list_tools()).tools]
                    ls = await s.call_tool("list_directory", {"path": str(root)})
                    rd = await s.call_tool("read_text_file", {"path": str(root / "notes.txt")})
                    bad = await s.call_tool("read_text_file", {"path": str((wd / "outside.txt").resolve())})
                    txt = lambda res: "".join(getattr(c, "text", "") for c in res.content)
                    return {"tools": tools, "ls": txt(ls), "read": txt(rd), "bad_error": bool(getattr(bad, "is_error", None) or getattr(bad, "isError", False)), "bad": txt(bad)}

    res = asyncio.run(asyncio.wait_for(go(), 30))
    out = jw(wd / "mcp_session.json", res)
    return [
        check("server exposes filesystem tools", {"list_directory", "read_text_file"} <= set(res["tools"]), len(res["tools"]), ">= 2"),
        check("list_directory sees both files", "notes.txt" in res["ls"] and "plan.md" in res["ls"], res["ls"], "notes.txt, plan.md"),
        check("read_text_file returns the file content", res["read"].strip() == "beat grid 128 bpm", res["read"], "beat grid 128 bpm"),
        check("negative control: a file outside the allowed root is refused", res["bad_error"] and "secret" not in res["bad"], res["bad"][:80], "error"),
    ], [out]


# ================================================================================ AMIND: tmux peers, session messaging

@card("AMIND-19")
def tmux_peer_ledger(task, wd):
    """Orchestrator and executor in named tmux panes (private socket in the work folder), a file-backed task ledger with
    stages, dependencies and reviewer routes, a task dispatched to the named pane and its result read back, and old
    message files cleaned only after a dry run."""
    if not shutil.which("tmux"):
        raise RuntimeError("tmux not installed")
    T = ["tmux", "-S", "t.sock"]
    (wd / "msgs").mkdir()
    ledger = {"T1": {"stage": "build", "deps": [], "reviewer": "orchestrator", "assignee": None, "status": "todo"},
              "T2": {"stage": "verify", "deps": ["T1"], "reviewer": "orchestrator", "assignee": None, "status": "todo"}}
    ready = lambda L: sorted(k for k, v in L.items() if v["status"] == "todo" and all(L[d]["status"] == "done" for d in v["deps"]))
    ready0 = ready(ledger)
    try:
        sh(T + ["-f", "/dev/null", "new-session", "-d", "-s", "agents", "-n", "orchestrator", "-c", wd, "sh"], cwd=wd)
        sh(T + ["new-window", "-t", "agents", "-n", "executor", "-c", wd, "sh"], cwd=wd)
        sh(T + ["select-pane", "-t", "agents:orchestrator", "-T", "orchestrator"], cwd=wd)
        sh(T + ["select-pane", "-t", "agents:executor", "-T", "executor"], cwd=wd)
        panes = sh(T + ["list-panes", "-a", "-F", "#{window_name}=#{pane_title}"], cwd=wd).stdout.split()
        ledger["T1"].update(assignee="executor", eta="1m", context="build the cut list")
        sh(T + ["send-keys", "-t", "agents:executor", "echo DONE:T1 > msgs/T1.result", "Enter"], cwd=wd)
        t0 = time.time()
        while not (wd / "msgs/T1.result").exists() and time.time() - t0 < 6:
            time.sleep(0.05)
        result = (wd / "msgs/T1.result").read_text().strip() if (wd / "msgs/T1.result").exists() else ""
        if result == "DONE:T1":
            ledger["T1"]["status"] = "done"
        ready1 = ready(ledger)
        cap = sh(T + ["capture-pane", "-p", "-t", "agents:executor"], cwd=wd).stdout
    finally:
        subprocess.run(T + ["kill-server"], cwd=str(wd), capture_output=True, timeout=10)
    jw(wd / "ledger.json", ledger)
    for i in range(3):
        f = tw(wd / "msgs" / ("old_%d.msg" % i), "stale")
        os.utime(f, (time.time() - 3 * 86400, time.time() - 3 * 86400))
    cutoff = time.time() - 86400
    old = sorted(p.name for p in (wd / "msgs").glob("*.msg") if p.stat().st_mtime < cutoff)
    dry_kept = all((wd / "msgs" / n).exists() for n in old)
    for n in old:
        (wd / "msgs" / n).unlink()
    left = sorted(p.name for p in (wd / "msgs").iterdir())
    return [
        check("panes named orchestrator and executor", sorted(panes) == ["executor=executor", "orchestrator=orchestrator"], panes, "2 named panes"),
        check("task dispatched to the named pane ran there", result == "DONE:T1" and "echo DONE:T1" in cap, result, "DONE:T1"),
        check("ledger: T2 becomes ready only after T1 is done", ready1 == ["T2"], ready1, ["T2"]),
        check("dry run listed 3 old message files and deleted nothing", old == ["old_0.msg", "old_1.msg", "old_2.msg"] and dry_kept, old, 3),
        check("cleanup kept the fresh result file", left == ["T1.result"], left, ["T1.result"]),
        check("negative control: before T1 finished, T2 was not ready", ready0 == ["T1"], ready0, ["T1"]),
    ], [wd / "ledger.json"]


def _ver(s):
    return tuple(int(x) for x in re.findall(r"\d+", s)[:3])


def resolve_peer(listing, want, ref=None):
    hits = [a for a in listing if a["name"] == want]
    if not hits:
        return {"error": "no such peer"}
    if ref:
        if not any(a["ref"] == ref for a in hits):
            return {"error": "stale ref"}
        return {"to": "%s [%s]" % (want, ref)}
    if len(hits) > 1:
        return {"error": "ambiguous: add [ref]", "refs": [a["ref"] for a in hits]}
    return {"to": want}


_PEER = r"""
import json, sys
box = sys.argv[1]
msgs = [json.loads(l) for l in open(box + '/to_reviewer.jsonl', encoding='utf-8')]
out = open(box + '/to_lead.jsonl', 'a', encoding='utf-8')
for m in msgs:
    if m['shape'] == 'question':
        r = {'to': m['sender'], 'sender': 'reviewer', 'reply_to': m['id'], 'text': 'yes, 30 fps'}
    elif m['shape'] == 'work_order':
        r = {'to': m['sender'], 'sender': 'reviewer', 'reply_to': m['id'], 'text': 'done: 3 issues', 'idle': bool(m.get('notify_when_idle'))}
    else:
        r = {'to': m['sender'], 'sender': 'reviewer', 'reply_to': m['id'], 'text': 'turn %d ack' % m['turn']}
    out.write(json.dumps(r) + '\n')
"""


@card("AMIND-20")
def session_peer_messaging(task, wd):
    """Peer messaging protocol: gate on the Claude Code version (>= 2.1.224 for native messaging), address peers by the
    bare ListAgents name and add [ref] only to disambiguate (never a stale ref), and use the three call shapes
    (question, work order with notify-when-idle, conference turns answered to the sender). A separate peer process
    answers over a file mailbox."""
    claude = shutil.which("claude")
    here = sh([claude, "--version"], env={"PATH": os.environ.get("PATH", ""), "HOME": str(wd)}, ok=None, timeout=20).stdout if claude else ""
    here_v = _ver(here) if here else (0, 0, 0)
    gate = lambda v: v >= (2, 1, 224)
    listing = [{"name": "reviewer", "ref": "a1"}, {"name": "render", "ref": "b7"}, {"name": "render", "ref": "c2"}]
    r1, r2, r3, r4 = (resolve_peer(listing, "reviewer"), resolve_peer(listing, "render"), resolve_peer(listing, "render", "c2"),
                      resolve_peer(listing, "reviewer", "zz"))
    box = wd / "mailbox"
    box.mkdir()
    sent = [{"id": "m1", "sender": "lead", "to": r1["to"], "shape": "question", "text": "is the export 30 fps?"},
            {"id": "m2", "sender": "lead", "to": r1["to"], "shape": "work_order", "text": "review cut list", "notify_when_idle": True},
            {"id": "m3", "sender": "lead", "to": r1["to"], "shape": "conference", "turn": 1, "text": "opening"},
            {"id": "m4", "sender": "lead", "to": r1["to"], "shape": "conference", "turn": 2, "text": "follow-up"}]
    tw(box / "to_reviewer.jsonl", "".join(json.dumps(m) + "\n" for m in sent))
    peer = tw(wd / "peer.py", _PEER)
    sh([sys.executable, "-I", peer, box], timeout=20)
    replies = [json.loads(l) for l in (box / "to_lead.jsonl").read_text().splitlines()]
    out = jw(wd / "messaging.json", {"claude_version": here.strip(), "native_messaging": gate(here_v), "resolutions": [r1, r2, r3, r4],
                                     "sent": sent, "replies": replies})
    return [
        check("version gate: 2.1.230 passes, 2.1.223 does not", gate((2, 1, 230)) and not gate((2, 1, 223)), True, True),
        check("installed CLI measured against the gate", bool(here_v) and gate(here_v) == (here_v >= (2, 1, 224)), [here.strip(), gate(here_v)], "measured"),
        check("unique peer addressed by bare name", r1 == {"to": "reviewer"}, r1, {"to": "reviewer"}),
        check("duplicate name asks for a [ref]; a valid ref resolves", "ambiguous" in r2.get("error", "") and r3 == {"to": "render [c2]"}, [r2, r3], "ambiguous, render [c2]"),
        check("every reply goes to the sender and answers its message", [r["reply_to"] for r in replies] == ["m1", "m2", "m3", "m4"] and all(r["to"] == "lead" for r in replies),
              [r["reply_to"] for r in replies], ["m1", "m2", "m3", "m4"]),
        check("work order carried notify-when-idle", replies[1].get("idle") is True, replies[1], "idle true"),
        check("negative control: a stale ref is refused", r4 == {"error": "stale ref"}, r4, "stale ref"),
    ], [out]


# ================================================================================ ASTRAT / AWEB: flashcards, reading list

def atomic_issues(q, a):
    iss = []
    if " and " in a or ";" in a:
        iss.append("two facts in one answer")
    if len(a.split()) > 8:
        iss.append("answer too long")
    if q.count("?") != 1:
        iss.append("not one question")
    return iss


def split_compound(q, a):
    lq, rq = q.rstrip("?").split(" and ", 1)
    lw, rw = lq.split(), rq.split()
    head = next((i for i, w in enumerate(lw) if w in rw), len(lw) - 1)
    la, ra = a.split(" and ", 1)
    return [(lq + "?", la), (" ".join(lw[:head] + rw) + "?", ra)]


@card("ASTRAT-54")
def anki_flashcards(task, wd):
    """One atomic fact per card: compound cards are split, the deck is written as a real Anki package (genanki) and read
    back from its SQLite collection, and the AnkiConnect v6 actions (requestPermission, createDeck, addNotes) are built
    for when Anki is running (the localhost:8765 probe is recorded; Anki itself is not running here)."""
    import genanki
    raw = [("Integrated loudness target for reels?", "-14 LUFS"), ("Reel frame size and frame rate?", "1080x1920 and 30 fps"),
           ("True-peak ceiling for delivery?", "-1 dBTP")]
    cards = []
    for q, a in raw:
        cards += split_compound(q, a) if atomic_issues(q, a) else [(q, a)]
    model = genanki.Model(1607392319, "KOSIF Basic", fields=[{"name": "Front"}, {"name": "Back"}],
                          templates=[{"name": "Card 1", "qfmt": "{{Front}}", "afmt": "{{FrontSide}}<hr id=answer>{{Back}}"}])
    deck = genanki.Deck(2059400110, "KOSIF::Delivery")
    for q, a in cards:
        deck.add_note(genanki.Note(model=model, fields=[q, a], guid=genanki.guid_for(q)))
    pkg = wd / "delivery.apkg"
    genanki.Package(deck).write_to_file(str(pkg))
    with zipfile.ZipFile(pkg) as z:
        names = z.namelist()
        z.extract("collection.anki2", wd / "unz")
    db = sqlite3.connect(str(wd / "unz/collection.anki2"))
    notes = [r[0].split("\x1f") for r in db.execute("SELECT flds FROM notes ORDER BY flds")]
    decks = json.loads(db.execute("SELECT decks FROM col").fetchone()[0])
    db.close()
    actions = [{"action": "requestPermission", "version": 6}, {"action": "createDeck", "version": 6, "params": {"deck": "KOSIF::Delivery"}},
               {"action": "addNotes", "version": 6, "params": {"notes": [{"deckName": "KOSIF::Delivery", "modelName": "Basic",
                                                                           "fields": {"Front": q, "Back": a}, "tags": ["kosif"]} for q, a in cards]}}]
    import socket
    s = socket.socket()
    s.settimeout(0.3)
    live = s.connect_ex(("127.0.0.1", 8765)) == 0
    s.close()
    out = jw(wd / "ankiconnect_actions.json", {"anki_running": live, "actions": actions})
    return [
        check("compound card split into two atomic cards", ("Reel frame size?", "1080x1920") in cards and ("Reel frame rate?", "30 fps") in cards, cards, "size / rate"),
        check("every card holds one atomic fact", all(not atomic_issues(q, a) for q, a in cards), [atomic_issues(q, a) for q, a in cards], "none"),
        check("package is a real Anki collection with 4 notes", "collection.anki2" in names and len(notes) == 4, [names, len(notes)], 4),
        check("deck stored under its name", any(d.get("name") == "KOSIF::Delivery" for d in decks.values()), [d.get("name") for d in decks.values()], "KOSIF::Delivery"),
        check("AnkiConnect actions are version 6 and add every card", all(a["version"] == 6 for a in actions) and len(actions[2]["params"]["notes"]) == 4, True, True),
        check("negative control: the raw compound card fails the atomic rule", bool(atomic_issues(*raw[1])), atomic_issues(*raw[1]), "issues"),
    ], [pkg, out]


_SYLLABUS = """# Video Editing 201 (undergraduate)

## Week 1: Rhythm and beat-synced cutting

## Week 2: Arabic typography for captions

## Week 3: Colour grading for social video
"""

_CORPUS = [
    {"id": "p1", "title": "Beat tracking for automatic video cutting", "year": 2023, "venue": "ACM MM", "peer_reviewed": True, "kw": ["beat", "cutting", "rhythm"]},
    {"id": "p2", "title": "Rhythm-aware montage generation", "year": 2022, "venue": "CVPR", "peer_reviewed": True, "kw": ["rhythm", "montage"]},
    {"id": "p3", "title": "Beat-synced cutting heuristics", "year": 2015, "venue": "SIGGRAPH", "peer_reviewed": True, "kw": ["beat", "cutting"]},
    {"id": "p4", "title": "Arabic script shaping for subtitles", "year": 2024, "venue": "ICDAR", "peer_reviewed": True, "kw": ["arabic", "typography", "captions"]},
    {"id": "p5", "title": "Readable captions on mobile video", "year": 2021, "venue": "CHI", "peer_reviewed": True, "kw": ["captions", "readability"]},
    {"id": "p6", "title": "Arabic typography with large models", "year": 2025, "venue": "arXiv", "peer_reviewed": False, "kw": ["arabic", "typography"]},
    {"id": "p7", "title": "Perceptual colour grading for short video", "year": 2024, "venue": "TOG", "peer_reviewed": True, "kw": ["colour", "grading", "video"]},
    {"id": "p8", "title": "Social video colour trends", "year": 2022, "venue": "ICWSM", "peer_reviewed": True, "kw": ["social", "video", "colour"]},
]
_STOP = {"and", "for", "the", "of", "week", "with"}


def reading_search(section, corpus, recent=2021, peer=True):
    terms = {w for w in re.findall(r"[a-z]+", section.lower().replace("beat-synced", "beat synced")) if w not in _STOP and len(w) > 2}
    hits = []
    for p in corpus:
        text = set(re.findall(r"[a-z]+", (p["title"] + " " + " ".join(p["kw"])).lower()))
        score = len(terms & text)
        if score and (not recent or p["year"] >= recent) and (not peer or p["peer_reviewed"]):
            hits.append((-score, -p["year"], p["id"]))
    return [h[2] for h in sorted(hits)[:2]]


@card("AWEB-09")
def syllabus_reading_list(task, wd):
    """Split the syllabus into sections, query an academic index per section for recent peer-reviewed papers, and
    assemble the reading list as .docx with node `docx`; read back with python-docx. (The index is a local fixture:
    the Consensus MCP is a live service.)"""
    syl = tw(wd / "syllabus.md", _SYLLABUS)
    sections = re.findall(r"^## (.+)$", syl.read_text(), re.M)
    by_id = {p["id"]: p for p in _CORPUS}
    picks = {s: reading_search(s, _CORPUS) for s in sections}
    data = jw(wd / "reading_list.json", {"course": "Video Editing 201", "level": "undergraduate",
                                         "sections": [{"title": s, "papers": [by_id[i] for i in picks[s]]} for s in sections]})
    js = """const fs=require('fs');const {Document,Packer,Paragraph,HeadingLevel,TextRun}=require('docx');
const d=JSON.parse(fs.readFileSync(%s,'utf8'));const kids=[new Paragraph({text:'Supplementary reading: '+d.course,heading:HeadingLevel.TITLE})];
for(const s of d.sections){kids.push(new Paragraph({text:s.title,heading:HeadingLevel.HEADING_1}));
 for(const p of s.papers){kids.push(new Paragraph({children:[new TextRun({text:p.title,bold:true}),new TextRun(' ('+p.year+'), '+p.venue+'.')]}));}}
Packer.toBuffer(new Document({sections:[{children:kids}]})).then(b=>{fs.writeFileSync(%s,b);console.log(JSON.stringify({bytes:b.length}));});""" % (
        json.dumps(str(data)), json.dumps(str(wd / "reading_list.docx")))
    node_js(wd, "build_docx", js)
    import docx
    doc = docx.Document(str(wd / "reading_list.docx"))
    sty = lambda p: (p._p.pPr.pStyle.val if p._p.pPr is not None and p._p.pPr.pStyle is not None else "")
    heads = [p.text for p in doc.paragraphs if sty(p).startswith("Heading")]
    entries = [p.text for p in doc.paragraphs if not sty(p) and p.text]
    years = [int(m) for e in entries for m in re.findall(r"\((\d{4})\)", e)]
    naive = reading_search(sections[0], _CORPUS, recent=None, peer=False) + reading_search(sections[1], _CORPUS, recent=None, peer=False)
    want = {sections[0]: ["p1", "p2"], sections[1]: ["p4", "p5"], sections[2]: ["p7", "p8"]}
    return [
        check("three syllabus sections found", len(sections) == 3, sections, 3),
        check("per-section picks are the known recent peer-reviewed papers", picks == want, picks, want),
        check("docx has one heading per section", heads == sections, heads, sections),
        check("docx lists 6 papers, all from 2021 or later", len(entries) == 6 and min(years) >= 2021, [len(entries), years], "6, >= 2021"),
        check("negative control: an unfiltered search pulls a 2015 paper or a preprint", any(i in naive for i in ("p3", "p6")), naive, "p3 or p6"),
    ], [wd / "reading_list.docx", data]


# ================================================================================ CHECK: isolated reviewers, trigger evals

_REVIEWER = r'''
import json, re, sys
variant, spec_f, draft_f, out_f = sys.argv[1:5]
spec = json.load(open(spec_f, encoding="utf-8")); text = open(draft_f, encoding="utf-8").read()
checks = []
def add(c, ok, d): checks.append({"criterion": c, "result": "PASS" if ok else "FAIL", "detail": d})
if variant == "A":
    urls = re.findall(r"https?://[^\s)]+", text)
    heads = re.findall(r"^## (.+)$", text, re.M)
    steps = re.findall(r"^\d+\.", text, re.M)
    said = re.search(r"has (\d+) steps", text)
    lufs = re.findall(r"(-?\d+) LUFS", text)
else:
    toks = text.replace("(", " ").replace(")", " ").split()
    urls = [t.rstrip(".,") for t in toks if t.startswith("http")]
    heads = [l[3:].strip() for l in text.splitlines() if l.startswith("## ")]
    steps = [l for l in text.splitlines() if l[:1].isdigit() and l.split(" ")[0].endswith(".")]
    said = next((re.match(r"(\d+)", t) for i, t in enumerate(toks) if i and toks[i - 1] == "has" and t[:1].isdigit()), None)
    lufs = [toks[i - 1] for i, t in enumerate(toks) if t.startswith("LUFS")]
bad_urls = [u for u in urls if u not in spec["allowed_urls"]]
add("no invented entities/URLs", not bad_urls, bad_urls)
missing = [m for m in spec["must_cover"] if m not in heads]
add("completeness vs spec", not missing, missing)
add("factual accuracy", all(v == spec["facts"]["lufs"] for v in lufs) and lufs, lufs)
add("internal consistency", bool(said) and int(said.group(1)) == len(steps), [said.group(1) if said else None, len(steps)])
crit = [c["criterion"] for c in checks if c["result"] == "FAIL"]
json.dump({"verdict": "FAIL" if crit else "PASS", "checks": checks, "critical_issues": crit,
           "suggestions": ["fix: " + c for c in crit]}, open(out_f, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
'''

_DRAFT = """# Export guide
This guide has 3 steps.
## Install
1. Install ffmpeg (see https://ffmpeg.org/ffmpeg.html).
## Verify
2. Run ffprobe; loudness must be -16 LUFS. Tips: https://ffmpeg-tips.example.com/loud
3. Check the frame rate.
4. Check the frame size.
"""


def santa_fix(text, spec, issues):
    if "no invented entities/URLs" in issues:
        text = re.sub(r" ?Tips: https?://\S+", "", text)
    if "factual accuracy" in issues:
        text = re.sub(r"-?\d+ LUFS", spec["facts"]["lufs"] + " LUFS", text)
    if "completeness vs spec" in issues:
        for m in spec["must_cover"]:
            if "## " + m not in text:
                n = len(re.findall(r"^\d+\.", text, re.M)) + 1
                text += "## %s\n%d. Restore the previous export if a check fails.\n" % (m, n)
    n = len(re.findall(r"^\d+\.", text, re.M))
    return re.sub(r"has \d+ steps", "has %d steps" % n, text)


@card("CHECK-15")
def santa_two_reviewers(task, wd):
    """Send output + spec to two isolated reviewers (separate processes, separate folders, independent implementations
    of the same rubric); ship only when both PASS, otherwise fix every critical issue and re-review, at most 3 loops."""
    spec = {"must_cover": ["Install", "Verify", "Rollback"], "allowed_urls": ["https://ffmpeg.org/ffmpeg.html"], "facts": {"lufs": "-14"}}
    rev = tw(wd / "reviewer.py", _REVIEWER)
    text, history = _DRAFT, []
    for loop in range(1, 4):
        verdicts = {}
        for v in ("A", "B"):
            d = wd / ("loop%d_%s" % (loop, v))
            d.mkdir()
            jw(d / "spec.json", spec)
            tw(d / "output.md", text)
            sh([sys.executable, "-I", rev, v, d / "spec.json", d / "output.md", d / "verdict.json"], cwd=d, timeout=20)
            verdicts[v] = json.loads((d / "verdict.json").read_text(encoding="utf-8"))
        history.append({"loop": loop, "A": verdicts["A"]["verdict"], "B": verdicts["B"]["verdict"],
                        "issues": sorted(set(verdicts["A"]["critical_issues"]) | set(verdicts["B"]["critical_issues"]))})
        if all(x["verdict"] == "PASS" for x in verdicts.values()):
            break
        text = santa_fix(text, spec, history[-1]["issues"])
    final = tw(wd / "shipped.md", text) if history[-1]["A"] == history[-1]["B"] == "PASS" else None
    log = jw(wd / "santa_log.json", history)
    keys = set(json.loads((wd / "loop1_A/verdict.json").read_text())) | set(json.loads((wd / "loop1_B/verdict.json").read_text()))
    return [
        check("both reviewers fail the first draft on the same four criteria", history[0]["A"] == history[0]["B"] == "FAIL" and len(history[0]["issues"]) == 4,
              history[0], "4 issues"),
        check("shipped only after both PASS, within 3 loops", final is not None and len(history) <= 3, len(history), "<= 3"),
        check("shipped text keeps only allowed URLs and the -14 LUFS fact", "example.com" not in text and "-14 LUFS" in text and "## Rollback" in text, True, True),
        check("verdict JSON has verdict/checks/critical_issues/suggestions", keys == {"verdict", "checks", "critical_issues", "suggestions"}, sorted(keys), 4),
        check("reviewers ran in separate folders (no shared context)", len({p.parent for p in wd.glob("loop*_*/verdict.json")}) == 2 * len(history), True, True),
        check("negative control: the untreated draft is not shippable", history[0]["A"] == "FAIL", history[0]["A"], "FAIL"),
    ], [final or log, log]


def route(prompt, attachments, installed, broad=False):
    p = prompt.lower()
    if re.fullmatch(r"\s*احسب\s+[\d\s+*/-]+", prompt):
        return {"action": "answer-direct", "skills": []}
    if "what can you do" in p:
        return {"action": "capability-summary", "skills": []}
    if any(w in p for w in ("انشر", "publish", "post to")):
        return {"action": "ask-approval", "skills": []}
    reel = "ريلز" in p or "reel" in p
    if reel and (broad or "audio" in attachments):
        skills = [s for s in ("audio-sync", "arabic-type") if s in installed]
        return {"action": "run", "skills": skills} if skills else {"action": "gap", "skills": []}
    if "بخط عربي" in p and "arabic-type" in installed:
        return {"action": "run", "skills": ["arabic-type"]}
    return {"action": "gap" if any(w in p for w in ("اعمل", "make")) else "answer", "skills": []}


def stale_probe(listing):
    return {k: ("downgraded" if (v == "ok" and not shutil.which(k)) else v) for k, v in listing.items()}


_CASES = [
    ("positive", "اعمل ريلز من الصوت ده", ["audio"], {"action": "run", "skills": ["audio-sync", "arabic-type"]}, "deterministic"),
    ("adjacent-negative", "اشرح لي يعني إيه ريلز", [], {"action": "answer", "skills": []}, "deterministic"),
    ("collision", "عنوان بخط عربي", [], {"action": "run", "skills": ["arabic-type"]}, "deterministic"),
    ("gap", "اعمل فيديو ثلاثي الأبعاد", [], {"action": "gap", "skills": []}, "deterministic"),
    ("side-effect", "انشر الريلز على تيك توك", [], {"action": "ask-approval", "skills": []}, "deterministic"),
    ("trivial", "احسب 37+15", [], {"action": "answer-direct", "skills": []}, "deterministic"),
    ("judged", "what can you do?", [], "summary is accurate and flags missing tools", "judged"),
]


@card("CHECK-21")
def trigger_eval_matrix(task, wd):
    """Trigger eval matrix for a skill: positive, adjacent-negative, collision, gap, side-effect and stale cases (+ a
    trivial one), deterministic cases graded exactly and judged ones set aside for a model, an A/B run with and without
    the skill, dated results."""
    import datetime as dt
    installed = {"audio-sync", "arabic-type"}
    rows = []
    for typ, prompt, att, want, mode in _CASES:
        got_a = route(prompt, att, installed)
        got_b = route(prompt, att, set())
        rows.append({"type": typ, "prompt": prompt, "mode": mode, "with_skill": got_a, "without_skill": got_b,
                     "pass": (got_a == want) if mode == "deterministic" else None})
    stale = stale_probe({"ffmpeg": "ok", "kosif-missing-binary-xyz": "ok"})
    rows.append({"type": "stale", "mode": "deterministic", "probe": stale, "pass": stale == {"ffmpeg": "ok", "kosif-missing-binary-xyz": "downgraded"}})
    res = jw(wd / "trigger_matrix.json", {"date": dt.date.today().isoformat(), "rows": rows})
    det = [r for r in rows if r["mode"] == "deterministic"]
    judged = [r for r in rows if r["mode"] == "judged"]
    ab = rows[0]["with_skill"]["action"] == "run" and rows[0]["without_skill"]["action"] == "gap"
    buggy = route("اشرح لي يعني إيه ريلز", [], installed, broad=True)
    types = {r["type"] for r in rows}
    return [
        check("matrix covers the six case types", {"positive", "adjacent-negative", "collision", "gap", "side-effect", "stale"} <= types, sorted(types), 6),
        check("every deterministic case passes", all(r["pass"] for r in det), [r["type"] for r in det if not r["pass"]], []),
        check("judged cases are not auto-scored", all(r["pass"] is None for r in judged) and len(judged) == 1, len(judged), 1),
        check("A/B: the positive case runs the skill only when it is installed", ab, [rows[0]["with_skill"], rows[0]["without_skill"]], "run / gap"),
        check("results are dated", bool(re.match(r"\d{4}-\d{2}-\d{2}$", json.loads(res.read_text())["date"])), True, True),
        check("negative control: an over-broad trigger fires on the adjacent negative", buggy["action"] == "run", buggy, "run (wrong)"),
    ], [res]


# ================================================================================ CODE: property tests, data contracts

@card("CODE-23")
def hypothesis_shrink(task, wd):
    """Property-based testing with Hypothesis: falsify a property, let it shrink the counter-example to the minimum,
    find the minimal crashing input of a real function, and confirm a true property is never falsified."""
    import hypothesis.configuration as hc
    from hypothesis import find, settings, strategies as st
    from hypothesis.errors import NoSuchExample
    hc.set_hypothesis_home_dir(str(wd / ".hypothesis"))   # keep Hypothesis' storage inside the work folder
    S = settings(database=None, max_examples=3000, deadline=None)
    ex = find(st.lists(st.integers(min_value=0, max_value=1000)), lambda xs: len(xs) >= 3 and sum(xs) >= 100, settings=S)

    def mean_fps(frame_times):
        span = frame_times[-1] - frame_times[0]
        return (len(frame_times) - 1) / span

    def crashes(xs):
        try:
            mean_fps(sorted(xs))
            return False
        except (ZeroDivisionError, IndexError):
            return True
    crash = find(st.lists(st.floats(min_value=0, max_value=60, allow_nan=False), max_size=8), crashes, settings=S)
    try:
        find(st.lists(st.integers()), lambda xs: sorted(sorted(xs)) != sorted(xs), settings=settings(database=None, max_examples=300))
        true_falsified = True
    except NoSuchExample:
        true_falsified = False
    hc.set_hypothesis_home_dir(None)
    rep = jw(wd / "hypothesis_report.json", {"shrunk": ex, "minimal_crash": crash, "true_property_falsified": true_falsified})
    return [
        check("'short or small' falsified and shrunk to [0, 0, 100]", ex == [0, 0, 100], ex, [0, 0, 100]),
        check("minimal crashing input of mean_fps is the empty list", crash == [], crash, []),
        check("no example database written (database=None)", not (wd / ".hypothesis/examples").exists(), (wd / ".hypothesis/examples").exists(), False),
        check("negative control: a true property is never falsified", not true_falsified, true_falsified, False),
    ], [rep]


@card("CODE-24")
def pandera_contract(task, wd):
    """A data contract on pandas and Polars frames with Pandera: fps must be one of 24/25/30/50/60, sizes positive;
    29 fps is rejected with its failure case, 30/60 accepted."""
    import pandas as pd
    import pandera.pandas as pa
    import pandera.polars as pap
    import polars as pl
    allowed = [24, 25, 30, 50, 60]
    schema = pa.DataFrameSchema({"clip": pa.Column(str), "fps": pa.Column(int, pa.Check.isin(allowed)),
                                 "width": pa.Column(int, pa.Check.gt(0)), "height": pa.Column(int, pa.Check.gt(0))}, strict=True)
    good = pd.DataFrame({"clip": ["a", "b"], "fps": [30, 60], "width": [1080, 1080], "height": [1920, 1920]})
    bad = pd.DataFrame({"clip": ["a", "b", "c"], "fps": [30, 29, 60], "width": [1080, 1080, 0], "height": [1920, 1920, 1920]})
    try:
        schema.validate(good)
        good_ok = True
    except pa.errors.SchemaError:
        good_ok = False
    try:
        schema.validate(bad, lazy=True)
        fc = []
    except pa.errors.SchemaErrors as e:
        fc = sorted(int(x) for x in e.failure_cases["failure_case"].tolist())
    pschema = pap.DataFrameSchema({"clip": pap.Column(str), "fps": pap.Column(int, pap.Check.isin(allowed))})
    pschema.validate(pl.DataFrame({"clip": ["a", "b"], "fps": [30, 60]}))
    try:
        pschema.validate(pl.DataFrame({"clip": ["a", "b"], "fps": [30, 29]}))
        pl_rejected = False
    except Exception as e:  # pandera.errors.SchemaError
        pl_rejected = "29" in str(e) or "isin" in str(e)
    rep = jw(wd / "contract.json", {"allowed_fps": allowed, "pandas_failure_cases": fc, "polars_rejected_29": pl_rejected,
                                    "schema": json.loads(schema.to_json())})
    return [
        check("30/60 fps frame accepted", good_ok, good_ok, True),
        check("pandas: failure cases are fps 29 and width 0", fc == [0, 29], fc, [0, 29]),
        check("polars: 29 fps rejected by the same rule", pl_rejected, pl_rejected, True),
        check("negative control: the raw bad frame breaks the rule without the contract", not set(bad["fps"]).issubset(allowed), sorted(set(bad["fps"])), "contains 29"),
    ], [rep]


# ================================================================================ DL / FOOT: link -> montage, studio, matte, reels

def click_track(path, seconds=4.5, bpm=120, rate=44100, tone_amp=0.1, click_amp=0.12):
    np = _np()
    t = np.arange(int(seconds * rate)) / rate
    y = tone_amp * np.sin(2 * np.pi * 220 * t)
    step = 60.0 / bpm
    for k in range(int(seconds / step) + 1):
        i = int(k * step * rate)
        n = min(len(y) - i, int(0.03 * rate))
        if n > 0:
            y[i:i + n] += click_amp * np.sin(2 * np.pi * 1500 * t[:n]) * np.exp(-t[:n] * 120)
    return fx.write_wav(path, y, rate)


def loudnorm_2pass(path, pre="", I=-14, TP=-1.5, LRA=11):
    """First pass measures (print_format=json); returns the linear second-pass loudnorm filter."""
    done = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-map", "0:a:0", "-af",
                           pre + "loudnorm=I=%s:TP=%s:LRA=%s:print_format=json" % (I, TP, LRA), "-f", "null", "-"],
                          capture_output=True, text=True, timeout=60, stdin=subprocess.DEVNULL)
    m = json.loads(done.stderr[done.stderr.rindex("{"):done.stderr.rindex("}") + 1])
    return ("loudnorm=I=%s:TP=%s:LRA=%s:measured_I=%s:measured_TP=%s:measured_LRA=%s:measured_thresh=%s:offset=%s:linear=true"
            % (I, TP, LRA, m["input_i"], m["input_tp"], m["input_lra"], m["input_thresh"], m["target_offset"]))


def scene_times(path, thr=0.3):
    done = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(path), "-vf", "select='gt(scene,%s)',showinfo" % thr, "-f", "null", "-"],
                          capture_output=True, text=True, timeout=60, stdin=subprocess.DEVNULL)
    return [round(float(x), 3) for x in re.findall(r"pts_time:([\d.]+)", done.stderr)]


@card("DL-10")
def link_analyse_montage(task, wd):
    """Link -> analyse -> montage: download the clip from its link (a local HTTP link here), --safe remux (H.264/AAC,
    +faststart), measure duration and cuts (ffmpeg scene), find the beat (librosa), cut on the beat with xfade, add the
    Arabic subtitle track, loudnorm to -14 LUFS, verify. The speech-to-text step uses a supplied transcript: the
    faster-whisper model host is blocked here."""
    import urllib.request
    import librosa
    remote = wd / "remote"
    remote.mkdir()
    aud = click_track(wd / "beat.wav")
    three_shot_clip(remote / "clip.mp4", size="180x320", sec=1.5, audio=aud)
    srv = _Serve(remote)
    try:
        op = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        data = op.open(srv.url + "/clip.mp4", timeout=10).read()
    finally:
        srv.close()
    dl = wd / "dl" / "clip.mp4"
    dl.parent.mkdir()
    dl.write_bytes(data)
    st = {s["codec_type"]: s["codec_name"] for s in fx.probe(dl)["streams"]}
    safe = wd / "safe.mp4"
    fx.ffmpeg("-i", dl, "-map", "0", "-c", "copy", "-movflags", "+faststart", safe)
    dur = duration(safe)
    cuts = scene_times(safe)
    fx.ffmpeg("-i", safe, "-vn", "-ac", "1", "-ar", "22050", wd / "a.wav")
    y, sr = librosa.load(str(wd / "a.wav"), sr=22050)
    on = librosa.onset.onset_detect(y=y, sr=sr, units="time", backtrack=False)
    ioi = float(_np().median(_np().diff(on)))
    tempo = float(_np().atleast_1d(librosa.beat.beat_track(y=y, sr=sr)[0])[0])
    beat = 60.0 / 120 if abs(ioi - 0.5) < 0.05 else ioi
    L, d = 2 * beat, beat
    starts = [0.0] + cuts
    srt = tw(wd / "ar.srt", "1\n00:00:00,000 --> 00:00:01,500\nأهلاً بكم\n\n2\n00:00:01,500 --> 00:00:03,000\nعلى الإيقاع\n")
    parts = "".join("[0:v]trim=%.3f:%.3f,setpts=PTS-STARTPTS[s%d];" % (s0, s0 + L, i) for i, s0 in enumerate(starts))
    offs = [round(L - d, 3), round(2 * (L - d), 3)]
    fc = parts + "[s0][s1]xfade=transition=fade:duration=%.3f:offset=%.3f[x1];[x1][s2]xfade=transition=fade:duration=%.3f:offset=%.3f,format=yuv420p[v];" % (d, offs[0], d, offs[1])
    total = 3 * L - 2 * d
    trim = "atrim=0:%.3f,asetpts=PTS-STARTPTS," % total
    fc += "[0:a]%s%s[a]" % (trim, loudnorm_2pass(safe, pre=trim))
    out = wd / "montage.mp4"
    fx.ffmpeg("-i", safe, "-i", srt, "-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-map", "1:0", "-c:v", "libx264", "-crf", "17",
              "-preset", "veryfast", "-r", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-c:s", "mov_text", "-metadata:s:s:0", "language=ara",
              "-movflags", "+faststart", out)
    pr = fx.probe(out)
    kinds = sorted(s["codec_type"] for s in pr["streams"])
    L_out, L_src = lufs(out), lufs(safe)
    od = float(pr["format"]["duration"])
    fx.ffmpeg("-i", out, "-map", "0:s:0", wd / "out.srt")
    subs = (wd / "out.srt").read_text(encoding="utf-8")
    on_grid = all(abs(o / beat - round(o / beat)) < 1e-6 for o in offs)
    rep = jw(wd / "dl10_report.json", {"source_codecs": st, "duration": dur, "cuts": cuts, "onset_ioi": ioi, "tempo": tempo,
                                       "xfade_offsets": offs, "lufs_out": L_out, "lufs_src": L_src, "streams": kinds,
                                       "asr": "transcript supplied (faster-whisper model host blocked here)"})
    return [
        check("download from the link is byte-identical", sha(dl) == sha(remote / "clip.mp4"), len(data), "same sha256"),
        check("--safe: H.264 + AAC remuxed with faststart", st == {"video": "h264", "audio": "aac"} and abs(dur - 4.5) < 0.1, [st, dur], "h264/aac 4.5 s"),
        check("scene detection finds the two hard cuts", len(cuts) == 2 and abs(cuts[0] - 1.5) < 0.05 and abs(cuts[1] - 3.0) < 0.05, cuts, [1.5, 3.0]),
        check("beat: onsets every 0.5 s (120 BPM)", abs(ioi - 0.5) < 0.03 and abs(tempo - 120) < 8, [ioi, tempo], "0.5 s / ~120"),
        check("xfade transitions start on the beat grid", on_grid, offs, "multiples of 0.5"),
        check("montage length = 3 x 1.0 - 2 x 0.5 = 2.0 s", abs(od - total) < 0.08, od, total),
        check("Arabic subtitle track carried", "subtitle" in kinds and "أهلاً بكم" in subs, kinds, "subtitle with Arabic"),
        check("loudness normalised to -14 LUFS", L_out is not None and abs(L_out + 14) <= 1.0, L_out, -14),
        check("negative control: the downloaded source was far from -14 LUFS", L_src is not None and abs(L_src + 14) > 3, L_src, "far from -14"),
    ], [out, rep]


@card("FOOT-22")
def studio_project_import(task, wd):
    """KOSIF Studio browser project (JSON v1) -> FFmpeg timeline: studio_import.convert() maps clips, text overlays and
    the soundtrack, reports skipped shapes, and the timeline renders offline at -14 LUFS with the delivery gate."""
    media = wd / "media"
    media.mkdir()
    fx.ffmpeg("-f", "lavfi", "-i", "testsrc2=s=320x320:r=30:d=3", "-f", "lavfi", "-i", "sine=f=440:d=3", "-shortest", "-pix_fmt", "yuv420p",
              "-c:v", "libx264", "-c:a", "aac", media / "a.mp4")
    fx.ffmpeg("-f", "lavfi", "-i", "sine=f=220:d=4", media / "song.wav")
    proj = jw(wd / "project.json", {"version": 1, "name": "اختبار", "aspect": "1:1",
                                    "assets": [{"id": "v", "name": "a.mp4", "type": "video"}, {"id": "s", "name": "song.wav", "type": "audio"}],
                                    "clips": [{"type": "video", "assetId": "v", "trim": 1, "duration": 1.5}, {"type": "demo", "preset": "sunset", "duration": 1}],
                                    "overlays": [{"type": "text", "text": "مرحبا", "x": 50, "y": 80, "size": 10, "color": "#ffcc00", "start": 0, "duration": 2},
                                                 {"type": "shape", "start": 0, "duration": 1}],
                                    "soundtrack": {"assetId": "s", "volume": 0.5}})
    film = wd / "film.mp4"
    done = sh([sys.executable, MM / "studio_import.py", proj, "--out", wd / "edit.json", "--media", media, "--size", "360x360",
               "--render", film], cwd=wd, env=py_env(wd), timeout=60)
    rep = json.loads(done.stdout[done.stdout.index("{"):])
    spec = json.loads((wd / "edit.json").read_text(encoding="utf-8"))
    vs = vstream(film)
    fr = fx.frames(film, size=(36, 36))
    colour = fr[int(2.0 * 30)].reshape(-1, 3).mean(axis=0)
    first = fr[10].std()
    L = lufs(film)
    sys.path.insert(0, str(MM))
    import studio_import as si
    try:
        si.convert({"version": 7})
        bad_refused = False
    except ValueError:
        bad_refused = True
    return [
        check("video clip mapped with trim in/out", spec["clips"][0].get("in") == 1.0 and spec["clips"][0].get("out") == 2.5, spec["clips"][0], "in 1 out 2.5"),
        check("demo clip became the sunset colour card", spec["clips"][1] == {"color": "#3a1a12", "dur": 1.0}, spec["clips"][1], "#3a1a12 1 s"),
        check("text overlay mapped to fractions and px", (spec["overlays"][0]["x"], spec["overlays"][0]["y"], spec["overlays"][0]["size"]) == (0.5, 0.8, 36),
              spec["overlays"][0], "0.5, 0.8, 36 px"),
        check("shape overlay reported as skipped", rep["skipped"] and rep["skipped"][0]["type"] == "shape", rep["skipped"], "shape"),
        check("rendered 360x360, 2.5 s, delivery gate ok", (vs["width"], vs["height"]) == (360, 360) and abs(duration(film) - 2.5) < 0.1 and rep["gate"]["ok"],
              [vs["width"], vs["height"], duration(film), rep["gate"]["ok"]], "360x360 2.5 s ok"),
        check("frame at 2.0 s is the sunset card, first frames are footage", abs(colour[0] - 0x3a) < 12 and abs(colour[2] - 0x12) < 12 and first > 20,
              [colour.round().tolist(), round(float(first), 1)], "#3a1a12 / textured"),
        check("loudness -14 LUFS", L is not None and abs(L + 14) <= 1, L, -14),
        check("negative control: a non-Studio project (version 7) is refused", bad_refused, bad_refused, True),
    ], [film, wd / "edit.json"]


def _presenter(i, W=320, H=320):
    np = _np()
    from PIL import Image, ImageDraw
    y, x = np.mgrid[0:H, 0:W]
    bg = np.stack([60 + x * 0.3, 90 + y * 0.2, np.full_like(x, 140.0)], -1)
    im = Image.fromarray(bg.astype("uint8"))
    m = Image.new("L", (W, H), 0)
    dx = 10 * i
    for dr, fill in ((ImageDraw.Draw(im), None), (ImageDraw.Draw(m), 255)):
        dr.ellipse((130 + dx, 50, 190 + dx, 115), fill=fill or (224, 172, 140))
        dr.rounded_rectangle((100 + dx, 115, 220 + dx, 320), radius=40, fill=fill or (200, 40, 40))
    return im, np.asarray(m) > 127


@card("FOOT-31")
def person_matte(task, wd):
    """Presenter cut-out: a U2-Net matte (rembg, the 4.6 MB u2netp model) on each frame, written as an alpha video (MOV,
    PNG codec, rgba) plus the optional inverse background plate. Measured against the drawn ground-truth masks."""
    from rembg import new_session, remove
    np = _np()
    if not (Path.home() / ".u2net/u2netp.onnx").exists():
        raise RuntimeError("u2netp model missing (~/.u2net/u2netp.onnx)")
    sess = new_session("u2netp")
    (wd / "rgba").mkdir()
    (wd / "plate").mkdir()
    ious, plate_in = [], []
    for i in range(3):
        im, gt = _presenter(i)
        im.save(wd / ("src_%d.png" % i))
        out = remove(im, session=sess)
        out.save(wd / "rgba" / ("f%03d.png" % i))
        a = np.asarray(out)[..., 3] / 255.0
        ious.append(float(((a > 0.5) & gt).sum() / ((a > 0.5) | gt).sum()))
        plate = np.asarray(im).astype(float) * (1 - a[..., None])
        save_png(plate, wd / "plate" / ("f%03d.png" % i))
        plate_in.append(float(plate[gt].mean()))
    fx.ffmpeg("-framerate", "3", "-i", wd / "rgba/f%03d.png", "-c:v", "png", "-pix_fmt", "rgba", wd / "presenter.mov")
    fx.ffmpeg("-framerate", "3", "-i", wd / "plate/f%03d.png", "-c:v", "libx264", "-pix_fmt", "yuv420p", wd / "plate.mp4")
    vs = vstream(wd / "presenter.mov")
    _, gt0 = _presenter(0)
    opaque_iou = float(gt0.sum() / gt0.size)
    return [
        check("matte matches the presenter (IoU >= 0.9 on every frame)", min(ious) >= 0.9, ious, ">= 0.9"),
        check("alpha video is rgba MOV with 3 frames", vs["pix_fmt"] == "rgba" and int(vs.get("nb_frames", 3)) == 3, [vs["pix_fmt"], vs.get("nb_frames")], "rgba, 3"),
        check("inverse plate is empty where the presenter was", max(plate_in) < 15, plate_in, "< 15"),
        check("matte follows the presenter moving 10 px per frame", all(x >= 0.9 for x in ious[1:]), ious[1:], ">= 0.9"),
        check("negative control: the untreated (fully opaque) frame is not a matte", opaque_iou < 0.6, opaque_iou, "< 0.6"),
    ], [wd / "presenter.mov", wd / "plate.mp4"]


@card("FOOT-55")
def talking_clip_reel(task, wd):
    """One command, raw talking clip -> vertical reel: reel.py transcript (pre-timed words.json, since the Whisper model
    host is blocked here) + decaption in parallel, restore + reframe, voice chain, karaoke captions, -14 LUFS, gate."""
    clip = wd / "clip.mp4"
    fx.ffmpeg("-f", "lavfi", "-i", "testsrc2=s=640x360:r=30:d=2.5", "-f", "lavfi", "-i", "sine=f=300:d=2.5,volume=0.3", "-shortest",
              "-pix_fmt", "yuv420p", "-c:v", "libx264", "-c:a", "aac", clip)
    words = jw(wd / "talk.words.json", [{"start": 0.2, "end": 2.3, "text": "مرحبا بكم هنا", "words": [
        {"text": "مرحبا", "start": 0.2, "end": 0.9}, {"text": "بكم", "start": 1.0, "end": 1.6}, {"text": "هنا", "start": 1.7, "end": 2.3}]}])
    final = wd / "final.mp4"
    done = sh([sys.executable, MM / "reel.py", clip, "--out", final, "--size", "360x640", "--music", "none", "--transcript", words],
              cwd=wd, env=py_env(wd), timeout=60)
    rep = json.loads((wd / "final.reel.json").read_text(encoding="utf-8"))
    vs = vstream(final)
    srt = (wd / "final.srt").read_text(encoding="utf-8")
    L, Ls = lufs(final), lufs(clip)
    svs = vstream(clip)
    return [
        check("vertical 360x640 output", (vs["width"], vs["height"]) == (360, 640), [vs["width"], vs["height"]], [360, 640]),
        check("delivery gate ok", rep["gate"]["ok"], rep["gate"], "ok"),
        check("loudness -14 LUFS (+-1)", L is not None and abs(L + 14) <= 1, L, -14),
        check("captions written from the timed words", all(w in srt for w in ("مرحبا", "بكم", "هنا")), srt.count("-->"), ">= 1 cue"),
        check("decaption pass ran on the source", "decaption" in rep, sorted(rep), "decaption"),
        check("negative control: the raw clip is landscape and not at -14 LUFS", (svs["width"] > svs["height"]) and abs((Ls or 0) + 14) > 2, [svs["width"], svs["height"], Ls], "landscape, far"),
    ], [final, wd / "final.srt"]


def _clip_metrics(path):
    np = _np()
    f = fx.frames(path, size=(64, 36))
    g = f.mean(axis=-1)
    lum = g.mean(axis=(1, 2))
    lap = np.array([np.abs(np.diff(x, 2, axis=0)).mean() + np.abs(np.diff(x, 2, axis=1)).mean() for x in g])
    mot = np.r_[0, np.abs(np.diff(g, axis=0)).mean(axis=(1, 2))]
    return {"lum": lum, "sharp": lap, "motion": mot, "n": len(g)}


def best_window(m, L, fps=30, avoid=()):
    np = _np()
    n = int(L * fps)
    score = m["motion"] / (m["motion"].max() + 1e-9) + m["sharp"] / (m["sharp"].max() + 1e-9) + (m["lum"] > 40)
    best, arg = -1, 0
    for s in range(0, m["n"] - n + 1):
        if any(s <= a < s + n for a in avoid):
            continue
        v = float(score[s:s + n].mean())
        if v > best:
            best, arg = v, s
    return arg / fps


@card("FOOT-58")
def basma_beat_montage(task, wd):
    """Beat montage of up to 24 clips: probe in parallel batches of 3, a 4-column numbered contact sheet, an order
    (here a deterministic quality score stands in for the AI's choice), lengths snapped to the beat within 0.4 s, and a
    bestWindow per clip that picks the lively, sharp, well-lit part away from cuts; then the cut."""
    from concurrent.futures import ThreadPoolExecutor
    from PIL import Image, ImageDraw
    np = _np()
    clips = []
    recipes = [("bright_static", "color=c=0x8899aa:s=160x90:r=30:d=2"), ("dark", "color=c=0x080808:s=160x90:r=30:d=2"),
               ("lively", "testsrc2=s=160x90:r=30:d=2"), ("half_motion", None), ("bars", "smptebars=s=160x90:r=30:d=2"),
               ("mandel", "mandelbrot=s=160x90:r=30")]
    for i, (name, src) in enumerate(recipes):
        p = wd / ("c%02d_%s.mp4" % (i + 1, name))
        if name == "half_motion":
            fx.ffmpeg("-f", "lavfi", "-i", "color=c=0x777777:s=160x90:r=30:d=1", "-f", "lavfi", "-i", "testsrc2=s=160x90:r=30:d=1",
                      "-filter_complex", "[0][1]concat=n=2:v=1[v]", "-map", "[v]", "-pix_fmt", "yuv420p", "-c:v", "libx264", p)
        else:
            fx.ffmpeg("-f", "lavfi", "-i", src, "-t", "2", "-pix_fmt", "yuv420p", "-c:v", "libx264", p)
        clips.append(p)
    with ThreadPoolExecutor(3) as ex:
        metrics = list(ex.map(_clip_metrics, clips))
    thumbs = [load_png(save_png(fx.frames(c, size=(160, 90))[30], wd / ("thumb_%d.png" % i))) for i, c in enumerate(clips)]
    cols, rows = 4, math.ceil(len(clips) / 4)
    sheet = Image.new("RGB", (cols * 160, rows * 90), (0, 0, 0))
    dr = ImageDraw.Draw(sheet)
    for i, t in enumerate(thumbs):
        sheet.paste(Image.fromarray(t.astype("uint8")), ((i % cols) * 160, (i // cols) * 90))
        dr.rectangle(((i % cols) * 160, (i // cols) * 90, (i % cols) * 160 + 22, (i // cols) * 90 + 16), fill=(255, 220, 0))
        dr.text(((i % cols) * 160 + 4, (i // cols) * 90 + 2), str(i + 1), fill=(0, 0, 0))
    sheet.save(wd / "contact_sheet.png")
    score = [float(m["motion"].mean() * 2 + m["sharp"].mean() + (m["lum"].mean() > 40) * 5) for m in metrics]
    order = sorted(range(len(clips)), key=lambda i: -score[i])
    beat = 60.0 / 120
    wanted = [1.3, 1.1, 0.9, 1.2, 0.7, 1.0]
    snapped = [max(beat, round(w / beat) * beat) for w in wanted]
    starts = [best_window(metrics[i], snapped[k]) for k, i in enumerate(order)]
    segs = "".join("[%d:v]trim=%.3f:%.3f,setpts=PTS-STARTPTS[s%d];" % (k, s0, s0 + snapped[j], j) for j, (k, s0) in enumerate(zip(order, starts)))
    ins = sum((["-i", str(clips[k])] for k in order), [])
    out = wd / "montage.mp4"
    fx.ffmpeg(*ins, "-filter_complex", segs + "".join("[s%d]" % j for j in range(len(order))) + "concat=n=%d:v=1[v]" % len(order),
              "-map", "[v]", "-pix_fmt", "yuv420p", "-c:v", "libx264", "-preset", "veryfast", out)
    cut_times = list(np.cumsum(snapped))[:-1]
    od = duration(out)
    hm = order.index(3)
    unsnapped_cuts = list(np.cumsum(wanted))[:-1]
    return [
        check("contact sheet is 4 columns x 2 rows, numbered", Image.open(wd / "contact_sheet.png").size == (640, 180), Image.open(wd / "contact_sheet.png").size, [640, 180]),
        check("dark clip ranked last, lively clip first", order[-1] == 1 and order[0] in (2, 5), order, "last=dark"),
        check("every length moved at most 0.4 s to snap to the beat", all(abs(a - b) <= 0.4 for a, b in zip(snapped, wanted)), [snapped, wanted], "<= 0.4"),
        check("every cut lands on a beat", all(abs(t / beat - round(t / beat)) < 1e-9 for t in cut_times), cut_times, "multiples of 0.5"),
        check("bestWindow skips the static first half of the half-motion clip", starts[hm] >= 0.9, starts[hm], ">= 1.0 s"),
        check("montage length equals the snapped plan", abs(od - sum(snapped)) < 0.1, od, sum(snapped)),
        check("negative control: unsnapped lengths put cuts off the beat", any(abs(t / beat - round(t / beat)) > 1e-6 for t in unsnapped_cuts), unsnapped_cuts, "off-beat"),
    ], [out, wd / "contact_sheet.png"]


_APP = """<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>body{margin:0;font:20px sans-serif;background:#0b1020;color:#fff}main{max-width:900px;margin:auto;padding:16px}
svg{width:100%%;height:auto;display:block}button{font-size:24px;padding:12px 20px;margin:12px 0}%s</style></head><body><main>
<h1>Beat counter</h1><svg viewBox="0 0 300 100"><rect x="10" y="10" width="60" height="80" fill="#334"/><rect x="80" y="10" width="60" height="80" fill="#334"/>
<rect x="150" y="10" width="60" height="80" fill="#334"/><rect x="220" y="10" width="60" height="80" fill="#334"/></svg>
<button id="b">+1 beat</button><p>Beats: <span id="n">0</span></p></main>
<script>let n=0;document.getElementById('b').onclick=()=>{n++;document.getElementById('n').textContent=n;document.querySelectorAll('rect')[(n-1)%%4].setAttribute('fill','#f4c542');};</script></body></html>"""


@card("IDEA-24")
def app_media_combo(task, wd):
    """APP + MEDIA: an interactive page with code-drawn SVG visuals, checked at 390 px and 1440 px, a scripted
    walkthrough recorded with Playwright, turned into a 1080x1920 reel with a sound bed at -14 LUFS, verified."""
    page = tw(wd / "app.html", _APP % "")
    fixed = tw(wd / "fixed.html", _APP % "main{width:1200px;max-width:none}")
    js = """const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const out={};
for (const [name,f] of [['app',%s],['fixed',%s]]) for (const [w,h] of [[390,844],[1440,900]]){const p=await b.newPage({viewport:{width:w,height:h}});
 await p.goto('file://'+f); out[name+w]=await p.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth); await p.close();}
const ctx=await b.newContext({viewport:{width:390,height:844},recordVideo:{dir:%s,size:{width:390,height:844}}});
const p=await ctx.newPage(); await p.goto('file://'+%s); await p.waitForTimeout(400);
for(let i=0;i<3;i++){await p.click('#b'); await p.waitForTimeout(350);} out.count=await p.textContent('#n'); await p.waitForTimeout(400);
const v=await p.video().path(); await ctx.close(); out.video=v; await b.close(); console.log(JSON.stringify(out));})();""" % (
        json.dumps(str(page)), json.dumps(str(fixed)), json.dumps(str(wd / "rec")), json.dumps(str(page)))
    res = node_js(wd, "walkthrough", js, timeout=60)
    reel = wd / "reel.mp4"
    nfr = len(fx.frames(res["video"], size=(8, 8)))
    fx.ffmpeg("-i", res["video"], "-f", "lavfi", "-i", "sine=f=220:sample_rate=48000:d=%.2f" % (nfr / 25.0 + 1), "-filter_complex",
              "[0:v]scale=-2:1920:flags=lanczos,pad=1080:1920:(ow-iw)/2:0:color=0x0b1020,fps=30,format=yuv420p[v];[1:a]volume=0.05,loudnorm=I=-14:TP=-1.5[a]",
              "-map", "[v]", "-map", "[a]", "-shortest", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-c:a", "aac", "-b:a", "192k",
              "-movflags", "+faststart", reel, timeout=40)
    vs = vstream(reel)
    fr = fx.frames(reel, size=(108, 192))
    yellow = lambda f: int(((f[..., 0] > 200) & (f[..., 1] > 160) & (f[..., 2] < 120)).sum())
    L = lufs(reel)
    return [
        check("page fits at 390 px and 1440 px (no horizontal scroll)", res["app390"] and res["app1440"], [res["app390"], res["app1440"]], [True, True]),
        check("three scripted clicks counted on the page", res["count"] == "3", res["count"], "3"),
        check("reel is 1080x1920 at 30 fps", (vs["width"], vs["height"]) == (1080, 1920) and vs["r_frame_rate"] == "30/1",
              [vs["width"], vs["height"], vs["r_frame_rate"]], "1080x1920 30/1"),
        check("recorded clicks visible: lit bars at the end, none at the start", yellow(fr[-1]) > 20 and yellow(fr[0]) == 0, [yellow(fr[0]), yellow(fr[-1])], "0 -> > 20"),
        check("sound bed at -14 LUFS", L is not None and abs(L + 14) <= 1, L, -14),
        check("negative control: a fixed-width layout overflows at 390 px", not res["fixed390"], res["fixed390"], False),
    ], [reel, page]


# ================================================================================ PROD: market metrics, CP-SAT, LP, physics

@card("PROD-15")
def market_tearsheet(task, wd):
    """Portfolio tear-sheet metrics with quantstats on a deterministic return series (no unofficial market endpoint is
    called: yfinance scrapes Yahoo and is not used), cross-checked against the formulas, and the HTML tear-sheet."""
    import pandas as pd
    import quantstats as qs
    np = _np()
    idx = pd.bdate_range("2025-01-01", periods=252)
    r = pd.Series(0.0008 + 0.012 * np.sin(np.arange(252) / 5.0), index=idx)
    sharpe = float(qs.stats.sharpe(r))
    mdd = float(qs.stats.max_drawdown(r))
    vol = float(qs.stats.volatility(r))
    eq = (1 + r).cumprod()
    m_sharpe = float(r.mean() / r.std(ddof=1) * math.sqrt(252))
    m_mdd = float((eq / eq.cummax() - 1).min())
    m_vol = float(r.std(ddof=1) * math.sqrt(252))
    rep = wd / "tearsheet.html"
    import matplotlib
    matplotlib.use("Agg")
    qs.reports.html(r, output=str(rep), title="Fixture strategy", download_filename=str(rep))
    up = pd.Series(0.001, index=idx)
    out = jw(wd / "metrics.json", {"sharpe": sharpe, "max_drawdown": mdd, "volatility": vol, "data_source": "deterministic fixture (no yfinance call)"})
    html = rep.read_text(encoding="utf-8", errors="replace") if rep.exists() else ""
    return [
        check("Sharpe equals mean/std*sqrt(252)", abs(sharpe - m_sharpe) < 1e-6, [sharpe, m_sharpe], "equal"),
        check("max drawdown equals the equity-curve formula", abs(mdd - m_mdd) < 1e-9 and mdd < -0.05, [mdd, m_mdd], "equal, < -5%"),
        check("annualised volatility equals std*sqrt(252)", abs(vol - m_vol) < 1e-9, [vol, m_vol], "equal"),
        check("HTML tear-sheet written with the title", "Fixture strategy" in html and len(html) > 5000, len(html), "> 5000 bytes"),
        check("negative control: a never-falling series has no drawdown", float(qs.stats.max_drawdown(up)) == 0.0, float(qs.stats.max_drawdown(up)), 0.0),
    ], [rep, out]


@card("PROD-16")
def ortools_cpsat(task, wd):
    """CP-SAT: the classic 3-job x 3-machine job shop (optimal makespan 11) and 4 jobs on one machine (makespan 10),
    with no-overlap and precedence constraints, solved to proven optimality."""
    from ortools.sat.python import cp_model
    jobs = [[(0, 3), (1, 2), (2, 2)], [(0, 2), (2, 1), (1, 4)], [(1, 4), (2, 3)]]
    m = cp_model.CpModel()
    horizon = sum(d for j in jobs for _, d in j)
    starts, ends, per_machine = {}, {}, {}
    for j, ops in enumerate(jobs):
        for k, (mc, d) in enumerate(ops):
            s, e = m.NewIntVar(0, horizon, "s%d%d" % (j, k)), m.NewIntVar(0, horizon, "e%d%d" % (j, k))
            per_machine.setdefault(mc, []).append(m.NewIntervalVar(s, d, e, "i%d%d" % (j, k)))
            starts[j, k], ends[j, k] = s, e
            if k:
                m.Add(s >= ends[j, k - 1])
    for iv in per_machine.values():
        m.AddNoOverlap(iv)
    mk = m.NewIntVar(0, horizon, "mk")
    m.AddMaxEquality(mk, [ends[j, len(o) - 1] for j, o in enumerate(jobs)])
    m.Minimize(mk)
    sol = cp_model.CpSolver()
    sol.parameters.max_time_in_seconds = 10
    st = sol.Solve(m)
    sched = {"%d.%d" % k: [sol.Value(starts[k]), sol.Value(ends[k])] for k in starts}
    ok_overlap = True
    for mc in per_machine:
        ivs = sorted([sched["%d.%d" % (j, k)] for j, o in enumerate(jobs) for k, (mm, _) in enumerate(o) if mm == mc])
        ok_overlap &= all(a[1] <= b[0] for a, b in zip(ivs, ivs[1:]))
    m2 = cp_model.CpModel()
    d2 = [3, 2, 4, 1]
    iv2, e2 = [], []
    for i, d in enumerate(d2):
        s = m2.NewIntVar(0, 20, "s%d" % i)
        e = m2.NewIntVar(0, 20, "e%d" % i)
        iv2.append(m2.NewIntervalVar(s, d, e, "i%d" % i))
        e2.append(e)
    m2.AddNoOverlap(iv2)
    mk2 = m2.NewIntVar(0, 20, "mk2")
    m2.AddMaxEquality(mk2, e2)
    m2.Minimize(mk2)
    s2 = cp_model.CpSolver()
    st2 = s2.Solve(m2)
    out = jw(wd / "schedule.json", {"status": sol.StatusName(st), "makespan": sol.Value(mk), "schedule": sched, "single_machine": s2.Value(mk2)})
    return [
        check("job shop solved to OPTIMAL", st == cp_model.OPTIMAL, sol.StatusName(st), "OPTIMAL"),
        check("optimal makespan is 11", sol.Value(mk) == 11, sol.Value(mk), 11),
        check("no two operations overlap on a machine", ok_overlap, ok_overlap, True),
        check("4 jobs on one machine: optimal makespan 10", st2 == cp_model.OPTIMAL and s2.Value(mk2) == 10, s2.Value(mk2), 10),
        check("negative control: running every operation in sequence takes 21", horizon == 21 and horizon > sol.Value(mk), horizon, 21),
    ], [out]


@card("PROD-17")
def pulp_lp(task, wd):
    """PuLP: max 3a + 2b s.t. a + b <= 100, a <= 60 -> 260 at (60, 40), and an integer budget split, solved with the
    available solver (HiGHS here; PuLP 4 ships no CBC)."""
    import pulp
    solver = pulp.getSolver(pulp.listSolvers(onlyAvailable=True)[0], msg=False)
    p = pulp.LpProblem("mix", pulp.LpMaximize)
    a, b = p.add_variable("a", 0, 1000, cat="Integer"), p.add_variable("b", 0, 1000, cat="Integer")  # CP-SAT needs finite bounds
    p += 3 * a + 2 * b
    p += a + b <= 100
    p += a <= 60
    rp = p.solve(solver)
    q = pulp.LpProblem("budget", pulp.LpMaximize)
    ch = ["reels", "shorts", "stories"]
    reach = {"reels": 5, "shorts": 4, "stories": 2}
    x = {c: q.add_variable("x_" + c, 0, 1000, cat="Integer") for c in ch}
    q += pulp.lpSum(reach[c] * x[c] for c in ch)
    q += pulp.lpSum(x.values()) <= 10
    q += x["reels"] <= 4
    q += x["stories"] >= 2
    q.solve(solver)
    p2 = pulp.LpProblem("relaxed", pulp.LpMaximize)
    a2, b2 = p2.add_variable("a2", 0, 1000), p2.add_variable("b2", 0, 1000)
    p2 += 3 * a2 + 2 * b2
    p2 += a2 + b2 <= 100
    p2.solve(solver)
    out = jw(wd / "lp.json", {"solver": solver.name, "status": rp.status.name, "a": a.value(), "b": b.value(), "obj": pulp.value(p.objective),
                              "budget": {c: x[c].value() for c in ch}, "budget_reach": pulp.value(q.objective), "relaxed_obj": pulp.value(p2.objective)})
    return [
        check("LP optimal", rp.status.name == "Optimal", rp.status.name, "Optimal"),
        check("objective 260 at a=60, b=40", (round(pulp.value(p.objective)), round(a.value()), round(b.value())) == (260, 60, 40),
              [pulp.value(p.objective), a.value(), b.value()], [260, 60, 40]),
        check("budget split: 4 reels, 4 shorts, 2 stories -> reach 40", {c: round(x[c].value()) for c in ch} == {"reels": 4, "shorts": 4, "stories": 2}
              and round(pulp.value(q.objective)) == 40, {c: x[c].value() for c in ch}, "4/4/2, 40"),
        check("negative control: without a <= 60 the optimum moves to 300", round(pulp.value(p2.objective)) == 300, pulp.value(p2.objective), 300),
    ], [out]


_MJ = """<mujoco><option timestep="0.001" gravity="0 0 -9.81"/><worldbody>
<body name="ball" pos="0 0 1"><freejoint/><geom type="sphere" size="0.05" mass="1" contype="0" conaffinity="0"/></body>
<body name="pend" pos="2 0 2"><joint name="hinge" type="hinge" axis="0 1 0" damping="0"/>
<geom type="sphere" pos="0 0 -1" size="0.01" mass="1" contype="0" conaffinity="0"/></body></worldbody></mujoco>"""


@card("PROD-18")
def mujoco_sim(task, wd):
    """MuJoCo: simulate a free-falling ball and a 1 m pendulum, log the trajectories to CSV and compare with the
    analytic answers (z = 1 - g t^2 / 2; small-angle period 2 pi sqrt(L/g))."""
    import mujoco
    np = _np()
    m = mujoco.MjModel.from_xml_string(_MJ)
    d = mujoco.MjData(m)
    d.qpos[7] = 0.05
    rows, zs, angs = [], [], []
    z0 = float(d.qpos[2])
    while d.time < 4.0 - 1e-9:
        mujoco.mj_step(m, d)
        rows.append((round(d.time, 6), float(d.qpos[2]), float(d.qpos[7])))
    log = tw(wd / "trajectory.csv", "t,ball_z,pend_angle\n" + "".join("%.4f,%.6f,%.6f\n" % r for r in rows))
    t = np.array([r[0] for r in rows])
    z = np.array([r[1] for r in rows])
    th = np.array([r[2] for r in rows])
    i3 = int(np.argmin(np.abs(t - 0.3)))
    err = abs(z[i3] - (1 - 9.81 * 0.3 ** 2 / 2))
    up = np.where((th[:-1] < 0) & (th[1:] >= 0))[0]
    period = float(np.mean(np.diff(t[up]))) if len(up) >= 2 else None
    I = 1.0 + 0.4 * 1 * 0.01 ** 2
    want = 2 * math.pi * math.sqrt(I / 9.81)
    return [
        check("free fall: z(0.3 s) matches 1 - g t^2/2 within 2 mm", err < 2e-3, [float(z[i3]), 1 - 9.81 * 0.09 / 2], "within 0.002"),
        check("pendulum period matches 2 pi sqrt(L/g) within 1 %", period is not None and abs(period - want) / want < 0.01, [period, want], "within 1 %"),
        check("trajectory logged for 4 s at 1 ms steps", len(rows) == 4000, len(rows), 4000),
        check("negative control: the unsimulated start state is not the 0.3 s answer", abs(z0 - (1 - 9.81 * 0.09 / 2)) > 0.4, z0, "far from 0.559"),
    ], [log]


# ================================================================================ RETRO: twos, print treatments, HUD, synthwave, glitch

@card("RETRO-06")
def integer_grid_twos(task, wd):
    """All motion snaps to whole pixels on a 64x36 logical grid (Math.round), and time is quantised to twos
    (t2 = floor(t*12)/12): an 8x8 block crosses the grid, upscaled x5 nearest-neighbour, 24 fps."""
    np = _np()
    fps, W, H, S = 24, 64, 36, 5

    def x_at(t):
        return 4 + 37 * t / 2.0

    frames, xs = [], []
    for f in range(2 * fps):
        t = f / fps
        t2 = math.floor(t * 12) / 12
        x = int(round(x_at(t2)))
        xs.append(x)
        img = np.zeros((H, W, 3))
        img[14:22, x:x + 8] = (255, 200, 40)
        frames.append(np.kron(img, np.ones((S, S, 1))))
    out = write_video(wd / "twos.mp4", frames, fps)
    fr = read_video(out)
    lefts = [int(np.argmax((f[75, :, 0] > 128))) for f in fr]
    on_grid = all(l % S == 0 for l in lefts)
    changes = sum(1 for a, b in zip(lefts, lefts[1:]) if a != b)
    holds = [len(list(g)) for _, g in __import__("itertools").groupby(lefts)]
    smooth = [x_at(f / fps) for f in range(2 * fps)]
    frac = sum(1 for v in smooth if abs(v - round(v)) > 1e-9)
    return [
        check("block edge always on the logical pixel grid (multiples of 5 px)", on_grid, sorted(set(l % S for l in lefts)), [0]),
        check("12 drawings per second: 23 changes in 2 s at 24 fps", changes == 23, changes, 23),
        check("every drawing is held for exactly two frames", set(holds) == {2}, sorted(set(holds)), [2]),
        check("moves in whole logical pixels", all(float(x).is_integer() for x in xs), xs[:6], "integers"),
        check("negative control: unquantised motion lands on fractional pixels", frac > 20, frac, "> 20 of 48"),
    ], [out]


@card("RETRO-14")
def hyperframes_print_treatments(task, wd):
    """HyperFrames print treatments, non-destructive: `hyperframes media-treatment --apply` writes data attributes for
    Two-Ink Print on one image and Halftone on another (the source files stay untouched), and `hyperframes snapshot`
    renders the result, where the ink reduction and the dot raster are measured."""
    from PIL import Image
    np = _np()
    proj = wd / "hf"
    proj.mkdir()
    shutil.copy(NM / "gsap/dist/gsap.min.js", proj / "gsap.min.js")
    y, x = np.mgrid[0:270, 0:240]
    grad = np.stack([x * 255 / 239, y * 255 / 269, np.full_like(x, 128.0)], -1)
    save_png(grad, proj / "a.png")
    save_png(grad, proj / "b.png")
    before = (sha(proj / "a.png"), sha(proj / "b.png"))
    tw(proj / "index.html", """<!doctype html><html><head><meta charset="UTF-8"><script src="gsap.min.js"></script>
<style>html,body{margin:0;width:480px;height:270px;overflow:hidden;background:#000}img{position:absolute;top:0;width:240px;height:270px}#a{left:0}#b{left:240px}</style></head>
<body><div id="root" data-composition-id="main" data-start="0" data-duration="2" data-width="480" data-height="270">
<img id="a" class="clip" src="a.png" data-start="0" data-duration="2" data-track-index="0"><img id="b" class="clip" src="b.png" data-start="0" data-duration="2" data-track-index="1"></div>
<script>window.__timelines=window.__timelines||{};const tl=gsap.timeline({paused:true});tl.to("#a",{opacity:1,duration:2},0);window.__timelines["main"]=tl;</script></body></html>""")
    env = node_env(HOME=wd / "home", HYPERFRAMES_NO_TELEMETRY=1, HYPERFRAMES_NO_UPDATE_CHECK=1, HYPERFRAMES_SKIP_SKILLS=1)
    ra = sh([HF, "media-treatment", "--project", proj, "--selector", "#a", "--grading", json.dumps({"effects": {"twoInkPrint": 1, "twoInkPrintSize": 0.42}}),
             "--apply", "--json"], cwd=proj, env=env, timeout=60)
    rb = sh([HF, "media-treatment", "--project", proj, "--selector", "#b", "--grading", json.dumps({"effects": {"halftone": 1, "halftoneSize": 0.5}}),
             "--apply", "--json"], cwd=proj, env=env, timeout=60)
    html = (proj / "index.html").read_text(encoding="utf-8")
    sh([HF, "snapshot", ".", "--at", "0.5", "--no-end", "--json", "-o", wd / "snaps"], cwd=proj, env=env, timeout=90)
    shot = load_png(sorted((wd / "snaps").glob("frame-*.png"))[0])
    A, B = shot[:, :240], shot[:, 240:]

    def top_share(img, k=8):
        u, n = np.unique(img.reshape(-1, 3).round(), axis=0, return_counts=True)
        return float(np.sort(n)[::-1][:k].sum() / n.sum())

    def hf_energy(img):
        g = img.mean(axis=-1)
        return float(np.abs(np.diff(g, axis=1)).mean() + np.abs(np.diff(g, axis=0)).mean())

    after = (sha(proj / "a.png"), sha(proj / "b.png"))
    attrs = re.findall(r'data-color-grading="([^"]+)"', html)
    import html as H
    effs = [json.loads(H.unescape(a))["effects"] for a in attrs]
    return [
        check("treatments written as data attributes on both images", len(attrs) == 2 and effs[0]["twoInkPrint"] == 1 and effs[1]["halftone"] == 1,
              [len(attrs), effs[0].get("twoInkPrint"), effs[1].get("halftone")], [2, 1, 1]),
        check("non-destructive: source files unchanged", before == after, True, True),
        check("two-ink: 8 colours cover most of the image", top_share(A) > 0.6, top_share(A), "> 0.6"),
        check("halftone: a dot raster (high-frequency energy x5 over the gradient)", hf_energy(B) > 5 * hf_energy(grad), [hf_energy(B), hf_energy(grad)], "> 5x"),
        check("negative control: the untreated gradient has no dominant inks", top_share(grad) < 0.01, top_share(grad), "< 0.01"),
    ], [sorted((wd / "snaps").glob("frame-*.png"))[0], proj / "index.html"]


@card("RETRO-17")
def camcorder_hud(task, wd):
    """Camcorder HUD installed with `hyperframes add camcorder-hud` (4 s overlay, GSAP paused timeline), mounted in
    Chromium over footage, seeked: the counter and the REC blink come from the timeline, not the wall clock."""
    hf = wd / "hf"
    hf.mkdir()
    res = sh([HF, "add", "camcorder-hud", "--no-clipboard", "--json", "--dir", hf], cwd=hf, env=node_env(HOME=wd / "home", HYPERFRAMES_NO_TELEMETRY=1, HYPERFRAMES_NO_UPDATE_CHECK=1, HYPERFRAMES_SKIP_SKILLS=1), timeout=60)
    comp = hf / "compositions/camcorder-hud.html"
    src = comp.read_text(encoding="utf-8")
    page = src.replace('<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>',
                       "<script>%s</script>" % (NM / "gsap/dist/gsap.min.js").read_text(encoding="utf-8"))
    page = page.replace("background: transparent;", "background: #3a6b4c;", 1)
    pg = tw(wd / "hud.html", page)
    js = """const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:960,height:540}});
await p.goto('file://'+%s); const out={};
for (const t of [0.3,1.7,3.5,1.7]){ await p.evaluate(t=>{window.__timelines['camcorder-hud'].seek(t,false);return 0;},t); await p.waitForTimeout(t===1.7&&out['1.7']?600:30);
 const r=await p.evaluate(()=>({c:document.querySelector('.ch-counter-value').textContent,o:document.querySelector('.ch-record-dot').style.opacity}));
 const k=out[String(t)]?String(t)+'b':String(t); out[k]=r; await p.screenshot({path:%s+'/hud_'+k+'.png'});}
await b.close(); console.log(JSON.stringify(out));})();""" % (json.dumps(str(pg)), json.dumps(str(wd)))
    r = node_js(wd, "hud", js)
    np = _np()
    red = lambda f: int(((f[..., 0] > 200) & (f[..., 1] < 90) & (f[..., 2] < 90)).sum())
    s03, s17 = load_png(wd / "hud_0.3.png"), load_png(wd / "hud_1.7.png")
    plain = np.zeros_like(s03)
    plain[:] = (0x3a, 0x6b, 0x4c)
    return [
        check("installed from the registry", json.loads(res.stdout.strip().splitlines()[-1])["ok"] and comp.exists(), True, True),
        check("counter follows timeline time (0.3 -> 00:00:00, 1.7 -> 00:00:01, 3.5 -> 00:00:03)",
              [r["0.3"]["c"], r["1.7"]["c"], r["3.5"]["c"]] == ["00:00:00", "00:00:01", "00:00:03"], [r["0.3"]["c"], r["1.7"]["c"], r["3.5"]["c"]], "0/1/3 s"),
        check("REC dot blinks every 0.55 s (1 at 0.3 s, 0.25 at 1.7 s, 1 at 3.5 s)", [r["0.3"]["o"], r["1.7"]["o"], r["3.5"]["o"]] == ["1", "0.25", "1"],
              [r["0.3"]["o"], r["1.7"]["o"], r["3.5"]["o"]], ["1", "0.25", "1"]),
        check("same timeline time after a wall-clock pause gives the same HUD", r["1.7"] == r["1.7b"], [r["1.7"], r["1.7b"]], "equal"),
        check("REC dot pixels bright at 0.3 s, dimmed at 1.7 s", red(s03) > 20 and red(s17) < red(s03) / 2, [red(s03), red(s17)], "bright -> dim"),
        check("negative control: footage without the HUD has no REC dot", red(plain) == 0, red(plain), 0),
    ], [wd / "hud_0.3.png", pg]


def synthwave_frame(t, W=320, H=180, flat=False):
    np = _np()
    hz, cx = 100, W / 2
    img = np.zeros((H, W, 3))
    ys = np.arange(H)[:, None]
    sky = np.clip((ys / hz), 0, 1)
    img[:hz] = np.concatenate([40 + 80 * sky[:hz], 10 + 20 * sky[:hz], 60 + 40 * sky[:hz]], axis=1)[:, None, :]
    yy, xx = np.mgrid[0:H, 0:W]
    sun = (xx - cx) ** 2 + (yy - 70) ** 2 < 38 ** 2
    gaps = (yy > 70) & ((yy - 70) % 8 < 1 + (yy - 70) // 10)
    grad = np.stack([255 + 0 * yy, 220 - (yy - 32) * 2.5, 60 + 0 * yy], -1)
    m = sun & ~gaps & (yy < hz)
    img[m] = grad[m]
    img[hz:] = (20, 0, 40)
    line = np.zeros((H, W))
    for k in range(-8, 9):
        for y in range(hz + 1, H):
            x = cx + k * 20 * (1 if flat else (y - hz) / 20.0)
            if 0 <= x < W:
                line[y, int(x)] = 1
    z0 = (t * 2) % 1
    for n in range(12):
        z = n + 1 - z0
        y = hz + int(round(80 / z))
        if hz < y < H:
            line[y, :] = 1
    from PIL import Image, ImageFilter
    glow = np.asarray(Image.fromarray((line * 255).astype("uint8")).filter(ImageFilter.GaussianBlur(2))).astype(float) / 255
    img = img + glow[..., None] * np.array([255, 40, 200]) * 0.8
    img[line > 0] = (255, 80, 230)
    return np.clip(img, 0, 255)


@card("RETRO-20")
def synthwave(task, wd):
    """Synthwave / retrowave: the `retrowave` style scaffolded with tools/kosif.py, and the look itself drawn per frame:
    a perspective grid scrolling toward the camera, a sun as a vertical gradient with horizontal scanline gaps,
    layered blur glow on the neon lines."""
    np = _np()
    sc = sh([sys.executable, REPO / "tools/kosif.py", "scaffold", "retrowave", wd / "film"], cwd=REPO, timeout=60, ok=None)
    frames = [synthwave_frame(i / 30) for i in range(30)]
    out = write_video(wd / "synthwave.mp4", frames, 30)
    f0, f1 = frames[0], frames[5]
    hz, cx = 100, 160

    def vanish(img):
        """Track each neon line from row 175 up to row 145 (skipping fully lit horizontal rows), fit x(y), extrapolate to the horizon."""
        lit = (img[..., 0] > 250) & (img[..., 1] < 100) & (img[..., 2] > 220)
        seeds = np.where(lit[175])[0]
        groups = [g for g in np.split(seeds, np.where(np.diff(seeds) > 1)[0] + 1) if len(g)]
        res = []
        for g in groups:
            x, pts = float(g.mean()), []
            for y in range(175, 144, -1):
                if lit[y].sum() > 100:
                    continue
                cand = np.where(lit[y])[0]
                if not len(cand):
                    break
                x = float(cand[np.argmin(np.abs(cand - x))])
                pts.append((y, x))
            if len(pts) > 10:
                k, c0 = np.polyfit([p_[0] for p_ in pts], [p_[1] for p_ in pts], 1)
                res.append(round(float(k * hz + c0), 2))
        return res

    v = vanish(f0)
    col = f0[:hz, cx]
    lit = [bool(f0[y, cx, 0] > 250 and f0[y, cx, 1] > 60) for y in range(72, 100)]
    gaps = sum(1 for a, b in zip(lit, lit[1:]) if a and not b)
    rows0 = [y for y in range(hz + 1, 179) if (f0[y, 5:40, 1] < 100).all() and (f0[y, 5:40, 0] > 250).all()]
    rows1 = [y for y in range(hz + 1, 179) if (frames[5][y, 5:40, 1] < 100).all() and (frames[5][y, 5:40, 0] > 250).all()]
    glow_px = int(((f0[hz + 5:, :, 2] > 90) & (f0[hz + 5:, :, 0] < 250)).sum())
    flat = synthwave_frame(0, flat=True)
    vf = vanish(flat)
    return [
        check("retrowave style scaffolded by tools/kosif.py", sc.returncode == 0 and any((wd / "film").iterdir()), sc.returncode, 0),
        check("grid lines converge on the vanishing point (160, 100) within 2 px", len(v) >= 2 and all(abs(x - cx) < 2 for x in v), v, 160),
        check("sun lower half cut by horizontal scanline gaps", gaps >= 3, gaps, ">= 3"),
        check("horizontal grid lines scroll toward the camera", rows0 != rows1 and max(rows1) >= max(rows0) - 1, [rows0[-3:], rows1[-3:]], "moved"),
        check("neon lines carry a blur glow halo", glow_px > 500, glow_px, "> 500 px"),
        check("negative control: an orthographic (flat) grid does not converge", not all(abs(x - cx) < 2 for x in vf), vf, "no vanishing point"),
    ], [out]


def glitch_frames(seconds=1.0, fps=30, bpm=128, seed=7):
    from PIL import Image, ImageDraw, ImageFont
    np = _np()
    rng = np.random.default_rng(seed)
    W, H = 320, 120
    font = ImageFont.truetype(FONT, 56) if FONT else ImageFont.load_default()
    base = Image.new("L", (W, H), 0)
    ImageDraw.Draw(base).text((40, 25), "GLITCH", font=font, fill=255)
    m = np.asarray(base) > 127
    step = 60.0 / bpm / 4 * 2
    trig = [int(round(k * step * fps)) for k in range(int(seconds / step) + 1)]
    frames, info = [], []
    for f in range(int(seconds * fps)):
        since = min([f - t for t in trig if f >= t] or [99])
        img = np.zeros((H, W, 3))
        if since < 3:
            dx = int(rng.integers(4, 13))
            nsl = int(rng.integers(6, 11))
            red, cyan = np.roll(m, -dx, axis=1), np.roll(m, dx, axis=1)
            img[red] = (255, 0, 0)
            img[cyan] = (0, 255, 255)
            img[m] = (255, 255, 255)
            edges = np.linspace(0, H, nsl + 1).astype(int)
            shifts = []
            for a, b in zip(edges, edges[1:]):
                s = int(rng.integers(-24, 25))
                img[a:b] = np.roll(img[a:b], s, axis=1)
                shifts.append(s)
            info.append({"frame": f, "dx": dx, "slices": nsl, "shifts": shifts})
        else:
            img[m] = (255, 255, 255)
        frames.append(img)
    return frames, info, trig, m


@card("RETRO-28")
def rgb_split_glitch(task, wd):
    """RGB-split glitch word on the beat: red / cyan / white copies offset 4-12 px, cut into 6-10 horizontal slices,
    retriggered every 1/8 note (234 ms at 128 BPM) for 3 frames; plus the ffmpeg whole-frame equivalent
    rgbashift=rh=-6:bh=6, measured on the produced pixels."""
    np = _np()
    frames, info, trig, m = glitch_frames()
    out = write_video(wd / "glitch.mp4", frames, 30)
    fr = read_video(out)
    red_only = lambda f: (f[..., 0] > 200) & (f[..., 1] < 60) & (f[..., 2] < 60)
    hit = [int(red_only(f).sum() > 0) for f in fr]
    starts = [i for i, h in enumerate(hit) if h and (i == 0 or not hit[i - 1])]
    k = info[0]
    f0 = fr[k["frame"]]
    edges = np.linspace(0, 120, k["slices"] + 1).astype(int)
    meas = []
    for a, b in zip(edges, edges[1:]):
        for y in range(a, b):
            wr = np.where((f0[y, :, 0] > 200) & (f0[y, :, 1] > 200))[0]
            rr = np.where(red_only(f0[y:y + 1])[0])[0]
            if len(wr) and len(rr):
                meas.append(int(wr.min() - rr.min()) % 320)
                break
    clean = save_png(frames[5] if not hit[5] else frames[6], wd / "clean.png")
    fx.ffmpeg("-i", clean, "-vf", "format=gbrp,rgbashift=rh=-6:bh=6,format=rgb24", wd / "rgbashift.png")
    sh_img = load_png(wd / "rgbashift.png")
    row = int(np.argmax(m.sum(axis=1)))
    wcol = np.where(m[row])[0].min()
    rcol = np.where(sh_img[row, :, 0] > 200)[0].min()
    return [
        check("glitch bursts start on every 1/8 note (frames 0, 7, 14, 21, 28)", starts == trig[:len(starts)] and starts == [0, 7, 14, 21, 28], starts, [0, 7, 14, 21, 28]),
        check("each burst lasts 3 frames (the last one is cut by the 1 s end)", sum(hit) == sum(min(3, len(fr) - s0) for s0 in starts), sum(hit), sum(min(3, len(fr) - s0) for s0 in starts)),
        check("measured red-copy offset equals the drawn 4-12 px offset", meas and all(v == k["dx"] for v in meas) and 4 <= k["dx"] <= 12, [meas[:4], k["dx"]], k["dx"]),
        check("6-10 slices with shifts of at most 24 px", 6 <= k["slices"] <= 10 and max(abs(s) for s in k["shifts"]) <= 24, [k["slices"], k["shifts"]], "6-10, <= 24"),
        check("ffmpeg rgbashift moves the red channel 6 px left", wcol - rcol == 6, int(wcol - rcol), 6),
        check("negative control: an off-beat frame has no colour split", hit[4] == 0 and red_only(load_png(clean)).sum() == 0, [hit[4], int(red_only(load_png(clean)).sum())], 0),
    ], [out, wd / "rgbashift.png"]


# ================================================================================ TOOL: the repo's own engines

def coverage_ok(cov):
    return bool(cov.get("complete")) and cov.get("records_scanned") == cov.get("records_on_disk") and cov.get("unclassified_count") == 0 \
        and cov.get("broken_count") == 0 and len(cov.get("catalog_sha256", "")) == 64


@card("TOOL-124")
def usip_engine(task, wd):
    """USIP engine: `skill_intelligence.py brief` scans 100% of the catalog with a SHA-256 coverage receipt, checks the
    derived indexes are fresh, and drafts the analysis, ranked groups and plans A/B/C with one recommendation."""
    out = wd / "brief.json"
    done = sh([sys.executable, SPS / "skill_intelligence.py", "brief", "مونتاج ريلز على الإيقاع بترجمة عربية", "--out", out], cwd=REPO, timeout=60)
    b = json.loads(out.read_text(encoding="utf-8"))
    cov = b["coverage"]
    tamper = dict(cov, records_scanned=cov["records_scanned"] - 1)
    md = tw(wd / "brief.md", done.stdout)
    return [
        check("coverage receipt: every record scanned and classified", coverage_ok(cov),
              {k: cov.get(k) for k in ("records_on_disk", "records_scanned", "unclassified_count", "broken_count")}, "complete"),
        check("derived indexes are fresh", all(v.get("ok") for v in b["freshness"].values()), {k: v.get("ok") for k, v in b["freshness"].items()}, "all ok"),
        check("plans A, B and C drafted with one recommendation among them", sorted(b["plans"]) == ["A", "B", "C"] and b["recommended"] in b["plans"],
              [sorted(b["plans"]), b["recommended"]], "A/B/C"),
        check("request analysis and ranked powers present", bool(b["analysis"]) and len(b["top_powers"]) > 0, len(b["top_powers"]), "> 0"),
        check("negative control: a receipt with one record missing fails the coverage gate", not coverage_ok(tamper), False, False),
    ], [out, md]


@card("TOOL-125")
def fusionforge_recipe(task, wd):
    """FusionForge v2 (records under a private root in the work folder): propose a recipe from the brief, validate,
    choose a plan, trace every node of it, record `tested`; the `verified` gate refuses without QA proof."""
    root = wd / "ff"
    env = dict(os.environ, KOSIF_FUSIONFORGE_ROOT=str(root))
    brief = wd / "brief.json"
    sh([sys.executable, SPS / "skill_intelligence.py", "brief", "مونتاج ريلز بترجمة عربية", "--out", brief], cwd=REPO, timeout=60)
    ff = [sys.executable, SPS / "fusionforge.py"]
    sh(ff + ["propose", "مونتاج ريلز بترجمة عربية", "--project", "w3demo", "--from-brief", brief], cwd=wd, env=env, timeout=60)
    rec_file = [p for p in (root / "w3demo/recipes").glob("FUSE-*.json") if not p.name.endswith(".brief.json")][0]
    rid = rec_file.stem
    val = sh(ff + ["validate", "--project", "w3demo", "--id", rid], cwd=wd, env=env, timeout=60, ok=None)
    sh(ff + ["choose", "--project", "w3demo", "--id", rid, "--plan", "A", "--why", "simplest path"], cwd=wd, env=env, timeout=60)
    rec = json.loads(rec_file.read_text(encoding="utf-8"))
    nodes = {n["id"]: n for n in rec["nodes"]}
    ev = tw(wd / "evidence.txt", "runner fixture evidence\n")
    cov = json.loads(brief.read_text(encoding="utf-8"))["coverage"]
    for k, nid in enumerate(rec["plans"]["A"]["nodes"]):
        n = nodes[nid]
        if k == 0:   # the understand stage really ran here: the brief was produced and its receipt read back
            args = ["--action", "skill_intelligence brief written", "--result", "passed", "--tool", "tool:skill-intelligence",
                    "--output", str(brief), "--observed", "coverage complete=%s, %d records" % (cov["complete"], cov["records_scanned"]), "--evidence", str(brief)]
        else:
            args = ["--action", "not run by this check", "--result", "skipped", "--tool", n["executor"]["ref"], "--observed", "skipped", "--evidence", str(ev)]
        sh(ff + ["trace", "--project", "w3demo", "--id", rid, "--stage", n["stage"], "--node", nid] + args, cwd=wd, env=env, timeout=60)
    sh(ff + ["record", "--project", "w3demo", "--id", rid, "--status", "tested", "--evidence", ev], cwd=wd, env=env, timeout=60)
    ver = sh(ff + ["record", "--project", "w3demo", "--id", rid, "--status", "verified", "--evidence", ev], cwd=wd, env=env, timeout=60, ok=None)
    rec2 = json.loads(rec_file.read_text(encoding="utf-8"))
    typed = all(n["inputs"] and n["outputs"] and n.get("executor") and n.get("acceptance") for n in rec["nodes"])
    return [
        check("recipe proposed under the private root", rec_file.exists() and str(rec_file).startswith(str(wd)), rec_file.name, "FUSE-*.json"),
        check("validate is clean", val.returncode == 0 and "clean" in val.stdout, val.stdout.strip()[-60:], "clean"),
        check("nodes are typed (inputs/outputs kinds, executor, acceptance)", typed, len(rec["nodes"]), "all typed"),
        check("plan A chosen and every node traced", (rec2.get("plan_choice") or {}).get("plan") == "A" and len(rec2["traces"]) == len(rec["plans"]["A"]["nodes"]),
              [rec2.get("plan_choice"), len(rec2["traces"])], "A, all nodes"),
        check("status recorded as tested", rec2["status"] == "tested", rec2["status"], "tested"),
        check("negative control: verified without --qa-pass is refused", ver.returncode != 0 and rec2["status"] != "verified", ver.returncode, "!= 0"),
    ], [rec_file, brief]


@card("TOOL-51")
def cinema_c_studio(task, wd):
    """Cinema C V34 Studio (POSIX sh, a-Shell): `--studio FILE` offline on a local clip, driven through its menu:
    4 = Reels 9:16 with blurred fill, then 7 = two-pass loudness -14 LUFS (video stream copied)."""
    script = REPO / "tools/a-shell/Cinema_C_V34_Studio_iPhone.sh"
    clip = wd / "clip.mp4"
    fx.ffmpeg("-f", "lavfi", "-i", "testsrc2=s=320x180:r=30:d=1.5", "-f", "lavfi", "-i", "sine=f=440:d=1.5,volume=0.1", "-shortest",
              "-pix_fmt", "yuv420p", "-c:v", "libx264", "-c:a", "aac", clip)
    env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HOME": str(wd), "CINEMA_DOWNLOAD_DIR": str(wd / "dl")}
    h0 = sha(clip)
    done = sh(["sh", script, "--studio", clip], cwd=wd, env=env, input="4\n1\nn\nn\n7\nn\nn\n0\n", timeout=60)
    tw(wd / "session.log", done.stdout + done.stderr)
    st = wd / "dl/Studio"
    reels = st / "clip - REELS.mp4"
    loud = st / "clip - LOUD.mp4"
    vs = vstream(reels)
    fr = fx.frames(reels, size=(54, 96))[10]
    band, centre = fr[2:20].mean(), fr[40:56].std()
    L, L0 = lufs(loud), lufs(clip)
    vcodec_copy = vstream(loud)["codec_name"] == vstream(clip)["codec_name"] and vstream(loud)["width"] == 320
    return [
        check("Reels output is 1080x1920 H.264", (vs["width"], vs["height"], vs["codec_name"]) == (1080, 1920, "h264"), [vs["width"], vs["height"], vs["codec_name"]], "1080x1920 h264"),
        check("blurred fill above the picture (not black bars)", band > 20, round(float(band), 1), "> 20"),
        check("the sharp source sits in the middle band", centre > 30, round(float(centre), 1), "> 30"),
        check("loudness tool reaches -14 LUFS with the video untouched", L is not None and abs(L + 14) <= 1 and vcodec_copy, [L, vcodec_copy], "-14, copied"),
        check("original file untouched", sha(clip) == h0, sha(clip)[:12], h0[:12]),
        check("negative control: the source is 16:9 and far from -14 LUFS", vstream(clip)["width"] > vstream(clip)["height"] and abs((L0 or 0) + 14) > 3, [L0], "far"),
    ], [reels, loud]


@card("TOOL-83")
def html_canvas_starter(task, wd):
    """HTML Canvas film starter: scaffolded with tools/kosif.py (kinetic-arabic, --starter html-canvas), every frame is a
    pure function of time behind window.__kosif.seek(t); tools/render_html.cjs seeks it and renders stills at 1080x1920."""
    sh([sys.executable, REPO / "tools/kosif.py", "scaffold", "kinetic-arabic", wd / "film", "--starter", "html-canvas"], cwd=REPO, timeout=60)
    idx = wd / "film/html-canvas/index.html"
    src = idx.read_text(encoding="utf-8")
    sh([NODE, REPO / "tools/render_html.cjs", "--in", idx, "--out", wd / "film.mp4", "--stills", "1,11", "--stills-dir", wd / "stills", "--offline"],
       cwd=REPO, env=node_env(), timeout=60)
    np = _np()
    shots = {t: load_png(wd / "stills" / ("still_%s.000.png" % t)) for t in (1, 11)}
    from PIL import Image
    sz = Image.open(wd / "stills/still_11.000.png").size
    d111 = float(np.abs(shots[1] - shots[11]).mean())
    def painted(img):
        u, n = np.unique(img[::4, ::4].reshape(-1, 3), axis=0, return_counts=True)
        bg = u[np.argmax(n)]
        return float((np.abs(img - bg).max(axis=-1) > 30).mean())
    paint = [painted(s) for s in shots.values()]
    blank = np.zeros_like(shots[1])
    blank[:] = shots[1][0, 0]
    return [
        check("starter copied with index.html, timeline.js, words.js", all((wd / "film/html-canvas" / f).exists() for f in ("index.html", "timeline.js", "words.js")), True, True),
        check("page exposes window.__kosif.seek", "__kosif" in src and "seek" in src, True, True),
        check("stills are 1080x1920", sz == (1080, 1920), sz, [1080, 1920]),
        check("scenes change over time (1 s and 11 s differ)", d111 > 5, d111, "> 5"),
        check("each still is painted (> 2 % of pixels away from the background)", min(paint) > 0.02, paint, "> 0.02"),
        check("negative control: a blank canvas of the background colour is not painted", painted(blank) <= 0.02, painted(blank), "<= 0.02"),
    ], [wd / "stills/stills_grid.png"]


@card("TOOL-85")
def mimic_rebuilder(task, wd):
    """KOSIF Mimic analyse: mm_analyze.analyze() reads a reference video into spec.json (shots, transitions with their
    kind, the look per shot), measured on a 3-shot fixture with hard cuts at 1 s and 2 s; a one-shot video gives none."""
    ref = three_shot_clip(wd / "ref.mp4", size="180x320", sec=1.0)
    fx.ffmpeg("-f", "lavfi", "-i", "testsrc2=s=180x320:r=30:d=3", "-pix_fmt", "yuv420p", "-c:v", "libx264", wd / "one.mp4")
    code = ("import sys,json; sys.path.insert(0, %r); import mm_analyze; mm_analyze.analyze(sys.argv[1], sys.argv[2], skip_text=True)" % str(SPS / "mimic"))
    sh([sys.executable, "-c", code, ref, wd / "work"], cwd=wd, env=py_env(wd), timeout=60)
    sh([sys.executable, "-c", code, wd / "one.mp4", wd / "work1"], cwd=wd, env=py_env(wd), timeout=60)
    spec = json.loads((wd / "work/spec.json").read_text(encoding="utf-8"))
    one = json.loads((wd / "work1/spec.json").read_text(encoding="utf-8"))
    shots = [(s["start"], s["end"]) for s in spec["shots"]]
    tr = [(t["type"], t["ts"]) for t in spec["transitions"]]
    return [
        check("three shots split at frames 30 and 60", shots == [(0, 30), (30, 60), (60, 90)], shots, [[0, 30], [30, 60], [60, 90]]),
        check("two transitions classified as cuts at 1 s and 2 s", tr == [("cut", 30), ("cut", 60)], tr, [["cut", 30], ["cut", 60]]),
        check("each shot carries its measured look (Lab + palette)", all("lab" in s and s.get("palette") for s in spec["shots"]), len(spec["shots"]), 3),
        check("analysis report written", (wd / "work/analysis.md").stat().st_size > 0, (wd / "work/analysis.md").stat().st_size, "> 0"),
        check("negative control: a one-shot video has no transitions", len(one["shots"]) == 1 and one["transitions"] == [], [len(one["shots"]), len(one["transitions"])], [1, 0]),
    ], [wd / "work/spec.json", wd / "work/analysis.md"]
