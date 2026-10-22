"""Landing page served at GET / - editorial ink style: cream paper,
forest-green ink, amber wax accent, serif display + mono margin notes.
Brand images are served from the GitHub repo via jsDelivr."""

_BRAND = "/brand"

LANDING_HTML = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Nook - your reading nook on Telegram</title>
<meta name="description" content="Toss links into your nook all day. Wake up to one digest: your reads, summarized, plus fresh paid openings worth applying to. A self-hosted Telegram bot on Cloudflare's free tier.">
<link rel="icon" href="__BRAND__/seal.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..900;1,9..144,300..900&family=IBM+Plex+Mono:ital,wght@0,400;0,500;1,400&display=swap" rel="stylesheet">
<style>
:root {
  --paper: #F6F1E5;
  --ink: #1E3D2F;
  --ink-soft: #3C5A4A;
  --wax: #E8A33D;
  --rule: rgba(30, 61, 47, .22);
}
* { margin: 0; padding: 0; box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  background: var(--paper);
  color: var(--ink);
  font-family: Georgia, 'Times New Roman', serif;
  line-height: 1.55;
  -webkit-font-smoothing: antialiased;
}
.serif { font-family: 'Fraunces', Georgia, serif; }
.mono { font-family: 'IBM Plex Mono', ui-monospace, monospace; }

/* paper grain */
body::before {
  content: ""; position: fixed; inset: 0; pointer-events: none; z-index: 0;
  background-image: radial-gradient(rgba(30,61,47,.045) 1px, transparent 1px);
  background-size: 22px 22px;
}
.page { position: relative; z-index: 1; max-width: 1080px; margin: 0 auto; padding: 0 24px; }

header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 28px 0; border-bottom: 1px solid var(--rule);
}
.brand { display: flex; align-items: center; gap: 12px; }
.brand img { width: 40px; height: 40px; border-radius: 9px; }
.brand .word { font-family: 'Fraunces', serif; font-weight: 600; font-size: 26px; letter-spacing: .5px; }
nav a { color: var(--ink); text-decoration: none; margin-left: 26px; font-family: 'IBM Plex Mono', monospace; font-size: 13px; }
nav a:hover { color: var(--wax); }

.hero { display: grid; grid-template-columns: 1.15fr .85fr; gap: 48px; align-items: center; padding: 84px 0 64px; }
@media (max-width: 820px) { .hero { grid-template-columns: 1fr; padding: 56px 0 40px; } }
.kicker { font-family: 'IBM Plex Mono', monospace; font-size: 13px; letter-spacing: .14em; text-transform: uppercase; color: var(--ink-soft); }
.kicker::before { content: ""; display: inline-block; width: 34px; height: 1px; background: var(--wax); vertical-align: middle; margin-right: 10px; }
h1 { font-family: 'Fraunces', serif; font-weight: 560; font-size: clamp(44px, 6.2vw, 76px); line-height: 1.04; letter-spacing: -0.015em; margin: 22px 0 24px; }
h1 em { font-style: italic; color: var(--ink-soft); }
.lede { font-size: 19px; max-width: 30em; color: var(--ink-soft); }
.cta { display: flex; gap: 16px; margin-top: 36px; flex-wrap: wrap; }
.btn {
  font-family: 'IBM Plex Mono', monospace; font-size: 14px; text-decoration: none;
  padding: 14px 26px; border-radius: 999px; border: 1.5px solid var(--ink);
  color: var(--ink); transition: all .25s ease;
}
.btn.primary { background: var(--ink); color: var(--paper); }
.btn.primary:hover { background: var(--wax); border-color: var(--wax); color: var(--ink); transform: translateY(-2px); }
.btn.ghost:hover { border-color: var(--wax); color: var(--wax); transform: translateY(-2px); }
.hero figure { position: relative; }
.hero figure img { width: 100%; border-radius: 12px; display: block; animation: bob 5s ease-in-out infinite; }
@keyframes bob { 0%,100% { transform: translateY(0) rotate(0deg); } 50% { transform: translateY(-8px) rotate(-0.6deg); } }
.tape {
  position: absolute; top: -14px; left: 50%; transform: translateX(-50%) rotate(-3deg);
  width: 120px; height: 30px; background: rgba(232,163,61,.75); border-radius: 2px;
}
.margin-note {
  font-family: 'IBM Plex Mono', monospace; font-size: 12.5px; color: var(--ink-soft);
  border-left: 2px solid var(--wax); padding-left: 12px; margin-top: 18px; max-width: 26em;
}

section { padding: 72px 0; border-top: 1px solid var(--rule); }
.sec-label { font-family: 'IBM Plex Mono', monospace; font-size: 12.5px; letter-spacing: .14em; text-transform: uppercase; color: var(--ink-soft); margin-bottom: 14px; }
h2 { font-family: 'Fraunces', serif; font-weight: 560; font-size: clamp(30px, 3.6vw, 44px); line-height: 1.12; letter-spacing: -0.01em; max-width: 18em; }
.cols { display: grid; grid-template-columns: repeat(3, 1fr); gap: 28px; margin-top: 44px; }
@media (max-width: 820px) { .cols { grid-template-columns: 1fr; } }
.card {
  background: rgba(255,255,255,.55); border: 1px solid var(--rule); border-radius: 10px;
  padding: 26px 24px; position: relative;
}
.card .n { font-family: 'IBM Plex Mono', monospace; font-size: 12px; color: var(--wax); letter-spacing: .1em; }
.card h3 { font-family: 'Fraunces', serif; font-weight: 600; font-size: 21px; margin: 10px 0 8px; }
.card p { font-size: 15.5px; color: var(--ink-soft); }

/* flow diagram */
.flow { display: grid; grid-template-columns: 1fr 44px 1fr 44px 1fr; align-items: center; gap: 8px; margin-top: 48px; }
@media (max-width: 820px) { .flow { grid-template-columns: 1fr; } .arrow { transform: rotate(90deg); margin: 6px auto; } }
.step { text-align: center; padding: 22px 14px; border: 1.5px dashed var(--rule); border-radius: 12px; background: rgba(255,255,255,.4); }
.step .glyph { font-size: 30px; line-height: 1; }
.step .t { font-family: 'IBM Plex Mono', monospace; font-size: 12.5px; margin-top: 10px; color: var(--ink-soft); }
.arrow { height: 2px; background: var(--ink-soft); position: relative; }
.arrow::after { content: ""; position: absolute; right: -1px; top: -4px; border: 5px solid transparent; border-left-color: var(--ink-soft); }
.step .glyph .dot { display: inline-block; animation: hop 2.4s ease-in-out infinite; }
@keyframes hop { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-7px); } }

.digest-mock {
  margin-top: 44px; background: #fff; border: 1px solid var(--rule); border-radius: 12px;
  padding: 30px 28px; font-size: 15px; box-shadow: 6px 6px 0 rgba(30,61,47,.12);
  position: relative; max-width: 620px;
}
.digest-mock .seal { position: absolute; top: -26px; right: -22px; width: 74px; transform: rotate(8deg); }
.digest-mock .seal { opacity: 0; transform: rotate(8deg) scale(1.6); transition: opacity .45s ease, transform .45s cubic-bezier(.2,1.6,.4,1); }
.digest-mock.in .seal { opacity: 1; transform: rotate(8deg) scale(1); }
.digest-mock .dh { font-family: 'IBM Plex Mono', monospace; font-size: 12px; letter-spacing: .12em; color: var(--wax); text-transform: uppercase; }
.digest-mock .di { margin-top: 14px; }
.digest-mock .di b { font-weight: 600; }
.digest-mock .di small { display: block; color: var(--ink-soft); }
.digest-mock .du { font-family: 'IBM Plex Mono', monospace; font-size: 12px; color: var(--wax); }

footer { border-top: 1px solid var(--rule); padding: 40px 0 56px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 14px; }
footer .quip { font-family: 'Fraunces', serif; font-style: italic; font-size: 17px; color: var(--ink-soft); }
footer .mono a { color: var(--ink-soft); }

.reveal { opacity: 0; transform: translateY(26px); transition: opacity .7s ease, transform .7s ease; }
.reveal.in { opacity: 1; transform: none; }
</style>
</head>
<body>
<div class="page">

<header>
  <div class="brand">
    <img src="__BRAND__/mark.png" alt="Nook logo - an n formed by a stack of clippings">
    <span class="word">Nook</span>
  </div>
  <nav class="mono">
    <a href="#how">How it works</a>
    <a href="#digest">The morning letter</a>
    <a href="#selfhost">Self-host</a>
    <a href="https://github.com/Prajit-22/nook">GitHub</a>
  </nav>
</header>

<div class="hero">
  <div>
    <div class="kicker">A Telegram bot, kept by a magpie</div>
    <h1>Toss links in all day. <em>Wake up to one digest.</em></h1>
    <p class="lede">Nook fetches every link you send it, summarizes and tags it, and answers your questions with sources. Every morning it delivers one letter: your unread reads, plus fresh paid openings matched to you.</p>
    <div class="cta">
      <a class="btn primary" href="https://t.me/Nook_digest_bot">Talk to @Nook_digest_bot</a>
      <a class="btn ghost" href="https://github.com/Prajit-22/nook">Star on GitHub</a>
    </div>
    <p class="margin-note">runs on Cloudflare's free tier - no server, no Docker, no bill</p>
  </div>
  <figure class="reveal">
    <div class="tape"></div>
    <img src="__BRAND__/magpie.jpg" alt="A magpie perched on a stack of sealed letters, ink illustration">
  </figure>
</div>

<section id="how">
  <div class="sec-label">No. 1 - The collector</div>
  <h2>Magpies hoard shiny things. Yours hoards links.</h2>
  <div class="cols">
    <div class="card reveal"><div class="n">01</div><h3>Send anything</h3><p>A link, a thought with /note. The page is fetched, the text pulled out, and a 2-3 sentence summary plus tags are written by an LLM at the edge.</p></div>
    <div class="card reveal"><div class="n">02</div><h3>Ask it back</h3><p>Plain questions search your saves with BM25 and answer with cited sources. Duplicates are detected, so nothing is ever filed twice.</p></div>
    <div class="card reveal"><div class="n">03</div><h3>Forget on command</h3><p>/list shows your latest saves, /forget removes one. Your nook lives in your own Cloudflare account - your data, your database.</p></div>
  </div>
</section>

<section id="digest">
  <div class="sec-label">No. 2 - The morning letter</div>
  <h2>One sealed digest, 08:00 sharp.</h2>
  <p class="lede" style="margin-top:14px">Unread reads on top, then fresh openings - pulled live from public job boards at send time, paid roles only, each one sent exactly once.</p>
  <div class="digest-mock reveal">
    <img class="seal" src="__BRAND__/seal.png" alt="">
    <div class="dh">Good morning - your daily Nook digest</div>
    <div class="di"><b>IN YOUR NOOK - 3 unread</b>
      <small>#12 Vector indexes, explained simply - why HNSW wins at recall per ms</small>
      <small>#14 The $0 LLM stack - free tiers, compared honestly</small>
    </div>
    <div class="di"><b>FRESH OPENINGS (paid, live at send time)</b>
      <small>Backend Engineer Intern @ Acme - $20k-$40k/yr</small>
      <span class="du">remoteok.com/remote-jobs/...</span>
    </div>
  </div>
</section>

<section>
  <div class="sec-label">No. 3 - Under the feathers</div>
  <h2>One Python Worker, four free services.</h2>
  <div class="flow">
    <div class="step reveal"><div class="glyph">&#128279;</div><div class="t">Telegram webhook<br>secret-verified</div></div>
    <div class="arrow"></div>
    <div class="step reveal"><div class="glyph"><span class="dot">&#129518;</span></div><div class="t">Workers AI<br>summaries, tags, answers</div></div>
    <div class="arrow"></div>
    <div class="step reveal"><div class="glyph">&#128231;</div><div class="t">D1 + FTS5<br>BM25 search, dedup</div></div>
  </div>
  <p class="margin-note">58 unit tests, CI on every push - the runtime file is the only untested seam</p>
</section>

<section id="selfhost">
  <div class="sec-label">No. 4 - Keep your own magpie</div>
  <h2>Deploy your own in about five minutes.</h2>
  <p class="lede" style="margin-top:14px">One BotFather token, one D1 database, two secrets, <span class="mono">wrangler deploy</span>. Full instructions in the repo README - keywords, digest hour and allow-list are all yours to tune.</p>
  <div class="cta">
    <a class="btn primary" href="https://github.com/Prajit-22/nook">Deploy from GitHub</a>
    <a class="btn ghost" href="https://deploy.workers.cloudflare.com/?url=https://github.com/Prajit-22/nook">Deploy to Cloudflare</a>
  </div>
</section>

<footer>
  <div class="quip">No magpies were rushed in the making of your digest.</div>
  <div class="mono" style="font-size:12.5px"><a href="https://github.com/Prajit-22/nook">Prajit-22/nook</a> &nbsp;-&nbsp; MIT</div>
</footer>

</div>
<script>
const io = new IntersectionObserver((entries) => {
  for (const e of entries) if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
}, { threshold: 0.15 });
document.querySelectorAll('.reveal').forEach((el) => io.observe(el));
</script>
</body>
</html>
""".replace("__BRAND__", _BRAND)
