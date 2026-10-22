"""USIP protocol structure: a lean core, appendices reachable by trigger, one version, one meaning per plan letter.

Deterministic and read-only (stdlib unittest). The cheap subset also runs as the 'protocol' check of
scripts/check_skill.py; this file adds per-assertion detail, the fusionforge.py command and required-flag check, and
the v5.2 text-retention check (H01/H02 in A9): every sentence and table cell of the v5.2 PROTOCOL.md must still be in
the core, an appendix or the CHANGELOG, or be replaced by a named v5.3 text listed in V52_REPLACED with its reason.
After a deliberate edit of retained text, see which v5.2 units it touched (needs the git history):

    python3 .claude/skills/kosif-superpowers/evals/test_protocol_structure.py --retention-report

    python3 -m unittest discover -s .claude/skills/kosif-superpowers/evals -p 'test_protocol_structure.py' -v
"""
import hashlib
import re
import subprocess
import sys
import unittest
import urllib.parse
from collections import Counter
from pathlib import Path

SK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SK / "scripts"))
import check_skill as C  # noqa: E402

EXPECTED_VERSION = "5.3"
CORE = C.PROTO_CORE
SESSION = SK / "SESSION_PROMPT.md"
SKILL_MD = SK / "SKILL.md"
CLAUDE_MD = C.REPO / "CLAUDE.md"
FF = SK / "scripts" / "fusionforge.py"
SI = SK / "scripts" / "skill_intelligence.py"
FF_RE = re.compile(r"fusionforge\.py\s+([a-z][a-z-]*)")
FLAG_RE = re.compile(r"(?<![\w-])--[a-z][a-z-]*")


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def protocol_files():
    return C.protocol_files()


def appendices():
    return [f for f in protocol_files() if f != CORE]


def phase_text(n: int) -> str:
    core = read(CORE)
    title = next(t for _lv, t, _i in C.md_headings(core) if t.startswith(f"المرحلة {n} —"))
    return C.md_section(core, title)


def quoted_commands(text: str):
    """[(line_no, sub, flags)] for every 'fusionforge.py <sub> …' mention. A mention ends at the next mention, at the
    end of the inline code span it sits in, or at the end of the line."""
    out, fence = [], False
    for no, line in enumerate(text.split("\n"), 1):
        if re.match(r"^\s{0,3}(```|~~~)", line):
            fence = not fence
            continue
        hits = list(FF_RE.finditer(line))
        for k, m in enumerate(hits):
            end = hits[k + 1].start() if k + 1 < len(hits) else len(line)
            if not fence and line[:m.start()].count("`") % 2 == 1:  # inside an inline code span
                close = line.find("`", m.end())
                end = min(end, close if close >= 0 else len(line))
            out.append((no, m.group(1), FLAG_RE.findall(line[m.end():end])))
    return out


def command_files():
    return protocol_files() + [SESSION, SKILL_MD] + ([CLAUDE_MD] if CLAUDE_MD.is_file() else [])


def required_flags(help_text: str) -> set:
    """Flags outside [...] in an argparse usage block (the text before the first blank line)."""
    usage = help_text.split("\n\n", 1)[0]
    prev = None
    while prev != usage:
        prev, usage = usage, re.sub(r"\[[^\[\]]*\]", "", usage)
    return set(FLAG_RE.findall(usage))


# ------------------------------------------------------------------ v5.2 text retention
# A "unit" is one sentence of a paragraph or list item (wrapped lines joined), one table cell (header rows skipped) or
# one line of a code block, with every "(v5.3: …)" note removed and whitespace, '*' and '`' dropped. V52_UNITS holds the
# sha256[:8] of every v5.2 unit of 12+ characters, per old section ID (the CHANGELOG map's IDs; the contents list and the
# paste block were rewritten and are not included). The v5.3 side adds, for each table row, "first cell + cell" units,
# so a v5.2 cell "R02 @kosif see فقط" matches the merged A9 row "| R02 | … | @kosif see فقط |".
V52_COMMIT = "bf910be"
V52_PATH = ".claude/skills/kosif-superpowers/PROTOCOL.md"
UNIT_MIN = 12
_LINE_START = re.compile(r"^(#{1,6} |\s*[-*] |\s*\d+\. |>|\|)")
_SENTENCE_END = re.compile(r"(?<=[.!?؟؛])\s+")
_TABLE_SEP = re.compile(r"^\|?[\s:|-]+\|[\s:|-]*$")


def strip_v53(text: str) -> str:
    """Text without its "(v5.3: …)" notes (balanced parentheses)."""
    out, i = [], 0
    while True:
        j = text.find("(v5.3:", i)
        if j < 0:
            return "".join(out) + text[i:]
        out.append(text[i:j])
        depth, k = 0, j
        while k < len(text):
            depth += {"(": 1, ")": -1}.get(text[k], 0)
            if depth == 0:
                break
            k += 1
        i = k + 1


def unit_norm(s: str) -> str:
    return re.sub(r"[\s*`]", "", s).strip(".؛،:;,")


def unit_hash(norm: str) -> str:
    return hashlib.sha256(norm.encode("utf-8")).hexdigest()[:8]


def logical_lines(text: str) -> list:
    """[(kind, line)]: kind is 'code' for a line inside a fence, else 'text'; wrapped prose lines are joined."""
    out, fence = [], None
    for raw in text.split("\n"):
        m = re.match(r"^\s{0,3}(```|~~~)", raw)
        if m:
            fence = None if fence == m.group(1) else (fence or m.group(1))
            out.append(None)
            continue
        line = raw.strip()
        if fence:
            out += [("code", line), None]
        elif not line:
            out.append(None)
        elif out and out[-1] is not None and out[-1][0] == "text" and not _LINE_START.match(raw) \
                and not out[-1][1].startswith(("#", "|")):
            out[-1] = ("text", out[-1][1] + " " + line)
        else:
            out.append(("text", line))
    return [x for x in out if x is not None and x[1]]


def units(text: str, row_keys: bool = False) -> list:
    """[(normalized, raw)] units of a Markdown text (see the comment above)."""
    lines, res = logical_lines(strip_v53(text)), []

    def add(raw):
        for sentence in _SENTENCE_END.split(raw):
            n = unit_norm(sentence)
            if len(n) >= UNIT_MIN:
                res.append((n, sentence.strip()))

    for k, (kind, ln) in enumerate(lines):
        if kind == "code":
            add(ln)
        elif ln.startswith("|"):
            if _TABLE_SEP.match(ln) or (k + 1 < len(lines) and _TABLE_SEP.match(lines[k + 1][1])):
                continue   # separator or header row
            cells = [c.strip() for c in re.split(r"(?<!\\)\|", ln.strip().strip("|"))]
            for c in cells:
                add(c)
            if row_keys and len(cells) > 1:
                for c in cells[1:]:
                    n = unit_norm(cells[0] + c)
                    if len(n) >= UNIT_MIN:
                        res.append((n, f"{cells[0]} {c}"))
        else:
            add(re.sub(r"^(#{1,6} |[-*] |\d+\. |> ?)", "", ln))
    return res


def retention_texts() -> dict:
    """{file name: text} of the core and the appendices A1-A11. The CHANGELOG does not count: it names old titles and
    quotes changed rules, which would hide a deletion."""
    return {f.name: read(f) for f in protocol_files() if f.name != "CHANGELOG.md"}


def v53_corpus(texts=None):
    """(unit hashes, whole normalized text) of the given texts (default: retention_texts())."""
    text = "\n\n".join((texts or retention_texts()).values())
    return {unit_hash(n) for n, _raw in units(text, row_keys=True)}, unit_norm(strip_v53(text).replace("|", " "))


def _alternatives(new):
    return new if isinstance(new, tuple) else (new,)


def retention_gaps(texts=None) -> list:
    """[(old section id, v5.2 unit hash, problem)] for v5.2 units the v5.3 texts no longer hold or replace."""
    have, flat = v53_corpus(texts)
    contained = {unit_hash(unit_norm(t)): t for t in V52_CONTAINED}
    replaced = {unit_hash(unit_norm(old)): new for old, new, _why in V52_REPLACED}
    gaps = []
    for sid, hashes in V52_UNITS.items():
        for h in hashes.split():
            if h in have:
                continue
            if h in contained:
                if unit_norm(contained[h]) not in flat:
                    gaps.append((sid, h, f"«{contained[h][:60]}» is no longer in the core or an appendix"))
            elif h in replaced:
                gone = [x for x in _alternatives(replaced[h]) if unit_norm(x) not in flat]
                if gone:
                    gaps.append((sid, h, f"its v5.3 replacement «{gone[0][:60]}» is gone"))
            else:
                gaps.append((sid, h, "missing (run this file with --retention-report to see its v5.2 text)"))
    return gaps


def v52_sections(text: str) -> dict:
    """{old section id: Markdown body} of the v5.2 PROTOCOL.md, keyed like the CHANGELOG map."""
    named = {"الفهرس / contents": "toc", "المستودع الأصل": "repo-origin", "الحلقة في شاشة واحدة": "loop",
             "الدور والقاعدة العليا": "priority", "مستوى البروتوكول": "levels", "دروس ميدانية": "field-lessons",
             "النسخة المختصرة": "paste"}
    out, sid = {}, "banner"
    for ln in text.split("\n"):
        m = re.match(r"^#{2,3} (.*)$", ln)
        if m:
            t = m.group(1)
            sm = re.match(r"^(-1\.\d+(?:\.[أب])?)\s", t)
            pm = re.match(r"^المرحلة (\d+) —", t)
            sid = (sm.group(1) if sm else "-1" if t.startswith("المرحلة -1 ") else f"Phase {pm.group(1)}" if pm
                   else next((v for k, v in named.items() if t.startswith(k)), t))
        out.setdefault(sid, []).append(ln)
    return {k: "\n".join(v) for k, v in out.items()}


def v52_text():
    """The v5.2 PROTOCOL.md from git history, or None in a shallow clone."""
    r = subprocess.run(["git", "show", f"{V52_COMMIT}:{V52_PATH}"], capture_output=True, text=True, cwd=str(C.REPO))
    return r.stdout if r.returncode == 0 and r.stdout else None


def retention_report() -> int:
    """Print every v5.2 unit the current files no longer hold, with its text (for maintainers; needs git history)."""
    old = v52_text()
    if old is None:
        print(f"git show {V52_COMMIT}:{V52_PATH} failed: run in a clone with history (git fetch --unshallow)")
        return 2
    raw_of = {unit_hash(n): raw for sid, body in v52_sections(old).items() if sid not in V52_SKIPPED for n, raw in units(body)}
    gaps = retention_gaps()
    for sid, h, problem in gaps:
        print(f"{sid}\t{h}\t{problem}\n\tv5.2: {raw_of.get(h, '?')}")
    have, flat = v53_corpus()
    fresh = {sid: [unit_hash(n) for n, _raw in units(body)] for sid, body in v52_sections(old).items() if sid not in V52_SKIPPED}
    if fresh != {sid: hs.split() for sid, hs in V52_UNITS.items()}:
        print("V52_UNITS differs from the units of the v5.2 file: the unit rules changed; regenerate the fixture")
    print(f"{len(gaps)} v5.2 unit(s) neither kept nor replaced by name")
    return 1 if gaps else 0


class CoreTests(unittest.TestCase):
    def test_core_exists_and_stays_lean(self):
        n = read(CORE).count("\n")
        self.assertLess(n, C.PROTO_MAX_LINES, "PROTOCOL.md is the always-read core: move conditional material to an appendix")
        self.assertGreater(n, 200, "the core lost its phases")

    def test_core_holds_the_required_sections_in_order(self):
        titles = [t for lv, t, _i in C.md_headings(read(CORE)) if lv == 2]
        want = ["الفهرس / contents", C.PROTO_TRIGGERS, "المستودع الأصل", "الحلقة في شاشة واحدة", "الدور والقاعدة العليا وترتيب الأولوية",
                "مستوى البروتوكول حسب حجم الطلب", "المسار القانوني الواحد / canonical pipeline"] + \
               [f"المرحلة {n} —" for n in range(12)] + [C.PROTO_GLOSSARY, "دروس ميدانية", C.PROTO_PASTE]
        pos = []
        for w in want:
            idx = [k for k, t in enumerate(titles) if t.startswith(w)]
            self.assertEqual(len(idx), 1, f"core section {w!r} must exist exactly once")
            pos.append(idx[0])
        self.assertEqual(pos, sorted(pos), "core sections are out of order")

    def test_one_priority_list_with_the_platform_tier_on_top(self):
        body = C.md_section(read(CORE), "الدور والقاعدة العليا وترتيب الأولوية")
        items = re.findall(r"^(\d+)\. ", body, re.M)
        self.assertEqual(items[:7], [str(i) for i in range(7)])
        self.assertIn("المنصة", body.split("\n0. ", 1)[1].split("\n", 1)[0])
        a1 = read(C.PROTO_DIR / "A1-see-thinking.md")
        self.assertIn("ترتيب الأولوية الوحيد صار في [النواة]", a1, "-1.1 item 4 must point to the single list")

    def test_fusionforge_is_wired_into_the_phases(self):
        hooks = {2: ["fusionforge.py reuse", "fusionforge.py propose", "--from-brief", "FUSE-"], 6: ["set-graph", "validate"],
                 7: ["FUSE-", "MEMORY_RUNTIME_UNAVAILABLE"], 8: ["fusionforge.py choose", "`D`", "--nodes"],
                 9: ["fusionforge.py trace", "--result", "fusionforge.py record", "--qa-pass", "fork", "fusionforge.py lessons"],
                 10: ["lessons", "export", "promote", "pending_human"]}
        for n, needles in hooks.items():
            text = phase_text(n)
            for s in needles:
                self.assertIn(s, text, f"Phase {n} lacks the FusionForge hook {s!r}")
        laws = phase_text(11)
        self.assertRegex(laws, r"\n25\. ")
        for s in ("verified", "promote", "قراءة الملف"):
            self.assertIn(s, laws.split("\n25. ", 1)[1])

    def test_glossary_rules_for_questions_replies_and_l0(self):
        gloss = C.md_section(read(CORE), C.PROTO_GLOSSARY)
        for s in ("داخل تقرير الخطط الواحد", "L0 بلا خطط ولا أسئلة", "`موافق` = نفّذ الخطة الموصى بها", "الإجابة المقترحة",
                  "candidate → planned → tested → verified | failed", "method_loaded ≠ executed ≠ verified", "PARTIALLY_VERIFIED",
                  "understand, research, plan, build, create, refine, assemble, verify, deliver"):
            self.assertIn(s, gloss)
        session = read(SESSION)
        for s in ("بلا خطط ولا أسئلة", "داخل تقرير الخطط", "`موافق` = نفّذ الخطة الموصى بها واقبل كل إجابة مقترحة"):
            self.assertIn(s, session)

    def test_a_money_or_sensitive_question_gets_only_the_safe_default(self):
        """-1.23 «ما له أثر مالي أو حساس لا يُفترض» survives «موافق accepts every suggested answer»."""
        gloss = C.md_section(read(CORE), C.PROTO_GLOSSARY)
        for s in ("لا يُفترض جوابه", "الخيار الآمن", "ولا يعتمد `موافق` غيرها", "القانون 17"):
            self.assertIn(s, gloss)
        for n in (5, 7, 8):
            self.assertRegex(phase_text(n), r"الأقل صرفًا|الخيار الآمن", f"Phase {n}")
        self.assertIn("الخيار الآمن", read(SESSION))
        self.assertIn("الخيار الآمن وحده", read(C.PROTO_DIR / "A1-see-thinking.md"))
        if CLAUDE_MD.is_file():
            self.assertIn("only the safe default", read(CLAUDE_MD))

    def test_a_brief_written_to_a_work_dir_creates_it_first(self):
        """brief --out writes into an existing folder: every entry point that quotes --out <dir>/brief.json says mkdir -p."""
        for f in (CORE, SESSION, SKILL_MD, CLAUDE_MD, SK / "scripts" / "boot.py"):
            if not f.is_file():
                continue
            text = read(f)
            if re.search(r"brief\s+\S.*--out\s+\S+/brief\.json", text):
                with self.subTest(file=f.name):
                    self.assertIn("mkdir -p", text)

    def test_verified_needs_a_baseline_the_engine_does_not_check(self):
        laws = phase_text(11).split("\n25. ", 1)[1]
        self.assertIn("--baseline", laws)
        self.assertIn("المحرك لا يفحصها", laws)
        a4 = read(C.PROTO_DIR / "A4-fusionforge-composition.md")
        self.assertIn("لا يشترطه", a4)
        self.assertNotIn("وخط الأساس بـ `--baseline`.)", a4, "the old note implied the engine enforces the baseline")

    def test_dated_snapshots_left_the_core(self):
        core = read(CORE)
        for s in ("0.39.26", "1.7.6", "fullProGateway", "expertCognitiveRoster"):
            self.assertNotIn(s, core, f"dated snapshot {s!r} belongs in A11")


class FileStructureTests(unittest.TestCase):
    def test_headings_unique_in_every_protocol_file(self):
        for f in protocol_files():
            dup = [t for t, c in Counter(t for _lv, t, _i in C.md_headings(read(f))).items() if c > 1]
            self.assertEqual(dup, [], f"{f.name}: duplicate headings")

    def test_contents_list_matches_heading_order(self):
        for f in protocol_files():
            text = read(f)
            with self.subTest(file=f.name):
                if text.count("\n") > C.PROTO_TOC_MIN_LINES:
                    self.assertRegex(text, C.TOC_RE, f"{f.name} needs a '## الفهرس / contents' list")
                self.assertIsNone(C.toc_problem(text))

    def test_every_appendix_starts_with_when_to_read_and_links_back(self):
        for f in appendices():
            head = read(f).split("\n## ", 1)[0]
            with self.subTest(file=f.name):
                self.assertIn("متى تقرأه / when to read", head)
                self.assertRegex(head, C.CORE_LINK_RE)

    def test_every_appendix_is_linked_from_the_trigger_table(self):
        table = C.md_section(read(CORE), C.PROTO_TRIGGERS)
        linked = {Path(urllib.parse.unquote(t).split("#")[0]).name for t in C.LINK_RE.findall(table)}
        self.assertEqual({f.name for f in appendices()} - linked, set())
        self.assertIn("CHANGELOG.md", linked)

    def test_links_and_anchors_resolve(self):
        for f in protocol_files():
            for target in C.LINK_RE.findall(C.strip_code(read(f))):
                if re.match(r"^(?:[a-z][a-z0-9+.-]*:|//)", target, re.I):
                    continue
                path, _, anchor = urllib.parse.unquote(target).partition("#")
                dest = (f.parent / path) if path else f
                with self.subTest(file=f.name, link=target):
                    self.assertTrue(dest.exists())
                    if anchor and dest.suffix == ".md":
                        self.assertIn(anchor, C.md_anchors(dest))

    def test_every_named_script_exists(self):
        for f in protocol_files():
            text = C.strip_fences(read(f))
            for name in sorted(set(re.findall(r"scripts/([A-Za-z0-9_][\w-]*\.py)", text))):
                with self.subTest(file=f.name, script=name):
                    self.assertTrue((SK / "scripts" / name).is_file(), f"{f.name} names scripts/{name}")
            for kind, name in sorted(set(C.NAMED_FILE_RE.findall(text))):
                base = SK if kind in ("scripts", "evals") else C.REPO
                with self.subTest(file=f.name, path=f"{kind}/{name}"):
                    self.assertTrue((base / kind / name).is_file())

    def test_old_sections_live_exactly_once(self):
        ids = Counter()
        for f in appendices():
            for _lv, t, _i in C.md_headings(read(f)):
                m = re.match(r"^(-1\.\d+(?:\.[أب])?) ", t)
                if m:
                    ids[m.group(1)] += 1
        want = [f"-1.{i}" for i in range(1, 49)] + ["-1.10.أ", "-1.10.ب"]
        for sid in want:
            self.assertEqual(ids[sid], 1, f"section {sid} must live in exactly one appendix")
        self.assertEqual(sum(1 for _lv, t, _i in C.md_headings(read(CORE)) if t.startswith("-1.")), 0, "no -1.x section in the core")

    def test_changelog_maps_every_old_section_to_an_existing_anchor(self):
        mp = C.changelog_map()
        self.assertEqual([i for i in C.PROTO_OLD_IDS if i not in mp], [])
        base = C.PROTO_DIR
        for sid, targets in mp.items():
            self.assertTrue(targets, f"{sid} has no link")
            for target in targets:
                path, _, anchor = urllib.parse.unquote(target).partition("#")
                dest = base / path
                with self.subTest(old=sid, link=target):
                    self.assertTrue(dest.is_file())
                    self.assertIn(anchor, C.md_anchors(dest))
            if sid.startswith("-1."):
                first = urllib.parse.unquote(targets[0]).partition("#")[2]
                self.assertTrue(first.startswith(C.gh_slug(sid + " ")), f"{sid} maps to {first!r}")
        log = read(base / "CHANGELOG.md")
        versions = [m.group(1) for m in re.finditer(r"^## v(\d+(?:\.\d+)*)", log, re.M)]
        self.assertEqual(versions[:6], ["5.3", "5.2", "5.1", "5.0", "4.2", "3.1"], "CHANGELOG is newest first")
        self.assertIn("2", versions)


class VersionAndMeaningTests(unittest.TestCase):
    def test_one_version_everywhere(self):
        self.assertEqual(C.protocol_version(), EXPECTED_VERSION, "PROTOCOL.md title")
        tag = f"USIP v{EXPECTED_VERSION}"
        self.assertIn(tag, C.md_section(read(CORE), C.PROTO_PASTE), "paste block")
        for f in (SESSION, SKILL_MD, CLAUDE_MD):
            if f == CLAUDE_MD and not f.is_file():
                continue
            with self.subTest(file=f.name):
                self.assertEqual(set(C.VERSION_RE.findall(read(f))), {EXPECTED_VERSION})
        for f in (SI, FF):
            with self.subTest(engine=f.name):
                self.assertIn(tag, C.module_doc(f), f"scripts/{f.name} docstring must name {tag}")
        for f in (SESSION, SKILL_MD, CLAUDE_MD):
            if f.is_file():
                self.assertNotIn("FusionForge v5", read(f), f"{f.name}: the engine is FusionForge v2")

    def test_plan_letters_have_one_meaning(self):
        gloss = C.md_section(read(CORE), C.PROTO_GLOSSARY)
        session = read(SESSION)
        for s in C.PLAN_AR:
            self.assertIn(s, gloss)
            self.assertIn(s, session)
        ff = read(FF)
        for s in C.PLAN_EN:
            self.assertIn(s, ff, "fusionforge.py plan labels")
            self.assertIn(s, gloss, "glossary English one-liners")
        phase6 = phase_text(6)
        for s in ("A — الذكية السريعة", "B — الاحترافية المتوازنة", "C — القصوى الابتكارية", "ليست B + إضافات"):
            self.assertIn(s, phase6)

    def test_retired_plan_wordings_are_gone(self):
        files = [f for f in protocol_files() if f.name != "CHANGELOG.md"] + [SESSION, SKILL_MD, FF] + ([CLAUDE_MD] if CLAUDE_MD.is_file() else [])
        for f in files:
            text = read(f)
            for s in C.PLAN_DRIFT:
                with self.subTest(file=f.name, wording=s):
                    self.assertNotIn(s, text)

    def test_check_skill_protocol_check_is_clean(self):
        errors = [m for lv, m in C.protocol_problems() if lv == "error"]
        self.assertEqual(errors, [])


class RetentionTests(unittest.TestCase):
    """H01/H02: nothing of v5.2 is lost silently (the CHANGELOG's «حُذف: لا شيء من الأحكام»)."""

    def test_fixture_covers_every_old_section(self):
        self.assertEqual(set(V52_UNITS) | set(V52_SKIPPED), set(C.PROTO_OLD_IDS))
        self.assertEqual(set(V52_UNITS) & set(V52_SKIPPED), set())
        v52 = {h for hs in V52_UNITS.values() for h in hs.split()}
        self.assertGreater(len(v52), 1500)
        for text in list(V52_CONTAINED) + [old for old, _new, _why in V52_REPLACED]:
            with self.subTest(unit=text[:50]):
                self.assertIn(unit_hash(unit_norm(text)), v52, "an allow-list entry that is not a v5.2 unit")
        for _old, _new, why in V52_REPLACED:
            self.assertRegex(why, r"^[^:]+: \S", "each replacement names its old section and why")

    def test_every_v52_sentence_is_kept_or_replaced_by_name(self):
        gaps = retention_gaps()
        self.assertEqual(gaps, [], f"{len(gaps)} v5.2 unit(s) lost; first: {gaps[:3]}")

    def test_a_deleted_section_body_or_law_is_caught(self):
        texts = retention_texts()
        a6, core = texts["A6-evidence-security-numbers.md"], texts["PROTOCOL.md"]
        start = a6.index("\n### -1.27 ")
        body_start = a6.index("\n\n", start) + 2
        body_end = a6.find("\n### ", body_start)
        texts["A6-evidence-security-numbers.md"] = a6[:body_start] + "(placeholder)\n" + (a6[body_end:] if body_end > 0 else "")
        texts["PROTOCOL.md"] = re.sub(r"(?m)^20\. .*$", "20. (removed)", core, count=1)
        lost = {sid for sid, _h, _p in retention_gaps(texts)}
        self.assertIn("-1.27", lost)
        self.assertIn("Phase 11", lost)

    def test_fixture_matches_the_v52_file(self):
        old = v52_text()
        if old is None:
            self.skipTest(f"no git history for {V52_COMMIT} (shallow clone): the fixture itself cannot be re-derived here")
        fresh = {sid: [unit_hash(n) for n, _raw in units(body)] for sid, body in v52_sections(old).items() if sid not in V52_SKIPPED}
        self.assertEqual(fresh, {sid: hs.split() for sid, hs in V52_UNITS.items()})


class FusionForgeCommandTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        def run(*args):
            return subprocess.run([sys.executable, str(FF), *args], capture_output=True, text=True, cwd=str(SK), timeout=60)
        main = run("--help")
        cls.main_rc = main.returncode
        m = re.search(r"\{([a-z,-]+)\}", main.stdout)
        cls.subs = set(m.group(1).split(",")) if m else set()
        cls.globals = set(FLAG_RE.findall(main.stdout.split("{", 1)[0])) | {"--help", "--json"}
        cls.help, cls.required = {}, {}
        if {"choose", "validate", "lessons", "reuse"} <= cls.subs:
            for s in cls.subs:
                out = run(s, "--help").stdout
                cls.help[s] = set(FLAG_RE.findall(out))
                cls.required[s] = required_flags(out)

    def test_every_quoted_command_parses(self):
        self.assertEqual(self.main_rc, 0, "scripts/fusionforge.py --help must exit 0")
        self.assertTrue(self.help, "scripts/fusionforge.py --help must list the FusionForge v2 subcommands (choose/validate/lessons/reuse)")
        seen = 0
        for f in command_files():
            for no, sub, flags in quoted_commands(read(f)):
                seen += 1
                with self.subTest(file=f.name, line=no, sub=sub):
                    self.assertIn(sub, self.subs, f"{f.name}:{no} quotes an unknown subcommand")
                    unknown = [x for x in flags if x not in self.help[sub] | self.globals]
                    self.assertEqual(unknown, [], f"{f.name}:{no} fusionforge.py {sub} has no such flag")
        self.assertGreater(seen, 20, "the docs should quote the FusionForge v2 commands")

    def test_quoted_command_forms_carry_their_required_flags(self):
        """A quote written as a command (it carries at least one flag) must run as written: every required flag is there.
        A bare name such as `fusionforge.py validate` is a reference, not a command form."""
        self.assertTrue(self.required, "no subcommand help to read the required flags from")
        self.assertTrue(self.required.get("trace", set()) >= {"--project", "--id", "--stage", "--action"}, self.required.get("trace"))
        for f in command_files():
            for no, sub, flags in quoted_commands(read(f)):
                if not flags or sub not in self.required:
                    continue
                with self.subTest(file=f.name, line=no, sub=sub):
                    missing = sorted(self.required[sub] - set(flags))
                    self.assertEqual(missing, [], f"{f.name}:{no} fusionforge.py {sub} lacks required flag(s)")

    def test_the_parser_sees_through_prose(self):
        cmds = quoted_commands('a `fusionforge.py choose --plan B --why "x"` then `--note` and fusionforge.py validate ثم fusionforge.py record --status tested')
        self.assertEqual(cmds, [(1, "choose", ["--plan", "--why"]), (1, "validate", []), (1, "record", ["--status"])])
        usage = "usage: fusionforge.py trace [-h] [--json] --project PROJECT --id ID\n   --stage {a,b} --action ACTION [--node NODE]\n   [--capabilities [CAPABILITIES ...]]\n\nappend"
        self.assertEqual(required_flags(usage), {"--project", "--id", "--stage", "--action"})


# ------------------------------------------------------------------ v5.2 retention fixture (data)
V52_SKIPPED = {
    "toc": "the v5.2 contents list: navigation, rebuilt from the v5.3 headings",
    "paste": "the paste block: rewritten for v5.3 as a summary of the core, whose phases hold its rules",
}

# sha256[:8] of every v5.2 unit, per old section ID (generated; see the comment above)
V52_UNITS = {
    "banner": ("9711434a 503d9c27 1f5cc2b6 274522ae 8bd00f0b "),
    "repo-origin": ("45386d70 deebd47b 28bf819c 07b42ea7 f4fffed0 9bc362b1 781ca57f 928d07e5 28819bd8 48832d93 261c6a3e "
                    "b18ecc95 97a7bbae f78ee6f9 0dc9a185 74c4dc32 46037d62 c4b66cbe 59e2d67d 431abdaa c95e751f 4bdb9a55 "),
    "loop": ("3cb1eb7e 8826f376 902a9c32 a9b468c6 cdc7e9cf f440d4e2 47f54675 096a9306 cd2f2ec3 77383bfb fcb65368 "
             "3f7eeacf b5207b00 44a130a7 "),
    "priority": ("a1fe6427 af2c881a 939dd949 d10fbe94 bb810e61 d80f3259 54a1702c 60ad52b1 d198a995 8bf0fbe8 8d315f34 "
                 "2f09f4a2 eabc10db a5ab5d35 decb670e 48832d93 b5a568cd d317c62a 6cf72655 f70874cc 61519935 f85ca129 "
                 "415f869e 90842bc9 f34543ea 4f956ca9 ce6ecc3d e4b39b05 8919e832 29737b08 e44a4fce 6f67bf3f 63436579 "
                 "43040d4d 71dc430f ee05f3dd fd37a51e 71e873f5 3cce0d1a "),
    "levels": ("20683601 0135083a 7e3c424b a8c7782c f9d9a0b5 29fed327 05a287a5 95d00170 2db299be b6845bb4 6f6e6b69 "
               "2f83e329 978250f4 62420e49 a48bacf0 c7b3645d 46deff0b 57c7050f bd55de24 5750f21f ec9833e4 58d4c0c4 "
               "3fcf2ffb 724f415d 10391f6c 27e0c1d2 d53b6982 0c3a91ae 9da06d7c 46d53663 32a5cd9b b9af45f3 70332515 "
               "750c9ead "),
    "-1": ("e007fd5c 8aeff1ff af194e75 8bf5d150 52de573c 32afbccb "),
    "-1.1": ("72e7619c e83d73ea 636504fa 3880c33c e48c152f fa96324c 5725406c 66e1f709 41303486 24795f21 813a3b9b "
             "1b895f6c 341ce2e7 cdbd1eca 6c76048d b74ea75a 80d227d6 a040d506 12030342 f8391e58 "),
    "-1.2": ("a4a73ff3 f84d5bf9 de09645d 78244aaf 61ccc352 225cdfaf b479b0b8 64ec7c95 fa393811 67ee3621 df0f923a "
             "65eda7e6 91304bbb 9747aab5 e3ba9ad5 428ce7bd ff260b95 325595ca df0be738 b5e73fdd d7b81e8d 7ef8244d "
             "7011e70f 7e02449e 4e93fc4b 11efbd7d 55dfbae6 b3e1eb28 3d708b7d 34aeea3a 316ae750 e4b7dfc5 6b6904d6 "
             "a2da2ccc 13d21006 "),
    "-1.3": ("7e0f8e21 a83c1933 d37adbd3 8c97be37 7def6f20 d3bdeffa c33810ab 107a9d94 40d00859 119f63fa 5e49cffa "
             "6f4fca29 b58859a7 6ca16d53 0f16e64f 6f5b7d5f ebdb7879 aa136e57 9d6d8c63 5cee70ff 7b8d21cb ae31a26b "
             "7ca15830 59dfe8b6 0d819418 8c4c6a58 8ca66fe5 fed0d7cf 21cb576c dcc3ec14 3f0c46dd e75ecc04 d6d16792 "
             "6efddbda 101fd181 0362fc8f "),
    "-1.4": ("161655a9 405727d0 fd2ffcba b56b00f9 19623879 4673d2c4 0bcfdc4d e290ae3e 228981d0 9c5c1e7f df169a70 "
             "75f8eedb 615c9f22 0cbc9a6d 78ab08ba f71cc822 bc6350c9 220d4ebe df82f78e bde02340 9548857f 43698ac6 "
             "4c4e9d0c 63193b6d 26cbd2fc d832dd66 88c8db75 1aac6b3f f37ff015 11af83c2 faa0c0d0 c913e851 2ef47009 "
             "bf4f2497 0c54a12a c9dd7337 cf122de4 3d322932 f1ed3d54 52581cd8 6277cf01 0418ce3a 96af4e38 058d2b22 "
             "8ae1daf7 "),
    "-1.5": ("585a05a9 6b925c6b 3dbab1a7 1219de43 bb3e6902 275cc92f 5a4d4b7c 618672d7 2ffcba5f 2d13e3ba 1cba71cd "
             "25d33984 bb836077 a100f0e0 d16c8dd0 371616be f77511da a540bcc3 "),
    "-1.6": ("d0cae756 f7507067 a62035e7 0913deaf 76636ad9 e17f164c 371c1dbb 395e4fa5 b1945cce 838a43ab 80531844 "
             "6d7020f3 dfac8a72 e9acfce0 48cf3754 83d82b92 8adc53ed dfbce971 c14f7dd4 9212addf "),
    "-1.7": ("364c67b7 d040967b fccc79c0 51dc46cc 354af48f 335c3842 4febffe6 13cc3aed 0c02702e bcd0b84b 959502ce "
             "abd3f8d5 085b3bb1 3ba88d74 "),
    "-1.8": ("6e081ad7 4d77545c f987410a da3e7b91 d39d332d 7986143b 55d043c3 991a199b d3acb0e7 487d454d 1dd936a5 "
             "0680284d 8e2290f9 c0ca3c93 d0e92d89 5ecb10da 7a43db78 76757ead b72a00fd e2dfc1ac 97e031c3 966f99bf "
             "8436a0a7 43767664 "),
    "-1.9": ("9f3765f7 2a5d51e1 028238dd f902561c 7faa32ae c1693384 dbf793d7 730465a2 af811da5 2ea2bc25 2462006a "
             "5ce3bd8b f817c533 5e4e6d4f 187ffdd4 "),
    "-1.10": ("d7c596fc 878d0d45 dcd09530 12aaa139 8843c768 a7361849 5f1931ae 1d427c40 7301048d a6bfd2c5 814ab6a2 "
              "23e521ce 48c5d679 97500fa9 e66854f7 "),
    "-1.10.أ": ("384a4f87 2fa8684a d18b1eda b6997b11 3fbf84d2 433edeae ad8fe23d 9abd7b7d 31e18f1d ea2ea0e3 2266648d "
                "02d751fe cc4a25c3 6f68387b "),
    "-1.10.ب": ("b65925a3 c6cdc75f c3fbaab4 dde3f935 ec86beb0 38cde986 8e083946 622fb108 9b75c2cb 9c059fe3 a603d53d "
                "8873d1b5 c6ac635f 5d9a9243 a9d5ab95 a6c0d6e5 44aa4c2c b7dd8d04 aadb3612 d5de40e6 78f80f84 edd07443 "
                "151fadeb 28b2b081 33a8d24f 24b1c2bb 24b45e9c 134d6b9a 3db5988b "),
    "-1.11": ("ada3c6db 4f326c86 7694dfd0 dd662529 afa6d1ef ac544a4d ddaa2f8a 3cd3c103 6eef43c1 f4624e3c e9e0fdbc "
              "b96555f1 80224722 7a0f07b2 fdea1e25 793c9fa0 789397bf d0e68246 9fa2ebe3 b32dc107 46b3a7e5 571960bc "
              "3c97c04f c62bd4f0 e8c8e29e 0c8100bf 865f7ef4 5eefae73 51741847 7f76473c ca301153 b28eb801 ef59be74 "
              "ad59668b acb78675 263d683b 6b160762 d864f7cf 71154c37 1920dbed 991a199b 3ccae0b8 0909a0eb c43fb8ab "
              "f4b30909 6aaf2088 7dc69097 ce688766 577b6220 78e9a320 c7beff92 8698efc9 a902f7ff e34a527f 37364ff3 "
              "520a953b 05271f2f 468c3001 "),
    "-1.12": ("89dcf600 f4e04be1 4cf9b01a c3c724e4 44ebfe8b 6d900d8a 21cfda0a 51de82c4 a33193ed 3b3e9555 7bbbf5c0 "
              "be96908d f077af3e 86ddccaa b42c6412 b6a35825 5ada033b d2665dfd ce113097 7ce5a406 7a242a19 5d7bf9e9 "
              "f0c40359 a6d6d204 "),
    "-1.13": ("77141a0f c503d16a 6ed82112 489b08f9 7b962b10 10318afb 27258f3a e248b93e 03b3ec9b 614d01c2 f0122bde "
              "99c6ca68 584c7abf a9d76169 798403ce 507aa08d 6cf65937 24f5dd57 41a1f302 64febf69 d6596fd0 b14f45f4 "
              "8af1d035 8399d514 "),
    "-1.14": ("040f3968 2ca4a795 25cc4f82 4bc9a9b2 ffc52521 bec379d8 06089669 1c702fc7 85feede5 c4006cea 3aa71c92 "
              "6bca7ff0 380a6133 6607caff 5209829e 712a80b1 892bb844 0c0fe423 909fbb1a 75cf956e dafd6195 ec7ed48a "
              "565d0a6d 31049bb6 9b30dddf ddfc071c 6537a900 8c10571e 8f899b00 f97e6e3d e965df3d ba4fd95f cbfa5e29 "
              "239000ce ed8c1e4a 27ba0b4d 851696fa "),
    "-1.15": ("bf88bd17 f5bddbe8 46c276a8 92e56a6b 762e2da8 a92eed0a 3b3da8f7 20f96058 58adc94c 81fd4036 df438842 "
              "9943ed8a d1d1151c 77145f00 a1bd1a85 4d7a9086 127ce663 006f7a7f f436f7ef 57d174b2 b56c3cea f22bdec8 "
              "dc97ea8e fac76c49 51bf04e2 23e993f8 7e7aab55 c9b202cc baed551c 702b6eb5 8f619c99 298fde5f 9fc82b4a "
              "33e995c4 "),
    "-1.16": ("890be64e 69c29edc 83c06cf6 92f00326 a58865de e5e40d5a a427b740 b7668682 8c65942f 94a0eb09 b368139a "
              "9b926a0a 40b5c747 d6341382 60678f93 2f2cdd01 4798bd53 64fe6692 1fb39339 cf446843 8987deb5 a2c90448 "
              "d1eb597e 3b71c61a 2a625e2e 058fb220 0898b0a3 732d0ebb bee4e8b7 c706a7b2 9eec3c8c 56e95942 31d1a2cf "
              "364f7a36 300e0a5e c06e5688 bba9ef75 5619c63d 85a25380 c0c82e2d 56123750 21968900 55d2fd91 4d5d6f6b "
              "a1f28fad e6944906 ef35676d a84ed8bf f3cd7286 9ab16ec0 95fb27a9 580d6076 e1be9851 53aaaf26 1bf0dc3d "
              "4e93c235 "),
    "-1.17": ("d666624d 66417ec2 045b58b6 7be1d163 20f6de97 50e1c198 626739cc a0cd3cbe "),
    "-1.18": ("fcd64771 4a457837 3eb16364 4363e818 d0220f51 3a2dfded 9826a07b d01af520 f98b83f9 fa16b20b ca84a87c "),
    "-1.19": ("85a4bf72 fefc7775 ca8ebef6 c5df965a 130cd812 a67408c8 2132d80e 31f096ce 74654ae7 ea55089d 6529920a "
              "58b38a1e 9837b97b 818672a8 b1cab58a 9faf1926 "),
    "-1.20": ("a231f47a c4f711c2 210311b2 d80ed391 4e7c2367 bcbf77d4 1101a9d8 ab2851db 8307f01f e8773cd7 d2e1dcc5 "
              "ce00b09e def66792 "),
    "-1.21": ("4cb99b14 c7e0ff37 0b80bb53 f6d7f9a9 edf28aea 430ab5ee ca151e70 c4cd0502 c589e9d4 080c5127 a66c988a "
              "0712a38f e8e789f7 0cc01f6c 79a08e7e 701d70bc a620534a 98a63303 "),
    "-1.22": ("d0f3bab5 7c85c432 e72bc00a fcce6d9d 14acac74 fc565925 274f9336 9f5f2210 0cd914b4 972c5b01 b6ac2fe5 "
              "ffdce553 da4460f0 a2928c59 12df4f26 af070062 51afd0f0 178461a8 c95bb254 2bd2ab46 dd69ff89 4d0e4225 "
              "b3ec669d 41af3755 "),
    "-1.23": ("48031680 7be45d2c 422215eb 79d2ae4c 73dc9e4b 4f0760f4 eda7edc4 5863b246 faa0357e 19dffef7 0c1ac340 "
              "466f5eb6 7ffd0498 3b0aac10 ca71da08 353f7917 109325bc "),
    "-1.24": ("c825382a 45d59d26 b584ac18 464344f7 77797d26 7991f5ee 75e2b672 e99fb2e2 463a2be3 6dc6583c "),
    "-1.25": ("5f447c12 5ae2671a 3db03197 0fb2cd9a aa3ea78c 04f3ed84 29e29452 0558f552 9f1f0723 "),
    "-1.26": ("268f0f5a 6fc9d994 4d544788 4d512fd8 36ce0ac9 13e0a422 032c2864 8e24b9db 63fe815e 36b55906 0921f6c5 "
              "617c9a8b c6b4a663 da6b0131 "),
    "-1.27": ("9e7330b5 83056d9d cbb4a477 7522cd51 ca4fe78a 2a2ec82f e81cd3bc d901db95 2f3c5444 "),
    "-1.28": ("52021a96 4ddbe1f5 b1d59edc c55d2b6d 7099d23a 98238765 21cfe870 2e97331b f2677569 9f2d4058 b062067b "
              "bffaa047 "),
    "-1.29": ("c539f865 55a56989 be2218f4 e41748a5 33a6098e 5517ddca e63b3e2b d4414c64 ec6822fe 38a5b4bb d5b3c6ac "
              "ae68a303 "),
    "-1.30": ("d3dbbcde c51e31b9 ee856a13 97b4e558 29d7bc32 cd604893 4ba1548c ceacbc3b 08506082 e178527f 31cec97f "
              "e9804634 "),
    "-1.31": ("c421c748 afbd9898 fee84d75 a4fc1ea2 4a76fb02 435838c7 bbb8e9ed 05cbb6e3 b30d28be e7d89719 48fb200b "
              "237723fc 2929bfcc 59e71a51 289a6e0f d2a99f13 0f789757 7eb80873 1098762c d2d339f4 952a3824 c4f1c9be "
              "7d20af74 b655472f 554aded7 8e481335 a9ab9e49 6c4f5bf9 e1a93fcb 85529bd3 "),
    "-1.32": ("d316ed80 b5cb0344 85620567 06fabf27 86b8596b fa7b397c 21f28741 f97c0656 22b492a6 fb4f9bc4 7fc7df9d "
              "81b414a6 3a2bb765 3d121212 443d3b51 170eded8 dd9ea0d5 6445a6bd a165e277 5e6e9d33 12233cf9 af59f579 "
              "497faef2 5add70dd 08a828aa b1079a41 35dfb1b7 3b4103f6 bd90afb5 6f6bcd5b c95dd3e6 cece1899 627d2cb0 "
              "13459cf2 8db7cd65 1011d0de 4a380915 7ebc3866 07bc0719 6a4f3675 8f6fe499 1a3819f6 1e47fe98 4d8660fe "
              "dcc92da1 c89db1ec bef10928 8d3eeb13 b7d5c79c 964ee9c9 090490d0 6ac9bd9d ec74100e ff95dc2e 168d5e1f "
              "2031b09b f19d9434 b1f69b4b 64ed7b29 67bcad06 e5ac41df df2b5f68 9b264590 fa550dd0 7f437b7a a00b1caf "
              "d8f05df0 e282725e c61ab657 "),
    "-1.33": ("71b634c1 1709dbc4 c331831b ecbc7cfe c1a2104f 355a0f9d e8790bec cf3f2763 3e6e7eb8 fe51117b 4ac338db "
              "31ee81e2 e1c0a1ff 53188e91 102e62b5 d08b75b2 2b4cada1 ed239a0d 384ea30d 700934a8 11fed0bc "),
    "-1.34": ("aefb90da adea23c9 3a6292e3 12a599b2 cb7b798b "),
    "-1.35": ("74e106cb aa12453e 2b143877 1b7ad493 bab7d5d1 9d96d925 3e315be0 ae3301bc 7b479c6a e2145a81 5d0182fc "
              "2dff855f 4d0820b9 d8becd62 1a3928f0 ae7faa3e 4645f9e9 "),
    "-1.36": ("9c822c94 3d3427a8 972fe6a1 e89b04e8 a85b4156 a2c88b50 d669dbe2 52e2d989 275c60b7 a7b961f1 07a461c9 "
              "80bf8207 df725805 664de52d 9cd04598 5be61b48 c8ae1908 c8ec6117 8482b7a7 3d51afc2 2ab6fdc9 "),
    "-1.37": ("11d479ef 9466999a 3752d5d2 edadeab6 fe282ef4 0753d34a d72c38f6 72083ac7 00cfd760 e63aa798 ba89ef61 "),
    "-1.38": ("e877f200 66bf57d9 3d988224 06384e23 b0757d98 56c19783 83657fbd c37dece9 98692340 5a9af6ad 62f59525 "
              "f36c44f3 18fc5283 a2664fc6 "),
    "-1.39": ("bfbe508d 3b041a48 3d44d37c 956861e4 edb9e3ca 5caedb89 3a09a410 6de40bc6 cf51c051 ffadaa67 5fb7473b "
              "4630f3ea 34649a52 ea704c0e 16b13002 7be59b8e 5d5a5b74 54b569bc 439dda22 "),
    "-1.40": ("42bafe2a 33cdda98 f35601a6 3638a52e 7eb95d46 a3224beb 9bca6800 01a52118 a5f27dab 991a199b 01975df7 "
              "a7556f2c e8ed491f c926e889 fb3053ce ed0027cc b8b8df7e 19d7d8ea d59278b6 6a299f1a 3c365b47 a32ccdee "
              "7fd316a9 a19bcc44 711a9f29 2dd59cd8 2d686a54 c0522b2e "),
    "-1.41": ("b89665a8 256fdf45 3420e5a8 51b9a8b4 ae3a991f a9b2d3a0 dcbf4453 5b737eea 19f4c608 557e4d44 76088eeb "
              "bcfbeee9 435483df 8cd2367b 5ad0b339 cf69a0b3 5c5747c4 3bbb1c3b "),
    "-1.42": ("9b031429 e8275dc7 be9a30b9 298b7fc9 de7c40bb 44f7d80d ff08b0d6 ee153f8e a0e56ece b2584b05 be63eacf "
              "22d68dda 9b651213 bc1d3090 dc18b9d2 a27183fe e63caba6 8c923c1f dec4a0aa f0e55147 cf91933a "),
    "-1.43": ("9f92fe7b 8fac28da 43953d8d 52b68673 93df0b38 029602f0 5ac02c86 2e001f46 ceb49c19 2f704138 77ae6c5d "
              "304dcaf7 8d225330 4bb8fe35 8678c442 5b0a1cf1 "),
    "-1.44": ("552a7a38 49c0feb0 41058c39 fe14ecf2 9cb5eb08 76ff5967 72a744a7 0c83d7d6 c4159f48 abb3262d "),
    "-1.45": ("2f31f313 6dca5151 21b25f1f 2345290c 4a365c81 b3760f2e 3bdfe883 825c2866 d64e5779 79813fa1 96bfd877 "
              "a100ad2d "),
    "-1.46": ("e1e3569f 0fcd5327 a4bc3e8e a1c86f7f 876ad31b 79064f75 e663060f "),
    "-1.47": ("39fd7a9a cbd503b7 a45f54fd 0c2df5d3 6ddb75bf cfc58f4e 69b8c45a 9d03378a 58a01057 e25748b6 67a0e73a "
              "1bc4c497 3fa13f1d bff4846d 307d0db0 7d54b8cc 5b8e553b 54d2f848 72ef031c b7a8ace8 512794f2 9f4c72e8 "
              "8a897453 04f3c71b e9f5439b cf345873 d67d9c69 f11c3691 13cca6b4 380e931b 7695cb3b f536537b 5cada33b "
              "3e5b60f2 0d5f7953 2d3db7d8 73ff221a 640331d3 8ccd0613 635aab68 83a531b2 42308ed8 f6a32062 1f9386f6 "
              "910c3e24 1c077b63 71e86aca a8cd5152 ae7c9572 d7b62891 af89003a 4c0f293f 460f685f 7edd2cce 394444ca "
              "73c075be ca3af434 2cc53862 82d3223c a5e3a110 74922c6e 58fb5e3a 9dfdfdea d7eb0a7f 60badfb8 ce8c390d "
              "7371809f f5f5d569 8084c545 6806a8c2 ef1855fd "),
    "-1.48": ("fc06a5ce 4f2d6569 509d2cdc f8ad0f3e 735dafe3 656d364b 767d11bb 1ccefd4e cfa2354c 5acfd8fc ca4496d0 "
              "84cddc88 59608c08 88710665 b1487ee7 "),
    "Phase 0": ("ed0f39d0 88e679a1 46dbae6f d8e60b35 89e1f7b7 55b91cb5 e378b0ab 5e4e802d 2886b03f e46711b7 42bd2497 "
                "b06a1f89 0c39c6b0 73ed15ec 8627b7ce 6a9fdf60 4fe7b070 c330fb23 2817c067 5e2355ac ef9a8fcb 3b9faf57 "
                "f83d3488 7a0dda40 "),
    "Phase 1": ("65b72984 fc953221 6bf2de0a d6e834c5 a70f71e5 84e0629a 9b75a213 59425ab4 65788428 cf7f113a 1a756b14 "
                "0db6d86f 56e5ee96 3b9bfc01 b123c4fe a8ad789b ded72169 fe312060 f1b138a8 cd63a581 288f0885 f15efbc0 "
                "f2eecfcd 7a825607 6f6f57ec 28d1a581 2d04f19d ffd04192 59b8c56c 7b84cba1 a0107012 9595ffd6 fa82fa03 "
                "7f2bf356 92055178 19af657d 61b60724 50e9b501 80ca0069 ba399ae9 43a4ca5f 1ec7ca3c 997d299b 0d91433d "
                "9bbf70cf bff2b41b "),
    "Phase 2": ("e1ad2a53 6d1d2ba3 464b3c8b fc180574 3e379996 4edcc8eb 4fc7af06 86854ef9 3c14be33 b4124a36 d3d095e3 "
                "a4df4163 29ebfec6 7f7b1fdc c271f3a1 8cc05dcf 57ca8cc4 d9ae9ad5 219fed2e b7a20ebf 781f6431 cf912aab "
                "fefea7bd dfb5edb2 0e096950 23755e3a 183d08e8 65e9b95e 943d9e59 d65a19a7 6418e2be 35903e1a ca422e1c "
                "49b48bd5 57c4b8dc 363a8caf 218d528b 0f1bab75 2e0144de 2edb3482 023ba6d7 5a06149a 0e84a745 467f5bb6 "
                "a793758d 9387b241 f6db867f 9ec912e0 ce78d7de 7caa0a70 098e351e cd63ff40 5c8db863 dde3f31d 5a242f50 "
                "921c13ac 0191b433 41b6e368 40acd667 b70b5031 e8201f4f 3803b023 a9866e54 36cbdfe5 406dfbd1 4a2ef7cf "
                "5a1be311 830d1976 b6b6d7f0 "),
    "Phase 3": ("c2ec1528 20d752ba f80b7504 f1b01e91 8f8a9991 87d59210 192e6f0c 6abf43b3 16435fac 289052dc 70de645e "
                "23479be5 a3a3da70 55378557 9ba48468 e027c46d f177d9a2 531e7c33 e27db171 2618de7b a5044a62 8f74f1b3 "
                "f53e600e c1adef39 73bf408c 152f6e7f "),
    "Phase 4": ("9265732c c6353d4a ebce993c 4b11a4b1 128f4a84 35394ea5 d883816d 4bd5520f 7bdbbfb7 d432a6ae fb2f6db1 "
                "d17dcd46 09936061 4b68db97 23a4e14c a7a8eece 0effcffd ce0a3bb8 9f82b42b "),
    "Phase 5": ("f1a29e94 b9898429 c5e7cebd 3e18c1a9 ea6c01f1 cbd25567 ab114496 6231b3b6 8d62762c 9d9cc9c6 6c83ab27 "
                "33af0a04 eebb4a19 67dc1832 eb7ea461 f06e52f1 d11a03e0 0e8bd720 ee7acf9d e5b5039a 1b6612a9 cbc7be70 "
                "683ddd9d c63b5d47 7285911a 6fa4c104 56094fed ee15ec39 0523a129 "),
    "Phase 6": ("0a69ed76 93349df3 6ca801dc a8e17a76 4f27da56 ac4663ef 814340cf 071730cf 242a144d ce42e1a9 de25e848 "
                "33c3f495 790f2e4f d30e52bb 7dfc58d3 4e71bb9d 013c234c d01f20a0 08cd7191 f7c5d179 d82b3ac3 4e890040 "
                "7f584bef da3688f8 bd51227f d855249d 86325c97 46164978 88139283 44740fac d0ddcf27 68e805c6 e6b026d4 "
                "727daf21 e29faf3a 4f5115ab 97f09a9f 490b8c26 f0e81f0d 0ce76827 bdec6590 04dc4a60 36d2e149 "),
    "Phase 7": ("955d721d 912e3829 e406eb76 c8612cb0 d5936247 6ca3d0f6 3fb22ab7 d8c3e21e 7d391041 d8055dfa ca0e3270 "
                "9ccc9fc1 f8eda29d 960c5c9c 81d1fca8 2a2980db 1c77ab88 7df6e439 0e83fcc5 bb3bb61a faec3e52 546cd55e "
                "0dd1687e b0e85bd0 675b5948 8ddfef87 6dc5287c c92acae9 95a686cb a83978bd 55b8b321 7472b31d ed1aa446 "
                "307d94e0 65731bfc "),
    "Phase 8": ("7caecbe1 64d23b27 383ef8f6 943dd31c 3c15a917 34377793 ddd0a062 b3ca65ac a2625bf0 fe6f3289 cb03bca2 "
                "6a32a444 c6d9f461 a55641b3 5d123205 f3cc72c8 c13da428 03fa133c fc7dcbaf 5533939e 26f65611 690a602e "),
    "Phase 9": ("fc6b6b0d 11345bb8 9b58451f eb04474b 0f0ddec9 ef814d4b 6b33c55c 42060662 a242e506 e3733dc0 2ab2b852 "
                "910b0ddf 01036e88 268c1e9e 0a449fcf a83a10b3 850100f5 4a5c1cd4 680b1e83 432cd2a8 7a38c7b3 38b1e7b2 "
                "0682ec9e 32f3c75d a10bce2a dc72f414 37ef08ff 040c00f5 a350d7b9 ff2f15a2 2b0825df "),
    "Phase 10": ("3553d78d 842f4422 9ef720b2 8947ce3d 83396c30 5b03c7b6 f739da9c e2695592 a1eb0bc2 dbf1a402 e055d74e "
                 "4d19e09d a028077a 1a8fc9ba 0589087c d4178ee7 3502596a b652effc bc408b30 b19f915d 947002a2 39401539 "),
    "Phase 11": ("8dc69752 c5c82adc d4e454e7 70ff6da9 6cb577b0 fffbad4f 4e74d5b3 d7e63a7e 103ba83e eb5e7974 f9a04728 "
                 "a953bf27 4997e0d4 4c93611e 276acf1d 90c0c960 a9ca2d1c 5916027d 29633d3f 758c7ab9 6bf9a97b f8922269 "
                 "2a0ff30f 49a2a4f1 2a901e54 eb6e7ba6 feb240ac 3a9caefc 8908144b 191142ed 1c430fbf a8f33f08 83495822 "
                 "e5cb6458 3579d2fa 308b6bbe a0b3ad14 439cf030 aa753bde 67af9258 1762df05 "),
    "field-lessons": ("1d6109db 52b8820f 42af76db 9db71b14 78aea9f8 d23e302e 3d980b2f d93db947 ddeb533d db4359ca 0be7b621 "
                      "8ee53c9c a5555a1c 752bb0c0 66b276b1 2280ef7e 89ce7c4d 0007e840 1968c560 7b578b4a aef22577 c7990276 "
                      "241e8e1a 4cf28c8e f05edaac 2095b7c5 13b6bbbb c7c332be 62bcbcf8 a4932797 99c392e4 d90e26df d40dcba9 "
                      "ec377b7e "),
}

# v5.2 units now inside a longer v5.3 sentence, or table cells now written as prose: checked as substrings
V52_CONTAINED = (
    "<https://github.com/kosif199022-jpg/kosif-tool/blob/main/.claude/skills/kosif-superpowers/PROTOCOL.md>",   # repo-origin
    "L0 يُجاب أو يُنفَّذ فورًا بلا `brief` ولا خطط.",   # loop
    "الحالية: القدرات والعائلات والأدوات من `boot.py`، والمجموعات من إيصال `verify`، والقدرات الخارقة من جرد `brief`، لا من هذه الصفحة):",   # priority
    "المجموعات (15)",   # priority
    "مجالات العمل الكبرى",   # priority
    "`scripts/smart_capabilities.py groups`",   # priority
    "العائلات (~60)",   # priority
    "ملف لكل عائلة، وكل عائلة داخل مجموعة",   # priority
    "`data/powers/<family>.json`",   # priority
    "القدرات الخارقة (~450)",   # priority
    "قدرات تؤدي العمل نفسه مدمجة مع توائمها وروابطها ومراحلها",   # priority
    "القدرات الذرية (~5,300)",   # priority
    "كل وصفة/طريقة بشارة دليل ومتطلبات",   # priority
    "الأدوات القابلة للتشغيل (~115)",   # priority
    "سكربتات تعمل فعلًا بأوامر جاهزة",   # priority
    "فهارس وصفية لملفاتي الخاصة (أولها أطلس الخطوط)",   # priority
    "قسم «مكتبات أصولك» في `brief`",   # priority
    "لا تخلط بين عدد القدرات وعدد الأدوات، ولا تعدّ مكتبات الأصول ضمن القدرات.",   # priority
    "المرحلة 0 كاملة والبروتوكول بالتقرير القياسي",   # levels
    "تبقى نقطة المراجعة في L3 وبوابات الإذن (القانون 17).",   # levels
    "مستوى البروتوكول (L0–L3) غير سلّم التفكير في `think.py ladder` (L0–L6)؛",   # levels
    "عند النشر راجع النسخ الحية.",   # -1.1
    "اسمح للمستخدم بجمعها في D.",   # -1.35
    "افحص في مسودته تسعة أشياء:",   # Phase 2
    "`brief` يحسب لكل قدرة خارقة مرشحة درجة بالأوزان المعلنة:",   # Phase 5
    "الملاءمة لهدفي",   # Phase 5
    "التكامل مع المرشحات الأخرى",   # Phase 5
    "إمكانية التنفيذ الآن (جاهزية الأعضاء والمتطلبات الحاضرة)",   # Phase 5
    "قوة الدليل (أفضل شارة)",   # Phase 5
    "التكلفة والوقت (متطلبات ناقصة ومفاتيح مدفوعة)",   # Phase 5
    "الإبداع (من خارج المجالين الأقرب)",   # Phase 5
    "إن كان الفرق بين الأولى والثانية 10 أو أقل، أو انقلب الفائز بتغيير وزن واحد ±1 (`robust = false`)، فالقرار متقارب: قل ذلك، واذكر العامل الحاسم، واسألني فقط إن كان ذوقًا أو ميزانية.",   # Phase 5
    "**L2 كامل:** 60 سطرًا مصدريًا على الأكثر، وخلية الجدول 12 كلمة على الأكثر: البطاقة ≤10 أسطر · الجرد ≤6 صفوف · جدول مقارنة واحد · خريطة التفاعل ≤3 أسطر · فكرتان عابرتان ≤ سطرين لكل منهما · سطر المناهج المستبعدة · تشريح مسبق ≤5 صفوف؛",   # Phase 7
    "**نتيجة الجرد:** إجمالي القدرات · ما فُحص (100% ✅ أو الفجوة) · المجموعات والعائلات المغطاة · القدرات ذات الصلة · قائمة الترشيح · ما قرأته بالتفصيل (ملفات: عدد + بطاقات CLI: عدد) · ما تعذر · الأدوات الجاهزة الآن · بصمة الكتالوج.",   # Phase 7
    "**جدول المقارنة:**",   # Phase 7
    "الفكرة الأساسية",   # Phase 7
    "المجموعات / القدرات الخارقة / القدرات / الأدوات",   # Phase 7
    "الوقت التقديري",   # Phase 7
    "التكلفة المحتملة",   # Phase 7
    "النتيجة المتوقعة",   # Phase 7
    "اعتمد اختياري بدل توصيتك",   # Phase 8
    "احفظ الأدلة والمصادر والملفات القابلة للتعديل.",   # Phase 9
    "الفهرس الدائم موجود ولا يُبنى من الصفر في كل مهمة:",   # Phase 10
    "المجموعات وتصنيف كل قدرة",   # Phase 10
    "`data/smart_capability_index.json`",   # Phase 10
    "`smart_capabilities.py build`",   # Phase 10
    "القدرات الخارقة والتوائم والروابط",   # Phase 10
    "`data/superpowers.json`",   # Phase 10
    "`superpower_fusion.py build`",   # Phase 10
    "خريطة المجموعات وخطط التثبيت",   # Phase 10
    "`kosif_hubs.py build`",   # Phase 10
    "المراحل وخرائط المهام وتدقيق التكرار",   # Phase 10
    "`data/capability_mindmap.json`",   # Phase 10
    "`capability_mindmap.py build`",   # Phase 10
)

# (v5.2 unit, the v5.3 text(s) that replace it, why): the replacement must stay in the core or an appendix
V52_REPLACED = (
    ("KOSIF SUPERPOWERS × KOSIF SEE — UNIVERSAL SKILL INTELLIGENCE PROTOCOL (USIP v5.2)",
     "UNIVERSAL SKILL INTELLIGENCE PROTOCOL (USIP v5.3)",
     "banner: the title carries the current version"),
    ("نصفه الآلي `scripts/skill_intelligence.py` (إيصال، ترشيح، مسودة خطط)، ونصفه العقلي هذه الصفحة (فهم، تنقيح، حكم).",
     "نصفه الآلي `scripts/skill_intelligence.py` (إيصال، ترشيح، مسودة خطط وأسئلة) و`scripts/fusionforge.py` (وصفة المشروع وسجل التجربة)، ونصفه العقلي هذه الصفحة",
     "banner: the machine half now names the questions and FusionForge"),
    ("**قاعدة v4:** استخدم `Stage0Card` الفكرية لـ KOSIF SEE قبل اختيار الأدوات؛",
     "**قاعدة SEE:** استخدم `Stage0Card` الفكرية قبل اختيار الأدوات؛",
     "loop: «قاعدة v4» renamed «قاعدة SEE» (CHANGELOG v5.3)"),
    ("**`brief`** بإيصال `complete = true`، ثم **نقّح مسودته**: المستوى، المتطلبات الضمنية، الأفكار العابرة، المخاطر، البوابات، الشارات.",
     ("**`brief`** بإيصال `complete = true`", "ثم **ثبّت المستوى** بقاعدة الحسم", "ثم **أكمل تنقيح المسودة**: المتطلبات الضمنية، الأفكار العابرة، المخاطر، البوابات، الشارات"),
     "loop: loop steps 4-5: the level is confirmed before the FusionForge recipe, the rest of the refinement after it"),
    ("**A/B/C مختلفة المنهج** بأعداد من مصدر واحد، وتوصية واحدة بعد تشريح مسبق.",
     "**A/B/C مختلفة المنهج** بمعاني [المسرد](#المسرد--glossary)، بأعداد من مصدر واحد، وتوصية واحدة بعد تشريح مسبق",
     "loop: the plan letters now point to the glossary"),
    ("**افحص التقرير قبل إرساله**، واختم بسؤال الموافقة، ثم **انتظر ردي**.",
     "افحصه قبل إرساله، واختم بسؤال الموافقة، ثم **انتظر ردي**",
     "loop: merged into loop step 9 (one report with the questions)"),
    ("**بعد الموافقة:** مراحل ببوابات فحص، وقياس كل معيار، وتقرير تسليم بالمقيس فعلًا.",
     "**بعد الموافقة:** `choose`، ثم مراحل ببوابات فحص و`trace` لكل عقدة، وقياس كل معيار، و`record`، وتقرير تسليم بالمقيس فعلًا",
     "loop: the FusionForge steps were added"),
    ("**ترتيب الأولوية عند التعارض** (الأعلى يغلب؛",
     "**ترتيب الأولوية عند التعارض** — القائمة الوحيدة (تحل محل البند 4 من -1.1)؛ الأعلى يغلب",
     "priority: one priority list (-1.1 item 4 folded in)"),
    ("اذكر أي تعارض في سطر مع المسار الذي اخترته):",
     "واذكر أي تعارض في سطر مع المسار الذي اخترته",
     "priority: same sentence, new punctuation"),
    ("به أتنازل عن خطوات الإجراء (الفحص الشامل، العرض، الانتظار)، لا عن البند 1.",
     "به أتنازل عن خطوات الإجراء (الفحص الشامل، العرض، الانتظار)، لا عن البندين 0 و1",
     "priority: the platform tier (item 0) was added above item 1"),
    ("مخرجات `brief` و`verify` الآلية (المستوى، الخطط، التوصية، أوامر الإصلاح): مسودة تنقّحها، لا حكم نهائي.",
     "مخرجات `brief` و`verify` و`fusionforge.py` الآلية (المستوى، الخطط، الأسئلة المقترحة، التوصية، أوامر الإصلاح): مسودة تنقّحها، لا حكم نهائي",
     "priority: fusionforge.py and the suggested questions are drafts too"),
    ("`scripts/superpower_fusion.py` · `references/superpowers.md`",
     "`scripts/superpower_fusion.py` و`references/superpowers.md`",
     "priority: the catalog-structure table became one paragraph"),
    ("`data/powers/*.json` · `scripts/powers.py`",
     "`data/powers/*.json` و`scripts/powers.py`",
     "priority: the catalog-structure table became one paragraph"),
    ("`scripts/hub.py` · `data/tools.json`",
     "`scripts/hub.py` و`data/tools.json`",
     "priority: the catalog-structure table became one paragraph"),
    ("لا خطط ولا سؤال موافقة.",
     "لا خطط ولا أسئلة ولا سؤال موافقة ولا وصفة",
     "levels: L0 also has no questions and no recipe (glossary)"),
    ("`brief` وحده، ثم شاشة واحدة: البطاقة + سطر لكل خطة + التوصية + سؤال الموافقة",
     "`brief` وحده، ثم شاشة واحدة: البطاقة + سطر لكل خطة + الأسئلة بإجاباتها المقترحة + التوصية + سؤال الموافقة",
     "levels: the questions with their suggested answers are part of the one report"),
    ("البروتوكول كاملًا، لكن التقرير شاشة واحدة؛",
     "البروتوكول كاملًا مع وصفة FusionForge، لكن التقرير شاشة واحدة",
     "levels: L2 includes the FusionForge recipe"),
    ("`brief` يقترح المستوى في حقل `level` بمطابقة الكلمات، فيخطئ في الاتجاهين: يرفع سؤالًا بلهجة («وش معنى…؟») أو «صلّح خطأ إملائي» إلى L1، ويخفض شعارًا أو ملفًا للتسليم إلى L1، بل يخفض طلب إنتاج أو نشر يبدأ بـ«اشرح» أو «لخص» أو «ترجم» إلى L0 فلا يطبع خططًا ولا سؤال موافقة.",
     "فقد يخفض شعارًا أو ملفًا للتسليم إلى L1، بل يخفض طلب إنتاج أو نشر يبدأ بـ«اشرح» أو «لخص» أو «ترجم» إلى L0 فلا يطبع خططًا ولا سؤال موافقة",
     "levels: the upward errors (a dialect question, a spelling fix) were fixed in the engine and are tested, as the v5.3 note there says; the downgrades stay"),
    ("**متابعة على مخرج معتمد** في الجلسة نفسها (غيّر اللون، قصّر المقدمة، بدّل الخط) لا تعيد البروتوكول: نفّذها ضمن الخطة المعتمدة وقل ذلك في سطر؛",
     "لا تعيد البروتوكول ولا تنشئ وصفة جديدة: نفّذها ضمن الخطة المعتمدة وقل ذلك في سطر",
     "levels: a follow-up also creates no new recipe"),
    ("المرحلة -1 — دمج KOSIF SEE: نواة التفكير والتخطيط والتوجيه (إلزامية قبل المرحلة 0)",
     "المرحلة -1 — دمج KOSIF SEE: نواة التفكير والتخطيط والتوجيه",
     "-1: «(إلزامية قبل المرحلة 0)» dropped: the lenses apply inside Phases 1-9 (A1 note); the session starts with boot.py"),
    ("عند اكتمال الحد الأدنى، اعرض ثلاث خطط **تختلف في المنهج**: A عملية سريعة، B توليفة ابتكارية، C أقصى نتيجة مناسبة للموارد المتاحة.",
     "A الذكية السريعة — أبسط مسار يحقق كل متطلب إلزامي، B الاحترافية المتوازنة — أفضل توازن مع تكاملات من مجالات أخرى، C القصوى الابتكارية — محرك أو مصدر أو طريقة تحقق مختلفة، ليست B + إضافات",
     "-1.23: -1.23 plan meanings corrected to Phase 6 (glossary)"),
    ("أنتج 3 توليفات A (قصيرة موثوقة)، B (مبتكرة بترابط بعيد)، C (طموحة مع بوابات جودة إضافية).",
     "A أبسط مسار يحقق كل متطلب إلزامي، B احترافية متوازنة بتكاملات من مجالات أخرى، C محرك أو مصدر أو طريقة تحقق مختلفة (ليست B + إضافات)",
     "-1.35: -1.35 plan meanings corrected to Phase 6 (glossary)"),
    ("مجلد out/ مستثنى من gitignore.",
     "مجلد out/ مُدرج في .gitignore فلا يُرفع إلى git",
     "-1.36: the old sentence said the opposite of the real .gitignore"),
    ("النسخ المرفقة v2/v3.1 وSESSION_PROMPT v4.2 تاريخية، ولا يجوز استبدال v5.1 بها.",
     "النسخ الأقدم في تاريخ git (v2 … v5.2) تاريخية، ولا يجوز استبدال النسخة الحالية (انظر عنوان النواة) بها",
     "-1.39: a general rule instead of naming attached files and v5.1"),
    ("لا تسألني إلا عن قرار يغير الخطة جذريًا.",
     "**الأسئلة:** ما يغيّر النتيجة يُكتب سؤالًا **داخل تقرير الخطط** (المرحلة 7) ومعه إجابة مقترحة",
     "Phase 1: one questions rule (glossary) replaces this v3.1 line and -1.23's «ask every question» (CHANGELOG v5.3)"),
    ("`skill_intelligence.py brief` يعطيك مسودة آلية: المستوى، المخرج الأساسي، القيود، الأصول التي لا تُستبدل، المتطلبات الإلزامية وجدول تغطيتها، وما استُبعد ولماذا؛",
     "المتطلبات الإلزامية وجدول تغطيتها، والأسئلة المقترحة بإجاباتها، وما استُبعد ولماذا",
     "Phase 1: brief now drafts the questions too"),
    ("mkdir -p out/<YYYYMMDD>-<اسم-قصير>                                                                                   # مجلد العمل (out/ مستثنى من git)؛",
     "# مجلد العمل (out/ مُدرج في .gitignore)؛ أنشئه قبل --out",
     "Phase 2: same command; the comment names .gitignore"),
    ("--out لا ينشئه",
     "أنشئه قبل --out",
     "Phase 2: worded so it stays true whether or not brief --out creates the folder"),
    ("اعرض تقريرًا منظمًا بميزانية طول (`brief` يطبع هيكله؛",
     "اعرض تقريرًا واحدًا منظمًا بميزانية طول (`brief` يطبع هيكله؛",
     "Phase 7: «one» report"),
    ("**المدخلات الحاجبة** إن وُجدت (سطر واحد بطريقة الإحضار)، ثم سطر **ردود العرض**: `موافق` · `تفاصيل` · `A/B/C` · `طوّر` · `نفّذ بأقصى قوة` · `كمّل بدوني`، ثم **سؤال الموافقة** آخر سطر في L1–L3 (لا سؤال موافقة في L0): «أنصحك بالخطة [A/B/C].",
     "ثم سطر **ردود العرض**: `موافق` · `تفاصيل` · `A/B/C` · `D` (دمج) · `طوّر` · `نفّذ بأقصى قوة` · `كمّل بدوني`، ثم **سؤال الموافقة** آخر سطر في L1–L3",
     "Phase 7: the D reply was added"),
    ("تحب أعرض لك تفاصيل القدرات وخطوات التنفيذ، ولا توافق على الخطة ونبدأ مباشرة؟» `كمّل` و`وقف` و`تراجع` ردود أثناء التنفيذ؛",
     ("تحب أعرض لك تفاصيل القدرات وخطوات التنفيذ، ولا توافق على الخطة ونبدأ مباشرة؟»", "`كمّل` و`وقف` و`تراجع` ردود أثناء التنفيذ"),
     "Phase 7: «موافق» = the plan and the suggested answers, inserted between the two"),
    ("A تحقق كل الإلزامي، والخطط الثلاث تجتاز اختبار اختلاف المنهج أو هي درجات عمق لمنهج واحد بطبيعته مذكورة في سطر.",
     "A تحقق كل الإلزامي، والخطط الثلاث بمعاني المسرد وتجتاز اختبار اختلاف المنهج",
     "Phase 7: the plans follow the glossary meanings"),
    ("نفّذ الخطة الموصى بها دون إعادة الأسئلة؛",
     "نفّذ الخطة الموصى بها واقبل الإجابة المقترحة لكل سؤال في التقرير",
     "Phase 8: «موافق» also accepts the suggested answers (glossary)"),
    ("خطّط بصمت (ومعه `brief` إن كان الطلب إنتاجًا) ونفّذ الخطة الموصى بها",
     "خطّط بصمت (ومعه `brief` والوصفة إن كان الطلب إنتاجًا) ونفّذ الخطة الموصى بها بالإجابات المقترحة",
     "Phase 8: the recipe is created silently too"),
    ("**تقرير التسليم:** ما سُلّم (الملفات بمساراتها وصيغها) · جدول المعايير (المعيار · العتبة · المقيس فعلًا · الأداة · ✅/❌) · ما لم يُفحص ولماذا · الفروق عن الخطة المعتمدة وسببها · المخاطر الباقية · درس يُرجَّح تكراره إن وُجد (المرحلة 10) · خطوة تالية واحدة إن وُجدت.",
     "· المخاطر الباقية · حالة التسليم (المسرد) · في L2/L3 رقم الوصفة `FUSE-…`",
     "Phase 9: the delivery state and the recipe were added to the report"),
    ("`data/hubs_index.json` · `START.md`",
     "`data/hubs_index.json` و`START.md`",
     "Phase 10: the rebuild table became one paragraph"),
    ("`data/tools.json` → `manifest.json`",
     "`data/tools.json` ثم `manifest.json`",
     "Phase 10: the rebuild table became one paragraph"),
    ("وبعد تعديل أي ملف في المهارة (وهذا البروتوكول منها) شغّل `scripts/check_skill.py` من مجلد المهارة؛",
     "وبعد تعديل أي ملف في المهارة (وهذا البروتوكول وملاحقه منها) شغّل `scripts/check_skill.py` من مجلد المهارة",
     "Phase 10: the appendices are part of the skill too"),
    ("ما يفحصه مفصّل في `references/guides/maintain.md`.",
     "وقائمة فحوصه في رأس `scripts/check_skill.py`",
     "Phase 10: references/guides/maintain.md is generated from data/tools.json and lags behind"),
    ("والقوانين 18–24 تحفظ حدود الحقيقة والحزم والأمان ولا تُسقطها عبارات تسريع العمل.",
     "والقوانين 18–26 تحفظ حدود الحقيقة والحزم والأمان والتعلم",
     "Phase 11: law 25 was added"),
    ("أما توجيهات `brief` و`verify` (المستوى، الخطط، أوامر الإصلاح) فمسودات في البند 5 من ترتيب الأولوية: خذ منها ما وافق هذا البروتوكول.",
     "أما توجيهات `brief` و`verify` و`fusionforge.py` (المستوى، الخطط، الأسئلة، أوامر الإصلاح) فمسودات في البند 5 من ترتيب الأولوية",
     "Phase 11: fusionforge.py output is a draft too"),
)


if __name__ == "__main__":
    if "--retention-report" in sys.argv:
        sys.exit(retention_report())
    unittest.main()
