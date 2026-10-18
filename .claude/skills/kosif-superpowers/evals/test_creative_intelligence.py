"""Evidence-driven tests for KOSIF original WAV-to-editable-storyboard bridge."""
import importlib.util
import json
from pathlib import Path
import struct
import sys
import tempfile
import unittest
import wave

SCRIPTS=Path(__file__).resolve().parents[1]/'scripts'
sys.path.insert(0,str(SCRIPTS))
import audio_cue_mapper as ac
import creative_reasoning_bridge as cb
import motion_director as md


def make_wav(path,secs=3):
    sr=8000; length=int(sr*secs)
    pcm=[]
    for n in range(length):
        # Audio energy bursts precisely every 0.5 seconds.
        high= int(n/(sr*.5))
        on= (n%int(sr*.5)) < int(sr*.16)
        pcm.append(12500 if on and n%2 else -12500 if on else 0)
    with wave.open(str(path),'wb') as out:
        out.setnchannels(1);out.setsampwidth(2);out.setframerate(sr)
        out.writeframes(struct.pack('<'+'h'*length,*pcm))


class CreativeIntelligenceTest(unittest.TestCase):
    def setUp(self):
        self.ctx=tempfile.TemporaryDirectory();self.addCleanup(self.ctx.cleanup)
        self.root=Path(self.ctx.name)
        make_wav(self.root/'sound.wav')

    def test_audio_onsets_measured_not_labelled_beats(self):
        cues=ac.measure_wav(self.root/'sound.wav')
        self.assertEqual(cues['schema'],'kosif.audio-cues.v1')
        self.assertEqual(cues['duration'],3)
        self.assertIsNone(cues['bpm'])
        self.assertFalse(cues['verified_beats'])
        self.assertGreaterEqual(len(cues['onset_candidates_seconds']),3)

    def test_alignment_preserves_arabic_words_and_timestamps(self):
        f=self.root/'timings.json'
        f.write_text(json.dumps({'segments':[{'words':[
            {'word':'كل','start':0.1,'end':0.4},
            {'word':'فكرة','start':0.55,'end':1.1},
            {'word':'تتحرك','start':1.5,'end':2.5}]}]},ensure_ascii=False),encoding='utf8')
        words=ac.import_aligned_words(f,3)
        self.assertEqual([x['text'] for x in words],['كل','فكرة','تتحرك'])
        cues=ac.measure_wav(self.root/'sound.wav');cues['words']=words
        out=cb.build_plan(cues)
        self.assertEqual(out['evidence']['aligned_word_count'],3)
        self.assertEqual([w['text'] for s in out['storyboard']['scenes'] for w in s['words']],['كل','فكرة','تتحرك'])
        self.assertEqual(md.validate(out['storyboard'])['duration'],3)
        self.assertEqual(out['render_status'],'unrendered_storyboard')

    def test_alignment_rejects_overlap_and_missing_timings(self):
        f=self.root/'broken.json'
        for words in ([{'word':'missing'}],[{'word':'a','start':0,'end':1},{'word':'b','start':0.5,'end':2}],
                      [{'word':'a','start':0,'end':3.5}]):
            f.write_text(json.dumps({'words':words}),encoding='utf8')
            with self.assertRaises(ValueError):ac.import_aligned_words(f,3)

    def test_determinism_and_no_fabricated_lyrics(self):
        cues=ac.measure_wav(self.root/'sound.wav');cues['words']=[]
        a=cb.build_plan(cues,'doodle');b=cb.build_plan(cues,'doodle')
        self.assertEqual(a,b)
        self.assertFalse(any(s['words'] for s in a['storyboard']['scenes']))
        self.assertFalse(a['decision']['style_override'] is False)

    def test_prevent_overwrite(self):
        p=self.root/'saved.json';p.write_text('keep',encoding='utf8')
        with self.assertRaises(FileExistsError):ac.write_json_new(p,{'data':1})
        self.assertEqual(p.read_text(), 'keep')

    def test_reject_unreal_number_and_bad_cue(self):
        cues=ac.measure_wav(self.root/'sound.wav')
        cues['duration']=float('nan')
        with self.assertRaises(ValueError):cb.build_plan(cues)
        cues['duration']=3;cues['words']=[{'text':'كلمة','start':0,'end':3.5}]
        with self.assertRaises(ValueError):cb.build_plan(cues)


if __name__=='__main__':unittest.main()