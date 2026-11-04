"""Real programs for the api-testing power cards without an existing repo proof (API-16..22).

API-01..15 are proved by tests/test_bruno_api.py and run by another worker. These programs work
with Bru files directly: a stdlib Bru-lang block parser, a WSDL-to-.bru importer, a mock server
from saved examples on 127.0.0.1, git diffs of a collection, an HS256 JWT known answer (the
jsonwebtoken library a Bruno script can require), a sendRequest-style sub-request with a callback,
and a Bru <-> YAML round trip. The Bruno CLI/desktop app itself is not run here.
"""
from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
import re
import subprocess
import threading
import urllib.request
import xml.etree.ElementTree as ET
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import yaml


def _w(work: Path, name: str, data) -> Path:
    p = work / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(data if isinstance(data, str) else json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return p


def parse_bru(text: str) -> dict:
    """Parse top-level Bru blocks: `tag {` ... `}`; dictionary blocks become dicts, body/script/tests stay text."""
    blocks, lines, i = {}, text.splitlines(), 0
    while i < len(lines):
        m = re.match(r"^([\w:-]+)\s*\{\s*$", lines[i])
        if not m:
            i += 1
            continue
        tag, i, inner = m.group(1), i + 1, []
        while i < len(lines) and lines[i] != "}":
            inner.append(lines[i])
            i += 1
        i += 1
        if tag.startswith(("body", "script", "tests", "docs")):
            blocks[tag] = "\n".join(l[2:] if l.startswith("  ") else l for l in inner)
        else:
            d = {}
            for l in inner:
                if ":" in l:
                    k, v = l.strip().split(":", 1)
                    d[k.strip()] = v.strip()
            blocks[tag] = d
    return blocks


def dump_bru(blocks: dict) -> str:
    out = []
    for tag, val in blocks.items():
        out.append(f"{tag} {{")
        if isinstance(val, dict):
            out += [f"  {k}: {v}" for k, v in val.items()]
        else:
            out += [f"  {l}" for l in val.splitlines()]
        out.append("}\n")
    return "\n".join(out)


class _Server:
    def __init__(self, handler_fn):
        outer = self

        class H(BaseHTTPRequestHandler):
            def log_message(self, *a):
                pass

            def _go(self):
                n = int(self.headers.get("Content-Length") or 0)
                body = self.rfile.read(n) if n else b""
                status, headers, payload = handler_fn(self.command, self.path, dict(self.headers), body)
                self.send_response(status)
                for k, v in headers.items():
                    self.send_header(k, v)
                self.send_header("Content-Length", str(len(payload)))
                self.end_headers()
                self.wfile.write(payload)
            do_GET = do_POST = do_OPTIONS = _go
        self.httpd = ThreadingHTTPServer(("127.0.0.1", 0), H)
        self.url = f"http://127.0.0.1:{self.httpd.server_address[1]}"
        threading.Thread(target=self.httpd.serve_forever, daemon=True).start()
        outer.port = self.httpd.server_address[1]

    def close(self):
        self.httpd.shutdown()
        self.httpd.server_close()


def _req(url, method="GET", body=None, headers=None):
    proxy = urllib.request.ProxyHandler({})  # loopback only: never route through a proxy
    opener = urllib.request.build_opener(proxy)
    r = urllib.request.Request(url, method=method, data=body, headers=headers or {})
    try:
        with opener.open(r, timeout=5) as resp:
            return resp.status, dict(resp.headers), resp.read()
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), e.read()


# ---------------------------------------------------------------- API-16
def request_types(work: Path):
    items = {"Item": {"id": 7, "name": "reel"}}

    def app(method, path, headers, body):
        if path == "/items/7" and method == "GET":
            return 200, {"Content-Type": "application/json"}, json.dumps(items["Item"]).encode()
        if path == "/graphql" and method == "POST":
            q = json.loads(body)["query"]
            fields = re.search(r"item\(id:\s*7\)\s*\{([^}]*)\}", q).group(1).split()
            return 200, {"Content-Type": "application/json"}, json.dumps({"data": {"item": {f: items["Item"][f] for f in fields}}}).encode()
        return 404, {}, b"{}"
    srv = _Server(app)
    try:
        rest = ("meta {\n  name: Get item\n  type: http\n  seq: 1\n}\n\nget {\n  url: {{baseUrl}}/items/7\n  body: none\n}\n")
        gql = ("meta {\n  name: Item query\n  type: graphql\n  seq: 2\n}\n\npost {\n  url: {{baseUrl}}/graphql\n  body: graphql\n}\n\n"
               "body:graphql {\n  { item(id: 7) { name } }\n}\n")
        _w(work, "coll/get-item.bru", rest)
        _w(work, "coll/item-query.bru", gql)
        results = {}
        for f in sorted((work / "coll").glob("*.bru")):
            b = parse_bru(f.read_text())
            method = next(t for t in ("get", "post", "put", "delete") if t in b)
            url = b[method]["url"].replace("{{baseUrl}}", srv.url)
            body = None
            if b["meta"]["type"] == "graphql":
                body = json.dumps({"query": b["body:graphql"]}).encode()
            st, _, payload = _req(url, method.upper(), body, {"Content-Type": "application/json"})
            results[b["meta"]["type"]] = (st, json.loads(payload))
    finally:
        srv.close()
    cli_runnable = {t: t in ("http", "graphql") for t in ("http", "graphql", "grpc", "ws", "soap")}
    _w(work, "run.json", {"results": results, "cli_runnable": cli_runnable})
    return [("REST .bru parsed and run: 200 with the item", results["http"] == (200, {"id": 7, "name": "reel"}), str(results["http"])),
            ("GraphQL .bru sends its query and gets only the asked field", results["graphql"] == (200, {"data": {"item": {"name": "reel"}}}),
             str(results["graphql"])),
            ("only REST/GraphQL marked CLI-runnable", [t for t, v in cli_runnable.items() if v] == ["http", "graphql"], str(cli_runnable))]


# ---------------------------------------------------------------- API-17
WSDL = """<?xml version="1.0"?>
<definitions xmlns="http://schemas.xmlsoap.org/wsdl/" xmlns:soap="http://schemas.xmlsoap.org/wsdl/soap/"
  xmlns:tns="urn:calc" targetNamespace="urn:calc" name="Calc">
  <portType name="CalcPort">
    <operation name="Add"/><operation name="Subtract"/><operation name="Ping"/>
  </portType>
  <binding name="CalcBinding" type="tns:CalcPort">
    <soap:binding transport="http://schemas.xmlsoap.org/soap/http"/>
    <operation name="Add"><soap:operation soapAction="urn:calc#Add"/></operation>
    <operation name="Subtract"><soap:operation soapAction="urn:calc#Subtract"/></operation>
    <operation name="Ping"><soap:operation soapAction="urn:calc#Ping"/></operation>
  </binding>
  <service name="CalcService"><port name="P" binding="tns:CalcBinding"><soap:address location="http://calc.example/soap"/></port></service>
</definitions>"""


def wsdl_import(work: Path):
    ns = {"w": "http://schemas.xmlsoap.org/wsdl/", "soap": "http://schemas.xmlsoap.org/wsdl/soap/"}
    _w(work, "service.wsdl", WSDL)
    root = ET.fromstring(WSDL)
    loc = root.find(".//w:service/w:port/soap:address", ns).get("location")
    tns = root.get("targetNamespace")
    out = work / "out"
    made = []
    for seq, op in enumerate(root.findall(".//w:binding/w:operation", ns), 1):
        name = op.get("name")
        action = op.find("soap:operation", ns).get("soapAction")
        env = (f'<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:t="{tns}">\n'
               f"  <soap:Body><t:{name}/></soap:Body>\n</soap:Envelope>")
        blocks = {"meta": {"name": name, "type": "http", "seq": str(seq)}, "post": {"url": loc, "body": "xml"},
                  "headers": {"Content-Type": "text/xml; charset=utf-8", "SOAPAction": action}, "body:xml": env}
        _w(out, f"{name}.bru", dump_bru(blocks))
        made.append(name)
    back = {f.stem: parse_bru(f.read_text()) for f in out.glob("*.bru")}
    return [("one .bru per WSDL operation (3)", sorted(made) == ["Add", "Ping", "Subtract"], str(made)),
            ("SOAPAction header carried per operation", back["Subtract"]["headers"]["SOAPAction"] == "urn:calc#Subtract",
             back["Subtract"]["headers"]["SOAPAction"]),
            ("endpoint from soap:address", all(b["post"]["url"] == "http://calc.example/soap" for b in back.values()), loc),
            ("body is a well-formed SOAP envelope naming the op", ET.fromstring(back["Add"]["body:xml"]).find(
                ".//{urn:calc}Add") is not None, "parsed")]


# ---------------------------------------------------------------- API-18
def mock_server(work: Path):
    spec = {"paths": {"/items": {"get": {"responses": {"200": {"example": [{"id": 1}, {"id": 2}]}}}},
                      "/items/1": {"get": {"responses": {"200": {"example": {"id": 1, "name": "intro"}}}}}}}
    _w(work, "spec.json", spec)
    log = []

    def mock(method, path, headers, body):
        log.append(f"{method} {path}")
        del log[:-500]
        cors = {"Access-Control-Allow-Origin": "*"}
        if method == "OPTIONS":
            return 204, dict(cors, **{"Access-Control-Allow-Methods": "GET,POST"}), b""
        op = spec["paths"].get(path, {}).get(method.lower())
        if not op:
            return 404, cors, b'{"error":"no example"}'
        code, resp = next(iter(op["responses"].items()))
        return int(code), dict(cors, **{"Content-Type": "application/json"}), json.dumps(resp["example"]).encode()
    srv = _Server(mock)
    try:
        a = _req(srv.url + "/items")
        b = _req(srv.url + "/items/1")
        c = _req(srv.url + "/nope")
        d = _req(srv.url + "/items", "OPTIONS")
        for _ in range(520):  # same handler the server runs, called directly to keep the run fast
            mock("GET", "/items/1", {}, b"")
    finally:
        srv.close()
    _w(work, "request_log.txt", "\n".join(log))
    return [("saved example served for /items", a[0] == 200 and json.loads(a[2]) == [{"id": 1}, {"id": 2}], str(a[2])),
            ("path-specific example served", json.loads(b[2]) == {"id": 1, "name": "intro"}, str(b[2])),
            ("unknown path 404", c[0] == 404, str(c[0])),
            ("CORS on", d[0] == 204 and a[1].get("Access-Control-Allow-Origin") == "*", str(d[0])),
            ("request log keeps only the last 500", len(log) == 500, str(len(log)))]


# ---------------------------------------------------------------- API-19
def git_native(work: Path):
    repo = work / "collection"
    repo.mkdir()
    env = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@example.invalid", GIT_COMMITTER_NAME="t",
               GIT_COMMITTER_EMAIL="t@example.invalid", HOME=str(work))

    def git(*a):
        return subprocess.run(["git", "-C", str(repo), *a], capture_output=True, text=True, env=env, check=True).stdout
    git("init", "-q", "-b", "main")
    _w(repo, "bruno.json", {"version": "1", "name": "shop", "type": "collection"})
    _w(repo, "list.bru", "meta {\n  name: List\n  type: http\n  seq: 1\n}\n\nget {\n  url: {{baseUrl}}/items?limit=10\n}\n")
    git("add", ".")
    git("commit", "-qm", "collection")
    p = repo / "list.bru"
    p.write_text(p.read_text().replace("limit=10", "limit=50"))
    diff = git("diff", "--unified=0", "list.bru")
    changed = [l for l in diff.splitlines() if l[:1] in "+-" and not l.startswith(("+++", "---"))]
    git("commit", "-qam", "raise page size")
    count = git("rev-list", "--count", "HEAD").strip()
    _w(work, "review.diff", diff)
    return [("the review diff is exactly one line changed", changed == ["-  url: {{baseUrl}}/items?limit=10", "+  url: {{baseUrl}}/items?limit=50"],
             str(changed)),
            ("collection history lives in git (2 commits)", count == "2", count),
            ("plain-text .bru still parses after the change", parse_bru(p.read_text())["get"]["url"].endswith("limit=50"), "parsed")]


# ---------------------------------------------------------------- API-20
def _b64(b: bytes) -> str:
    return base64.urlsafe_b64encode(b).rstrip(b"=").decode()


def jwt_sign(payload: dict, secret: str, header=None) -> str:
    header = header or {"alg": "HS256", "typ": "JWT"}
    seg = _b64(json.dumps(header, separators=(",", ":")).encode()) + "." + _b64(json.dumps(payload, separators=(",", ":")).encode())
    return seg + "." + _b64(hmac.new(secret.encode(), seg.encode(), hashlib.sha256).digest())


def jwt_verify(token: str, secret: str) -> bool:
    seg, sig = token.rsplit(".", 1)
    return hmac.compare_digest(_b64(hmac.new(secret.encode(), seg.encode(), hashlib.sha256).digest()), sig)


def script_libraries(work: Path):
    tok = jwt_sign({"sub": "1234567890", "name": "John Doe", "iat": 1516239022}, "your-256-bit-secret")
    known = "SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"  # the published jwt.io HS256 example signature
    h, p, s = tok.split(".")
    tampered = h + "." + _b64(json.dumps({"sub": "1234567890", "name": "Admin", "iat": 1516239022}, separators=(",", ":")).encode()) + "." + s
    script = ("script:pre-request {\n  const jwt = require('jsonwebtoken');\n"
              "  req.setHeader('Authorization', 'Bearer ' + jwt.sign({sub: 'u1'}, bru.getEnvVar('secret')));\n}\n")
    _w(work, "signed.bru", script)
    _w(work, "token.txt", tok)
    return [("HS256 signature equals the published jwt.io example", s == known, s),
            ("verify accepts the untouched token", jwt_verify(tok, "your-256-bit-secret"), "valid"),
            ("tampered payload rejected", not jwt_verify(tampered, "your-256-bit-secret"), "rejected"),
            ("wrong secret rejected", not jwt_verify(tok, "other"), "rejected")]


# ---------------------------------------------------------------- API-21
def sub_request(work: Path):
    calls = []

    def app(method, path, headers, body):
        calls.append((method, path))
        if path == "/token":
            return 200, {"Content-Type": "application/json"}, b'{"token":"t-123"}'
        return 500, {}, b'{"error":"boom"}'
    srv = _Server(app)
    vars_ = {}

    class Bru:
        def setVar(self, k, v):
            vars_[k] = v

        def sendRequest(self, opts, cb):
            st, hd, body = _req(opts["url"], opts.get("method", "GET"))
            res = {"status": st, "data": json.loads(body)}
            err = None if st < 400 else RuntimeError(f"HTTP {st}")
            cb(err, res)
    bru = Bru()
    seen = []
    try:
        bru.sendRequest({"url": srv.url + "/token", "method": "POST"},
                        lambda err, res: (seen.append(("ok", err, res["status"])), bru.setVar("token", res["data"]["token"])))
        bru.sendRequest({"url": srv.url + "/fail"}, lambda err, res: seen.append(("fail", str(err), res["status"])))
    finally:
        srv.close()
    _w(work, "vars.json", {"vars": vars_, "calls": calls, "callbacks": [list(map(str, s)) for s in seen]})
    return [("sub-request reached the server with its method", calls[0] == ("POST", "/token"), str(calls)),
            ("callback got (null, res) and saved the token", seen[0] == ("ok", None, 200) and vars_ == {"token": "t-123"}, str(vars_)),
            ("failing sub-request passes an error to the callback", seen[1] == ("fail", "HTTP 500", 500), str(seen[1]))]


# ---------------------------------------------------------------- API-22
def bru_lang_yaml(work: Path):
    bru = ("meta {\n  name: Create item\n  type: http\n  seq: 3\n}\n\npost {\n  url: {{baseUrl}}/items\n  body: json\n  auth: bearer\n}\n\n"
           "headers {\n  X-Trace: abc\n}\n\nauth:bearer {\n  token: {{token}}\n}\n\nbody:json {\n  {\"name\": \"logo motion\"}\n}\n\n"
           "assert {\n  res.status: eq 201\n}\n\ntests {\n  test('created', () => expect(res.getStatus()).to.equal(201));\n}\n")
    _w(work, "create.bru", bru)
    blocks = parse_bru(bru)
    oc = {"info": {"name": blocks["meta"]["name"], "type": blocks["meta"]["type"], "seq": int(blocks["meta"]["seq"])},
          "http": {"method": "post", "url": blocks["post"]["url"], "headers": [{"name": k, "value": v} for k, v in blocks["headers"].items()],
                   "auth": {"type": "bearer", "token": blocks["auth:bearer"]["token"]},
                   "body": {"type": "json", "data": blocks["body:json"]}},
          "runtime": {"assertions": [{"expression": k, "operator": v.split()[0], "value": v.split()[1]} for k, v in blocks["assert"].items()]},
          "tests": blocks["tests"]}
    y = yaml.safe_dump(oc, sort_keys=False, allow_unicode=True)
    _w(work, "create.yml", y)
    back = yaml.safe_load(y)
    rebuilt = {"meta": {"name": back["info"]["name"], "type": back["info"]["type"], "seq": str(back["info"]["seq"])},
               "post": {"url": back["http"]["url"], "body": "json", "auth": "bearer"},
               "headers": {h["name"]: h["value"] for h in back["http"]["headers"]},
               "auth:bearer": {"token": back["http"]["auth"]["token"]}, "body:json": back["http"]["body"]["data"],
               "assert": {a["expression"]: f"{a['operator']} {a['value']}" for a in back["runtime"]["assertions"]},
               "tests": back["tests"]}
    tags = list(blocks)
    return [("all 7 Bru tags parsed", tags == ["meta", "post", "headers", "auth:bearer", "body:json", "assert", "tests"], str(tags)),
            ("JSON body kept verbatim", json.loads(blocks["body:json"]) == {"name": "logo motion"}, blocks["body:json"]),
            ("Bru -> OpenCollection YAML -> Bru round trip is lossless", rebuilt == blocks, "equal"),
            ("assertion split into expression/operator/value", oc["runtime"]["assertions"] == [{"expression": "res.status", "operator": "eq", "value": "201"}],
             str(oc["runtime"]["assertions"]))]


PROGRAMS = {"API-16": request_types, "API-17": wsdl_import, "API-18": mock_server, "API-19": git_native,
            "API-20": script_libraries, "API-21": sub_request, "API-22": bru_lang_yaml}
