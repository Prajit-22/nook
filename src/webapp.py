"""Nook web app (PWA): session auth via one-time code the bot DMs you,
plus the app shell, manifest and service worker. Same editorial grid style
as the landing page. All state stays in D1, keyed by chat_id."""

import base64
import hashlib
import hmac
import time

SESSION_COOKIE = "nook_session"
SESSION_TTL = 60 * 60 * 24 * 30  # 30 days


def sign_session(chat_id: int, secret: str) -> str:
    exp = int(time.time()) + SESSION_TTL
    payload = f"{chat_id}.{exp}"
    sig = hmac.new(secret.encode(), payload.encode(), hashlib.sha256).hexdigest()[:32]
    return base64.urlsafe_b64encode(f"{payload}.{sig}".encode()).decode()


def verify_session(cookie_value: str, secret: str):
    """Return chat_id for a valid, unexpired session cookie, else None."""
    try:
        raw = base64.urlsafe_b64decode(cookie_value.encode()).decode()
        chat_id_s, exp_s, sig = raw.rsplit(".", 2)
        payload = f"{chat_id_s}.{exp_s}"
        want = hmac.new(secret.encode(), payload.encode(), hashlib.sha256).hexdigest()[:32]
        if not hmac.compare_digest(sig, want):
            return None
        if int(exp_s) < int(time.time()):
            return None
        return int(chat_id_s)
    except Exception:
        return None


def session_from_headers(cookie_header: str, secret: str):
    if not cookie_header:
        return None
    for part in cookie_header.split(";"):
        part = part.strip()
        if part.startswith(SESSION_COOKIE + "="):
            return verify_session(part.split("=", 1)[1], secret)
    return None


MANIFEST = {
    "name": "Nook - your reading nook",
    "short_name": "Nook",
    "description": "Toss links in all day. Wake up to one sealed letter.",
    "start_url": "/app",
    "scope": "/",
    "display": "standalone",
    "background_color": "#F8F5EE",
    "theme_color": "#F8F5EE",
    "icons": [
        {"src": "/brand/avatar.png", "sizes": "640x640", "type": "image/png", "purpose": "any"},
        {"src": "/brand/avatar.png", "sizes": "640x640", "type": "image/png", "purpose": "maskable"},
    ],
    "share_target": {
        "action": "/share",
        "method": "GET",
        "params": {"title": "title", "text": "text", "url": "url"},
    },
}

SERVICE_WORKER = """const CACHE = 'nook-v2';
self.addEventListener('install', (e) => { self.skipWaiting(); });
self.addEventListener('activate', (e) => { e.waitUntil(clients.claim()); });
self.addEventListener('fetch', (e) => {
  const url = new URL(e.request.url);
  if (e.request.method !== 'GET') return;
  if (url.pathname.startsWith('/api/')) return; // always live
  if (url.pathname.startsWith('/brand/')) {
    e.respondWith(
      caches.match(e.request).then((hit) => hit || fetch(e.request).then((r) => {
        const copy = r.clone();
        caches.open(CACHE).then((c) => c.put(e.request, copy));
        return r;
      }))
    );
  }
});
"""

_HEAD = """<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<link rel="icon" type="image/png" href="/brand/seal.png">
<link rel="manifest" href="/app/manifest.webmanifest">
<meta name="theme-color" content="#F8F5EE">
<meta name="apple-mobile-web-app-capable" content="yes">
<link rel="apple-touch-icon" href="/brand/avatar.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Oswald:wght@400;500;600&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400;1,6..72,500&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">"""

_CSS = """
:root { --paper:#F8F5EE; --card:#FFFDF6; --ink:#17130C; --ink-soft:rgba(23,19,12,.7); --ink-faint:rgba(23,19,12,.42); --wax:#C2491D;
  --rule:rgba(23,19,12,.16); --rule-soft:rgba(23,19,12,.09); --ease:cubic-bezier(.22,1,.36,1); }
* { margin:0; padding:0; box-sizing:border-box; }
body { background:var(--paper); color:var(--ink); font-family:'Newsreader',Georgia,serif; -webkit-font-smoothing:antialiased; }
.mono { font-family:'IBM Plex Mono',monospace; }
.wrap { max-width:920px; margin:0 auto; padding:0 20px 90px; }
header { display:flex; align-items:center; justify-content:space-between; padding:18px 0 16px; border-bottom:1px solid var(--rule);
  position:sticky; top:0; background:rgba(246,241,229,.92); backdrop-filter:blur(6px); z-index:5; }
.brand { display:flex; align-items:center; gap:10px; }
.brand img { width:34px; height:34px; }
.brand .word { font-family:'Oswald',sans-serif; font-weight:600; font-size:20px; letter-spacing:.12em; text-transform:uppercase; }
.btn { font-family:'IBM Plex Mono',monospace; font-size:12px; letter-spacing:.08em; text-transform:uppercase; text-decoration:none; padding:12px 20px;
  border:1px solid var(--ink); color:var(--ink); background:none; cursor:pointer; transition:all .25s var(--ease); }
.btn.primary { background:var(--ink); color:var(--paper); }
.btn.primary:hover { background:var(--wax); border-color:var(--wax); color:var(--paper); }
nav.tabs { display:flex; gap:4px; margin:22px 0 26px; border-bottom:1px solid var(--rule); }
nav.tabs button { font-family:'IBM Plex Mono',monospace; font-size:13px; background:none; border:none; color:var(--ink-soft);
  padding:10px 14px; cursor:pointer; border-bottom:2px solid transparent; margin-bottom:-1px; }
nav.tabs button.on { color:var(--ink); border-bottom-color:var(--wax); }
.grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(240px,1fr)); gap:22px; }
.clip { position:relative; background:var(--card); border:1px solid var(--rule); padding:20px 18px 16px;
  box-shadow:6px 6px 0 rgba(23,19,12,.05);
  animation:clipin .5s var(--ease) both; }
.clip::before { content:""; position:absolute; top:-1px; left:-1px; width:26px; height:5px; background:var(--wax); }
@keyframes clipin { from { opacity:0; transform:translateY(14px) rotate(-1deg); } }
.clip .id { font-family:'IBM Plex Mono',monospace; font-size:11px; color:var(--wax); letter-spacing:.12em; }
.clip h3 { font-family:'Newsreader',serif; font-weight:600; font-size:17.5px; margin:8px 0 6px; line-height:1.25; }
.clip h3 a { color:var(--ink); text-decoration:none; border-bottom:1px solid transparent; }
.clip h3 a:hover { border-bottom-color:var(--wax); }
.clip p { font-size:13.5px; color:var(--ink-soft); line-height:1.55; }
.clip .tags { display:flex; flex-wrap:wrap; gap:6px; margin-top:10px; font-family:'IBM Plex Mono',monospace; font-size:10.5px; color:var(--ink-faint); }
.clip .tags span { border:1px solid var(--rule-soft); padding:2px 8px; }
.bar { display:flex; gap:10px; margin-bottom:24px; }
.bar input { flex:1; font-family:'IBM Plex Mono',monospace; font-size:14px; padding:12px 16px; border:1px solid var(--rule);
  background:var(--card); color:var(--ink); outline:none; }
.bar input:focus { border-color:var(--ink); }
.empty { text-align:center; padding:70px 20px; color:var(--ink-soft); font-style:italic; font-family:'Newsreader',serif; font-size:19px; }
.note { font-family:'IBM Plex Mono',monospace; font-size:12px; color:var(--ink-faint); text-align:center; margin-top:10px; }
.answer { background:var(--card); border:1px solid var(--rule); padding:22px 20px; margin-bottom:24px; font-size:15.5px; line-height:1.65; }
.answer .q { font-family:'IBM Plex Mono',monospace; font-size:11.5px; letter-spacing:.12em; text-transform:uppercase; color:var(--wax); margin-bottom:10px; }
.letter { position:relative; background:var(--card); border:1px solid var(--rule); padding:34px 28px 28px; max-width:560px; margin:0 auto;
  box-shadow:8px 8px 0 rgba(23,19,12,.05); }
.letter .lh { display:flex; justify-content:space-between; gap:12px; flex-wrap:wrap; border-bottom:1px solid var(--rule); padding-bottom:10px;
  font-family:'IBM Plex Mono',monospace; font-size:11px; letter-spacing:.14em; text-transform:uppercase; color:var(--ink-soft); }
.letter .sec-h { font-family:'IBM Plex Mono',monospace; font-size:11px; letter-spacing:.14em; text-transform:uppercase; color:var(--wax); margin-top:20px; }
.letter .item { margin-top:10px; font-size:14.5px; line-height:1.55; }
.letter .item small { display:block; color:var(--ink-soft); }
.letter .item .u { font-family:'IBM Plex Mono',monospace; font-size:11px; color:var(--ink-faint); }
.job { background:var(--card); border:1px solid var(--rule); padding:18px 18px 14px; margin-bottom:16px; }
.job b { font-family:'Newsreader',serif; font-weight:600; font-size:17px; }
.job a { color:var(--ink); }
.job .meta { font-family:'IBM Plex Mono',monospace; font-size:11.5px; color:var(--ink-soft); margin-top:6px; }
.spinner { text-align:center; padding:50px; font-family:'IBM Plex Mono',monospace; font-size:13px; color:var(--ink-faint); }
.askwrap { max-width:640px; margin:0 auto; }
.askintro { font-size:15px; color:var(--ink-soft); line-height:1.6; margin-bottom:18px; }
.chips { display:flex; flex-wrap:wrap; gap:8px; margin-bottom:22px; }
.chip { font-family:'IBM Plex Mono',monospace; font-size:11.5px; color:var(--ink-soft); border:1px solid var(--rule); background:none; padding:7px 12px; cursor:pointer; transition:all .25s var(--ease); }
.chip:hover { border-color:var(--wax); color:var(--wax); }
.feednote { font-family:'IBM Plex Mono',monospace; font-size:11px; color:var(--ink-faint); letter-spacing:.04em; margin:2px 0 18px; }
.srcs { font-family:'IBM Plex Mono',monospace; font-size:11px; color:var(--ink-faint); margin-top:14px; }
.srcs a { color:var(--ink-soft); }
@media (max-width:640px){ .grid { grid-template-columns:1fr; } }
"""

LOGIN_HTML = """<!doctype html>
<html lang="en"><head>__HEAD__
<title>Sign in - Nook</title>
<style>__CSS__
.login { max-width:420px; margin:12vh auto 0; text-align:center; }
.login img { width:88px; }
.login h1 { font-family:'Oswald',sans-serif; font-weight:500; text-transform:uppercase; font-size:36px; letter-spacing:.01em; margin:18px 0 10px; }
.login p { color:var(--ink-soft); font-size:15.5px; line-height:1.65; }
.login .bar { margin-top:28px; }
.login input { text-align:center; letter-spacing:.3em; text-transform:uppercase; }
.login .err { color:#A4452B; font-family:'IBM Plex Mono',monospace; font-size:12.5px; margin-top:12px; min-height:1.2em; }
.login a { color:inherit; }
.login .btn.big { display:inline-block; margin-top:8px; padding:15px 30px; font-size:13px; text-decoration:none; }
.login .how { font-size:13.5px; color:var(--ink-faint); margin-top:14px; }
</style></head>
<body><div class="wrap"><div class="login">
<img src="/brand/mark.png" alt="Nook">
<h1>Open your nook.</h1>
<p>One tap in Telegram and the bot hands you a key.</p>
<a class="btn primary big" href="https://t.me/Nook_digest_bot?start=webkey">Get a key from the bot</a>
<p class="how">It DMs back a 6-letter key - and on your phone, a one-tap button that signs you in outright.</p>
<form class="bar" id="f"><input id="code" maxlength="6" autocomplete="one-time-code" placeholder="ABC123"><button class="btn" type="submit">Open</button></form>
<div class="err" id="err"></div>
<p class="note">no password, no email - the bot already knows you</p>
</div></div>
<script>
async function tryCode(code) {
  const r = await fetch('/app/login', { method: 'POST', headers: {'content-type':'application/json'}, body: JSON.stringify({code}) });
  if (r.ok) { location.href = '/app'; }
  else { document.getElementById('err').textContent = 'That code did not work. Keys last ten minutes and work once - tap the button above for a fresh one.'; }
}
document.getElementById('f').addEventListener('submit', (e) => {
  e.preventDefault();
  tryCode(document.getElementById('code').value);
});
const fromLink = new URLSearchParams(location.search).get('key');
if (fromLink) {
  document.getElementById('code').value = fromLink.toUpperCase();
  tryCode(fromLink);
}
</script>
</body></html>
""".replace("__HEAD__", _HEAD).replace("__CSS__", _CSS)

APP_HTML = """<!doctype html>
<html lang="en"><head>__HEAD__
<title>Nook</title>
<style>__CSS__</style></head>
<body>
<div class="wrap">
<header>
  <div class="brand"><img src="/brand/mark.png" alt="Nook"><span class="word">Nook</span></div>
  <a class="btn" href="https://t.me/Nook_digest_bot">Bot</a>
</header>

<div class="bar">
  <input id="saveurl" placeholder="Paste a link to file it...">
  <button class="btn primary" id="savebtn">File it</button>
</div>

<nav class="tabs">
  <button data-tab="reads" class="on">Reads</button>
  <button data-tab="ask">Ask</button>
  <button data-tab="letter">Letter</button>
  <button data-tab="jobs">Openings</button>
</nav>

<main id="main"><div class="spinner">collecting your clippings...</div></main>
<p class="note" id="toast"></p>
</div>
<script>
const main = document.getElementById('main');
const toast = document.getElementById('toast');
const esc = (s) => (s||'').replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const clip = (it) => `<div class="clip"><div class="id">#${it.id}</div><h3><a href="${esc(it.url)}">${esc(it.title)}</a></h3><p>${esc((it.summary||'').split('\\n')[0])}</p><div class="tags">${(it.tags||'').split(',').filter(t=>t.trim()).map(t=>`<span>${esc(t.trim())}</span>`).join('')}</div></div>`;

async function load(tab) {
  document.querySelectorAll('nav.tabs button').forEach(b => b.classList.toggle('on', b.dataset.tab === tab));
  main.innerHTML = '<div class="spinner">collecting...</div>';
  if (tab === 'reads') {
    const items = await (await fetch('/api/reads')).json();
    main.innerHTML = items.length ? `<div class="grid">${items.map(clip).join('')}</div>` : '<div class="empty">The shelf is empty. Toss the bot a link.</div>';
  } else if (tab === 'letter') {
    const d = await (await fetch('/api/digest')).json();
    const reads = d.reads.map(it => `<div class="item"><b>#${it.id} ${esc(it.title)}</b><small>${esc((it.summary||'').split('\\n')[0])}</small><span class="u">${esc((it.url||'').replace(/^https?:\\/\\//,'').split('/')[0])}</span></div>`).join('');
    const jobs = d.jobs.map(j => `<div class="item"><b>${esc(j.title)} @ ${esc(j.company)}</b><small>${esc(j.salary)}</small><span class="u">${esc((j.url||'').replace(/^https?:\\/\\//,'').split('/')[0])}</span></div>`).join('');
    main.innerHTML = `<div class="letter"><div class="lh"><span>Nook - The Morning Letter</span><span>${new Date().toDateString()}</span></div>
      <div class="sec-h">In your nook - ${d.reads.length} unread</div>${reads || '<div class="item">All caught up.</div>'}
      <div class="sec-h">Fresh openings - paid, checked now</div>${jobs || '<div class="item">Nothing fresh right now.</div>'}
      <p style="font-family:Newsreader,serif;font-style:italic;color:var(--ink-soft);margin-top:22px">- your magpie</p></div>`;
  } else if (tab === 'jobs') {
    const jobs = await (await fetch('/api/jobs')).json();
    const rows = jobs.map(j => `<div class="job"><b><a href="${esc(j.url)}">${esc(j.title)}</a></b> @ ${esc(j.company)}<div class="meta">${esc(j.salary)} &middot; ${esc((j.url||'').replace(/^https?:\\/\\//,'').split('/')[0])}</div></div>`).join('');
    main.innerHTML = '<p class="feednote">Live from RemoteOK + Remotive at open. Paid listings matched to your fresher-dev keywords, cross-posts merged.</p>' + (jobs.length ? rows : '<div class="empty">No fresh openings right now.</div>');
  } else if (tab === 'ask') {
    main.innerHTML = `<div class="askwrap">
      <p class="askintro">Ask across everything you have filed. The magpie answers from your own clippings and notes, and names its sources.</p>
      <div class="bar"><input id="q" placeholder="Ask your nook anything..."><button class="btn primary" id="askbtn">Ask</button></div>
      <div class="chips">
        <button class="chip">Summarize my unread reads</button>
        <button class="chip">What did I save about AI?</button>
        <button class="chip">What themes keep coming up in my nook?</button>
      </div>
      <div id="ans"></div></div>`;
    document.getElementById('askbtn').onclick = ask;
    document.getElementById('q').addEventListener('keydown', (e) => { if (e.key === 'Enter') ask(); });
    document.querySelectorAll('.chip').forEach(c => c.onclick = () => { document.getElementById('q').value = c.textContent; ask(); });
  }
}
async function ask() {
  const q = document.getElementById('q').value.trim();
  if (!q) return;
  document.getElementById('ans').innerHTML = '<div class="spinner">the magpie is thinking...</div>';
  const r = await (await fetch('/api/ask?q=' + encodeURIComponent(q))).json();
  const srcs = (r.sources || []).map(x => `<a href="${esc(x.url)}">#${x.id} ${esc(x.title)}</a>`).join(' &middot; ');
  document.getElementById('ans').innerHTML = `<div class="answer"><div class="q">${esc(q)}</div>${esc(r.answer).replace(/\\n/g,'<br>')}${srcs ? `<div class="srcs">${srcs}</div>` : ''}</div>`;
}
document.querySelectorAll('nav.tabs button').forEach(b => b.onclick = () => load(b.dataset.tab));
document.getElementById('savebtn').onclick = async () => {
  const u = document.getElementById('saveurl').value.trim();
  if (!u) return;
  toast.textContent = 'filing...';
  const r = await fetch('/api/save', { method:'POST', headers:{'content-type':'application/json'}, body: JSON.stringify({url: u}) });
  toast.textContent = r.ok ? 'Filed. The summary lands in a few seconds - check Reads.' : 'Could not file that one.';
  if (r.ok) { document.getElementById('saveurl').value = ''; setTimeout(() => load('reads'), 4000); }
};
document.getElementById('saveurl').addEventListener('keydown', (e) => { if (e.key === 'Enter') document.getElementById('savebtn').click(); });
if ('serviceWorker' in navigator) navigator.serviceWorker.register('/app/sw.js');
const params = new URLSearchParams(location.search);
const shared = params.get('url') || params.get('text');
if (shared && /^https?:\\/\\//.test(shared)) { document.getElementById('saveurl').value = shared; document.getElementById('savebtn').click(); history.replaceState(null,'','/app'); }
load('reads');
</script>
</body></html>
""".replace("__HEAD__", _HEAD).replace("__CSS__", _CSS)
