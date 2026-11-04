"""skills part 4: catalog SKILL.md procedures turned into real, measured programs.

Each runner does the skill's core procedure on a fixture made in the work folder and checks known answers on what
it produced, plus a negative control (the same check on the untreated input / the naive path fails).
Engines: python stdlib + numpy/PIL/PyYAML, sqlite3, ruff, black, flake8, cargo/clippy, go, bun, git.
SaaS packs (Ideogram, Linear, Notion, Shopify, ...) run their governance/review procedure on synthetic local records;
no network, no vendor account, no credential is used. Skills whose substance is a dialogue with a person, an external
advisor model, a paid generation, or an engine that is not installed are listed in GAPS with the reason.
"""
import base64
import hashlib
import hmac
import json
import os
import re
import shutil
import sqlite3
import subprocess
import textwrap
from pathlib import Path

from _harness import card, check

GAPS: dict = {}

SK = "skill:kosif-superpowers/vendor/kosif-atlas/skills/"


def K(rel):
    return SK + rel


def jw(path, obj):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(obj, ensure_ascii=False, indent=1), encoding="utf-8")
    return Path(path)


def tw(path, text):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(textwrap.dedent(text).lstrip("\n"), encoding="utf-8")
    return p


def sh(cmd, cwd=None, env=None, timeout=60):
    """Run a command, return (returncode, stdout+stderr). Never raises on non-zero exit."""
    e = dict(os.environ)
    e.update(env or {})
    p = subprocess.run([str(c) for c in cmd], cwd=cwd, env=e, capture_output=True, text=True, timeout=timeout,
                       stdin=subprocess.DEVNULL)
    return p.returncode, (p.stdout or "") + (p.stderr or "")


# ───────────────────────────── Ideogram data lifecycle ─────────────────────────────

def _bbox_to_px(box, w, h):
    """Ideogram V4 describe boxes: [y_min, x_min, y_max, x_max] normalised to 0..1000 -> pixel (x0, y0, x1, y1)."""
    y0, x0, y1, x1 = box
    return (round(x0 * w / 1000), round(y0 * h / 1000), round(x1 * w / 1000), round(y1 * h / 1000))


def _lifecycle(db, rec, governed, naive=False):
    """Trace one synthetic record through every store, then run deletion. naive=True is the ungoverned pipeline."""
    c = db.cursor()
    tenant, prompt = rec["tenant"], rec["prompt"]
    gen_id = hashlib.sha256(("gen:" + rec["id"]).encode()).hexdigest()[:16]
    c.execute("insert into uploads values (?,?,?)", (rec["id"], tenant, "source.png"))
    c.execute("insert into generations values (?,?,?,?,?)",
              (gen_id, tenant, rec["id"], "passed", rec["vendor_url"] if naive else None))
    c.execute("insert into outputs values (?,?,?)",
              (tenant + "/" + hashlib.sha256(rec["png"]).hexdigest()[:24], tenant, rec["id"]))
    c.execute("insert into logs values (?,?)", (rec["id"], ("prompt=" + prompt) if naive else ("gen=" + gen_id + " safety=passed")))
    c.execute("insert into queue values (?,?)", (rec["id"], "done"))
    c.execute("insert into cache values (?,?)", (rec["id"], "thumb"))
    if rec.get("legal_hold"):
        c.execute("insert into legal_holds values (?,?)", (gen_id, "case-17"))
    db.commit()
    # deletion request for the source record
    stores = ["uploads"] if naive else governed
    for t in stores:
        col = "record" if t not in ("uploads",) else "id"
        if t == "generations":
            held = c.execute("select 1 from legal_holds where gen_id=?", (gen_id,)).fetchone()
            if held:
                continue
            c.execute("delete from generations where record=?", (rec["id"],))
            continue
        c.execute("delete from %s where %s=?" % (t, col), (rec["id"],))
    db.commit()
    return gen_id


@card(K("1869-ideogram-pack/5949-ideogram-data-handling"))
def ideogram_data_handling(task, wd):
    from PIL import Image, ImageDraw
    import numpy as np
    wd = Path(wd)
    # 1) normalised describe bbox -> pixels, proven on a rendered image
    W, H = 640, 480
    box = [250, 100, 750, 400]  # y_min, x_min, y_max, x_max on 0..1000
    im = Image.new("RGB", (W, H), (20, 20, 20))
    ImageDraw.Draw(im).rectangle((64, 120, 255, 359), fill=(220, 30, 30))
    src = wd / "describe_source.png"
    im.save(src)
    px = _bbox_to_px(box, W, H)
    crop = np.asarray(Image.open(src).crop(px)).reshape(-1, 3).mean(0)
    swapped = (round(box[0] * W / 1000), round(box[1] * H / 1000), round(box[2] * W / 1000), round(box[3] * H / 1000))
    crop_bad = np.asarray(Image.open(src).crop(swapped)).reshape(-1, 3).mean(0)
    # 2) lifecycle with governed deletion across every store
    schema = ["create table uploads(id, tenant, name)", "create table generations(gen_id, tenant, record, safety, vendor_url)",
              "create table outputs(key, tenant, record)", "create table logs(record, line)",
              "create table queue(record, state)", "create table cache(record, item)", "create table legal_holds(gen_id, reason)"]
    governed = ["uploads", "generations", "outputs", "logs", "queue", "cache"]
    res = {}
    for mode in ("governed", "naive"):
        db = sqlite3.connect(str(wd / ("lifecycle_%s.db" % mode)))
        for s in schema:
            db.execute(s)
        recs = [{"id": "rec-1", "tenant": "t-a", "prompt": "SECRET product launch poster", "png": src.read_bytes(),
                 "vendor_url": "https://ideogram.example/ephemeral/abc?exp=3600"},
                {"id": "rec-2", "tenant": "t-a", "prompt": "held asset", "png": b"x2", "legal_hold": True,
                 "vendor_url": "https://ideogram.example/ephemeral/def?exp=3600"}]
        gens = [_lifecycle(db, r, governed, naive=(mode == "naive")) for r in recs]
        left = {t: db.execute("select count(*) from %s where %s='rec-1'" % (t, "id" if t == "uploads" else "record")).fetchone()[0]
                for t in governed}
        leaked_prompt = db.execute("select count(*) from logs where line like '%prompt=%'").fetchone()[0]
        urls = db.execute("select count(*) from generations where vendor_url is not null").fetchone()[0]
        held_kept = db.execute("select count(*) from generations where gen_id=?", (gens[1],)).fetchone()[0]
        keys = [r[0] for r in db.execute("select key from outputs")]
        res[mode] = {"remaining_rec1": left, "prompt_in_logs": leaked_prompt, "vendor_urls_stored": urls,
                     "legal_hold_kept": held_kept, "output_keys": keys}
        db.close()
    g, n = res["governed"], res["naive"]
    report = jw(wd / "data_map.json", {"bbox_norm": box, "bbox_px": px, "lifecycle": res,
                                       "classes": ["prompt", "source_upload", "generation_id", "safety_result",
                                                   "vendor_url", "output", "log", "queue", "cache", "legal_hold"]})
    checks = [
        check("bbox [y0,x0,y1,x1]/1000 -> pixel box", px == (64, 120, 256, 360), px, (64, 120, 256, 360)),
        check("crop of converted box is the red object", crop[0] > 200 and crop[1] < 50, crop.tolist(), "R>200,G<50"),
        check("negative control: axis-swapped box misses the object", not (crop_bad[0] > 200 and crop_bad[1] < 50),
              crop_bad.tolist(), "not red"),
        check("governed deletion: rec-1 gone from every store", sum(g["remaining_rec1"].values()) == 0, g["remaining_rec1"], 0),
        check("legal-hold record retained", g["legal_hold_kept"] == 1, g["legal_hold_kept"], 1),
        check("content-free telemetry and no durable vendor URL", g["prompt_in_logs"] == 0 and g["vendor_urls_stored"] == 0,
              [g["prompt_in_logs"], g["vendor_urls_stored"]], [0, 0]),
        check("outputs stored under opaque tenant-scoped keys", all(re.fullmatch(r"t-a/[0-9a-f]{24}", k) for k in g["output_keys"]),
              g["output_keys"], "t-a/<sha24>"),
        check("negative control: naive pipeline leaves data, prompt and URL",
              sum(n["remaining_rec1"].values()) > 0 and n["prompt_in_logs"] > 0 and n["vendor_urls_stored"] > 0,
              n, "residue present"),
    ]
    return checks, [report, src]


# ───────────────────────────── Linear multi-environment isolation ─────────────────────────────

def _env_audit(envs):
    f = []
    seen = {}
    for name, e in envs.items():
        for ref in [e["client_secret_ref"], e["webhook_secret_ref"]]:
            if ref in seen and seen[ref] != name:
                f.append(("shared-secret", name, ref))
            seen.setdefault(ref, name)
        for cb in e["callbacks"]:
            if "*" in cb:
                f.append(("wildcard-callback", name, cb))
            if not cb.startswith("https://") and not cb.startswith("http://localhost"):
                f.append(("non-https-callback", name, cb))
        if not e["webhook_url"].startswith("https://"):
            f.append(("non-https-webhook", name, e["webhook_url"]))
        if name != "production":
            for j in e.get("ci_jobs", []):
                if any("prod" in s.lower() for s in j["secrets"]):
                    f.append(("non-prod-job-resolves-prod-secret", name, j["name"]))
        if e.get("team_access") == "all-teams" and name == "production":
            f.append(("broad-team-access", name, "all-teams"))
    return f


@card(K("1878-linear-pack/6189-linear-multi-env-setup"))
def linear_multi_env(task, wd):
    wd = Path(wd)
    good = {
        "development": {"oauth_app": "app-dev", "client_secret_ref": "vault:linear/dev/client", "webhook_secret_ref": "vault:linear/dev/wh",
                        "callbacks": ["http://localhost:3000/oauth/callback"], "webhook_url": "https://dev.example.com/linear/wh",
                        "ci_jobs": [{"name": "pr-tests", "secrets": ["LINEAR_DEV_KEY"]}], "team_access": "team:sandbox"},
        "staging": {"oauth_app": "app-stg", "client_secret_ref": "vault:linear/stg/client", "webhook_secret_ref": "vault:linear/stg/wh",
                    "callbacks": ["https://stg.example.com/oauth/callback"], "webhook_url": "https://stg.example.com/linear/wh",
                    "ci_jobs": [{"name": "deploy-stg", "secrets": ["LINEAR_STG_KEY"]}], "team_access": "team:qa"},
        "production": {"oauth_app": "app-prod", "client_secret_ref": "vault:linear/prod/client", "webhook_secret_ref": "vault:linear/prod/wh",
                       "callbacks": ["https://app.example.com/oauth/callback"], "webhook_url": "https://app.example.com/linear/wh",
                       "ci_jobs": [{"name": "deploy-prod", "secrets": ["LINEAR_PROD_KEY"]}], "team_access": "team:eng"}}
    bad = json.loads(json.dumps(good))
    bad["staging"]["webhook_secret_ref"] = "vault:linear/prod/wh"
    bad["staging"]["callbacks"] = ["https://*.example.com/oauth/callback"]
    bad["development"]["ci_jobs"][0]["secrets"].append("LINEAR_PROD_KEY")
    bad["production"]["team_access"] = "all-teams"
    fg, fb = _env_audit(good), _env_audit(bad)
    # misrouting scenario: a staging-signed webhook must not verify with the production secret
    secrets = {"stg": b"stg-signing-secret", "prod": b"prod-signing-secret"}  # synthetic test values only
    body = json.dumps({"type": "Issue", "action": "create", "webhookId": "wh-1"}).encode()
    sig = hmac.new(secrets["stg"], body, hashlib.sha256).hexdigest()
    ok_stg = hmac.compare_digest(sig, hmac.new(secrets["stg"], body, hashlib.sha256).hexdigest())
    ok_prod = hmac.compare_digest(sig, hmac.new(secrets["prod"], body, hashlib.sha256).hexdigest())
    handoff = "credential-boundary=%s; callback=%s; prod-access=%s" % (
        "separate" if not any(x[0] == "shared-secret" for x in fg) else "shared",
        "exact" if not any(x[0] == "wildcard-callback" for x in fg) else "wildcard",
        "none" if not any(x[0] == "non-prod-job-resolves-prod-secret" for x in fg) else "leak")
    rep = jw(wd / "env_isolation.json", {"good_findings": fg, "bad_findings": fb, "handoff": handoff,
                                         "misroute": {"staging_secret_verifies": ok_stg, "prod_secret_verifies": ok_prod}})
    kinds = sorted({x[0] for x in fb})
    blob = rep.read_text()
    return [
        check("isolated manifest has no findings", fg == [], fg, []),
        check("handoff line matches the skill's expected handoff",
              handoff == "credential-boundary=separate; callback=exact; prod-access=none", handoff),
        check("negative control: shared secret, wildcard, prod leak, broad access all caught",
              kinds == ["broad-team-access", "non-prod-job-resolves-prod-secret", "shared-secret", "wildcard-callback"], kinds),
        check("misrouted webhook fails verification under the other env's secret", ok_stg and not ok_prod, [ok_stg, ok_prod], [True, False]),
        check("report carries secret references only, never values", "signing-secret" not in blob, "no values"),
    ], [rep]


# ───────────────────────────── Mistral governed reference architecture ─────────────────────────────

SURFACES = {"chat": ("chat.completions", "stable", "stateless"), "embeddings": ("embeddings", "stable", "stateless"),
            "classify": ("classifiers", "stable", "stateless"), "ocr": ("files+ocr", "stable", "stateful"),
            "bulk": ("batch", "stable", "stateful"), "agent": ("agents/conversations", "preview", "stateful")}


class _Gateway:
    def __init__(self, budgets, idempotent=True):
        self.budgets, self.idem, self.ledger, self.calls, self.rejected = dict(budgets), idempotent, {}, [], []
        self.provider_files = set()

    def submit(self, job):
        if job["tenant"] != job["auth_tenant"]:
            self.rejected.append((job["key"], "cross-tenant"))
            return "rejected"
        if self.budgets.get(job["tenant"], 0) < job["cost"]:
            self.rejected.append((job["key"], "budget"))
            return "rejected"
        if self.idem and job["key"] in self.ledger:
            return "duplicate"
        surface = SURFACES[job["workload"]][0]
        self.calls.append((job["key"], surface))
        self.budgets[job["tenant"]] -= job["cost"]
        if surface in ("files+ocr", "batch"):
            self.provider_files.add("file-" + job["key"])
        self.ledger[job["key"]] = surface
        return "accepted"


@card(K("1885-mistral-pack/6344-mistral-reference-architecture"))
def mistral_reference_architecture(task, wd):
    wd = Path(wd)
    jobs = [{"key": "j1", "tenant": "a", "auth_tenant": "a", "workload": "chat", "cost": 1},
            {"key": "j2", "tenant": "a", "auth_tenant": "a", "workload": "bulk", "cost": 5},
            {"key": "j2", "tenant": "a", "auth_tenant": "a", "workload": "bulk", "cost": 5},   # timeout retry
            {"key": "j3", "tenant": "b", "auth_tenant": "a", "workload": "chat", "cost": 1},   # cross-tenant
            {"key": "j4", "tenant": "a", "auth_tenant": "a", "workload": "ocr", "cost": 2},
            {"key": "j4", "tenant": "a", "auth_tenant": "a", "workload": "ocr", "cost": 2},    # duplicate delivery
            {"key": "j5", "tenant": "b", "auth_tenant": "b", "workload": "agent", "cost": 50}]  # over budget
    gw, naive = _Gateway({"a": 20, "b": 10}), _Gateway({"a": 20, "b": 10}, idempotent=False)
    out = [gw.submit(j) for j in jobs]
    for j in jobs:
        naive.submit(j)
    app_state = {"file-j2"}  # app tracked only the batch file: the OCR upload is unmanaged until reconciled
    orphans = sorted(gw.provider_files - app_state)
    mapping = {w: {"surface": s, "stability": st, "state": sta, "behind_versioned_adapter": st == "preview"}
               for w, (s, st, sta) in SURFACES.items()}
    keys = [k for k, _ in gw.calls]
    rep = jw(wd / "architecture.json", {"workload_map": mapping, "outcomes": out, "calls": gw.calls,
                                        "rejected": gw.rejected, "orphans_to_reconcile": orphans,
                                        "remaining_budget": gw.budgets,
                                        "paths_walked": ["happy", "timeout-retry", "duplicate", "cross-tenant", "budget"]})
    return [
        check("each idempotency key executed once", sorted(keys) == ["j1", "j2", "j4"], keys, ["j1", "j2", "j4"]),
        check("cross-tenant and over-budget jobs stopped at the gateway",
              sorted(gw.rejected) == [("j3", "cross-tenant"), ("j5", "budget")], gw.rejected),
        check("bulk routed to batch, preview agent marked behind adapter",
              mapping["bulk"]["surface"] == "batch" and mapping["agent"]["behind_versioned_adapter"], mapping["agent"]),
        check("reconciliation finds the untracked OCR upload", orphans == ["file-j4"], orphans, ["file-j4"]),
        check("budget ledger arithmetic", gw.budgets == {"a": 12, "b": 10}, gw.budgets, {"a": 12, "b": 10}),
        check("negative control: without idempotency duplicates execute twice", len(naive.calls) == 5, len(naive.calls), 5),
    ], [rep]


# ───────────────────────────── Notion integration pitfalls ─────────────────────────────

NOTION_RULES = [
    ("database-id-to-data-source-query", re.compile(r"dataSources\.query\(\s*\{\s*data_source_id:\s*\w*database\w*", re.I)),
    ("single-page-query", re.compile(r"(?s)(dataSources\.query|search)\((?:(?!has_more|next_cursor).)*?\)\s*;(?:(?!has_more|next_cursor).)*$")),
    ("write-retry-without-idempotency", re.compile(r"retry\(\s*\(\)\s*=>\s*notion\.pages\.create")),
    ("webhook-trusts-order", re.compile(r"webhook[\s\S]{0,200}apply\(event\.data\)(?![\s\S]{0,120}retrieve)")),
    ("stale-api-version", re.compile(r"notionVersion:\s*['\"]2022-")),
]


def _notion_audit(src):
    return sorted(name for name, rx in NOTION_RULES if rx.search(src))


@card(K("1887-notion-pack/6390-notion-known-pitfalls"))
def notion_known_pitfalls(task, wd):
    wd = Path(wd)
    bad = tw(wd / "bad_integration.js", """
        const notion = new Client({ auth: process.env.NOTION_TOKEN, notionVersion: '2022-06-28' });
        export async function list(databaseId) {
          const r = await notion.dataSources.query({ data_source_id: databaseId });
          return r.results;
        }
        export async function add(p) { return retry(() => notion.pages.create(p), 3); }
        app.post('/webhook', (req) => { const event = req.body; apply(event.data); });
        """)
    good = tw(wd / "good_integration.js", """
        const notion = new Client({ auth: process.env.NOTION_TOKEN, notionVersion: '2025-09-03' });
        export async function list(dataSourceId) {
          const out = []; let cursor;
          do { const r = await notion.dataSources.query({ data_source_id: dataSourceId, start_cursor: cursor });
               out.push(...r.results); cursor = r.has_more ? r.next_cursor : undefined; } while (cursor);
          return out;
        }
        export async function add(p, key) { const prior = await findByKey(key); return prior || notion.pages.create(p); }
        app.post('/webhook', async (req) => { const event = req.body; const cur = await notion.pages.retrieve({page_id: event.entity.id}); reconcile(cur); });
        """)
    fb, fg = _notion_audit(bad.read_text()), _notion_audit(good.read_text())
    # pagination path exercised on a mock: 250 rows, page_size 100
    rows = list(range(250))

    def page(cursor=0):
        nxt = cursor + 100
        return {"results": rows[cursor:nxt], "has_more": nxt < len(rows), "next_cursor": nxt if nxt < len(rows) else None}
    single = len(page()["results"])
    got, cur = [], 0
    while True:
        r = page(cur)
        got += r["results"]
        if not r["has_more"]:
            break
        cur = r["next_cursor"]
    rep = jw(wd / "pitfall_inventory.json", {"bad": fb, "good": fg, "pagination": {"single_call": single, "paginated": len(got)}})
    return [
        check("all five planted pitfalls found in the bad integration", len(fb) == 5, fb),
        check("corrected integration is clean", fg == [], fg, []),
        check("paginated read returns every row", len(got) == 250 and got == rows, len(got), 250),
        check("negative control: single query page is incomplete", single == 100, single, 100),
    ], [rep, bad]


# ───────────────────────────── OpenEvidence quality audit ─────────────────────────────

PHI = [re.compile(r"\bMRN[:# ]*\d{6,}\b", re.I), re.compile(r"\b\d{3}-\d{3}-\d{4}\b"), re.compile(r"\bDOB[: ]+\d{4}-\d{2}-\d{2}\b", re.I)]


def _kappa(a, b):
    labels = sorted(set(a) | set(b))
    n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n
    pe = sum((a.count(l) / n) * (b.count(l) / n) for l in labels)
    return (po - pe) / (1 - pe)


@card(K("1890-openevidence-pack/6464-openevidence-observability"))
def openevidence_observability(task, wd):
    import random
    wd = Path(wd)
    rnd = random.Random(7)
    samples = []
    for i in range(25):
        traced = i % 5 != 0            # 20 of 25 cite traceable evidence
        unsupported = 1 if i in (3, 11) else 0
        override = i in (4, 9, 17)
        text = "Answer %d with citation [%d]" % (i, i)
        if i == 21:
            text += " patient MRN: 00123456 call 555-123-4567"   # PHI slipped into a sample
        samples.append({"id": "s%02d" % i, "traced": traced, "unsupported_claims": unsupported, "override": override, "text": text})
    r1 = [("ok" if s["traced"] and not s["unsupported_claims"] else "issue") for s in samples]
    r2 = list(r1)
    for i in rnd.sample(range(25), 3):
        r2[i] = "issue" if r2[i] == "ok" else "ok"
    quarantined = [s["id"] for s in samples if any(p.search(s["text"]) for p in PHI)]
    export = [dict(s, text=None) for s in samples if s["id"] not in quarantined]
    k = _kappa(r1, r2)
    po = sum(x == y for x, y in zip(r1, r2)) / 25
    metrics = {"traceability": sum(s["traced"] for s in samples) / 25, "unsupported_claims": sum(s["unsupported_claims"] for s in samples),
               "overrides": sum(s["override"] for s in samples), "kappa": k, "agreement": po, "incidents": len(quarantined),
               "actions": 3}
    handoff = "traceability=measured; overrides=recorded; incidents=%d; actions=%d" % (metrics["incidents"], metrics["actions"])
    p = jw(wd / "quality_audit.json", {"metrics": metrics, "handoff": handoff, "export": export, "quarantined": quarantined,
                                       "limitations": "local 25-sample review; no patient-outcome or vendor-wide inference"})
    naive_blob = json.dumps(samples)
    blob = p.read_text()
    return [
        check("traceability 20/25 and 3 overrides measured", metrics["traceability"] == 0.8 and metrics["overrides"] == 3,
              [metrics["traceability"], metrics["overrides"]], [0.8, 3]),
        check("inter-reviewer agreement 22/25 with Cohen kappa < agreement", abs(po - 0.88) < 1e-9 and k < po, [po, k]),
        check("PHI sample quarantined, handoff matches", quarantined == ["s21"] and handoff.endswith("incidents=1; actions=3"),
              [quarantined, handoff]),
        check("governed export carries no PHI", not any(px.search(blob) for px in PHI), "clean"),
        check("negative control: unscreened export contains PHI", any(px.search(naive_blob) for px in PHI), "PHI present"),
    ], [p]


# ───────────────────────────── PostHog enterprise RBAC ─────────────────────────────

READONLY_LABEL = re.compile(r"readonly|read-only|bi-")


def _rbac_audit(org):
    f = []
    for k in org["keys"]:
        if "*" in k["scopes"]:
            f.append(("wildcard-scope", k["label"]))
        if READONLY_LABEL.search(k["label"]) and any(not s.endswith(":read") for s in k["scopes"]):
            f.append(("write-scope-on-readonly-key", k["label"]))
        if k["label"] == "flag-service" and any(not s.startswith("feature_flag:") for s in k["scopes"]):
            f.append(("flag-key-overbroad", k["label"]))
    for m in org["members"]:
        if m["email"].split("@")[1] not in org["verified_domains"]:
            f.append(("member-outside-verified-domain", m["email"]))
        prod = m["projects"].get("production")
        if prod is not None and m["team"] == "product" and prod > 1:
            f.append(("prod-admin-for-product", m["email"]))
        if m["org_level"] >= 8 and m["team"] not in ("platform",):
            f.append(("org-admin-outside-platform", m["email"]))
    if not org["enforce_sso"]:
        f.append(("sso-not-enforced", org["name"]))
    return sorted(f)


def _effective(member, project):
    return max(member["org_level"] if member["org_level"] >= 8 else 0, member["projects"].get(project, 0))


@card(K("1894-posthog-pack/6533-posthog-enterprise-rbac"))
def posthog_rbac(task, wd):
    wd = Path(wd)
    good = {"name": "acme", "enforce_sso": True, "verified_domains": ["acme.io"],
            "keys": [{"label": "bi-dashboard-readonly", "scopes": ["insight:read", "dashboard:read", "query:read"]},
                     {"label": "flag-service", "scopes": ["feature_flag:read", "feature_flag:write"]},
                     {"label": "data-export-readonly", "scopes": ["event:read", "query:read"]}],
            "members": [{"email": "ops@acme.io", "team": "platform", "org_level": 8, "projects": {"production": 8, "staging": 8}},
                        {"email": "eng@acme.io", "team": "engineering", "org_level": 1, "projects": {"production": 1, "staging": 8}},
                        {"email": "pm@acme.io", "team": "product", "org_level": 1, "projects": {"production": 1, "staging": 1}}]}
    bad = json.loads(json.dumps(good))
    bad["enforce_sso"] = False
    bad["keys"][0]["scopes"].append("insight:write")
    bad["keys"][1]["scopes"].append("person:write")
    bad["members"][2]["projects"]["production"] = 8
    bad["members"].append({"email": "temp@gmail.com", "team": "engineering", "org_level": 1, "projects": {"staging": 1}})
    fg, fb = _rbac_audit(good), _rbac_audit(bad)
    eff = {m["email"]: {p: _effective(m, p) for p in ("production", "staging")} for m in good["members"]}
    rep = jw(wd / "rbac_matrix.json", {"effective_levels": eff, "good_findings": fg, "bad_findings": fb})
    return [
        check("least-privilege org passes", fg == [], fg, []),
        check("effective levels: engineering admin in staging, member in prod",
              eff["eng@acme.io"] == {"production": 1, "staging": 8} and eff["ops@acme.io"]["production"] == 8, eff),
        check("negative control: every planted violation detected", [x[0] for x in fb] == sorted(
            ["flag-key-overbroad", "member-outside-verified-domain", "prod-admin-for-product", "sso-not-enforced",
             "write-scope-on-readonly-key"]), fb),
    ], [rep]


# ───────────────────────────── Procore endpoint contract cutover ─────────────────────────────

def _shape(obj, prefix=""):
    out = {}
    if isinstance(obj, dict):
        for k, v in obj.items():
            out.update(_shape(v, prefix + k + "."))
    elif isinstance(obj, list):
        out.update(_shape(obj[0], prefix + "[]."))
    else:
        out[prefix.rstrip(".")] = type(obj).__name__
    return out


def _state_hash(rows, fields):
    canon = sorted(json.dumps({f: r.get(f) for f in fields}, sort_keys=True) for r in rows)
    return hashlib.sha256("\n".join(canon).encode()).hexdigest()


@card(K("1895-procore-pack/6571-procore-upgrade-migration"))
def procore_migration(task, wd):
    wd = Path(wd)
    old = [{"id": 11, "name": "RFI 1", "status": "open", "assignee_id": 7, "due": "2026-11-10"},
           {"id": 12, "name": "RFI 2", "status": "closed", "assignee_id": 8, "due": "2026-11-12"}]
    new = {"data": [{"id": 11, "title": "RFI 1", "status": {"name": "open"}, "assignees": [{"id": 7}], "due_date": "2026-11-10",
                     "created_by": {"id": 1}},
                    {"id": 12, "title": "RFI 2", "status": {"name": "closed"}, "assignees": [{"id": 8}], "due_date": "2026-11-12",
                     "created_by": {"id": 1}}], "meta": {"next": None}}
    so, sn = _shape(old[0]), _shape(new["data"][0])
    diff = {"removed": sorted(set(so) - set(sn)), "added": sorted(set(sn) - set(so))}

    def adapter(resp):
        return [{"id": r["id"], "name": r["title"], "status": r["status"]["name"], "assignee_id": r["assignees"][0]["id"],
                 "due": r["due_date"]} for r in resp["data"]]
    fields = ["id", "name", "status", "assignee_id", "due"]
    h_old, h_new = _state_hash(old, fields), _state_hash(adapter(new), fields)
    h_raw = _state_hash(new["data"], fields)
    repo = wd / "repo"
    tw(repo / "jobs/monthly.py", "r = client.get('/rest/v1.0/projects/{pid}/rfis')\n")
    tw(repo / "svc/sync.py", "r = client.get('/rest/v1.1/projects/{pid}/rfis')\n")
    tw(repo / "svc/other.py", "r = client.get('/rest/v1.0/projects/{pid}/submittals')\n")
    rx = re.compile(r"/rest/v1\.0/projects/\{pid\}/rfis\b")
    callers = sorted(str(p.relative_to(repo)) for p in repo.rglob("*.py") if rx.search(p.read_text()))
    traffic = {"2026-10": 120, "2026-11": 0}
    removal_ok = traffic["2026-11"] == 0 and callers == []
    rep = jw(wd / "cutover_receipt.json", {"contract_diff": diff, "callers": callers, "dual_read": {"old": h_old, "adapted": h_new},
                                          "traffic": traffic, "removal_allowed": removal_ok})
    return [
        check("contract diff names renamed/nested fields",
              diff == {"removed": ["assignee_id", "due", "name", "status"],
                       "added": ["assignees.[].id", "created_by.id", "due_date", "status.name", "title"]}, diff),
        check("dual read: adapted new contract hashes equal to old", h_old == h_new, h_new[:12], h_old[:12]),
        check("negative control: unadapted new payload differs", h_raw != h_old, h_raw[:12]),
        check("caller inventory finds the remaining legacy caller", callers == ["jobs/monthly.py"], callers),
        check("removal blocked while a legacy caller remains", removal_ok is False, removal_ok, False),
    ], [rep]


# ───────────────────────────── Shopify advanced troubleshooting ─────────────────────────────

def _gql_parse(q):
    """Tiny GraphQL selection parser: returns [(name, args, children)] for the top-level selection set."""
    toks = re.findall(r"[A-Za-z_][A-Za-z0-9_]*|\d+|[{}():,]|\"[^\"]*\"", q)
    pos = [0]

    def sel():
        out = []
        assert toks[pos[0]] == "{"
        pos[0] += 1
        while toks[pos[0]] != "}":
            name = toks[pos[0]]
            pos[0] += 1
            args = {}
            if toks[pos[0]] == "(":
                pos[0] += 1
                while toks[pos[0]] != ")":
                    k = toks[pos[0]]
                    v = toks[pos[0] + 2]
                    args[k] = v
                    pos[0] += 3
                    if toks[pos[0]] == ",":
                        pos[0] += 1
                pos[0] += 1
            kids = sel() if toks[pos[0]] == "{" else None
            out.append((name, args, kids))
        pos[0] += 1
        return out
    while toks[pos[0]] != "{":
        pos[0] += 1
    return sel()


def _gql_cost(fields):
    """Shopify requested-cost rules: scalar 0, object 1, connection 2 + first x (cost of one node)."""
    total = 0
    for name, args, kids in fields:
        if kids is None:
            continue
        if "first" in args:
            node = [k for k in kids if k[0] in ("edges", "nodes")]
            inner = 0
            for n in node:
                sub = n[2]
                if n[0] == "edges":
                    sub = [s for s in sub if s[0] == "node"][0][2]
                inner += 1 + _gql_cost(sub)
            total += 2 + int(args["first"]) * inner
        elif name in ("edges", "nodes", "node"):
            total += _gql_cost(kids)
        else:
            total += 1 + _gql_cost(kids)
    return total


@card(K("1905-shopify-pack/6771-shopify-advanced-troubleshooting"))
def shopify_troubleshooting(task, wd):
    wd = Path(wd)
    q = """query { products(first: 50) { edges { node { id title
            variants(first: 20) { edges { node { id price metafields(first: 5) { edges { node { key value } } } } } } } } } }"""
    cost = _gql_cost(_gql_parse(q))
    # by hand: metafields = 2 + 5*1 = 7 ; variant node = 1 + 7 = 8 ; variants = 2 + 20*8 = 162 ;
    #          product node = 1 + 162 = 163 ; products = 2 + 50*163 = 8152
    q2 = q.replace("first: 50", "first: 5").replace("first: 20", "first: 10").replace("metafields(first: 5) { edges { node { key value } } }", "")
    cost2 = _gql_cost(_gql_parse(q2))
    # intermittent-failure debug log: failures follow point exhaustion
    log, avail = [], 1000.0
    for i in range(100):
        avail = min(1000.0, avail + 50.0)    # restore 50 points per tick
        qc = 400 if i % 7 == 0 else 60
        ok = avail >= qc
        log.append({"i": i, "queryCost": qc, "availablePoints": avail, "statusCode": 200 if ok else 429,
                    "requestId": "req-%04d" % i, "durationMs": 120 + (900 if not ok else 0)})
        if ok:
            avail -= qc
    fails = [e for e in log if e["statusCode"] != 200]
    exhausted = all(e["availablePoints"] < e["queryCost"] for e in fails)
    heavy = {e["queryCost"] for e in fails}
    p = jw(wd / "cost_breakdown.json", {"requestedQueryCost": cost, "after_reduction": cost2, "max_single_query": 1000,
                                        "failures": len(fails), "failure_query_costs": sorted(heavy),
                                        "request_ids": [e["requestId"] for e in fails][:10]})
    jw(wd / "debug_log.json", log)
    return [
        check("requested cost multiplies first through nested connections", cost == 8152, cost, 8152),
        check("reduced page sizes bring cost under the 1000 cap", cost2 < 1000, cost2, "<1000"),
        check("negative control: original query exceeds the cap", cost > 1000, cost, ">1000"),
        check("every failure happens with availablePoints < queryCost", bool(fails) and exhausted, len(fails)),
        check("pattern isolates the heavy operation", heavy == {400}, sorted(heavy), [400]),
    ], [p]


# ───────────────────────────── Shopify reliability patterns ─────────────────────────────

class _Breaker:
    """opossum-equivalent: errorThresholdPercentage 50, volumeThreshold 5, resetTimeout 30 s, errorFilter 5xx/timeouts."""

    def __init__(self, threshold=50, volume=5, reset=30.0):
        self.threshold, self.volume, self.reset = threshold, volume, reset
        self.state, self.opened_at, self.window = "closed", None, []

    def counts(self, err):
        return err is None or err.get("code", 0) >= 500 or err.get("errno") in ("ECONNRESET", "ETIMEDOUT")

    def fire(self, now, backend, cache):
        if self.state == "open":
            if now - self.opened_at >= self.reset:
                self.state = "half-open"
            else:
                return ("cache", cache)
        err = backend(now)
        failed = err is not None and self.counts(err)
        if self.state == "half-open":
            if failed:
                self.state, self.opened_at = "open", now
                return ("cache", cache)
            self.state, self.window = "closed", []
            return ("live", "fresh")
        if err is not None and not failed:
            return ("error", err)   # 422 etc: surfaced to caller, not counted as circuit failure
        self.window.append(failed)
        self.window = self.window[-10:]
        if len(self.window) >= self.volume and 100.0 * sum(self.window) / len(self.window) >= self.threshold:
            self.state, self.opened_at = "open", now
        return ("cache", cache) if failed else ("live", "fresh")


def _retry_delay_ms(attempt, retry_after=None, throttle=None):
    wait_points = ((100 - throttle["currentlyAvailable"]) / throttle["restoreRate"]) * 1000 if throttle else 0
    return float(retry_after) * 1000 if retry_after else max(wait_points, 1000 * 2 ** attempt)


@card(K("1905-shopify-pack/6802-shopify-reliability-patterns"))
def shopify_reliability(task, wd):
    wd = Path(wd)
    hits = []

    def backend(now):
        hits.append(now)
        if 10 <= now < 60:
            return {"code": 503}
        return None
    b, served = _Breaker(), []
    for t in range(0, 100, 2):
        served.append((t, b.fire(float(t), backend, "cached")[0], b.state))
    outage_hits_breaker = len([h for h in hits if 10 <= h < 60])
    nb_hits = len([t for t in range(0, 100, 2) if 10 <= t < 60])
    b2 = _Breaker()
    for t in range(10):
        b2.fire(float(t), lambda now: {"code": 422}, "c")
    # idempotent webhook processing with 7-day TTL; a failing handler releases the key for Shopify's retry
    store, processed = {}, []

    def handle(wid, now, fail=False):
        k = "shopify:webhook:" + wid
        if k in store and store[k][1] > now:
            return "duplicate"
        store[k] = ("processing", now + 7 * 86400)
        if fail:
            del store[k]
            return "error"
        processed.append(wid)
        store[k] = ("completed", now + 7 * 86400)
        return "processed"
    deliveries = [("w1", 0, False), ("w1", 60, False), ("w2", 0, True), ("w2", 120, False), ("w2", 300, False), ("w1", 8 * 86400, False)]
    results = [handle(*d) for d in deliveries]
    secret, body = b"shpss_test_secret", b'{"id":1001,"topic":"orders/create"}'
    sig = base64.b64encode(hmac.new(secret, body, hashlib.sha256).digest()).decode()
    ok = hmac.compare_digest(sig, base64.b64encode(hmac.new(secret, body, hashlib.sha256).digest()).decode())
    tampered = hmac.compare_digest(sig, base64.b64encode(hmac.new(secret, body + b" ", hashlib.sha256).digest()).decode())
    d1 = _retry_delay_ms(0, throttle={"currentlyAvailable": 20, "restoreRate": 50})
    d2 = _retry_delay_ms(1, retry_after="2.0")
    d3 = _retry_delay_ms(3, throttle={"currentlyAvailable": 90, "restoreRate": 50})
    p = jw(wd / "reliability_trace.json", {"breaker": served, "backend_hits_during_outage": outage_hits_breaker,
                                           "webhook_results": results, "delays_ms": [d1, d2, d3]})
    states = [s for _, _, s in served]
    return [
        check("circuit opens during the 5xx outage and recovers through half-open",
              "open" in states and states[-1] == "closed", states[::5]),
        check("breaker shields the backend during the outage", outage_hits_breaker < nb_hits / 2, outage_hits_breaker, nb_hits),
        check("negative control: 422 validation errors never open the circuit", b2.state == "closed", b2.state, "closed"),
        check("webhooks: duplicate skipped, failed delivery re-processed, TTL expiry re-admits",
              results == ["processed", "duplicate", "error", "processed", "duplicate", "processed"], results),
        check("HMAC verifies original and rejects tampered body", ok and not tampered, [ok, tampered], [True, False]),
        check("retry delays: points 1600 ms, Retry-After 2000 ms, backoff floor 8000 ms", [d1, d2, d3] == [1600.0, 2000.0, 8000.0],
              [d1, d2, d3]),
    ], [p]


# ───────────────────────────── Windsurf / Devin Desktop pitfalls ─────────────────────────────

def _windsurf_audit(root):
    root = Path(root)
    f = []
    rules = root / ".devin/rules/project.md"
    if rules.exists() and len(rules.read_text()) > 12000:
        f.append(("high", "rules-over-limit", str(rules.relative_to(root)), len(rules.read_text())))
    for p in list(root.glob(".devin/**/*.md")) + list(root.glob(".windsurf/**/*.md")):
        if re.search(r"\b(sk-[A-Za-z0-9]{16,}|ghp_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16})", p.read_text()):
            f.append(("critical", "secret-in-ai-context", str(p.relative_to(root)), "redacted"))
    st = root / ".windsurf/settings.json"
    if st.exists():
        s = json.loads(st.read_text())
        deny = " ".join(s.get("cascadeCommandsDenyList", []))
        if s.get("turboMode") and not all(x in deny for x in ("rm", "push --force", "sudo")):
            f.append(("critical", "turbo-without-deny-list", ".windsurf/settings.json", s.get("cascadeCommandsDenyList", [])))
        conf = [e for e in s.get("extensions", []) if re.search(r"copilot|tabnine|cody", e, re.I)]
        if conf:
            f.append(("medium", "conflicting-ai-extensions", ".windsurf/settings.json", conf))
    rc, out = sh(["git", "status", "--porcelain"], cwd=root)
    dirty = [l for l in out.splitlines() if l.strip()] if rc == 0 else []
    if dirty:
        f.append(("high", "no-checkpoint-before-cascade", "git status", len(dirty)))
    n = sum(1 for _ in root.rglob("*") if ".git" not in _.parts)
    if n > 5000:
        f.append(("medium", "workspace-too-large", ".", n))
    order = {"critical": 0, "high": 1, "medium": 2}
    return sorted(f, key=lambda x: (order[x[0]], x[1]))


@card(K("1915-windsurf-pack/7023-windsurf-known-pitfalls"))
def windsurf_pitfalls(task, wd):
    wd = Path(wd)
    env = {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@x", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@x"}
    out = {}
    for name in ("clean", "risky"):
        r = wd / name
        tw(r / "src/app.py", "print('hi')\n")
        tw(r / ".devin/rules/project.md", "# Rules\nUse src/ paths.\n" if name == "clean" else
           "# Rules\n" + ("Always follow the payment style guide. " * 400) + "\nkey: sk-abcdefghijklmnop1234\n")
        jw(r / ".windsurf/settings.json", {"turboMode": True, "cascadeCommandsDenyList": ["rm", "sudo", "git push --force"],
                                           "extensions": ["ms-python.python"]} if name == "clean" else
           {"turboMode": True, "cascadeCommandsDenyList": [], "extensions": ["GitHub.copilot", "ms-python.python"]})
        sh(["git", "init", "-q"], cwd=r)
        sh(["git", "add", "-A"], cwd=r, env=env)
        sh(["git", "commit", "-qm", "checkpoint: before cascade"], cwd=r, env=env)
        if name == "risky":
            tw(r / "src/wip.py", "x = 1\n")
        out[name] = _windsurf_audit(r)
    p = jw(wd / "windsurf_audit.json", out)
    kinds = [x[1] for x in out["risky"]]
    return [
        check("clean workspace has no pitfalls", out["clean"] == [], out["clean"], []),
        check("negative control: every planted pitfall found, prioritised",
              kinds == ["secret-in-ai-context", "turbo-without-deny-list", "no-checkpoint-before-cascade", "rules-over-limit",
                        "conflicting-ai-extensions"], kinds),
        check("audit table never contains the secret value", "sk-abcdefghijklmnop1234" not in p.read_text(), "redacted"),
    ], [p]


# ───────────────────────────── agent-debug-fixer (TDD minimal fix gate) ─────────────────────────────

def _changed_lines(a, b):
    import difflib
    return sum(1 for l in difflib.unified_diff(a.splitlines(), b.splitlines(), lineterm="", n=0)
               if l[:1] in "+-" and not l.startswith(("+++", "---")))


@card(K("2-agent-workflow-system/2-agent-debug-fixer"))
def agent_debug_fixer(task, wd):
    import sys
    wd = Path(wd)
    proj = wd / "proj"
    buggy = "def mean(xs):\n    return sum(xs) // len(xs)\n\n\ndef total(xs):\n    return sum(xs)\n"
    tw(proj / "calc.py", buggy)
    rollback = hashlib.sha256(buggy.encode()).hexdigest()
    py = sys.executable

    def run_tests():
        rc, out = sh([py, "-m", "unittest", "-q"], cwd=proj)
        return rc
    tw(proj / "test_calc.py", "import unittest, calc\nclass T(unittest.TestCase):\n    def test_mean(self):\n"
                              "        self.assertEqual(calc.mean([1, 2]), 1.5)\n")
    before = run_tests()                                                # must fail: reproduces the bug
    minimal = buggy.replace("sum(xs) // len(xs)", "sum(xs) / len(xs)")
    refactor = ("import statistics\n\n\ndef mean(xs):\n    if not xs:\n        raise ValueError('empty')\n"
                "    return statistics.fmean(xs)\n\n\ndef total(xs):\n    return sum(xs)\n\n\ndef median(xs):\n"
                "    return statistics.median(xs)\n")
    gate = {}
    for name, cand in (("minimal", minimal), ("refactor", refactor)):
        (proj / "calc.py").write_text(cand)
        passes = run_tests() == 0
        n_changed = _changed_lines(buggy, cand)
        new_defs = set(re.findall(r"^def (\w+)", cand, re.M)) - set(re.findall(r"^def (\w+)", buggy, re.M))
        gate[name] = {"tests_pass": passes, "changed_lines": n_changed, "new_functions": sorted(new_defs),
                      "accepted": passes and n_changed <= 2 and not new_defs}
    (proj / "calc.py").write_text(minimal)
    after = run_tests()
    events_ok = ["write_test", "test_fails", "fix", "test_passes"]
    events_bad = ["fix", "write_test", "test_passes"]

    def tdd_order(ev):
        return ev.index("write_test") < ev.index("fix") and "test_fails" in ev and ev.index("test_fails") < ev.index("fix")
    snap = tw(wd / "STATE_SNAPSHOT.md", "current_phase: 执行·调试 -> 审计\nrollback_point: sha256:%s\n" % rollback)
    rep = jw(wd / "fix_report.json", {"reproduced": before != 0, "gate": gate, "after": after, "rollback_point": rollback,
                                      "evidence_chain": events_ok, "remaining_risk": ["mean([]) raises ZeroDivisionError (unchanged)"]})
    return [
        check("new test reproduces the bug before the fix", before != 0, before, "non-zero"),
        check("minimal one-line fix accepted and suite green", gate["minimal"]["accepted"] and after == 0, gate["minimal"]),
        check("negative control: refactor that also passes is rejected by the minimal-fix gate",
              gate["refactor"]["tests_pass"] and not gate["refactor"]["accepted"], gate["refactor"]),
        check("TDD order enforced: code-before-test sequence rejected", tdd_order(events_ok) and not tdd_order(events_bad)),
        check("rollback point recorded", rollback in snap.read_text(), rollback[:12]),
    ], [rep, snap]


# ───────────────────────────── agent-drift-auditor ─────────────────────────────

def _drift_audit(root, today):
    import datetime as dt
    root = Path(root)
    f = []
    q = (root / "TASK_QUEUE.md").read_text()
    active = re.findall(r"^- \[~\] (.+?)(?: \(last_active: (\d{4}-\d{2}-\d{2})\))?$", q, re.M)
    if len(active) > 1:
        f.append(("warning", "multiple-active-tasks", [a[0] for a in active]))
    for name, last in active:
        if last and (today - dt.date.fromisoformat(last)).days > 3:
            f.append(("info", "task-stale-over-3-days", name))
    dec = (root / "DECISIONS.md").read_text()
    for d, when in re.findall(r"^- (.+?) \(decided_at: (\d{4}-\d{2}-\d{2})\)$", dec, re.M):
        if (today - dt.date.fromisoformat(when)).days > 7 and active:
            f.append(("info", "decision-may-be-stale", d))
    conv = re.search(r"naming: (\w+)", dec)
    code = "\n".join(p.read_text() for p in sorted((root / "src").glob("*.py")))
    if conv and conv.group(1) == "snake_case":
        bad = sorted(set(re.findall(r"^def ([a-z]+[A-Z]\w*)", code, re.M)))
        if bad:
            f.append(("warning", "naming-inconsistent", bad))
    if re.search(r"(api_key|password|secret)\s*=\s*['\"][^'\"]{6,}['\"]", code, re.I):
        f.append(("critical", "hardcoded-secret", "src"))
    lines = [l.strip() for l in code.splitlines() if l.strip()]
    blocks = {}
    for i in range(len(lines) - 3):
        blocks.setdefault(tuple(lines[i:i + 4]), []).append(i)
    if any(len(v) > 1 for v in blocks.values()):
        f.append(("warning", "duplicate-code-over-3-lines", "src"))
    scope = re.findall(r"^- (.+)$", (root / "PROJECT.md").read_text().split("## Out of scope")[1], re.M)
    for s in scope:
        if s.lower() in q.lower():
            f.append(("critical", "scope-creep", s))
    sev = [x[0] for x in f]
    level = 0 if not f else (3 if sev.count("critical") >= 2 else 2 if "critical" in sev else 1)
    advice = {0: "继续", 1: "继续", 2: "暂停", 3: "决策闸门"}[level]
    return sorted(f), level, advice


@card(K("2-agent-workflow-system/3-agent-drift-auditor"))
def agent_drift_auditor(task, wd):
    import datetime as dt
    wd = Path(wd)
    today = dt.date(2026, 11, 3)
    reps = {}
    for name in ("aligned", "drifted"):
        r = wd / name
        tw(r / "PROJECT.md", "# Project\nCLI to sum CSV columns.\n## Out of scope\n- web dashboard\n")
        tw(r / "DECISIONS.md", "- naming: snake_case (decided_at: 2026-11-01)\n")
        tw(r / "STATE_SNAPSHOT.md", "current_phase: 审计\n")
        if name == "aligned":
            tw(r / "TASK_QUEUE.md", "- [~] parse csv (last_active: 2026-11-02)\n- [ ] sum column\n")
            tw(r / "src/a.py", "def read_rows(p):\n    return open(p).read().split()\n")
        else:
            tw(r / "TASK_QUEUE.md", "- [~] parse csv (last_active: 2026-10-20)\n- [~] build web dashboard (last_active: 2026-11-02)\n")
            dup = "    a = 1\n    b = 2\n    c = a + b\n    return c\n"
            tw(r / "src/a.py", "def readRows(p):\n" + dup + "\ndef other():\n" + dup + "\nAPI_KEY = 'abcdef123456'\n")
        before = sha_tree(r)
        reps[name] = _drift_audit(r, today) + (before == sha_tree(r),)
    p = jw(wd / "drift_report.json", {k: {"findings": v[0], "level": v[1], "advice": v[2], "read_only": v[3]} for k, v in reps.items()})
    kinds = [x[1] for x in reps["drifted"][0]]
    return [
        check("aligned project: no drift, continue", reps["aligned"][0] == [] and reps["aligned"][2] == "继续", reps["aligned"][:3]),
        check("negative control: every planted drift detected", sorted(kinds) == sorted(
            ["duplicate-code-over-3-lines", "hardcoded-secret", "multiple-active-tasks", "naming-inconsistent", "scope-creep",
             "task-stale-over-3-days"]), kinds),
        check("two critical findings escalate to level 3 decision gate", reps["drifted"][1] == 3 and reps["drifted"][2] == "决策闸门",
              reps["drifted"][1:3]),
        check("auditor is read-only (tree hash unchanged)", reps["aligned"][3] and reps["drifted"][3]),
    ], [p]


def sha_tree(root):
    h = hashlib.sha256()
    for p in sorted(Path(root).rglob("*")):
        if p.is_file():
            h.update(str(p.relative_to(root)).encode() + p.read_bytes())
    return h.hexdigest()


# ───────────────────────────── container optimisation (Go / Node / Python) ─────────────────────────────

def _elf_info(path):
    """Parse an ELF64 file: PT_INTERP present (dynamic) and section names (symtab / debug info)."""
    import struct
    b = Path(path).read_bytes()
    assert b[:4] == b"\x7fELF" and b[4] == 2
    e_phoff, e_shoff = struct.unpack_from("<QQ", b, 0x20)
    e_phentsize, e_phnum, e_shentsize, e_shnum, e_shstrndx = struct.unpack_from("<HHHHH", b, 0x36)
    interp = any(struct.unpack_from("<I", b, e_phoff + i * e_phentsize)[0] == 3 for i in range(e_phnum))
    names = []
    if e_shnum:
        so = e_shoff + e_shstrndx * e_shentsize
        str_off = struct.unpack_from("<Q", b, so + 0x18)[0]
        for i in range(e_shnum):
            n = struct.unpack_from("<I", b, e_shoff + i * e_shentsize)[0]
            names.append(b[str_off + n:b.index(b"\0", str_off + n)].decode())
    return {"dynamic": interp, "sections": names, "size": len(b)}


def _dockerfile_stages(text):
    stages, cur = [], None
    for raw in text.splitlines():
        line = raw.strip()
        m = re.match(r"FROM\s+(\S+)(?:\s+AS\s+(\S+))?", line, re.I)
        if m:
            cur = {"image": m.group(1), "name": m.group(2), "lines": []}
            stages.append(cur)
        elif cur is not None and line and not line.startswith("#"):
            cur["lines"].append(line)
    args = dict(re.findall(r"^ARG\s+(\w+)=(\S+)", text, re.M))
    return stages, args


@card(K("2146-container-plugin/7718-go-containers"))
def go_containers(task, wd):
    """Static, stripped, trimpath Go binary for a scratch image. Uses the standard Go build cache (GOCACHE)."""
    wd = Path(wd)
    src = wd / "app"
    tw(src / "go.mod", "module example.com/app\n\ngo 1.21\n")
    tw(src / "main.go", 'package main\n\nimport "fmt"\n\nfunc main() { fmt.Println("ok") }\n')
    env = {"CGO_ENABLED": "0", "GOFLAGS": "-mod=mod", "GO111MODULE": "on", "GOTOOLCHAIN": "local"}
    rc1, o1 = sh(["go", "build", "-o", wd / "main-default", "."], cwd=src, env=env, timeout=120)
    rc2, o2 = sh(["go", "build", "-trimpath", "-ldflags=-s -w", "-o", wd / "main-opt", "."], cwd=src, env=env, timeout=120)
    if rc1 or rc2:
        raise RuntimeError(o1[-300:] + o2[-300:])
    d, o = _elf_info(wd / "main-default"), _elf_info(wd / "main-opt")
    run = sh([wd / "main-opt"])[1].strip()
    path_in_default = str(src).encode() in (wd / "main-default").read_bytes()
    path_in_opt = str(src).encode() in (wd / "main-opt").read_bytes()
    dockerfile = tw(wd / "Dockerfile", """
        FROM golang:1.23-alpine AS builder
        WORKDIR /app
        COPY go.mod ./
        RUN go mod download
        COPY . .
        RUN CGO_ENABLED=0 go build -trimpath -ldflags="-s -w" -o /main .
        FROM scratch
        COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
        COPY --from=builder /main /main
        USER 65534:65534
        ENTRYPOINT ["/main"]
        """)
    stages, _ = _dockerfile_stages(dockerfile.read_text())
    rep = jw(wd / "go_image_report.json", {"default": {k: d[k] for k in ("size", "dynamic")}, "optimized": {k: o[k] for k in ("size", "dynamic")},
                                           "reduction_pct": round(100 * (1 - o["size"] / d["size"]), 1),
                                           "runtime_stage": stages[-1]["image"]})
    return [
        check("CGO_ENABLED=0 binary is static (no PT_INTERP), runs on scratch", not o["dynamic"] and run == "ok", [o["dynamic"], run]),
        check("-s -w strips the symbol table", ".symtab" not in o["sections"], [s for s in o["sections"] if "sym" in s]),
        check("negative control: default build keeps .symtab and is larger", ".symtab" in d["sections"] and d["size"] > o["size"] * 1.2,
              [d["size"], o["size"]]),
        check("-trimpath removes the build directory from the binary", path_in_default and not path_in_opt,
              [path_in_default, path_in_opt], [True, False]),
        check("final stage is scratch with CA certs and non-root user",
              stages[-1]["image"] == "scratch" and any("ca-certificates" in l for l in stages[-1]["lines"])
              and any(l.startswith("USER") for l in stages[-1]["lines"]), stages[-1]["lines"]),
    ], [rep, wd / "main-opt"]


def _node_dockerfile_audit(text):
    stages, _ = _dockerfile_stages(text)
    f = []
    final = stages[-1]
    if len(stages) < 2:
        f.append("single-stage")
    if not re.search(r"alpine|slim|distroless", final["image"]):
        f.append("full-base-runtime")
    if not any(l.startswith("USER") and "root" not in l for l in final["lines"]):
        f.append("runs-as-root")
    if not re.search(r"npm ci\b.*(--omit=dev|--only=production)|pnpm install.*--prod|yarn.*--production", text):
        f.append("dev-deps-in-runtime")
    if re.search(r"npm install(?!\s+-g)", text):
        f.append("npm-install-not-ci")
    if not any(l.startswith("HEALTHCHECK") for l in final["lines"]):
        f.append("no-healthcheck")
    return sorted(f)


@card(K("2146-container-plugin/7719-nodejs-containers"))
def nodejs_containers(task, wd):
    wd = Path(wd)
    for n, v in (("runtime-lib", "1.0.0"), ("dev-tool", "2.0.0")):
        jw(wd / "pkgs" / n / "package.json", {"name": n, "version": v, "main": "index.js"})
        (wd / "pkgs" / n / "index.js").write_text("module.exports = %r;\n" % n)
        (wd / "pkgs" / n / "blob.bin").write_bytes(os.urandom(200000 if n == "dev-tool" else 1000))
    app = wd / "app"
    jw(app / "package.json", {"name": "svc", "version": "1.0.0", "private": True,
                              "dependencies": {"runtime-lib": "file:../pkgs/runtime-lib"},
                              "devDependencies": {"dev-tool": "file:../pkgs/dev-tool"}})
    (app / "server.js").write_text("console.log(require('runtime-lib'))\n")
    env = {"npm_config_cache": str(wd / ".npm"), "npm_config_offline": "true", "npm_config_audit": "false",
           "npm_config_fund": "false", "npm_config_install_links": "true"}
    rc, out = sh(["npm", "install", "--no-audit"], cwd=app, env=env, timeout=60)  # lockfile for npm ci
    if rc:
        raise RuntimeError(out[-400:])
    full = sorted(os.listdir(app / "node_modules"))
    full_size = sum(p.stat().st_size for p in (app / "node_modules").rglob("*") if p.is_file())
    shutil.rmtree(app / "node_modules")
    rc, out = sh(["npm", "ci", "--omit=dev"], cwd=app, env=env, timeout=60)
    if rc:
        raise RuntimeError(out[-400:])
    prod = sorted(p for p in os.listdir(app / "node_modules") if not p.startswith("."))
    prod_size = sum(p.stat().st_size for p in (app / "node_modules").rglob("*") if p.is_file())
    runs = sh(["node", "server.js"], cwd=app)[1].strip()
    good = textwrap.dedent("""
        FROM node:20-alpine AS deps
        WORKDIR /app
        COPY package*.json ./
        RUN npm ci --omit=dev
        FROM node:20-alpine AS build
        WORKDIR /app
        COPY package*.json ./
        RUN npm ci
        COPY . .
        RUN npm run build
        FROM node:20-alpine
        WORKDIR /app
        RUN addgroup -g 1001 -S nodejs && adduser -u 1001 -S nodejs -G nodejs
        COPY --from=deps --chown=nodejs:nodejs /app/node_modules ./node_modules
        COPY --from=build --chown=nodejs:nodejs /app/dist ./dist
        USER nodejs
        HEALTHCHECK --interval=30s CMD node healthcheck.js || exit 1
        CMD ["node", "dist/server.js"]
        """)
    bad = "FROM node:20\nWORKDIR /app\nCOPY . .\nRUN npm install\nCMD [\"node\", \"server.js\"]\n"
    tw(wd / "Dockerfile", good)
    fg, fb = _node_dockerfile_audit(good), _node_dockerfile_audit(bad)
    rep = jw(wd / "node_image_report.json", {"all_deps": full, "prod_deps": prod, "bytes_all": full_size, "bytes_prod": prod_size,
                                             "dockerfile_findings": fg, "naive_findings": fb})
    return [
        check("npm ci --omit=dev installs only runtime deps", prod == ["runtime-lib"], prod, ["runtime-lib"]),
        check("negative control: full install carries the dev tool", "dev-tool" in full and full_size > prod_size * 10,
              [full, full_size, prod_size]),
        check("production tree still runs the app", runs == "runtime-lib", runs),
        check("optimised multi-stage Dockerfile passes the audit", fg == [], fg, []),
        check("naive Dockerfile flagged on every rule", fb == ["dev-deps-in-runtime", "full-base-runtime", "no-healthcheck",
                                                              "npm-install-not-ci", "runs-as-root", "single-stage"], fb),
    ], [rep, wd / "Dockerfile"]


def _py_dockerfile_audit(text):
    stages, args = _dockerfile_stages(text)
    f = []

    def ver(img):
        img = re.sub(r"\$\{(\w+)\}", lambda m: args.get(m.group(1), "?"), img)
        m = re.search(r"python(?::|)(\d+\.\d+)", img)
        return m.group(1) if m else None
    vers = {ver(s["image"]) for s in stages if "python" in s["image"]}
    if len(vers) > 1:
        f.append("interpreter-split-across-stages")
    if any("alpine" in s["image"] and "python" in s["image"] for s in stages):
        f.append("alpine-for-python")
    final = stages[-1]
    if not any(l.startswith("USER") for l in final["lines"]):
        f.append("runs-as-root")
    if not re.search(r"PYTHONUNBUFFERED=1", text):
        f.append("no-pythonunbuffered")
    if re.search(r"pip install(?!.*--no-cache-dir)", text):
        f.append("pip-cache-in-layer")
    if re.search(r"apt-get install", text) and "rm -rf /var/lib/apt/lists" not in text:
        f.append("apt-lists-left")
    return sorted(f)


@card(K("2146-container-plugin/7720-python-containers"))
def python_containers(task, wd):
    """Interpreter coupling proven for real: a 3.12 venv copied onto a 3.13 runtime drops off sys.path."""
    wd = Path(wd)
    if not (shutil.which("python3.12") and shutil.which("python3.13")):
        raise RuntimeError("needs python3.12 and python3.13")
    venv = wd / "venv"
    rc, out = sh(["python3.12", "-m", "venv", "--without-pip", venv])
    if rc:
        raise RuntimeError(out)
    (venv / "lib/python3.12/site-packages/appdep.py").write_text("VALUE = 42\n")
    probe = "import sys\nassert [p for p in sys.path if '/venv/' in p], sys.path\nimport appdep\nprint('ok', appdep.VALUE, sys.version_info[:2])\n"
    p_ok = subprocess.run([str(venv / "bin/python"), "-"], input=probe, capture_output=True, text=True, timeout=30)
    # runtime stage on a different minor version: same venv directory, interpreter swapped to 3.13
    mism = wd / "venv313"
    shutil.copytree(venv, mism, symlinks=True)
    for n in ("python", "python3", "python3.12"):
        t = mism / "bin" / n
        if t.is_symlink() or t.exists():
            t.unlink()
    os.symlink(shutil.which("python3.13"), mism / "bin/python")
    cfg = (mism / "pyvenv.cfg").read_text()
    cfg = re.sub(r"version = .*", "version = 3.13.0", cfg)
    cfg = re.sub(r"home = .*", "home = " + str(Path(shutil.which("python3.13")).parent), cfg)
    (mism / "pyvenv.cfg").write_text(cfg)
    p_bad = subprocess.run([str(mism / "bin/python"), "-"], input=probe, capture_output=True, text=True, timeout=30)
    # the check without stdin asserts nothing and passes anyway (the -i trap)
    p_empty = subprocess.run([str(mism / "bin/python"), "-"], input="", capture_output=True, text=True, timeout=30)
    good = textwrap.dedent("""
        ARG PYTHON_VERSION=3.12
        FROM python:${PYTHON_VERSION}-slim AS builder
        WORKDIR /app
        RUN pip install --no-cache-dir uv
        COPY pyproject.toml uv.lock ./
        RUN uv sync --frozen --no-dev
        FROM python:${PYTHON_VERSION}-slim
        RUN apt-get update && apt-get install -y --no-install-recommends libpq5 && rm -rf /var/lib/apt/lists/*
        RUN adduser --uid 1001 --disabled-password appuser
        COPY --from=builder --chown=appuser /app/.venv /app/.venv
        ENV PATH="/app/.venv/bin:$PATH" PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
        USER appuser
        CMD ["python", "-m", "app"]
        """)
    bad = "FROM ghcr.io/astral-sh/uv:python3.12-alpine AS build\nRUN pip install -r req.txt\nFROM python:3.13-alpine\nRUN apt-get install -y libpq5\nCOPY --from=build /app/.venv /app/.venv\n"
    tw(wd / "Dockerfile", good)
    fg, fb = _py_dockerfile_audit(good), _py_dockerfile_audit(bad)
    rep = jw(wd / "python_image_report.json", {"matched": p_ok.stdout.strip(), "mismatched_rc": p_bad.returncode,
                                               "mismatched_err": p_bad.stderr.strip().splitlines()[-1:],
                                               "empty_stdin_rc": p_empty.returncode, "good_findings": fg, "bad_findings": fb})
    return [
        check("matched interpreter: venv on sys.path, dependency imports", p_ok.returncode == 0 and "ok 42" in p_ok.stdout,
              p_ok.stdout.strip()),
        check("negative control: 3.12 venv under a 3.13 runtime loses the venv entirely", p_bad.returncode != 0
              and "AssertionError" in p_bad.stderr, p_bad.stderr.strip().splitlines()[-1:]),
        check("gate without stdin passes vacuously (why -i is load-bearing)", p_empty.returncode == 0, p_empty.returncode, 0),
        check("one-ARG slim multi-stage Dockerfile passes the audit", fg == [], fg, []),
        check("split/alpine/root Dockerfile flagged", fb == ["alpine-for-python", "apt-lists-left", "interpreter-split-across-stages",
                                                            "no-pythonunbuffered", "pip-cache-in-layer", "runs-as-root"], fb),
    ], [rep, wd / "Dockerfile"]


# ───────────────────────────── GitHub Actions: AI review triage, auto-fix workflow, dev loop ─────────────────────────────

def _ai_review_cause(log, duration_s=60, pr_comments=0):
    """The skill's decision table: read subtype and is_error together, then the finding count."""
    if duration_s <= 6:
        return "skipped-not-a-control"
    sub = re.search(r'"subtype":\s*"(\w+)"', log)
    err = re.search(r'"is_error":\s*(true|false)', log)
    sub, err = (sub.group(1) if sub else None), (err.group(1) == "true" if err else None)
    found = re.search(r"Found (\d+)", log)
    if sub == "error_max_turns":
        return "1-budget-exhaustion"
    if sub == "success" and err is False and found and pr_comments == 0:
        return "3-unpublished-finding"
    if sub == "success" and err is False and not found and "exceeding the configured maximum" in log:
        return "2-turn-ceiling-overrun"
    if sub == "success" and err is True and not found:
        return "4-errored-despite-completing"
    return "unclassified"


@card(K("2153-github-actions-plugin/7753-ai-review-max-turns"))
def ai_review_max_turns(task, wd):
    wd = Path(wd)
    logs = {
        "c1": ('{"subtype": "error_max_turns", "is_error": true, "num_turns": 7}', 300, 0),
        "c2": ('{"subtype": "success", "is_error": false, "num_turns": 53}\n##[error]Claude reported a successful result after 53 '
               'turns, exceeding the configured maximum of 50', 400, 0),
        "c3": ('{"subtype": "success", "is_error": false, "permission_denials_count": 13}\n::error::Found 2 critical security issues',
               500, 0),
        "c4": ('{"subtype": "success", "is_error": true, "num_turns": 5, "permission_denials_count": 0}\n##[error]Claude result '
               'reported subtype success with is_error:true', 90, 0),
        "skip": ('{"subtype": "success", "is_error": false}', 5, 0),
    }
    got = {k: _ai_review_cause(v[0], v[1], v[2]) for k, v in logs.items()}
    # is_error alone (the trap): files c2/c3 as "fine" and c4 with c1
    naive = {k: ("error" if '"is_error": true' in v[0] else "pass") for k, v in logs.items()}
    reruns = [{"aria": "fail", "typescript": "pass", "secrets": "pass", "owasp": "pass"},
              {"aria": "pass", "typescript": "fail", "secrets": "fail", "owasp": "fail"}]
    failing = [frozenset(k for k, v in r.items() if v == "fail") for r in reruns]
    rotating = len(set(failing)) > 1
    p = jw(wd / "triage.json", {"causes": got, "naive_is_error_only": naive, "rerun_sets": [sorted(f) for f in failing],
                                "rotating_budget_signature": rotating})
    return [
        check("four causes and the skipped-run trap separated", got == {"c1": "1-budget-exhaustion", "c2": "2-turn-ceiling-overrun",
              "c3": "3-unpublished-finding", "c4": "4-errored-despite-completing", "skip": "skipped-not-a-control"}, got),
        check("negative control: is_error alone conflates causes", naive["c1"] == naive["c4"] and naive["c2"] == naive["c3"], naive),
        check("rotating failure set across reruns detected", rotating, [sorted(f) for f in failing]),
    ], [p]


def _yaml():
    import yaml
    return yaml


@card(K("2153-github-actions-plugin/7760-github-workflow-auto-fix"))
def github_workflow_auto_fix(task, wd):
    yaml = _yaml()
    wd = Path(wd)
    wf = wd / ".github/workflows"
    existing = {"test.yml": "Test: Suite", "lint.yml": "Plugin: Lint skills", "release.yml": "Release: please",
                "claude.yml": "Claude: Code review", "reusable-build.yml": "Reusable: Build"}
    for f, n in existing.items():
        on = "workflow_call" if f.startswith("reusable") else "push"
        tw(wf / f, "name: \"%s\"\non: [%s]\njobs:\n  j:\n    runs-on: ubuntu-latest\n    steps:\n      - run: echo\n" % (n, on))

    def candidates(paths, naive=False):
        out = []
        for p in sorted(paths):
            d = yaml.safe_load(p.read_text())
            name, trig = d["name"], d.get(True, d.get("on"))
            if not naive and (re.match(r"(Release|Deploy)", name) or "Claude" in name or "workflow_call" in json.dumps(trig)):
                continue
            out.append(name)
        return out
    mon = candidates(wf.glob("*.yml"))
    mon_naive = candidates(wf.glob("*.yml"), naive=True)
    doc = {"name": "Auto-fix: CI failures",
           "on": {"workflow_run": {"workflows": mon, "types": ["completed"]}},
           "concurrency": {"group": "auto-fix-${{ github.event.workflow_run.head_branch }}", "cancel-in-progress": False},
           "permissions": {"contents": "write", "pull-requests": "write", "issues": "write", "actions": "read", "id-token": "write"},
           "jobs": {"auto-fix": {"if": "github.event.workflow_run.conclusion == 'failure' && github.event.workflow_run.actor.type != 'Bot'"
                                       " && github.event.workflow_run.head_branch != 'main' && github.event.workflow_run.head_branch != 'master'",
                                 "runs-on": "ubuntu-latest",
                                 "steps": [{"name": "Checkout failed branch", "uses": "actions/checkout@v4",
                                            "with": {"ref": "${{ github.event.workflow_run.head_branch }}", "fetch-depth": 0}},
                                           {"name": "Analyze and fix with Claude", "uses": "anthropics/claude-code-action@v1",
                                            "with": {"claude_code_oauth_token": "${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}",
                                                     "claude_args": "--model opus\n--effort medium\n--max-turns 30\n"
                                                                    "--allowedTools \"Read,Write,Edit,Grep,Glob,Bash(git *),Bash(gh *)\""}}]}}}
    out = wf / "github-workflow-auto-fix.yml"
    out.write_text(yaml.safe_dump(doc, sort_keys=False, allow_unicode=True))
    back = yaml.safe_load(out.read_text())
    names = set(existing.values())
    trig = back.get("on", back.get(True))
    monitored = trig["workflow_run"]["workflows"]

    def guard(cond, ev):
        env = {"github.event.workflow_run.conclusion": ev["conclusion"], "github.event.workflow_run.actor.type": ev["actor"],
               "github.event.workflow_run.head_branch": ev["branch"]}
        expr = cond
        for k, v in env.items():
            expr = expr.replace(k, repr(v))
        return eval(expr.replace("&&", " and ").replace("!=", " != "), {})
    cond = back["jobs"]["auto-fix"]["if"]
    evs = [{"conclusion": "failure", "actor": "User", "branch": "feat/x"}, {"conclusion": "failure", "actor": "Bot", "branch": "feat/x"},
           {"conclusion": "failure", "actor": "User", "branch": "main"}, {"conclusion": "success", "actor": "User", "branch": "feat/x"}]
    fires = [guard(cond, e) for e in evs]
    return [
        check("generated YAML parses and display name follows '<Domain>: <Action>'", back["name"] == "Auto-fix: CI failures"),
        check("monitored names match existing workflows' name: exactly", set(monitored) <= names and monitored ==
              ["Plugin: Lint skills", "Test: Suite"], monitored),
        check("negative control: naive auto-detect would monitor release/Claude/reusable (recursion)",
              {"Release: please", "Claude: Code review", "Reusable: Build"} <= set(mon_naive), mon_naive),
        check("job guard fires only on non-bot failures off main", fires == [True, False, False, False], fires),
        check("max-turns bound and tool boundary in claude_args",
              "--max-turns 30" in back["jobs"]["auto-fix"]["steps"][1]["with"]["claude_args"]),
    ], [out]


@card(K("2153-github-actions-plugin/7763-workflow-dev"))
def workflow_dev(task, wd):
    import sys
    wd = Path(wd)
    repo = wd / "repo"
    env = {"GIT_AUTHOR_NAME": "dev", "GIT_AUTHOR_EMAIL": "d@x", "GIT_COMMITTER_NAME": "dev", "GIT_COMMITTER_EMAIL": "d@x"}
    tw(repo / "pyproject.toml", "[project]\nname = \"slug\"\nversion = \"0.1.0\"\n")
    tw(repo / "slug.py", "def slugify(s):\n    return s.lower().replace(' ', '-')\n")
    tw(repo / "test_slug.py", "import unittest, slug\nclass T(unittest.TestCase):\n    def test_basic(self):\n"
                              "        self.assertEqual(slug.slugify('A B'), 'a-b')\n    def test_strip(self):\n"
                              "        self.assertEqual(slug.slugify('  A B '), 'a-b')\n")
    sh(["git", "init", "-q", "-b", "main"], cwd=repo)
    sh(["git", "add", "-A"], cwd=repo, env=env)
    sh(["git", "commit", "-qm", "init"], cwd=repo, env=env)
    kinds = {"manage.py": "django", "package.json": "node", "Cargo.toml": "rust", "pyproject.toml": "python", "go.mod": "go"}
    ptype = next(v for k, v in kinds.items() if (repo / k).exists())
    rc, out = sh([sys.executable, "-m", "unittest", "-v"], cwd=repo)
    failing = re.findall(r"^(test_\w+) \(.*\) \.\.\. FAIL", out, re.M)
    issues = [{"number": 1, "title": "Docs typo", "labels": ["documentation"], "acceptance": True, "assignee": None},
              {"number": 2, "title": "Refactor parser", "labels": ["technical-debt"], "acceptance": True, "assignee": None},
              {"number": 3, "title": "Crash on upload", "labels": ["bug", "priority: critical"], "acceptance": True, "assignee": None,
               "blocked": True}]
    for t in failing:
        issues.append({"number": len(issues) + 1, "title": "Test failure: %s" % t, "labels": ["bug", "test-failure"],
                       "acceptance": True, "assignee": None, "body": out[-300:]})

    def eligible(i):
        return i["acceptance"] and not i.get("blocked") and i["assignee"] is None

    def prio(i):
        L = i["labels"]
        if "priority: critical" in L or ("bug" in L and "high priority" in L):
            return 0
        if "test-failure" in L:
            return 1
        if "good first issue" in L:
            return 2
        if "technical-debt" in L or "refactor" in L:
            return 4
        return 3
    pick = sorted([i for i in issues if eligible(i)], key=lambda i: (prio(i), i["number"]))[0]
    naive_pick = sorted(issues, key=lambda i: (prio(i), i["number"]))[0]
    br = "fix/issue-%d-strip-whitespace" % pick["number"]
    sh(["git", "switch", "-qc", br], cwd=repo)
    (repo / "slug.py").write_text("def slugify(s):\n    return s.strip().lower().replace(' ', '-')\n")
    rc2, _ = sh([sys.executable, "-m", "unittest"], cwd=repo)
    msg = "fix: resolve issue #%d - strip whitespace" % pick["number"]
    sh(["git", "commit", "-qam", msg], cwd=repo, env=env)
    log = sh(["git", "log", "-1", "--format=%s", br], cwd=repo)[1].strip()
    pr = {"title": msg, "body": "Fixes #%d" % pick["number"], "head": br, "base": "main", "checks": "green" if rc2 == 0 else "red"}
    p = jw(wd / "dev_loop.json", {"project_type": ptype, "failing_tests": failing, "issues": issues, "picked": pick["number"],
                                  "pr": pr})
    return [
        check("project type detected and suite run", ptype == "python" and rc != 0, [ptype, rc]),
        check("failing test filed as issue with bug/test-failure labels", failing == ["test_strip"]
              and issues[-1]["title"] == "Test failure: test_strip", failing),
        check("selection skips the blocked critical bug and picks the test failure", pick["number"] == 4, pick["number"], 4),
        check("negative control: priority without eligibility filter picks the blocked issue", naive_pick["number"] == 3, naive_pick["number"]),
        check("TDD fix on branch turns suite green; conventional commit references issue", rc2 == 0 and log == msg
              and pr["body"] == "Fixes #4", [rc2, log]),
    ], [p]


# ───────────────────────────── Home Assistant config validation ─────────────────────────────

def _ha_validate(root):
    yaml = _yaml()

    class L(yaml.SafeLoader):
        pass
    used, dups, errors = set(), [], []

    def secret(loader, node):
        used.add(node.value)
        return "<secret:%s>" % node.value

    def include(loader, node):
        return "<include:%s>" % node.value

    def mapping(loader, node, deep=False):
        keys = [k.value for k, _ in node.value if isinstance(k, yaml.ScalarNode)]
        for k in sorted({k for k in keys if keys.count(k) > 1}):
            dups.append((Path(node.start_mark.name).name, node.start_mark.line + 1, k))
        return yaml.SafeLoader.construct_mapping(loader, node, deep)
    L.add_constructor("!secret", secret)
    for t in ("!include", "!include_dir_merge_named", "!include_dir_list", "!input", "!env_var"):
        L.add_constructor(t, include)
    L.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, mapping)
    for p in sorted(Path(root).glob("*.yaml")):
        if p.name == "secrets.yaml":
            continue
        try:
            with open(p) as fh:
                yaml.load(fh, Loader=L)
        except yaml.YAMLError as e:
            m = getattr(e, "problem_mark", None)
            errors.append((p.name, (m.line + 1) if m else None, str(getattr(e, "problem", e))))
    sec = Path(root) / "secrets.yaml"
    defined = set(yaml.safe_load(sec.read_text()) or {}) if sec.exists() else set()
    return {"syntax_errors": errors, "duplicate_keys": dups, "undefined_secrets": sorted(used - defined)}


@card(K("2155-home-assistant-plugin/7774-ha-validate"))
def ha_validate(task, wd):
    yaml = _yaml()
    wd = Path(wd)
    good, bad = wd / "good", wd / "bad"
    for r in (good, bad):
        tw(r / "secrets.yaml", "wifi_password: hunter2\napi_token: abc\n")
    tw(good / "configuration.yaml", "homeassistant:\n  name: Home\n  token: !secret api_token\nautomation: !include automations.yaml\n")
    tw(good / "automations.yaml", "- alias: Lights\n  trigger:\n    platform: sun\n    event: sunset\n")
    tw(bad / "configuration.yaml", "homeassistant:\n  name: Home\n  token: !secret api_tokn\n  name: Other\n")
    tw(bad / "scripts.yaml", "wake:\n  sequence:\n    - service: light.on\n   bad_indent: 1\n")
    rg, rb = _ha_validate(good), _ha_validate(bad)
    try:
        yaml.safe_load((good / "configuration.yaml").read_text())
        plain = "parsed"
    except yaml.YAMLError as e:
        plain = "error: " + str(e).split("\n")[0]
    p = jw(wd / "ha_validation.json", {"good": rg, "bad": rb, "plain_safe_load_on_good": plain})
    return [
        check("valid config with !secret/!include passes every check", rg == {"syntax_errors": [], "duplicate_keys": [],
              "undefined_secrets": []}, rg),
        check("undefined secret found", rb["undefined_secrets"] == ["api_tokn"], rb["undefined_secrets"]),
        check("duplicate key found with file and line", rb["duplicate_keys"] == [("configuration.yaml", 2, "name")], rb["duplicate_keys"]),
        check("indentation error reported with line", len(rb["syntax_errors"]) == 1 and rb["syntax_errors"][0][0] == "scripts.yaml"
              and rb["syntax_errors"][0][1] == 4, rb["syntax_errors"]),
        check("negative control: plain safe_load cannot read HA tags", plain.startswith("error"), plain),
    ], [p]


# ───────────────────────────── Python tool migrations and ruff format ─────────────────────────────

PY_FIXTURE = '''import os, sys
def f(a,b):
    x = {'k': "v", 'long_key_name_number_one': 1, 'long_key_name_number_two': 2, 'k3': 3}
    unused = 5
    return a+b
'''


def _black_to_ruff(pyproject_text, precommit_text):
    import tomllib
    yaml = _yaml()
    cfg = tomllib.loads(pyproject_text)
    blk = cfg.get("tool", {}).get("black", {})
    ruff, fmt = {}, {}
    if "line-length" in blk:
        ruff["line-length"] = blk["line-length"]
    if "target-version" in blk:
        tv = blk["target-version"]
        ruff["target-version"] = tv[0] if isinstance(tv, list) else tv
    if blk.get("skip-string-normalization"):
        fmt["quote-style"] = "preserve"
    if blk.get("skip-magic-trailing-comma"):
        fmt["skip-magic-trailing-comma"] = True
    if blk.get("preview"):
        fmt["preview"] = True
    body = re.sub(r"(?ms)^\[tool\.black\]\n.*?(?=^\[|\Z)", "", pyproject_text).rstrip() + "\n"

    def val(v):
        return json.dumps(v) if not isinstance(v, bool) else ("true" if v else "false")
    body += "\n[tool.ruff]\n" + "".join("%s = %s\n" % (k, val(v)) for k, v in ruff.items())
    if fmt:
        body += "\n[tool.ruff.format]\n" + "".join("%s = %s\n" % (k, val(v)) for k, v in fmt.items())
    pc = yaml.safe_load(precommit_text)
    pc["repos"] = [r for r in pc["repos"] if "psf/black" not in r["repo"]]
    rr = [r for r in pc["repos"] if "ruff-pre-commit" in r["repo"]]
    if rr:
        if "ruff-format" not in [h["id"] for h in rr[0]["hooks"]]:
            rr[0]["hooks"].append({"id": "ruff-format"})
    else:
        pc["repos"].append({"repo": "https://github.com/astral-sh/ruff-pre-commit", "rev": "v0.9.1",
                            "hooks": [{"id": "ruff", "args": ["--fix"]}, {"id": "ruff-format"}]})
    return body, yaml.safe_dump(pc, sort_keys=False), {"black": blk}


@card(K("2160-migration-patterns-plugin/7799-black-to-ruff-format"))
def black_to_ruff(task, wd):
    import tomllib
    wd = Path(wd)
    proj = wd / "proj"
    pyproject = "[project]\nname = \"demo\"\nversion = \"0.1\"\n\n[tool.black]\nline-length = 100\ntarget-version = [\"py311\"]\nskip-string-normalization = true\n"
    pc = "repos:\n  - repo: https://github.com/psf/black\n    rev: 24.1.0\n    hooks:\n      - id: black\n  - repo: https://github.com/astral-sh/ruff-pre-commit\n    rev: v0.9.1\n    hooks:\n      - id: ruff\n"
    new_pp, new_pc, audit = _black_to_ruff(pyproject, pc)
    tw(proj / "pyproject.toml", new_pp)
    (proj / ".pre-commit-config.yaml").write_text(new_pc)
    for d in ("black_out", "ruff_out", "ruff_default"):
        tw(wd / d / "m.py", PY_FIXTURE)
    rc_b, ob = sh(["black", "-q", "-l", "100", "-S", "-t", "py311", wd / "black_out/m.py"])
    rc_r, orr = sh(["ruff", "format", "--config", proj / "pyproject.toml", wd / "ruff_out/m.py"])
    rc_d, od = sh(["ruff", "format", "--isolated", wd / "ruff_default/m.py"])
    if rc_b or rc_r or rc_d:
        raise RuntimeError(ob + orr + od)
    B, R, D = [(wd / d / "m.py").read_text() for d in ("black_out", "ruff_out", "ruff_default")]
    parsed = tomllib.loads(new_pp)
    hooks = [h["id"] for r in _yaml().safe_load(new_pc)["repos"] for h in r["hooks"]]
    return [
        check("[tool.black] mapped to [tool.ruff]/[tool.ruff.format]", "black" not in parsed["tool"]
              and {k: v for k, v in parsed["tool"]["ruff"].items() if k != "format"} == {"line-length": 100, "target-version": "py311"}
              and parsed["tool"]["ruff"]["format"] == {"quote-style": "preserve"}, parsed["tool"]),
        check("pre-commit: psf/black removed, ruff-format added to existing ruff repo", hooks == ["ruff", "ruff-format"], hooks),
        check("ruff format with migrated config reproduces black's output byte for byte", R == B, hashlib.sha256(R.encode()).hexdigest()[:12],
              hashlib.sha256(B.encode()).hexdigest()[:12]),
        check("negative control: ruff with default config differs from the team's black style", D != B, "differs"),
    ], [proj / "pyproject.toml", proj / ".pre-commit-config.yaml"]


def _lint_set(out, rx):
    return sorted(set(re.findall(rx, out, re.M)))


@card(K("2160-migration-patterns-plugin/7802-flake8-to-ruff"))
def flake8_to_ruff(task, wd):
    import configparser
    import tomllib
    wd = Path(wd)
    proj = wd / "proj"
    tw(proj / "setup.cfg", "[flake8]\nmax-line-length = 100\nextend-ignore = E203,W503\nper-file-ignores =\n    tests/*:F401\n")
    long = "x = '" + "a" * 92 + "'\n"           # 98 chars: fine at 100, E501 at 79
    longer = "y = '" + "b" * 100 + "'\n"        # 106 chars: E501 at 100
    tw(proj / "pkg/mod.py", "import os\n" + long + longer + "\n\ndef g():\n    z = 1\n    return 2\n")
    tw(proj / "tests/test_m.py", "import sys\n")
    cp = configparser.ConfigParser()
    cp.read(proj / "setup.cfg")
    f8 = cp["flake8"]
    ignore = [c.strip() for c in f8["extend-ignore"].split(",")]
    pfi = {}
    for line in f8["per-file-ignores"].strip().splitlines():
        path, codes = line.strip().split(":")
        pfi[path] = [c.strip() for c in codes.split(",")]
    ruff_ignore = [c for c in ignore if not c.startswith("W503")]      # W503 has no ruff rule (formatter-owned)
    toml = ("[tool.ruff]\nline-length = %d\n\n[tool.ruff.lint]\nselect = [\"E\", \"F\", \"W\"]\nignore = %s\n\n"
            "[tool.ruff.lint.per-file-ignores]\n%s" % (int(f8["max-line-length"]), json.dumps(ruff_ignore),
                                                       "".join('"%s" = %s\n' % (k, json.dumps(v)) for k, v in pfi.items())))
    tw(proj / "pyproject.toml", toml)
    rc1, o_f8 = sh(["flake8", "."], cwd=proj)
    rc2, o_rf = sh(["ruff", "check", "--no-cache", "--output-format", "concise", "."], cwd=proj)
    rc3, o_rd = sh(["ruff", "check", "--no-cache", "--isolated", "--output-format", "concise", "."], cwd=proj)
    norm = r"^\.?/?([\w/]+\.py):(\d+):\d+:? ([A-Z]\d+)"
    s_f8 = sorted(set(re.findall(norm, o_f8, re.M)))
    s_rf = sorted(set(re.findall(norm, o_rf, re.M)))
    s_rd = sorted(set(re.findall(norm, o_rd, re.M)))
    p = jw(wd / "migration_audit.json", {"flake8": s_f8, "ruff_migrated": s_rf, "ruff_default": s_rd,
                                         "dropped_without_equivalent": ["W503"], "ruff_config": tomllib.loads(toml)})
    return [
        check("flake8 found the planted issues", ("pkg/mod.py", "3", "E501") in s_f8 and ("pkg/mod.py", "7", "F841") in s_f8 and ("pkg/mod.py", "1", "F401") in s_f8, s_f8),
        check("ruff with migrated config reports exactly flake8's findings", s_rf == s_f8, s_rf, s_f8),
        check("per-file-ignores carried over (tests F401 silenced)", not any(x[0].startswith("tests") for x in s_rf), s_rf),
        check("negative control: unmigrated ruff disagrees with flake8", s_rd != s_f8, s_rd),
    ], [p, proj / "pyproject.toml"]


RENOVATE_ALLOWED_POST_UPDATE = {"bundlerConservative", "gomodMassage", "gomodTidy", "gomodTidy1.17", "gomodTidyE", "gomodUpdateImportPaths",
                                "gomodSkipVendor", "gomodVendor", "helmUpdateSubChartArchives", "kustomizeInflateHelmCharts",
                                "npmDedupe", "npmInstallTwice", "pnpmDedupe", "yarnDedupeFewer", "yarnDedupeHighest", "dotnetWorkloadRestore"}


def _cutover_gate(runs, side_effects, secret_on_repo):
    succ = [r for r in runs if r["conclusion"] == "success"]
    diag = []
    for r in runs:
        if r["conclusion"] == "failure":
            diag.append("credential/token" if r["steps_run"] >= 1 and r["seconds"] <= 10 else
                        "quota" if r["steps_run"] == 0 and r["seconds"] <= 3 else "other")
    allowed = bool(succ) and bool(side_effects) and secret_on_repo
    return {"remove_incumbent": allowed, "stage": "merge" if allowed else "draft-PR", "failure_diagnosis": diag}


@card(K("2160-migration-patterns-plugin/7805-tool-migration-cutover"))
def tool_migration_cutover(task, wd):
    wd = Path(wd)
    broken = [{"conclusion": "failure", "seconds": 8, "steps_run": 1}] * 4 + [{"conclusion": "failure", "seconds": 2, "steps_run": 0}]
    working = broken[:2] + [{"conclusion": "success", "seconds": 95, "steps_run": 6}]
    g1 = _cutover_gate(broken, [], True)
    g2 = _cutover_gate(working, ["renovate/lodash-4.x"], False)
    g3 = _cutover_gate(working, ["Dependency Dashboard #12", "renovate/lodash-4.x"], True)
    naive = bool(Path(tw(wd / "renovate.json", json.dumps({"extends": ["config:recommended"]}))).exists())   # "config exists"
    cfgs = {"bad": {"extends": ["config:recommended"], "postUpdateOptions": ["bunDedupe"]},
            "good": {"extends": ["config:recommended"], "lockFileMaintenance": {"enabled": True}}}
    val = {k: sorted(set(v.get("postUpdateOptions", [])) - RENOVATE_ALLOWED_POST_UPDATE) for k, v in cfgs.items()}
    # which formatter is canonical: ask both tools on the committed file
    tw(wd / "committed/m.py", "x = {'a': 1}\n")
    rc_black_S = sh(["black", "--check", "-q", "-S", wd / "committed/m.py"])[0]
    rc_ruff = sh(["ruff", "format", "--isolated", "--check", wd / "committed/m.py"])[0]
    canonical = "black -S" if rc_black_S == 0 else "ruff"
    leftover = "ruff" if rc_ruff != 0 else "black -S"
    p = jw(wd / "cutover_decision.json", {"never_ran": g1, "no_secret": g2, "operational": g3, "renovate_invalid_values": val,
                                          "canonical_formatter": canonical, "leftover_formatter": leftover})
    return [
        check("replacement that never succeeded: keep incumbent, stage draft", g1["remove_incumbent"] is False and g1["stage"] == "draft-PR"
              and g1["failure_diagnosis"] == ["credential/token"] * 4 + ["quota"], g1),
        check("secret missing on consuming repo still blocks removal", g2["remove_incumbent"] is False, g2),
        check("positive operational signal unlocks removal", g3["remove_incumbent"] is True, g3),
        check("negative control: config presence alone would have approved the cutover", naive and not g1["remove_incumbent"]),
        check("invented bunDedupe rejected by allowedValues", val == {"bad": ["bunDedupe"], "good": []}, val),
        check("canonical formatter decided mechanically by --check", canonical == "black -S" and leftover == "ruff"
              and rc_black_S == 0 and rc_ruff != 0, [rc_black_S, rc_ruff]),
    ], [p]


@card(K("2166-python-plugin/7851-ruff-formatting"))
def ruff_formatting(task, wd):
    wd = Path(wd)
    proj = wd / "proj"
    tw(proj / "pyproject.toml", "[tool.ruff]\nline-length = 100\n\n[tool.ruff.format]\nquote-style = \"single\"\nexclude = [\"generated/*\"]\n")
    tw(proj / "src/a.py", PY_FIXTURE)
    tw(proj / "generated/g.py", PY_FIXTURE)
    original_g = (proj / "generated/g.py").read_text()
    rc_check0, _ = sh(["ruff", "format", "--check", "--no-cache", "."], cwd=proj)
    rc_diff, diff = sh(["ruff", "format", "--diff", "--no-cache", "."], cwd=proj)
    unchanged_by_diff = (proj / "src/a.py").read_text() == PY_FIXTURE
    sh(["ruff", "format", "--no-cache", "."], cwd=proj)
    once = (proj / "src/a.py").read_text()
    sh(["ruff", "format", "--no-cache", "."], cwd=proj)
    twice = (proj / "src/a.py").read_text()
    rc_check1, _ = sh(["ruff", "format", "--check", "--no-cache", "."], cwd=proj)
    import ast
    same_ast = ast.dump(ast.parse(PY_FIXTURE)) == ast.dump(ast.parse(once))
    longest = max(len(l) for l in once.splitlines())
    p = jw(wd / "format_report.json", {"check_before": rc_check0, "check_after": rc_check1, "diff_lines": len(diff.splitlines()),
                                       "longest_line": longest})
    return [
        check("negative control: --check fails on unformatted code", rc_check0 == 1, rc_check0, 1),
        check("--diff previews without writing", rc_diff == 1 and "+" in diff and unchanged_by_diff, rc_diff),
        check("format then --check passes; idempotent", rc_check1 == 0 and once == twice, rc_check1, 0),
        check("config honoured: single quotes, line length 100, exclude kept", '"v"' not in once and "'v'" in once and longest <= 100
              and (proj / "generated/g.py").read_text() == original_g, longest),
        check("formatting preserved the AST", same_ast),
    ], [p, proj / "src/a.py"]


# ───────────────────────────── Rust: unused deps, clippy configuration, development loop ─────────────────────────────

def _crate(root, name, deps=None, body="", lib=True, extra_toml=""):
    root = Path(root)
    dl = "".join('%s = { path = "../%s" }%s\n' % (d, d, c) for d, c in (deps or {}).items())
    tw(root / "Cargo.toml", '[package]\nname = "%s"\nversion = "0.1.0"\nedition = "2021"\n\n[dependencies]\n%s%s' % (name, dl, extra_toml))
    tw(root / ("src/lib.rs" if lib else "src/main.rs"), body)
    return root


def _cargo(args, cwd, wd, timeout=120):
    return sh(["cargo", args[0], "--offline", *args[1:]], cwd=cwd, env={"CARGO_TARGET_DIR": str(Path(wd) / "target"), "CARGO_TERM_COLOR": "never"},
              timeout=timeout)


def _machete_scan(crate_dir):
    """cargo-machete's method: for every declared dependency, search the crate's sources for a use of its
    (hyphen-to-underscore) name; honour `# machete:ignore` comments and .cargo-machete.toml ignores."""
    import tomllib
    crate_dir = Path(crate_dir)
    toml_text = (crate_dir / "Cargo.toml").read_text()
    deps = tomllib.loads(toml_text).get("dependencies", {})
    ignored = set(re.findall(r"^([\w-]+)\s*=.*#\s*machete:ignore", toml_text, re.M))
    cfg = crate_dir / ".cargo-machete.toml"
    if cfg.exists():
        ignored |= set(tomllib.loads(cfg.read_text()).get("ignore", {}).get("dependencies", []))
    src = "\n".join(p.read_text() for p in crate_dir.rglob("*.rs") if "target" not in p.parts)
    unused = []
    for d in deps:
        ident = d.replace("-", "_")
        if re.search(r"\b(use\s+(::)?%s\b|%s::|extern\s+crate\s+%s\b)" % (ident, ident, ident), src):
            continue
        if d not in ignored:
            unused.append(d)
    return sorted(unused), sorted(ignored)


@card(K("2167-rust-plugin/7864-cargo-machete"))
def cargo_machete(task, wd):
    wd = Path(wd)
    for d in ("dep-a", "dep_b", "dep-c", "dep-d"):
        _crate(wd / d, d, body="pub fn v() -> u32 { 7 }\n")
    app = _crate(wd / "app", "app", {"dep-a": "", "dep_b": "", "dep-c": "", "dep-d": "  # machete:ignore - used by build tooling"},
                 body="use dep_a::v;\nfn main() { println!(\"{}\", v() + dep_b::v()); }\n", lib=False)
    unused, ignored = _machete_scan(app)
    rc0, o0 = _cargo(["build", "-q"], app, wd)
    toml0 = (app / "Cargo.toml").read_text()
    (app / "Cargo.toml").write_text(re.sub(r"^dep-c = .*\n", "", toml0, flags=re.M))      # --fix equivalent
    rc_fix, o_fix = _cargo(["build", "-q"], app, wd)
    (app / "Cargo.toml").write_text(re.sub(r"^dep-a = .*\n", "", toml0, flags=re.M))      # removing a used dep
    rc_neg, _ = _cargo(["build", "-q"], app, wd)
    (app / "Cargo.toml").write_text(re.sub(r"^dep-c = .*\n", "", toml0, flags=re.M))
    after, _ = _machete_scan(app)
    p = jw(wd / "machete_report.json", {"unused": unused, "ignored": ignored, "build_before": rc0, "build_after_fix": rc_fix,
                                        "build_without_used_dep": rc_neg, "unused_after_fix": after})
    return [
        check("only the genuinely unused dependency is flagged", unused == ["dep-c"], unused, ["dep-c"]),
        check("machete:ignore annotation honoured", ignored == ["dep-d"], ignored),
        check("crate still builds after removing the flagged dep", rc0 == 0 and rc_fix == 0, [rc0, rc_fix, o_fix[-200:]]),
        check("negative control: removing a used dep breaks the build", rc_neg != 0, rc_neg, "non-zero"),
        check("rescan after fix is clean", after == [], after),
    ], [p]


def _clippy_lints(out):
    codes = []
    for line in out.splitlines():
        if line.startswith("{"):
            try:
                m = json.loads(line)
            except ValueError:
                continue
            c = (m.get("message") or {}).get("code") or {}
            if m.get("reason") == "compiler-message" and str(c.get("code", "")).startswith("clippy::"):
                codes.append(c["code"])
    return sorted(set(codes))


@card(K("2167-rust-plugin/7867-clippy-advanced"))
def clippy_advanced(task, wd):
    wd = Path(wd)
    body = ("pub fn home() -> String { std::env::var(\"HOME\").unwrap() }\n"
            "pub fn empty(v: &[u8]) -> bool { v.len() == 0 }\n")
    lints = "\n[lints.clippy]\ncorrectness = { level = \"deny\", priority = -1 }\nunwrap_used = \"deny\"\n"
    conf = _crate(wd / "configured", "configured", body=body, extra_toml=lints)
    tw(conf / "clippy.toml", "disallowed-methods = [\n  { path = \"std::env::var\", reason = \"Use std::env::var_os\" },\n]\n"
                             "disallowed-names = [\"foo\"]\n")
    plain = _crate(wd / "plain", "plain", body=body)
    rc_c, oc = _cargo(["clippy", "--message-format=json", "-q"], conf, wd)
    rc_p, op = _cargo(["clippy", "--message-format=json", "-q"], plain, wd)
    lc, lp = _clippy_lints(oc), _clippy_lints(op)
    fixed = ("pub fn home() -> Option<std::ffi::OsString> { std::env::var_os(\"HOME\") }\n"
             "pub fn empty(v: &[u8]) -> bool { v.is_empty() }\n")
    (conf / "src/lib.rs").write_text(fixed)
    rc_f, of = _cargo(["clippy", "-q", "--", "-D", "warnings"], conf, wd)
    p = jw(wd / "clippy_report.json", {"configured": lc, "plain": lp, "configured_rc": rc_c, "fixed_rc": rc_f})
    return [
        check("configured crate: disallowed_methods and unwrap_used fire, configured as errors",
              {"clippy::disallowed_methods", "clippy::unwrap_used", "clippy::len_zero"} <= set(lc) and rc_c != 0, lc),
        check("negative control: same code without config only gets default style lints",
              "clippy::disallowed_methods" not in lp and "clippy::unwrap_used" not in lp and "clippy::len_zero" in lp, lp),
        check("fixed code passes clippy -D warnings under the strict config", rc_f == 0, [rc_f, of[-200:]]),
    ], [p]


RUST_LIB = r'''
use std::fmt;

#[derive(Debug, PartialEq)]
pub enum ParseError { Empty, Bad(String) }

impl fmt::Display for ParseError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self { ParseError::Empty => write!(f, "empty input"), ParseError::Bad(s) => write!(f, "bad token: {s}") }
    }
}
impl std::error::Error for ParseError {}

/// Sum comma-separated integers, borrowing the input (no allocation of the source string).
pub fn sum_csv(input: &str) -> Result<i64, ParseError> {
    if input.trim().is_empty() { return Err(ParseError::Empty); }
    input.split(',').map(|t| t.trim().parse::<i64>().map_err(|_| ParseError::Bad(t.trim().to_string()))).sum()
}

pub fn longest<'a>(a: &'a str, b: &'a str) -> &'a str { if a.len() >= b.len() { a } else { b } }

#[cfg(test)]
mod tests {
    use super::*;
    #[test] fn sums() { assert_eq!(sum_csv("1, 2,3"), Ok(6)); }
    #[test] fn empty() { assert_eq!(sum_csv("  "), Err(ParseError::Empty)); }
    #[test] fn bad() { assert_eq!(sum_csv("1,x").unwrap_err().to_string(), "bad token: x"); }
    #[test] fn lifetimes() { let a = String::from("abc"); assert_eq!(longest(&a, "zz"), "abc"); }
}
'''


@card(K("2167-rust-plugin/7869-rust-development"))
def rust_development(task, wd):
    wd = Path(wd)
    c = _crate(wd / "csvsum", "csvsum", body=RUST_LIB)
    tw(c / "tests/integration.rs", "#[test]\nfn api() { assert_eq!(csvsum::sum_csv(\"10,-4\").unwrap(), 6); }\n")
    rc_fmt, ofmt = sh(["cargo", "fmt", "--check"], cwd=c)
    sh(["cargo", "fmt"], cwd=c)
    rc_fmt2, _ = sh(["cargo", "fmt", "--check"], cwd=c)
    rc, out = _cargo(["test", "-q"], c, wd)
    passed = sum(int(n) for n in re.findall(r"test result: ok\. (\d+) passed", out))
    (c / "src/lib.rs").write_text(RUST_LIB.replace("if input.trim().is_empty() { return Err(ParseError::Empty); }", ""))
    rc_bug, out_bug = _cargo(["test", "-q"], c, wd)
    p = jw(wd / "cargo_test_report.json", {"rc": rc, "passed": passed, "fmt_check_before": rc_fmt, "fmt_check_after": rc_fmt2,
                                           "buggy_rc": rc_bug})
    return [
        check("unit + integration tests pass (5 tests)", rc == 0 and passed == 5, [rc, passed], [0, 5]),
        check("rustfmt normalises the crate (check fails, then passes)", rc_fmt != 0 and rc_fmt2 == 0, [rc_fmt, rc_fmt2]),
        check("negative control: removing the empty-input guard fails the test suite", rc_bug != 0 and "empty" in out_bug, rc_bug),
    ], [p, c / "src/lib.rs"]


# ───────────────────────────── Bun: add, package manager, lockfile, development, publish ─────────────────────────────

def _bun(args, cwd, wd, env=None, timeout=60):
    e = {"BUN_INSTALL_CACHE_DIR": str(Path(wd) / ".bun-cache"), "DO_NOT_TRACK": "1", "NO_COLOR": "1"}
    e.update(env or {})
    return sh(["bun", *args], cwd=cwd, env=e, timeout=timeout)


def _bun_lock(path):
    """bun.lock is JSONC with trailing commas: strip them and parse."""
    txt = Path(path).read_text()
    return json.loads(re.sub(r",(\s*[}\]])", r"\1", txt))


def _monorepo(root):
    root = Path(root)
    jw(root / "package.json", {"name": "mono", "private": True, "workspaces": ["packages/*"]})
    jw(root / "packages/core/package.json", {"name": "@m/core", "version": "1.0.0", "main": "index.ts"})
    (root / "packages/core/index.ts").write_text("export const answer = (): number => 42;\n")
    jw(root / "packages/utils/package.json", {"name": "@m/utils", "version": "0.1.0", "main": "index.ts"})
    (root / "packages/utils/index.ts").write_text("export const twice = (n: number): number => n * 2;\n")
    for n in ("leftpad-local", "devkit-local"):
        jw(root / "vendor" / n / "package.json", {"name": n, "version": "3.1.0", "main": "index.js"})
        (root / "vendor" / n / "index.js").write_text("module.exports = %r;\n" % n)
    return root


@card(K("2174-typescript-plugin/7929-bun-add"))
def bun_add(task, wd):
    wd = Path(wd)
    root = _monorepo(wd / "mono")
    utils = root / "packages/utils"
    _bun(["install"], root, wd)
    before = (utils / "package.json").read_text()
    rc_dry, _ = _bun(["add", "--dry-run", "@m/core@workspace:*", "--cwd", "packages/utils"], root, wd)
    after_dry = (utils / "package.json").read_text()
    rc1, o1 = _bun(["add", "@m/core@workspace:*", "--cwd", "packages/utils"], root, wd)
    rc2, o2 = _bun(["add", "--dev", "devkit-local@file:../../vendor/devkit-local", "--cwd", "packages/utils"], root, wd)
    pj = json.loads((utils / "package.json").read_text())
    rc_why, why = _bun(["why", "@m/core"], root, wd)
    lock = _bun_lock(root / "bun.lock")
    p = jw(wd / "bun_add_report.json", {"utils_package": pj, "why": why.strip().splitlines()[:4], "lock_packages": sorted(lock["packages"])})
    return [
        check("negative control: --dry-run leaves package.json untouched", rc_dry == 0 and before == after_dry and "dependencies" not in
              json.loads(before)),
        check("runtime dep added to the targeted workspace", rc1 == 0 and pj.get("dependencies") == {"@m/core": "workspace:*"},
              pj.get("dependencies")),
        check("--dev lands in devDependencies only", rc2 == 0 and list(pj.get("devDependencies", {})) == ["devkit-local"]
              and "devkit-local" not in pj.get("dependencies", {}), pj.get("devDependencies")),
        check("bun why shows the new edge from @m/utils", rc_why == 0 and "@m/utils" in why, why.strip()[:120]),
        check("lockfile records both packages", "@m/core" in lock["packages"] and any(k.endswith("devkit-local") for k in lock["packages"]), sorted(lock["packages"])),
    ], [p, utils / "package.json"]


@card(K("2174-typescript-plugin/7936-bun-package-manager"))
def bun_package_manager(task, wd):
    wd = Path(wd)
    app = wd / "app"
    for n in ("leftpad-local", "devkit-local"):
        jw(wd / "vendor" / n / "package.json", {"name": n, "version": "3.1.0", "main": "index.js"})
        (wd / "vendor" / n / "index.js").write_text("module.exports = %r;\n" % n)
    jw(app / "package.json", {"name": "app", "version": "1.0.0", "dependencies": {"leftpad-local": "file:../vendor/leftpad-local"},
                              "devDependencies": {"devkit-local": "file:../vendor/devkit-local"}})
    rc_dry, _ = _bun(["install", "--dry-run"], app, wd)
    dry_nm = (app / "node_modules").exists()
    rc_i, _ = _bun(["install"], app, wd)
    full = sorted(os.listdir(app / "node_modules"))
    rc_f, _ = _bun(["install", "--frozen-lockfile"], app, wd)
    shutil.rmtree(app / "node_modules")
    rc_p, _ = _bun(["install", "--production"], app, wd)
    prod = sorted(x for x in os.listdir(app / "node_modules") if not x.startswith("."))
    pj = json.loads((app / "package.json").read_text())
    pj["dependencies"]["extra-local"] = "file:../vendor/devkit-local"
    jw(app / "package.json", pj)
    rc_stale, o_stale = _bun(["install", "--frozen-lockfile"], app, wd)
    rc_rm, _ = _bun(["remove", "extra-local"], app, wd)
    rc_f2, _ = _bun(["install", "--frozen-lockfile"], app, wd)
    p = jw(wd / "bun_pm_report.json", {"full": full, "production": prod, "frozen_ok": rc_f, "frozen_after_manual_edit": rc_stale,
                                       "frozen_after_remove": rc_f2})
    return [
        check("--dry-run installs nothing", rc_dry == 0 and not dry_nm, dry_nm, False),
        check("--production skips devDependencies", rc_p == 0 and prod == ["leftpad-local"] and "devkit-local" in full, [full, prod]),
        check("frozen lockfile passes when in sync", rc_i == 0 and rc_f == 0, rc_f, 0),
        check("negative control: frozen install fails after an unlocked package.json edit", rc_stale != 0, rc_stale, "non-zero"),
        check("bun remove restores a lock-consistent state", rc_rm == 0 and rc_f2 == 0, [rc_rm, rc_f2]),
    ], [p, app / "bun.lock"]


@card(K("2174-typescript-plugin/7934-bun-lockfile-update"))
def bun_lockfile_update(task, wd):
    wd = Path(wd)
    root = _monorepo(wd / "mono")
    jw(root / "packages/utils/package.json", {"name": "@m/utils", "version": "0.1.0", "dependencies": {"@m/core": "workspace:*"}})
    rc0, _ = _bun(["install"], root, wd)
    lock0 = (root / "bun.lock").read_text()
    L = _bun_lock(root / "bun.lock")
    # a merge conflict in the text lockfile: regenerate from package.json instead of hand-merging
    conflicted = lock0.replace('"packages": {', '"packages": {\n<<<<<<< HEAD\n    "x": ["x@1"],\n=======\n    "x": ["x@2"],\n>>>>>>> branch', 1)
    (root / "bun.lock").write_text(conflicted)
    rc_frozen_conflict, _ = _bun(["install", "--frozen-lockfile"], root, wd)
    (root / "bun.lock").unlink()
    rc_regen, _ = _bun(["install"], root, wd)
    regen = (root / "bun.lock").read_text()
    rc_frozen, _ = _bun(["install", "--frozen-lockfile"], root, wd)
    jw(root / "packages/core/package.json", {"name": "@m/core", "version": "1.0.0", "main": "index.ts",
                                             "dependencies": {"leftpad-local": "file:../../vendor/leftpad-local"}})
    rc_stale, _ = _bun(["install", "--frozen-lockfile"], root, wd)
    rc_upd, _ = _bun(["install"], root, wd)
    L2 = _bun_lock(root / "bun.lock")
    p = jw(wd / "lockfile_report.json", {"lockfileVersion": L.get("lockfileVersion"), "workspaces": sorted(L["workspaces"]),
                                         "regenerated_identical": regen == lock0, "conflict_frozen_rc": rc_frozen_conflict,
                                         "stale_rc": rc_stale, "packages_after_update": sorted(L2["packages"])})
    return [
        check("text bun.lock parses with every workspace", rc0 == 0 and sorted(L["workspaces"]) == ["", "packages/core", "packages/utils"],
              sorted(L["workspaces"])),
        check("conflicted lockfile is rejected, regeneration is deterministic", rc_frozen_conflict != 0 and rc_regen == 0
              and regen == lock0 and rc_frozen == 0, [rc_frozen_conflict, regen == lock0]),
        check("negative control: new dependency without lock update fails --frozen-lockfile", rc_stale != 0, rc_stale),
        check("bun install updates the lock to include the new package", rc_upd == 0 and any(k.endswith("leftpad-local") for k in L2["packages"])
              and not any(k.endswith("leftpad-local") for k in L["packages"]),
              sorted(L2["packages"])),
    ], [p, root / "bun.lock"]


@card(K("2174-typescript-plugin/7932-bun-development"))
def bun_development(task, wd):
    wd = Path(wd)
    root = _monorepo(wd / "mono")
    for n in ("core", "utils"):
        pj = json.loads((root / "packages" / n / "package.json").read_text())
        pj["scripts"] = {"build": "echo built-%s > built.txt" % n}
        jw(root / "packages" / n / "package.json", pj)
    jw(root / "package.json", {"name": "mono", "private": True, "workspaces": ["packages/*"], "scripts": {"hello": "echo hello-from-script"}})
    tw(root / "math.ts", "export function mean(xs: number[]): number { return xs.reduce((a, b) => a + b, 0) / xs.length; }\n"
                         "if (import.meta.main) console.log(mean([1, 2, 3, 4]));\n")
    tw(root / "math.test.ts", 'import { expect, test } from "bun:test";\nimport { mean } from "./math";\n'
                              'test("mean", () => { expect(mean([1, 2, 3, 4])).toBe(2.5); });\n'
                              'test("single", () => { expect(mean([7])).toBe(7); });\n')
    rc_run, o_run = _bun(["run", "--silent", "hello"], root, wd)
    rc_file, o_file = _bun(["math.ts"], root, wd)
    rc_t, o_t = _bun(["test"], root, wd)
    passed = re.search(r"(\d+) pass", o_t)
    rc_b, o_b = _bun(["build", "math.ts", "--target=node", "--minify", "--outfile", "dist/math.js"], root, wd)
    node_out = sh(["node", "-e", "const m=require('./dist/math.js');console.log(typeof m)"], cwd=root)
    rc_flt, _ = _bun(["run", "--filter", "@m/core", "build"], root, wd)
    core_built = (root / "packages/core/built.txt").exists()
    utils_built = (root / "packages/utils/built.txt").exists()
    (root / "math.ts").write_text((root / "math.ts").read_text().replace("/ xs.length", "/ (xs.length + 1)"))
    rc_bad, o_bad = _bun(["test"], root, wd)
    p = jw(wd / "bun_dev_report.json", {"script": o_run.strip(), "direct_ts": o_file.strip(), "tests": o_t.strip().splitlines()[-4:],
                                        "bundle_bytes": (root / "dist/math.js").stat().st_size if (root / "dist/math.js").exists() else 0,
                                        "filter": {"core": core_built, "utils": utils_built}})
    return [
        check("bun run script and direct .ts execution", rc_run == 0 and o_run.strip() == "hello-from-script" and o_file.strip() == "2.5",
              [o_run.strip(), o_file.strip()]),
        check("bun test passes 2 tests", rc_t == 0 and passed and passed.group(1) == "2", o_t.strip()[-80:]),
        check("bun build emits a minified bundle node can load", rc_b == 0 and (root / "dist/math.js").stat().st_size > 0
              and node_out[0] == 0, [rc_b, node_out]),
        check("--filter runs only the matching workspace", rc_flt == 0 and core_built and not utils_built, [core_built, utils_built]),
        check("negative control: a broken implementation fails bun test", rc_bad != 0, rc_bad),
    ], [p, root / "dist/math.js"]


def _pack_files(tgz):
    import tarfile
    with tarfile.open(tgz) as t:
        return sorted(m.name.split("/", 1)[1] for m in t.getmembers() if m.isfile()), {m.name.split("/", 1)[1]: m.mode for m in t.getmembers()}


def _publish_pkg(root, name, files=True):
    root = Path(root)
    pj = {"name": name, "version": "1.2.0", "type": "module", "bin": {"mytool": "./dist/cli.js"},
          "exports": {".": "./dist/index.js"}, "scripts": {"build": "bun build src/index.ts --outdir dist --target node && "
                                                                       "bun build src/cli.ts --outfile dist/cli.js --target node",
                                                             "prepublishOnly": "bun run build"}}
    if files:
        pj["files"] = ["dist", "README.md"]
    jw(root / "package.json", pj)
    tw(root / "src/index.ts", "export const greet = (n: string): string => `hi ${n}`;\n")
    tw(root / "src/cli.ts", "#!/usr/bin/env node\nimport { greet } from './index';\ndeclare const process: { argv: string[] };\ndeclare const console: { log(m: string): void };\nconsole.log(greet(process.argv[2] ?? 'x'));\n")
    tw(root / "tests/index.test.ts", "// test\n")
    tw(root / "README.md", "# tool\n")
    tw(root / "notes.local.md", "internal notes\n")
    tw(root / "tsconfig.json", json.dumps({"compilerOptions": {"strict": True, "noEmit": True, "module": "esnext", "target": "es2022",
                                                               "moduleResolution": "bundler", "types": [],
                                                               "lib": ["es2022"], "skipLibCheck": True}, "include": ["src"]}))
    return root


@card(K("2174-typescript-plugin/7938-bun-publishing"))
def bun_publishing(task, wd):
    wd = Path(wd)
    pkg = _publish_pkg(wd / "pkg", "@acme/mytool")
    raw = _publish_pkg(wd / "raw", "@acme/rawtool", files=False)
    out = {}
    for name, r in (("pkg", pkg), ("raw", raw)):
        rc_b, ob = _bun(["run", "build"], r, wd)
        if rc_b:
            raise RuntimeError(ob[-300:])
        rc, o = _bun(["pm", "pack"], r, wd)
        tgz = next(r.glob("*.tgz"))
        out[name] = _pack_files(tgz)
    files, modes = out["pkg"]
    cli = (pkg / "dist/cli.js").read_text()
    run = sh(["node", pkg / "dist/cli.js", "bun"])[1].strip()
    p = jw(wd / "publishing_report.json", {"whitelisted": files, "no_whitelist": out["raw"][0]})
    return [
        check("files whitelist ships only dist, README and package.json",
              files == ["README.md", "dist/cli.js", "dist/index.js", "package.json"], files),
        check("negative control: without a whitelist sources, tests and local notes leak",
              {"src/index.ts", "tests/index.test.ts", "notes.local.md"} <= set(out["raw"][0]), out["raw"][0]),
        check("bin entry keeps its shebang and runs", cli.startswith("#!/usr/bin/env node") and run == "hi bun", [cli[:22], run]),
    ], [p]


@card(K("2174-typescript-plugin/7937-bun-publish"))
def bun_publish(task, wd):
    wd = Path(wd)
    pkg = _publish_pkg(wd / "pkg", "@acme/mytool")
    # dummy, scoped-to-this-folder registry token so the dry run can resolve settings; nothing is uploaded
    tw(pkg / "bunfig.toml", '[install]\nregistry = { url = "https://registry.npmjs.org/", token = "dry-run-placeholder" }\n')
    tsc = shutil.which("tsc")
    rc_tc, o_tc = sh([tsc, "--noEmit", "-p", "."], cwd=pkg) if tsc else (0, "tsc missing")
    (pkg / "src/bad.ts").write_text("export const n: number = 'nope';\n")
    rc_tc_bad, _ = sh([tsc, "--noEmit", "-p", "."], cwd=pkg) if tsc else (1, "")
    (pkg / "src/bad.ts").unlink()
    name = json.loads((pkg / "package.json").read_text())["name"]
    scoped = name.startswith("@")
    args = ["publish", "--dry-run"] + (["--access", "public"] if scoped else [])
    rc_pub, o_pub = _bun(args, pkg, wd, timeout=60)
    rc_plain, o_plain = _bun(["publish", "--dry-run"], pkg, wd, timeout=60)
    access = re.search(r"Access:\s*(\w+)", o_pub)
    access_plain = re.search(r"Access:\s*(\w+)", o_plain)
    total = re.search(r"Total files:\s*(\d+)", o_pub)
    p = jw(wd / "publish_dry_run.json", {"typecheck": rc_tc, "typecheck_bad": rc_tc_bad, "scoped": scoped, "args": args,
                                         "access": access.group(1) if access else None, "files": int(total.group(1)) if total else None,
                                         "dry_run_line": [l for l in o_pub.splitlines() if "(dry-run)" in l]})
    return [
        check("pre-publish type check passes; a type error fails it", rc_tc == 0 and rc_tc_bad != 0, [rc_tc, rc_tc_bad]),
        check("scoped name detected and --access public applied", scoped and access and access.group(1) == "public", o_pub[-160:]),
        check("negative control: without --access the scoped dry run is not public", access_plain and access_plain.group(1) != "public",
              access_plain.group(1) if access_plain else None),
        check("dry run (prepublishOnly build) lists the 4 whitelisted files and uploads nothing",
              rc_pub == 0 and total and total.group(1) == "4" and "@acme/mytool@1.2.0 (dry-run)" in o_pub, o_pub[-120:]),
    ], [p]


TEMPORAL_TEST = r'''
import { expect, test, setSystemTime } from "bun:test";
const TZ = "Europe/Helsinki";
export const today = (tz = TZ) => Temporal.Instant.fromEpochMilliseconds(Date.now()).toZonedDateTimeISO(tz).toPlainDate();
const R: Record<string, unknown> = {};
test("today in a named zone at the boundary", () => {
  setSystemTime(new Date("2026-01-14T22:30:00Z"));          // 00:30 on the 15th in Helsinki
  R.utcSlice = new Date().toISOString().slice(0, 10);
  R.today = today().toString();
  expect(R.today).toBe("2026-01-15");
  setSystemTime();
});
test("calendar arithmetic and types", () => {
  R.feb = Temporal.PlainYearMonth.from("2026-02").daysInMonth;
  R.jan31 = Temporal.PlainDate.from("2026-01-31").add({ months: 1 }).toString();
  R.hours = Temporal.Duration.from({ hours: 7, minutes: 15 }).total("hours");
  R.dow = Temporal.PlainDate.from("2026-06-14").dayOfWeek;     // a Sunday -> 7
  R.legacyDateGetDate = new Date("2026-06-15").getDate();       // host zone read of a UTC-midnight Date
  R.plain = Temporal.PlainDate.from("2026-06-15").day;
  let impossible = "accepted"; try { Temporal.PlainDate.from("2026-02-30"); } catch (e) { impossible = (e as Error).name; }
  R.impossible = impossible;
  R.clamped = Temporal.PlainDate.from({ year: 2026, month: 2, day: 30 }).toString();
  let rejected = "accepted"; try { Temporal.PlainDate.from({ year: 2026, month: 2, day: 30 }, { overflow: "reject" }); } catch (e) { rejected = (e as Error).name; }
  R.rejected = rejected;
  R.json = JSON.stringify({ d: Temporal.PlainDate.from("2026-06-15") });
  expect(R.jan31).toBe("2026-02-28");
  await_write();
});
function await_write() { require("fs").writeFileSync(process.env.OUT_JSON!, JSON.stringify(R)); }
'''


@card(K("2174-typescript-plugin/7945-typescript-temporal"))
def typescript_temporal(task, wd):
    wd = Path(wd)
    proj = wd / "proj"
    tw(proj / "dates.test.ts", TEMPORAL_TEST)
    jw(proj / "package.json", {"name": "dates", "version": "0.0.0", "private": True})
    out = wd / "temporal_results.json"
    rc, o = _bun(["test"], proj, wd, env={"TZ": "America/New_York", "OUT_JSON": str(out)})
    if not out.exists():
        raise RuntimeError(o[-400:])
    R = json.loads(out.read_text())
    return [
        check("bun test passes with TZ=America/New_York", rc == 0, rc, 0),
        check("today() seam: Helsinki date at the instant", R["today"] == "2026-01-15", R["today"]),
        check("negative control: UTC slicing gives yesterday", R["utcSlice"] == "2026-01-14", R["utcSlice"]),
        check("negative control: legacy Date reads 2026-06-15 as the 14th west of UTC; PlainDate keeps 15",
              R["legacyDateGetDate"] == 14 and R["plain"] == 15, [R["legacyDateGetDate"], R["plain"]]),
        check("known answers: Feb 28 days, Jan31+1mo, 7.25 h, Sunday=7",
              [R["feb"], R["jan31"], R["hours"], R["dow"]] == [28, "2026-02-28", 7.25, 7], [R["feb"], R["jan31"], R["hours"], R["dow"]]),
        check("validation: impossible string throws, bag clamps, overflow reject throws",
              R["impossible"] == "RangeError" and R["clamped"] == "2026-02-28" and R["rejected"] == "RangeError",
              [R["impossible"], R["clamped"], R["rejected"]]),
        check("ISO string round-trip through JSON", R["json"] == '{"d":"2026-06-15"}', R["json"]),
    ], [out, proj / "dates.test.ts"]


# ───────────────────────────── spec-superflow: spec merger and spec writer ─────────────────────────────

def _reqs(md, header="## Requirements"):
    """Return ordered {name: block} under a header; block includes its scenarios."""
    m = re.search(r"(?ms)^%s\s*\n(.*?)(?=^## |\Z)" % re.escape(header), md)
    if not m:
        return None
    out = {}
    for part in re.split(r"(?m)^(?=### Requirement: )", m.group(1)):
        h = re.match(r"### Requirement: (.+)", part)
        if h:
            out[h.group(1).strip()] = part.strip()
    return out


def _render_main(purpose, reqs):
    return "# Spec\n\n## Purpose\n%s\n\n## Requirements\n\n%s\n" % (purpose, "\n\n".join(reqs.values()))


def _merge(main_md, delta_md):
    """Apply ADDED/MODIFIED/REMOVED/RENAMED; validate before writing; idempotent no-ops; near matches fail."""
    errors, ops = [], {"ADDED": 0, "MODIFIED": 0, "REMOVED": 0, "RENAMED": 0, "noop": 0}
    if main_md is None:
        purpose = (re.search(r"(?ms)^## Purpose\s*\n(.*?)(?=^## |\Z)", delta_md) or [None, ""])[1].strip() or "Default purpose."
        reqs = {}
    else:
        if re.search(r"(?m)^## (ADDED|MODIFIED|REMOVED|RENAMED) Requirements", main_md):
            return None, ops, ["baseline contains delta headers: rejected"]
        purpose = re.search(r"(?ms)^## Purpose\s*\n(.*?)(?=^## |\Z)", main_md).group(1).strip()
        reqs = _reqs(main_md) or {}

    def near(name):
        return [k for k in reqs if k != name and re.sub(r"\s+", " ", k).lower() == re.sub(r"\s+", " ", name).lower()]
    for name, block in (_reqs(delta_md, "## ADDED Requirements") or {}).items():
        if name in reqs:
            if reqs[name] == block:
                ops["noop"] += 1
            else:
                errors.append("ADDED %s already exists with different content" % name)
            continue
        reqs[name] = block
        ops["ADDED"] += 1
    for name, block in (_reqs(delta_md, "## MODIFIED Requirements") or {}).items():
        if name not in reqs:
            errors.append(("MODIFIED near-match %r" % near(name)) if near(name) else "MODIFIED missing %s" % name)
            continue
        if reqs[name] == block:
            ops["noop"] += 1
        else:
            reqs[name] = block
            ops["MODIFIED"] += 1
    rem = re.search(r"(?ms)^## REMOVED Requirements\s*\n(.*?)(?=^## |\Z)", delta_md)
    for name in (re.findall(r"### Requirement: (.+)", rem.group(1)) if rem else []):
        name = name.strip()
        if name in reqs:
            del reqs[name]
            ops["REMOVED"] += 1
        elif near(name):
            errors.append("REMOVED near-match %r" % near(name))
        else:
            ops["noop"] += 1
    ren = re.search(r"(?ms)^## RENAMED Requirements\s*\n(.*?)(?=^## |\Z)", delta_md)
    for old, new in (re.findall(r"- FROM: `?(.+?)`?\s*\n\s*- TO: `?(.+?)`?\s*$", ren.group(1), re.M) if ren else []):
        if new in reqs and old not in reqs:
            ops["noop"] += 1
            continue
        if new in reqs:
            errors.append("RENAMED target %s collides" % new)
            continue
        if old not in reqs:
            errors.append("RENAMED missing %s" % old)
            continue
        reqs = {(new if k == old else k): (v.replace("### Requirement: " + old, "### Requirement: " + new, 1) if k == old else v)
                for k, v in reqs.items()}
        ops["RENAMED"] += 1
    if errors:
        return None, ops, errors
    out = _render_main(purpose, reqs)
    if re.search(r"(?m)^## (ADDED|MODIFIED|REMOVED|RENAMED)", out) or "## Requirements" not in out:
        return None, ops, ["candidate failed validation"]
    return out, ops, []


def _req(name, shall, when, then):
    return "### Requirement: %s\nThe system SHALL %s.\n\n#### Scenario: %s\n- **WHEN** %s\n- **THEN** %s" % (name, shall, name.lower(), when, then)


@card(K("2200-spec-superflow/8210-spec-merger"))
def spec_merger(task, wd):
    wd = Path(wd)
    main = _render_main("Authenticate users.", {
        "Login": _req("Login", "accept valid credentials", "valid password", "a session is issued"),
        "Lockout": _req("Lockout", "lock after 5 failures", "5 failures", "the account is locked"),
        "Legacy SSO": _req("Legacy SSO", "support SAML 1", "SAML 1 assertion", "login succeeds")})
    delta = ("## ADDED Requirements\n\n" + _req("MFA", "require a TOTP code", "password ok", "a TOTP prompt is shown") +
             "\n\n## MODIFIED Requirements\n\n" + _req("Lockout", "lock after 3 failures", "3 failures", "the account is locked") +
             "\n\n## REMOVED Requirements\n\n### Requirement: Legacy SSO\n\n## RENAMED Requirements\n\n- FROM: `Login`\n- TO: `Password Login`\n")
    root = wd / "specs/auth"
    tw(root / "spec.md", main)
    change = tw(wd / "changes/add-mfa/specs/auth/spec.md", delta)
    state = jw(wd / "changes/add-mfa/state.json", {"state": "executing"})
    if json.loads(state.read_text())["state"] != "executing":
        raise RuntimeError("guard")
    merged, ops, errs = _merge(main, delta)
    (root / "spec.md").write_text(merged)
    again, ops2, errs2 = _merge(merged, delta)             # re-sync: every op already reflected
    near_delta = "## MODIFIED Requirements\n\n" + _req("lockout ", "x", "y", "z")
    bad, _, errs3 = _merge(merged, near_delta)
    coll = "## RENAMED Requirements\n\n- FROM: `MFA`\n- TO: `Lockout`\n"
    bad2, _, errs4 = _merge(merged, coll)
    bad3, _, errs5 = _merge(delta, delta)                  # a delta-only baseline must be rejected
    names = list(_reqs(merged))
    receipt = jw(wd / "changes/add-mfa/publication_receipt.json", {"delta_sha256": hashlib.sha256(delta.encode()).hexdigest(),
                                                                   "baseline_sha256": hashlib.sha256(merged.encode()).hexdigest(),
                                                                   "ops": ops})
    return [
        check("one op of each kind applied", ops == {"ADDED": 1, "MODIFIED": 1, "REMOVED": 1, "RENAMED": 1, "noop": 0}, ops),
        check("published baseline has exactly the merged requirements", names == ["Password Login", "Lockout", "MFA"]
              and "lock after 3 failures" in merged and "SAML" not in merged, names),
        check("re-sync is an idempotent no-op with identical output", again == merged and ops2["noop"] == 4 and errs2 == [], ops2),
        check("negative control: near-match name and rename collision fail without writing", bad is None and bad2 is None
              and "near-match" in errs3[0] and "collides" in errs4[0], [errs3, errs4]),
        check("delta-only baseline rejected; delta file kept", bad3 is None and change.exists(), errs5),
    ], [root / "spec.md", receipt]


VAGUE = re.compile(r"\b(TBD|TODO|better|robust|efficient)\b", re.I)


def _validate_pack(d):
    d = Path(d)
    f = []
    prop = (d / "proposal.md").read_text()
    why = re.search(r"(?ms)^## Why\s*\n(.*?)(?=^## |\Z)", prop)
    if not why or len(why.group(1).strip()) <= 50:
        f.append("proposal: Why <= 50 chars")
    for h in ("## What Changes", "## Scope", "## Impact"):
        if h not in prop:
            f.append("proposal: missing " + h)
    if not re.search(r"(?i)\bIn:", prop) or not re.search(r"(?i)\bOut:", prop):
        f.append("proposal: scope lacks In/Out")
    req_names = []
    for sp in sorted((d / "specs").rglob("spec.md")):
        t = sp.read_text()
        if not re.search(r"(?m)^## (ADDED|MODIFIED|REMOVED) Requirements", t):
            f.append("specs: no delta header")
        for name, block in (_reqs(t, "## ADDED Requirements") or {}).items():
            req_names.append(name)
            if not re.search(r"\b(SHALL|MUST)\b", block):
                f.append("specs: %s lacks SHALL/MUST" % name)
            if "#### Scenario:" not in block or "WHEN" not in block or "THEN" not in block:
                f.append("specs: %s lacks WHEN/THEN scenario" % name)
    des = (d / "design.md").read_text()
    if "## Decisions" not in des or not all(k in des for k in ("Choice", "Rationale", "Alternatives", "Consequences")):
        f.append("design: decision lacks Choice/Rationale/Alternatives/Consequences")
    if "## Goals" not in des or "Non-goals" not in des:
        f.append("design: goals/non-goals")
    tasks = (d / "tasks.md").read_text()
    boxes = re.findall(r"(?m)^- \[ \] (\d+)\. (.+)$", tasks)
    if not boxes:
        f.append("tasks: no checkbox tasks")
    for n, t in boxes:
        if "`" not in t or "->" not in t or "evidence:" not in t:
            f.append("tasks: %s lacks path/outcome/evidence" % n)
    for r in req_names:
        if r not in tasks:
            f.append("tasks: requirement %s unmapped" % r)
    for name in ("proposal.md", "design.md", "tasks.md"):
        if VAGUE.search((d / name).read_text()):
            f.append("%s: placeholder or empty adjective" % name)
    return f


def _write_pack(d, cfg):
    d = Path(d)
    if not cfg.get("dp_0_confirmed"):
        return None
    reqs = cfg["requirements"]
    tw(d / "proposal.md", "# Proposal: %s\n\n## Why\n%s\n\n## What Changes\n%s\n\n## Scope\nIn: %s\nOut: %s\n\n## Impact\n%s\n\n"
       "## Proof of completion\n%s\n" % (cfg["title"], cfg["problem"], cfg["change"], cfg["in"], cfg["out"], cfg["impact"], cfg["proof"]))
    tw(d / "specs" / cfg["capability"] / "spec.md", "## ADDED Requirements\n\n" + "\n\n".join(
        _req(r["name"], r["shall"], r["when"], r["then"]) for r in reqs) + "\n")
    tw(d / "design.md", "# Design\n\n## Facts and constraints\n%s\n\n## Goals\n%s\n\nNon-goals: %s\n\n## Decisions\n"
       "- Choice: %s\n- Rationale: %s\n- Alternatives: %s\n- Consequences: %s\n\n## Risks and verification\n%s\n" % (
           cfg["facts"], cfg["goal"], cfg["out"], *cfg["decision"], cfg["risk"]))
    tw(d / "tasks.md", "# Tasks\n\n## Delivery / proof map\n%s\n\n%s\n" % (
        "\n".join("- %s -> task %d" % (r["name"], i + 1) for i, r in enumerate(reqs)),
        "\n".join("- [ ] %d. %s: `%s` -> %s (evidence: `%s`)%s" % (i + 1, r["name"], r["path"], r["then"], r["evidence"],
                                                                     "" if i == 0 else " depends on %d" % i) for i, r in enumerate(reqs))))
    return d


@card(K("2200-spec-superflow/8211-spec-writer"))
def spec_writer(task, wd):
    wd = Path(wd)
    cfg = {"dp_0_confirmed": True, "title": "CSV export", "capability": "export",
           "problem": "Support receives 40 tickets a month because reports can only be copied from the HTML table by hand.",
           "change": "Add a CSV download for the monthly report.", "in": "monthly report CSV", "out": "XLSX, scheduled emails",
           "impact": "reports service, report page", "proof": "pytest tests/test_export.py passes; manual download opens in a spreadsheet",
           "facts": "Report rows come from ReportQuery; max 50k rows.", "goal": "One-click CSV of the current filter.",
           "decision": ("stream rows with csv.writer", "bounded memory for 50k rows", "build in memory; client-side export",
                        "no total row in the file"), "risk": "Excel locale separators; verified by test with ';' locale fixture.",
           "requirements": [
               {"name": "CSV download", "shall": "return the filtered report as text/csv", "when": "the user clicks Download CSV",
                "then": "a file with one row per report row is returned", "path": "reports/export.py", "evidence": "pytest tests/test_export.py"},
               {"name": "Header row", "shall": "write column titles as the first row", "when": "a CSV is generated",
                "then": "row 1 equals the visible column titles", "path": "reports/export.py", "evidence": "pytest -k header"}]}
    pack = _write_pack(wd / "changes/csv-export", cfg)
    good = _validate_pack(pack)
    weak = wd / "changes/weak"
    tw(weak / "proposal.md", "# P\n\n## Why\nMake it better.\n\n## What Changes\nTBD\n")
    tw(weak / "specs/x/spec.md", "## ADDED Requirements\n\n### Requirement: Export\nIt should export.\n")
    tw(weak / "design.md", "# Design\n\nWe will see.\n")
    tw(weak / "tasks.md", "# Tasks\n1. do it\n")
    bad = _validate_pack(weak)
    stopped = _write_pack(wd / "changes/unconfirmed", dict(cfg, dp_0_confirmed=False))
    rep = jw(wd / "spec_pack_validation.json", {"good": good, "weak": bad, "unconfirmed_dp0_written": stopped is not None})
    return [
        check("generated pack passes every checklist item", good == [], good, []),
        check("negative control: weak pack fails on Why, scenarios, SHALL, decisions, tasks and placeholders",
              len(bad) >= 8 and any("SHALL" in x for x in bad) and any("scenario" in x for x in bad)
              and any("placeholder" in x for x in bad), bad),
        check("DP-0 not confirmed: nothing written", stopped is None and not (wd / "changes/unconfirmed").exists()),
        check("every requirement mapped to a checkbox task", all(r["name"] in (pack / "tasks.md").read_text() for r in cfg["requirements"])),
    ], [rep, pack / "tasks.md"]


# ───────────────────────────── honest gaps ─────────────────────────────

_DIALOGUE = ("its deliverable is a turn-by-turn dialogue in which the person settles each decision; there is no deterministic "
             "procedure to run without the person's turns (a scripted 'answer' would fake the protocol)")
GAPS.update({
    K("1989-epharmoge/7149-contextualize"): "dialogical protocol: " + _DIALOGUE,
    K("1991-euporia/7159-elicit"): "dialogical protocol: " + _DIALOGUE,
    K("1993-horismos/7161-bound"): "dialogical protocol: " + _DIALOGUE,
    K("1996-katalepsis/7164-grasp"): "dialogical protocol: " + _DIALOGUE,
    K("1990-epistemic-cooperative/7150-gate-check"): "needs an independent external advisor model (codex) as adjudicator; "
                                                     "a second pass by this program would void the independence the skill exists for",
    K("1990-epistemic-cooperative/7157-white-bear"): "semantic audit: deciding whether a prohibition is load-bearing (the rewrite test) is "
                                                    "a meaning-level LLM judgment; a regex would report safety boundaries as findings",
    K("1990-epistemic-cooperative/7158-zero-shot"): "semantic audit: telling anchoring examples from scope-delineating or reliability "
                                                   "examples is a meaning-level LLM judgment, not a lexical rule",
    K("2160-migration-patterns-plugin/7801-eslint-to-biome"): "Biome is not installed and cannot be fetched offline; the migration's proof "
                                                             "(biome migrate / biome check accepting the config) cannot run here",
    K("2160-migration-patterns-plugin/7803-mypy-to-ty"): "ty is not installed and cannot be fetched offline; the cutover must be proven "
                                                        "by running ty check against the mypy baseline",
    K("2166-python-plugin/7853-ty-type-checking"): "ty (Astral type checker) is not installed and cannot be fetched offline",
    K("2166-python-plugin/7861-vulture-dead-code"): "vulture and deadcode are not installed and cannot be fetched offline",
    K("2174-typescript-plugin/7928-biome-tooling"): "Biome is not installed and cannot be fetched offline",
    K("2174-typescript-plugin/7935-bun-outdated"): "bun outdated compares installed versions with the npm registry; needs network",
    K("2209-majestic-founder/8267-company-values"): "needs the founder's real decision episodes and judgment; the output is a "
                                                    "qualitative synthesis with no known answer to measure",
    K("2209-majestic-founder/8276-operating-priorities"): "needs the leader's real calendar, stage and bottlenecks plus a judgment "
                                                         "conversation; no deterministic known answer",
    K("2209-majestic-founder/8277-strategic-plan-review"): "qualitative review of a real business plan under a posture the owner "
                                                          "selects; no deterministic known answer",
})
