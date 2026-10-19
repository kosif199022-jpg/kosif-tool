# KOSIF Superpowers — Local Remote Commander (MCP)

**State:** executable local-first capability (11 tools). This is not a remote-cloud desktop controller or a copy of a proprietary relay service.

## Run / verify

From this skill directory:

~~~powershell
python scripts/kosif_remote_superpowers.py doctor
python scripts/kosif_remote_superpowers.py demo
python -m unittest discover -s scripts -p test_kosif_remote_superpowers.py -v
~~~

The demo command creates a **temporary** directory, confirms writes are denied by default, enables writes only within that temporary directory, writes a sample, searches it, reads it, and exits. It restores prior environment variables. The demo does **not** connect to, or modify, the user's laptop.

## Connect from a local MCP client

Use stdio transport, program python, arguments: scripts/kosif_remote_superpowers.py serve; working directory: the skill root; environment variable KOSIF_REMOTE_ROOT: the specifically allowed workspace.

Available tools: health, system_info, list_directory, file_info, read_file, search_text, create_directory, write_file, replace_block, move_file, run_command.

- Read-only is the default.
- To permit workspace file writes: explicitly set KOSIF_ALLOW_WRITES=1 in the local MCP launch configuration.
- To permit **only allowlisted, read-only commands**: explicitly set KOSIF_ALLOW_EXEC=1. Arbitrary shell commands are not available.
- All file operations are scoped to the configured workspace; paths resolving outside it are rejected. Files exceeding 512 KB are not read/written. Search and lists have bounded results.
- This is a developer prototype; do not expose it to an untrusted network and do not run it with elevated privileges.

## REA and Ghidra evidence

The independently implemented skill was informed by a static **REA** examination of three files from the installed local open-source Desktop Commander JS code (file handlers and process handlers). The other 264 inventoried files were not analyzed. REA's 3-file focused run succeeded; the initial whole-application run timed out. Ghidra archives were detected on Windows, but **Ghidra did not run** because JDK21 and the extracted headless installation were not ready.

- Prototype on the laptop was separately tested (6/6 local tests) in an existing unpushed branch.
- The self-contained skill runtime in this branch was tested in an isolated execution environment (7/7 functional tests; MCP handshake; demo printed PASS).
- These two results are separate and **do not prove live cross-device remote connectivity**.
- Source references: [DesktopCommanderMCP (MIT)](https://github.com/wonderwhy-er/DesktopCommanderMCP), [REA](https://github.com/morluto/rea), [Ghidra](https://github.com/NationalSecurityAgency/ghidra).

## Future features (NOT included)

Authenticated remote relay, device pairing and revocation, secure transport, session process streaming, computer UI/desktop control, user-visible per-action approvals, long-lived remote sessions, cloud browser, native screen/camera capture, and production security review. Avoid claims of feature parity.

## Safety acceptance

Seven tests cover default write denial, command denial, permitted text modifications in temporary directories, path traversal rejection, directory and search operations, MCP stdio request handling, and a CLI demo. No network listener or persistence service is created.
