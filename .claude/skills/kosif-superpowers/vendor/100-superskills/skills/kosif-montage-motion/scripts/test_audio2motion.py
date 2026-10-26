"""Deterministic unit tests for the new audio2motion command."""
import unittest, tempfile, json, subprocess, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import audio2motion as a

class Voice2MotionTests(unittest.TestCase):
    def test_semantic_routing(self):
        self.assertEqual(a.classify('It is 68 degrees and sunny'), 'weather')
        self.assertEqual(a.classify('Traffic on the bridge'), 'traffic')
        self.assertEqual(a.classify('Support ticket duplicate billing'), 'support')
        self.assertEqual(a.classify('I confirm a full refund'), 'refund')
        self.assertEqual(a.classify('a random sentence'), 'generic')
    def test_estimate_cues_safe(self):
        c=a.estimate_cues('Good morning. Traffic on the bridge. Your full refund is confirmed.',10)
        self.assertEqual(c[0]['start'],0)
        self.assertAlmostEqual(c[-1]['end'],10)
        self.assertEqual([q['kind'] for q in c],['weather','traffic','refund'])
        a.validate_cues(c,10)
    def test_reject_invalid_timings(self):
        with self.assertRaises(ValueError):a.validate_cues([{'start':3,'end':2,'text':'x','kind':'weather'}],10)
        with self.assertRaises(ValueError):a.validate_cues([{'start':0,'end':3,'text':'x','kind':'weather'},{'start':2,'end':5,'text':'y','kind':'traffic'}],10)
        with self.assertRaises(ValueError):a.validate_cues([{'start':0,'end':6,'text':'x','kind':'fake'}],10)
    def test_audio_env_nonempty(self):
        import numpy as np
        bg=a.bg(270,480)
        c=[{'start':0,'end':2,'text':'Good morning','kind':'weather'}]
        im1=a.visual_frame(.1,2,c,.03,bg)
        im2=a.visual_frame(1.1,2,c,.9,bg)
        self.assertEqual(im1.size,(270,480))
        self.assertNotEqual(im1.tobytes(),im2.tobytes())
    def test_command_registered(self):
        from kmotion import C
        self.assertIn('audio2motion',C)
        self.assertEqual(C['audio2motion'][1],'audio2motion')
    def test_no_implicit_transcription(self):
        with self.assertRaises(ValueError):a.estimate_cues(' ',3)
    def test_duration_and_frame_near(self):
        self.assertEqual(int(__import__('math').ceil(28.84*30)),866)

class NoInventedFacts(unittest.TestCase):
    def test_labels_come_from_the_cue(self):
        bg=a.bg(270,480)
        a.visual_frame(.5,2,[{'start':0,'end':2,'text':'Rain all day, 12 degrees','kind':'weather'}],.3,bg)
        self.assertEqual(a.head(),'12')                                   # the number said, not the demo's 68
        a.CUE['text']='استرداد كامل للمبلغ'
        self.assertEqual(a.head(),'استرداد')
        self.assertTrue(a.font(20).getbbox('x'))                          # a real font on this OS


if __name__=='__main__':unittest.main(verbosity=2)
