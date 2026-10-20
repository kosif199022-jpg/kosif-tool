#!/usr/bin/env python3
"""Create metadata-only reviewed manifest and findings for KOSIF Superpower."""
import argparse,collections,json
from pathlib import Path

def main():
 p=argparse.ArgumentParser()
 for flag in ['records','rea-dir','manifest-out','report-out']:
  p.add_argument('--'+flag,required=True)
 a=p.parse_args()
 raw=json.loads(Path(a.records).read_text(encoding='utf-8'))
 byid={}
 for r in raw:
  key=str(r['skill_id'])
  item=byid.setdefault(key,{'id':r['skill_id'],'name':r['skill_name'],
    'source':r.get('origin'),'license_claim':r.get('license_claim'),
    'license_scope':r.get('license_scope'),'verdict_claim':r.get('verdict'),
    'risk_flags':r.get('risk_flags',[]),'document_sha256':None,
    'code_files_read':0,'code_sha256':[],'content_indicators':set(),
    'status':'METADATA_ONLY'})
  if r['status']!='FETCHED':continue
  item['content_indicators'].update(r.get('details',{}).get('indicators',{}).keys())
  if r.get('kind')=='skill':
   item['document_sha256']=r.get('sha256')
   item['atlas_path']=r.get('path')
   item['status']='SKILL_MD_READ_STATIC'
  elif r.get('kind')=='code':
   item['code_files_read']+=1
   item['code_sha256'].append({'path':r.get('path'),'sha256':r.get('sha256')})
 for item in byid.values():
  item['content_indicators']=sorted(item['content_indicators'])
  item['runtime_verified']=False
  item['auto_install_allowed']=False
 rea=[]
 for file in sorted(Path(getattr(a,'rea_dir')).glob('rea_*.json')):
  try:
   content=json.loads(file.read_text(encoding='utf-16'))
   stats=content['normalized_result']['statistics']
   rea.append({'skill_id':file.stem.removeprefix('rea_'),
    'evidence_id':content.get('evidence_id'),
    'tool':'REA 6.7.0 static JS','status':'STATIC_PARSED',
    'parsed_files':stats.get('parsed_javascript_files',0),
    'ast_nodes':stats.get('visited_ast_nodes',0),
    'structural_findings':stats.get('findings',0),
    'parse_failures':stats.get('parse_failures',0)})
  except (OSError,ValueError,KeyError,UnicodeError):pass
 items=sorted(byid.values(),key=lambda r:str(r['id']))
 scope={'schema':'kosif.atlas.reviewed-manifest.v1','records':len(items),
   'method':'static read of selected SKILL.md files and bounded selected scripts',
   'status':'CANDIDATES_NOT_ACTIVATED',
   'source_revision':'raw main checked with per-file SHA256',
   'privacy':'No third-party code, private local paths or credentials committed',
   'rea_static_analyses':rea,'skills':items}
 output=Path(getattr(a,'manifest_out'));output.parent.mkdir(parents=True,exist_ok=True)
 output.write_text(json.dumps(scope,ensure_ascii=False,indent=2),encoding='utf-8')
 flagged=[i for i in items if i['content_indicators']]
 cats=collections.Counter(c for i in flagged for c in i['content_indicators'])
 bodies=sum(i['document_sha256'] is not None for i in items)
 scripts=sum(i['code_files_read'] for i in items)
 parsed=sum(i['parsed_files'] for i in rea)
 nodes=sum(i['ast_nodes'] for i in rea)
 findings=sum(i['structural_findings'] for i in rea)
 md=[
 '# KOSIF Atlas source audit - 2026-10-20','',
 'Scope is a prioritized sample, not all 14,793 indexed skills. Third-party instructions remain untrusted data.',
 '',
 '## Evidence counts', '',
 f'- Actual SKILL.md bodies read: {bodies}.',
 f'- Selected source code files read: {scripts}.',
 f'- Skills with static risk-review indicators: {len(flagged)}.',
 f'- Indicator categories (counting skills): {dict(cats)}.',
 f'- REA successful code-group analyses: {len(rea)}; parsed JS files: {parsed}; AST nodes: {nodes}; structural findings: {findings}.',
 'Source presence and code parsing are not runtime feature verification.','',
 '## Tool selection', '',
 'REA inspects supported JavaScript/TypeScript; Ghidra handles native binary inputs.',
 'No native .exe, .dll, .so or .wasm artifact was declared in the full Atlas index file inventories.',
 'The prior REA plus Ghidra end-to-end proof on an authorized Windows executable remains valid, but cannot substitute for analysis of external skill source.','',
 '## Extractable concepts - CANDIDATES ONLY', '',
 '- Critical thinking, scientific evidence and uncertainty checking.',
 '- Motion and video rendering using Remotion plus already verified KOSIF Blender Cycles/FFmpeg pipeline.',
 '- Permission-gated browser automation and app validation.',
 '- Data safety checks, financial audit logging and versioned evidence receipts.',
 '- Repeatable workflow orchestration and accountable verification.','',
 '## Manually reviewed warning examples', '',
 '- 1943 superloopy-research: prompt-injection phrase is quoted as an example to reject, not an attack instruction.',
 '- 5838 grammarly-document-evaluator: mentions secrets while documenting environment-only OAuth handling; not a confirmed leak.',
 '- 7735 evaluate-context-engineering: regex matches sensitive actions to protect against them; not an executed harmful command.',
 '- 10459 temporal-cloud-setup: contains real cloud setup and secret-handling workflows; requires separate authorization and code audit.',
 '',
 '## Activation gates', '',
 '1. Do not run external skill code by default.',
 '2. Require matching license, dependencies, permissions and per-task safety review.',
 '3. Treat static detection as a review signal, not proof of malicious behavior.',
 '4. Copyleft source stays reference-only until redistribution duties are reviewed.',
 '5. Require real functional tests before marking a skill runnable.',
 '',
 'Metadata-only evidence in data/atlas-reviewed/manifest.json.',
 'Full third-party source and REA JSON evidence remain on the authorized computer in a private location.',
 '']
 rpt=Path(getattr(a,'report_out'));rpt.parent.mkdir(parents=True,exist_ok=True)
 rpt.write_text('\n'.join(md),encoding='utf-8')
 print(json.dumps({'bodies':bodies,'code':scripts,'rea':len(rea),'rea_files':parsed,
  'ast_nodes':nodes,'flagged_skills':len(flagged),'manifest':str(output),
  'report':str(rpt)},ensure_ascii=False))
if __name__=='__main__':main()
