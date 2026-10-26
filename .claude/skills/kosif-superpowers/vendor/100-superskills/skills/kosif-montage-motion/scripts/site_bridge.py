"""Consent-gated client for the public KOSIF Motion Workbench. Python 3.10+.

No renderer imports, credential acquisition, uploads, command execution or redirects.
Anonymous requests are the default. Optional KOSIF_SITE_TOKEN is never acquired here.
"""
from __future__ import annotations
import argparse
import json
import math
import os
from pathlib import Path
import sys
import urllib.error
import urllib.parse
import urllib.request

ORIGIN = 'https://kosif-motion-workbench.smartsphere152.chatgpt.site'
MAX_BYTES = 1_048_576
TIMEOUT = 20
OPERATIONS = {'health': 'GET', 'templates': 'GET', 'plan': 'POST', 'validate': 'POST', 'compile': 'POST'}

class BridgeError(Exception):
    """Safe diagnostics: no response bodies, request text, credentials or URLs."""

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise BridgeError('Redirect refused; use the approved exact Site origin.')


def parse_json(raw: bytes) -> dict:
    if len(raw) > MAX_BYTES:
        raise BridgeError('JSON exceeds the 1 MiB limit.')
    try:
        def reject_constant(_):
            raise ValueError('Nonfinite number')
        value = json.loads(raw.decode('utf-8'), parse_constant=reject_constant)
    except (ValueError, UnicodeError, RecursionError):
        raise BridgeError('Expected bounded, finite UTF-8 JSON.') from None
    if not isinstance(value, dict):
        raise BridgeError('Expected a JSON object.')
    if any(isinstance(item, float) and not math.isfinite(item) for item in json_values(value)):
        raise BridgeError('Expected finite JSON numbers.')
    return value


def json_values(value):
    """Visit keys and leaf values without recursive descent."""
    pending = [value]
    while pending:
        item = pending.pop()
        if isinstance(item, dict):
            pending.extend(item.keys())
            pending.extend(item.values())
        elif isinstance(item, list):
            pending.extend(item)
        else:
            yield item


def request(operation: str, payload: dict | None = None, *, allow_remote=False) -> dict:
    if operation not in OPERATIONS:
        raise BridgeError('Unsupported operation.')
    method = OPERATIONS[operation]
    if method == 'POST' and not allow_remote:
        raise BridgeError('Sending task or plan contents requires explicit --allow-remote approval.')
    token = os.environ.get('KOSIF_SITE_TOKEN', '')
    if token and (not token.isascii() or any(ord(c) < 33 or ord(c) > 126 for c in token) or len(token) > 16384):
        raise BridgeError('Invalid credential format.')
    body = None
    if method == 'POST':
        if not isinstance(payload, dict):
            raise BridgeError('A JSON object payload is required.')
        try:
            body = json.dumps(payload, ensure_ascii=False, allow_nan=False).encode('utf-8')
        except (TypeError, ValueError, RecursionError):
            raise BridgeError('Payload must be finite JSON.') from None
        if len(body) > MAX_BYTES:
            raise BridgeError('Request exceeds the 1 MiB limit.')
        if token and (token.encode() in body or any(isinstance(item, str) and token in item for item in json_values(payload))):
            raise BridgeError('Credential detected in payload; refusing transmission.')
    url = ORIGIN + '/api/' + operation
    parts = urllib.parse.urlsplit(url)
    if parts.scheme != 'https' or parts.netloc != urllib.parse.urlsplit(ORIGIN).netloc or parts.username or parts.password or parts.query or parts.fragment:
        raise BridgeError('Only the approved HTTPS origin is allowed.')
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
    if token:
        headers['OAI-Sites-Authorization'] = token
    req = urllib.request.Request(url, data=body, method=method, headers=headers)
    # Ignore environment proxy configuration: secrets go only to the exact Site.
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect())
    try:
        with opener.open(req, timeout=TIMEOUT) as response:
            if response.geturl() != url:
                raise BridgeError('Unexpected response location refused.')
            if response.headers.get('Content-Type','').split(';',1)[0].strip().lower() != 'application/json':
                raise BridgeError('Expected JSON; check Site availability and access.')
            raw = response.read(MAX_BYTES + 1)
    except urllib.error.HTTPError as exc:
        if exc.code in (401,403):
            raise BridgeError('Site access denied (HTTP %d); no automatic credential acquisition or retry.' % exc.code) from None
        raise BridgeError('Site request failed (HTTP %d).' % exc.code) from None
    except (urllib.error.URLError, TimeoutError, OSError, ValueError):
        raise BridgeError('Site connection failed; check access and network availability.') from None
    if token and token.encode() in raw:
        raise BridgeError('Credential echo detected; response discarded.')
    result = parse_json(raw)
    # Also catch JSON escaped representations of a token before printing or writing.
    if token and any(isinstance(item, str) and token in item for item in json_values(result)):
        raise BridgeError('Credential echo detected; response discarded.')
    return result


def read_plan(path: Path) -> dict:
    try:
        if not path.is_file() or path.is_symlink():
            raise BridgeError('Plan must be a regular non-symlink file.')
        with path.open('rb') as stream:
            obj = parse_json(stream.read(MAX_BYTES + 1))
    except OSError:
        raise BridgeError('Could not read the plan file.') from None
    if obj.get('schema') != 'kosif.proplan.v1':
        raise BridgeError('Expected a kosif.proplan.v1 plan, not a compile response.')
    return obj


def checked_new_directory(path: Path) -> Path:
    if '..' in path.parts:
        raise BridgeError('Parent traversal is not permitted in the project path.')
    target = path.absolute()
    for candidate in (target, *target.parents):
        if candidate.is_symlink():
            raise BridgeError('Symlink project paths are not permitted.')
    if target.exists() or not target.parent.is_dir():
        raise BridgeError('Choose a new project directory beneath an existing directory.')
    return target


def write_project(result: dict, path: Path) -> Path:
    html = result.get('project_html')
    if not isinstance(html, str) or not html or len(html.encode('utf-8')) > MAX_BYTES:
        raise BridgeError('No supported 2D project HTML returned; keep the manifest for manual authoring.')
    target = checked_new_directory(path)
    try:
        target.mkdir(mode=0o700)
        # Exclusive file creation; do not replace an existing index.html.
        with (target/'index.html').open('x', encoding='utf-8') as stream:
            stream.write(html)
    except OSError:
        raise BridgeError('Could not create the new project; no existing files were replaced.') from None
    return target/'index.html'


def output_json(result: dict, path: Path | None):
    content = json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False) + '\n'
    if path:
        try:
            # Exclusive creation prevents overwriting user work and following final symlinks.
            with path.open('x', encoding='utf-8') as stream:
                stream.write(content)
        except OSError:
            raise BridgeError('Output must be a new writable file; existing files are preserved.') from None
    else:
        print(content, end='')


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    for command in ('health','templates','plan','validate','compile','project'):
        p = sub.add_parser(command)
        p.add_argument('--allow-remote', action='store_true', help='Acknowledge approved transmission of task/plan contents to this public Site')
        if command != 'project':
            p.add_argument('--out', type=Path, help='New JSON output file; otherwise stdout')
        if command == 'plan':
            p.add_argument('--task', required=True)
            p.add_argument('--seconds', type=float, default=12)
            p.add_argument('--fps', type=int, default=30, choices=(24,25,30,50,60))
            p.add_argument('--aspect', default='9:16', choices=('9:16','16:9','1:1','4:5'))
            p.add_argument('--mode', default='pro', choices=('standard','pro'))
        if command in ('validate','compile','project'):
            p.add_argument('--plan', type=Path, required=True)
        if command == 'project':
            p.add_argument('--out-dir', type=Path, required=True, help='New directory beneath an existing nonsymlink parent')
    args = parser.parse_args(argv)
    try:
        payload = None
        if args.command == 'plan':
            if not args.task.strip() or len(args.task)>5000 or not 2 <= args.seconds <= 600:
                raise BridgeError('Task must be 1–5000 characters; duration must be 2–600 seconds.')
            payload = {key:getattr(args,key) for key in ('task','seconds','fps','aspect','mode')}
        if args.command in ('validate','compile','project'):
            payload = {'plan':read_plan(args.plan)}
        if args.command == 'project':
            checked_new_directory(args.out_dir)
        op = 'compile' if args.command == 'project' else args.command
        result = request(op, payload, allow_remote=args.allow_remote)
        if args.command == 'project':
            saved = write_project(result, args.out_dir)
            print('Saved 2D HTML project to ' + str(saved) + '. Review before local rendering; nothing was executed.')
        else:
            output_json(result,args.out)
        return 0
    except BridgeError as exc:
        print('Error: ' + str(exc), file=sys.stderr)
        return 2

if __name__ == '__main__':
    raise SystemExit(main())
