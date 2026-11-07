"""Source-traceable, non-executing Atlas candidate bridge regression checks."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / '.claude/skills/kosif-black-dragon/scripts/atlas_council_bridge.py'
SPEC = importlib.util.spec_from_file_location('atlas_council_bridge', SCRIPT)
bridge = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(bridge)


class AtlasBridgeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'docs').mkdir()
        candidates = [
            {'path': 'skills/fake%d/SKILL.md' % i, 'name':'Example %d' % i,
             'proposed_roles':['analyst','research'], 'classification':'reference_only'}
            for i in range(23)
        ]
        candidates += [
            {'path': bridge.OPERATIONS_PATH, 'name':'Cognitive Operations',
             'proposed_roles':['analyst','critic'], 'classification':'method_collection'},
            {'path': bridge.MIRROR_PATH, 'name':'Cognitive Operations mirror',
             'proposed_roles':['analyst'], 'classification':'exact_duplicate'},
            {'path': bridge.PATTERNS_PATH, 'name':'Reasoning Patterns',
             'proposed_roles':['analyst','learning'], 'classification':'method_collection'},
        ]
        self.catalog = {'atlas_commit':'a'*40, 'source_items':candidates,
                        'known_byte_duplicate':{'paths':[bridge.OPERATIONS_PATH,bridge.MIRROR_PATH],
                                                'sha':'b'*40}}
        self.save()

    def save(self):
        (self.root / bridge.CATALOG).write_text(json.dumps(self.catalog), encoding='utf-8')

    def test_all_sources_routed_with_known_mirror_deduplicated(self):
        p = bridge.plan('audience storyboard story visual', self.root)
        self.assertEqual(p['catalogued_paths'], 26)
        self.assertEqual(p['paths_after_known_exact_duplicate'], 25)
        self.assertEqual(p['candidate_procedure_count'], 23)
        self.assertEqual(len(p['source_assignments']), 26)
        self.assertTrue(p['primary_assigned_once'])
        self.assertTrue(all(r['advisory_action'] and r['evidence_gate'] for r in p['source_assignments']))
        self.assertEqual(len({m['id'] for m in p['candidate_procedures']}), 23)
        self.assertTrue(all(m['primary'] in bridge.ROLES for m in p['candidate_procedures']))
        self.assertTrue(all(m['status']=='LOCAL_PLANNING_PROCEDURE_NOT_AGENT' for m in p['candidate_procedures']))
        self.assertTrue(all(m['semantic_overlap_with_internal_486']=='UNREVIEWED' for m in p['candidate_procedures']))
        self.assertTrue(p['selected_procedures'])

    def test_source_provenance_retained_and_no_fake_execution(self):
        p = bridge.plan('Bayesian probability estimate', self.root)
        matched = next(m for m in p['candidate_procedures'] if m['id']=='atlas-procedure:bayesian_updating')
        self.assertEqual(matched['source_id'],'atlas:'+bridge.OPERATIONS_PATH)
        self.assertEqual(matched['source_mirror'], bridge.MIRROR_PATH)
        self.assertEqual(matched['source_commit'], 'a'*40)
        self.assertEqual(p['status'],'CANDIDATES_ROUTED_NOT_EXECUTED')
        self.assertNotIn('executed_agents',p)
        self.assertNotIn('video_path',p)

    def test_invalid_duplicates_roles_or_missing_provenance_rejected(self):
        self.catalog['source_items'].append(dict(self.catalog['source_items'][0]))
        self.save()
        with self.assertRaisesRegex(ValueError,'duplicate or unsafe'):
            bridge.plan('test',self.root)
        self.catalog['source_items'].pop()
        self.catalog['source_items'][0]['proposed_roles']=['unknown']
        self.save()
        with self.assertRaisesRegex(ValueError,'unassigned'):
            bridge.plan('test',self.root)
        self.catalog['source_items'][0]['proposed_roles']=['analyst']
        self.catalog['known_byte_duplicate']['sha']='unknown'
        self.save()
        with self.assertRaisesRegex(ValueError,'blob SHA'):
            bridge.plan('test',self.root)

    def test_missing_manifest_is_explicit(self):
        (self.root / bridge.CATALOG).unlink()
        p=bridge.plan('any task', self.root)
        self.assertEqual(p['status'],'NO_EXTERNAL_ATLAS_CATALOG')
        self.assertEqual(p['catalogued_paths'], 0)

    def test_repository_integration_and_486_not_inflated(self):
        if not (ROOT / bridge.CATALOG).is_file():
            self.skipTest('repository fixture absent')
        real = bridge.plan('فيديو جمهور تفسير وتحليل',ROOT)
        self.assertEqual(real['catalogued_paths'],26)
        self.assertEqual(real['candidate_procedure_count'],23)
        council_path=ROOT/'.claude/skills/kosif-black-dragon/scripts/creative_council.py'
        spec=importlib.util.spec_from_file_location('creative_council_bridge_integration', council_path)
        council=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(council)
        report=council.plan('فيديو جمهور تفسير وتحليل',ROOT)
        self.assertEqual(report['total_source_records'],525)
        self.assertEqual(report['external_atlas']['catalogued_paths'],26)
        self.assertEqual(sum(s['external_atlas_candidate_count'] for s in report['roles']),26)
        self.assertEqual(sum(len(s['external_atlas_candidate_actions']) for s in report['roles']),26)
        self.assertEqual(len(report['roles']),12)


if __name__=='__main__':
    unittest.main()
