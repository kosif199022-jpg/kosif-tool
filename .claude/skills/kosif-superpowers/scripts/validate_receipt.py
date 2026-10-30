#!/usr/bin/env python3
"""Validate a USIP v6.0 execution receipt (appendix A43) without network or third-party modules.

Usage: python3 validate_receipt.py receipt.json   (exit 0 = coherent, 1 = not)

A receipt is not a substitute for independent verification. This validator
checks internal coherence, not the truth of attached evidence.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

STATES = {'PLANNED','RUNNING','VERIFIED','PARTIAL','FAILED','BLOCKED','SKIPPED'}
TEST_RESULTS = {'PASS','FAIL','NOT_RUN'}


def validate(data, base):
    errors=[]
    if not isinstance(data,dict):return ['Root must be an object']
    if data.get('version') not in ('USIP-6.0','6.0'):errors.append('version must be USIP-6.0')
    status=data.get('status')
    if status not in STATES:errors.append(f'Invalid status: {status}')
    art=data.get('artifact')
    if not isinstance(art,str) or not art.strip():errors.append('artifact must be a path string')
    elif status=='VERIFIED':
        target=Path(art)
        if not target.is_absolute():target=(base/target).resolve()
        if not target.is_file():errors.append('VERIFIED requires a present artifact file')
        elif not target.is_relative_to(base.resolve()) and not Path(art).is_absolute():
            errors.append('Artifact path escapes receipt base')
    checks=data.get('checks')
    if not isinstance(checks,list):errors.append('checks must be a list');checks=[]
    for i,c in enumerate(checks):
        if not isinstance(c,dict):errors.append(f'checks[{i}] must be an object');continue
        if c.get('result') not in TEST_RESULTS:errors.append(f'checks[{i}].result invalid')
        if c.get('result')=='PASS' and not c.get('evidence'):
            errors.append(f'checks[{i}] PASS without evidence')
    if status=='VERIFIED':
        if not checks:errors.append('VERIFIED requires at least one test')
        elif any(c.get('result')!='PASS' for c in checks if isinstance(c,dict)):
            errors.append('VERIFIED cannot include failed or unrun checks')
    for i,s in enumerate(data.get('inputs',[])):
        if not isinstance(s,dict):errors.append(f'inputs[{i}] must be object');continue
        h=s.get('sha256','')
        if h and not (isinstance(h,str) and len(h)==64 and all(x in '0123456789abcdef' for x in h.lower())):
            errors.append(f'inputs[{i}] SHA256 must be 64 hexadecimal characters')
    if data.get('remote_deployment') is True and not data.get('remote_evidence'):
        errors.append('remote_deployment=true requires remote_evidence')
    return errors


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('receipt',type=Path)
    args=p.parse_args(argv)
    if not args.receipt.is_file():print('FAIL: receipt file not found');return 1
    try: doc=json.loads(args.receipt.read_text(encoding='utf-8-sig'))
    except (OSError,UnicodeError,json.JSONDecodeError) as ex:print(f'FAIL: cannot read receipt: {ex}');return 1
    errors=validate(doc,args.receipt.resolve().parent)
    if errors:
        for e in errors:print('FAIL:',e)
        return 1
    print('PASS: coherent receipt (evidence authenticity NOT independently verified)')
    return 0

if __name__=='__main__':sys.exit(main())
