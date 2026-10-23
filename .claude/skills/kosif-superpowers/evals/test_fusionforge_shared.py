#!/usr/bin/env python3
"""Synthetic security-boundary tests for FusionForge shared memory (not real production QA)."""
import hashlib
import importlib.util
import json
import sys
import tempfile
import types
import unittest
from pathlib import Path

FILE=Path(__file__).resolve().parents[1]/'scripts'/'fusionforge_shared.py'
spec=importlib.util.spec_from_file_location('fsh',FILE)
fsh=importlib.util.module_from_spec(spec)
spec.loader.exec_module(fsh)

class StubCtx:
    def __init__(self,args): pass

class TestShared(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        self.addCleanup(lambda: sys.modules.pop('fusionforge',None))
        self.fake=types.SimpleNamespace(Ctx=StubCtx, validate_recipe=lambda ctx,space,recipe:{'errors':[]},
                  proven_here=lambda ctx,space,recipe,check: None, FFError=RuntimeError)
        sys.modules['fusionforge']=self.fake
        self.graph={'nodes':[{'stage':'create','executor':'bin:ffmpeg','inputs':['plan'],'outputs':['video'],
            'capabilities':[{'name_en':'Private company test','atoms_sha256':'a'*64}], 'acceptance':'client confidential'},
            {'stage':'verify','executor':'human','inputs':['video'],'outputs':['evidence'],
            'capabilities':[], 'acceptance':'verified QA'}],
            'edges':[['create','verify','video','verify']]}
        self.sig=fsh.signature({'sanitized':self.graph})

    def fixture(self,project,idx):
        path=self.root/project
        (path/'recipes').mkdir(parents=True,exist_ok=True)
        (path/'promotions').mkdir(exist_ok=True)
        (path/'evidence').mkdir(exist_ok=True)
        rid=f'FUSE-20261022-{idx:010x}'
        qa=f'actual QA outcome {project} {idx}'.encode()
        sha=hashlib.sha256(qa).hexdigest()
        stored=f'evidence/{sha}.json'
        (path/stored).write_bytes(qa)
        rec={'sha256':sha,'stored':stored}
        recipe={'id':rid,'project':project,'status':'verified','nodes':[{'id':'N01','stage':'create','status':'passed',
              'last_trace':1,'executor':{'ref':'bin:ffmpeg'},'capability_ids':['SP-0001'],
              'inputs':[{'kind':'plan'}],'outputs':[{'kind':'video'}],'acceptance':'client confidential'},
              {'id':'N02','stage':'verify','status':'passed','last_trace':2,'executor':{'ref':'human'},
              'capability_ids':[], 'inputs':[{'kind':'video'}],'outputs':[{'kind':'evidence'}],'acceptance':'verified QA'}],
              'capabilities':{'SP-0001':{'name_en':'Private company test','atoms_sha256':'a'*64}},
              'edges':[{'from':'N01','to':'N02','kind':'video','relation':'verify'}],
              'plan_choice':{'nodes':['N01','N02']},'traces':[{'seq':1,'node':'N01','result':'passed'},
              {'seq':2,'node':'N02','result':'passed','evidence':rec}],
              'evidence':[{'status':'verified',**rec}],'status_log':[{'to':'verified','evidence_sha256':sha}]}
        (path/'recipes'/f'{rid}.json').write_text(json.dumps(recipe))
        p={'schema':'kosif.fusionforge.promotion.v2','recipe_id':rid,
           'graph_signature':self.sig,'sanitized':self.graph,'approval':{'state':'pending_human'}}
        (path/'promotions'/f'{rid}.proposal.json').write_text(json.dumps(p))
        return path,rec

    def test_requires_independent_three_projects(self):
        self.fixture('clientA',1)
        data=fsh.collect(self.root)
        self.assertEqual(fsh.tier(data[self.sig])['tier'],'experimental')
        self.fixture('clientA',2)
        data=fsh.collect(self.root)
        self.assertEqual(fsh.tier(data[self.sig])['tier'],'local_trusted')
        self.fixture('clientB',3)
        data=fsh.collect(self.root)
        self.assertEqual(fsh.tier(data[self.sig])['tier'],'local_trusted')
        self.fixture('clientC',4)
        data=fsh.collect(self.root)
        self.assertEqual(fsh.tier(data[self.sig])['tier'],'shared_eligible')

    def test_reject_tamper_and_duplicate_proof(self):
        path,rec=self.fixture('clientA',1)
        path2,_=self.fixture('clientB',2)
        qa_src=(path/rec['stored']).read_bytes()
        qa_dest=f'evidence/{rec["sha256"]}.json'
        (path2/qa_dest).write_bytes(qa_src)
        recipe_path=next((path2/'recipes').glob('*.json'))
        recipe=json.loads(recipe_path.read_text())
        recipe['evidence']=[dict(status='verified',sha256=rec['sha256'],stored=qa_dest)]
        recipe['traces'][1]['evidence']={'sha256':rec['sha256'],'stored':qa_dest}
        recipe_path.write_text(json.dumps(recipe))
        data=fsh.collect(self.root)
        self.assertEqual(fsh.tier(data[self.sig])['independent_tests'],1)
        (path/rec['stored']).write_bytes(b'tampered')
        data=fsh.collect(self.root)
        self.assertEqual(fsh.tier(data[self.sig])['independent_tests'],1)

    def test_no_private_fields_in_public_graph(self):
        public=fsh.public_graph({'sanitized':self.graph})
        raw=json.dumps(public)
        self.assertNotIn('Private company test',raw)
        self.assertNotIn('client confidential',raw)
        self.assertEqual(public['artifact_kinds'],['video'])

    def test_approval_gate(self):
        for i,p in enumerate(('alpha','beta','gamma'),1):self.fixture(p,i)
        review=self.root/'_shared'/'reviews'
        review.mkdir(parents=True)
        sig=self.sig
        incomplete={'signature':sig,'decision':'approve','reviewer':'QA','independent_qa':True,
                    'security_review':True,'privacy_review':True,'catalog_collision_check':True,
                    'scenarios':['motion','accounting','software'],
                    'baseline_comparison':{'direction':'higher','baseline':2,'candidate':3}}
        (review/f'{sig}.json').write_text(json.dumps(incomplete))
        self.assertTrue(fsh.approved_review(review/f'{sig}.json',sig))
        groups=fsh.collect(self.root)
        self.assertEqual(fsh.tier(groups[sig])['tier'],'shared_eligible')
        reg=fsh.registry(self.root)
        reg['items'][sig]={'graph':fsh.public_graph(groups[sig][0]['proposal'])}
        fsh.write_atomic(self.root/'_shared'/'registry.json',reg)
        raw=(self.root/'_shared'/'registry.json').read_text()
        self.assertNotIn('alpha',raw)
        self.assertNotIn('Private company',raw)
        incomplete['baseline_comparison']['candidate']=1
        (review/f'{sig}.json').write_text(json.dumps(incomplete))
        with self.assertRaises(ValueError):fsh.approved_review(review/f'{sig}.json',sig)
    def test_docstring_lists_every_subcommand(self):
        for name in ('audit','approve','recall','review-template'):
            self.assertIn('fusionforge_shared.py '+name,fsh.__doc__,name)
        src=FILE.read_text(encoding='utf-8')
        for name in __import__('re').findall(r"add_parser\('([a-z-]+)'",src):
            self.assertIn('fusionforge_shared.py '+name,fsh.__doc__,name)

if __name__=='__main__':unittest.main(verbosity=2)
