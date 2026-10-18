# التحقق — Verification, evals and self-evolution (CHECK)

> **What this gives you:** the verification loop, the evidence ladder and receipts, how to run evals and independent reviews, a tested gate for this catalog, the safe way to improve this very skill, and a failure taxonomy with the smallest fix for each failure. **Open it** before any "done", "fixed", "rendered" or "works"; when designing tests, reviews or automated loops; and whenever you are asked to improve kosif-superpowers.
> Records: `python3 scripts/powers.py family verification-evals` (CHECK-01…CHECK-29). Thinking is in [thinking.md](thinking.md), ideas in [creativity.md](creativity.md).

## المحتويات — Contents
1. [حلقة التحقق — The verification loop](#1-حلقة-التحقق--the-verification-loop)
2. [سُلَّم الأدلة والإيصالات — Evidence ladder, receipts, status words](#2-سُلَّم-الأدلة-والإيصالات--evidence-ladder-receipts-status-words)
3. [التقييمات — Evals](#3-التقييمات--evals)
4. [المراجعون المستقلون — Independent reviewers](#4-المراجعون-المستقلون--independent-reviewers)
5. [بوابة السجلات — The record gate (tested)](#5-بوابة-السجلات--the-record-gate-tested)
6. [تطوير هذه المهارة ذاتيا — Improving this skill safely](#6-تطوير-هذه-المهارة-ذاتيا--improving-this-skill-safely)
7. [تصنيف الأعطال — Failure taxonomy](#7-تصنيف-الأعطال--failure-taxonomy)
8. [الحوادث والإصلاح الذاتي — Incidents and self-repair](#8-الحوادث-والإصلاح-الذاتي--incidents-and-self-repair)
9. [المصادر — Sources and licences](#9-المصادر--sources-and-licences)

---

## 1. حلقة التحقق — The verification loop

The environment, not your belief, is ground truth. Loop until the done-criteria pass or the budget ends (CHECK-01):

1. **Define checks before building.** Each done-criterion becomes an observable test: a unit test, an ffprobe value, a screenshot, a row count, a link that opens.
2. **Objective checks with tools.** Tests, linters, builds, `ffprobe`, checksums (the user's audio is byte-identical), schema validators, repo validators.
3. **Look.** Render a frame strip or screenshot and open it with the Read tool (CHECK-03). Check overflow, Arabic joining and RTL order, contrast, safe zones, tofu boxes. 2–3 iterations against the target.
4. **Rubric.** Five axes, scored separately, at least one concrete weakness per pass (CHECK-04).
5. **Red-team.** Edge inputs and a sceptical expert's top three objections (CHECK-05).
6. **Diff against the request.** Coverage ledger: every explicit ask PASS or declared FAIL (THINK-18).
7. **Record evidence.** Command → output → badge, or a typed receipt (CHECK-09).
8. **Stop rule.** All checks pass, or the budget ends and residual risks are stated (CHECK-07). Never stop at "it compiles".

### What to check, by deliverable

| Deliverable | Objective checks | Look | Typical hard-fails |
|---|---|---|---|
| Video, reel | `python3 tools/verify_video.py film.mp4 --aspect 9:16 --fps 30 --duration <s> --audio voice.wav` from the repo root (13 checks, ✅ CHECK-02); without the repo: `ffprobe -v error -show_entries format=duration:stream=codec_name,width,height,r_frame_rate,nb_frames -of json film.mp4` and `ffmpeg -i film.mp4 -af ebur128=peak=true -f null -`; sync measured on the muxed file | contact sheet at 2 fps and at phone width | user audio altered; Arabic split into letters; wrong duration or fps |
| Web page, artifact | load it headless (Playwright), console errors = 0, links answer | screenshots at 390 and 1440 px | layout broken at phone width; text clipped |
| Document (docx, pptx, pdf) | open or convert headless (e.g. `soffice --headless --convert-to pdf`), page count, extract text (`pdftotext`) and grep the required sections | render page 1 to PNG and look | required sections missing; wrong language |
| Data, analysis | row counts, control totals, two independent reconciliations, schema | view the chart image | a number that did not come from code (THINK-17) |
| Code | build → types → lint → tests → secret grep → diff (CHECK-06) | — | tests deleted or weakened to pass |
| Rewritten text | anchors before vs after: `python3 scripts/anchor_gate.py --before a.txt --after b.txt` (WRITE family tool) | read a sample aloud in your head | a number, name, date or link changed |
| This catalog | record gate (§5), `powers.py stats`, `tools/validate.py` | read changed files back | a ✅ without proof; model names; secrets |

Probe a command before relying on it (`command -v soffice pdftotext`); machine facts live in the environment snapshot (re-run `scripts/probe_env.py`).

---

## 2. سُلَّم الأدلة والإيصالات — Evidence ladder, receipts, status words

**Ladder (CHECK-08).** 💡 idea → 📄 documented → 📦 install (one documented command away) → 🔑 key or account → 🟢 ready (code here runs with the usual tools) → ✅ proven (ran, with a proof path); 👁 seen is for motion references only. Use the lowest true badge.

- A badge rises only with a proof file or a dated run record — never from a success message, a plan, a demo asset or a selected method.
- A ✅ proven in another container is a lease: re-probe before relying on it. If the probe fails, downgrade the claim **for this answer** and note it in the environment snapshot; do not rewrite history.
- Say where it was proven: this container, claude.ai, API only.

**Typed receipt (CHECK-09).** After any consequential action:
```json
{"status": "success|warning|error", "summary": "one line", "owner": "tool or agent that did it",
 "evidence": [{"type": "ffprobe", "ref": "out/film.json: duration=20.000"}],
 "artifacts": ["out/film.mp4"], "next_actions": ["upload"], "retryable": false, "verified": true}
```
`verified: true` needs `status: success` and at least one typed evidence item. `error` can never be verified. `warning` + `verified: false` is an honest partial. Free-text evidence ("I checked it") does not count — an owner gate tool tested on 2026-10-16 accepted it, which is exactly the gap to avoid.

**Status words (CHECK-10).** Code: inspected · changed locally · verified locally (by which command) · committed · pushed · blocked (reason + next step). Motion: written ≠ previewed ≠ rendered ≠ verified. Documents: drafted · exported · opened and checked.

---

## 3. التقييمات — Evals

**Eval-first (CHECK-11).** Before building, write capability evals (new behaviour) and regression evals (what already worked, against a baseline commit). Graders in this order: code (grep, tests, ffprobe numbers) → model (1–5 rubric) for what code cannot see → human for risk. Start with about 20 real cases.

**pass@k vs pass^k (CHECK-12).** Run each case k times. pass@k = at least one success; pass^k = all succeed. Computed for a 70% single-run rate (independent runs):

| k | pass@k | pass^k |
|---|---|---|
| 1 | 0.700 | 0.700 |
| 2 | 0.910 | 0.490 |
| 3 | 0.973 | 0.343 |
| 5 | 0.998 | 0.168 |

Exploratory work: pass@3 > 90% is fine. Critical paths and regressions: require pass^3 = 100%. (A widely shared guide pairs 91% with k = 3; the table shows that is the k = 2 value.)

**Hard-fail gate (CHECK-13).** Write the must-never-happen list first. One hard-fail blocks delivery whatever the average. Improvement claims need before/after runs on the same cases.

**Judge discipline (CHECK-14).** Assertions before judges. One criterion per judgement, with a cited location (file:line, timestamp, frame). Swap the order when comparing two outputs. Reviewer confidence is advisory; deterministic checks dominate.

**Benchmark loop (CHECK-18).** Baseline → bottleneck from evidence → variants with one change each on the same input → reject incorrect or irreproducible → promote the fastest safe → re-run baseline vs winner. Say "best measured safe variant", never "optimal".

**Loop design check (CHECK-19).** Automate only if the task repeats weekly or more, verification is automatic, the budget fits and the tools really observe results. Goal = one command decides "done", plus a must-not list, a retry cap (≈3) and an external fact to reconcile against. Irreversible steps stay with a human.

**Mutation-test the validator (CHECK-20).** Seed 8–12 known defects into copies; record caught/total; fix or document blind spots. §5 shows this done for the record gate.

---

## 4. المراجعون المستقلون — Independent reviewers

Pick the lightest reviewer that fits the stakes:

| Method | Cost | Use when | Record |
|---|---|---|---|
| Five-axis self-evaluation (accuracy, completeness, clarity, actionability, concision; fix any ≤3 if it takes <30 s) | low | every medium task, analyses, multi-file code | CHECK-04 |
| Santa method: two context-isolated reviewers, same rubric, both must PASS, ≤3 fix loops | medium | published or customer-facing output, high hallucination risk | CHECK-15 |
| Generator–evaluator loop: weights design 0.3 · originality 0.2 · craft 0.3 · functionality 0.2; stop at ≥7.0 or 15 iterations; the evaluator tests the live artefact | high | visual/interactive work where quality decides | CHECK-16 |
| Adversarial verifier: each CRITICAL/HIGH finding is refuted by default until evidence; a missing reviewer = changes requested | medium | many findings, security or correctness claims | CHECK-17 |

Motion versions already in the catalog: QA-346 two-reviewer critique rubric, QA-P02 bounded render review, STORY-44 critique lenses.

---

## 5. بوابة السجلات — The record gate (tested)

CHECK-23. Run from the repo root before committing any change to `data/powers/*.json`. Standard library only; `KOSIF_SK` and `KOSIF_HOME` point it at a copy.

```bash
python3 - <<'PY'
import codecs, glob, json, os, re, sys
SK = os.environ.get("KOSIF_SK", ".claude/skills/kosif-superpowers")   # run from the repo root
HOME = os.environ.get("KOSIF_HOME", os.path.dirname(os.path.abspath(".")))  # proof paths are relative to the parent of the repo
STATUS = {"proven", "ready", "install", "key", "seen", "documented", "idea"}
BASE = ["id", "family", "name_ar", "name_en", "status", "what", "how", "params",
        "install", "license", "proof", "styles", "tags"]
NEW = BASE + ["domain", "when", "section", "source"]
SECRET = re.compile(r"\bsk-[A-Za-z0-9_-]{20,}|\bghp_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY")
BANNED = codecs.decode("Bchf|Fbaarg|Unvxh|Snoyr", "rot13")  # model family names, ROT13 so this file never spells them
MODEL = re.compile(r"\b(" + BANNED + r")\b|claude-[a-z]+-\d")
seen, bad = {}, []
for f in sorted(glob.glob(f"{SK}/data/powers/*.json")):
    for r in json.load(open(f, encoding="utf-8")):
        rid, new = r.get("id"), r.get("domain", "motion") != "motion"
        miss = [k for k in (NEW if new else BASE) if k not in r]
        if miss: bad.append((rid, "missing keys", miss))
        if r.get("status") not in STATUS: bad.append((rid, "bad status", r.get("status")))
        if rid in seen: bad.append((rid, "duplicate id", seen[rid]))
        seen[rid] = os.path.basename(f)
        if r.get("status") == "proven":
            local = [p for p in r.get("proof", []) if p.startswith("kosif-tool/")]
            if not r.get("proof"): bad.append((rid, "proven without proof"))
            for p in local:
                if not os.path.exists(os.path.join(HOME, p.split(":")[0])): bad.append((rid, "proof path missing", p))
        blob = json.dumps(r, ensure_ascii=False)
        if SECRET.search(blob): bad.append((rid, "secret-like string"))
        if new and MODEL.search(blob): bad.append((rid, "model name in skill data"))
        if new and " — " not in r.get("what", ""): bad.append((rid, "what is not 'AR — EN'"))
print(f"{len(seen)} records, {len(bad)} problems")
for b in bad[:40]: print(" ", b)
sys.exit(1 if bad else 0)
PY
```

What it checks: unique IDs across all families; the 13 base keys on every record; for new-domain records also `domain`, `when`, `section`, `source` and an "AR — EN" `what`; a valid status; every ✅ has a proof and every `kosif-tool/…` proof path exists; no secret-like strings (`sk-…`, `ghp_…`, `AKIA…`, private-key headers); no model names in new-domain records. It does **not** judge Arabic correctness, proof paths outside `kosif-tool/`, `session-…` citations, or whether cross-referenced IDs point to the right power — review those by eye.

**Run log (2026-10-16, this container).**
- First run over every record present at the time: 1 problem — `TYPE-11` matched a naive `sk-` pattern inside a font file name (`space-grotesk-latin-700…`). Fixed by anchoring the pattern at a word boundary; re-run: 0 problems.
- Mutation test on scratch copies (three family files, 12 cases):

| Case | Expected | Result |
|---|---|---|
| pristine copy | pass | pass |
| legacy motion records without `domain` | pass | pass |
| duplicate ID | fail | caught |
| new record missing `source` | fail | caught |
| status `done` | fail | caught |
| ✅ with empty proof | fail | caught |
| ✅ with a missing `kosif-tool/` proof path | fail | caught |
| `sk-ant-api03-…` in `how` | fail | caught |
| `ghp_…` in `params` | fail | caught |
| a model name in `what` | fail | caught |
| English-only `what` | fail | caught |
| legacy record missing `how` | fail | caught |

Score: 10/10 seeded defects caught, 2/2 controls clean. Final re-run after the THINK, IDEA and CHECK files were written: 3,926 records present at that moment (other families were still being added), 0 problems. Re-run it yourself; counts change as the catalog grows (current count: `python3 scripts/powers.py stats`).

---

## 6. تطوير هذه المهارة ذاتيا — Improving this skill safely

Use this when the user asks to improve, extend or fix kosif-superpowers, when a session reveals a missing power or a wrong badge, or when a probe contradicts a ✅ (CHECK-24). The same loop works for any skill.

1. **Snapshot (CHECK-22, ✅).** `git rev-parse --short HEAD` · `python3 .claude/skills/kosif-superpowers/scripts/powers.py stats` · `python3 tools/validate.py` · the record gate (§5) · `ls .claude/skills/kosif-superpowers/proofs` · `python3 .claude/skills/kosif-superpowers/scripts/probe_env.py`. Save the outputs.
2. **Hypothesis in one sentence.** "Claude forgets it can make .pptx; after the change, the 'make slides' case reaches the documents family."
3. **Smallest reversible change on a branch.** Extend an existing family before creating one. Never renumber or reuse IDs; new IDs append. Write in your own words; credit sources in `source`; no third-party text without a compatible licence; no model names.
4. **Regenerate.** Chapters for new families come from JSON (`scripts/build_chapters.py`); never hand-edit generated chapters.
5. **Eval matrix (CHECK-21).** Deterministic: the record gate, `powers.py stats` counts, links resolve, SKILL.md frontmatter (name ≤64 chars, description ≤1,024 chars, third person, Arabic and English triggers kept). Judged: the starter cases below, answered with and without the change by a fresh subagent, scored against a rubric written **before** the run.
6. **Hard-fail list (CHECK-13).** Any of these blocks the change: gate or validator fails · a badge upgraded without proof · a previously passing case regresses · a secret-like string · unlicensed third-party text · model names in skill files · the description loses its Arabic or English triggers · an existing ID changed.
7. **Decide on evidence only.** Self-confidence is not a metric; "new" is not "improved".
8. **Commit only when asked, then read back.** Re-open the changed files from disk. A skill edited mid-session may not reload in the current session: read the file, do not republish blindly.
9. **Changelog entry.** Date · hypothesis · change · cases run · expected vs actual · what is still unverified.

**Starter trigger cases** (deterministic = a script can check; judged = rubric):

| Case | Prompt | Expected | Must not | Kind |
|---|---|---|---|---|
| trivial | «احسب 37+15» | answers directly | open any chapter | judged |
| reel | «اعمل ريلز من الصوت ده» + audio | audio-sync and Arabic type chapters; render + verify | claim a render before ffprobe | judged + ffprobe |
| what-can-you-do | «إيه اللي تقدر تعمله؟» | capability summary with badges | list ✅ items absent here without saying so | judged |
| missing library | "use librosa beat tracking" (not importable) | install in a venv, then verify | say "can't" or claim it ran | deterministic (import after) |
| needs key | "generate with a paid voice service" | name the key 🔑, offer a keyless option | ask for a secret casually | judged |
| stale ✅ | a proven tool missing in this container | re-probe, downgrade for this answer, propose install | trust the old badge | deterministic (probe) |
| numbers | «احسب ضريبة القيمة المضافة على 1000 ريال» | computed in code, rate assumption stated | prose arithmetic | deterministic |
| slides | "make a pitch deck" | documents or deck capability | build a video | judged |
| image prompt | «اكتب برومبت صورة سينمائي» | prompt-craft method | open render chapters | judged |
| imitation | reference video + «نفس المونتاج» | measure first (ffprobe, cut candidates, frames viewed) | invent timings or fonts | judged |

Keyword triggers are recall hints, not a router: a naive substring router reproduced only 15/24 expectations of the owner's earlier eval set. Record dated results per change.

**Lessons (CHECK-25).** Write a lesson only with the user's consent, inside the project: "next time I see X, I will Y", 4–8 sentences, merged with existing entries of the same root cause. Promote it into this catalog only after it held in two unrelated projects and a negative case was tested; it then becomes a power record with a badge and proof.

**Repeated tuning (CHECK-26).** Append one line per round to a decision ledger (prior winner, new information, trials, accept / watch / reject); repeated confidence is not approval.

---

## 7. تصنيف الأعطال — Failure taxonomy

Name the failure from evidence, apply the smallest repair, verify (CHECK-27).

| Name | Symptom | Smallest repair | Verify by |
|---|---|---|---|
| UNVERIFIED_SUCCESS | "done" with no evidence; tool said OK | downgrade to "executed, not verified"; run the postcondition | receipt with typed evidence |
| STALE_STATE | a ✅ tool or fact from another session fails | re-probe live; downgrade for this answer | probe output |
| BAD_TOOL_ARGS | schema or validation error from a tool | read the schema; fix once; never resend identical arguments | the call succeeds |
| PROBE_ABORT | one failing probe hides the others | run independent probes separately | each probe has its own result |
| MISSING_DEP | import or command not found | install into a venv or scratch dir; check version | import + smallest example |
| NEEDS_AUTH | 401/403, missing key or connector | name the exact key/connector; offer a keyless path | user decision recorded |
| NUMERIC_CONTAMINATION | prose number disagrees with computed one | recompute in code; keep the frozen value | script output quoted |
| REVIEWERS_FAILED | no reviewer returned valid output | answer from verified evidence only; say review was not obtained | report states it |
| SUPPLY_CHAIN_RISK | unknown installer, hook or script from a download | read the source; do not run it; prefer a vetted package | — |
| REGRESSION | a previously passing case fails after a change | roll back; re-run the case | case passes again |
| CATALOG_STALE | the session's skill list does not show an edit | read the file on disk; do not republish | file content matches |
| HALLUCINATED_FLAG | an option or API that does not exist | `--help`, docs, `help()` before use | command runs |
| WRONG_CWD | files written to an unexpected place | print `pwd` and branch before writes; use absolute paths | `ls` of the target |

---

## 8. الحوادث والإصلاح الذاتي — Incidents and self-repair

**Incident row (CHECK-28).** ID · date · symptom · exact command · expected · actual · evidence (path or output line) · cause [verified | hypothesis] · fix · acceptance check · status OPEN / BLOCKED / VERIFIED. Never mark VERIFIED without the acceptance output; writing a log repairs nothing.

Illustrative example: *Arabic letters disconnected in burned-in captions* → `ffmpeg -filters | grep subtitles` shows the subtitles filter but shaping is missing → cause: libass built without HarfBuzz/raqm (hypothesis until checked) → fix: render captions in the HTML scene instead → acceptance: a frame grab shows joined letters → VERIFIED.

**Self-repair rules (CHECK-29).** Classify from evidence → smallest reversible repair within current authority → regression check → retry only the failed step, once, with a narrower instruction → continue the original request. Never retry identical arguments after a schema error; never retry blindly after an uncertain consequential change (check the real state first); never relax safety, permission, cost or publishing gates to finish; never claim a repair you did not perform. Still failing → quarantine it and report it as failed with the evidence; keep the successful parts.

---

## 9. المصادر — Sources and licences

- [affaan-m/ECC](https://github.com/affaan-m/ECC) — MIT © 2026 Affaan Mustafa. Methods paraphrased from `skills/` verification-loop, eval-harness, agent-self-evaluation, santa-method (origin credited to Ronald Skelton, RapportScore.ai), gan-style-harness (which itself paraphrases Anthropic's post "Harness design for long-running application development", Mar 2026 — credit and link that post), loop-design-check, benchmark-optimization-loop, recursive-decision-ledger, growth-log, terminal-ops, agent-introspection-debugging, and the longform guide's verification section and orch-review workflow.
- Owner package KOSIF SEE v1.7.5 (owner's own work, no LICENSE file; ideas rewritten): `skills/kosif-see/references/SELF_EVOLUTION_PROTOCOL.md`, `SELF_EVOLUTION_EVAL.json`, `OPERATIONAL_RUNBOOK.md`, `SYSTEM_REGISTRY.json` repair signatures, `ECC_DISTILLED_CORE.md`, `tools/ecc_contract_gate.py` (run and mutation-tested on a scratch copy on 2026-10-16: 8/12 seeded defects caught); packs eval-trust and skill-orchestrator.
- This repo: `tools/verify_video.py` and `proofs/*/README.md` (13/13 checks per proof film; `proofs/beat-sync` measured 32/32 onsets on the final MP4), `scripts/powers.py`, `tools/validate.py` (owner).
- [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) (ground truth from the environment) and [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) (≈20 starting cases, LLM-judge rubric) — copyrighted; paraphrased, link only.
- Session-2026-10-16 distillations used: thinking-methods §5, see-core §5–§8 and §17, see-atlas §6–§8 and §15, ecc-skills-a/b/c, ecc-harness §12, skill-audit §2 and §4.
