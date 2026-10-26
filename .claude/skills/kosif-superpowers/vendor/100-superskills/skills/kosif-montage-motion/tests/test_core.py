"""Offline regression tests; no network, no model billing, no source edits."""
from pathlib import Path
import importlib.util
import json
import sys
import tempfile
import unittest

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE / 'scripts'))
import env_check
import kmotion
import proplan
import transcribe

class UnitTests(unittest.TestCase):
    def test_cli_registry(self):
        self.assertIn('proplan', kmotion.C)
        for v in kmotion.C.values():
            if v[1]: self.assertIsNotNone(importlib.util.find_spec(v[1]))

    def test_env_supports_manual_transcript(self):
        env = env_check.check()
        self.assertIn(env['route'], ('A','B','C'))
        self.assertIn('reel_with_transcript', env['can'])

    def test_timed_transcript_validates(self):
        good = [{'start':0.0,'end':1.0,'text':'أهلاً','words':[{'start':0.0,'end':0.9,'text':'أهلاً'}]}]
        with tempfile.TemporaryDirectory() as td:
            path = Path(td)/'words.json'
            path.write_text(json.dumps(good,ensure_ascii=False),encoding='utf-8')
            self.assertEqual(len(transcribe.load_transcript(path,1.0)),1)
            good[0]['words'][0]['end']=1.5
            path.write_text(json.dumps(good,ensure_ascii=False),encoding='utf-8')
            with self.assertRaisesRegex(ValueError,'invalid'):
                transcribe.load_transcript(path,1.0)
            good[0]['words'][0]['end']=float('nan')
            path.write_text(json.dumps(good,ensure_ascii=False),encoding='utf-8')
            with self.assertRaisesRegex(ValueError,'invalid'):
                transcribe.load_transcript(path,1.0)

    def test_router_positive_negative(self):
        p=proplan.plan('مونتاج ريلز عربي مع ترجمة وصوت',mode='pro')
        self.assertEqual(p['intent'],'footage_edit')
        self.assertIn('reel',p['available_commands'])
        self.assertIn('captions',p['available_commands'])
        self.assertLessEqual(len(p['selected_skills']),4)
        self.assertEqual(p['full_pro_status'],'NOT_FULL_PRO')
        a=proplan.plan('اصنع مشهد ثلاثي الأبعاد',mode='standard')
        self.assertEqual(a['intent'],'3d_motion')
        self.assertEqual(proplan.plan('برومبت Veo سينمائي')['intent'],'prompt')
        self.assertNotIn('transcribe',proplan.plan('صورة فوتوغرافية')['available_commands'])

    def test_timed_shotplan_contiguous(self):
        p=proplan.plan('اعمل فيلم 3d',seconds=11,fps=30,aspect='9:16')
        shots=p['timeline']['shots']
        self.assertEqual(len(shots),5)
        self.assertEqual(shots[0]['start_frame'],0)
        self.assertEqual(shots[-1]['end_frame_exclusive'],330)
        self.assertTrue(all(a['end_frame_exclusive']==b['start_frame'] for a,b in zip(shots,shots[1:])))
        self.assertEqual(p['timeline']['safe_area']['text_top_pct'],15)
        with self.assertRaises(ValueError): proplan.plan('فيلم', seconds=0)

    def test_receipt_binds_request(self):
        q='فيلم تعليمي'
        p=proplan.plan(q)
        receipts=dict(runtime_complete=True, executor_verified=True, qa_verified=True, request_digest='wrong')
        self.assertEqual(proplan.plan(q,full_pro_receipts=receipts)['full_pro_status'],'NOT_FULL_PRO')
        receipts['request_digest']=p['request_digest']
        self.assertEqual(proplan.plan(q,full_pro_receipts=receipts)['full_pro_status'],'NOT_FULL_PRO')

if __name__=='__main__':unittest.main()
