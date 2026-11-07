#!/usr/bin/env python3
"""Route inspected external Atlas source candidates to the 12-seat council.

No external skills, MCP tools, models, or scripts are loaded or executed.
The practical prompts below are locally authored operational interpretations,
not claims of 23 novel skills, independent expert runs, or semantic deduplication.
"""
from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from pathlib import Path

CATALOG = Path('docs/atlas_thinking_candidates_20261106.json')
ROLES = frozenset(('chair', 'analyst', 'story', 'creative', 'visual', 'engineer',
                   'critic', 'decision', 'research', 'systems', 'audience', 'learning'))
OPERATIONS_PATH = 'skills/1134-cognitive-operations/2713-cognitive-operations/references/operations.md'
MIRROR_PATH = 'skills/1120-ambient-library/2604-cognitive-operations/references/operations.md'
PATTERNS_PATH = 'skills/15-ai-tooling/24-prompt-engineering/references/reasoning-patterns.md'

# id, source-family, primary seat, optional supporting seats, task cues, practical prompt, output/check.
# Procedures are an original council adaptation of labels catalogued in the inspected sources.
PROCEDURES = (
 ('first_principles','operations','analyst','systems','problem design assumptions سبب مشكلة تصميم','Separate the goal from assumptions and irreducible constraints.','List testable assumptions and constraints.'),
 ('falsification','operations','critic','research','proof evidence test تحقق دليل اختبار','Specify an observation that would disprove the preferred answer.','A falsifiable claim and a concrete check.'),
 ('analogy','operations','creative','systems','creative visual analogy تشبيه ابتكار إبداع','Find a structural analogy, then state where it breaks.','A transferable principle and its limit.'),
 ('abduction','operations','research','analyst','diagnosis cause mystery error تشخيص سبب عطل','Compare competing explanations of observed evidence.','Candidate causes, evidence and unknowns.'),
 ('counterfactual','operations','decision','critic','decision alternative failure بديل قرار فشل','Ask which minimal changed condition would reverse the outcome.','A counterfactual and assumptions to test.'),
 ('dialectical_synthesis','operations','chair','critic,research','debate conflict disagreement جدل اعتراض تعارض','Record the strongest case for and against without inventing agent runs.','A synthesis retaining unresolved objections.'),
 ('systems_thinking','operations','systems','engineer','architecture dependency feedback نظام ترابط اعتماد','Map dependencies, feedback and downstream effects.','A dependency map with failure points.'),
 ('bayesian_updating','operations','research','decision','probability uncertain forecast احتمال توقع','State a prior and evidence before revising confidence.','A documented update, or unknown if inputs are absent.'),
 ('perspective_simulation','operations','audience','story','audience viewer customer user جمهور مشاهد مستخدم','Compare stakeholder perspectives as hypotheses, not real audience feedback.','Perspective differences requiring user testing.'),
 ('chain_of_thought','patterns','analyst','critic','complex reasoning problem تحليل تفكير مسألة','Structure a concise answer with assumptions, checkpoints and evidence, not private reasoning traces.','An inspectable summary of the decision basis.'),
 ('step_back','patterns','analyst','systems','principle problem scope مبدأ إطار مشكلة','Identify the broader principle before choosing a local tactic.','A stated principle and its relevance.'),
 ('self_consistency','patterns','critic','decision','uncertainty choices alternative بدائل اتساق','Compare independently specified candidate conclusions without pretending model independence.','Agreement and disagreement table.'),
 ('tree_of_thought','patterns','decision','creative','alternatives branches options بدائل مسارات خيارات','Sketch alternative routes with explicit feasibility and stopping checks.','An option tree; no branches claimed executed.'),
 ('react','patterns','engineer','research','tool execute observe action أداة تنفيذ فحص','Plan action-observation checkpoints; take no external action without a runner.','An authorized action plan and expected evidence.'),
 ('reflexion','patterns','learning','critic','retry error feedback improve تعلّم تحسين خطأ','Compare observed failures to the plan, then revise one hypothesis.','A versioned lesson and retest criterion.'),
 ('plan_and_solve','patterns','chair','engineer','complex project tasks timeline خطة مشروع مهمة','Break the goal into dependent deliverables with exit criteria.','A testable plan and ownership.'),
 ('least_to_most','patterns','analyst','learning','decompose difficult learn تجزئة صعب تعلم','Solve prerequisites before the harder dependent question.','Ordered prerequisite checks.'),
 ('self_ask','patterns','research','analyst','unknown question source سؤال بحث مجهول','List missing factual subquestions and which source would answer each.','An evidence request list, not invented answers.'),
 ('skeleton_of_thought','patterns','story','chair','writing outline script structure كتابة مخطط نص','Draft an outline, then expand only the necessary sections.','A structured draft with gaps labelled.'),
 ('chain_of_draft','patterns','story','learning','draft concise revision اختصار مسودة تحرير','Use compact drafts and an explicit final quality check.','A final draft and verification notes.'),
 ('concise_cot','patterns','analyst','decision','brief rationale explain concise ملخص تفسير قرار','Provide a short evidence-based rationale rather than an unverifiable thought transcript.','Decision, key reasons and uncertainty.'),
 ('token_budget','patterns','chair','engineer','budget cost efficient time ميزانية وقت تكلفة','Allocate attention by risk and reversibility instead of arbitrary verbosity.','A review budget and escalation triggers.'),
 ('sketch_of_thought','patterns','visual','systems','diagram sketch storyboard رسم تخطيط مشهد','Express dependencies as a compact diagram or storyboard sketch.','A sketch with explicitly untested assumptions.'),
)


# All 26 inspected paths get a council-specific *advisory* action, not a tool adapter.
# The source's actual procedures must be checked before treating these as equivalent.
SOURCE_ACTIONS = {
 'large_inventory_candidate': ('Select a relevant family of models before choosing any model.', 'Record selected source labels and compare with internal models.'),
 'orchestration_candidate': ('Prepare a for/against evidence matrix.', 'Do not report independent debate unless run receipts exist.'),
 'external_dependency': ('Check the declared external runtime, authorization and credentials.', 'Mark unavailable unless a real runner is verified.'),
 'creative_workflow_candidate': ('Generate several genuinely different candidate concepts.', 'Require a storyboard or viewer test before ranking.'),
 'knowledge_capture_candidate': ('Record the expert workflow as explicit inputs, steps and checks.', 'Keep original source and separate inference from observed expertise.'),
 'engineering_protocol_candidate': ('Draw dependencies and failure boundaries before implementation.', 'Check against actual code and tests.'),
 'orchestration_overlap': ('Compare the proposed council protocol with current debate rules.', 'Retain only distinct steps and do not add phantom agents.'),
 'verification_enhancement': ('Link each requirement to evidence, claim and counterexample.', 'Flag missing or contradicted evidence.'),
 'probable_method_overlap': ('Compare full method steps with the existing named lens.', 'Record semantic review needed; preserve both source IDs.'),
 'dialogue_enhancement': ('Elicit the real task, stakeholder and missing constraints.', 'Mark assumptions if no user answer was supplied.'),
 'method_collection': ('Select source-labelled procedures relevant to the task.', 'Do not treat labels as novel runnable tools.'),
 'exact_duplicate': ('Keep the mirror as a provenance-only pointer.', 'Do not count or activate the same bytes twice.'),
 'scientific_verification_candidate': ('Separate correlation, mechanism and alternative causes.', 'Request underlying study evidence before confidence claims.'),
 'bias_check_candidate': ('Name a possible judgment bias and a disconfirming check.', 'Do not infer a user psychological trait.'),
 'probable_workflow_overlap': ('Compare brainstorming stages with existing creative workflow.', 'Retain distinct instructions; avoid duplicate capability counts.'),
 'reference_only': ('Store source metadata without activating an uninspected tool.', 'No executable claim is permitted.'),
}

def _tokens(text: str) -> set[str]:
    text = unicodedata.normalize('NFKC', text).casefold()
    text = re.sub(r'[\u064b-\u065f\u0670\u0640]', '', text)
    text = text.translate(str.maketrans({'أ':'ا','إ':'ا','آ':'ا','ى':'ي'}))
    return {w for w in re.findall(r'[a-z0-9]+|[\u0621-\u064a]+', text) if len(w) > 2}


def plan(task: str, root: Path, roles=ROLES) -> dict:
    """Return a source-linked *candidate* plan; no third-party execution occurs."""
    allowed = set(roles)
    if allowed != ROLES:
        raise ValueError('external Atlas bridge requires the existing 12 council seats')
    if not task or not task.strip():
        raise ValueError('task is required')
    file = root / CATALOG
    if not file.is_file():
        return {'status':'NO_EXTERNAL_ATLAS_CATALOG', 'catalogued_paths':0, 'source_assignments':[],
                'candidate_procedures':[], 'selected_procedures':[], 'limits':'No external Atlas catalog at this root.'}
    raw = file.read_bytes()
    catalog = json.loads(raw.decode('utf-8'))
    paths = catalog.get('source_items')
    if not isinstance(paths, list) or not paths:
        raise ValueError('external Atlas catalog must contain a source_items list')
    commit = catalog.get('atlas_commit')
    if not isinstance(commit, str) or not re.fullmatch(r'[0-9a-f]{40}', commit):
        raise ValueError('invalid pinned external Atlas commit')
    records, seen = [], set()
    for item in paths:
        if not isinstance(item, dict):
            raise ValueError('invalid external source record')
        path, roles_for = item.get('path'), item.get('proposed_roles')
        if not isinstance(path, str) or path in seen or path.startswith('/') or '..' in Path(path).parts:
            raise ValueError('duplicate or unsafe external source path')
        if not isinstance(roles_for, list) or not roles_for or len(set(roles_for)) != len(roles_for) or not set(roles_for) <= allowed:
            raise ValueError('external Atlas source has unassigned/duplicate council roles')
        if not isinstance(item.get('classification'), str) or not item['classification']:
            raise ValueError('external Atlas source needs classification')
        seen.add(path)
        if item['classification'] not in SOURCE_ACTIONS:
            raise ValueError('unreviewed external Atlas source classification')
        action, evidence = SOURCE_ACTIONS[item['classification']]
        records.append({'advisory_action':action, 'evidence_gate':evidence,
                        'source_id':'atlas:'+path, 'name':item.get('name',path),
                        'primary':roles_for[0], 'secondary':roles_for[1:],
                        'classification':item['classification'], 'source_path':path,
                        'source_commit':commit, 'status':'CATALOGUED_NOT_EXECUTED'})
    mirror = catalog.get('known_byte_duplicate', {})
    pair = mirror.get('paths')
    if not isinstance(pair, list) or len(pair) != 2 or pair != [OPERATIONS_PATH,MIRROR_PATH] or not set(pair) <= seen:
        raise ValueError('known duplicate paths changed; source review required')
    if not re.fullmatch(r'[0-9a-f]{40}', str(mirror.get('sha',''))):
        raise ValueError('known duplicate Git blob SHA is missing')
    if not {OPERATIONS_PATH,PATTERNS_PATH} <= seen:
        raise ValueError('external methods source paths missing')
    methods=[]
    for ident, family, seat, secondary, cues, question, output in PROCEDURES:
        if seat not in allowed or not set(secondary.split(',')) <= allowed:
            raise ValueError('procedure has invalid council roles')
        source = OPERATIONS_PATH if family == 'operations' else PATTERNS_PATH
        methods.append({'id':'atlas-procedure:'+ident, 'name':ident.replace('_',' '),
                        'source_id':'atlas:'+source, 'source_commit':commit,
                        'primary':seat, 'secondary':secondary.split(','),
                        'task_cues':cues, 'question':question, 'output_check':output,
                        'status':'LOCAL_PLANNING_PROCEDURE_NOT_AGENT',
                        'semantic_overlap_with_internal_486':'UNREVIEWED',
                        'source_mirror':MIRROR_PATH if family=='operations' else None})
    query = _tokens(task)
    ranked=sorted(methods,key=lambda m:(-len(query & _tokens(m['task_cues']+' '+m['name'])),m['id']))
    selected=[m for m in ranked if query & _tokens(m['task_cues']+' '+m['name'])][:8]
    if not selected:
        preferred={'first_principles','falsification','systems_thinking','plan_and_solve'}
        selected=[m for m in methods if m['id'].split(':')[-1] in preferred]
    return {'status':'CANDIDATES_ROUTED_NOT_EXECUTED','catalog_sha256':hashlib.sha256(raw).hexdigest(),
            'atlas_commit':commit, 'catalogued_paths':len(records),
            'paths_after_known_exact_duplicate':len(records)-1,
            'known_exact_duplicate_pairs':1, 'candidate_procedure_count':len(methods),
            'source_assignments':records, 'candidate_procedures':methods,
            'selected_procedures':selected,
            'primary_assigned_once':len({r['source_id'] for r in records})==len(records),
            'limits':'Sampled external sources only; no exhaustive Atlas coverage, semantic uniqueness, independent agents, external tool execution or CI proof.'}
