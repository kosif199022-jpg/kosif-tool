const $ = (id) => document.getElementById(id);
const store = chrome.storage.local;
let tab = null;
let handle = "";
const RESERVED = new Set(["p", "reel", "reels", "tv", "explore", "stories", "accounts", "direct", "about", "developer", "legal"]);

function profileOf(url) {
  try {
    const u = new URL(url);
    if (u.hostname !== "www.instagram.com") return "";
    const first = (u.pathname.split("/").filter(Boolean)[0] || "").toLowerCase();
    return first && !RESERVED.has(first) && /^[a-z0-9._]{1,30}$/.test(first) ? first : "";
  } catch { return ""; }
}

function fileName() {
  const day = new Date().toISOString().slice(0, 10);
  return `instagram-${handle || "links"}-${day}.txt`;
}

async function render() {
  const { run } = await store.get("run");
  const mine = run && run.handle === handle;
  const links = mine ? run.links : [];
  $("count").textContent = links.length;
  $("copy").disabled = $("txt").disabled = !links.length;
  const running = mine && run.state === "running";
  $("start").disabled = running || !handle;
  $("stop").disabled = !running;
  $("msg").textContent = !mine ? "" : {
    running: "بيجمع... سيب التبويب مفتوح (ممكن تقفل النافذة دي).",
    done: "خلص: وصل لآخر الحساب.",
    stopped: "وقفته.",
    limit: "وصل للحد الأقصى اللي اخترته.",
  }[run.state] || "";
  $("cmd").textContent = `python3 scripts/instagram_finder.py get --urls ${fileName()}`;
  return links;
}

async function init() {
  [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  handle = profileOf(tab && tab.url);
  $("where").textContent = handle ? `الحساب: @${handle}` : "افتح صفحة أي حساب على إنستجرام الأول.";
  $("reels").disabled = !handle || /\/reels\/?$/.test(new URL(tab.url).pathname);
  const { opts = {} } = await store.get("opts");
  if (opts.max) $("max").value = opts.max;
  if (opts.videosOnly === false) $("videosOnly").checked = false;
  render();
}

$("reels").onclick = async () => {
  await chrome.tabs.update(tab.id, { url: `https://www.instagram.com/${handle}/reels/` });
  window.close();
};

$("start").onclick = async () => {
  await store.set({ opts: { max: Number($("max").value) || 1000, videosOnly: $("videosOnly").checked }, stop: false,
                    run: { handle, state: "running", links: [], at: Date.now() } });
  await chrome.scripting.executeScript({ target: { tabId: tab.id }, files: ["collector.js"] });
  render();
};

$("stop").onclick = () => store.set({ stop: true });

$("copy").onclick = async () => {
  const links = await render();
  await navigator.clipboard.writeText(links.join("\n") + "\n");
  $("msg").textContent = `اتنسخ ${links.length} رابط.`;
};

$("txt").onclick = async () => {
  const links = await render();
  const head = `# @${handle} — ${links.length} links — ${new Date().toISOString()}\n`;
  const url = URL.createObjectURL(new Blob([head + links.join("\n") + "\n"], { type: "text/plain" }));
  const a = Object.assign(document.createElement("a"), { href: url, download: fileName() });
  a.click();
  setTimeout(() => URL.revokeObjectURL(url), 2000);
};

chrome.storage.onChanged.addListener((c) => { if (c.run) render(); });
init();
