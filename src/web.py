"""Landing page served at GET / - editorial grid style: light paper, warm ink,
one sealing-wax accent, condensed display + reading serif + mono metadata,
hairline rules, numbered rows, a dense morning-letter mock, load choreography.
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
<meta name="theme-color" content="#F8F5EE">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Oswald:wght@400;500;600&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;1,6..72,400;1,6..72,500&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root {
  --paper: #F8F5EE;
  --card: #FFFDF6;
  --ink: #17130C;
  --ink-70: rgba(23, 19, 12, .7);
  --ink-55: rgba(23, 19, 12, .55);
  --ink-35: rgba(23, 19, 12, .35);
  --wax: #C2491D;
  --rule: rgba(23, 19, 12, .16);
  --rule-strong: rgba(23, 19, 12, .9);
  --ease-out: cubic-bezier(.22, 1, .36, 1);
  --ease-spring: cubic-bezier(.2, 1.5, .35, 1);
}
* { margin: 0; padding: 0; box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  background: var(--paper);
  color: var(--ink);
  font-family: 'Newsreader', Georgia, serif;
  font-size: 17px;
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
  overflow-x: hidden;
}
.display { font-family: 'Oswald', 'Arial Narrow', sans-serif; }
.mono { font-family: 'IBM Plex Mono', ui-monospace, monospace; }
.page { position: relative; z-index: 1; max-width: 1180px; margin: 0 auto; padding: 0 28px; }
::selection { background: rgba(194, 73, 29, .28); }
a { color: inherit; }
a:focus-visible, button:focus-visible { outline: 2px solid var(--wax); outline-offset: 3px; }
img { user-select: none; }

/* the punctuation square - one wax mark, used sparingly */
.sq { display: inline-block; width: .2em; height: .2em; background: var(--wax); margin-left: .14em; vertical-align: baseline; }

/* ---------- intro animation (once per session) ---------- */
#intro { position: fixed; inset: 0; z-index: 50; background: var(--paper); display: none;
  place-items: center;
  transition: transform .55s cubic-bezier(.7,0,.2,1); will-change: transform; }
#intro.play { display: grid; }
#intro.leaving { transform: translateY(-100%); }
.intro-inner { position: relative; width: min(74vw, 400px); height: min(64vh, 400px); }
.intro-desk { position: absolute; left: 8%; right: 8%; bottom: 56px; height: 1.5px; background: var(--rule-strong);
  transform: scaleX(0); transform-origin: center; animation: deskdraw .5s var(--ease-out) .95s both; }
@keyframes deskdraw { to { transform: scaleX(1); } }
.intro-flight { position: absolute; left: 50%; top: 34%; width: min(60vw, 300px);
  animation: flightin .95s var(--ease-out) .08s both; will-change: transform; }
@keyframes flightin {
  0% { transform: translate(-160%, -120%) rotate(-14deg); opacity: 0; }
  55% { opacity: 1; }
  78% { transform: translate(-50%, -46%) rotate(2.5deg); }
  100% { transform: translate(-50%, -46%) rotate(0deg); opacity: 1; } }
.intro-magpie { width: 100%; display: block;
  filter: drop-shadow(0 14px 18px rgba(23,19,12,.22)); }
.intro-letter { position: absolute; left: 50%; bottom: 62px; width: min(46vw, 220px); height: min(30vw, 138px);
  background: var(--card); border: 1px solid var(--rule-strong);
  box-shadow: 0 2px 0 rgba(23,19,12,.08), 0 18px 30px -16px rgba(23,19,12,.4);
  animation: letterdrop .6s var(--ease-spring) .8s both; will-change: transform; }
.intro-letter::before { content: ""; position: absolute; inset: 7px; border: 1px solid var(--rule); }
@keyframes letterdrop {
  0% { transform: translate(-50%, -120px); opacity: 0; }
  60% { opacity: 1; }
  100% { transform: translate(-50%, 0); opacity: 1; } }
.intro-seal { position: absolute; right: -24px; bottom: -24px; width: min(19vw, 92px);
  animation: introstamp .5s var(--ease-spring) 1.3s both; }
@keyframes introstamp { 0% { opacity: 0; transform: scale(2.2) rotate(16deg); }
  55% { opacity: 1; transform: scale(.9) rotate(4deg); }
  75% { transform: scale(1.06) rotate(10deg); } 100% { opacity: 1; transform: scale(1) rotate(8deg); } }
.intro-ring { position: absolute; right: -24px; bottom: -24px; width: min(19vw, 92px); aspect-ratio: 1;
  border: 2px solid var(--wax); border-radius: 50%; opacity: 0;
  animation: sealring .55s var(--ease-out) 1.42s both; }
@keyframes sealring { 0% { opacity: .85; transform: scale(.8); } 100% { opacity: 0; transform: scale(2); } }
.intro-skip { position: absolute; bottom: 26px; left: 50%; transform: translateX(-50%);
  font-size: 11px; letter-spacing: .14em; text-transform: uppercase; color: var(--ink-35); }
@media (prefers-reduced-motion: reduce) { #intro.play { display: none; } }

/* ---------- load choreography ---------- */
.rise { opacity: 0; transform: translateY(16px); }
body.ready .rise { opacity: 1; transform: none; transition: opacity .7s var(--ease-out), transform .7s var(--ease-out); }
body.ready .rise.d1 { transition-delay: .04s } body.ready .rise.d2 { transition-delay: .14s }
body.ready .rise.d3 { transition-delay: .24s } body.ready .rise.d4 { transition-delay: .34s }
body.ready .rise.d5 { transition-delay: .44s } body.ready .rise.d6 { transition-delay: .56s }
.kicker-line { display: inline-block; width: 0; height: 1px; background: var(--wax); vertical-align: middle; margin-right: 10px; transition: width .7s var(--ease-out) .3s; }
body.ready .kicker-line { width: 34px; }

/* ---------- header ---------- */
header {
  display: flex; align-items: center; justify-content: space-between; gap: 20px;
  padding: 18px 0 16px; border-bottom: 1px solid var(--rule-strong);
}
.brand { display: flex; align-items: center; gap: 12px; }
.brand img { width: 40px; height: 40px; transition: transform .4s var(--ease-spring); }
.brand:hover img { transform: rotate(-6deg) scale(1.06); }
.brand .word { font-family: 'Oswald', sans-serif; font-weight: 600; font-size: 24px; letter-spacing: .14em; text-transform: uppercase; }
header nav { display: flex; gap: 30px; font-size: 11.5px; letter-spacing: .16em; text-transform: uppercase; }
header nav a { text-decoration: none; color: var(--ink-70); position: relative; padding: 4px 0; }
header nav a::after { content: ""; position: absolute; left: 0; bottom: 0; height: 1px; width: 100%; background: var(--wax);
  transform: scaleX(0); transform-origin: left; transition: transform .3s var(--ease-out); }
header nav a:hover { color: var(--ink); }
header nav a:hover::after { transform: scaleX(1); }
.head-cta { font-family: 'IBM Plex Mono', monospace; font-size: 11px; letter-spacing: .12em; text-transform: uppercase;
  text-decoration: none; background: var(--wax); color: var(--paper); padding: 9px 16px; transition: background .25s, color .25s; }
.head-cta:hover { background: var(--ink); color: var(--paper); }
@media (max-width: 860px) { header nav { display: none; } }

/* ---------- hero ---------- */
.hero { display: grid; grid-template-columns: 7fr 5fr; gap: 64px; align-items: center; padding: 84px 0 64px; }
@media (max-width: 860px) { .hero { grid-template-columns: 1fr; gap: 44px; padding: 52px 0 44px; } }
.kicker { font-family: 'IBM Plex Mono', monospace; font-size: 11.5px; letter-spacing: .18em; text-transform: uppercase; color: var(--ink-70); }
h1 {
  font-family: 'Oswald', sans-serif; font-weight: 500; text-transform: uppercase;
  font-size: clamp(52px, 8vw, 106px); line-height: .98; letter-spacing: -0.005em;
  margin: 22px 0 26px;
}
h1 em { font-family: 'Newsreader', serif; font-style: italic; font-weight: 400; text-transform: none; letter-spacing: -0.02em; color: var(--wax); }
h1 .wm { display: inline-block; overflow: hidden; vertical-align: bottom; padding-bottom: .09em; margin-bottom: -.09em; }
h1 .w { display: inline-block; transform: translateY(115%); transition: transform .85s var(--ease-out); will-change: transform; }
body.ready h1 .w { transform: none; }
.lede { font-size: 20px; line-height: 1.55; color: var(--ink-70); max-width: 34em; }
.cta { display: flex; flex-wrap: wrap; gap: 14px; margin-top: 34px; }
.btn { font-family: 'IBM Plex Mono', monospace; font-size: 12.5px; letter-spacing: .1em; text-transform: uppercase;
  text-decoration: none; padding: 15px 24px; border: 1px solid var(--ink); display: inline-block;
  transition: background .25s, color .25s, border-color .25s; will-change: transform; }
.btn.primary { background: var(--ink); color: var(--paper); }
.btn.primary:hover { background: var(--wax); border-color: var(--wax); color: var(--paper); }
.btn.ghost { color: var(--ink); }
.btn.ghost:hover { background: var(--ink); color: var(--paper); }
.micro { font-family: 'IBM Plex Mono', monospace; font-size: 11px; letter-spacing: .14em; text-transform: uppercase; color: var(--ink-35); margin-top: 26px; }
.hero figure { position: relative; border: 1px solid var(--rule-strong); background: var(--card); padding: 10px; will-change: transform; }
.hero figure img { display: block; width: 100%; }
.hero figure .seal { position: absolute; top: -26px; right: -22px; width: 76px; transform: rotate(9deg);
  filter: drop-shadow(0 4px 6px rgba(23,19,12,.25)); }
.hero figcaption { display: flex; justify-content: space-between; gap: 12px;
  font-family: 'IBM Plex Mono', monospace; font-size: 10.5px; letter-spacing: .14em; text-transform: uppercase;
  color: var(--ink-55); padding-top: 12px; }

/* ---------- ticker ---------- */
.ticker { border-top: 1px solid var(--rule-strong); border-bottom: 1px solid var(--rule-strong); overflow: hidden; padding: 13px 0; }
.ticker-track { display: flex; width: max-content; animation: tick 38s linear infinite; }
.tick-group { display: flex; align-items: center; flex-shrink: 0; }
.tick-item { font-family: 'IBM Plex Mono', monospace; font-size: 11.5px; letter-spacing: .18em; text-transform: uppercase; color: var(--ink-70); white-space: nowrap; }
.tick-sq { width: 7px; height: 7px; background: var(--wax); margin: 0 26px; flex-shrink: 0; }
@keyframes tick { to { transform: translateX(-50%); } }
@media (prefers-reduced-motion: reduce) { .ticker-track { animation: none; } }

/* ---------- sections ---------- */
section { padding: 92px 0 8px; }
.mast { display: flex; justify-content: space-between; align-items: baseline; gap: 16px;
  border-top: 1px solid var(--rule-strong); padding-top: 14px;
  font-family: 'IBM Plex Mono', monospace; font-size: 11px; letter-spacing: .18em; text-transform: uppercase; color: var(--ink-55); }
.mast .r { color: var(--ink-35); }
h2 { font-family: 'Oswald', sans-serif; font-weight: 500; text-transform: uppercase;
  font-size: clamp(32px, 4.4vw, 54px); line-height: 1.04; letter-spacing: -0.005em; margin: 30px 0 18px; }
h2 .lr { display: block; overflow: hidden; }
h2 .lr > * , h2 .lr { transform-origin: left bottom; }
section h2 .lr { animation: none; }
h2 em { font-family: 'Newsreader', serif; font-style: italic; font-weight: 400; text-transform: none; color: var(--wax); }
.sec-lede { font-size: 19px; color: var(--ink-70); max-width: 36em; }

/* line reveal for h2 lines */
h2 .lr { position: relative; }
h2 .lr { clip-path: inset(0 0 0 0); }

/* numbered rows */
.rows { margin-top: 52px; border-top: 1px solid var(--rule); }
.row2 { display: grid; grid-template-columns: 100px 1fr 1.1fr; gap: 28px; align-items: baseline;
  padding: 26px 8px; border-bottom: 1px solid var(--rule); transition: background .3s; }
.row2:hover { background: rgba(23,19,12,.035); }
.row2 .idx { font-family: 'Oswald', sans-serif; font-weight: 500; font-size: 40px; color: var(--ink-35); transition: color .3s; }
.row2:hover .idx { color: var(--wax); }
.row2 h3 { font-family: 'Oswald', sans-serif; font-weight: 500; font-size: 26px; text-transform: uppercase; letter-spacing: .01em; }
.row2 .body p { font-size: 16.5px; color: var(--ink-70); }
.row2 .body .meta { font-family: 'IBM Plex Mono', monospace; font-size: 10.5px; letter-spacing: .16em; text-transform: uppercase; color: var(--ink-35); margin-top: 10px; }
@media (max-width: 860px) { .row2 { grid-template-columns: 56px 1fr; } .row2 .body { grid-column: 2; } .row2 .idx { font-size: 28px; } }

/* ---------- the morning letter ---------- */
.letter-wrap { display: grid; grid-template-columns: 5fr 7fr; gap: 56px; margin-top: 52px; align-items: start; }
@media (max-width: 860px) { .letter-wrap { grid-template-columns: 1fr; gap: 40px; } }
.rule-note { border-top: 1px solid var(--rule-strong); padding: 16px 0 20px; }
.rule-note b { display: block; font-family: 'IBM Plex Mono', monospace; font-weight: 500; font-size: 11px; letter-spacing: .16em; text-transform: uppercase; margin-bottom: 8px; }
.rule-note b::before { content: ""; display: inline-block; width: 7px; height: 7px; background: var(--wax); margin-right: 10px; }
.rule-note p { font-size: 16.5px; color: var(--ink-70); }
.letter { position: relative; background: var(--card); border: 1px solid var(--rule-strong);
  box-shadow: 10px 10px 0 rgba(23,19,12,.06); padding: 30px 34px 26px; }
.letter .lh { display: flex; justify-content: space-between; align-items: baseline; gap: 12px; flex-wrap: wrap;
  border-bottom: 3px double var(--rule-strong); padding-bottom: 12px; }
.letter .lh .t { font-family: 'Oswald', sans-serif; font-weight: 600; font-size: 19px; letter-spacing: .06em; text-transform: uppercase; }
.letter .lh .d { font-family: 'IBM Plex Mono', monospace; font-size: 10.5px; letter-spacing: .14em; text-transform: uppercase; color: var(--ink-55); }
.letter .salut { font-style: italic; font-size: 18px; color: var(--ink-70); padding: 16px 0 6px; }
.letter .sec-h { display: flex; align-items: center; gap: 14px;
  font-family: 'IBM Plex Mono', monospace; font-size: 10.5px; letter-spacing: .18em; text-transform: uppercase; color: var(--ink-55);
  margin: 22px 0 12px; }
.letter .sec-h::after { content: ""; flex: 1; height: 1px; background: var(--rule); }
.letter .item { padding: 12px 0; border-bottom: 1px solid var(--rule); }
.letter .item:last-of-type { border-bottom: 0; }
.letter .item b { display: block; font-weight: 500; font-size: 17px; }
.letter .item small { display: block; font-size: 15px; color: var(--ink-70); margin-top: 2px; }
.letter .item .u { display: block; font-family: 'IBM Plex Mono', monospace; font-size: 10.5px; letter-spacing: .1em; text-transform: uppercase; color: var(--ink-35); margin-top: 6px; }
.letter .job { display: grid; grid-template-columns: 1fr auto; gap: 4px 16px; padding: 13px 0; border-bottom: 1px solid var(--rule); align-items: baseline; }
.letter .job .role { font-weight: 500; font-size: 16.5px; }
.letter .job .co { font-family: 'IBM Plex Mono', monospace; font-size: 11px; letter-spacing: .08em; text-transform: uppercase; color: var(--ink-55); }
.letter .job .pay { font-family: 'IBM Plex Mono', monospace; font-size: 12px; text-align: right; }
.letter .job .by { font-family: 'IBM Plex Mono', monospace; font-size: 10.5px; letter-spacing: .1em; text-transform: uppercase; color: var(--ink-35); text-align: right; }
.letter .job .new { display: inline-block; background: var(--wax); color: var(--paper);
  font-family: 'IBM Plex Mono', monospace; font-size: 9.5px; letter-spacing: .14em; text-transform: uppercase;
  padding: 3px 7px; margin-left: 8px; vertical-align: 2px; }
.letter .job .co { margin-left: 6px; }
@media (max-width: 720px) {
  .letter { padding: 22px 20px 20px; box-shadow: 5px 5px 0 rgba(23,19,12,.06); }
  .letter .job { grid-template-columns: 1fr; gap: 3px; }
  .letter .job .co { display: block; margin: 4px 0 0; }
  .letter .job .pay, .letter .job .by { text-align: left; }
  .letter .job .new { margin-left: 0; margin-top: 6px; }
  .letter .sign { padding-right: 76px; }
  .mast { flex-wrap: wrap; gap: 4px 16px; }
}
.letter .sign { font-style: italic; font-size: 17px; color: var(--ink-70); margin-top: 18px; padding-right: 90px; }
.letter .seal { position: absolute; right: 22px; bottom: 18px; width: 82px; transform: rotate(8deg);
  mix-blend-mode: multiply; filter: drop-shadow(0 3px 4px rgba(23,19,12,.2)); }
/* letter reveal choreography */
.letter .item, .letter .job, .letter .salut, .letter .sign { opacity: 0; transform: translateY(12px); }
.letter.in .item, .letter.in .job, .letter.in .salut, .letter.in .sign {
  opacity: 1; transform: none; transition: opacity .6s var(--ease-out), transform .6s var(--ease-out); }
.letter.in .salut { transition-delay: .1s }
.letter.in .item:nth-of-type(1) { transition-delay: .18s } .letter.in .item:nth-of-type(2) { transition-delay: .26s }
.letter.in .job:nth-of-type(1) { transition-delay: .34s } .letter.in .job:nth-of-type(2) { transition-delay: .42s }
.letter.in .sign { transition-delay: .5s }
.letter .seal { opacity: 0; transform: scale(2) rotate(18deg); }
.letter.in .seal { opacity: 1; transform: scale(1) rotate(8deg); transition: opacity .45s var(--ease-spring) .55s, transform .45s var(--ease-spring) .55s; }

/* ---------- spec table ---------- */
.spec { margin-top: 52px; border-top: 1px solid var(--rule); }
.spec .row { display: grid; grid-template-columns: 200px 1fr auto; gap: 24px; align-items: baseline;
  padding: 20px 8px; border-bottom: 1px solid var(--rule); transition: background .3s; }
.spec .row:hover { background: rgba(23,19,12,.035); }
.spec .k { font-family: 'IBM Plex Mono', monospace; font-size: 11px; letter-spacing: .18em; text-transform: uppercase; color: var(--ink-55); }
.spec .v { font-size: 17.5px; color: var(--ink-70); }
.spec .v b { font-family: 'Oswald', sans-serif; font-weight: 500; font-size: 19px; text-transform: uppercase; color: var(--ink); letter-spacing: .01em; }
.spec .c { font-family: 'IBM Plex Mono', monospace; font-size: 11px; letter-spacing: .1em; text-transform: uppercase; color: var(--ink-35); }
@media (max-width: 720px) { .spec .row { grid-template-columns: 1fr; gap: 6px; } }
.margin-note { font-family: 'IBM Plex Mono', monospace; font-size: 11px; letter-spacing: .14em; text-transform: uppercase; color: var(--ink-35); margin-top: 22px; }

/* ---------- self-host ---------- */
.self-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 56px; margin-top: 40px; align-items: start; }
@media (max-width: 860px) { .self-grid { grid-template-columns: 1fr; gap: 36px; } }
.self-grid p.copy { font-size: 18px; color: var(--ink-70); max-width: 30em; }
.code { background: var(--ink); color: var(--paper); padding: 24px 26px;
  font-family: 'IBM Plex Mono', monospace; font-size: 13.5px; line-height: 2; overflow-x: auto; }
.code .p { color: var(--wax); }
.code .c { color: rgba(248,245,238,.45); }
.code-cap { font-family: 'IBM Plex Mono', monospace; font-size: 10.5px; letter-spacing: .16em; text-transform: uppercase; color: var(--ink-35); margin-top: 12px; }

/* ---------- closing band + footer ---------- */
.band { margin-top: 110px; background: var(--ink); color: var(--paper); }
.band-inner { max-width: 1180px; margin: 0 auto; padding: 96px 28px 0; text-align: center; }
.band h2 { color: var(--paper); margin: 0 0 30px; font-size: clamp(44px, 7vw, 96px); }
.band .sq { width: .22em; height: .22em; }
.band .btn.light { background: var(--paper); color: var(--ink); border-color: var(--paper); }
.band .btn.light:hover { background: var(--wax); border-color: var(--wax); color: var(--paper); }
.band .btn.ghostd { background: transparent; color: var(--paper); border-color: rgba(248,245,238,.4); }
.band .btn.ghostd:hover { border-color: var(--paper); }
.band .quip { font-style: italic; font-size: 17px; color: rgba(248,245,238,.55); margin-top: 44px; }
.band footer { margin-top: 72px; border-top: 1px solid rgba(248,245,238,.22); padding: 24px 0 26px;
  display: flex; justify-content: space-between; gap: 14px; flex-wrap: wrap; text-align: left;
  font-family: 'IBM Plex Mono', monospace; font-size: 10.5px; letter-spacing: .14em; text-transform: uppercase; color: rgba(248,245,238,.5); }
.band footer a { color: rgba(248,245,238,.75); text-decoration: none; }
.band footer a:hover { color: var(--paper); }
@media (max-width: 720px) { .band footer { flex-direction: column; gap: 8px; } }

/* ---------- reveals ---------- */
.reveal { opacity: 0; transform: translateY(22px); }
.reveal.in { opacity: 1; transform: none; transition: opacity .75s var(--ease-out), transform .75s var(--ease-out); }
.rows .row2.reveal.in:nth-child(1) { transition-delay: .05s } .rows .row2.reveal.in:nth-child(2) { transition-delay: .15s }
.rows .row2.reveal.in:nth-child(3) { transition-delay: .25s }
.spec .row.reveal.in:nth-child(1) { transition-delay: .05s } .spec .row.reveal.in:nth-child(2) { transition-delay: .13s }
.spec .row.reveal.in:nth-child(3) { transition-delay: .21s } .spec .row.reveal.in:nth-child(4) { transition-delay: .29s }
h2 .lr { transition: none; }
section h2 .lr { opacity: 0; transform: translateY(60%); display: block; }
section h2.in .lr { opacity: 1; transform: none; transition: opacity .8s var(--ease-out), transform .8s var(--ease-out); }
section h2.in .lr:nth-child(2) { transition-delay: .12s }

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: .01ms !important; transition-duration: .01ms !important; }
  .rise, h1 .w, .reveal, .letter .item, .letter .job, .letter .salut, .letter .sign, .letter .seal, section h2 .lr { opacity: 1 !important; transform: none !important; }
  .kicker-line { width: 34px !important; }
}
</style>
</head>
<body>
<div id="intro" aria-hidden="true">
  <div class="intro-inner">
    <div class="intro-flight"><img class="intro-magpie" src="__BRAND__/magpie.jpg" alt=""></div>
    <div class="intro-letter"><div class="intro-ring"></div><img class="intro-seal" src="__BRAND__/seal.png" alt=""></div>
    <div class="intro-desk"></div>
  </div>
  <div class="intro-skip mono">tap to skip</div>
</div>
<div class="page">

<header>
  <div class="brand rise d1">
    <img src="__BRAND__/mark.png" alt="Nook logo - an n formed by a stack of clippings, a magpie perched on top">
    <span class="word">Nook</span>
  </div>
  <nav class="mono rise d1">
    <a href="#how">How it works</a>
    <a href="#letter">The letter</a>
    <a href="#stack">The stack</a>
    <a href="#selfhost">Self-host</a>
  </nav>
  <a class="head-cta rise d1" href="/app">Open app</a>
</header>

<div class="hero">
  <div>
    <div class="kicker rise d2"><span class="kicker-line"></span>Read-it-later + job digest · a Telegram bot</div>
    <h1 aria-label="Save everything. Read what matters.">Save everything.<br>Read what <em>matters</em><span class="sq" aria-hidden="true"></span></h1>
    <p class="lede rise d4">Nook is a Telegram bot with a magpie's habits. Toss it a link any time; it fetches, summarizes and files each one. At 08:00 sharp you get one sealed letter: what you saved, what it says, and which paid openings are worth your morning.</p>
    <div class="cta rise d5">
      <a class="btn primary" href="https://t.me/Nook_digest_bot">Talk to @Nook_digest_bot</a>
      <a class="btn ghost" href="/app">Enter the web app</a>
    </div>
    <p class="micro rise d6">Cloudflare free tier · no server · no docker · no bill</p>
  </div>
  <figure class="rise d3">
    <img class="seal" src="__BRAND__/seal.png" alt="">
    <img id="magpie" src="__BRAND__/magpie.jpg" alt="Ink illustration of a magpie perched on a stack of sealed letters">
    <figcaption><span>Fig. 01</span><span>Pica pica, keeper of links</span></figcaption>
  </figure>
</div>
</div>

<div class="ticker" aria-hidden="true">
  <div class="ticker-track">
    <div class="tick-group">
      <span class="tick-item">Toss it a link</span><span class="tick-sq"></span>
      <span class="tick-item">Fetched at the edge</span><span class="tick-sq"></span>
      <span class="tick-item">Summarized + tagged</span><span class="tick-sq"></span>
      <span class="tick-item">One letter at 08:00</span><span class="tick-sq"></span>
      <span class="tick-item">Paid openings only</span><span class="tick-sq"></span>
      <span class="tick-item">Never the same opening twice</span><span class="tick-sq"></span>
    </div>
    <div class="tick-group">
      <span class="tick-item">Toss it a link</span><span class="tick-sq"></span>
      <span class="tick-item">Fetched at the edge</span><span class="tick-sq"></span>
      <span class="tick-item">Summarized + tagged</span><span class="tick-sq"></span>
      <span class="tick-item">One letter at 08:00</span><span class="tick-sq"></span>
      <span class="tick-item">Paid openings only</span><span class="tick-sq"></span>
      <span class="tick-item">Never the same opening twice</span><span class="tick-sq"></span>
    </div>
  </div>
</div>

<div class="page">

<section id="how">
  <div class="mast"><span>01 · How it works</span><span class="r">The collector</span></div>
  <h2>Magpies hoard shiny things.<br>Yours hoards <em>links</em>.</h2>
  <div class="rows">
    <div class="row2 reveal">
      <div class="idx">01</div>
      <h3>Send anything</h3>
      <div class="body">
        <p>A link, or a thought with /note. The page is fetched at the edge, an LLM writes a two-sentence summary with tags, and it lands on your shelf.</p>
        <div class="meta">Webhook · secret-verified</div>
      </div>
    </div>
    <div class="row2 reveal">
      <div class="idx">02</div>
      <h3>Ask it back</h3>
      <div class="body">
        <p>Plain questions search your whole nook with BM25 and answer with cited sources. Send the same link twice and it is recognized, not re-filed.</p>
        <div class="meta">D1 + FTS5 · sha256 dedup</div>
      </div>
    </div>
    <div class="row2 reveal">
      <div class="idx">03</div>
      <h3>Forget on command</h3>
      <div class="body">
        <p>/list shows recent saves, /forget removes one. The database lives in your own Cloudflare account; your clippings never sit on anyone else's shelf.</p>
        <div class="meta">Your account · your data</div>
      </div>
    </div>
  </div>
</section>

<section id="letter">
  <div class="mast"><span>02 · The morning letter</span><span class="r">Sealed · delivered once</span></div>
  <h2>One sealed digest,<br>08:00 <em>sharp</em>.</h2>
  <div class="letter-wrap">
    <div>
      <div class="rule-note reveal"><b>Reads first</b><p>Whatever you saved and never opened rides at the top, one line of summary each, source attached.</p></div>
      <div class="rule-note reveal"><b>Then openings</b><p>Job boards are queried at send time, not cached overnight. If a listing is dead by morning, it never reaches you.</p></div>
      <div class="rule-note reveal"><b>Exactly once</b><p>Every opening is hashed against your history. The letter never repeats itself.</p></div>
    </div>
    <div class="letter" id="letter">
      <div class="lh"><span class="t">Nook · The Morning Letter</span><span class="d">No. 214 · Fri 24 Oct · 08:00 IST</span></div>
      <p class="salut">Good morning. Three reads you filed, two openings worth your first coffee.</p>
      <div class="sec-h">In your nook · 3 unread</div>
      <div class="item"><b>Vector indexes, explained simply</b><small>Why HNSW wins at recall per millisecond, in pictures.</small><span class="u">simonwillison.net · 12 min · #vectors</span></div>
      <div class="item"><b>The $0 LLM stack</b><small>Free tiers compared honestly: what breaks first and when.</small><span class="u">github.com · 8 min · #infra</span></div>
      <div class="sec-h">Fresh openings · paid, checked at send</div>
      <div class="job"><div><span class="role">Python Development Intern</span> <span class="co">Digitap.ai · Bengaluru</span><span class="new">New</span></div><div class="pay">₹15-18k/mo</div><div class="by">Apply by 12 Nov</div></div>
      <div class="job"><div><span class="role">Junior Backend Engineer</span> <span class="co">Northwind · Remote</span></div><div class="pay">₹6-9 LPA</div><div class="by">Apply by 30 Oct</div></div>
      <p class="sign">your magpie,</p>
      <img class="seal" src="__BRAND__/seal.png" alt="A wax seal stamped with an N">
    </div>
  </div>
</section>

<section id="stack">
  <div class="mast"><span>03 · Under the feathers</span><span class="r">One worker · four free services</span></div>
  <h2>Zero servers,<br>zero <em>maintenance</em>.</h2>
  <div class="spec">
    <div class="row reveal"><span class="k">Telegram</span><span class="v"><b>Webhook in, letter out.</b> HMAC secret checked on every call; forged updates are dropped unread.</span><span class="c">@Nook_digest_bot</span></div>
    <div class="row reveal"><span class="k">Workers AI</span><span class="v"><b>Summaries, tags, answers.</b> Llama 3.1 at the edge, no API key, no quota anxiety.</span><span class="c">Free tier</span></div>
    <div class="row reveal"><span class="k">D1 + FTS5</span><span class="v"><b>Your shelf.</b> SQLite with BM25 full-text search and sha256 dedup.</span><span class="c">Your account</span></div>
    <div class="row reveal"><span class="k">Cron</span><span class="v"><b>The 08:00 alarm.</b> One trigger, one letter, then silence for 24 hours.</span><span class="c">30 2 * * *</span></div>
  </div>
  <p class="margin-note reveal">67 unit tests · CI on every push</p>
</section>

<section id="selfhost">
  <div class="mast"><span>04 · Keep your own magpie</span><span class="r">MIT · self-hosted</span></div>
  <h2>Deploy your own<br>in five <em>minutes</em>.</h2>
  <div class="self-grid">
    <div>
      <p class="copy">Ask BotFather for a token, fork the repo, create one D1 database, set two secrets, deploy. Keywords, digest hour and allow-list are yours to tune. The webhook registers itself.</p>
      <div class="cta">
        <a class="btn primary" href="https://github.com/Prajit-22/nook">Fork on GitHub</a>
        <a class="btn ghost" href="https://deploy.workers.cloudflare.com/?url=https://github.com/Prajit-22/nook">Deploy to Cloudflare</a>
      </div>
    </div>
    <div class="reveal">
      <div class="code"><span class="p">$</span> git clone github.com/Prajit-22/nook<br><span class="p">$</span> wrangler d1 create nook-db<br><span class="p">$</span> wrangler deploy<br><span class="c"># the webhook registers itself</span></div>
      <div class="code-cap">Three commands · your account · your data</div>
    </div>
  </div>
</section>

</div>

<div class="band">
  <div class="band-inner">
    <h2>Stop skimming.<br>Start keeping<span class="sq" aria-hidden="true"></span></h2>
    <div class="cta" style="justify-content:center">
      <a class="btn light" href="https://t.me/Nook_digest_bot">Open @Nook_digest_bot</a>
      <a class="btn ghostd" href="https://github.com/Prajit-22/nook">Star on GitHub</a>
    </div>
    <p class="quip">No magpies were rushed in the making of your digest.</p>
    <footer>
      <span>Nook · a magpie for your links</span>
      <span>Set in Oswald, Newsreader + Plex Mono</span>
      <span><a href="https://github.com/Prajit-22/nook">Prajit-22/nook</a> · MIT · © 2026</span>
    </footer>
  </div>
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
  var d = { value: 0.12 };
  var frag = walk(h1, d);
  h1.textContent = '';
  frag.forEach(function (c) { h1.appendChild(c); });
  /* mask-wrap each word so it rises out of a clipped window */
  Array.prototype.slice.call(h1.querySelectorAll('.w')).forEach(function (w) {
    var m = document.createElement('span');
    m.className = 'wm';
    w.parentNode.insertBefore(m, w);
    m.appendChild(w);
  });

  /* section headers reveal line by line */
  document.querySelectorAll('section h2').forEach(function (h) {
    h.innerHTML = h.innerHTML.split(/<br\s*\/?>/i).map(function (line) {
      return '<span class="lr">' + line + '</span>';
    }).join('');
  });

  /* intro: once per session, skippable, assets preloaded, hero waits for it */
  var intro = document.getElementById('intro');
  var forceIntro = new URLSearchParams(location.search).has('intro');
  var seenIntro = sessionStorage.getItem('nook-intro-seen');
  function readyUp() { document.body.classList.add('ready'); }
  function dismissIntro() {
    if (!intro.classList.contains('play')) return;
    intro.classList.add('leaving');
    sessionStorage.setItem('nook-intro-seen', '1');
    setTimeout(function () { intro.style.display = 'none'; }, 600);
    readyUp();
  }
  function playIntro() {
    var imgs = Array.prototype.slice.call(intro.querySelectorAll('img'));
    var loaded = Promise.all(imgs.map(function (im) {
      return im.complete ? 1 : new Promise(function (res) {
        im.onload = im.onerror = res;
      });
    }));
    Promise.race([loaded, new Promise(function (res) { setTimeout(res, 700); })]).then(function () {
      intro.classList.add('play');
      setTimeout(dismissIntro, 2900);
    });
  }
  if (!reduced && (forceIntro || !seenIntro)) {
    playIntro();
  } else {
    readyUp();
  }
  intro.addEventListener('click', dismissIntro);
  /* logo click replays the intro */
  var brandImg = document.querySelector('.brand img');
  if (brandImg) {
    brandImg.style.cursor = 'pointer';
    brandImg.title = 'replay the intro';
    brandImg.addEventListener('click', function () {
      if (reduced) return;
      intro.style.display = 'grid';
      intro.classList.remove('leaving');
      intro.querySelectorAll('.intro-flight, .intro-letter, .intro-seal, .intro-ring, .intro-desk').forEach(function (el) {
        el.style.animation = 'none';
        void el.offsetWidth;
        el.style.animation = '';
      });
      intro.classList.add('play');
      setTimeout(dismissIntro, 2900);
    });
  }

  /* scroll reveals - a sweep that catches jump-scrolls */
  var sweepTargets = Array.prototype.slice.call(document.querySelectorAll('.reveal, .letter, section h2'));
  function sweep() {
    var vh = window.innerHeight;
    sweepTargets = sweepTargets.filter(function (el) {
      var r = el.getBoundingClientRect();
      if (r.top < vh * 0.92 && r.bottom > -40) { el.classList.add('in'); return false; }
      if (r.bottom <= -40) { el.classList.add('in'); return false; }
      return true;
    });
  }
  sweep();
  window.addEventListener('scroll', sweep, { passive: true });
  window.addEventListener('resize', sweep, { passive: true });

  /* magnetic buttons (desktop pointers only) */
  if (!reduced && window.matchMedia('(pointer: fine)').matches) {
    document.querySelectorAll('.btn').forEach(function (b) {
      b.classList.add('magnet');
      b.addEventListener('mousemove', function (e) {
        var r = b.getBoundingClientRect();
        var dx = (e.clientX - r.left - r.width / 2) / (r.width / 2);
        var dy = (e.clientY - r.top - r.height / 2) / (r.height / 2);
        b.style.transform = 'translate(' + (dx * 5) + 'px,' + (dy * 4) + 'px)';
      });
      b.addEventListener('mouseleave', function () { b.style.transform = ''; });
    });
  }

  /* hero illustration: gentle scroll parallax */
  var heroFig = document.querySelector('.hero figure');
  if (!reduced && heroFig) {
    var figTick = false;
    window.addEventListener('scroll', function () {
      if (figTick) return;
      figTick = true;
      requestAnimationFrame(function () {
        var r = heroFig.getBoundingClientRect();
        if (r.bottom > 0 && r.top < window.innerHeight) {
          var p = (window.innerHeight / 2 - (r.top + r.height / 2)) / window.innerHeight;
          heroFig.style.transform = 'translateY(' + (p * -22) + 'px)';
        }
        figTick = false;
      });
    }, { passive: true });
  }

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
body { background: #F8F5EE; color: #17130C; font-family: 'Newsreader', Georgia, serif; display: grid; place-items: center; min-height: 100vh; margin: 0; text-align: center; }
h1 { font-family: 'Oswald', 'Arial Narrow', sans-serif; font-weight: 500; text-transform: uppercase; font-size: clamp(40px, 8vw, 72px); margin: 18px 0 10px; }
p { color: rgba(23,19,12,.7); font-size: 18px; }
a { color: #17130C; font-family: 'IBM Plex Mono', monospace; font-size: 14px; }
img { width: 84px; }
.num { font-family: 'IBM Plex Mono', monospace; font-size: 13px; letter-spacing: .2em; color: #C2491D; }
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
