# rea-static-runs — تشغيل REA فعليًا على هذه الآلة (v6.7.0)

<div dir="rtl">

## بالعربية

**ماذا يثبت:** أداة [morluto/rea](https://github.com/morluto/rea) (MIT) ثُبّتت من npm في مجلد مؤقت خارج المستودع وشُغّلت فعلًا على أهداف محلية مملوكة أو عامة: امتداد كروم أرسله المالك، وثنائيات Go وRust من النظام، وأرشيف ZIP، وبايت كود EVM، وصفحة `web/` من هذا المستودع مقدَّمة عبر Chromium بلا رأس على منفذ CDP محلي. كل أمر أعاد سجل أدلة JSON بمعرّف `evidence_id` وبصمة SHA-256 للهدف وقائمة حدود صريحة. 19 أمرًا نجح، و11 أوامر رفضت العمل بصدق لغياب محرك خارجي (Hopper/Ghidra/IDA/WABT/tshark/Binwalk/Wakaru/Node 24) أو لعدم مطابقة الهدف.

**ما لا يثبته:** لا يثبت استنساخ وظيفة أي برنامج، ولا تحليل ثنائيات أصلية بالتفكيك (يحتاج محرّكًا خارجيًا)، ولا أي فحص لموقع أو تطبيق لا يملك المستخدم حق فحصه.

**إعادة التشغيل:**

```bash
mkdir -p /tmp/rea && cd /tmp/rea && npm install rea-agents@6.7.0 --no-audit --no-fund
R=/tmp/rea/node_modules/.bin/rea
$R doctor --json
$R analyze-javascript-application /abs/path/to/extracted-app --json > js-app.json
$R inspect-go-binary /usr/local/bin/gh --json
# browser route: chromium --headless=new --remote-debugging-port=9333 http://127.0.0.1:8765/index.html
$R list-browser-targets http://127.0.0.1:9333 --json
```

الملف `runs.json` يحمل معرّفات الأدلة وبصمات المخرجات؛ المخرجات نفسها (تحوي مسارات محلية) لم تُلتزم.

</div>

## English

**What it proves:** REA v6.7.0 (MIT) was installed from npm into a scratch folder outside the repo and actually run against local targets we own or that are public: an owner-uploaded Chrome extension, the system's Go (`gh`) and Rust (`rg`) binaries, a ZIP archive, an EVM bytecode file, and this repository's `web/` page served to headless Chromium on a loopback CDP port. Every command returned an Evidence JSON record with an `evidence_id`, the target's SHA-256 and explicit limitations. 19 commands succeeded; 11 refused honestly because an external engine is absent or the target did not match.

| command | target | provider | result |
|---|---|---|---|
| `doctor` | — | `None` | exit 1 = not healthy, reported honestly: node 22.22 / ubuntu 24.04; Hopper, Ghidra, IDA, jadx, Kuna absent → classified missing_analysis_engine |
| `capabilities` | — | `None` | 4 providers advertised with effects: native-macos, rea-artifact-graph, rea-dotnet-static, sqlite |
| `providers` | — | `None` | configured providers listed with side-effect groups |
| `analyze-javascript-application` | extracted Chrome MV3 extension (owner upload, 14 files) | `rea-javascript-application` | JavaScriptApplicationGraph: 14 nodes (4 endpoints, 4 artifacts, 2 modules, 2 renderers, 2 assets), 17 edges, semantic graph with 396 unknowns retained |
| `inspect-analysis-view` | inline evidence from the run above | `rea-analysis-view` | javascript-facts rows for manifest.json/background.js with available_property_keys; coverage exhausted 1/1 |
| `trace-application-feature` | inline evidence, seed string 'download' | `rea-javascript-application-workflows` | feature trace through the authenticated graph |
| `inspect-go-binary` | /usr/local/bin/gh | `go-build-info` | go1.26.1, module github.com/cli/cli/v2 v2.89.0 with dependency list, limitations stated |
| `inspect-rust-binary` | /usr/bin/rg | `rust-auditable` | ELF amd64; no cargo-auditable section → auditable_metadata null (honest absence) |
| `inspect-artifact` | video-downloader.zip (owner upload) | `rea-artifact-graph` | safe artifact graph: observations, hypotheses, next_probes, coverage |
| `extract-artifact` | video-downloader.zip | `rea-artifact-graph` | safe extraction with per-file digests into an absent directory |
| `inspect-electron-fuses` | /usr/bin/rg (non-Electron ELF) | `electron-fuses` | fuse slices absent → runtime_implications empty, no false claim |
| `inspect-evm-interface` | 346-byte hex bytecode file | `evmole-interface` | evmole@0.9.3 interface candidates, discovery_completeness reported |
| `inspect-with-objdump` | /usr/bin/rg file_headers | `gnu.objdump` | GNU objdump raw output retained as Evidence |
| `list-objdump-architectures` | — | `gnu.objdump` | BFD targets of the installed objdump |
| `list-browser-targets` | headless Chromium 141 on 127.0.0.1:9333 | `rea-cdp-browser` | page target listed; file:// target excluded as unsupported_url |
| `inspect-web-page` | http://127.0.0.1:8765/index.html (repo web/ served locally) | `rea-cdp-browser` | frames, dom, accessibility, scripts, resources, network, console, workers |
| `analyze-web-bundle` | same page | `rea-cdp-browser` | capture + static bundle analysis; completeness complete |
| `capture-web-screenshot` | same page | `rea-cdp-browser` | self-verifying PNG artifact JSON |
| `inspect-web-event-listeners` | same page, selector body | `rea-cdp-browser` | native listener source locations |

**Refused or unavailable here (correct, fail-closed behaviour):**

| command | reason |
|---|---|
| `inspect-binary-layout` | needs REA_PWNTOOLS_PYTHON (pwntools 4.15 + pyelftools + Unicorn) |
| `inspect-sqlite-database` | needs Node 24.15+ DatabaseSync.limits (this box runs Node 22) |
| `inspect-wasm-artifact` | needs REA_WABT_BIN_DIRECTORY (WABT 1.0.42) |
| `recover-javascript-sources` | needs REA_WAKARU_COMMAND (Wakaru 1.13+) |
| `inspect-pcap-client` | needs tshark/capinfos (Wireshark 4.x) |
| `inspect-firmware-regions` | needs REA_BINWALK_COMMAND |
| `demangle-swift` | macOS toolchain only |
| `inspect-plist` | macOS toolchain only |
| `inspect-managed-artifact` | target was an ELF, not PE/CLI → capability_unavailable (correct refusal) |
| `compare-application-versions` | input shape needs two complete Evidence records in left/right; not retried |
| `export-web-scripts` | needs a saved page/scenario capture JSON, not a bundle analysis record |

**What it does not prove:** no functional cloning of any program, no native disassembly (needs a bring-your-own engine), and nothing about targets the user has no right to inspect. Raw outputs contain local paths and were not committed; `runs.json` keeps the evidence ids and output digests.
