"""Known-answer proof for proofs/general-graphify/graph_mindmap.py (GRAPH-17: graph -> communities -> mind map).

Builds a small NetworkX node-link graph.json with two communities, a stdlib hub without a source file
and hostile labels, runs the script and checks the exact Mermaid mindmap, the outline counts, the
degree ranking, label sanitising and the cross-community bridge count. Offline, stdlib only.
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / ".claude" / "skills" / "kosif-superpowers" / "proofs" / "general-graphify" / "graph_mindmap.py"

GRAPH = {
    "nodes": [
        {"id": "a1", "label": "parse()", "source_file": "src/parser.py", "community": 0},
        {"id": "a2", "label": "Lexer[tok]", "source_file": "src/parser.py", "community": 0},
        {"id": "a3", "label": "Token", "source_file": "src/tokens.py", "community": 0},
        {"id": "b1", "label": "render", "source_file": "src/render.py", "community": 1},
        {"id": "b2", "label": "<script>Canvas", "source_file": "src/render.py", "community": 1},
        {"id": "os", "label": "os", "community": 1},                                  # stdlib hub
    ],
    "links": [
        {"source": "a1", "target": "a2"}, {"source": "a1", "target": "a3"}, {"source": "a2", "target": "a3"},
        {"source": "a1", "target": "b1"},                                             # bridge 0 <-> 1
        {"source": "b1", "target": "b2"}, {"source": "b1", "target": "os"}, {"source": "b2", "target": "os"},
        {"source": "a1", "target": "missing"},                                        # dangling: ignored
    ],
}


def run(graph: dict, *args: str) -> str:
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "myproj" / "graphify-out" / "graph.json"
        p.parent.mkdir(parents=True)
        p.write_text(json.dumps(graph), encoding="utf-8")
        done = subprocess.run([sys.executable, "-I", "-B", str(SCRIPT), str(p), *args],
                              capture_output=True, text=True, timeout=30)
    if done.returncode:
        raise AssertionError(done.stderr)
    return done.stdout


class MindMap(unittest.TestCase):
    def test_mermaid_block(self):
        out = run(GRAPH, "--top", "2")
        mer = out.split("```mermaid\n", 1)[1].split("```", 1)[0].splitlines()
        self.assertEqual(mer, [
            "mindmap",
            "  root((myproj))",
            "    c0[parser.py +1 · 3]",
            "      parse",          # degree 3 (dangling edge not counted), brackets stripped
            "      Lexertok",
            "    c1[render.py · 3]",
            "      render",
            "      scriptCanvas",
        ])

    def test_outline_and_bridges(self):
        out = run(GRAPH, "--title", "Demo (v1)")
        self.assertIn("# Demo v1: 6 nodes, 8 edges, 2 communities", out)
        self.assertIn("- **parser.py +1** (community 0, 3 nodes): `parse` (3), `Lexertok` (2), `Token` (2)", out)
        self.assertIn("- **render.py** (community 1, 3 nodes): `render` (3), `scriptCanvas` (2)", out)
        self.assertNotIn("`os`", out)                     # hub without a source file is not a leaf
        self.assertTrue(out.rstrip().endswith("- parser.py +1 <-> render.py: 1 edges"))

    def test_edges_key_and_empty_labels(self):
        g = {"nodes": [{"id": 1, "label": "", "source_file": "x.py", "community": 5}], "edges": []}
        out = run(g)
        self.assertIn("    c5[x.py · 1]\n      ?\n", out)
        self.assertIn(": 1 nodes, 0 edges, 1 communities", out)


if __name__ == "__main__":
    unittest.main()
