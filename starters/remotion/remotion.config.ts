// Remotion CLI configuration for the KOSIF starter.
// Reference: https://www.remotion.dev/docs/config
import { existsSync, readdirSync } from "node:fs";
import { join } from "node:path";
import { Config } from "@remotion/cli/config";

Config.setEntryPoint("src/index.ts");
Config.setVideoImageFormat("jpeg");
Config.setOverwriteOutput(true);

/**
 * Reuse a Chromium that already exists on this machine instead of letting
 * Remotion download a headless shell. Resolution order:
 *   1. KOSIF_BROWSER=/path/to/chrome   (environment variable)
 *   2. any Playwright Chromium under $PLAYWRIGHT_BROWSERS_PATH or /opt/pw-browsers
 * The CLI flag --browser-executable=/path still wins over everything here.
 */
const playwrightRoot = process.env.PLAYWRIGHT_BROWSERS_PATH ?? "/opt/pw-browsers";

// Remotion drives Chrome with the classic headless flags, which full Chromium
// builds no longer accept; Playwright's "chromium_headless_shell" build is the
// standalone implementation of that mode, so it is preferred over "chromium".
const playwrightChromiums = (): string[] => {
  try {
    const names = readdirSync(playwrightRoot).sort().reverse();
    const shells = names
      .filter((name) => /^chromium_headless_shell-\d+$/.test(name))
      .map((name) => join(playwrightRoot, name, "chrome-linux", "headless_shell"));
    const full = names
      .filter((name) => /^chromium-\d+$/.test(name))
      .map((name) => join(playwrightRoot, name, "chrome-linux", "chrome"));
    return [...shells, ...full];
  } catch {
    return [];
  }
};

const candidates = [process.env.KOSIF_BROWSER, ...playwrightChromiums()].filter(
  (p): p is string => typeof p === "string" && p.length > 0,
);

const browser = candidates.find((p) => existsSync(p));
if (browser) {
  Config.setBrowserExecutable(browser);
}
