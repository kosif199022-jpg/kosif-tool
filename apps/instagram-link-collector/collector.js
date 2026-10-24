// Runs inside the Instagram tab (injected by popup.js). It scrolls the profile grid,
// keeps every post/reel link it sees (Instagram unloads rows while you scroll, so links
// are kept as they appear), and writes progress to chrome.storage.local under "run".
// Nothing leaves your browser: no requests are made besides Instagram's own page loading.
(async () => {
  if (window.__kosifCollecting) return;
  window.__kosifCollecting = true;
  const store = chrome.storage.local;
  const { opts = {} } = await store.get("opts");
  const max = Math.min(Number(opts.max) || 1000, 5000);
  const videosOnly = opts.videosOnly !== false;
  const idle = Math.max(Number(opts.idleRounds) || 5, 2);  // rounds with no new link before stopping
  const wait = (ms) => new Promise((r) => setTimeout(r, ms));
  const handle = (location.pathname.split("/").filter(Boolean)[0] || "").toLowerCase();
  const onReelsTab = /\/reels\/?$/.test(location.pathname);
  const found = new Map();  // shortcode -> {url, video}

  function harvest() {
    for (const a of document.querySelectorAll('a[href*="/reel/"], a[href*="/p/"], a[href*="/tv/"]')) {
      const m = a.getAttribute("href").match(/\/(reels?|p|tv)\/([A-Za-z0-9_-]{5,})/);
      if (!m || found.has(m[2])) continue;
      // A video tile is a /reel/ link, anything on the Reels tab, or a tile with the reel/clip icon.
      const icon = a.querySelector('svg[aria-label*="Reel" i], svg[aria-label*="Clip" i], svg[aria-label*="Video" i]');
      const video = m[1].startsWith("reel") || m[1] === "tv" || onReelsTab || !!icon;
      const kind = video ? "reel" : "p";
      found.set(m[2], { url: `https://www.instagram.com/${kind}/${m[2]}/`, video });
    }
  }
  const links = () => [...found.values()].filter((x) => !videosOnly || x.video).map((x) => x.url);
  const save = (state) => store.set({ run: { handle, page: location.href, state, links: links(),
                                              seen: found.size, videosOnly, at: Date.now() } });

  await store.set({ stop: false });
  let quiet = 0;
  harvest();
  await save("running");
  while (quiet < idle && links().length < max) {
    const before = found.size;
    window.scrollTo(0, document.documentElement.scrollHeight);
    await wait(1500 + Math.random() * 1000);  // human pace; keeps Instagram from throttling you
    harvest();
    quiet = found.size > before ? 0 : quiet + 1;
    await save("running");
    if ((await store.get("stop")).stop) break;
  }
  const { stop } = await store.get("stop");
  await save(stop ? "stopped" : links().length >= max ? "limit" : "done");
  window.__kosifCollecting = false;
})();
