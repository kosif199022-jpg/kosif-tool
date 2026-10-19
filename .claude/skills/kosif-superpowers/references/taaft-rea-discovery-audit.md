# There's An AI For That: bounded REA algorithm investigation (2026-10-20)

Target: https://theresanaiforthat.com/ — external, proprietary service.

## Direct evidence

- The user's visible Google Chrome window was observed via Windows accessibility tree. Its page showed Home, Search, Deals, Leaderboard, Tasks, Mini tools, Characters, Map, Prompts, Generate images, Generate videos, search field and pricing controls.
- A new isolated Chrome 155 CDP research session at 127.0.0.1:9234 was opened to the same public origin. REA 6.7.0 list-browser-targets succeeded (evidence ev_91b690bb4f2711b92b3a6e011e53eccd5d3751f0ba075d80629133da09c98023), but the target page title was "لحظة…" (security check).
- Direct HTTP headers produced Cloudflare HTTP 403. No attempt was made to evade site protections or capture user credentials.
- A bounded REA analyze-web-bundle attempt against the isolated browser did not produce a successful site-code artifact and was terminated; therefore the protected source bundle is unobserved.
- Ghidra cannot recover server-side search or recommendation algorithms from a browser DOM. No site-specific native binary or WebAssembly artifact suitable for Ghidra was exposed; Chrome executable analysis would reveal Chrome internals, NOT website ranking code.
- Backend search weights, personalization, database queries and recommendation implementation are unknown.

## Original independent KOSIF improvement

KOSIF already has its OWN 4,730-record capability catalog. The separate original local discovery script:
  python scripts/ai_tool_discovery.py --doctor
  python scripts/ai_tool_discovery.py "تحريك شخصيات فيديو" --top 8

The algorithm uses Arabic/English Unicode normalization, small bilingual aliases, corpus-relative term rarity, weighted names/tags/task contexts/summary matching, deterministic sorting and bounded output. Every suggestion includes existing KOSIF capability IDs, claimed status, proof scope and prerequisites, and explicitly states runtime_verified=false. It never accesses website cookies, makes external requests, executes catalog entries, or clones an outside service.

Verification: python -m unittest discover -s evals -p test_ai_tool_discovery.py -v

This is NOT a reconstruction of There's An AI For That's actual ranking algorithm. Its backend implementation, proprietary weights and data remain unobserved.
