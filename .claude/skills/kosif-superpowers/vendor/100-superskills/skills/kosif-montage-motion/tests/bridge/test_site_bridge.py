"""Only reviewed bridge code is imported; no legacy renderer execution."""
import importlib.util
import io
import json
import os
from pathlib import Path
import unittest
import tempfile
from unittest.mock import patch
import urllib.error

SCRIPT = Path(__file__).resolve().parents[2] / 'scripts' / 'site_bridge.py'

class Availability(unittest.TestCase):
    def test_reviewed_bridge_exists(self):
        self.assertTrue(SCRIPT.is_file(), 'The consent-gated public bridge is missing')

@unittest.skipUnless(SCRIPT.is_file(), 'Bridge implementation pending')
class Bridge(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location('site_bridge', SCRIPT)
        cls.m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.m)

    def response(self, body=b'{"ok":true}', url=None, content_type='application/json'):
        r = io.BytesIO(body)
        r.geturl = lambda: url or self.m.ORIGIN + '/api/health'
        r.headers = {'Content-Type': content_type}
        return r

    def test_plan_requires_acknowledgement_before_network(self):
        with patch.object(self.m.urllib.request, 'build_opener') as network:
            with self.assertRaises(self.m.BridgeError):
                self.m.request('plan', {'task':'private'}, allow_remote=False)
            network.assert_not_called()

    def test_anonymous_health_succeeds_without_token(self):
        with patch.dict(os.environ, {}, clear=True), patch.object(self.m.urllib.request, 'build_opener') as build:
            build.return_value.open.return_value = self.response()
            self.assertEqual(self.m.request('health'), {'ok': True})
            req = build.return_value.open.call_args.args[0]
            self.assertIsNone(req.get_header('Oai-sites-authorization'))
            self.assertEqual(req.full_url, self.m.ORIGIN+'/api/health')

    def test_anonymous_plan_requires_no_token(self):
        with patch.dict(os.environ, {}, clear=True), patch.object(self.m.urllib.request, 'build_opener') as build:
            build.return_value.open.return_value = self.response(b'{"schema":"kosif.proplan.v1"}', url=self.m.ORIGIN+'/api/plan')
            self.assertEqual(self.m.request('plan', {'task':'Launch'}, allow_remote=True)['schema'], 'kosif.proplan.v1')
            req = build.return_value.open.call_args.args[0]
            self.assertIsNone(req.get_header('Oai-sites-authorization'))
            self.assertEqual(json.loads(req.data), {'task':'Launch'})

    def test_empty_token_uses_anonymous_request(self):
        with patch.dict(os.environ, {'KOSIF_SITE_TOKEN': ''}, clear=True), patch.object(self.m.urllib.request, 'build_opener') as build:
            build.return_value.open.return_value = self.response()
            self.assertEqual(self.m.request('health'), {'ok': True})
            self.assertIsNone(build.return_value.open.call_args.args[0].get_header('Oai-sites-authorization'))

    def test_anonymous_post_operations_require_approval(self):
        with patch.dict(os.environ, {}, clear=True), patch.object(self.m.urllib.request, 'build_opener') as build:
            for operation in ('plan', 'validate', 'compile'):
                with self.assertRaises(self.m.BridgeError):
                    self.m.request(operation, {'task':'Launch'})
            build.assert_not_called()

    def test_invalid_optional_token_fails_before_network(self):
        for token in ('bad\ntoken', 'space token', 'رمز', 'x'*16385):
            with self.subTest(token_length=len(token)), patch.dict(os.environ, {'KOSIF_SITE_TOKEN':token}, clear=True), patch.object(self.m.urllib.request, 'build_opener') as build:
                with self.assertRaises(self.m.BridgeError): self.m.request('health')
                build.assert_not_called()

    def test_optional_token_in_payload_is_refused(self):
        with patch.dict(os.environ, {'KOSIF_SITE_TOKEN':'secret'}, clear=True), patch.object(self.m.urllib.request, 'build_opener') as build:
            with self.assertRaises(self.m.BridgeError): self.m.request('plan', {'task':'secret'}, allow_remote=True)
            build.assert_not_called()

    def test_anonymous_html_response_is_refused(self):
        with patch.dict(os.environ, {}, clear=True), patch.object(self.m.urllib.request, 'build_opener') as build:
            build.return_value.open.return_value = self.response(b'<html>login</html>', content_type='text/html')
            with self.assertRaises(self.m.BridgeError): self.m.request('health')

    def test_anonymous_access_denial_does_not_retry(self):
        with patch.dict(os.environ, {}, clear=True), patch.object(self.m.urllib.request, 'build_opener') as build:
            build.return_value.open.side_effect = urllib.error.HTTPError(self.m.ORIGIN, 403, 'Denied', {}, io.BytesIO(b'private'))
            with self.assertRaises(self.m.BridgeError): self.m.request('health')
            self.assertEqual(build.return_value.open.call_count, 1)

    def test_exact_origin_and_header(self):
        with patch.dict(os.environ, {'KOSIF_SITE_TOKEN':'secret'}), patch.object(self.m.urllib.request, 'build_opener') as build:
            build.return_value.open.return_value = self.response(url=self.m.ORIGIN+'/api/plan')
            self.m.request('plan', {'task':'Arabic launch','seconds':12,'fps':30,'aspect':'9:16','mode':'pro'}, allow_remote=True)
            req = build.return_value.open.call_args.args[0]
            self.assertEqual(req.full_url, self.m.ORIGIN+'/api/plan')
            self.assertEqual(req.get_header('Oai-sites-authorization'), 'secret')
            self.assertEqual(json.loads(req.data)['task'], 'Arabic launch')
            self.assertEqual(build.return_value.open.call_args.kwargs['timeout'], 20)

    def test_redirect_handler_rejects_even_same_origin(self):
        with self.assertRaises(self.m.BridgeError):
            self.m.NoRedirect().redirect_request(None,None,302,'redirect',{},self.m.ORIGIN+'/api/plan')

    def test_unexpected_final_origin_rejected(self):
        with patch.dict(os.environ, {'KOSIF_SITE_TOKEN':'secret'}), patch.object(self.m.urllib.request, 'build_opener') as build:
            build.return_value.open.return_value = self.response(url='https://evil.example/api/health')
            with self.assertRaises(self.m.BridgeError): self.m.request('health')

    def test_only_known_operations(self):
        for name in ['https://evil.example','../token','render','plan?leak=x']:
            with self.assertRaises(self.m.BridgeError): self.m.request(name,allow_remote=True)

    def test_response_size_bounded(self):
        with patch.dict(os.environ, {'KOSIF_SITE_TOKEN':'secret'}), patch.object(self.m.urllib.request, 'build_opener') as build:
            build.return_value.open.return_value = self.response(b'x'*(self.m.MAX_BYTES+1))
            with self.assertRaises(self.m.BridgeError): self.m.request('health')

    def test_request_size_bounded(self):
        with patch.dict(os.environ, {'KOSIF_SITE_TOKEN':'secret'}), patch.object(self.m.urllib.request, 'build_opener') as build:
            with self.assertRaises(self.m.BridgeError): self.m.request('plan', {'task':'x'*(self.m.MAX_BYTES+1)},allow_remote=True)
            build.assert_not_called()

    def test_errors_do_not_echo_remote_content_or_token(self):
        with patch.dict(os.environ, {'KOSIF_SITE_TOKEN':'secret'}), patch.object(self.m.urllib.request, 'build_opener') as build:
            build.return_value.open.side_effect = urllib.error.HTTPError(self.m.ORIGIN,401,'secret',{},io.BytesIO(b'secret'))
            with self.assertRaises(self.m.BridgeError) as ctx:self.m.request('health')
            self.assertNotIn('secret',str(ctx.exception))

    def test_bad_content_type_rejected(self):
        with patch.dict(os.environ, {'KOSIF_SITE_TOKEN':'secret'}), patch.object(self.m.urllib.request, 'build_opener') as build:
            build.return_value.open.return_value = self.response(content_type='text/html')
            with self.assertRaises(self.m.BridgeError):self.m.request('health')

    def test_credential_echo_is_never_returned(self):
        with patch.dict(os.environ, {'KOSIF_SITE_TOKEN':'super-secret-token'}), patch.object(self.m.urllib.request, 'build_opener') as build:
            build.return_value.open.return_value = self.response(b'{"echo":"super-secret-token"}')
            with self.assertRaises(self.m.BridgeError): self.m.request('health')

    def test_safe_cli_plan_payload(self):
        with patch.object(self.m,'request',return_value={'schema':'kosif.proplan.v1'}) as call, patch('sys.stdout',new_callable=io.StringIO):
            self.assertEqual(self.m.main(['plan','--task','Launch','--allow-remote']),0)
            call.assert_called_once_with('plan',{'task':'Launch','seconds':12,'fps':30,'aspect':'9:16','mode':'pro'},allow_remote=True)

    def test_project_creates_new_directory_without_execution(self):
        with tempfile.TemporaryDirectory() as root:
            target = Path(root)/'new-project'
            self.m.write_project({'project_html':'<!doctype html><title>Demo</title>'},target)
            self.assertEqual((target/'index.html').read_text(),'<!doctype html><title>Demo</title>')

    def test_project_rejects_existing_directory(self):
        with tempfile.TemporaryDirectory() as root:
            with self.assertRaises(self.m.BridgeError): self.m.write_project({'project_html':'hello'},Path(root))

    def test_project_rejects_symlink_parent(self):
        with tempfile.TemporaryDirectory() as root:
            link=Path(root)/'link'
            try:
                link.symlink_to(Path(root),target_is_directory=True)
            except OSError as e:                       # Windows without the symlink privilege: the guard cannot be exercised here
                self.skipTest(f'symlinks unavailable: {e}')
            with self.assertRaises(self.m.BridgeError):self.m.write_project({'project_html':'hello'},link/'new')

    def test_no_project_for_unsupported_intent(self):
        with tempfile.TemporaryDirectory() as root:
            with self.assertRaises(self.m.BridgeError):self.m.write_project({'project_html':None},Path(root)/'new')
            self.assertFalse((Path(root)/'new').exists())

    def test_json_rejects_nonfinite(self):
        with self.assertRaises(self.m.BridgeError):self.m.parse_json(b'{"seconds":NaN}')

    def test_json_rejects_overflowed_numbers(self):
        with self.assertRaises(self.m.BridgeError):self.m.parse_json(b'{"nested":[1e400]}')

    def test_escaped_credential_echo_is_never_returned(self):
        token='token-"-backslash\\-end'
        with patch.dict(os.environ, {'KOSIF_SITE_TOKEN':token}), patch.object(self.m.urllib.request, 'build_opener') as build:
            build.return_value.open.return_value = self.response(json.dumps({'nested':[{'secret':token}]}).encode())
            with self.assertRaises(self.m.BridgeError): self.m.request('health')

    def test_project_rejects_parent_traversal(self):
        with tempfile.TemporaryDirectory() as root:
            with self.assertRaises(self.m.BridgeError):self.m.write_project({'project_html':'hello'},Path(root)/'..'/'escape')

    def test_existing_json_output_preserved(self):
        with tempfile.TemporaryDirectory() as root:
            target=Path(root)/'out.json';target.write_text('keep')
            with self.assertRaises(self.m.BridgeError):self.m.output_json({'new':True},target)
            self.assertEqual(target.read_text(),'keep')

    def test_wrong_plan_schema_rejected(self):
        with tempfile.TemporaryDirectory() as root:
            target=Path(root)/'plan.json';target.write_text('{"schema":"wrong"}')
            with self.assertRaises(self.m.BridgeError):self.m.read_plan(target)

    def test_cli_compile_wraps_plan(self):
        with tempfile.TemporaryDirectory() as root:
            target=Path(root)/'plan.json';target.write_text('{"schema":"kosif.proplan.v1"}')
            with patch.object(self.m,'request',return_value={'manifest':{}}) as call, patch('sys.stdout',new_callable=io.StringIO):
                self.assertEqual(self.m.main(['compile','--plan',str(target),'--allow-remote']),0)
                call.assert_called_once_with('compile',{'plan':{'schema':'kosif.proplan.v1'}},allow_remote=True)

if __name__ == '__main__': unittest.main()
