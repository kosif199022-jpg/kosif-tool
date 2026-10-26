import io, json, os, sys, tempfile, unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import render_client as c

M={'schema':'kosif.motion.manifest.v1','title':'test','width':1920,'height':1080,'fps':24,'duration':2,'scenes':[{'id':'one','start_frame':0,'end_frame_exclusive':48,'title':'test','subtitle':'','camera':'slow_push','accent':'#a7e8d0'}]}
class Response(io.BytesIO):
    def __init__(self,data,kind='application/json',url=None):
        super().__init__(data);self.headers={'Content-Type':kind};self.url=url
    def geturl(self):return self.url
class Tests(unittest.TestCase):
    def test_pin(self):
        for path in ['https://evil.test','//evil.test','/api/render/jobs/../status','/api/render/status?token=x']:
            with self.assertRaises(c.RenderError):c.make_request('GET',path)
        with self.assertRaises(c.RenderError):c.NoRedirect().redirect_request(None,None,302,'',{},'https://evil.test')
    def test_no_auth(self):
        with patch.dict(os.environ,{'KOSIF_SITE_TOKEN':'not-forwarded'}):
            req=c.make_request('GET','/api/render/status')
            self.assertEqual(req.full_url,c.ORIGIN+'/api/render/status')
            self.assertFalse(any('authorization' in k.lower() for k in req.headers))
    def test_scale_limits(self):
        m=c.prepare_manifest(M);self.assertEqual((m['width'],m['height']),(1280,720))
        for override in [{'fps':60},{'duration':31},{'width':float('nan')}]:
            with self.assertRaises(c.RenderError):c.prepare_manifest({**M,**override})
    def test_not_2d(self):
        with patch.object(c,'api') as api:
            with self.assertRaises(c.RenderError):c.compile_plan({'intent':'3d_motion'})
            api.assert_not_called()
    def test_config_failure(self):
        with patch.object(c,'api',return_value={'configured':False,'ready':False}):
            with self.assertRaises(c.RenderError):c.check_status()
    def test_cancel(self):
        with tempfile.TemporaryDirectory() as d, patch.object(c,'check_status'), patch.object(c,'compile_plan',return_value=c.prepare_manifest(M)),patch.object(c,'api',side_effect=[{'job_id':'a'*24,'job_token':'b'*43},KeyboardInterrupt,{'status':'cancelled'}]) as api:
            with self.assertRaises(KeyboardInterrupt):c.render({},Path(d)/'new.mp4',allow_remote=True)
            self.assertEqual(api.call_args.args[:2],('DELETE','/api/render/jobs/'+'a'*24))
            self.assertEqual(api.call_args.kwargs['token'],'b'*43)
    def test_download(self):
        good=b'\x00\x00\x00\x18ftypisom'+b'0'*20
        with tempfile.TemporaryDirectory() as d:
            out=Path(d)/'new.mp4'
            url=c.ORIGIN+'/api/render/jobs/'+'a'*24+'/video'
            for raw,kind in [(good,'text/html'),(b'garbage','video/mp4'),(good*10,'video/mp4')]:
                with patch.object(c,'open_response',return_value=Response(raw,kind,url)),patch.object(c,'MAX_VIDEO_BYTES',100):
                    with self.assertRaises(c.RenderError):c.download('a'*24,'b'*43,out,10**20)
                self.assertFalse(out.exists());self.assertFalse(list(Path(d).glob('*.partial')))
            with patch.object(c,'open_response',return_value=Response(good,'video/mp4',url)):
                c.download('a'*24,'b'*43,out,10**20)
            self.assertEqual(out.read_bytes(),good)
            with self.assertRaises(c.RenderError):c.checked_output(out)
    def test_consent(self):
        with patch.object(c,'api') as api:
            with self.assertRaises(c.RenderError):c.render({},Path('/tmp/new.mp4'),allow_remote=False)
            api.assert_not_called()
    def test_validation_and_submission(self):
        responses=[{'valid':True},{'manifest':M,'handoff':{'commands':[['forbidden']]}}]
        with patch.object(c,'api',side_effect=responses) as api:
            result=c.compile_plan({'intent':'2d_motion'})
            self.assertEqual(result['width'],1280)
            self.assertEqual(api.call_args_list[0].args[:2],('POST','/api/validate'))
        with patch.object(c,'api',return_value={'valid':False}) as api:
            with self.assertRaises(c.RenderError):c.compile_plan({'intent':'2d_motion'})
            self.assertEqual(api.call_count,1)
    def test_http_json_bounds_and_redirect(self):
        url=c.ORIGIN+'/api/render/status'
        for data,kind in [(b'{}','text/html'),(b'x'*(c.MAX_JSON_BYTES+1),'application/json')]:
            with patch.object(c,'open_response',return_value=Response(data,kind,url)):
                with self.assertRaises(c.RenderError):c.api('GET','/api/render/status')
        opener=unittest.mock.Mock();opener.open.return_value=Response(b'{}',url='https://evil.test')
        with patch.object(c.urllib.request,'build_opener',return_value=opener):
            with self.assertRaises(c.RenderError):c.open_response(c.make_request('GET','/api/render/status'),10**20)
    def test_capability_header_only(self):
        token='b'*43
        req=c.make_request('GET','/api/render/jobs/'+'a'*24,token=token)
        self.assertEqual(req.get_header('X-job-token'),token)
        self.assertNotIn(token,req.full_url)
        with self.assertRaises(c.RenderError):c.make_request('GET','/api/render/status',token=token)
    def test_no_overwrite_race(self):
        good=b'\x00\x00\x00\x18ftypisom'+b'0'*20
        with tempfile.TemporaryDirectory() as d:
            out=Path(d)/'new.mp4'
            def response(*args):
                out.write_bytes(b'keep');return Response(good,'video/mp4')
            with patch.object(c,'open_response',side_effect=response):
                with self.assertRaises(c.RenderError):c.download('a'*24,'b'*43,out,10**20)
            self.assertEqual(out.read_bytes(),b'keep')
            self.assertFalse(list(Path(d).glob('*.partial')))
    def test_declared_size_and_secret_output(self):
        good=b'\x00\x00\x00\x18ftypisom'+b'0'*20
        with tempfile.TemporaryDirectory() as d:
            for size in ('1',str(c.MAX_VIDEO_BYTES+1),'900','invalid'):
                r=Response(good,'video/mp4');r.headers['Content-Length']=size
                with patch.object(c,'open_response',return_value=r):
                    with self.assertRaises(c.RenderError):c.download('a'*24,'b'*43,Path(d)/'new.mp4',10**20)
            with patch.object(c,'check_status'),patch.object(c,'compile_plan',return_value=c.prepare_manifest(M)),patch.object(c,'download',return_value=len(good)),patch.object(c,'api',side_effect=[{'job_id':'a'*24,'job_token':'b'*43},{'status':'succeeded','progress':1,'secret':'b'*43}]),patch('sys.stdout',new_callable=io.StringIO) as output:
                c.render({},Path(d)/'new.mp4',allow_remote=True)
                self.assertNotIn('b'*43,output.getvalue())
if __name__=='__main__':unittest.main()
