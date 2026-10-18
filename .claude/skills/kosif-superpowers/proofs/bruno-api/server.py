#!/usr/bin/env python3
"""Tiny owned test API for the Bruno proof (stdlib only). python3 server.py [port]"""
import json
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

TOKEN = "kosif-demo-token"
ITEMS = {1: {"id": 1, "name": "ريل الجمعة", "price": 0}}


class H(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def send(self, code, obj):
        body = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def authed(self):
        return self.headers.get("Authorization") == f"Bearer {TOKEN}"

    def body(self):
        n = int(self.headers.get("Content-Length") or 0)
        return json.loads(self.rfile.read(n) or b"{}")

    def do_GET(self):
        if self.path == "/health":
            return self.send(200, {"status": "ok"})
        if not self.authed():
            return self.send(401, {"error": "unauthorized"})
        if self.path == "/items":
            return self.send(200, {"items": list(ITEMS.values()), "count": len(ITEMS)})
        if self.path.startswith("/items/"):
            i = int(self.path.rsplit("/", 1)[1])
            return self.send(200, ITEMS[i]) if i in ITEMS else self.send(404, {"error": "not found"})
        self.send(404, {"error": "no route"})

    def do_POST(self):
        if self.path == "/login":
            b = self.body()
            ok = b.get("user") == "kosif" and b.get("password") == "demo"
            return self.send(200, {"token": TOKEN}) if ok else self.send(403, {"error": "bad credentials"})
        if self.path == "/items":
            if not self.authed():
                return self.send(401, {"error": "unauthorized"})
            b = self.body()
            if not b.get("name") or not isinstance(b.get("price"), (int, float)) or b["price"] < 0:
                return self.send(422, {"error": "invalid item"})
            i = max(ITEMS) + 1
            ITEMS[i] = {"id": i, "name": b["name"], "price": b["price"]}
            return self.send(201, ITEMS[i])
        self.send(404, {"error": "no route"})


if __name__ == "__main__":
    ThreadingHTTPServer(("127.0.0.1", int(sys.argv[1]) if len(sys.argv) > 1 else 8787), H).serve_forever()
