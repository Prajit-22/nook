"""Landing page served at GET / - editorial ink style, in the Memetic spirit:
cream paper, forest-green ink, one amber accent, serif display + mono margin
notes, hand-drawn SVG illustration, scroll-driven diagram, load choreography.
Brand images are served from the worker's static assets."""

_BRAND = "/brand"

LANDING_HTML = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Nook - your reading nook on Telegram</title>
<meta name="description" content="Toss links into your nook all day. Wake up to one sealed letter: your reads, summarized, plus fresh paid openings worth applying to. A self-hosted Telegram bot on Cloudflare's free tier.">
<link rel="icon" type="image/png" href="__BRAND__/seal.png">
<meta property="og:type" content="website">
<meta property="og:title" content="Nook - your reading nook on Telegram">
<meta property="og:description" content="Toss links in all day. Wake up to one sealed letter: your reads, summarized, plus fresh paid openings.">
<meta property="og:image" content="https://nook.prjtchaturvedi.workers.dev__BRAND__/og.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#F6F1E5">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..900;1,9..144,300..900&family=IBM+Plex+Mono:ital,wght@0,400;0,500;1,400&display=swap" rel="stylesheet">
<style>
:root {
  --paper: #F6F1E5;
  --paper-2: #EFead9;
  --ink: #1E3D2F;
  --ink-soft: #43614F;
  --ink-faint: #7b8f82;
  --wax: #E8A33D;
  --rule: rgba(30, 61, 47, .22);
  --rule-soft: rgba(30, 61, 47, .12);
  --ease-out: cubic-bezier(.22, 1, .36, 1);
  --ease-spring: cubic-bezier(.2, 1.5, .35, 1);
}
* { margin: 0; padding: 0; box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  background: var(--paper);
  color: var(--ink);
  font-family: Georgia, 'Times New Roman', serif;
  font-size: 16px;
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
  overflow-x: hidden;
}
.serif { font-family: 'Fraunces', Georgia, serif; }
.mono { font-family: 'IBM Plex Mono', ui-monospace, monospace; }

/* paper grain + faint top rule */
body::before {
  content: ""; position: fixed; inset: 0; pointer-events: none; z-index: 0;
  background-image: radial-gradient(rgba(30,61,47,.05) 1px, transparent 1px);
  background-size: 22px 22px;
}
.page { position: relative; z-index: 1; max-width: 1120px; margin: 0 auto; padding: 0 28px; }

::selection { background: rgba(232,163,61,.4); }

/* ---------- load choreography ---------- */
.rise { opacity: 0; transform: translateY(18px); }
body.ready .rise { opacity: 1; transform: none; transition: opacity .8s var(--ease-out), transform .8s var(--ease-out); }
body.ready .rise.d1 { transition-delay: .05s } body.ready .rise.d2 { transition-delay: .16s }
body.ready .rise.d3 { transition-delay: .28s } body.ready .rise.d4 { transition-delay: .4s }
body.ready .rise.d5 { transition-delay: .52s } body.ready .rise.d6 { transition-delay: .66s }
.kicker-line { display: inline-block; width: 0; height: 1px; background: var(--wax); vertical-align: middle; margin-right: 10px; transition: width .7s var(--ease-out) .35s; }
body.ready .kicker-line { width: 34px; }

/* ---------- header ---------- */
header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 24px 0 22px; border-bottom: 1px solid var(--rule);
}
.brand { display: flex; align-items: center; gap: 12px; }
.brand img { width: 42px; height: 42px; transition: transform .4s var(--ease-spring); }
.brand:hover img { transform: rotate(-6deg) scale(1.06); }
.brand .word { font-family: 'Fraunces', serif; font-weight: 600; font-size: 27px; letter-spacing: .5px; }
nav a {
  color: var(--ink); text-decoration: none; margin-left: 28px;
  font-family: 'IBM Plex Mono', monospace; font-size: 13px;
  background-image: linear-gradient(var(--wax), var(--wax));
  background-size: 0% 2px; background-repeat: no-repeat; background-position: 0 100%;
  transition: background-size .35s var(--ease-out), color .25s;
  padding-bottom: 3px;
}
nav a:hover { background-size: 100% 2px; }
@media (max-width: 720px) { nav a { margin-left: 18px; font-size: 12.5px; } nav a:nth-child(1), nav a:nth-child(2), nav a:nth-child(3) { display: none; } header { padding: 18px 0 16px; } }

/* ---------- hero ---------- */
.hero { display: grid; grid-template-columns: 1.12fr .88fr; gap: 56px; align-items: center; padding: 96px 0 72px; }
@media (max-width: 820px) { .hero { grid-template-columns: 1fr; gap: 40px; padding: 48px 0 40px; } }
@media (max-width: 640px) {
  .kicker { font-size: 11px; letter-spacing: .12em; }
  .lede { font-size: 17px; }
  .cta .btn { width: 100%; text-align: center; }
  .margin-note { font-size: 12px; }
}
.kicker { font-family: 'IBM Plex Mono', monospace; font-size: 12.5px; letter-spacing: .16em; text-transform: uppercase; color: var(--ink-soft); }
h1 {
  font-family: 'Fraunces', serif; font-weight: 560; font-variation-settings: "opsz" 100;
  font-size: clamp(46px, 6.4vw, 80px); line-height: 1.03; letter-spacing: -0.018em;
  margin: 26px 0 26px;
}
h1 em { font-style: italic; font-weight: 480; color: var(--ink-soft); }
h1 .w { display: inline-block; opacity: 0; transform: translateY(.55em) rotate(1.5deg); }
body.ready h1 .w { opacity: 1; transform: none; transition: opacity .7s var(--ease-out), transform .7s var(--ease-out); }
.lede { font-size: 19px; max-width: 30em; color: var(--ink-soft); line-height: 1.65; }
.cta { display: flex; gap: 16px; margin-top: 40px; flex-wrap: wrap; }
.btn {
  position: relative; overflow: hidden; isolation: isolate;
  font-family: 'IBM Plex Mono', monospace; font-size: 14px; text-decoration: none;
  padding: 15px 28px; border-radius: 999px; border: 1.5px solid var(--ink);
  color: var(--ink); transition: color .3s var(--ease-out), border-color .3s, transform .3s var(--ease-out);
}
.btn::before {
  content: ""; position: absolute; inset: 0; z-index: -1;
  background: var(--ink); transform: translateY(101%); transition: transform .35s var(--ease-out);
}
.btn:hover::before { transform: translateY(0); }
.btn.primary { background: var(--ink); color: var(--paper); }
.btn.primary::before { background: var(--wax); }
.btn.primary:hover { color: var(--ink); border-color: var(--wax); }
.btn.ghost:hover { color: var(--paper); }
.btn:hover { transform: translateY(-2px); }
.btn:active { transform: translateY(0) scale(.98); }
.margin-note {
  font-family: 'IBM Plex Mono', monospace; font-size: 12.5px; color: var(--ink-soft);
  border-left: 2px solid var(--wax); padding-left: 12px; margin-top: 22px; max-width: 30em;
  line-height: 1.7;
}
.hero figure { position: relative; }
.hero figure img {
  width: 100%; border-radius: 4px; display: block;
  box-shadow: 0 1px 0 rgba(30,61,47,.15), 14px 18px 0 -6px var(--paper-2), 14px 18px 0 -5px var(--rule);
  transform: rotate(1.2deg);
  transition: transform .5s var(--ease-out);
}
.tape {
  position: absolute; top: -13px; left: 50%; transform: translateX(-50%) rotate(-3.5deg);
  width: 118px; height: 28px; background: rgba(232,163,61,.8); border-radius: 1px;
  box-shadow: 0 1px 2px rgba(30,61,47,.15);
}
.tape::after { content: ""; position: absolute; inset: 4px 6px; border: 1px dashed rgba(246,241,229,.7); }

/* ---------- sections ---------- */
section { padding: 96px 0; border-top: 1px solid var(--rule); position: relative; }
.sec-no {
  position: absolute; top: 96px; right: 0; text-align: right;
  font-family: 'Fraunces', serif; font-style: italic; font-size: 15px; color: var(--ink-faint);
}
@media (max-width: 820px) { .sec-no { display: none; } section { padding: 64px 0; } }
.sec-label { font-family: 'IBM Plex Mono', monospace; font-size: 12.5px; letter-spacing: .16em; text-transform: uppercase; color: var(--ink-soft); margin-bottom: 16px; }
.sec-label::before { content: ""; display: inline-block; width: 26px; height: 1px; background: var(--wax); vertical-align: middle; margin-right: 9px; }
h2 { font-family: 'Fraunces', serif; font-weight: 560; font-variation-settings: "opsz" 60; font-size: clamp(32px, 3.8vw, 46px); line-height: 1.1; letter-spacing: -0.012em; max-width: 19em; }
.sec-lede { font-size: 18px; color: var(--ink-soft); max-width: 34em; margin-top: 16px; line-height: 1.65; }

/* ---------- clippings (the collector) ---------- */
.cols { display: grid; grid-template-columns: repeat(3, 1fr); gap: 32px; margin-top: 56px; }
@media (max-width: 820px) { .cols { grid-template-columns: 1fr; max-width: 460px; } }
.clipping {
  position: relative; background: #FBF8EF; padding: 30px 26px 28px;
  box-shadow: 0 2px 0 rgba(30,61,47,.08), 0 14px 28px -18px rgba(30,61,47,.35);
  border: 1px solid var(--rule-soft);
  transition: transform .45s var(--ease-out), box-shadow .45s var(--ease-out);
}
.clipping:nth-child(1) { transform: rotate(-1.1deg); }
.clipping:nth-child(2) { transform: rotate(.7deg) translateY(10px); }
.clipping:nth-child(3) { transform: rotate(-.5deg); }
.clipping:hover { transform: rotate(0) translateY(-6px); box-shadow: 0 2px 0 rgba(30,61,47,.08), 0 24px 40px -20px rgba(30,61,47,.45); }
.clipping::before { /* tape corner */
  content: ""; position: absolute; top: -11px; left: 22px; width: 62px; height: 22px;
  background: rgba(232,163,61,.65); transform: rotate(-4deg); border-radius: 1px;
}
.clipping .n { font-family: 'IBM Plex Mono', monospace; font-size: 11.5px; color: var(--wax); letter-spacing: .14em; }
.clipping h3 { font-family: 'Fraunces', serif; font-weight: 600; font-size: 22px; margin: 12px 0 10px; }
.clipping p { font-size: 15.5px; color: var(--ink-soft); line-height: 1.6; }
.clipping svg { position: absolute; top: 24px; right: 22px; width: 34px; height: 34px; stroke: var(--ink-soft); fill: none; stroke-width: 1.6; stroke-linecap: round; stroke-linejoin: round; opacity: .85; transition: transform .4s var(--ease-spring); }
.clipping:hover svg { transform: rotate(-8deg) scale(1.12); stroke: var(--wax); }

/* ---------- scroll-driven diagram ---------- */
.diagram { margin-top: 64px; position: relative; }
.diagram svg { width: 100%; height: auto; display: block; overflow: visible; }
.diagram .rail { stroke: var(--rule); stroke-width: 1.5; fill: none; stroke-dasharray: 3 7; }
.diagram .ink-line { stroke: var(--ink); stroke-width: 2; fill: none; }
.diagram .node { transition: opacity .4s; }
.diagram .node .ring { fill: var(--paper); stroke: var(--rule); stroke-width: 1.5; transition: stroke .4s; }
.diagram .node.lit .ring { stroke: var(--wax); }
.diagram .node text { font-family: 'IBM Plex Mono', monospace; font-size: 12.5px; fill: var(--ink-soft); }
.diagram .node.lit text { fill: var(--ink); }
.diagram .node .ic { stroke: var(--ink-soft); stroke-width: 1.7; fill: none; stroke-linecap: round; stroke-linejoin: round; transition: stroke .4s; }
.diagram .node.lit .ic { stroke: var(--ink); }
.diagram .caption-row { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-top: 20px; }
.diagram .caption { font-family: 'IBM Plex Mono', monospace; font-size: 12.5px; color: var(--ink-soft); text-align: center; line-height: 1.7; opacity: .45; transition: opacity .4s; }
.diagram .caption.lit { opacity: 1; }
@media (max-width: 640px) {
  .diagram svg { display: none; }
  .diagram .caption-row { grid-template-columns: 1fr; gap: 0; margin-top: 8px; }
  .diagram .caption { font-size: 12.5px; text-align: left; padding: 16px 0 16px 20px; border-left: 2px solid var(--rule); opacity: 1; position: relative; }
  .diagram .caption::before { content: ""; position: absolute; left: -6px; top: 22px; width: 10px; height: 10px; border-radius: 50%; background: var(--paper); border: 1.5px solid var(--wax); }
  .diagram .caption b { color: var(--ink); font-weight: 500; }
}

/* ---------- the letter ---------- */
.letter-wrap { display: grid; grid-template-columns: 1fr .7fr; gap: 56px; margin-top: 56px; align-items: start; }
@media (max-width: 820px) { .letter-wrap { grid-template-columns: 1fr; gap: 40px; } }
.letter {
  position: relative; background: #FDFBF4; border: 1px solid var(--rule-soft);
  padding: 44px 40px 36px; max-width: 560px;
  box-shadow: 0 2px 0 rgba(30,61,47,.08), 0 20px 34px -20px rgba(30,61,47,.35);
  transform: rotate(-.6deg);
}
.letter::before { content: ""; position: absolute; inset: 10px; border: 1px solid var(--rule-soft); pointer-events: none; }
.letter .lh { display: flex; justify-content: space-between; align-items: baseline; border-bottom: 1px solid var(--rule); padding-bottom: 12px; gap: 14px; flex-wrap: wrap; }
@media (max-width: 640px) { .letter { padding: 30px 22px 28px; } .letter .lh .d { width: 100%; } }
.letter .lh .t { font-family: 'IBM Plex Mono', monospace; font-size: 11.5px; letter-spacing: .16em; text-transform: uppercase; color: var(--ink-soft); }
.letter .lh .d { font-family: 'IBM Plex Mono', monospace; font-size: 11.5px; color: var(--ink-faint); }
.letter .salut { font-family: 'Fraunces', serif; font-style: italic; font-size: 20px; margin: 22px 0 4px; }
.letter .sec-h { font-family: 'IBM Plex Mono', monospace; font-size: 11.5px; letter-spacing: .14em; text-transform: uppercase; color: var(--wax); margin-top: 24px; }
.letter .item { margin-top: 12px; font-size: 15px; line-height: 1.55; }
.letter .item b { font-weight: 600; }
.letter .item small { display: block; color: var(--ink-soft); }
.letter .item .u { font-family: 'IBM Plex Mono', monospace; font-size: 11.5px; color: var(--ink-faint); }
.letter .sign { font-family: 'Fraunces', serif; font-style: italic; font-size: 16px; color: var(--ink-soft); margin-top: 28px; }
.letter .seal { position: absolute; bottom: -30px; right: -26px; width: 86px; transform: rotate(8deg) scale(1.7); opacity: 0; }
.letter.in .seal { animation: stamp .55s var(--ease-spring) .25s forwards; }
@keyframes stamp {
  0% { opacity: 0; transform: rotate(8deg) scale(1.7); }
  60% { opacity: 1; transform: rotate(6deg) scale(.94); }
  80% { transform: rotate(9deg) scale(1.04); }
  100% { opacity: 1; transform: rotate(8deg) scale(1); }
}
.letter .seal:hover { animation: sealpress .5s var(--ease-spring) forwards; }
@keyframes sealpress { 50% { transform: rotate(8deg) scale(.9); } 100% { transform: rotate(8deg) scale(1); } }
.letter .item, .letter .salut, .letter .sign { opacity: 0; transform: translateY(8px); transition: opacity .5s var(--ease-out), transform .5s var(--ease-out); }
.letter.in .salut, .letter.in .item, .letter.in .sign { opacity: 1; transform: none; }
.letter.in .salut { transition-delay: .15s; }
.letter.in .item { transition-delay: .35s; }
.letter.in .item ~ .item { transition-delay: .5s; }
.letter.in .sec-h ~ .item { transition-delay: .6s; }
.letter.in .sign { transition-delay: .8s; }
.letter-side .rule-note { border-top: 1px solid var(--rule); padding-top: 14px; margin-top: 22px; font-family: 'IBM Plex Mono', monospace; font-size: 12.5px; color: var(--ink-soft); line-height: 1.75; }
.letter-side .rule-note b { color: var(--ink); font-weight: 500; }

/* ---------- spec sheet ---------- */
.spec { margin-top: 56px; border-top: 1px solid var(--rule); }
.spec .row {
  display: grid; grid-template-columns: 220px 1fr auto; gap: 24px; align-items: baseline;
  padding: 20px 4px; border-bottom: 1px solid var(--rule-soft);
  transition: background .3s, padding-left .3s var(--ease-out);
}
.spec .row:hover { background: rgba(255,255,255,.5); padding-left: 14px; }
.spec .k { font-family: 'IBM Plex Mono', monospace; font-size: 13px; color: var(--ink-soft); letter-spacing: .04em; }
.spec .v { font-size: 16.5px; }
.spec .v b { font-family: 'Fraunces', serif; font-weight: 600; font-size: 18px; }
.spec .c { font-family: 'IBM Plex Mono', monospace; font-size: 12px; color: var(--ink-faint); }
@media (max-width: 720px) { .spec .row { grid-template-columns: 1fr; gap: 4px; } }

/* ---------- self-host ---------- */
.steps { margin-top: 52px; counter-reset: step; }
.step2 { display: grid; grid-template-columns: 64px 1fr; gap: 20px; padding: 18px 0; border-bottom: 1px dashed var(--rule); }
.step2 .num {
  font-family: 'Fraunces', serif; font-style: italic; font-size: 30px; color: var(--wax);
  width: 56px; height: 56px; border: 1.5px solid var(--rule); border-radius: 50%;
  display: grid; place-items: center;
}
.step2 p { font-size: 16.5px; padding-top: 6px; }
.step2 code { font-family: 'IBM Plex Mono', monospace; font-size: 14px; background: rgba(30,61,47,.07); padding: 2px 8px; border-radius: 4px; }

footer { border-top: 1px solid var(--rule); padding: 44px 0 60px; }
.foot-grid { display: flex; justify-content: space-between; align-items: flex-end; flex-wrap: wrap; gap: 18px; }
footer .quip { font-family: 'Fraunces', serif; font-style: italic; font-size: 19px; color: var(--ink-soft); max-width: 22em; }
footer .colophon { font-family: 'IBM Plex Mono', monospace; font-size: 12px; color: var(--ink-faint); line-height: 1.9; text-align: right; }
footer .colophon a { color: var(--ink-soft); text-decoration: none; border-bottom: 1px solid var(--rule); transition: color .25s, border-color .25s; }
footer .colophon a:hover { color: var(--wax); border-color: var(--wax); }

.reveal { opacity: 0; transform: translateY(28px); transition: opacity .75s var(--ease-out), transform .75s var(--ease-out); }
.reveal.in { opacity: 1; transform: none; }
.clipping.reveal:nth-child(1).in { transform: rotate(-1.1deg); }
.clipping.reveal:nth-child(2).in { transform: rotate(.7deg) translateY(10px); }
.clipping.reveal:nth-child(3).in { transform: rotate(-.5deg); }
.clipping.reveal.in:hover { transform: rotate(0) translateY(-6px); }

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: .01ms !important; transition-duration: .01ms !important; }
  .rise, h1 .w, .reveal, .letter .item, .letter .salut, .letter .sign, .letter .seal { opacity: 1 !important; transform: none !important; }
  .kicker-line { width: 34px !important; }
}
</style>
</head>
<body>
<div class="page">

<header>
  <div class="brand rise d1">
    <img src="__BRAND__/mark.png" alt="Nook logo - an n formed by a stack of clippings, a magpie perched on top">
    <span class="word">Nook</span>
  </div>
  <nav class="mono rise d1">
    <a href="#how">The collector</a>
    <a href="#digest">The morning letter</a>
    <a href="#selfhost">Self-host</a>
    <a href="https://github.com/Prajit-22/nook">GitHub</a>
  </nav>
</header>

<div class="hero">
  <div>
    <div class="kicker rise d2"><span class="kicker-line"></span>A Telegram bot, kept by a magpie</div>
    <h1 aria-label="Toss links in all day. Wake up to one sealed letter.">Toss links in all day. <em>Wake up to one sealed letter.</em></h1>
    <p class="lede rise d4">Nook is a small bot with a magpie's habits. Every link you toss at it gets fetched, read, summarized and filed. At 08:00 sharp it delivers one letter: what you saved, what it says, and which fresh paid openings are worth your morning.</p>
    <div class="cta rise d5">
      <a class="btn primary" href="https://t.me/Nook_digest_bot">Talk to @Nook_digest_bot</a>
      <a class="btn ghost" href="https://github.com/Prajit-22/nook">Star on GitHub</a>
    </div>
    <p class="margin-note rise d6">runs entirely on Cloudflare's free tier<br>no server &middot; no Docker &middot; no bill</p>
  </div>
  <figure class="rise d3">
    <div class="tape"></div>
    <img id="magpie" src="__BRAND__/magpie.jpg" alt="Ink illustration of a magpie perched on a stack of sealed letters">
  </figure>
</div>

<section id="how">
  <div class="sec-no">No. 1</div>
  <div class="sec-label">The collector</div>
  <h2>Magpies hoard shiny things.<br>Yours hoards links.</h2>
  <div class="cols">
    <div class="clipping reveal">
      <svg viewBox="0 0 34 34"><path d="M21 9 L10 20 a4.2 4.2 0 0 0 6 6 L27 15 a6.8 6.8 0 0 0 -9.6 -9.6 L7 16"/></svg>
      <div class="n">FIG. 01</div>
      <h3>Send anything</h3>
      <p>A link, or a thought with /note. The page is fetched at the edge, the text pulled out, and an LLM writes a two-sentence summary with tags before it hits the shelf.</p>
    </div>
    <div class="clipping reveal">
      <svg viewBox="0 0 34 34"><circle cx="15" cy="15" r="8"/><path d="M21 21 L28 28"/><path d="M12 15 a3 3 0 0 1 3 -3"/></svg>
      <div class="n">FIG. 02</div>
      <h3>Ask it back</h3>
      <p>Plain questions search your whole nook with BM25 and answer with cited sources. Send the same link twice and it is recognized, not re-filed.</p>
    </div>
    <div class="clipping reveal">
      <svg viewBox="0 0 34 34"><path d="M8 10 h18 M8 17 h18 M8 24 h11"/><path d="M22 22 l6 6 M28 22 l-6 6"/></svg>
      <div class="n">FIG. 03</div>
      <h3>Forget on command</h3>
      <p>/list shows recent saves, /forget removes one. The database lives in your own Cloudflare account - your clippings never sit on anyone else's shelf.</p>
    </div>
  </div>

  <div class="diagram" id="diagram">
    <svg viewBox="0 0 1000 170" aria-hidden="true">
      <path class="rail" d="M120 85 H 880"/>
      <path class="ink-line" id="inkpath" d="M120 85 H 880"/>
      <g class="node" id="node1">
        <circle class="ring" cx="120" cy="85" r="34"/>
        <g class="ic" transform="translate(108 73)"><path d="M14 4 L6 12 a4 4 0 0 0 5.6 5.6 L20 9 a6.5 6.5 0 0 0 -9.2 -9.2 L4 6"/></g>
        <text x="120" y="145" text-anchor="middle">you send a link</text>
      </g>
      <g class="node" id="node2">
        <circle class="ring" cx="500" cy="85" r="34"/>
        <g class="ic" transform="translate(488 73)"><path d="M3 12 q4 -8 9 -2 q5 -6 9 2"/><path d="M6 18 h12 M6 22 h8"/></g>
        <text x="500" y="145" text-anchor="middle">fetched, summarized, tagged</text>
      </g>
      <g class="node" id="node3">
        <circle class="ring" cx="880" cy="85" r="34"/>
        <g class="ic" transform="translate(866 71)"><rect x="2" y="6" width="24" height="17" rx="1.5"/><path d="M2 8 L14 16 L26 8"/></g>
        <text x="880" y="145" text-anchor="middle">one letter at 08:00</text>
      </g>
    </svg>
    <div class="caption-row">
      <div class="caption" id="cap1"><b>You send a link</b><br>webhook, secret-verified - dropped on the pile</div>
      <div class="caption" id="cap2"><b>Fetched, summarized, tagged</b><br>Workers AI at the edge - two sentences + tags</div>
      <div class="caption" id="cap3"><b>One letter at 08:00</b><br>D1 + FTS5 underneath - sealed, delivered once</div>
    </div>
  </div>
</section>

<section id="digest">
  <div class="sec-no">No. 2</div>
  <div class="sec-label">The morning letter</div>
  <h2>One sealed digest, 08:00 sharp.</h2>
  <p class="sec-lede">Unread reads on top, then fresh openings pulled live from public job boards at send time. Paid roles only. Nothing is ever sent twice.</p>
  <div class="letter-wrap">
    <div class="letter" id="letter">
      <img class="seal" src="__BRAND__/seal.png" alt="Amber wax seal stamped with an N">
      <div class="lh"><span class="t">Nook - The Morning Letter</span><span class="d">no. 214 &middot; 08:00 IST</span></div>
      <p class="salut">Good morning. Three things you saved, two worth applying to.</p>
      <div class="sec-h">In your nook - 3 unread</div>
      <div class="item"><b>#12 Vector indexes, explained simply</b><small>why HNSW wins at recall per ms, in pictures</small><span class="u">simonwillison.net</span></div>
      <div class="item"><b>#14 The $0 LLM stack</b><small>free tiers, compared honestly</small><span class="u">github.com</span></div>
      <div class="sec-h">Fresh openings - paid, checked at send time</div>
      <div class="item"><b>Backend Engineer Intern @ Acme</b><small>$20k-$40k/yr &middot; remote</small><span class="u">remoteok.com</span></div>
      <p class="sign">- your magpie</p>
    </div>
    <div class="letter-side">
      <div class="rule-note reveal"><b>Reads first.</b> Whatever you saved and never opened rides at the top, one line of summary each, source attached.</div>
      <div class="rule-note reveal"><b>Then openings.</b> RemoteOK and Remotive are queried at send time, not cached overnight - if a listing is dead by morning, it never reaches you.</div>
      <div class="rule-note reveal"><b>Exactly once.</b> Every opening is hashed against your history. The letter never repeats itself.</div>
    </div>
  </div>
</section>

<section id="stack">
  <div class="sec-no">No. 3</div>
  <div class="sec-label">Under the feathers</div>
  <h2>One Python Worker, four free services,<br>zero maintenance.</h2>
  <div class="spec">
    <div class="row reveal"><span class="k">TELEGRAM</span><span class="v"><b>Webhook in, letter out.</b> HMAC secret checked on every call; forged updates are dropped unread.</span><span class="c">@Nook_digest_bot</span></div>
    <div class="row reveal"><span class="k">WORKERS AI</span><span class="v"><b>Summaries, tags, answers.</b> Llama 3.1 at the edge - no API key, no quota anxiety.</span><span class="c">free tier</span></div>
    <div class="row reveal"><span class="k">D1 + FTS5</span><span class="v"><b>Your shelf.</b> SQLite with BM25 full-text search and sha256 dedup.</span><span class="c">your account</span></div>
    <div class="row reveal"><span class="k">CRON</span><span class="v"><b>The 08:00 alarm.</b> One trigger, one letter, then silence for 24 hours.</span><span class="c">30 2 * * *</span></div>
  </div>
  <p class="margin-note reveal">58 unit tests, CI on every push - the runtime file is the only untested seam</p>
</section>

<section id="selfhost">
  <div class="sec-no">No. 4</div>
  <div class="sec-label">Keep your own magpie</div>
  <h2>Deploy your own in about five minutes.</h2>
  <div class="steps">
    <div class="step2 reveal"><div class="num">1</div><p>Ask BotFather for a token. One message, no forms.</p></div>
    <div class="step2 reveal"><div class="num">2</div><p>Fork the repo, create one D1 database, set two secrets.</p></div>
    <div class="step2 reveal"><div class="num">3</div><p><code>wrangler deploy</code> - the webhook registers itself. Keywords, digest hour and allow-list are yours to tune.</p></div>
  </div>
  <div class="cta">
    <a class="btn primary" href="https://github.com/Prajit-22/nook">Deploy from GitHub</a>
    <a class="btn ghost" href="https://deploy.workers.cloudflare.com/?url=https://github.com/Prajit-22/nook">Deploy to Cloudflare</a>
  </div>
</section>

<footer>
  <div class="foot-grid">
    <div class="quip">No magpies were rushed in the making of your digest.</div>
    <div class="colophon">
      set in Fraunces &amp; IBM Plex Mono &middot; ink #1E3D2F on cream<br>
      <a href="https://github.com/Prajit-22/nook">Prajit-22/nook</a> &middot; MIT &middot; <a href="https://t.me/Nook_digest_bot">@Nook_digest_bot</a>
    </div>
  </div>
</footer>

</div>
<script>
(function () {
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* word-split the h1 for staggered rise */
  var h1 = document.querySelector('h1');
  var walk = function (node, delay) {
    var out = [];
    node.childNodes.forEach(function (n) {
      if (n.nodeType === 3) {
        n.textContent.split(/(\s+)/).forEach(function (piece) {
          if (!piece) return;
          if (/^\s+$/.test(piece)) { out.push(document.createTextNode(' ')); return; }
          var s = document.createElement('span');
          s.className = 'w'; s.textContent = piece;
          s.style.transitionDelay = (delay.value += 0.055) + 's';
          out.push(s);
        });
      } else {
        var wrap = n.cloneNode(false);
        walk(n, delay).forEach(function (c) { wrap.appendChild(c); });
        out.push(wrap);
      }
    });
    return out;
  };
  var d = { value: 0.1 };
  var frag = walk(h1, d);
  h1.textContent = '';
  frag.forEach(function (c) { h1.appendChild(c); });

  document.body.classList.add('ready');

  /* scroll reveals - observer plus a sweep that catches jump-scrolls */
  var sweepTargets = Array.prototype.slice.call(document.querySelectorAll('.reveal, .letter'));
  function sweep() {
    var vh = window.innerHeight;
    sweepTargets = sweepTargets.filter(function (el) {
      var r = el.getBoundingClientRect();
      if (r.top < vh * 0.92 && r.bottom > -40) { el.classList.add('in'); return false; }
      if (r.bottom <= -40) { el.classList.add('in'); return false; } /* jumped past it */
      return true;
    });
  }
  sweep();
  window.addEventListener('scroll', sweep, { passive: true });
  window.addEventListener('resize', sweep, { passive: true });

  /* scroll-driven diagram: the ink line draws itself between nodes */
  var path = document.getElementById('inkpath');
  var len = path.getTotalLength();
  path.style.strokeDasharray = len;
  path.style.strokeDashoffset = reduced ? 0 : len;
  var nodes = [document.getElementById('node1'), document.getElementById('node2'), document.getElementById('node3')];
  var caps = [document.getElementById('cap1'), document.getElementById('cap2'), document.getElementById('cap3')];
  var diagram = document.getElementById('diagram');
  function drawDiagram() {
    var r = diagram.getBoundingClientRect();
    var vh = window.innerHeight;
    var p = (vh * 0.85 - r.top) / (r.height + vh * 0.35);
    p = Math.max(0, Math.min(1, p));
    path.style.strokeDashoffset = reduced ? 0 : len * (1 - p);
    nodes.forEach(function (n, i) { n.classList.toggle('lit', p > 0.08 + i * 0.33); });
    caps.forEach(function (c, i) { c.classList.toggle('lit', p > 0.15 + i * 0.33); });
  }
  drawDiagram();
  window.addEventListener('scroll', drawDiagram, { passive: true });

  /* the magpie watches your cursor */
  var magpie = document.getElementById('magpie');
  if (!reduced) {
    var tx = 0, ty = 0, cx = 0, cy = 0;
    window.addEventListener('mousemove', function (e) {
      tx = (e.clientX / window.innerWidth - 0.5) * 7;
      ty = (e.clientY / window.innerHeight - 0.5) * 5;
    }, { passive: true });
    (function drift() {
      cx += (tx - cx) * 0.06; cy += (ty - cy) * 0.06;
      var t = Date.now() / 1000;
      var bobY = Math.sin(t * 1.25) * 5;
      var bobR = Math.sin(t * 0.8) * 0.6;
      magpie.style.transform = 'rotate(' + (1.2 + bobR + cx * 0.35) + 'deg) translate(' + cx + 'px,' + (cy + bobY) + 'px)';
      requestAnimationFrame(drift);
    })();
  }
})();
</script>
</body>
</html>
""".replace("__BRAND__", _BRAND)

_ERROR_TMPL = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__ - Nook</title>
<link rel="icon" type="image/png" href="__BRAND__/seal.png">
<style>
body { background: #F6F1E5; color: #1E3D2F; font-family: Georgia, serif; display: grid; place-items: center; min-height: 100vh; margin: 0; text-align: center; }
h1 { font-family: 'Fraunces', Georgia, serif; font-weight: 560; font-size: clamp(40px, 8vw, 72px); margin: 18px 0 10px; }
p { color: #43614F; font-size: 18px; }
a { color: #1E3D2F; font-family: 'IBM Plex Mono', monospace; font-size: 14px; }
img { width: 84px; }
.num { font-family: 'IBM Plex Mono', monospace; font-size: 13px; letter-spacing: .2em; color: #E8A33D; }
</style></head>
<body><div>
<img src="__BRAND__/mark.png" alt="Nook logo">
<div class="num">__CODE__</div>
<h1>__TITLE__</h1>
<p>__MSG__</p>
<p><a href="/">back to the nook</a></p>
</div></body></html>
"""

NOT_FOUND_HTML = (
    _ERROR_TMPL.replace("__CODE__", "ERROR 404")
    .replace("__TITLE__", "This shelf is empty.")
    .replace("__MSG__", "Whatever was clipped here is gone - or never was.")
    .replace("__BRAND__", _BRAND)
)

SERVER_ERROR_HTML = (
    _ERROR_TMPL.replace("__CODE__", "ERROR 500")
    .replace("__TITLE__", "The magpie dropped it.")
    .replace("__MSG__", "Something broke on our perch. Try again in a moment.")
    .replace("__BRAND__", _BRAND)
)
