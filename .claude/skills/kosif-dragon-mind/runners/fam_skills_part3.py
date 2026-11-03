"""skills part 3: catalog SKILL.md files (kosif-atlas vendor skills) turned into real programs.

Each runner does the skill's core procedure on a deterministic fixture in the work folder, measures the
result, and runs the same measurement where the method was not applied (negative control).
Real engines used where the skill names one: mypy, pyright, ruff, pytest, rustc/clippy/rustfmt, go vet/gofmt/
go test, javac/java, tsc, ripgrep, git, pandoc, esbuild + React + headless Chrome. Skills whose engine is not
on this machine (dotnet, fd, fzf, ty, the LiveKit `lk` CLI) are listed in GAPS rather than imitated.
Judgment-heavy skills (C-level reviews, legal/contract reviews, book outlining) are implemented through
their quantitative rules and gates only: the checks prove the rules were computed, not the quality of prose.
"""
import json
import os
import re
import shutil
import subprocess
import textwrap
from pathlib import Path

from _harness import card, check, fx

P = "skill:kosif-superpowers/vendor/kosif-atlas/skills/"
REPO = Path(__file__).resolve().parents[4]
SKROOT = REPO / ".claude/skills/kosif-superpowers/vendor/kosif-atlas/skills"

GAPS: dict = {
    P + "117-programming/304-writing-csharp": "needs the .NET SDK (dotnet build/test/format); no dotnet on this machine",
    P + "1226-fd/2908-fd": "the fd binary is not installed (nor fdfind) and the skill says stop rather than install or imitate it",
    P + "1230-fzf/2910-fzf": "the fzf binary is not installed; the skill is the fzf tool itself (interactive picker), not imitable",
    P + "1228-fuzzy-filter/2909-fuzzy-filter": "the pipeline's ranking stage is `fzf --filter`; fzf is not installed here",
    P + "1271-ty/2949-ty": "Astral's ty type checker is not installed and installing is out of scope (no network)",
    P + "1426-livekit-skills/3391-debugging-livekit-agents": "needs the LiveKit `lk agent debugger` CLI and an agent with its own LLM credentials",
    P + "1426-livekit-skills/3394-running-livekit-simulations": "needs `lk agent simulate`, a LiveKit Cloud project and paid LLM-judged runs",
}


# ---------------------------------------------------------------- helpers
def wt(path, text):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(text).lstrip("\n"), encoding="utf-8")
    return path


def jw(path, obj):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=1), encoding="utf-8")
    return path


def sh(cmd, cwd=None, env=None, timeout=60, stdin=None):
    e = dict(os.environ)
    e.update(env or {})
    done = subprocess.run([str(c) for c in cmd], cwd=str(cwd) if cwd else None, env=e, capture_output=True,
                          text=True, timeout=timeout, input=stdin, stdin=None if stdin is not None else subprocess.DEVNULL)
    return done.returncode, done.stdout + done.stderr


def _rust_bin(name):
    for tc in sorted(Path.home().glob(".rustup/toolchains/*/bin")):
        if (tc / name).exists():
            return str(tc / name)
    return shutil.which(name) or name


def md_table(rows, head):
    out = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    out += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    return "\n".join(out)


# ================================================================ programming
@card(P + "1112-python-scripting/2534-python-typing")
def python_typing(task, wd):
    """Typed boundary: untrusted JSON as object, narrowed with isinstance, bool rejected; mypy --strict."""
    bad = wt(wd / "cfg_bad.py", '''
        import json

        def parse(raw):
            data = json.loads(raw)
            return {"name": data["name"], "port": data["port"]}

        def port_of(cfg: dict[str, object]) -> int:
            return cfg["port"]
        ''')
    good = wt(wd / "cfg_good.py", '''
        import json
        from typing import TypedDict


        class Cfg(TypedDict):
            name: str
            port: int


        def parse(raw: str) -> Cfg:
            data: object = json.loads(raw)
            if not isinstance(data, dict):
                raise ValueError("config must be an object")
            name = data.get("name")
            port = data.get("port")
            if not isinstance(name, str):
                raise ValueError("name must be a string")
            if isinstance(port, bool) or not isinstance(port, int):
                raise ValueError("port must be an integer")
            return {"name": name, "port": port}


        def port_of(cfg: Cfg) -> int:
            return cfg["port"]
        ''')
    rc, out = sh(["mypy", "--strict", "--no-incremental", "--cache-dir", wd / ".mypy", "--no-error-summary",
                  bad.name, good.name], cwd=wd)
    errs = [ln for ln in out.splitlines() if ": error:" in ln]
    bad_errs = [e for e in errs if e.startswith("cfg_bad.py")]
    good_errs = [e for e in errs if e.startswith("cfg_good.py")]
    codes = sorted(set(re.findall(r"\[([a-z-]+)\]", "\n".join(bad_errs))))
    rt = sh(["python3", "-I", "-c", textwrap.dedent('''
        import json, sys
        sys.path.insert(0, ".")
        import cfg_good, cfg_bad
        r = {}
        try:
            cfg_good.parse('{"name":"api","port":true}'); r["good_bool"] = "accepted"
        except ValueError: r["good_bool"] = "rejected"
        r["good_ok"] = cfg_good.parse('{"name":"api","port":8080}')
        r["bad_bool"] = "accepted" if cfg_bad.parse('{"name":"api","port":true}')["port"] is True else "rejected"
        print(json.dumps(r))''')], cwd=wd)[1].strip().splitlines()[-1]
    rt = json.loads(rt)
    rep = jw(wd / "typing_report.json", {"mypy_errors": errs, "codes": codes, "runtime": rt})
    return [
        check("mypy --strict finds the planted errors in the untyped boundary", len(bad_errs) >= 2, len(bad_errs), ">=2"),
        check("planted error kinds caught (untyped def + object returned as int)",
              "no-untyped-def" in codes and "return-value" in codes, codes, ["no-untyped-def", "return-value"]),
        check("fixed module is clean under mypy --strict", good_errs == [], good_errs, []),
        check("fixed parser rejects bool as port (bool is an int subclass)", rt["good_bool"] == "rejected", rt["good_bool"], "rejected"),
        check("fixed parser returns the typed record", rt["good_ok"] == {"name": "api", "port": 8080}, rt["good_ok"]),
        check("negative control: untyped parser lets port=true through", rt["bad_bool"] == "accepted", rt["bad_bool"], "accepted"),
    ], [rep, good]


def _clippy(src, wd, extra=()):
    return sh([_rust_bin("clippy-driver"), "--edition", "2021", "-D", "warnings", "--crate-type", "lib", *extra,
               "-o", wd / (Path(src).stem + ".rlib"), src], cwd=wd)


def _rust_test(src, wd):
    exe = wd / (Path(src).stem + "_test")
    rc, out = sh([_rust_bin("rustc"), "--edition", "2021", "--test", src, "-o", exe], cwd=wd)
    if rc:
        return rc, out
    return sh([exe], cwd=wd)


@card(P + "1113-rust-coding/2535-rust-coding")
def rust_coding(task, wd):
    """Enum state machine instead of boolean flags, Result instead of panic, Display; fmt + clippy + tests."""
    good = wt(wd / "order.rs", '''
        //! Order lifecycle modelled as an enum state machine.
        use std::fmt;

        /// The states an order can be in.
        #[derive(Debug, Clone, Copy, PartialEq, Eq)]
        pub enum OrderState {
            /// Created, not paid.
            Pending,
            /// Paid, not shipped.
            Paid,
            /// Shipped to the customer.
            Shipped,
        }

        /// A rejected transition.
        #[derive(Debug, PartialEq, Eq)]
        pub struct TransitionError {
            /// State the order was in.
            pub from: OrderState,
            /// Requested action.
            pub action: &'static str,
        }

        impl OrderState {
            /// Pay a pending order.
            pub fn pay(self) -> Result<Self, TransitionError> {
                match self {
                    OrderState::Pending => Ok(OrderState::Paid),
                    from => Err(TransitionError { from, action: "pay" }),
                }
            }

            /// Ship a paid order.
            pub fn ship(self) -> Result<Self, TransitionError> {
                match self {
                    OrderState::Paid => Ok(OrderState::Shipped),
                    from => Err(TransitionError { from, action: "ship" }),
                }
            }
        }

        impl fmt::Display for OrderState {
            fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
                let s = match self {
                    OrderState::Pending => "pending",
                    OrderState::Paid => "paid",
                    OrderState::Shipped => "shipped",
                };
                f.write_str(s)
            }
        }

        #[cfg(test)]
        mod tests {
            use super::*;

            #[test]
            fn happy_path() {
                let s = OrderState::Pending.pay().and_then(OrderState::ship);
                assert_eq!(s, Ok(OrderState::Shipped));
            }

            #[test]
            fn cannot_ship_unpaid() {
                let e = OrderState::Pending.ship().unwrap_err();
                assert_eq!(e.from, OrderState::Pending);
            }

            #[test]
            fn cannot_pay_twice() {
                assert!(OrderState::Paid.pay().is_err());
            }

            #[test]
            fn display() {
                assert_eq!(OrderState::Shipped.to_string(), "shipped");
            }
        }
        ''')
    bad = wt(wd / "order_flags.rs", '''
        pub struct Order { pub paid: bool, pub shipped: bool }
        impl Order {
            pub fn ship(&mut self) { if self.paid == true { self.shipped = true } else { panic!("unpaid") } }
        }
        ''')
    pre_rc, _ = sh([_rust_bin("rustfmt"), "--check", "--edition", "2021", good], cwd=wd)
    sh([_rust_bin("rustfmt"), "--edition", "2021", good], cwd=wd)
    fmt_rc, fmt_out = sh([_rust_bin("rustfmt"), "--check", "--edition", "2021", good], cwd=wd)
    cg_rc, cg_out = _clippy(good, wd)
    cb_rc, cb_out = _clippy(bad, wd)
    t_rc, t_out = _rust_test(good, wd)
    m = re.search(r"test result: ok\. (\d+) passed; (\d+) failed", t_out)
    passed = int(m.group(1)) if m else 0
    rep = wt(wd / "rust_report.txt", "rustfmt rc=%d\nclippy good rc=%d\n%s\nclippy flags rc=%d\n%s\ntests:\n%s\n"
             % (fmt_rc, cg_rc, cg_out, cb_rc, cb_out, t_out))
    return [
        check("hand-written source needed formatting (rustfmt --check failed before cargo fmt)", pre_rc != 0, pre_rc, "nonzero"),
        check("after rustfmt: --check clean", fmt_rc == 0, fmt_rc, 0),
        check("clippy -D warnings clean on enum state machine", cg_rc == 0, cg_out[-200:], ""),
        check("transition tests pass (4: happy path, invalid ship, double pay, Display)", t_rc == 0 and passed == 4, passed, 4),
        check("negative control: boolean-flag version fails clippy (bool_comparison)",
              cb_rc != 0 and "bool_comparison" in cb_out, cb_rc, "nonzero + bool_comparison"),
    ], [rep, good]


@card(P + "117-programming/308-writing-rust")
def writing_rust(task, wd):
    """Newtype + FromStr with typed error, secrets kept out of Debug; full gates fmt/clippy/test."""
    good = wt(wd / "ids.rs", '''
        use std::fmt;
        use std::str::FromStr;

        /// A validated user id.
        #[derive(Debug, Clone, PartialEq, Eq)]
        pub struct UserId(u32);

        /// Why a user id was rejected.
        #[derive(Debug, PartialEq, Eq)]
        pub enum UserIdError {
            /// Not a number.
            NotNumeric,
            /// Zero is reserved.
            Zero,
        }

        impl FromStr for UserId {
            type Err = UserIdError;
            fn from_str(s: &str) -> Result<Self, Self::Err> {
                let n: u32 = s.trim().parse().map_err(|_| UserIdError::NotNumeric)?;
                if n == 0 {
                    return Err(UserIdError::Zero);
                }
                Ok(UserId(n))
            }
        }

        impl fmt::Display for UserId {
            fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
                write!(f, "user-{}", self.0)
            }
        }

        /// An API token whose value never reaches Debug output.
        pub struct Token(String);

        impl Token {
            /// Wrap a secret.
            pub fn new(s: &str) -> Self {
                Token(s.to_owned())
            }

            /// Length of the secret, for checks that must not print it.
            pub fn len(&self) -> usize {
                self.0.len()
            }

            /// True when empty.
            pub fn is_empty(&self) -> bool {
                self.0.is_empty()
            }
        }

        impl fmt::Debug for Token {
            fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
                f.write_str("Token(REDACTED)")
            }
        }

        #[cfg(test)]
        mod tests {
            use super::*;

            #[test]
            fn valid() {
                assert_eq!("42".parse::<UserId>(), Ok(UserId(42)));
            }

            #[test]
            fn invalid() {
                assert_eq!("x".parse::<UserId>(), Err(UserIdError::NotNumeric));
            }

            #[test]
            fn boundary_zero() {
                assert_eq!("0".parse::<UserId>(), Err(UserIdError::Zero));
            }

            #[test]
            fn display() {
                assert_eq!(UserId(7).to_string(), "user-7");
            }

            #[test]
            fn debug_redacts() {
                let t = Token::new("sk-SECRET-123");
                assert!(!format!("{:?}", t).contains("SECRET"));
                assert_eq!(t.len(), 13);
            }
        }
        ''')
    bad = wt(wd / "ids_leaky.rs", '''
        #[derive(Debug)]
        pub struct Token(pub String);
        pub fn count(v: &Vec<u32>) -> usize { v.len() }
        fn main() { println!("{:?} {}", Token("sk-SECRET-123".to_string()), count(&vec![1])); }
        ''')
    fmt_rc, _ = sh([_rust_bin("rustfmt"), "--check", "--edition", "2021", good], cwd=wd)
    cg_rc, cg_out = _clippy(good, wd)
    t_rc, t_out = _rust_test(good, wd)
    m = re.search(r"test result: ok\. (\d+) passed", t_out)
    passed = int(m.group(1)) if m else 0
    b_rc, b_out = sh([_rust_bin("rustc"), "--edition", "2021", bad, "-o", wd / "leaky"], cwd=wd)
    leak = sh([wd / "leaky"])[1] if b_rc == 0 else ""
    cb_rc, cb_out = sh([_rust_bin("clippy-driver"), "--edition", "2021", "-D", "warnings", bad, "-o", wd / "leaky2"], cwd=wd)
    rep = wt(wd / "rust_gates.txt", "fmt=%d clippy=%d tests=%d\n%s\nleaky stdout: %s\nclippy leaky:\n%s" %
             (fmt_rc, cg_rc, passed, t_out, leak, cb_out))
    return [
        check("cargo-fmt equivalent: rustfmt --check clean", fmt_rc == 0, fmt_rc, 0),
        check("clippy -D warnings clean", cg_rc == 0, cg_out[-200:], ""),
        check("valid / invalid / boundary / Display / Debug-redaction tests pass", t_rc == 0 and passed == 5, passed, 5),
        check("negative control: derived Debug leaks the secret", "sk-SECRET-123" in leak, leak.strip(), "contains secret"),
        check("negative control: &Vec parameter fails clippy (ptr_arg)", cb_rc != 0 and "ptr_arg" in cb_out, cb_rc, "ptr_arg"),
    ], [rep, good]


GOENV = {"GOTOOLCHAIN": "local", "GOPROXY": "off", "GOFLAGS": "-mod=mod", "GO111MODULE": "on"}


@card(P + "117-programming/305-writing-go")
def writing_go(task, wd):
    """Thin main -> run(ctx,args,stdin,stdout,stderr) error, tested; gofmt -l, go vet, go test."""
    g = wd / "good"
    wt(g / "go.mod", "module example.com/greet\n\ngo 1.22\n")
    wt(g / "cmd/greet/main.go", '''
        // Command greet prints a greeting.
        package main

        import (
        \t"context"
        \t"fmt"
        \t"os"

        \t"example.com/greet/internal/cli"
        )

        func main() {
        \tif err := cli.Run(context.Background(), os.Args[1:], os.Stdin, os.Stdout, os.Stderr); err != nil {
        \t\tfmt.Fprintln(os.Stderr, err)
        \t\tos.Exit(2)
        \t}
        }
        '''.replace("\\t", "\t"))
    wt(g / "internal/cli/cli.go", '''
        // Package cli holds the testable command logic.
        package cli

        import (
        \t"context"
        \t"errors"
        \t"flag"
        \t"fmt"
        \t"io"
        )

        // ErrNoName is returned when no name is given.
        var ErrNoName = errors.New("greet: -name is required")

        // Run parses args and writes the greeting to stdout.
        func Run(ctx context.Context, args []string, _ io.Reader, stdout, stderr io.Writer) error {
        \tfs := flag.NewFlagSet("greet", flag.ContinueOnError)
        \tfs.SetOutput(stderr)
        \tname := fs.String("name", "", "who to greet")
        \tif err := fs.Parse(args); err != nil {
        \t\treturn err
        \t}
        \tif *name == "" {
        \t\treturn ErrNoName
        \t}
        \tif err := ctx.Err(); err != nil {
        \t\treturn err
        \t}
        \t_, err := fmt.Fprintf(stdout, "hello, %s\\n", *name)
        \treturn err
        }
        '''.replace("\\t", "\t"))
    wt(g / "internal/cli/cli_test.go", '''
        package cli

        import (
        \t"bytes"
        \t"context"
        \t"errors"
        \t"testing"
        )

        func TestRunGreets(t *testing.T) {
        \tvar out, errb bytes.Buffer
        \tif err := Run(context.Background(), []string{"-name", "Ada"}, nil, &out, &errb); err != nil {
        \t\tt.Fatal(err)
        \t}
        \tif got := out.String(); got != "hello, Ada\\n" {
        \t\tt.Fatalf("got %q", got)
        \t}
        }

        func TestRunMissingName(t *testing.T) {
        \tvar out, errb bytes.Buffer
        \terr := Run(context.Background(), nil, nil, &out, &errb)
        \tif !errors.Is(err, ErrNoName) {
        \t\tt.Fatalf("want ErrNoName, got %v", err)
        \t}
        }

        func TestRunCancelled(t *testing.T) {
        \tctx, cancel := context.WithCancel(context.Background())
        \tcancel()
        \tvar out, errb bytes.Buffer
        \tif err := Run(ctx, []string{"-name", "x"}, nil, &out, &errb); !errors.Is(err, context.Canceled) {
        \t\tt.Fatalf("want Canceled, got %v", err)
        \t}
        }
        '''.replace("\\t", "\t"))
    b = wd / "bad"
    wt(b / "go.mod", "module example.com/bad\n\ngo 1.22\n")
    wt(b / "main.go", 'package main\nimport ("fmt";"log")\nfunc main(){ name:="x"\n if name=="" { log.Fatal("no") }\n fmt.Printf("%d\\n", name) }\n')
    fmt_rc, fmt_out = sh(["gofmt", "-l", "."], cwd=g)
    vet_rc, vet_out = sh(["go", "vet", "./..."], cwd=g, env=GOENV, timeout=90)
    tst_rc, tst_out = sh(["go", "test", "-count=1", "-v", "./..."], cwd=g, env=GOENV, timeout=90)
    npass = tst_out.count("--- PASS")
    bf_rc, bf_out = sh(["gofmt", "-l", "."], cwd=b)
    bv_rc, bv_out = sh(["go", "vet", "./..."], cwd=b, env=GOENV, timeout=90)
    rep = wt(wd / "go_report.txt", "gofmt good: %r\nvet good rc=%d %s\ntest:\n%s\ngofmt bad: %r\nvet bad:\n%s" %
             (fmt_out, vet_rc, vet_out, tst_out, bf_out, bv_out))
    return [
        check("gofmt -l lists nothing", fmt_out.strip() == "", fmt_out.strip(), ""),
        check("go vet clean", vet_rc == 0, vet_out[-200:], ""),
        check("go test: 3 tests through the run() seam pass (ok, missing flag, cancelled ctx)",
              tst_rc == 0 and npass == 3, npass, 3),
        check("negative control: unformatted file is listed by gofmt", "main.go" in bf_out, bf_out.strip(), "main.go"),
        check("negative control: go vet flags the Printf %d/string mismatch", bv_rc != 0 and "wrong type" in bv_out, bv_rc, "nonzero"),
    ], [rep, g / "internal/cli/cli.go"]


@card(P + "117-programming/306-writing-java-kotlin")
def writing_java(task, wd):
    """Java rules measured at runtime: InterruptedException restores the interrupt flag; CPU work on a bounded pool."""
    wt(wd / "Work.java", '''
        import java.util.ArrayList;
        import java.util.List;
        import java.util.concurrent.ExecutorService;
        import java.util.concurrent.Executors;
        import java.util.concurrent.Future;

        public final class Work {
            private Work() { }

            /** Blocking wait that keeps the interrupt status (the rule). */
            public static boolean waitGood() {
                try {
                    Thread.sleep(10_000);
                    return false;
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    return Thread.currentThread().isInterrupted();
                }
            }

            /** Swallows the interrupt (what the rule forbids). */
            public static boolean waitBad() {
                try {
                    Thread.sleep(10_000);
                    return false;
                } catch (InterruptedException e) {
                    return Thread.currentThread().isInterrupted();
                }
            }

            /** CPU-bound sum on a pool sized to the processors. */
            public static long sumSquares(int n) throws Exception {
                int threads = Runtime.getRuntime().availableProcessors();
                ExecutorService pool = Executors.newFixedThreadPool(threads);
                try {
                    List<Future<Long>> parts = new ArrayList<>();
                    int chunk = (n + threads - 1) / threads;
                    for (int t = 0; t < threads; t++) {
                        final int lo = t * chunk + 1;
                        final int hi = Math.min(n, (t + 1) * chunk);
                        parts.add(pool.submit(() -> {
                            long s = 0;
                            for (long i = lo; i <= hi; i++) {
                                s += i * i;
                            }
                            return s;
                        }));
                    }
                    long total = 0;
                    for (Future<Long> f : parts) {
                        total += f.get();
                    }
                    return total;
                } finally {
                    pool.shutdown();
                }
            }

            private static boolean probe(boolean good) throws Exception {
                final boolean[] seen = new boolean[1];
                Thread th = new Thread(() -> seen[0] = good ? waitGood() : waitBad());
                th.start();
                Thread.sleep(100);
                th.interrupt();
                th.join(5_000);
                return seen[0];
            }

            public static void main(String[] args) throws Exception {
                System.out.println("{\\"good_flag\\":" + probe(true) + ",\\"bad_flag\\":" + probe(false)
                    + ",\\"sum\\":" + sumSquares(100_000) + ",\\"threads\\":" + Runtime.getRuntime().availableProcessors() + "}");
            }
        }
        ''')
    c_rc, c_out = sh(["javac", "-Xlint:all", "-Werror", "-d", wd / "classes", wd / "Work.java"], cwd=wd, timeout=60)
    r_rc, r_out = sh(["java", "-cp", wd / "classes", "Work"], cwd=wd, timeout=60)
    line = [ln for ln in r_out.splitlines() if ln.startswith("{")]
    res = json.loads(line[-1]) if line else {}
    n = 100_000
    expect = n * (n + 1) * (2 * n + 1) // 6
    res["not_run"] = "Kotlin half (ktlint/detekt/runTest) not run: no kotlinc on this machine"
    rep = jw(wd / "java_report.json", {"javac_rc": c_rc, "javac": c_out[-300:], "result": res})
    return [
        check("javac -Xlint:all -Werror compiles cleanly", c_rc == 0, c_rc, 0),
        check("interrupt status preserved after InterruptedException", res.get("good_flag") is True, res.get("good_flag"), True),
        check("bounded-pool CPU sum equals closed form n(n+1)(2n+1)/6", res.get("sum") == expect, res.get("sum"), expect),
        check("negative control: swallowing catch loses the interrupt flag", res.get("bad_flag") is False, res.get("bad_flag"), False),
    ], [rep, wd / "Work.java"]


@card(P + "117-programming/307-writing-python")
def writing_python(task, wd):
    """main(argv)->int CLI with argparse, explicit encoding, `raise ... from`; ruff + pyright + pytest."""
    wt(wd / "pyproject.toml", '''
        [project]
        name = "wc"
        version = "0.1.0"
        requires-python = ">=3.12"
        [tool.ruff]
        target-version = "py312"
        [tool.ruff.lint]
        select = ["E", "F", "B", "UP", "I"]
        ''')
    wt(wd / "wc/__init__.py", "")
    wt(wd / "wc/cli.py", '''
        """Count words in a UTF-8 text file."""

        import argparse
        import sys
        from collections.abc import Sequence
        from pathlib import Path


        class CountError(Exception):
            """The input could not be counted."""


        def count_words(path: Path) -> int:
            try:
                text = path.read_text(encoding="utf-8")
            except OSError as exc:
                raise CountError(f"cannot read {path}") from exc
            return len(text.split())


        def main(argv: Sequence[str] | None = None) -> int:
            parser = argparse.ArgumentParser(prog="wc")
            parser.add_argument("path", type=Path)
            args = parser.parse_args(argv)
            try:
                n = count_words(args.path)
            except CountError as exc:
                print(f"error: {exc}", file=sys.stderr)
                return 1
            print(n)
            return 0


        if __name__ == "__main__":
            raise SystemExit(main())
        ''')
    wt(wd / "tests/test_cli.py", '''
        from pathlib import Path

        import pytest

        from wc.cli import main


        def test_counts(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
            p = tmp_path / "a.txt"
            p.write_text("one two  three\\nfour", encoding="utf-8")
            assert main([str(p)]) == 0
            assert capsys.readouterr().out.strip() == "4"


        def test_missing_exit_1(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
            assert main([str(tmp_path / "nope.txt")]) == 1
            assert "cannot read" in capsys.readouterr().err
        ''')
    wt(wd / "bad/legacy.py", '''
        import os
        def count(path, seen=[]):
            try:
                return len(open(path).read().split())
            except OSError:
                raise RuntimeError("cannot read")
        ''')
    r_rc, r_out = sh(["ruff", "check", "--no-cache", "wc", "tests"], cwd=wd)
    f_rc, f_out = sh(["ruff", "format", "--check", "--no-cache", "wc", "tests"], cwd=wd)
    rb_rc, rb_out = sh(["ruff", "check", "--no-cache", "bad"], cwd=wd)
    bad_codes = sorted(set(re.findall(r"\b([A-Z]+\d{3,4})\b", rb_out)))
    p_rc, p_out = sh(["pytest", "-q", "-p", "no:cacheprovider", "tests"], cwd=wd,
                     env={"PYTHONPATH": str(wd)}, timeout=60)
    m = re.search(r"(\d+) passed", p_out)
    ty_rc, ty_out = sh(["mypy", "--strict", "--no-incremental", "--cache-dir", wd / ".mypy", "wc"], cwd=wd)
    rep = wt(wd / "python_gates.txt", "ruff rc=%d\n%s\nformat rc=%d\n%s\nruff bad:\n%s\npytest:\n%s\ntypes:\n%s"
             % (r_rc, r_out, f_rc, f_out, rb_out, p_out, ty_out))
    return [
        check("ruff check clean", r_rc == 0, r_out.strip()[-120:], "All checks passed!"),
        check("ruff format --check clean", f_rc == 0, f_rc, 0),
        check("pytest: exit code 0 path and exit 1 + stderr path pass", p_rc == 0 and m and int(m.group(1)) == 2,
              m.group(1) if m else p_out[-200:], 2),
        check("strict type check clean (mypy --strict; pyright not required here)", ty_rc == 0, ty_out.strip()[-150:], "Success"),
        check("negative control: legacy code trips ruff (B006 mutable default, B904 raise-without-from, F401)",
              {"B006", "B904", "F401"} <= set(bad_codes), bad_codes, ["B006", "B904", "F401"]),
    ], [rep, wd / "wc/cli.py"]


TSC = "/opt/node22/lib/node_modules/typescript/bin/tsc"


@card(P + "117-programming/310-writing-typescript")
def writing_typescript(task, wd):
    """unknown at the boundary narrowed by a type guard, Result union, exhaustive never; strict tsc flags."""
    flags = {"strict": True, "noUncheckedIndexedAccess": True, "exactOptionalPropertyTypes": True,
             "useUnknownInCatchVariables": True, "noImplicitOverride": True, "noFallthroughCasesInSwitch": True,
             "target": "ES2022", "module": "commonjs", "outDir": "dist"}
    jw(wd / "good/tsconfig.json", {"compilerOptions": flags, "files": ["shape.ts"]})
    jw(wd / "bad/tsconfig.json", {"compilerOptions": dict(flags, noEmit=True), "files": ["shape.ts"]})
    wt(wd / "good/shape.ts", '''
        export type Shape = { kind: "circle"; r: number } | { kind: "rect"; w: number; h: number };
        export type Result<T> = { ok: true; value: T } | { ok: false; error: string };

        function isRecord(v: unknown): v is Record<string, unknown> {
          return typeof v === "object" && v !== null;
        }

        export function parseShape(raw: unknown): Result<Shape> {
          if (!isRecord(raw)) return { ok: false, error: "not an object" };
          if (raw["kind"] === "circle" && typeof raw["r"] === "number") return { ok: true, value: { kind: "circle", r: raw["r"] } };
          if (raw["kind"] === "rect" && typeof raw["w"] === "number" && typeof raw["h"] === "number")
            return { ok: true, value: { kind: "rect", w: raw["w"], h: raw["h"] } };
          return { ok: false, error: "unknown shape" };
        }

        export function area(s: Shape): number {
          switch (s.kind) {
            case "circle":
              return Math.PI * s.r * s.r;
            case "rect":
              return s.w * s.h;
            default: {
              const never: never = s;
              return never;
            }
          }
        }

        const inputs: unknown[] = [JSON.parse('{"kind":"rect","w":3,"h":4}'), JSON.parse('{"kind":"tri"}'), 7];
        console.log(JSON.stringify(inputs.map((i) => { const r = parseShape(i); return r.ok ? area(r.value) : r.error; })));
        ''')
    wt(wd / "bad/shape.ts", '''
        type Shape = { kind: "circle"; r: number } | { kind: "rect"; w: number; h: number } | { kind: "tri"; b: number };
        export function area(s: Shape): number {
          switch (s.kind) {
            case "circle": return Math.PI * s.r * s.r;
            case "rect": return s.w * s.h;
            default: { const never: never = s; return never; }
          }
        }
        export function first(xs: number[]): number { return xs[0]; }
        ''')
    g_rc, g_out = sh(["node", TSC, "-p", "good"], cwd=wd, timeout=60)
    b_rc, b_out = sh(["node", TSC, "-p", "bad"], cwd=wd, timeout=60)
    codes = sorted(set(re.findall(r"error (TS\d+)", b_out)))
    run_rc, run_out = sh(["node", wd / "good/dist/shape.js"], cwd=wd)
    vals = json.loads(run_out.strip().splitlines()[-1]) if run_rc == 0 else None
    rep = wt(wd / "ts_report.txt", "good rc=%d\n%s\nbad rc=%d\n%s\nrun: %s" % (g_rc, g_out, b_rc, b_out, run_out))
    return [
        check("tsc with strict + noUncheckedIndexedAccess + exactOptionalPropertyTypes compiles cleanly", g_rc == 0, g_out[-200:], ""),
        check("boundary guard: rect -> area 12, unknown kind and non-object rejected",
              vals == [12, "unknown shape", "not an object"], vals, [12, "unknown shape", "not an object"]),
        check("negative control: missing union case caught by the never check (TS2322)", "TS2322" in codes, codes, "TS2322"),
        check("negative control: unchecked index access caught (xs[0] is number|undefined)", b_out.count("error TS") >= 2,
              b_out.count("error TS"), ">=2"),
    ], [rep, wd / "good/shape.ts"]


@card(P + "1261-ripgrep/2941-ripgrep")
def ripgrep(task, wd):
    """rg search that respects .gitignore and hidden rules, typed filters, --json counts vs an independent walk."""
    t = wd / "tree"
    files = {"src/app.py": "x = 1  # TODO fix\nprint('TODO later')\n", "src/util.js": "// TODO js\n",
             "docs/readme.md": "nothing here\nTODO: write docs\n", "build/gen.py": "# TODO generated\n",
             ".cache/x.py": "# TODO hidden\n", "node_modules/m/index.js": "// TODO vendored\n"}
    for k, v in files.items():
        wt(t / k, v)
    wt(t / ".gitignore", "build/\nnode_modules/\n")
    sh(["git", "init", "-q"], cwd=t)
    rc, out = sh(["rg", "--json", "TODO"], cwd=t)
    hits = [json.loads(ln) for ln in out.splitlines() if ln.startswith("{")]
    matches = sorted((h["data"]["path"]["text"], h["data"]["line_number"]) for h in hits if h["type"] == "match")
    expected = []
    for k, v in files.items():
        if k.startswith(("build/", "node_modules/", ".")):
            continue
        for i, ln in enumerate(v.splitlines(), 1):
            if "TODO" in ln:
                expected.append((k, i))
    expected.sort()
    _, pyout = sh(["rg", "-t", "py", "-c", "TODO"], cwd=t)
    py_counts = dict(ln.split(":") for ln in pyout.split())
    _, grep_out = sh(["grep", "-rn", "TODO", "."], cwd=t)
    grep_n = len(grep_out.splitlines())
    rep = jw(wd / "rg_matches.json", {"rg": matches, "expected": expected, "py_counts": py_counts, "grep_r_hits": grep_n})
    return [
        check("rg --json matches equal an independent walk that skips .gitignored and hidden paths",
              matches == [tuple(e) for e in expected], len(matches), len(expected)),
        check("-t py restricts to python files (src/app.py:2)", py_counts == {"src/app.py": "2"}, py_counts, {"src/app.py": "2"}),
        check("negative control: plain grep -r also hits ignored/hidden/vendored files", grep_n > len(matches), grep_n,
              ">%d" % len(matches)),
    ], [rep]


# ================================================================ C-level forcing questions (quantitative rules)
def _memo(wd, name, title, sections):
    body = ["# " + title, ""]
    for h, txt in sections:
        body += ["## " + h, txt if isinstance(txt, str) else "\n".join("- " + str(x) for x in txt), ""]
    return wt(wd / name, "\n".join(body))


@card(P + "146-c-level-agents/457-cco-review")
def cco_review(task, wd):
    """Q1 gross vs net retention, Q2 churn taxonomy + preventable share, Q4 kill list (support>50% ARR + low ICP)."""
    rows = [  # id, start ARR, end ARR, churn reason, support cost, icp
        ("c1", 80_000, 0, "product_fit", 5_000, "high"), ("c2", 40_000, 0, "pricing", 3_000, "mid"),
        ("c3", 100_000, 40_000, None, 9_000, "mid"), ("c4", 200_000, 420_000, None, 20_000, "high"),
        ("c5", 100_000, 100_000, None, 60_000, "high"), ("c6", 100_000, 100_000, None, 8_000, "high"),
        ("c7", 100_000, 100_000, None, 7_000, "mid"), ("c8", 100_000, 100_000, None, 9_000, "high"),
        ("c9", 180_000, 180_000, None, 100_000, "low")]
    jw(wd / "customers.json", rows)
    start = sum(r[1] for r in rows)
    churn = sum(r[1] for r in rows if r[2] == 0)
    contraction = sum(r[1] - r[2] for r in rows if 0 < r[2] < r[1])
    expansion = sum(r[2] - r[1] for r in rows if r[2] > r[1])
    grr = (start - churn - contraction) / start
    nrr = (start - churn - contraction + expansion) / start
    preventable = {"product_fit", "no_value_realized", "tactical_failure"}
    prev_share = sum(r[1] for r in rows if r[2] == 0 and r[3] in preventable) / churn
    kill = [r[0] for r in rows if r[4] > 0.5 * r[2] and r[5] == "low"]
    masking = grr < 0.85 and nrr > 1.0
    naive_verdict = "healthy" if nrr >= 1.0 else "at risk"
    memo = _memo(wd, "cco_review.md", "CCO review", [
        ("1. Gross retention", "GRR %.1f%% vs NRR %.1f%%%s" % (grr * 100, nrr * 100,
                                                            " -> expansion is masking a leaky bucket" if masking else "")),
        ("2. #1 churn reason", "preventable share of churned ARR %.1f%% -> %s" % (
            prev_share * 100, "CS has clear leverage" if prev_share > 0.5 else "structural")),
        ("4. Customers to fire", kill or ["none (segmentation suspect)"])])
    return [
        check("GRR = (start-churn-contraction)/start = 82.0%", abs(grr - 0.82) < 1e-9, grr, 0.82),
        check("NRR = 104.0%", abs(nrr - 1.04) < 1e-9, nrr, 1.04),
        check("masking rule fires (GRR<85% and NRR>100%)", masking, masking, True),
        check("preventable churn share 66.7% (> 50% -> CS leverage)", abs(prev_share - 2 / 3) < 1e-9, prev_share, 0.6667),
        check("kill list = support cost > 50% of ARR AND low ICP fit", kill == ["c9"], kill, ["c9"]),
        check("negative control: an NRR-only view calls the base healthy", naive_verdict == "healthy", naive_verdict, "healthy"),
    ], [memo]


@card(P + "146-c-level-agents/458-cdo-review")
def cdo_review(task, wd):
    """Q1 decision per source, Q2 consent provenance vs intended use, Q3 consumer count -> architecture."""
    sources = [
        {"name": "billing_events", "decision": "price tiering", "consent": "1p_explicit", "cls": "business", "use": "analytics"},
        {"name": "support_chats", "decision": "", "consent": "tos_bundled", "cls": "pii", "use": "ai_training"},
        {"name": "product_clicks", "decision": "onboarding redesign", "consent": "1p_explicit", "cls": "pii", "use": "ai_training"},
        {"name": "crm_notes", "decision": "", "consent": "tos_bundled", "cls": "business", "use": "analytics"}]
    consumers = ["finance", "sales", "cs", "product", "growth", "ops", "eng", "legal", "exec", "marketing", "risk", "hr"]
    jw(wd / "data_plan.json", {"sources": sources, "consumers": consumers})
    no_decision = [s["name"] for s in sources if not s["decision"]]
    blocked = [s["name"] for s in sources if s["use"] == "ai_training" and s["cls"] == "pii" and s["consent"] != "1p_explicit"]
    n = len(consumers)
    arch = "warehouse-only" if n < 5 else ("lakehouse" if n <= 25 else "mesh")
    naive = all(s["consent"] for s in sources)
    memo = _memo(wd, "cdo_review.md", "CDO review", [
        ("1. Decision driven", ["%s: %s" % (s["name"], s["decision"] or "NO DECISION -> stop collecting") for s in sources]),
        ("2. Consent provenance", ["BLOCK %s: bundled TOS does not cover PII training" % b for b in blocked]),
        ("3. Consumers", "%d consumers -> %s" % (n, arch))])
    return [
        check("sources with no decision unblocked", no_decision == ["support_chats", "crm_notes"], no_decision),
        check("PII training on bundled-TOS consent is blocked", blocked == ["support_chats"], blocked, ["support_chats"]),
        check("12 consumers -> lakehouse (5-25 band)", arch == "lakehouse", arch, "lakehouse"),
        check("negative control: 'every source has a consent field' passes the naive check", naive, naive, True),
    ], [memo]


@card(P + "146-c-level-agents/460-ciso-review")
def ciso_review(task, wd):
    """STRIDE top-3 by likelihood x impact, FAIR ALE = SLE x ARO, GDPR 72h window, vendor DPA gaps."""
    import datetime as dt
    threats = {"Spoofing": (4, 4), "Tampering": (2, 5), "Repudiation": (2, 2), "Information disclosure": (5, 5),
               "Denial of service": (3, 3), "Elevation of privilege": (3, 5)}
    ranked = sorted(threats, key=lambda k: (-threats[k][0] * threats[k][1], k))
    top3 = ranked[:3]
    records, cost_per_record, aro = 120_000, 4.5, 0.2
    sle = records * cost_per_record
    ale = sle * aro
    detected = dt.datetime(2026, 3, 10, 14, 0)
    deadline = detected + dt.timedelta(hours=72)
    vendors = [{"name": "mailer", "dpa": True, "review": "2026-01"}, {"name": "analytics", "dpa": False, "review": "2024-05"}]
    gaps = [v["name"] for v in vendors if not v["dpa"]]
    naive_top = sorted(threats, key=lambda k: -threats[k][1])[:3]
    memo = _memo(wd, "ciso_review.md", "CISO review", [
        ("1. Threat model (STRIDE)", ["%s: %d" % (k, threats[k][0] * threats[k][1]) for k in ranked]),
        ("2. Blast radius", "SLE $%.0f, ARO %.1f, ALE $%.0f" % (sle, aro, ale)),
        ("5. Regulatory window", "GDPR notify by %s" % deadline.isoformat()),
        ("6. Vendors", ["%s: no DPA" % g for g in gaps])])
    return [
        check("top-3 by likelihood x impact", top3 == ["Information disclosure", "Spoofing", "Elevation of privilege"], top3),
        check("FAIR ALE = 120000 x 4.5 x 0.2 = 108000", ale == 108_000, ale, 108_000),
        check("GDPR 72h deadline", deadline.isoformat() == "2026-03-13T14:00:00", deadline.isoformat(), "2026-03-13T14:00:00"),
        check("vendor without DPA flagged", gaps == ["analytics"], gaps, ["analytics"]),
        check("negative control: ranking by impact alone picks Tampering into the top 3", "Tampering" in naive_top, naive_top),
    ], [memo]


@card(P + "146-c-level-agents/461-cmo-review")
def cmo_review(task, wd):
    """Q3 one-sentence positioning template, Q5 CAC payback per channel (> 18 months = a hobby)."""
    channels = {"paid_search": (1800, 250, 0.8), "content": (900, 120, 0.8), "events": (6000, 400, 0.75),
                "community": (300, 15, 0.8)}  # CAC, ARPA per month, gross margin
    payback = {k: round(c / (a * g), 2) for k, (c, a, g) in channels.items()}
    hobbies = sorted(k for k, v in payback.items() if v > 18)
    pos = "For RevOps leads at 50-500 seat SaaS firms, who need clean pipeline data, we are a CRM hygiene tool that fixes records automatically unlike manual spreadsheet audits."
    m = re.fullmatch(r"For (.+?), who need[s]? (.+?), we are (.+?) that (.+?) unlike (.+?)\.", pos)
    naive_best = min(channels, key=lambda k: channels[k][0])
    memo = _memo(wd, "cmo_review.md", "CMO review", [
        ("3. Positioning", pos), ("5. CAC payback (months)", ["%s: %.2f%s" % (k, v, " HOBBY" if v > 18 else "") for k, v in payback.items()])])
    return [
        check("payback = CAC / (ARPA x GM)", payback == {"paid_search": 9.0, "content": 9.38, "events": 20.0, "community": 25.0},
              payback),
        check("channels over 18 months flagged as hobbies", hobbies == ["community", "events"], hobbies),
        check("positioning fits the 5-slot one-sentence template", bool(m) and len(m.groups()) == 5, bool(m), True),
        check("negative control: lowest-CAC ranking picks a hobby channel", naive_best in hobbies, naive_best, "community"),
    ], [memo]


@card(P + "146-c-level-agents/462-cpo-review")
def cpo_review(task, wd):
    """Q3 retention-curve shape (flat / decaying / smiling), Q4 RICE ranking, Q5 cut list under capacity."""
    items = {"sso": (800, 2, 0.8, 4), "dark_mode": (5000, 0.5, 1.0, 2), "ai_summary": (1200, 3, 0.5, 8),
             "bulk_edit": (2000, 1, 0.8, 1), "audit_log": (300, 2, 1.0, 3)}  # reach, impact, confidence, effort
    rice = {k: round(r * i * c / e, 1) for k, (r, i, c, e) in items.items()}
    order = sorted(rice, key=lambda k: -rice[k])
    cap, used, ship = 7, 0, []
    for k in order:
        if used + items[k][3] <= cap:
            ship.append(k)
            used += items[k][3]
    cut = [k for k in order if k not in ship]

    def shape(curve):
        tail = curve[len(curve) // 2:]
        d = tail[-1] - tail[0]
        return "smiling" if d > 0.01 else ("flat" if abs(d) <= 0.01 else "decaying")
    curves = {"hired_job": [1, .62, .5, .46, .45, .45, .455], "other": [1, .5, .35, .25, .18, .12, .08],
              "smile": [1, .55, .42, .4, .42, .45, .48]}
    shapes = {k: shape(v) for k, v in curves.items()}
    naive_top = max(items, key=lambda k: items[k][1])
    memo = _memo(wd, "cpo_review.md", "CPO review", [("4. RICE", ["%s %.1f" % (k, rice[k]) for k in order]),
                                                     ("5. Cut list", cut), ("3. PMF", ["%s: %s" % kv for kv in shapes.items()])])
    return [
        check("RICE = R x I x C / E ranking", order == ["bulk_edit", "dark_mode", "sso", "ai_summary", "audit_log"], order),
        check("capacity 7 effort-units: ship bulk_edit+dark_mode+sso, cut the rest", ship == ["bulk_edit", "dark_mode", "sso"]
              and cut == ["ai_summary", "audit_log"], {"ship": ship, "cut": cut}),
        check("retention shapes classified", shapes == {"hired_job": "flat", "other": "decaying", "smile": "smiling"}, shapes),
        check("negative control: ranking by impact alone puts ai_summary first", naive_top == "ai_summary" and order[0] != naive_top,
              naive_top),
    ], [memo]


@card(P + "146-c-level-agents/463-cro-review")
def cro_review(task, wd):
    """Q1 stage-weighted pipeline coverage vs 3x/4x, Q3 NRR decomposition, Q5 discount creep."""
    target = 1_000_000
    pipe = {"discovery": (1_800_000, 0.10), "demo": (900_000, 0.25), "proposal": (600_000, 0.5), "commit": (200_000, 0.8)}
    total_cov = sum(a for a, _ in pipe.values()) / target
    weighted = sum(a * p for a, p in pipe.values())
    need = 3.0  # inbound-heavy coverage threshold
    gross, contraction, expansion = 0.85, 0.05, 0.30
    nrr = 1 - (1 - gross) - contraction + expansion
    disc = {"q-4": [10, 12, 11, 9], "q-3": [11, 10, 12], "q-2": [12, 11, 13], "q-1": [12, 13, 12], "q0": [18, 16, 20, 17]}
    import statistics as st
    hist = st.median([st.median(v) for k, v in disc.items() if k != "q0"])
    now = st.median(disc["q0"])
    memo = _memo(wd, "cro_review.md", "CRO review", [
        ("1. Coverage", "total %.2fx; stage-weighted expected value $%.0f = %.2fx of target" % (total_cov, weighted, weighted / target)),
        ("3. NRR", "gross %.0f%%, contraction %.0f%%, expansion %.0f%% -> NRR %.0f%%" % (gross * 100, contraction * 100, expansion * 100, nrr * 100)),
        ("5. Discount", "median %.1f%% vs trailing %.1f%%" % (now, hist))])
    return [
        check("total coverage 3.5x", abs(total_cov - 3.5) < 1e-9, total_cov, 3.5),
        check("stage-weighted expected value = sum(amount x stage probability) = $865k", abs(weighted - 865_000) < 1e-6, weighted, 865_000),
        check("NRR 110% hides 85% gross retention", abs(nrr - 1.10) < 1e-9 and gross < 0.9, nrr, 1.10),
        check("discount creep: median 17.5% vs trailing 11.5%", now == 17.5 and hist == 11.5 and now - hist > 3, [now, hist]),
        check("weighted expected value covers <1x the target (act now)", weighted / target < 1, weighted / target, "<1"),
        check("negative control: total coverage passes the 3x rule", total_cov >= need, total_cov, ">=3"),
    ], [memo]


@card(P + "146-c-level-agents/470-gc-review")
def gc_review(task, wd):
    """Contract clauses parsed: liability cap vs 12 months of fees, carve-outs, DPA, auto-renew notice, IP."""
    contract = wt(wd / "msa.txt", """
        1. Fees. Customer pays $20,000 per month.
        2. Liability. Each party's aggregate liability is capped at fees paid in the 3 months preceding the claim.
           Carve-outs: willful misconduct.
        3. Term. This agreement renews automatically for successive 12-month terms unless either party gives
           notice of non-renewal at least 90 days before the end of the term.
        4. IP. All work product created by Vendor is owned by Vendor and licensed to Customer.
        5. Data. Vendor processes customer personal data to provide the service.
        """)
    t = contract.read_text()
    cap_m = int(re.search(r"capped at fees paid in the (\d+) months", t).group(1))
    fees = int(re.search(r"\$([\d,]+) per month", t).group(1).replace(",", ""))
    carve = [c for c in ["IP infringement", "data breach", "willful misconduct"] if c.lower() in t.lower()]
    missing_carve = [c for c in ["IP infringement", "data breach", "willful misconduct"] if c not in carve]
    auto = bool(re.search(r"renews automatically", t))
    notice = int(re.search(r"at least (\d+) days", t).group(1))
    dpa = "data processing agreement" in t.lower() or "dpa" in t.lower().split()
    pd = "personal data" in t.lower()
    flags = []
    if cap_m < 12:
        flags.append("cap %d months (< 12): $%d vs standard $%d" % (cap_m, cap_m * fees, 12 * fees))
    flags += ["missing carve-out: " + c for c in missing_carve]
    if auto and notice >= 60:
        flags.append("auto-renew trap: %d-day notice" % notice)
    if pd and not dpa:
        flags.append("personal data processed with no DPA")
    if "owned by vendor" in t.lower():
        flags.append("IP: vendor owns work product (license only)")
    memo = _memo(wd, "gc_review.md", "GC review (not legal advice)", [("Flags", flags)])
    naive = "liability" in t.lower() and "capped" in t.lower()
    return [
        check("liability cap parsed: 3 months x $20,000 = $60,000 vs $240,000 standard", cap_m == 3 and cap_m * fees == 60_000,
              cap_m * fees, 60_000),
        check("missing carve-outs found", missing_carve == ["IP infringement", "data breach"], missing_carve),
        check("auto-renew with 90-day notice flagged", any("auto-renew" in f for f in flags), auto, True),
        check("personal data without DPA flagged", any("DPA" in f for f in flags), pd and not dpa, True),
        check("6 flags total (cap, 2 carve-outs, auto-renew, DPA, IP)", len(flags) == 6, len(flags), 6),
        check("negative control: 'liability is capped' keyword check passes the contract", naive, naive, True),
    ], [memo, contract]


@card(P + "146-c-level-agents/474-vpe-review")
def vpe_review(task, wd):
    """Q2 DORA level per metric, overall = worst; Q3 offer-accept < 70%; Q4 span-of-control triggers."""
    def lvl_df(per_week):
        return "Elite" if per_week >= 7 else "High" if per_week >= 1 else "Medium" if per_week >= 0.25 else "Low"

    def lvl_lt(hours):
        return "Elite" if hours < 24 else "High" if hours < 168 else "Medium" if hours < 720 else "Low"

    def lvl_mttr(hours):
        return "Elite" if hours < 1 else "High" if hours < 24 else "Medium" if hours < 168 else "Low"

    def lvl_cfr(p):
        return "Elite" if p <= 0.05 else "High" if p <= 0.10 else "Medium" if p <= 0.15 else "Low"
    m = {"deploy_freq": lvl_df(10), "lead_time": lvl_lt(900), "mttr": lvl_mttr(0.5), "cfr": lvl_cfr(0.08)}
    rank = ["Low", "Medium", "High", "Elite"]
    overall = min(m.values(), key=rank.index)
    avg = rank[round(sum(rank.index(v) for v in m.values()) / 4)]
    funnel = {"applied": 600, "screen": 120, "onsite": 40, "offer": 10, "accept": 6}
    accept_rate = funnel["accept"] / funnel["offer"]
    teams = {"payments": {"ics": 11, "em": True}, "growth": {"ics": 6, "em": False}, "infra": {"ics": 7, "em": True}}
    mgr_trigger = [k for k, v in teams.items() if v["ics"] >= 5 and not v["em"]]
    squad_size = [k for k, v in teams.items() if not 5 <= v["ics"] <= 9]
    memo = _memo(wd, "vpe_review.md", "VPE review", [("2. DORA", ["%s: %s" % kv for kv in m.items()] + ["overall: " + overall]),
                                                     ("3. Funnel", "offer-accept %.0f%%" % (accept_rate * 100)),
                                                     ("4. Structure", ["no EM: %s" % mgr_trigger, "squad size out of 5-9: %s" % squad_size])])
    return [
        check("per-metric DORA levels", m == {"deploy_freq": "Elite", "lead_time": "Low", "mttr": "Elite", "cfr": "High"}, m),
        check("overall level = worst metric = Low", overall == "Low", overall, "Low"),
        check("offer-accept 60% < 70% (comp or close discipline)", accept_rate == 0.6, accept_rate, 0.6),
        check("manager trigger (5+ ICs, no EM) and squad-size rule", mgr_trigger == ["growth"] and squad_size == ["payments"],
              [mgr_trigger, squad_size]),
        check("negative control: averaging levels would report High", avg == "High", avg, "High"),
    ], [memo]


def _decision(wd, status="APPROVED"):
    return wt(wd / "decision.md", """
        # Decision: Move SMB tier to usage pricing
        **Status:** %s
        **Date:** 2026-04-01
        **Type:** pricing
        **Sponsor:** Dana (CEO)
        **Chosen option:** usage-based pricing for SMB
        ## Success criteria
        - SMB net revenue: >= 1.10 (index vs baseline)
        - SMB logo churn: <= 0.03
        ## Kill criteria
        - SMB logo churn: > 0.06
        ## Devil's advocate concerns
        - Billing system cannot meter usage in time
        - Support volume spikes after the change
        ## Dissent
        - CFO: revenue will dip for two quarters
        """ % status)


def _parse_decision(path):
    t = Path(path).read_text(encoding="utf-8")
    sec = {}
    cur = None
    for ln in t.splitlines():
        if ln.startswith("## "):
            cur = ln[3:].strip()
            sec[cur] = []
        elif cur and ln.startswith("- "):
            sec[cur].append(ln[2:].strip())
    head = dict(re.findall(r"\*\*(\w[\w ]*):\*\* (.+)", t))
    return head, sec


@card(P + "146-c-level-agents/467-execute")
def execute_plan(task, wd):
    """Approved decision -> 90-day plan: 3-6 workstreams with DRIs, 12 dated weekly milestones, 30/60/90, risk register."""
    import datetime as dt
    head, sec = _parse_decision(_decision(wd))
    if head.get("Status") != "APPROVED":
        raise RuntimeError("decision not approved")
    start = dt.date.fromisoformat("2026-04-06")
    ws = [("Metering + billing", "Ravi"), ("Pricing page + comms", "Mona"), ("Support readiness", "Lee"), ("Analytics", "Sam")]
    weeks = [(i + 1, (start + dt.timedelta(days=7 * i + 4)).isoformat(), ws[i % len(ws)]) for i in range(12)]
    risks = [(c, "M", "H", ws[0][1] if "Billing" in c else ws[2][1]) for c in sec["Devil's advocate concerns"]]
    plan = ["# Execution Plan: Move SMB tier to usage pricing", "**Start:** %s" % start,
            "**Checkpoint:** %s (90d)" % (start + dt.timedelta(days=90)), "", "## Workstreams",
            md_table([(w, d, "see milestones", "Not started") for w, d in ws], ["Workstream", "DRI", "Success Metric", "Status"]),
            "", "## Weekly Milestones",
            md_table([(n, "%s milestone %d" % (w[0], n), w[1], "due %s" % day) for n, day, w in weeks], ["Week", "Milestone", "DRI", "Definition of Done"]),
            "", "## Cadence", "- Weekly: owner review", "- Bi-weekly: cross-functional sync",
            "- Day 30 / 60 / 90: %s" % ", ".join(str(start + dt.timedelta(days=d)) for d in (30, 60, 90)), "",
            "## Risk Register", md_table(risks, ["Risk", "Likelihood", "Impact", "Owner"]), "", "## Kill Criteria Watch"] + \
        ["- " + k for k in sec["Kill criteria"]]
    out = wt(wd / "execution_plan.md", "\n".join(plan) + "\n")

    def validate(text):
        rows = re.findall(r"^\| (\d+) \| .+? \| (\w*) \| due (\d{4}-\d\d-\d\d) \|$", text, re.M)
        wsr = re.findall(r"^\| ([A-Z][^|]+?) \| (\w*) \| see milestones", text, re.M)
        return {"weeks": len(rows), "all_dri": all(d for _, d, _ in rows) and all(d for _, d in wsr),
                "ws": len(wsr), "risks_cover": all(c in text for c in sec["Devil's advocate concerns"])}
    v = validate(out.read_text())
    broken = validate(out.read_text().replace("| Lee |", "|  |"))
    return [
        check("12 weekly milestones, each with a DRI and due date", v["weeks"] == 12 and v["all_dri"], v),
        check("3-6 workstreams", 3 <= v["ws"] <= 6, v["ws"], "3..6"),
        check("week 12 due start+81d; checkpoint start+90d", weeks[-1][1] == "2026-06-26" and "2026-07-05 (90d)" in out.read_text(),
              weeks[-1][1], "2026-06-26"),
        check("every devil's-advocate concern is in the risk register", v["risks_cover"], v["risks_cover"], True),
        check("negative control: a plan with a missing DRI fails the validator", not broken["all_dri"], broken["all_dri"], False),
    ], [out]


FREEZE_DAYS = {"fundraise": 30, "pricing": 60, "market": 90, "layoff": 30, "pivot": 90, "personnel": 60, "m&a": 30}


def _freeze(path, today, reason):
    import datetime as dt
    head, _ = _parse_decision(path)
    if head.get("Status") != "APPROVED":
        return None
    days = FREEZE_DAYS[head["Type"]]
    until = (dt.date.fromisoformat(today) + dt.timedelta(days=days)).isoformat()
    t = Path(path).read_text(encoding="utf-8").replace("**Status:** APPROVED", "**Status:** FROZEN\n**Frozen until:** %s\n"
                                                        "**Reason for freeze:** %s\n**Override condition:** Kill criterion "
                                                        "SMB logo churn triggers OR /cs:unfreeze with stated reason" % (until, reason))
    Path(path).write_text(t, encoding="utf-8")
    return until


def _router(path, today, kill_triggered=False):
    head, _ = _parse_decision(path)
    if head.get("Status") == "FROZEN" and today < head["Frozen until"] and not kill_triggered:
        return "refuse: frozen until " + head["Frozen until"]
    return "route to boardroom"


@card(P + "146-c-level-agents/469-freeze")
def freeze(task, wd):
    """Lock an APPROVED decision for its default cooldown, index it, and make the router refuse re-litigation."""
    d = _decision(wd)
    until = _freeze(d, "2026-04-01", "pricing change needs a full cycle")
    idx = wt(wd / "freezes/active.md", "# Active Freezes\n**Updated:** 2026-04-01\n\n" + md_table(
        [("Move SMB tier to usage pricing", until, "kill criterion SMB logo churn or /cs:unfreeze")],
        ["Decision", "Frozen until", "Override condition"]) + "\n")
    r_during = _router(d, "2026-05-01")
    r_kill = _router(d, "2026-05-01", kill_triggered=True)
    r_after = _router(d, "2026-06-01")
    draft = _decision(wd / "draft", status="PROPOSED")
    refused = _freeze(draft, "2026-04-01", "x")
    unfrozen_router = _router(_decision(wd / "plain"), "2026-05-01")
    return [
        check("pricing decision frozen 60 days -> 2026-05-31", until == "2026-05-31", until, "2026-05-31"),
        check("decision record now FROZEN with override condition", "**Status:** FROZEN" in d.read_text()
              and "Override condition" in d.read_text(), True, True),
        check("router refuses during freeze", r_during.startswith("refuse"), r_during),
        check("kill criterion overrides the freeze; expiry releases it", r_kill == r_after == "route to boardroom", [r_kill, r_after]),
        check("non-APPROVED decision cannot be frozen", refused is None, refused, None),
        check("negative control: without the freeze the router re-litigates", unfrozen_router == "route to boardroom", unfrozen_router),
    ], [d, idx]


@card(P + "146-c-level-agents/473-post-mortem")
def post_mortem(task, wd):
    """Score actuals against PRE-COMMITTED success and kill criteria; WIN/PARTIAL/LOSS; revisit dissent."""
    head, sec = _parse_decision(_decision(wd))
    actual = {"SMB net revenue": 1.04, "SMB logo churn": 0.025}

    def score(criteria, kills):
        rows, met = [], []
        for c in criteria:
            name, rule = c.split(": ")
            op, thr = rule.split()[0], float(rule.split()[1])
            ok = actual[name] >= thr if op == ">=" else actual[name] <= thr
            rows.append((name, rule, actual[name], "yes" if ok else "no"))
            met.append(ok)
        trig = []
        for c in kills:
            name, rule = c.split(": ")
            op, thr = rule.split()[0], float(rule.split()[1])
            trig.append(actual[name] > thr if op == ">" else actual[name] < thr)
        status = "LOSS" if any(trig) or not any(met) else ("WIN" if all(met) else "PARTIAL")
        return rows, trig, status
    rows, trig, status = score(sec["Success criteria"], sec["Kill criteria"])
    dissent = [(d, "YES" if "revenue" in d and actual["SMB net revenue"] < 1.10 else "NO") for d in sec["Dissent"]]
    pm = wt(wd / "postmortem.md", "# Post-Mortem: %s\n**Status:** %s\n\n" % ("Move SMB tier to usage pricing", status) +
            md_table(rows, ["Success Criterion", "Threshold", "Actual", "Met?"]) + "\n\nKill triggered: %s\n\n## Preserved Dissent\n" % any(trig) +
            "\n".join("- %s -> materialized: %s" % d for d in dissent) + "\n")
    _, _, retro = score(["SMB net revenue: >= 1.00", "SMB logo churn: <= 0.03"], sec["Kill criteria"])
    return [
        check("scored against pre-committed thresholds: revenue missed, churn met", [r[3] for r in rows] == ["no", "yes"], [r[3] for r in rows]),
        check("no kill criterion triggered (churn 2.5% <= 6%)", not any(trig), trig, [False]),
        check("overall PARTIAL", status == "PARTIAL", status, "PARTIAL"),
        check("CFO dissent revisited and marked materialized", dissent[0][1] == "YES", dissent),
        check("negative control: retroactively lowered thresholds would call it a WIN", retro == "WIN", retro, "WIN"),
    ], [pm]


# ================================================================ agent / CLI / instruction tooling
def _hashes(root):
    import hashlib
    return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(Path(root).rglob("*")) if p.is_file() and not p.is_symlink()}


HARNESS = r'''
import json, sys
from pathlib import Path

WD = Path(sys.argv[1]); MODE = sys.argv[2]; CRASH_AT = int(sys.argv[3])
TRANSCRIPT = WD / "transcript.jsonl"; COUNTER = WD / ("exec_count_%s.json" % MODE)
POLICY = {"read_file": "allow", "append_note": "allow", "write_file": "ask", "shell": "deny"}
PLAN = [("c1", "read_file", {"path": "input.txt"}), ("c2", "append_note", {"text": "summary: 3 lines"}),
        ("c3", "shell", {"cmd": "rm -rf /"}), ("c4", "write_file", {"path": "out.txt", "text": "x"}),
        ("c5", "append_note", {"text": "done"})]

def tool(name, args):
    if name == "read_file":
        return (WD / args["path"]).read_text(encoding="utf-8")
    if name == "append_note":
        with open(WD / ("notes_%s.txt" % MODE), "a", encoding="utf-8") as f: f.write(args["text"] + "\n")
        return "ok"
    if name == "write_file":
        (WD / args["path"]).write_text(args["text"], encoding="utf-8"); return "ok"
    if name == "shell":
        return "would run " + args["cmd"]

def assemble(done):
    return {"system": "You are a file assistant.", "memory": (WD / "MEMORY.md").read_text(encoding="utf-8"),
            "transcript_tail": done[-3:]}

def model(request, done_ids):          # deterministic stand-in for the model: next planned call not yet done
    for c in PLAN:
        if c[0] not in done_ids: return c
    return None

done = []
if MODE == "durable" and TRANSCRIPT.exists():
    done = [json.loads(l) for l in TRANSCRIPT.read_text(encoding="utf-8").splitlines()]
counts = json.loads(COUNTER.read_text()) if COUNTER.exists() else {}
step = 0
while True:
    call = model(assemble(done), {d["id"] for d in done})
    if call is None: break
    cid, name, args = call
    decision = POLICY.get(name, "deny")
    if decision == "allow":
        counts[cid] = counts.get(cid, 0) + 1; result = tool(name, args)
    else:
        result = "DENIED by permission gate (%s)" % decision
    rec = {"id": cid, "tool": name, "decision": decision, "result": str(result)[:80]}
    done.append(rec)
    if MODE == "durable":
        with open(TRANSCRIPT, "a", encoding="utf-8") as f: f.write(json.dumps(rec) + "\n")
    COUNTER.write_text(json.dumps(counts))
    step += 1
    if step == CRASH_AT: sys.exit(17)
print(json.dumps({"steps": len(done)}))
'''

BLUEPRINT = ["System goal and delegation boundary", "Harness layers", "Request assembly design", "Turn loop design",
             "Tool and capability runtime", "Context and memory model", "Permissions and safety gates",
             "Transcript and recovery model", "Extension surfaces", "Implementation sequence"]


@card(P + "1211-claude-code-harness/2867-claude-code-harness")
def claude_code_harness(task, wd):
    """Blueprint (10 sections) + a runnable reference harness: assembly, loop, permission gate, durable transcript."""
    h = wt(wd / "harness.py", HARNESS)
    wt(wd / "input.txt", "a\nb\nc\n")
    wt(wd / "MEMORY.md", "- user prefers short notes\n")
    r1 = sh(["python3", "-I", h, wd, "durable", "2"])[0]
    r2, o2 = sh(["python3", "-I", h, wd, "durable", "0"])
    counts = json.loads((wd / "exec_count_durable.json").read_text())
    tr = [json.loads(ln) for ln in (wd / "transcript.jsonl").read_text().splitlines()]
    sh(["python3", "-I", h, wd, "oneshot", "2"])
    sh(["python3", "-I", h, wd, "oneshot", "0"])
    naive = json.loads((wd / "exec_count_oneshot.json").read_text())
    bp = ["# Harness blueprint: file assistant", ""]
    impl = {"Permissions and safety gates": "POLICY table allow/ask/deny checked before every tool call; ask without a "
            "human = deny.", "Transcript and recovery model": "append-only transcript.jsonl; resume skips completed call ids.",
            "Turn loop design": "assemble -> model -> gate -> tool -> record, until the model returns no call."}
    for i, s in enumerate(BLUEPRINT, 1):
        bp += ["## %d. %s" % (i, s), impl.get(s, "See harness.py (reference implementation)."), ""]
    bpf = wt(wd / "blueprint.md", "\n".join(bp))
    return [
        check("crash after step 2 then resume completes (exit 17, then 0)", r1 == 17 and r2 == 0, [r1, r2], [17, 0]),
        check("durable transcript: each allowed call executed exactly once across the crash",
              counts == {"c1": 1, "c2": 1, "c5": 1}, counts, {"c1": 1, "c2": 1, "c5": 1}),
        check("permission gate: shell (deny) and write_file (ask) never ran", not (wd / "out.txt").exists()
              and [t["decision"] for t in tr if t["id"] in ("c3", "c4")] == ["deny", "ask"], [t["decision"] for t in tr]),
        check("side effects happened once each (notes.txt)", (wd / "notes_durable.txt").read_text().splitlines() == ["summary: 3 lines", "done"],
              (wd / "notes_durable.txt").read_text().splitlines(), ["summary: 3 lines", "done"]),
        check("blueprint has the 10 contract sections", all("## %d. %s" % (i, s) in bpf.read_text() for i, s in enumerate(BLUEPRINT, 1)),
              10, 10),
        check("negative control: a loop without a transcript re-executes completed calls after the crash",
              naive.get("c1", 0) == 2 and naive.get("c2", 0) == 2, naive, {"c1": 2, "c2": 2}),
    ], [bpf, wd / "transcript.jsonl"]


CLI_SRC = r'''
import argparse, json, re, sys
from pathlib import Path
DATA = Path(__file__).parent / "data"
SCHEMA = {"list": {"params": {"fields": "csv of id,name,status", "limit": "int 1..100"}},
          "get": {"params": {"id": "string ^[a-z0-9-]{1,32}$"}},
          "delete": {"params": {"id": "string", "dry_run": "bool"}, "mutating": True}}
ID_RE = re.compile(r"^[a-z0-9-]{1,32}$")

def fail(code, msg, kind):
    sys.stderr.write(json.dumps({"error": {"kind": kind, "message": msg}}) + "\n"); sys.exit(code)

def harden(i):
    if any(ord(c) < 32 for c in i) or "%" in i or ".." in i or "/" in i or not ID_RE.match(i):
        fail(2, "invalid id %r" % i, "validation")
    return i

def items():
    return [json.loads(p.read_text(encoding="utf-8")) for p in sorted(DATA.glob("*.json"))]

def emit(rows, fields):
    for r in rows:
        print(json.dumps({k: r[k] for k in fields} if fields else r, sort_keys=True))

ap = argparse.ArgumentParser(prog="items")
ap.add_argument("cmd", choices=["list", "get", "delete", "schema"])
ap.add_argument("--id"); ap.add_argument("--fields"); ap.add_argument("--limit", type=int, default=50)
ap.add_argument("--dry-run", action="store_true"); ap.add_argument("--json")
a = ap.parse_args()
if a.json:
    try: payload = json.loads(a.json)
    except ValueError: fail(2, "bad --json payload", "validation")
    for k, v in payload.items(): setattr(a, k, v)
if a.cmd == "schema": print(json.dumps(SCHEMA, sort_keys=True)); sys.exit(0)
fields = [f for f in (a.fields or "").split(",") if f]
bad = [f for f in fields if f not in ("id", "name", "status")]
if bad: fail(2, "unknown fields %s" % bad, "validation")
if not 1 <= int(a.limit) <= 100: fail(2, "limit out of range", "validation")
if a.cmd == "list": emit(items()[: int(a.limit)], fields); sys.exit(0)
i = harden(a.id or "")
p = DATA / (i + ".json")
if not p.exists(): fail(3, "not found", "not_found")
if a.cmd == "get": emit([json.loads(p.read_text(encoding="utf-8"))], fields); sys.exit(0)
if a.dry_run: print(json.dumps({"would_delete": i})); sys.exit(0)
p.unlink(); print(json.dumps({"deleted": i}))
'''

NAIVE_CLI = r'''
import sys
from pathlib import Path
print(Path(__file__).parent.joinpath("data", sys.argv[1] + ".json").read_text())
'''


@card(P + "1216-ai-friendly-cli/2898-ai-friendly-cli")
def ai_friendly_cli(task, wd):
    """A CLI built to the 8 principles (JSON I/O, schema, field masks, hardening, dry-run, exit codes), then probed."""
    cli = wt(wd / "cli/items.py", CLI_SRC)
    for n, (name, st) in enumerate([("alpha", "open"), ("beta", "closed"), ("gamma", "open")]):
        jw(wd / ("cli/data/%s.json" % name), {"id": name, "name": name.title(), "status": st, "blob": "x" * 500})
    wt(wd / "cli/secret.json", '{"token": "TOP-SECRET"}')
    wt(wd / "naive/naive.py", NAIVE_CLI)
    shutil.copytree(wd / "cli/data", wd / "naive/data")
    wt(wd / "naive/secret.json", '{"token": "TOP-SECRET"}')

    def run(*a):
        return subprocess.run(["python3", "-I", cli, *a], capture_output=True, text=True, timeout=20)
    lst = run("list", "--fields", "id,status", "--limit", "2")
    rows = [json.loads(x) for x in lst.stdout.splitlines()]
    sch = json.loads(run("schema").stdout)
    trav = run("get", "--id", "../secret")
    enc = run("get", "--id", "%2e%2e")
    miss = run("get", "--id", "zeta")
    dry = run("delete", "--json", '{"id": "beta", "dry_run": true}')
    still = (wd / "cli/data/beta.json").exists()
    naive = subprocess.run(["python3", "-I", wd / "naive/naive.py", "../secret"], capture_output=True, text=True)
    err = json.loads(trav.stderr.strip().splitlines()[-1])
    rep = jw(wd / "cli_probe.json", {"list": rows, "schema": sch, "traversal": [trav.returncode, err], "missing": miss.returncode,
                                     "dry": dry.stdout, "naive": naive.stdout[:60]})
    return [
        check("NDJSON list with field mask + limit: exactly the 2 rows, only id/status", rows == [
            {"id": "alpha", "status": "open"}, {"id": "beta", "status": "closed"}], rows),
        check("schema introspection lists 3 commands and marks delete mutating", set(sch) == {"list", "get", "delete"}
              and sch["delete"].get("mutating") is True, sorted(sch)),
        check("path traversal and percent-encoding rejected with exit 2 + JSON error", trav.returncode == 2 and enc.returncode == 2
              and err["error"]["kind"] == "validation", [trav.returncode, enc.returncode], [2, 2]),
        check("not-found has its own exit code 3", miss.returncode == 3, miss.returncode, 3),
        check("--json payload with dry_run deletes nothing", still and "would_delete" in dry.stdout, still, True),
        check("negative control: naive CLI reads ../secret.json", "TOP-SECRET" in naive.stdout, naive.stdout[:40], "TOP-SECRET"),
    ], [rep, cli]


@card(P + "1280-instruction-audit/2957-instruction-audit")
def instruction_audit(task, wd):
    """Read-only audit of a fixture instruction stack: baseline chars/tokens by load class, never-fired skills,
    cross-layer contradictions; proves no file changed."""
    s = wd / "stack"
    wt(s / "home/.claude/CLAUDE.md", "# Global\n- Always use tabs for indentation.\n- Never commit without running tests.\n" + "- Be concise.\n" * 30)
    wt(s / "proj/CLAUDE.md", "# Project\n- Never use tabs for indentation; use 4 spaces.\n- Always run `make lint` before finishing.\n" + "- Prefer small diffs.\n" * 40)
    wt(s / "proj/src/legacy/CLAUDE.md", "# Legacy dir\n" + "- Keep the old API names.\n" * 200)
    wt(s / "proj/.claude/skills/deploy/SKILL.md", "---\nname: deploy\n---\n" + "deploy steps\n" * 50)
    wt(s / "proj/.claude/skills/release-notes/SKILL.md", "---\nname: release-notes\n---\n" + "notes steps\n" * 50)
    wt(s / "transcripts/s1.jsonl", "\n".join(json.dumps(e) for e in [
        {"type": "skill", "name": "deploy"}, {"type": "tool", "name": "Bash"}, {"type": "skill", "name": "deploy"}]) + "\n")
    wt(s / "transcripts/s2.jsonl", json.dumps({"type": "tool", "name": "Read"}) + "\n")
    before = _hashes(s)
    surfaces = []
    for p in sorted(s.rglob("*.md")):
        rel = str(p.relative_to(s))
        cls = "on-demand" if "/skills/" in rel else ("scope-loaded" if rel.count("/") > 1 and rel.startswith("proj/src") else "always")
        n = len(p.read_text(encoding="utf-8"))
        surfaces.append({"file": rel, "chars": n, "est_tokens": n // 4, "load": cls})
    always = sum(x["est_tokens"] for x in surfaces if x["load"] == "always")
    naive_total = sum(x["est_tokens"] for x in surfaces if x["load"] != "on-demand")
    rules = []
    for x in surfaces:
        for ln in (s / x["file"]).read_text(encoding="utf-8").splitlines():
            m = re.match(r"- (Always|Never) (use|commit|run) (.+?)[.;]", ln)
            if m:
                rules.append((x["file"], m.group(1).lower(), m.group(2), m.group(3).split(" for ")[0].strip("` ")))
    conflicts = [(a[0], b[0], a[2] + " " + a[3]) for i, a in enumerate(rules) for b in rules[i + 1:]
                 if a[2:] == b[2:] and a[1] != b[1]]
    fired = set()
    for t in sorted((s / "transcripts").glob("*.jsonl")):
        fired |= {json.loads(ln)["name"] for ln in t.read_text().splitlines() if '"skill"' in ln}
    skills = sorted(p.parent.name for p in s.rglob("SKILL.md"))
    never = [k for k in skills if k not in fired]
    after = _hashes(s)
    rep = wt(wd / "instruction_audit.md", "# Instruction audit (read-only)\n\nScopes covered: host files, skills, transcripts (2 sessions)\n\n" +
             md_table([(x["file"], x["chars"], "%d est." % x["est_tokens"], x["load"]) for x in surfaces],
                      ["File", "Chars", "Est. tokens", "When loaded"]) +
             "\n\nAlways-loaded total: %d est. tokens\n\n## Conflicts\n" % always +
             "\n".join("- %s vs %s on '%s' -> proposed edit: delete the global rule" % c for c in conflicts) +
             "\n\n## Never fired (2-session window)\n" + "\n".join("- skill %s" % k for k in never) + "\n")
    exp_always = (len((s / "home/.claude/CLAUDE.md").read_text()) // 4) + (len((s / "proj/CLAUDE.md").read_text()) // 4)
    return [
        check("baseline: always-loaded est. tokens = chars/4 of global + project files", always == exp_always, always, exp_always),
        check("nested legacy file classed scope-loaded, skills on-demand",
              [x["load"] for x in surfaces if "legacy" in x["file"]] == ["scope-loaded"]
              and all(x["load"] == "on-demand" for x in surfaces if "skills" in x["file"]), True, True),
        check("cross-layer contradiction found (always vs never use tabs)", len(conflicts) == 1 and "tabs" in conflicts[0][2], conflicts),
        check("never-fired skill found from transcripts", never == ["release-notes"], never, ["release-notes"]),
        check("audit modified no file (hashes identical)", before == after, len(after), len(before)),
        check("negative control: billing the scope-loaded file as per-session overstates the baseline",
              naive_total > always * 2, naive_total, ">%d" % (always * 2)),
    ], [rep]


@card(P + "1362-tool-advisor/3094-tool-advisor")
def tool_advisor(task, wd):
    """Phase 1 read-only discovery of real binaries, task profile, approaches using only discovered tools,
    gaps in 'Missing but Useful', and the mandatory Quick Action table."""
    wanted = {"search": ["rg", "fd", "fzf", "grep"], "media": ["ffmpeg", "ffprobe"], "docs": ["pandoc", "tesseract"],
              "code": ["node", "python3", "go", "cargo", "dotnet"], "vcs": ["git", "gh"]}
    found = {k: [b for b in v if shutil.which(b)] for k, v in wanted.items()}
    missing = sorted(b for v in wanted.values() for b in v if not shutil.which(b))
    bash_check = sh(["bash", "-c", "for b in %s; do command -v $b >/dev/null && echo $b; done" %
                     " ".join(b for v in wanted.values() for b in v)])[1].split()
    task_s = "Find every TODO in a repo and convert the matching markdown docs to PDF"
    approach = [("rg", "rg -n TODO"), ("pandoc", "pandoc doc.md -o doc.pdf")] if "rg" in found["search"] else []
    used = [a for a, _ in approach]
    out = ["## Tool Advisor v3.5", "", "### Your Environment",
           md_table([(k, ", ".join(v) or "-") for k, v in found.items()], ["Layer", "Available"]), "",
           "### Task Profile", "Task: " + task_s, "Type: Investigation | Scale: Medium | Traits: search, conversion",
           "Done when: every TODO is listed with file:line and each doc has a PDF.", "",
           "### Relevant Capabilities", ", ".join(used), "", "### Suggested Approaches",
           "1. " + " -> ".join(c for _, c in approach), "", "### Performance Tips", "- rg respects .gitignore; no -u needed.", "",
           "### Missing but Useful", "\n".join("- %s (not installed; ask before installing)" % m for m in missing), "",
           "## Quick Action", md_table([(i + 1, "`%s`" % c) for i, (_, c) in enumerate(approach)], ["#", "Command"])]
    f = wt(wd / "tool_advice.md", "\n".join(out) + "\n")
    txt = f.read_text()
    static = ["fd", "fzf", "rg"]
    return [
        check("discovery matches an independent `command -v` scan", sorted(sum(found.values(), [])) == sorted(bash_check),
              sorted(sum(found.values(), [])), sorted(bash_check)),
        check("every suggested tool is actually installed", all(shutil.which(u) for u in used) and len(used) == 2, used),
        check("missing tools are surfaced, not suggested", all(m not in used for m in missing) and "fd" in missing, missing),
        check("all template sections present and output ends with Quick Action", all(h in txt for h in [
            "### Your Environment", "### Task Profile", "### Suggested Approaches", "### Missing but Useful"])
              and re.findall(r"^##+ .+$", txt, re.M)[-1] == "## Quick Action", re.findall(r"^##+ .+$", txt, re.M)[-1], "## Quick Action"),
        check("negative control: a static recommendation list names tools absent here",
              any(not shutil.which(b) for b in static), [b for b in static if not shutil.which(b)]),
    ], [f]


# ================================================================ writing / planning gates
CH_FIELDS = ["Purpose", "Entry state", "Exit state", "Pull", "Content", "Sets up", "Pays off", "Must not", "Length target"]


def _outline_text(chapters, approved=False):
    out = ["# Outline: Small Data, Big Decisions", "", "## Structure and rationale",
           "Nonfiction: problem -> principles -> practice -> advanced, chosen because readers arrive with a problem.", "",
           "## Pacing map", md_table([(c["n"], c["title"], c["Length target"]) for c in chapters], ["Ch", "Title", "Words"]), "",
           "## Chapter specs"]
    for c in chapters:
        out += ["### %d. %s" % (c["n"], c["title"])] + ["- **%s:** %s" % (f, c.get(f, "")) for f in CH_FIELDS if f in c] + [""]
    out += ["## Validation", "structure checked by outline_gate()"]
    if approved:
        out += ["", "## Approval", approved]
    return "\n".join(out) + "\n"


def _outline_gate(text):
    specs = re.split(r"^### (\d+)\. .+$", text, flags=re.M)
    chs = {}
    for i in range(1, len(specs), 2):
        chs[int(specs[i])] = dict(re.findall(r"^- \*\*(.+?):\*\* (.*)$", specs[i + 1], re.M))
    issues = []
    for n, c in chs.items():
        for f in ["Purpose", "Entry state", "Exit state", "Pull", "Content"]:
            if not c.get(f):
                issues.append("ch%d missing %s" % (n, f))
    purposes = [c.get("Purpose") for c in chs.values()]
    if len(set(purposes)) != len(purposes):
        issues.append("duplicate purpose (one chapter redundant)")
    for n, c in chs.items():
        for ref in re.findall(r"ch(\d+)", c.get("Sets up", "")):
            r = int(ref)
            if r not in chs or r <= n:
                issues.append("ch%d sets up ch%d which is missing or earlier" % (n, r))
            elif "ch%d" % n not in chs[r].get("Pays off", ""):
                issues.append("ch%d setup not paid off in ch%d" % (n, r))
    return {"chapters": len(chs), "issues": issues, "score": max(0, 10 - 2 * len(issues)),
            "approved": "## Approval" in text}


@card(P + "1376-velith/3225-book-outline")
def book_outline(task, wd):
    """Outline + bible with complete chapter specs, setup/payoff map validated; the approval gate stays closed
    until a human approves (the program never writes approval on the author's behalf)."""
    titles = ["Why gut feel fails", "Ask a decision question", "Count before you model", "Small experiments", "Reading noise",
              "Deciding under doubt"]
    chs = []
    for i, t in enumerate(titles, 1):
        chs.append({"n": i, "title": t, "Purpose": "reader can %s" % t.lower(), "Entry state": "knows ch%d ideas" % (i - 1),
                    "Exit state": "applies '%s'" % t.lower(), "Pull": "what breaks next?", "Content": "claims C%d.1-2, sources S%d" % (i, i),
                    "Sets up": ("ch%d" % (i + 2)) if i <= 4 else "", "Pays off": ("ch%d" % (i - 2)) if i >= 3 else "",
                    "Must not": "formulas before ch3", "Length target": 4000 + 500 * (i % 2)})
    outline = wt(wd / "outline.md", _outline_text(chs))
    bible = wt(wd / "bible.md", "# Bible\n## Key concepts\n" + "\n".join("- %s: first in ch%d" % (c["title"], c["n"]) for c in chs) +
               "\n## Open threads\n" + "\n".join("- ch%d -> %s" % (c["n"], c["Sets up"]) for c in chs if c["Sets up"]) +
               "\n## Chapter ledger\n")
    g = _outline_gate(outline.read_text())
    bad = [dict(c) for c in chs]
    bad[4]["Purpose"] = bad[1]["Purpose"]
    bad[3]["Sets up"] = "ch9"
    del bad[5]["Pull"]
    gb = _outline_gate(_outline_text(bad))
    return [
        check("6 chapter specs, every one with purpose/entry/exit/pull/content", g["chapters"] == 6 and not g["issues"], g["issues"], []),
        check("every setup is paid off in a later chapter (4 setup/payoff pairs)",
              sum(1 for c in chs if c["Sets up"]) == 4 and not g["issues"], 4, 4),
        check("structure score >= 8/10", g["score"] >= 8, g["score"], ">=8"),
        check("router treats the outline as unapproved (no ## Approval until the author signs)", g["approved"] is False, g["approved"], False),
        check("bible lists concepts and open threads", bible.read_text().count("first in ch") == 6, 6, 6),
        check("negative control: duplicate purpose, dangling setup, missing pull fail the gate", len(gb["issues"]) >= 3 and gb["score"] < 8,
              gb["issues"]),
    ], [outline, bible]


@card(P + "1376-velith/3227-book-publish")
def book_publish(task, wd):
    """Gate on readiness PASS, strip chapter frontmatter, poetry line breaks, pandoc EPUB build, structural EPUB check."""
    import zipfile
    proj = wd / "book"
    wt(proj / "edits/readiness-report.md", "verdict: PASS\n")
    wt(proj / "drafts/01-rain.md", "---\nstatus: final\nslug: rain\n---\n# Rain\n\nThe first chapter opens.\n")
    wt(proj / "drafts/02-poem.md", "---\nstatus: final\nslug: poem\ngenre: poetry\n---\n# Poem\n\nline one\nline two\nline three\n")
    wt(proj / "publish/metadata.yaml", "title: Small Weather\nauthor: A. Writer\nlang: en\nrights: (c) 2026 A. Writer\n")

    def publish(project):
        if "verdict: PASS" not in (project / "edits/readiness-report.md").read_text():
            return None
        chapters = sorted((project / "drafts").glob("*.md"))
        if any("status: final" not in c.read_text() for c in chapters):
            return None
        tmp = project / "publish/tmp"
        tmp.mkdir(parents=True, exist_ok=True)
        built = []
        for c in chapters:
            t = c.read_text(encoding="utf-8")
            fm, body = t.split("---\n", 2)[1], t.split("---\n", 2)[2]
            if "genre: poetry" in fm:
                body = "\n".join(ln + "  " if ln.strip() and not ln.startswith("#") else ln for ln in body.splitlines()) + "\n"
            built.append(wt(tmp / c.name, body))
        out = project / "publish/book.epub"
        fx.run(["pandoc", "--metadata-file", project / "publish/metadata.yaml", "--toc", "-o", out, *built], timeout=60)
        wt(project / "publish/PUBLISH-NOTES.md", "- PDF not built: no PDF engine (pdflatex/xelatex/wkhtmltopdf) on this machine\n"
                                                "- epubcheck not installed: structural checks below instead\n")
        return out
    epub = publish(proj)
    z = zipfile.ZipFile(epub)
    names = z.namelist()
    first = z.infolist()[0]
    opf = z.read([n for n in names if n.endswith(".opf")][0]).decode()
    xhtml = "".join(z.read(n).decode() for n in names if n.endswith(".xhtml"))
    chapters = [n for n in names if re.search(r"ch\d+\.xhtml$", n)]
    blocked = wd / "blocked"
    shutil.copytree(proj / "drafts", blocked / "drafts")
    wt(blocked / "edits/readiness-report.md", "verdict: FAIL\n")
    wt(blocked / "publish/metadata.yaml", "title: x\n")
    refused = publish(blocked)
    return [
        check("EPUB mimetype is the first entry and stored uncompressed", first.filename == "mimetype" and first.compress_type == 0,
              [first.filename, first.compress_type], ["mimetype", 0]),
        check("metadata title in content.opf", "Small Weather" in opf, "Small Weather" in opf, True),
        check("2 chapter documents + nav", len(chapters) == 2 and any(n.endswith("nav.xhtml") for n in names), len(chapters), 2),
        check("frontmatter stripped (no 'status: final' in the book)", "status: final" not in xhtml and "slug:" not in xhtml, True, True),
        check("poetry line breaks preserved (<br />)", xhtml.count("<br />") >= 2, xhtml.count("<br />"), ">=2"),
        check("negative control: readiness verdict FAIL refuses to build", refused is None and not (blocked / "publish/book.epub").exists(),
              refused, None),
    ], [epub, proj / "publish/PUBLISH-NOTES.md"]


def _triage(req):
    full = ["public api", "migration", "schema", "auth", "privacy", "billing", "cost", "unclear", "security"]
    compact = ["default", "flag", "config", "compat"]
    r = req.lower()
    if any(k in r for k in full):
        return "Full"
    if any(k in r for k in compact):
        return "Compact"
    return "Minimal"


@card(P + "1397-brainstorm/3333-brainstorm")
def brainstorm(task, wd):
    """Triage, one exact-text search for repository evidence, a capsule with the five fields; never edits code."""
    repo = wd / "repo"
    wt(repo / "src/retry.py", "import time\n\n\ndef with_backoff(fn, attempts=3):\n    \"\"\"Project convention: retries use with_backoff.\"\"\"\n    return fn()\n")
    wt(repo / "src/client.py", "from retry import with_backoff\n\n\ndef get(url):\n    return with_backoff(lambda: url)\n")
    sh(["git", "init", "-q"], cwd=repo)
    before = _hashes(repo / "src")
    reqs = {"rename variable x to count in client.py": "Minimal", "add a retry flag default for uploads": "Compact",
            "add a public API for webhooks with auth": "Full"}
    tri = {r: _triage(r) for r in reqs}
    rc, out = sh(["rg", "-n", "--no-heading", "def with_backoff", "src"], cwd=repo)
    hit = out.strip().splitlines()[0] if rc == 0 else ""
    f, line = hit.split(":")[0], int(hit.split(":")[1]) if hit else 0
    real = (repo / f).read_text().splitlines()[line - 1] if hit else ""
    cap = {"Outcome": "uploads retry transient failures, observable as <=3 attempts in logs",
           "Material defaults/non-goal": "default attempts=3 via existing helper; no new retry library",
           "Repository evidence": "%s:%d `%s`" % (f, line, real.strip()),
           "Risk": "double-submit on non-idempotent uploads", "Handoff": "suggested next: /delivery-flow:delivery-flow"}
    capsule = wt(wd / "capsule.md", "\n".join("- **%s:** %s" % kv for kv in cap.items()) + "\n")

    def valid(text):
        got = dict(re.findall(r"^- \*\*(.+?):\*\* (.+)$", text, re.M))
        ev = re.match(r"(\S+):(\d+) ", got.get("Repository evidence", ""))
        return all(got.get(k) for k in cap) and bool(ev) and (repo / ev.group(1)).exists()
    no_ev = capsule.read_text().replace(cap["Repository evidence"], "we usually retry somewhere")
    return [
        check("triage picks Minimal / Compact / Full", list(tri.values()) == list(reqs.values()), tri),
        check("one exact-text search finds the convention at its real line", "def with_backoff" in real and line == 4, hit, "src/retry.py:4"),
        check("capsule has the five fields and evidence resolves to a real file:line", valid(capsule.read_text()), True, True),
        check("standalone brainstorm edited no code", _hashes(repo / "src") == before, True, True),
        check("negative control: a capsule with unsourced evidence fails validation", not valid(no_ev), valid(no_ev), False),
    ], [capsule]


EARS = re.compile(r"^(?:(?:WHEN|WHILE|IF|WHERE) .+?,?\s*)?THE SYSTEM SHALL .+$")


def _spec_check(req_md, tasks_md):
    us = re.findall(r"^### (US-\d+)", req_md, re.M)
    crit = re.findall(r"^\d+\. (.+)$", req_md, re.M)
    bad_ears = [c for c in crit if not EARS.match(c)]
    tasks = {}
    for blk in re.split(r"^### ", tasks_md, flags=re.M)[1:]:
        tid = blk.split(":")[0]
        f = dict(re.findall(r"^- \*\*(\w+)\*\*: (.+)$", blk, re.M))
        tasks[tid] = f
    covered = {u for t in tasks.values() for u in re.findall(r"US-\d+", t.get("Requirements", ""))}
    uncovered = [u for u in us if u not in covered]
    order, seen, cyc = [], set(), []

    def visit(t, stack):
        if t in stack:
            cyc.append(t)
            return
        if t in seen:
            return
        for d in re.findall(r"T-\d+", tasks.get(t, {}).get("Dependencies", "")):
            visit(d, stack | {t})
        seen.add(t)
        order.append(t)
    for t in tasks:
        visit(t, set())
    bad_status = [t for t, f in tasks.items() if f.get("Status") not in ("pending", "in_progress", "completed")]
    return {"us": us, "bad_ears": bad_ears, "uncovered": uncovered, "cycle": cyc, "order": order, "bad_status": bad_status}


@card(P + "1497-spec-driven/3713-spec-workflow")
def spec_workflow(task, wd):
    """requirements.md (EARS), design.md, tasks.md -> EARS lint, requirement->task traceability, dependency order."""
    d = wd / ".claude/specs/password-reset"
    req = wt(d / "requirements.md", """
        # Requirements: password reset
        ### US-1 Request a reset link
        1. WHEN a user submits a registered email THE SYSTEM SHALL send a reset link within 60 seconds
        2. IF the email is not registered THE SYSTEM SHALL show the same confirmation message
        ### US-2 Set a new password
        1. WHILE the reset token is unexpired THE SYSTEM SHALL accept a new password of at least 12 characters
        ### US-3 Audit
        1. THE SYSTEM SHALL log every reset request without the token value
        ## Out of scope
        - SMS reset
        """)
    wt(d / "design.md", "# Design\n## Components\n- TokenStore\n- Mailer\n- ResetController\n## Data flow\nController -> TokenStore -> Mailer\n")
    tsk = wt(d / "tasks.md", """
        ### T-1: Token store
        - **Status**: completed
        - **Requirements**: US-1, US-2
        - **Dependencies**: none
        ### T-2: Mailer
        - **Status**: in_progress
        - **Requirements**: US-1
        - **Dependencies**: T-1
        ### T-3: Reset form
        - **Status**: pending
        - **Requirements**: US-2
        - **Dependencies**: T-1
        ### T-4: Audit log
        - **Status**: pending
        - **Requirements**: US-3
        - **Dependencies**: T-2, T-3
        """)
    r = _spec_check(req.read_text(), tsk.read_text())
    rep = jw(wd / "spec_check.json", r)
    bad_req = req.read_text() + "### US-4 Speed\n1. The system should be fast\n"
    bad_tasks = tsk.read_text().replace("- **Dependencies**: none", "- **Dependencies**: T-4")
    rb = _spec_check(bad_req, bad_tasks)
    return [
        check("all acceptance criteria are EARS statements", r["bad_ears"] == [] and len(r["us"]) == 3, r["bad_ears"], []),
        check("every user story is covered by a task", r["uncovered"] == [], r["uncovered"], []),
        check("dependency order is a valid topological order", r["order"].index("T-1") < r["order"].index("T-2") < r["order"].index("T-4")
              and not r["cycle"], r["order"]),
        check("task statuses valid", r["bad_status"] == [], r["bad_status"], []),
        check("negative control: vague requirement, uncovered story and a dependency cycle are all caught",
              rb["bad_ears"] and rb["uncovered"] == ["US-4"] and rb["cycle"], [rb["bad_ears"], rb["uncovered"], rb["cycle"]]),
    ], [rep, req, tsk]


CLAIM_PATTERNS = [
    ("statistical", r"(\d+(?:\.\d+)?)% (?:increase|reduction) in \w+"),
    ("statistical", r"\w+ rate is (\d+(?:\.\d+)?)%"),
    ("statistical", r"(\d+(?:\.\d+)?)x (ROAS|faster)"),
    ("performance", r"([\d,]+)\+ (customers|users)"),
    ("ranking", r"(#1) ([a-z ]+?)(?= in| for|\.|,)"),
    ("award", r"(ISO \d+|SOC 2) (certified|compliant)"),
    ("citation", r"according to ([A-Z][a-z]+)"),
]


@card(P + "1520-digital-marketing-pro/4131-verify-claims")
def verify_claims(task, wd):
    """Extract verifiable claims, match each to evidence, classify verified / partial / unverified / contradicted,
    flag stale (>12 months) evidence, and score."""
    import datetime as dt
    content = ("Acme delivered a 73% increase in conversions and 4.8x ROAS for retail brands. Trusted by 10,000+ customers, "
               "we are the #1 rated scheduling tool. Acme is ISO 27001 certified, and according to Gartner adoption is surging. "
               "Our churn rate is 2% for annual plans.")
    ev = [{"claim": "increase in conversions", "value": 73.0, "date": "2026-06-01", "source": "GA4 export"},
          {"claim": "ROAS", "value": 3.1, "date": "2026-05-01", "source": "ads report"},
          {"claim": "customers", "value": 9800, "date": "2026-07-01", "source": "CRM"},
          {"claim": "ISO 27001", "value": None, "date": "2024-02-01", "source": "certificate"},
          {"claim": "churn rate", "value": 2.0, "date": "2026-08-01", "source": "billing"}]
    jw(wd / "evidence.json", ev)
    claims = []
    for kind, pat in CLAIM_PATTERNS:
        for m in re.finditer(pat, content):
            claims.append({"type": kind, "text": m.group(0), "value": m.group(1), "pos": m.start()})
    claims.sort(key=lambda c: c["pos"])
    today = dt.date(2026, 11, 3)
    for c in claims:
        e = next((e for e in ev if e["claim"].lower() in c["text"].lower()), None)
        if e is None:
            c["status"] = "unverified"
            continue
        c["evidence"] = e["source"]
        stale = (today - dt.date.fromisoformat(e["date"])).days > 365
        if e["value"] is None:
            c["status"] = "partially verified (stale)" if stale else "verified"
            continue
        v = float(c["value"].replace(",", "").replace("#", ""))
        rel = (v - e["value"]) / e["value"]
        c["status"] = "verified" if abs(rel) <= 0.02 else ("contradicted" if rel > 0.10 else "partially verified")
        if c["status"] != "verified":
            c["fix"] = "use %s (%s)" % (e["value"], e["source"])
    ok = sum(1 for c in claims if c["status"].startswith(("verified", "partially")))
    score = round(100 * ok / len(claims))
    rep = jw(wd / "claims_report.json", {"score": score, "claims": claims})
    st = {c["text"]: c["status"] for c in claims}
    naive = sum(1 for c in claims if re.search(r"\d", c["text"])) / len(claims)
    return [
        check("7 claims extracted across 5 types", len(claims) == 7 and len({c["type"] for c in claims}) == 5, len(claims), 7),
        check("73% conversions verified, churn 2% verified", st["73% increase in conversions"] == "verified" and st.get("churn rate is 2%") == "verified", st),
        check("4.8x ROAS contradicted by 3.1 evidence (overstated 55%)", st["4.8x ROAS"] == "contradicted", st["4.8x ROAS"], "contradicted"),
        check("10,000+ vs 9,800 customers is partial (2.04% over)", st["10,000+ customers"] == "partially verified", st["10,000+ customers"]),
        check("ISO 27001 evidence older than 12 months flagged stale", "stale" in st["ISO 27001 certified"], st["ISO 27001 certified"]),
        check("#1 ranking and Gartner citation unverified", st["#1 rated scheduling tool"] == "unverified"
              and st["according to Gartner"] == "unverified", [st["#1 rated scheduling tool"], st["according to Gartner"]]),
        check("verification score = 4/7 = 57", score == 57, score, 57),
        check("negative control: 'claim has a number' passes most claims including the contradicted one", naive > 0.5, naive, ">0.5"),
    ], [rep]


@card(P + "1528-safeguard/4180-trust-and-safety-review")
def trust_and_safety_review(task, wd):
    """Model content flows as a graph and find abuse paths that reach an audience without moderation
    (API import, edit-after-approval), plus missing report/block/rate-limit controls per surface."""
    design = {"edges": [["create", "moderation"], ["moderation", "publish"], ["publish", "edit"], ["edit", "publish"],
                        ["api_import", "publish"], ["publish", "email_digest"], ["publish", "search_index"]],
              "audience": ["publish"], "moderation": ["moderation"], "sources": ["create", "api_import", "edit"],
              "controls": {"listing": ["report", "rate_limit"], "message": ["report"], "profile": ["report", "block"]}}
    fixed = json.loads(json.dumps(design))
    fixed["edges"] = [["create", "moderation"], ["moderation", "publish"], ["publish", "edit"], ["edit", "moderation"],
                      ["api_import", "moderation"], ["publish", "email_digest"], ["publish", "search_index"]]
    fixed["controls"] = {k: ["report", "block", "rate_limit"] for k in design["controls"]}
    jw(wd / "design.json", design)

    def bypasses(d):
        g = {}
        for a, b in d["edges"]:
            g.setdefault(a, []).append(b)
        found = []
        for s in d["sources"]:
            stack = [(s, [s])]
            while stack:
                n, path = stack.pop()
                if n in d["moderation"]:
                    continue
                if n in d["audience"] and len(path) > 1:
                    found.append("->".join(path))
                    continue
                stack += [(m, path + [m]) for m in g.get(n, []) if m not in path]
        return sorted(found)
    need = {"report", "block", "rate_limit"}
    gaps = {k: sorted(need - set(v)) for k, v in design["controls"].items() if need - set(v)}
    b = bypasses(design)
    bf = bypasses(fixed)
    rep = wt(wd / "tns_findings.md", "# Trust and safety findings\n\n" + "\n".join(
        "- HIGH: unmoderated path %s (content reaches the audience without review)" % p for p in b) + "\n" +
        "\n".join("- MEDIUM: %s surface lacks %s" % (k, ", ".join(v)) for k, v in gaps.items()) +
        "\n\nRecommendation: route edit and API import back through moderation; add block + rate limits.\n")
    return [
        check("two bypass paths found: API import and edit-after-approval", b == ["api_import->publish", "edit->publish"], b),
        check("missing controls per surface", gaps == {"listing": ["block"], "message": ["block", "rate_limit"], "profile": ["rate_limit"]}, gaps),
        check("fixed design has no unmoderated path to the audience", bf == [], bf, []),
        check("negative control: the happy-path check (create passes moderation) passes the flawed design",
              "create" not in " ".join(b), "create" not in " ".join(b), True),
    ], [rep]


SAFE_START = set("-?:,[]{}#&*!|>'\"%@`")


def _fm_lines(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    return (m.group(1).split("\n"), m.group(0)) if m else ([], "")


def _fm_value_ok(v):
    if v.startswith('"'):
        try:
            return isinstance(json.loads(v), str)
        except ValueError:
            return False
    if v.startswith("'"):
        return False
    return bool(v) and v[0] not in SAFE_START and ": " not in v and " #" not in v and not v.endswith(":")


def _skill_standards(path):
    lines, block = _fm_lines(path.read_text(encoding="utf-8"))
    issues, vals = [], {}
    for ln in lines:
        m = re.match(r"^([a-z_-]+): (.+)$", ln)
        if not m:
            issues.append("not key: value -> %r" % ln)
            continue
        k, v = m.groups()
        vals[k] = v
        if not _fm_value_ok(v):
            issues.append("non-canonical value for %s" % k)
    raw_desc = vals.get("description", "")
    desc = json.loads(raw_desc) if raw_desc.startswith('"') and _fm_value_ok(raw_desc) else raw_desc
    if len(desc) > 500:
        issues.append("description %d > 500 chars" % len(desc))
    if len(block) > 1024:
        issues.append("frontmatter > 1024")
    name = vals.get("name", "")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name) or name != path.parent.name:
        issues.append("name not kebab-case or != directory")
    if "when_to_use" not in vals and not desc.startswith("Use when"):
        issues.append("description must start with 'Use when'")
    return issues


def _fm_fix(path):
    text = path.read_text(encoding="utf-8")
    lines, block = _fm_lines(text)
    out = []
    for ln in lines:
        m = re.match(r"^([a-z_-]+):\s*(.+)$", ln)
        k, v = m.groups()
        if _fm_value_ok(v):
            out.append(ln)
            continue
        if v.startswith("'") and v.endswith("'"):
            v = v[1:-1].replace("''", "'")
        elif v.startswith('"'):
            v = v.strip('"')
        out.append("%s: %s" % (k, json.dumps(v, ensure_ascii=False)))
    path.write_text("---\n" + "\n".join(out) + "\n---\n" + text[len(block):], encoding="utf-8")
    return out


@card(P + "1543-toolkit-ops/4233-toolkit-skill-standards")
def toolkit_skill_standards(task, wd):
    """Budgets, trigger contract and canonical frontmatter form, a --fix that rewrites only illegal values,
    and a strict YAML parse proving the form."""
    import yaml
    good = wt(wd / "skills/log-triage/SKILL.md", "---\nname: log-triage\ndescription: Use when a CI log fails and you need the first real error, not the noise.\n---\n# Log triage\n")
    bad = wt(wd / "skills/pdf-tools/SKILL.md", "---\nname: PDF_Tools\ndescription: 'Merges PDFs: that''s all'\nversion: 1.0 # pinned\nowner: team\n---\n# body\n")
    g_issues = _skill_standards(good)
    b_issues = _skill_standards(bad)
    before_lines = _fm_lines(bad.read_text())[0]
    fixed_lines = _fm_fix(bad)
    unchanged = [ln for ln in before_lines if ln in fixed_lines]
    parsed = yaml.safe_load(bad.read_text().split("---\n")[1])
    after = _skill_standards(bad)
    rep = jw(wd / "standards_report.json", {"good": g_issues, "bad_before": b_issues, "fixed_frontmatter": fixed_lines, "bad_after": after})
    return [
        check("compliant skill passes every rule", g_issues == [], g_issues, []),
        check("single quotes, ' #' comment value, non-kebab name and missing 'Use when' all caught",
              sum(1 for i in b_issues if "non-canonical" in i) == 2 and any("kebab" in i for i in b_issues)
              and any("Use when" in i for i in b_issues), b_issues),
        check("--fix rewrites illegal values to JSON double quotes and leaves legal lines byte-identical",
              fixed_lines[1] == 'description: "Merges PDFs: that\'s all"' and "owner: team" in unchanged and "name: PDF_Tools" in unchanged,
              fixed_lines),
        check("strict YAML parse of the fixed frontmatter returns the intended values",
              parsed["description"] == "Merges PDFs: that's all" and parsed["version"] == "1.0 # pinned", parsed),
        check("after fix only the human decisions remain (name, trigger wording)",
              all("non-canonical" not in i for i in after) and len(after) == 2, after),
        check("negative control: the original file fails the canonical-form gate", len(b_issues) >= 4, len(b_issues), ">=4"),
    ], [rep, bad]


# ================================================================ data, code-walkthrough, provenance, legal
@card(P + "1550-ml-pipeline/4304-ml-pipeline")
def ml_pipeline(task, wd):
    """Steps 1-3 + 6 for real (profile, EDA figures, leakage suspects, time-based split with a frozen test
    fingerprint) and the gate hook that refuses training until Gate A/B approval lines exist."""
    import hashlib
    import numpy as np
    import pandas as pd
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    rng = np.random.default_rng(7)
    n = 400
    df = pd.DataFrame({"signup": pd.date_range("2025-01-01", periods=n, freq="D"),
                       "visits": rng.poisson(5, n), "plan": rng.choice(["free", "pro"], n, p=[.7, .3])})
    df["churned"] = (rng.random(n) < 0.12).astype(int)
    df["refund_issued"] = df["churned"]  # leakage: only known after the outcome
    df.loc[rng.choice(np.arange(12, n), 20, replace=False), "visits"] = np.nan
    df = pd.concat([df, df.iloc[:12]], ignore_index=True)
    mp = wd / "ml_pipeline"
    (mp / "figures").mkdir(parents=True, exist_ok=True)
    df.to_csv(mp / "raw.csv", index=False)
    raw_sha = hashlib.sha256((mp / "raw.csv").read_bytes()).hexdigest()
    dups = int(df.duplicated().sum())
    num = df.select_dtypes("number").drop(columns=["churned"])
    leak = sorted(c for c in num if abs(num[c].corr(df["churned"])) > 0.95)
    profile = {"rows": len(df), "cols": df.shape[1], "duplicates": dups, "missing": {"visits": int(df["visits"].isna().sum())},
               "leakage_suspects": leak, "traits": {"has_datetime": True, "minority_share": round(float(df["churned"].mean()), 3)}}
    jw(mp / "data_profile.json", profile)
    for name, plot in [("01_missingness", lambda ax: ax.bar(df.columns, df.isna().sum())),
                       ("02_target_balance", lambda ax: ax.bar(["stay", "churn"], df["churned"].value_counts().sort_index()))]:
        fig, ax = plt.subplots(figsize=(4, 3))
        plot(ax)
        fig.savefig(mp / "figures" / (name + ".png"), dpi=60)
        plt.close(fig)
    clean = df.drop_duplicates().drop(columns=leak).sort_values("signup")
    a, b = int(len(clean) * .7), int(len(clean) * .85)
    train, val, test = clean.iloc[:a], clean.iloc[a:b], clean.iloc[b:]
    fp = hashlib.sha256(pd.util.hash_pandas_object(test, index=True).values.tobytes()).hexdigest()
    overlap = len(set(train.index) & set(test.index)) + len(set(train.index) & set(val.index))
    rnd = clean.sample(frac=1, random_state=0)
    r_train, r_test = rnd.iloc[:a], rnd.iloc[b:]
    steps = ["Data inspection", "EDA", "Define the prediction problem", "Data cleaning", "Data engineering", "Split",
             "Feature engineering", "Preprocessing", "Baseline model", "Model training", "Hyperparameter tuning", "Model evaluation",
             "Error analysis", "Final test", "Deployment", "Monitoring + retraining plan"]
    status = {1: "done", 2: "done", 3: "done", 6: "done"}
    pl = wt(mp / "PIPELINE.md", "# ML pipeline\n" + "\n".join("- [%s] %d. %s" % (status.get(i, "todo"), i, s) for i, s in enumerate(steps, 1)) +
            "\n\n## Gates\n- Gate A: pending (contract awaiting user)\n- Test fingerprint: %s\n" % fp)

    def hook(text, gate_needed="B"):
        ok = {g for g in "ABCD" if re.search(r"^- Gate %s: approved \d{4}-\d\d-\d\d$" % g, text, re.M)}
        ok |= {g for g in "ABCD" if re.search(r"^- Override: Gate %s - user approved" % g, text, re.M)}
        need = {"A", "B"} if gate_needed == "B" else {"A"}
        rationale = all(re.search(r"^- %s: " % k, text, re.M) for k in ["traits", "baseline", "candidates", "ruled out", "metric"])
        return need <= ok and (gate_needed != "B" or rationale)
    parser_fixture = ("- Gate A: approved 2026-09-16\n- Gate B: approved 2026-09-17\nModel rationale:\n- traits: binary\n"
                      "- baseline: dummy\n- candidates: gbm\n- ruled out: knn\n- metric: PR-AUC\n")
    return [
        check("profile: 412 rows, 12 exact duplicates, 20 missing visits", profile["rows"] == 412 and dups == 12
              and profile["missing"]["visits"] == 20, [profile["rows"], dups, profile["missing"]["visits"]]),
        check("leakage suspect found (refund_issued mirrors the target)", leak == ["refund_issued"], leak),
        check("EDA figures written", all((mp / "figures" / f).stat().st_size > 0 for f in ["01_missingness.png", "02_target_balance.png"]), 2, 2),
        check("time-based split: no shared rows, train ends before val, val before test", overlap == 0
              and train["signup"].max() < val["signup"].min() and val["signup"].max() < test["signup"].min(), overlap, 0),
        check("raw data untouched (read-only step 1)", hashlib.sha256((mp / "raw.csv").read_bytes()).hexdigest() == raw_sha, True, True),
        check("gate hook refuses training while Gate A is pending", hook(pl.read_text()) is False, False, False),
        check("hook parser accepts the exact approval + 5-bullet rationale shape", hook(parser_fixture) is True, True, True),
        check("negative control: a random split puts test dates before training dates (temporal leakage)",
              r_test["signup"].min() < r_train["signup"].max(), str(r_test["signup"].min().date()), "< train max"),
    ], [pl, mp / "data_profile.json"]


@card(P + "162-code-tour/531-code-tour")
def code_tour(task, wd):
    """CodeTour .tour JSON for a fixture repo with every file/line verified; pattern steps survive edits."""
    repo = wd / "repo"
    wt(repo / "README.md", "# shop\n")
    wt(repo / "src/app.py", "from store import Store\n\n\ndef main():\n    s = Store()\n    s.add('pen', 2)\n    return s.total()\n")
    wt(repo / "src/store.py", "class Store:\n    def __init__(self):\n        self.items = {}\n\n    def add(self, k, n):\n        self.items[k] = n\n\n    def total(self):\n        return sum(self.items.values())\n")
    anchors = [("src/app.py", "def main", "Entry point"), ("src/store.py", "class Store", "The one domain object"),
               ("src/store.py", "def total", "Where the answer is computed")]
    steps = [{"title": "Welcome", "description": "A 3-stop tour of the shop for a new joiner."},
             {"directory": "src", "title": "Source layout", "description": "All code lives in src/."}]
    for f, pat, title in anchors:
        lines = (repo / f).read_text().splitlines()
        ln = next(i for i, x in enumerate(lines, 1) if pat in x)
        steps.append({"file": f, "line": ln, "title": title, "description": "`%s` at line %d." % (pat, ln), "_anchor": pat})
    steps.append({"file": "src/store.py", "pattern": "def add", "title": "Adding items", "description": "Pattern step: survives edits."})
    tour = {"$schema": "https://aka.ms/codetour-schema", "title": "Shop — new-joiner / overview", "steps": steps}
    clean = {**tour, "steps": [{k: v for k, v in s.items() if not k.startswith("_")} for s in steps]}
    tf = jw(repo / ".tours/new-joiner-overview.tour", clean)

    def validate(t, root):
        bad = []
        for s, src in zip(t["steps"], steps):
            if "file" in s:
                p = root / s["file"]
                if not p.exists():
                    bad.append("missing " + s["file"])
                    continue
                lines = p.read_text().splitlines()
                if "line" in s and (s["line"] > len(lines) or src.get("_anchor", "") not in lines[s["line"] - 1]):
                    bad.append("stale %s:%d" % (s["file"], s["line"]))
                if "pattern" in s and not re.search(s["pattern"], p.read_text()):
                    bad.append("pattern gone " + s["pattern"])
            if "directory" in s and not (root / s["directory"]).is_dir():
                bad.append("missing dir")
        return bad
    ok = validate(clean, repo)
    content_steps = sum(1 for s in clean["steps"] if set(s) <= {"title", "description"})
    shifted = wd / "shifted"
    shutil.copytree(repo, shifted)
    (shifted / "src/store.py").write_text("# header added later\n\n" + (shifted / "src/store.py").read_text())
    stale = validate(clean, shifted)
    return [
        check("every file/line anchor verified against the real file", ok == [], ok, []),
        check("schema, title and 6 steps (<= 2 content-only steps)", clean["$schema"].endswith("codetour-schema")
              and len(clean["steps"]) == 6 and content_steps == 1, [len(clean["steps"]), content_steps]),
        check("line numbers found by search (main=4, Store=1, total=8)", [s.get("line") for s in clean["steps"] if "line" in s] == [4, 1, 8],
              [s.get("line") for s in clean["steps"] if "line" in s]),
        check("negative control: after an edit the line anchors go stale while the pattern step survives",
              len(stale) == 2 and not any("pattern" in x for x in stale), stale),
    ], [tf]


@card(P + "163-collab-proof/532-collab-proof")
def collab_proof(task, wd):
    """Layer 01 signal from real git history + conversation, a WORKLOG/DECISIONS proof, and the tamper-evident
    sha256 attached with git notes and re-verified."""
    import hashlib
    repo = wd / "repo"
    env = {"GIT_AUTHOR_NAME": "dev", "GIT_AUTHOR_EMAIL": "dev@example.com", "GIT_COMMITTER_NAME": "dev",
           "GIT_COMMITTER_EMAIL": "dev@example.com", "GIT_CONFIG_GLOBAL": str(wd / "gitconfig"), "GIT_CONFIG_NOSYSTEM": "1"}
    wt(wd / "gitconfig", "[init]\n\tdefaultBranch = main\n")
    g = lambda *a: sh(["git", *a], cwd=repo, env=env)  # noqa: E731
    repo.mkdir()
    g("init", "-q")
    wt(repo / "app.py", "def rate(x):\n    return x\n")
    wt(repo / "README.md", "# Ap\n")
    g("add", "-A"), g("commit", "-qm", "init")
    wt(repo / "README.md", "# App\n")
    g("add", "-A"), g("commit", "-qm", "fix typo in readme")
    wt(repo / "limiter.lua", "-- token bucket\nreturn 1\n")
    wt(repo / "app.py", "def rate(x):\n    return min(x, 10)\n")
    g("add", "-A"), g("commit", "-qm", "fix rate limiter race")
    convo = "The bug was caused by two workers reading the counter before either wrote it, because the check was not atomic. Chose a Lua script instead of a lock because Redis runs it atomically."

    def signal(rev_range, conversation):
        stat = g("diff", "--numstat", "--diff-filter=AM", rev_range)[1].strip().splitlines()
        added = g("diff", "--name-only", "--diff-filter=A", rev_range)[1].split()
        files = len(stat)
        root = bool(re.search(r"(the bug was|caused by|because)", conversation, re.I))
        if added or files >= 4 or root:
            return "HIGH", {"new_files": added, "files": files, "root_cause": root}
        if files <= 1 and re.search(r"(change this text|fix typo|rename variable)", conversation, re.I):
            return "LOW", {"files": files}
        if files:
            return "MEDIUM", {"files": files}
        return "LOW", {}
    s_hi, why_hi = signal("HEAD~1..HEAD", convo)
    s_lo, _ = signal("HEAD~2..HEAD~1", "change this text")
    s_med, _ = signal("HEAD~2..HEAD~1", "updated the heading")
    sig_lo = s_lo
    proof = wt(wd / "proof.html", "<html><body><h1>Session proof</h1><h2>Decision</h2><p>Lua script over lock: atomic in Redis.</p>"
               "<h2>Root cause</h2><p>%s</p><p>Signal: %s</p></body></html>\n" % (convo, s_hi))
    digest = hashlib.sha256(proof.read_bytes()).hexdigest()
    g("notes", "add", "-f", "-m", "collab-proof sha256: " + digest, "HEAD")
    note = g("notes", "show", "HEAD")[1].strip()
    verified = note.endswith(hashlib.sha256(proof.read_bytes()).hexdigest())
    tampered = wd / "proof_tampered.html"
    tampered.write_text(proof.read_text().replace("Lua script", "Mutex"))
    t_ok = note.endswith(hashlib.sha256(tampered.read_bytes()).hexdigest())
    wl = wt(wd / "WORKLOG.md", "# Worklog\n- %s: %s (signal %s)\n" % (g("rev-parse", "--short", "HEAD")[1].strip(),
                                                                     "fix rate limiter race", s_hi))
    return [
        check("bug fix with root-cause discussion and a new file -> HIGH", s_hi == "HIGH" and why_hi["new_files"] == ["limiter.lua"]
              and why_hi["root_cause"], [s_hi, why_hi]),
        check("trivial typo session -> LOW (routine, nothing recorded)", sig_lo == "LOW", sig_lo, "LOW"),
        check("same 1-file change without trivial context -> MEDIUM (WORKLOG only)", s_med == "MEDIUM", s_med, "MEDIUM"),
        check("proof hash attached as a git note on HEAD and re-verified", note.startswith("collab-proof sha256: ") and verified, note[:40]),
        check("negative control: an edited proof no longer matches the note", t_ok is False, t_ok, False),
    ], [proof, wl]


IRS = {"Instructions": r"shall follow company'?s procedures", "Training": r"mandatory onboarding", "Integration": r"exclusive",
       "Personal services": r"may not subcontract|personally perform", "Hiring assistants": r"no subcontractors",
       "Continuing relationship": r"renews automatically|indefinite", "Set hours": r"core hours|9:00", "Full-time required": r"exclusive|best efforts",
       "Work on premises": r"on-site|company offices", "Order of work": r"step-by-step", "Reports required": r"daily standup|timesheets",
       "Payment method": r"hourly", "Expenses": r"company will reimburse|equipment provided", "Tools/materials": r"company laptop|company systems",
       "Investment": r"company laptop", "Profit/loss": r"guaranteed minimum", "Multiple clients": r"non-compete|exclusive",
       "Public availability": r"may not market", "Right to fire": r"at any time without cause", "Right to quit": r"no termination fee for contractor"}


def _freelancer(text):
    t = text.lower()
    hits = sorted(k for k, p in IRS.items() if re.search(p, t))
    n = len(hits)
    risk = "LOW" if n <= 5 else "MODERATE" if n <= 10 else "HIGH" if n <= 15 else "CRITICAL"
    net = int(re.search(r"net[- ](\d+)", t).group(1)) if re.search(r"net[- ](\d+)", t) else 90
    lens = {
        "Misclassification Risk": {"LOW": 9, "MODERATE": 5, "HIGH": 3, "CRITICAL": 1}[risk],
        "IP Ownership": 8 if "background ip" in t else 2,
        "Payment Terms": 9 if net <= 15 else 7 if net <= 30 else 3,
        "Payment Amount": 6, "Kill Fee / Cancellation": 8 if "kill fee" in t else 1,
        "Scope Definition": 8 if "statement of work" in t else 4, "Scope Creep Protection": 8 if "change order" in t else 3,
        "Non-Compete Clause": 2 if "non-compete" in t else 9, "Non-Solicitation": 5, "Confidentiality Burden": 7 if "mutual" in t else 4,
        "Termination Rights": 7 if "either party may terminate" in t else 3, "Liability Exposure": 7 if "capped" in t else 2,
        "Dispute Resolution": 4 if "arbitration" in t else 7, "Credit and Portfolio": 8 if "portfolio" in t else 3}
    rights = ["own schedule" in t, "other clients" in t, "subcontract with notice" in t, "own location" in t, "own tools" in t,
              "background ip" in t, "portfolio" in t, net <= 30, "late payment" in t, "kill fee" in t, "change order" in t,
              "out-of-scope" in t, "revision" in t, "either party may terminate" in t, "mutual" in t, "non-compete" not in t,
              "capped" in t, "arbitration" not in t, "in writing" in t, "credit" in t]
    pay = (lens["Payment Terms"] + lens["Kill Fee / Cancellation"] + (8 if "late payment" in t else 2)) / 30 * 10
    score = round(sum(lens.values()) / 14 / 10 * 50 + {"LOW": 20, "MODERATE": 12, "HIGH": 6, "CRITICAL": 0}[risk]
                  + sum(rights) / 20 * 20 + pay)
    grade = "A" if score >= 90 else "B" if score >= 80 else "C" if score >= 70 else "D" if score >= 60 else "F"
    return {"irs_hits": hits, "risk": risk, "lens": lens, "rights": sum(rights), "pay": round(pay, 2), "score": score, "grade": grade,
            "playbook": sorted(k for k, v in lens.items() if v <= 5)}


@card(P + "1634-general-legal-assistant/4612-freelancer-review")
def freelancer_review(task, wd):
    """14 lenses + IRS 20-factor indicator count + Bill of Rights -> Freelancer Fairness Score, on two contracts."""
    client = wt(wd / "client_contract.txt", """Independent Contractor Agreement. Contractor shall follow Company's procedures and attend
        mandatory onboarding. Contractor works core hours 9:00-17:00 at company offices on-site and joins the daily standup with
        timesheets. Paid hourly, net-60. Contractor may not subcontract and is exclusive to Company. A 24-month non-compete applies.
        All work product and any IP are assigned to Company. Company may end this agreement at any time without cause.
        Disputes go to binding arbitration in Company's city.""")
    fair = wt(wd / "fair_contract.txt", """Statement of work attached. Contractor sets own schedule, works from own location with own
        tools, may serve other clients and may subcontract with notice. Contractor keeps background IP; deliverables may be shown in
        a portfolio with credit. Milestone payments net-15 with a 1.5% late payment charge; a kill fee of 50% applies on
        cancellation. Out-of-scope work is billed via a change order agreed in writing; two revision rounds included. Either party
        may terminate on 14 days notice. Liability capped at fees paid. Mutual confidentiality.""")
    rc, rf = _freelancer(client.read_text()), _freelancer(fair.read_text())
    rep = wt(wd / "FREELANCER-REVIEW-2026-11-03.md", "# Freelancer Contract Review\n## Freelancer Fairness Score: %d/100 (%s)\n\n" % (rc["score"], rc["grade"]) +
             md_table([(i + 1, k, v) for i, (k, v) in enumerate(rc["lens"].items())], ["#", "Lens", "Score (1-10)"]) +
             "\n\n### IRS 20-Factor Test Results\n%d indicators: %s\n### Risk Level: %s\n\n## Negotiation playbook\n%s\n\n"
             "Not legal advice.\n" % (len(rc["irs_hits"]), ", ".join(rc["irs_hits"]), rc["risk"], "\n".join("- " + p for p in rc["playbook"])))
    lens_avg = sum(rc["lens"].values()) / 14
    recomputed = round(lens_avg / 10 * 50 + 6 + rc["rights"] / 20 * 20 + rc["pay"])
    labelled_ic = "independent contractor" in client.read_text().lower()
    return [
        check("client contract: 11+ employment indicators -> HIGH misclassification risk", len(rc["irs_hits"]) >= 11 and rc["risk"] == "HIGH",
              [len(rc["irs_hits"]), rc["risk"]]),
        check("score recomputes from the weighted formula (50/20/20/10)", recomputed == rc["score"], rc["score"], recomputed),
        check("client contract grades F, fair contract grades B or better", rc["grade"] == "F" and rf["grade"] in "AB", [rc["score"], rf["score"]]),
        check("playbook covers every lens scoring <= 5 (IP, kill fee, non-compete, ...)", {"IP Ownership", "Kill Fee / Cancellation",
              "Non-Compete Clause"} <= set(rc["playbook"]), rc["playbook"]),
        check("fair contract: LOW risk", rf["risk"] == "LOW", rf["risk"], "LOW"),
        check("negative control: the 'Independent Contractor' title alone would suggest no misclassification issue", labelled_ic, labelled_ic, True),
    ], [rep]


# ================================================================ React (real React 19 in headless Chrome)
NODE_MODULES = "/opt/node22/lib/node_modules"


def _chrome():
    for c in ["google-chrome", "chromium", "chromium-browser"]:
        if shutil.which(c):
            return shutil.which(c)
    for p in sorted(Path("/opt/pw-browsers").glob("chromium-*/chrome-linux64/chrome")):
        return str(p)
    return None


def _bundle_and_run(wd, name, jsx, budget=3000):
    src = wt(wd / (name + ".jsx"), jsx)
    out = wd / (name + ".js")
    script = wt(wd / ("build_" + name + ".cjs"), "require(%s).buildSync({entryPoints:[%s],bundle:true,outfile:%s,jsx:'automatic',"
                "nodePaths:[%s],alias:{react:%s},define:{'process.env.NODE_ENV':'\"production\"'},logLevel:'error'});" % (
                    json.dumps(NODE_MODULES + "/esbuild"), json.dumps(str(src)), json.dumps(str(out)), json.dumps(NODE_MODULES), json.dumps(NODE_MODULES + "/react")))
    fx.run(["node", script], timeout=60)
    page = wt(wd / (name + ".html"), "<!doctype html><html><body><div id=root></div><script src=%s></script></body></html>" % out.name)
    done = subprocess.run([_chrome(), "--headless=new", "--no-sandbox", "--disable-gpu", "--allow-file-access-from-files",
                           "--virtual-time-budget=%d" % budget, "--dump-dom", page.as_uri()], capture_output=True, text=True,
                          timeout=40, stdin=subprocess.DEVNULL)
    import html as _h
    m = re.search(r'data-r="([^"]*)"', done.stdout)
    if not m:
        raise RuntimeError("page produced no result: " + done.stderr[-300:])
    return json.loads(_h.unescape(m.group(1)))


REACT_RACE = r'''
import { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import { flushSync } from "react-dom";

const DELAY = { a: 400, ab: 50 };                       // the older request answers last
const fetchHits = (q) => new Promise((res) => setTimeout(() => res(q.toUpperCase() + "-results"), DELAY[q]));

function Search({ query, guard }) {
  const [hits, setHits] = useState("loading");
  useEffect(() => {
    let ignore = false;
    fetchHits(query).then((h) => { if (!guard || !ignore) setHits(h); });
    return () => { ignore = true; };
  }, [query, guard]);
  const label = hits === "loading" ? "..." : hits;     // derived during render, not a second state
  return <p className="out">{label}</p>;
}

function mount(guard) {
  const el = document.createElement("div"); document.body.appendChild(el);
  const root = createRoot(el);
  flushSync(() => root.render(<Search query="a" guard={guard} />));
  setTimeout(() => flushSync(() => root.render(<Search query="ab" guard={guard} />)), 10);
  return el;
}
const good = mount(true), bad = mount(false);
setTimeout(() => { document.body.dataset.r = JSON.stringify({ good: good.textContent, bad: bad.textContent }); }, 1000);
'''


@card(P + "1530-webcraft/4194-react-development")
def react_development(task, wd):
    """Effect fetch that ignores stale results on cleanup (the skill's data rule), run in real React 19."""
    r = _bundle_and_run(wd, "race", REACT_RACE)
    rep = jw(wd / "react_race.json", r)
    return [
        check("with cleanup flag the view shows the latest query's results", r["good"] == "AB-results", r["good"], "AB-results"),
        check("negative control: without it the late response overwrites the current view", r["bad"] == "A-results", r["bad"], "A-results"),
    ], [rep, wd / "race.jsx"]


ASYNC_SRC = r'''
const sleep = (ms, v) => new Promise((r) => setTimeout(() => r(v), ms));
const fetchUser = () => sleep(120, { id: 1 });
const fetchPosts = () => sleep(120, ["p1", "p2"]);
const fetchComments = () => sleep(120, ["c1"]);
async function sequential() {
  const user = await fetchUser();
  const posts = await fetchPosts();
  const comments = await fetchComments();
  return { user, posts, comments };
}
module.exports = { sleep, fetchUser, fetchPosts, fetchComments, sequential };
'''


def _waterfalls(src):
    """Detect runs of consecutive `const x = await f()` where later calls do not use earlier results."""
    lines = [ln.strip() for ln in src.splitlines()]
    runs, cur = [], []
    for ln in lines:
        m = re.match(r"const (\w+) = await (\w+)\((.*)\);", ln)
        if m and not any(re.search(r"\b%s\b" % v, m.group(3)) for v, _ in cur):
            cur.append((m.group(1), m.group(2)))
        else:
            if len(cur) > 1:
                runs.append(cur)
            cur = [(m.group(1), m.group(2))] if m else []
    if len(cur) > 1:
        runs.append(cur)
    return runs


def _parallelize(src):
    for run in _waterfalls(src):
        names = ", ".join(v for v, _ in run)
        calls = ",\n    ".join("%s()" % f for _, f in run)
        first = "const %s = await %s();" % run[0]
        block = "const [%s] = await Promise.all([\n    %s\n  ]);" % (names, calls)
        pat = r"const %s = await %s\(\);" % run[0] + "".join(r"\s*const %s = await %s\(\);" % r for r in run[1:])
        src = re.sub(pat, block, src, count=1)
        assert first not in src
    return src.replace("async function sequential", "async function parallel").replace("sequential }", "parallel }")


@card(P + "1434-react-skills/3417-vercel-react-best-practices")
def vercel_react_best_practices(task, wd):
    """Rule async-parallel (CRITICAL): detect independent sequential awaits, rewrite to Promise.all, measure."""
    seq = wt(wd / "data_seq.js", ASYNC_SRC)
    runs = _waterfalls(ASYNC_SRC)
    par = wt(wd / "data_par.js", _parallelize(ASYNC_SRC))
    bench = wt(wd / "bench.cjs", """
        const s = require(%s), p = require(%s);
        (async () => {
          let t = Date.now(); const a = await s.sequential(); const ts = Date.now() - t;
          t = Date.now(); const b = await p.parallel(); const tp = Date.now() - t;
          console.log(JSON.stringify({ ts, tp, same: JSON.stringify(a) === JSON.stringify(b) }));
        })();
        """ % (json.dumps(str(seq)), json.dumps(str(par))))
    r = json.loads(fx.run(["node", bench]).stdout.strip().splitlines()[-1])
    rule = (SKROOT / "1434-react-skills/3417-vercel-react-best-practices/rules/async-parallel.md").read_text()
    rep = jw(wd / "async_parallel.json", {"rule_impact": re.search(r"impact: (\w+)", rule).group(1), "waterfalls": runs, **r})
    return [
        check("detector finds one 3-call waterfall of independent awaits", len(runs) == 1 and len(runs[0]) == 3, runs),
        check("rewritten code uses Promise.all and has no waterfall left", "Promise.all" in par.read_text() and not _waterfalls(par.read_text()),
              True, True),
        check("same results before and after", r["same"], r["same"], True),
        check("parallel takes about one round trip (< 220 ms for 3 x 120 ms calls)", r["tp"] < 220, r["tp"], "<220"),
        check("negative control: sequential version takes >= 3 round trips (>= 355 ms)", r["ts"] >= 355, r["ts"], ">=355"),
    ], [rep, par]


# ================================================================ vendor operator packs (provider-free cores)
def _flatten(d, pre=""):
    out = {}
    for k, v in d.items():
        if isinstance(v, dict):
            out.update(_flatten(v, pre + k + "."))
        else:
            out[pre + k] = v
    return out


def _unflatten(f):
    out = {}
    for k, v in f.items():
        cur = out
        parts = k.split(".")
        for p in parts[:-1]:
            cur = cur.setdefault(p, {})
        cur[parts[-1]] = v
    return out


@card(P + "1818-abridge-pack/4886-abridge-upgrade-migration")
def abridge_upgrade_migration(task, wd):
    """Reversible migration map between frozen source/target tenant configs: changes classified by impact area,
    forward + rollback applied and proven, in-flight encounters pinned to the source template."""
    source = {"care_setting": {"ed": {"note_template": "ED-v3", "cohort": "pilot"}},
              "ehr": {"handoff": "draft-to-inbox", "template_map": {"ED-v3": "EpicNoteA"}},
              "access": {"reviewers": ["dr_a", "dr_b"]}, "capture": {"consent_prompt": True}}
    target = {"care_setting": {"ed": {"note_template": "ED-v4", "cohort": "all"}},
              "ehr": {"handoff": "draft-to-inbox", "template_map": {"ED-v4": "EpicNoteB"}},
              "access": {"reviewers": ["dr_a", "dr_b", "dr_c"]}, "capture": {"consent_prompt": True}}
    jw(wd / "frozen_source.json", source)
    jw(wd / "frozen_target.json", target)
    fs, ft = _flatten(source), _flatten(target)
    area = lambda k: {"care_setting": "note-template" if "template" in k else "patient-selection", "ehr": "EHR handoff",  # noqa: E731
                      "access": "access", "capture": "capture"}[k.split(".")[0]]
    ops = []
    for k in sorted(set(fs) | set(ft)):
        if fs.get(k, "<absent>") != ft.get(k, "<absent>"):
            ops.append({"key": k, "area": area(k), "before": fs.get(k, "<absent>"), "after": ft.get(k, "<absent>")})

    def apply(state, ops_, direction):
        f = _flatten(state)
        for o in (ops_ if direction == "forward" else list(reversed(ops_))):
            v = o["after"] if direction == "forward" else o["before"]
            if v == "<absent>":
                f.pop(o["key"], None)
            else:
                f[o["key"]] = v
        return _unflatten(f)
    fwd = apply(source, ops, "forward")
    back = apply(fwd, ops, "rollback")
    encounters = [{"id": "e1", "started": "2026-11-03T08:00"}, {"id": "e2", "started": "2026-11-03T10:30"}]
    cutover = "2026-11-03T09:00"
    pins = {e["id"]: (source if e["started"] < cutover else fwd)["care_setting"]["ed"]["note_template"] for e in encounters}
    mm = wt(wd / "migration_map.md", "# Migration map (requires tenant release notes + approved test records before cutover)\n\n" +
            md_table([(o["key"], o["area"], o["before"], o["after"]) for o in ops], ["Setting", "Impact", "Source", "Target"]) +
            "\n\nCutover %s; in-flight encounters keep the source template.\nRollback authority: named owner; no PHI in this file.\n" % cutover)
    forward_only = [{"key": o["key"], "area": o["area"], "before": "<absent>", "after": o["after"]} for o in ops]
    lossy = apply(apply(source, forward_only, "forward"), forward_only, "rollback")
    return [
        check("changes classified by impact area", sorted({o["area"] for o in ops}) == ["EHR handoff", "access", "note-template", "patient-selection"],
              sorted({o["area"] for o in ops})),
        check("forward migration reaches the frozen target exactly", fwd == target, fwd == target, True),
        check("rollback restores the frozen source exactly", back == source, back == source, True),
        check("in-flight encounter pinned to source template, new one on target", pins == {"e1": "ED-v3", "e2": "ED-v4"}, pins),
        check("negative control: a forward-only change list cannot roll back to the source", lossy != source, lossy == source, False),
    ], [mm]


@card(P + "1821-algolia-pack/4955-algolia-reference-architecture")
def algolia_reference_architecture(task, wd):
    """Record contract with stable objectID and deletion semantics; sync planner (upserts + deletes) applied to a
    local index model and proven equal to the source; replay after partial failure is idempotent."""
    v1 = [{"type": "product", "id": 1, "name": "Pen", "price": 2, "secret_cost": 1}, {"type": "product", "id": 2, "name": "Ink", "price": 5, "secret_cost": 2},
          {"type": "article", "id": 1, "name": "How to write", "price": None, "secret_cost": 0}]
    v2 = [{"type": "product", "id": 1, "name": "Pen", "price": 3, "secret_cost": 1}, {"type": "article", "id": 1, "name": "How to write", "price": None, "secret_cost": 0},
          {"type": "product", "id": 3, "name": "Pad", "price": 4, "secret_cost": 2}]
    public = ["name", "price"]

    def record(r):
        return {"objectID": "%s:%d" % (r["type"], r["id"]), **{k: r[k] for k in public}, "type": r["type"]}

    def plan(src, index):
        want = {x["objectID"]: x for x in map(record, src)}
        ups = [want[k] for k in sorted(want) if index.get(k) != want[k]]
        dels = sorted(k for k in index if k not in want)
        return ups, dels

    def apply(index, ups, dels, fail_after=None):
        for i, u in enumerate(ups):
            if fail_after is not None and i == fail_after:
                raise IOError("partial indexing failure")
            index[u["objectID"]] = u
        for d in dels:
            index.pop(d, None)
    index = {}
    apply(index, *plan(v1, index))
    ups, dels = plan(v2, index)
    try:
        apply(index, ups, dels, fail_after=1)
    except IOError:
        pass
    apply(index, *plan(v2, index))
    final_plan = plan(v2, index)
    expected = {x["objectID"]: x for x in map(record, v2)}
    naive = {}
    for r in v1 + v2:
        naive[str(r["id"])] = record(r)
    adr = wt(wd / "architecture.md", "# Search architecture decisions\n- Record contract: objectID = <type>:<id> (stable across types)\n"
             "- Public attributes only: %s (no cost data in the index)\n- Deletion: tombstone by planner diff, not append\n"
             "- Sync plan v1->v2: %d upserts, %d deletes\n- Failure model: partial indexing -> replay full plan (idempotent)\n"
             % (public, len(ups), len(dels)))
    jw(wd / "index_state.json", index)
    return [
        check("v1->v2 plan: 2 upserts (price change, new item) and 1 delete", len(ups) == 2 and dels == ["product:2"], [len(ups), dels]),
        check("after a partial failure and replay the index equals the source projection", index == expected, len(index), len(expected)),
        check("replay is idempotent: nothing left to do", final_plan == ([], []), final_plan, [[], []]),
        check("no private attribute reaches the index", all("secret_cost" not in v for v in index.values()), True, True),
        check("negative control: id-only keys collide across types and append-only keeps the deleted item",
              len(naive) != len(expected) or "2" in naive, sorted(naive), "collision/stale"),
    ], [adr, wd / "index_state.json"]


CLAY_ERRORS = {"No data found": ("provider has no data for this input", "add more waterfall providers"),
               "Rate limit exceeded": ("provider API rate limit hit", "reduce rows, add delay between batches"),
               "Invalid API key": ("provider connection lost or key expired", "reconnect with a valid API key"),
               "Timeout": ("provider took too long", "retry later / smaller batches")}


@card(P + "1836-clay-pack/5262-clay-advanced-troubleshooting")
def clay_advanced_troubleshooting(task, wd):
    """Layer-isolation test (webhook, enterprise API, callback) against local stand-in endpoints: the first failing
    layer is the root-cause location; enrichment cell errors mapped to cause + fix."""
    import http.server
    import threading
    import urllib.request
    import urllib.error

    class H(http.server.BaseHTTPRequestHandler):
        def do_POST(self):
            self.rfile.read(int(self.headers.get("Content-Length", 0)))
            code = 200 if self.path.startswith("/webhook") else 500
            self.send_response(code)
            self.end_headers()
            self.wfile.write(b"{}")

        def log_message(self, *a):
            pass
    srv = http.server.HTTPServer(("127.0.0.1", 0), H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    base = "http://127.0.0.1:%d" % srv.server_port

    def post(url):
        req = urllib.request.Request(url, data=b'{"_debug": true, "domain": "example.com"}', headers={"Content-Type": "application/json"})
        try:
            return urllib.request.urlopen(req, timeout=5).status
        except urllib.error.HTTPError as e:
            return e.code
    layers = [("webhook", post(base + "/webhook")), ("enterprise_api", "skipped: no CLAY_API_KEY"), ("callback", post(base + "/api/clay/enriched"))]
    srv.shutdown()
    first_fail = next((n for n, c in layers if isinstance(c, int) and c >= 400), None)
    cells = ["Rate limit exceeded", "No data found", "Rate limit exceeded", "Timeout"]
    diag = {c: CLAY_ERRORS[c] for c in cells}
    top = max(set(cells), key=cells.count)
    rep = jw(wd / "layer_test.json", {"layers": layers, "first_failing_layer": first_fail, "cell_errors": diag, "dominant": top})
    e2e = "failed" if any(isinstance(c, int) and c >= 400 for _, c in layers) else "ok"
    return [
        check("webhook layer 200, callback layer 500", layers[0][1] == 200 and layers[2][1] == 500, [layers[0][1], layers[2][1]]),
        check("first failing layer = callback (root-cause location)", first_fail == "callback", first_fail, "callback"),
        check("API layer reported as skipped, not passed", str(layers[1][1]).startswith("skipped"), layers[1][1]),
        check("dominant cell error mapped to cause and fix", top == "Rate limit exceeded" and "delay" in diag[top][1], top),
        check("negative control: an end-to-end test only says 'failed' with no layer", e2e == "failed", e2e, "failed"),
    ], [rep]


CLAY_FIELDS = {"company_name": "public", "industry": "public", "domain": "public", "work_email": "business", "job_title": "business",
               "first_name": "business", "phone_number": "personal", "personal_email": "restricted", "home_address": "restricted"}
PERSONAL_DOMAINS = {"gmail.com", "yahoo.com", "hotmail.com", "outlook.com"}


@card(P + "1836-clay-pack/5269-clay-data-handling")
def clay_data_handling(task, wd):
    """Sensitivity classification, pre-enrichment validation, retention purge and DSAR erasure with a PII-free audit log."""
    import datetime as dt
    today = dt.date(2026, 11, 3)
    rows = [
        {"domain": "acme.io", "company_name": "Acme", "work_email": "ana@acme.io", "phone_number": "+1 555 0101",
         "personal_email": "ana@gmail.com", "enriched": "2026-10-01"},
        {"domain": "gmail.com", "company_name": None, "work_email": "x@gmail.com", "enriched": "2026-10-20"},
        {"domain": "beta.dev", "company_name": "Beta", "work_email": "bo@beta.dev", "home_address": "1 Main St",
         "phone_number": "+1 555 0102", "enriched": "2026-05-01"},
        {"domain": "not a domain", "company_name": "Bad", "work_email": "q@bad", "enriched": "2026-10-30"}]
    raw_pii = sum(1 for r in rows for k in r if CLAY_FIELDS.get(k) in ("personal", "restricted"))
    valid, rejected = [], []
    for r in rows:
        d = r["domain"]
        if not re.fullmatch(r"[a-z0-9-]+(\.[a-z0-9-]+)+", d) or d in PERSONAL_DOMAINS:
            rejected.append(d)
        else:
            valid.append(dict(r))
    classes = {}
    for r in valid:
        for k, v in r.items():
            if v is not None and k in CLAY_FIELDS:
                classes.setdefault(CLAY_FIELDS[k], set()).add(k)
    retention = {"personal": 90, "restricted": 30}
    audit = []
    for r in valid:
        age = (today - dt.date.fromisoformat(r["enriched"])).days
        for k in list(r):
            lim = retention.get(CLAY_FIELDS.get(k, ""))
            if lim and age > lim:
                del r[k]
                audit.append({"action": "retention_purge", "field": k, "row": r["domain"], "age_days": age})
    subject = "ana@acme.io"
    before = len(valid)
    valid = [r for r in valid if r.get("work_email") != subject]
    import hashlib
    audit.append({"action": "dsar_erasure", "subject_sha256": hashlib.sha256(subject.encode()).hexdigest()[:16], "rows": before - len(valid)})
    out = jw(wd / "clay_clean.json", valid)
    log = wt(wd / "audit.log", "\n".join(json.dumps(a) for a in audit) + "\n")
    leftover = sum(1 for r in valid for k in r if CLAY_FIELDS.get(k) in ("personal", "restricted"))
    return [
        check("validation rejects personal-email domain and malformed domain", rejected == ["gmail.com", "not a domain"], rejected),
        check("fields classified by sensitivity", classes.get("restricted") == {"personal_email", "home_address"}
              and classes.get("public") == {"domain", "company_name"}, {k: sorted(v) for k, v in classes.items()}),
        check("retention purge: restricted > 30 days (33d personal_email, 186d home_address), personal > 90 days (186d phone)",
              [a["field"] for a in audit if a["action"] == "retention_purge"] == ["personal_email", "home_address", "phone_number"], [a["field"] for a in audit if a["action"] == "retention_purge"]),
        check("DSAR erased the subject's row", audit[-1]["rows"] == 1 and all(r.get("work_email") != subject for r in valid), audit[-1]["rows"], 1),
        check("audit log carries no raw PII", subject not in log.read_text() and "555" not in log.read_text(), True, True),
        check("negative control: the raw table held restricted/personal values; the cleaned table holds none",
              raw_pii == 4 and leftover == 0, [raw_pii, leftover], [4, 0]),
    ], [out, log]


@card(P + "1840-coderabbit-pack/5379-coderabbit-observability")
def coderabbit_observability(task, wd):
    """Review coverage, time-to-first-review and finding resolution from an export, with explicit UTC window,
    exclusions and denominators."""
    import datetime as dt
    import statistics as st
    prs = [  # id, opened UTC, author, draft, first AI review minutes, findings, resolved
        (1, "2026-10-01T09:00Z", "ana", False, 4, 5, 4), (2, "2026-10-02T09:00Z", "bob", False, 6, 2, 2),
        (3, "2026-10-03T09:00Z", "dependabot[bot]", False, None, 0, 0), (4, "2026-10-04T09:00Z", "cy", True, None, 0, 0),
        (5, "2026-10-05T09:00Z", "dee", False, None, 0, 0), (6, "2026-10-06T09:00Z", "eve", False, 10, 3, 1),
        (7, "2026-09-29T09:00Z", "old", False, 2, 1, 1), (8, "2026-10-07T09:00Z", "fay", False, 8, 0, 0)]
    win = (dt.datetime(2026, 10, 1, tzinfo=dt.timezone.utc), dt.datetime(2026, 11, 1, tzinfo=dt.timezone.utc))
    jw(wd / "export.json", prs)

    def ts(s):
        return dt.datetime.fromisoformat(s.replace("Z", "+00:00"))
    in_win = [p for p in prs if win[0] <= ts(p[1]) < win[1]]
    eligible = [p for p in in_win if not p[3] and not p[2].endswith("[bot]")]
    reviewed = [p for p in eligible if p[4] is not None]
    cov = len(reviewed) / len(eligible)
    ttfr = st.median(p[4] for p in reviewed)
    fsum, rsum = sum(p[5] for p in reviewed), sum(p[6] for p in reviewed)
    res = rsum / fsum
    naive_cov = sum(1 for p in prs if p[4] is not None) / len(prs)
    rep = wt(wd / "observability.md", "# Review observability (UTC %s to %s)\n" % (win[0].date(), win[1].date()) +
             md_table([("coverage", "%d/%d" % (len(reviewed), len(eligible)), "%.1f%%" % (100 * cov)),
                       ("median time to first review", "n=%d" % len(reviewed), "%.1f min" % ttfr),
                       ("finding resolution", "%d/%d" % (rsum, fsum), "%.1f%%" % (100 * res))], ["Metric", "Denominator", "Value"]) +
             "\n\nExcluded: 1 out-of-window, 1 draft, 1 bot. No thresholds published without a baseline.\n")
    return [
        check("window + exclusions: 5 eligible PRs, 4 reviewed -> 80% coverage", len(eligible) == 5 and cov == 0.8, [len(reviewed), len(eligible)], [4, 5]),
        check("median time to first review = 7 min", ttfr == 7, ttfr, 7),
        check("finding resolution 7/10", (rsum, fsum) == (7, 10), [rsum, fsum], [7, 10]),
        check("negative control: no window/exclusions gives a different coverage figure (62.5%)", naive_cov == 0.625 and naive_cov != cov,
              naive_cov, 0.625),
    ], [rep]


@card(P + "1841-cohere-pack/5396-cohere-enterprise-rbac")
def cohere_enterprise_rbac(task, wd):
    """Application authorization in front of provider calls: tenant isolation, model/endpoint allow-lists, budgets,
    owner-only key rotation, member removal and service revocation tested."""
    state = {"members": {"olu": ("Owner", "t1"), "uma": ("User", "t1"), "bea": ("User", "t2")},
             "services": {"svc-t1": {"tenant": "t1", "key": "k1", "revoked": False}},
             "keys": {"t1": "k1", "t2": "k2"},
             "policy": {"t1": {"models": {"command-r"}, "endpoints": {"chat", "embed"}, "budget": 100}, "t2": {"models": {"command-r"}, "endpoints": {"chat"}, "budget": 10}},
             "spend": {"t1": 95, "t2": 0}, "audit": []}

    def authorize(principal, tenant, model, endpoint, cost):
        m = state["members"].get(principal)
        s = state["services"].get(principal)
        if m is None and (s is None or s["revoked"]):
            return "deny: unknown or revoked principal"
        ptenant = m[1] if m else s["tenant"]
        if ptenant != tenant:
            return "deny: cross-tenant"
        pol = state["policy"][tenant]
        if model not in pol["models"] or endpoint not in pol["endpoints"]:
            return "deny: model/endpoint not allowed"
        if state["spend"][tenant] + cost > pol["budget"]:
            return "deny: budget"
        state["audit"].append((principal, tenant, endpoint))
        return "allow"

    def rotate(principal, tenant):
        m = state["members"].get(principal)
        if not m or m[0] != "Owner" or m[1] != tenant:
            return "deny"
        state["keys"][tenant] = state["keys"][tenant] + "-r"
        for s in state["services"].values():
            if s["tenant"] == tenant:
                s["key"] = state["keys"][tenant]
        return "rotated"
    r = {"own": authorize("uma", "t1", "command-r", "chat", 1), "cross": authorize("bea", "t1", "command-r", "chat", 1),
         "model": authorize("uma", "t1", "command-a", "chat", 1), "endpoint": authorize("bea", "t2", "command-r", "embed", 1),
         "budget": authorize("uma", "t1", "command-r", "chat", 10), "user_rotate": rotate("uma", "t1"), "owner_rotate": rotate("olu", "t1")}
    old_key_valid = state["keys"]["t1"] == "k1"
    del state["members"]["uma"]
    r["removed"] = authorize("uma", "t1", "command-r", "chat", 1)
    state["services"]["svc-t1"]["revoked"] = True
    r["revoked_svc"] = authorize("svc-t1", "t1", "command-r", "chat", 1)
    provider_only = {"bea": state["members"]["bea"][0] in ("Owner", "User")}
    rep = jw(wd / "rbac_tests.json", {"results": r, "old_key_valid": old_key_valid, "audit": state["audit"]})
    matrix = wt(wd / "rbac_matrix.md", md_table([("Owner", "members, prod keys, billing, rotation", "own tenant only"),
                                                 ("User", "chat/embed per tenant policy", "own tenant only"),
                                                 ("Service identity", "runtime calls, env-specific key", "revocable")],
                                                ["Role", "May", "Scope"]) + "\n")
    return [
        check("own-tenant call allowed and audited", r["own"] == "allow" and len(state["audit"]) == 1, r["own"]),
        check("cross-tenant, disallowed model, disallowed endpoint, over-budget all denied",
              [r[k].split(":")[0] for k in ["cross", "model", "endpoint", "budget"]] == ["deny"] * 4, [r[k] for k in ["cross", "model", "endpoint", "budget"]]),
        check("only the Owner can rotate; old key invalid after rotation", r["user_rotate"] == "deny" and r["owner_rotate"] == "rotated"
              and not old_key_valid, [r["user_rotate"], r["owner_rotate"]]),
        check("removed member and revoked service are denied", r["removed"].startswith("deny") and r["revoked_svc"].startswith("deny"),
              [r["removed"], r["revoked_svc"]]),
        check("negative control: provider role alone would let bea (t2 User) call t1", provider_only["bea"], provider_only["bea"], True),
    ], [rep, matrix]


class _FakeCrawlAPI:
    """Deterministic stand-in for a crawl provider: scripted errors, paged results, duplicate webhooks."""

    def __init__(self, script):
        self.script = list(script)
        self.jobs = {}
        self.submits = 0

    def submit(self, work_id):
        self.submits += 1
        err = self.script.pop(0) if self.script else None
        if err:
            return {"error": err}
        jid = "job-%d" % self.submits
        self.jobs[jid] = [["p1", "p2"], ["p3", "p2"], ["p4"]]
        return {"id": jid}

    def page(self, jid, i):
        pages = self.jobs[jid]
        return {"data": pages[i], "next": i + 1 if i + 1 < len(pages) else None}


def _crawl_client(api, store, crash_after_submit=False, naive=False):
    state = json.loads(store.read_text()) if store.exists() else {"attempts": 0, "job": None, "pages": [], "cursor": 0,
                                                                   "clock": 0.0, "breaker": 0, "webhooks": []}
    retryable = {"429", "500", "502", "503", "timeout"}
    if not state["job"] or naive:
        while True:
            if state["breaker"] >= 3:
                state["status"] = "circuit-open"
                break
            state["attempts"] += 1
            r = api.submit("tenant1:site:v1")
            if "id" in r:
                state["job"] = r["id"]
                state["breaker"] = 0
                break
            if r["error"] not in retryable and not naive:
                state["status"] = "failed: " + r["error"]
                store.write_text(json.dumps(state))
                return state
            state["breaker"] += 1
            state["clock"] += min(8.0, 0.5 * 2 ** (state["attempts"] - 1))  # virtual backoff, no real sleep
            if state["attempts"] >= 5:
                state["status"] = "gave up"
                break
        store.write_text(json.dumps(state))
        if crash_after_submit:
            raise SystemExit("crash after submit")
    if state.get("status") in ("circuit-open", "gave up"):
        return state
    nxt = state["cursor"]
    while nxt is not None:
        p = api.page(state["job"], nxt)
        for u in p["data"]:
            if naive or u not in state["pages"]:
                state["pages"].append(u)
        nxt = p["next"]
        state["cursor"] = nxt if nxt is not None else state["cursor"] + 1
        store.write_text(json.dumps(state))
    for wh in [("wh-1", "completed"), ("wh-1", "completed"), ("wh-2", "page")]:
        if naive or list(wh) not in state["webhooks"]:
            state["webhooks"].append(list(wh))
    state["status"] = "done"
    store.write_text(json.dumps(state))
    return state


@card(P + "1853-firecrawl-pack/5675-firecrawl-reliability-patterns")
def firecrawl_reliability_patterns(task, wd):
    """Durable job state, retry only retryable classes with bounded backoff, circuit breaker, crash-after-submit
    resume, idempotent page acceptance and webhook dedupe, all against a scripted fake provider."""
    api = _FakeCrawlAPI(["429", "503", None])
    store = wd / "state.json"
    try:
        _crawl_client(api, store, crash_after_submit=True)
    except SystemExit:
        pass
    s = _crawl_client(api, store)
    api401 = _FakeCrawlAPI(["401", None])
    s401 = _crawl_client(api401, wd / "state401.json")
    apiout = _FakeCrawlAPI(["503"] * 10)
    sout = _crawl_client(apiout, wd / "state_out.json")
    napi = _FakeCrawlAPI(["429", "401", None])
    nstore = wd / "naive.json"
    try:
        _crawl_client(napi, nstore, crash_after_submit=True, naive=True)
    except SystemExit:
        pass
    ns = _crawl_client(napi, nstore, naive=True)
    rep = jw(wd / "reliability_report.json", {"main": s, "auth": s401, "outage": sout, "naive": ns, "submits": api.submits,
                                               "naive_submits": napi.submits})
    return [
        check("429 and 503 retried with bounded backoff (0.5 + 1.0 s virtual), job submitted once on success",
              s["attempts"] == 3 and s["clock"] == 1.5 and api.submits == 3, [s["attempts"], s["clock"], api.submits]),
        check("crash after submit: resume reuses the persisted job id (no resubmission)", s["job"] == "job-3" and api.submits == 3, s["job"]),
        check("pages accepted idempotently across pagination (p2 duplicated by provider)", s["pages"] == ["p1", "p2", "p3", "p4"], s["pages"]),
        check("duplicate webhook delivery deduplicated", s["webhooks"] == [["wh-1", "completed"], ["wh-2", "page"]], s["webhooks"]),
        check("401 is not retried", s401["status"] == "failed: 401" and api401.submits == 1, [s401["status"], api401.submits]),
        check("outage opens the circuit after 3 failures", sout["status"] == "circuit-open" and apiout.submits == 3, [sout["status"], apiout.submits]),
        check("negative control: naive client resubmits after the crash and double-accepts pages/webhooks",
              napi.submits > 3 and len(ns["pages"]) > 4 and len(ns["webhooks"]) > 2, [napi.submits, len(ns["pages"]), len(ns["webhooks"])]),
    ], [rep]


@card(P + "1854-fireflies-pack/5694-fireflies-multi-env-setup")
def fireflies_multi_env_setup(task, wd):
    """Startup validator for per-environment isolation: distinct bearer + signing secrets (compared by hash),
    env-specific HTTPS webhooks, no production fallback, synthetic-only dev data, redacted logging."""
    import hashlib
    secrets = {"dev": ("ff_dev_aaa", "sig_dev"), "staging": ("ff_stg_bbb", "sig_stg"), "prod": ("ff_prd_ccc", "sig_prd")}
    good = {e: {"api_key_ref": "vault://fireflies/%s/api" % e, "signing_ref": "vault://fireflies/%s/sig" % e,
                "webhook": "https://hooks.%s.example.com/fireflies" % e, "data": "synthetic" if e == "dev" else "reviewed" if e == "staging" else "live",
                "fallback": None, "metrics_tags": ["env", "operation"]} for e in secrets}
    bad = json.loads(json.dumps(good))
    bad["staging"]["api_key_ref"] = "vault://fireflies/prod/api"
    bad["dev"]["webhook"] = "http://hooks.prod.example.com/fireflies"
    bad["dev"]["fallback"] = "prod"
    bad["dev"]["data"] = "live"
    bad["staging"]["metrics_tags"] = ["env", "meeting_title"]
    resolved = {e: secrets[e] for e in secrets}
    resolved_bad = dict(resolved, staging=secrets["prod"])

    def validate(cfg, res):
        issues, log = [], []
        hashes = {e: hashlib.sha256(res[e][0].encode()).hexdigest() for e in cfg}
        if len(set(hashes.values())) != len(hashes):
            issues.append("shared bearer secret across environments")
        for e, c in cfg.items():
            if "/%s/" % e not in c["api_key_ref"] or "/%s/" % e not in c["signing_ref"]:
                issues.append("%s: secret reference points at another environment" % e)
            if not c["webhook"].startswith("https://") or ".%s." % e not in c["webhook"]:
                issues.append("%s: webhook not env-specific HTTPS" % e)
            if c["fallback"]:
                issues.append("%s: fallback to %s" % (e, c["fallback"]))
            if e == "dev" and c["data"] != "synthetic":
                issues.append("dev: non-synthetic data")
            if set(c["metrics_tags"]) - {"env", "operation"}:
                issues.append("%s: content-bearing metric tag" % e)
            log.append("%s key=%s…(%d chars)" % (e, hashes[e][:8], len(res[e][0])))
        return issues, log
    gi, glog = validate(good, resolved)
    bi, _ = validate(bad, resolved_bad)
    naive_ok = all(c["api_key_ref"] for c in bad.values())
    rep = jw(wd / "env_validation.json", {"good": gi, "bad": bi, "startup_log": glog})
    return [
        check("isolated config passes startup validation", gi == [], gi, []),
        check("startup log shows hashes only, never a secret", all(v[0] not in " ".join(glog) for v in secrets.values()), glog),
        check("leaky config: shared secret, cross-env ref, http/prod webhook, prod fallback, live dev data, content tag all caught",
              len(bi) == 6, bi),
        check("negative control: 'every environment has a key' passes the leaky config", naive_ok, naive_ok, True),
    ], [rep]
