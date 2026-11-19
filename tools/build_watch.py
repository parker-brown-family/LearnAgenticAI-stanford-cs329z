#!/usr/bin/env python3
"""Write media/watch.src.html: the clips as a library to post from, every clip a card that takes notes.

Laid out to the Cinema Delight library's standard (its index.html, built by cinema-delight/tools/index.py): one card
per clip with its facts, a player, and the buttons that get a file onto a social site: ▶ Omarchy (play outside the
browser), ⇱ drag (a real file at the pointer, to drop into X), path (copy, then Ctrl+L in an upload dialog), note,
source. Filters and search sit in a bar at the top, and stars persist in this browser. The ▶ and ⇱ buttons ask
Cinema Delight's drag helper (cinema-delight/tools/dragd.py, the cinema-drag user service), which only hands out files
inside its own folders; so each clip is hard-linked into ~/.local/share/cinema-delight/shared/ (no second copy on
disk), and the page carries the helper's token. The look and the reader notes come from the briefing build, so every
card is its own commentable section. Build:

    python3 -I tools/build_watch.py
    python3 ~/.claude/skills/briefing/scripts/brief.py html media/watch.src.html media/watch.html
"""
import html, json, os, re, subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
MEDIA = HERE / "media"
CLIPS = MEDIA / "clips"
SHARED = Path.home() / ".local/share/cinema-delight/shared/learnagenticai-cs329z"
TOKEN = Path.home() / ".cache/cinema-delight/index/drag-token"
X_FREE_S = 140           # X's longest video for an account without Premium, 2:20
SMALL_MB = 100           # the Cinema Delight library's "shareable" line

def secs(t):
    m, s = t.split(":"); return int(m) * 60 + int(float(s))

def slug(title):
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:60].rstrip("-")

def e(s):
    return html.escape(str(s), quote=True)

def mmss(s):
    s = int(round(s)); return f"{s // 60}:{s % 60:02d}"

def probe(p):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                          "stream=width,height:format=duration", "-of", "json", str(p)], capture_output=True, text=True).stdout
    j = json.loads(out)
    st = (j.get("streams") or [{}])[0]
    return float(j["format"]["duration"]), st.get("width"), st.get("height")

def link(mp4):
    """Hard-link a clip where the drag helper will hand it out; re-link if the clip was re-cut since."""
    SHARED.mkdir(parents=True, exist_ok=True)
    dst = SHARED / mp4.name
    if dst.exists() and dst.stat().st_ino != mp4.stat().st_ino:
        dst.unlink()
    if not dst.exists():
        os.link(mp4, dst)
    return dst

def transcript(note):
    t = note.read_text() if note.exists() else ""
    return t.split("--- transcript ---", 1)[1].strip() if "--- transcript ---" in t else ""

def main():
    cuts = json.loads((HERE / "cuts.json").read_text())
    lectures = sorted(json.loads((HERE / "lectures.json").read_text()),
                      key=lambda l: (l["course_order"] == "guest", 0 if l["course_order"] == "guest" else l["course_order"]))
    token = TOKEN.read_text().strip() if TOKEN.exists() else ""
    cards, n_must, n_x, n_small, total = {}, 0, 0, 0, 0.0
    for c in cuts:
        name = f"{c['id']}-{slug(c['title'])}"
        mp4 = CLIPS / f"{name}.mp4"
        if not mp4.exists():
            continue
        d, w, h = probe(mp4)
        mb = mp4.stat().st_size / 1e6
        total += d
        fits_x, small = d <= X_FREE_S, mb < SMALL_MB
        n_must += c["priority"] == 1; n_x += fits_x; n_small += small
        cards[c["id"]] = dict(c=c, name=name, mp4=mp4, shared=link(mp4), d=d, w=w, h=h, mb=mb, fits_x=fits_x, small=small,
                              note=CLIPS / "notes" / f"{name}.txt")
    out = [f"""<!doctype html>
<html lang="en"><head><title>CS329Z clips · library</title><!-- briefing: {{"id": "cs329z-watch", "purpose": "summary"}} --><!--BRIEF:head-->
<style>
/* Laid out after the Cinema Delight library (cinema-delight/tools/index.template.html); colours come from the wall. */
.small{{font-size:13px;color:var(--dim)}}
.hudbar{{display:flex;flex-wrap:wrap;gap:8px 10px;align-items:center;margin:14px 0 4px}}
.hudbar input{{flex:1 1 260px;min-width:200px;padding:8px 12px;border-radius:999px;border:1px solid color-mix(in srgb,var(--fg) 25%,transparent);background:color-mix(in srgb,var(--bg0,#000) 55%,transparent);color:var(--fg);font:inherit}}
.pill{{padding:5px 13px;border-radius:999px;border:1px solid color-mix(in srgb,var(--fg) 28%,transparent);background:transparent;color:var(--fg);font:13px var(--mono,monospace);cursor:pointer}}
.pill.on{{background:color-mix(in srgb,var(--acc) 70%,transparent);color:var(--bg0,#000);border-color:transparent}}
.keys{{font:12px var(--mono,monospace);color:var(--dim);margin:2px 0 10px}}
.keys kbd{{border:1px solid color-mix(in srgb,var(--fg) 30%,transparent);border-radius:4px;padding:0 5px}}
.clips{{display:grid;grid-template-columns:repeat(auto-fill,minmax(440px,1fr));gap:16px}}
figure.clip{{margin:0;display:flex;flex-direction:column;gap:7px}}
figure.clip[hidden]{{display:none}}
.c-head{{display:flex;justify-content:space-between;align-items:flex-start;gap:10px}}
.c-title{{font-weight:700;font-size:17px;line-height:1.25}}
.badge{{font:11px var(--mono,monospace);letter-spacing:.08em;padding:2px 8px;border-radius:5px;border:1px solid var(--green,#9ece6a);color:var(--green,#9ece6a);white-space:nowrap}}
.badge.more{{border-color:color-mix(in srgb,var(--fg) 35%,transparent);color:var(--dim)}}
.c-meta{{font:12.5px var(--mono,monospace);color:var(--dim)}}
.c-stats{{font-size:14px}}
.c-stats .ok{{color:var(--green,#9ece6a)}} .c-stats .no{{color:var(--dim)}}
.strip{{display:flex;gap:2px;border-top:2px solid color-mix(in srgb,var(--acc) 55%,transparent)}}
.strip span{{flex:1;font-size:12px;padding:3px 6px;background:color-mix(in srgb,var(--acc) 14%,transparent);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.c-job{{font-size:14px}}
figure.clip video{{width:100%;border-radius:10px;display:block}}
.acts{{display:flex;flex-wrap:wrap;gap:6px}}
.acts button,.acts a{{font:12.5px var(--mono,monospace);padding:3px 10px;border-radius:6px;border:1px solid color-mix(in srgb,var(--fg) 28%,transparent);color:var(--fg);background:transparent;cursor:pointer;text-decoration:none}}
.acts .om{{border-color:var(--green,#9ece6a);color:var(--green,#9ece6a)}}
.acts .dr{{border-color:var(--acc);color:var(--acc)}}
.acts .pin.on{{color:var(--yellow,#e0af68);border-color:var(--yellow,#e0af68)}}
figure.clip details{{border-top:1px dashed color-mix(in srgb,var(--fg) 18%,transparent);padding-top:5px}}
figure.clip summary{{font:12.5px var(--mono,monospace);color:var(--dim);cursor:pointer}}
figure.clip .tx{{font-size:13px;line-height:1.55;max-height:320px;overflow:auto;margin:6px 0 0}}
#toast{{position:fixed;left:50%;bottom:26px;transform:translateX(-50%);padding:9px 16px;border-radius:10px;background:color-mix(in srgb,var(--bg0,#000) 85%,transparent);border:1px solid var(--acc);font:13px var(--mono,monospace);opacity:0;transition:opacity .2s;pointer-events:none;z-index:99}}
#toast.on{{opacity:1}}
</style></head><body>
<!--brief-content-->
<header class="top"><div class="wrap"><div class="eyebrow">LearnAgenticAI · Stanford CS329Z · clip library</div><div class="opening" id="top" data-brief-anchor="top"><h1>61 clips to post with your commentary</h1> <p class="lede">Cut from Stanford's ten public lectures on engineering AI agents, about {round(total / 3600, 1)} hours in all. {n_must} are must-watch. Each card plays the clip, drags it into X, or copies its path for any upload box. Leave a note on any card to re-cut or drop it.</p></div><nav class="sections"></nav></div></header>
<main class="wrap">
<section class="pane"><h2 id="sec-how" data-brief-anchor="sec-how"><span class="n">01</span> Posting a clip</h2>
<p><b>⇱ drag</b> puts the real file at your pointer: drop it straight into X's composer or any upload box. <b>path</b> copies the file's path; in an upload dialog press <kbd>Ctrl</kbd>+<kbd>L</kbd> and paste. <b>▶ Omarchy</b> plays it in the desktop's player. <b>note</b> opens the clip's note, with the link to the original lecture for your post. To record commentary over a clip, add it to OBS as a Media Source beside your camera, or drop it on a Kdenlive timeline and record a voiceover.</p>
<p class="small">{n_x} clips fit X's 2:20 limit for accounts without Premium, and {n_small} are under {SMALL_MB} MB. The ▶ and ⇱ buttons use Cinema Delight's drag helper (<code>systemctl --user start cinema-drag</code> if they do nothing).</p>
<div class="hudbar"><input id="q" type="search" placeholder="search titles, lectures, topics…  ( / )">
<button class="pill on" data-f="all">all {len(cards)}</button><button class="pill" data-f="must">must-watch {n_must}</button><button class="pill" data-f="pinned">☆ pinned</button><button class="pill" data-f="x">fits X ≤2:20 · {n_x}</button><button class="pill" data-f="small">&lt;{SMALL_MB} MB · {n_small}</button></div>
<div class="keys"><kbd>/</kbd> search · <kbd>Esc</kbd> clear · ☆ pin · ⇱ drag into X · copy a path, then <kbd>Ctrl</kbd>+<kbd>L</kbd> in an upload dialog</div></section>
"""]
    n = 2
    for lec in lectures:
        mine = [cards[c["id"]] for c in cuts if c["lecture"] == lec["n"] and c["id"] in cards]
        if not mine:
            continue
        sec = f"sec-{mine[0]['c']['id'].split('-')[0].lower()}"
        out.append(f"""<section class="pane lec"><h2 id="{sec}" data-brief-anchor="{sec}"><span class="n">{n:02d}</span> {e(lec['who'])}: {e(lec['title'])}</h2>
<p class="small">{len(mine)} clips · full lecture on <a href="https://www.youtube.com/watch?v={lec['id']}">YouTube</a></p>
<div class="clips">""")
        for k in mine:
            c = k["c"]
            fid = f"fig-{c['id'].lower()}"
            must = c["priority"] == 1
            src_t = secs(c["start"])
            search = " ".join([c["id"], c["title"], lec["title"], lec["who"], *c["tags"], c["job"], c["learn"]]).lower()
            human = f"<p><b>The human part:</b> {e(c['human'])}</p>" if c.get("human") else ""
            out.append(f"""<figure class="clip" id="{fid}" data-brief-anchor="{fid}" data-id="{c['id']}" data-must="{int(must)}" data-x="{int(k['fits_x'])}" data-small="{int(k['small'])}" data-s="{e(search)}">
<div class="c-head"><div class="c-title">{e(c['title'])}</div><span class="badge{'' if must else ' more'}">{'MUST-WATCH' if must else 'MORE'}</span></div>
<div class="c-meta">{e(lec['who'])} · {e(lec['title'])} · {c['id']} · from {c['start']}</div>
<div class="c-stats">{mmss(k['d'])} · {k['mb']:.0f} MB · {k['w']}×{k['h']} · <span class="{'ok' if k['fits_x'] else 'no'}">{'fits X' if k['fits_x'] else 'over X’s 2:20'}</span></div>
<div class="strip">{''.join(f'<span>{e(t)}</span>' for t in c['tags'])}</div>
<div class="c-job"><b>For the job:</b> {e(c['job'])}</div>
<video controls preload="none" playsinline poster="clips/posters/{c['id']}.jpg" src="clips/{k['name']}.mp4"></video>
<div class="acts"><button class="pin" data-pin="{c['id']}" title="pin (kept in this browser)">☆</button><button class="om" data-play="{e(k['shared'])}" title="play in Omarchy's player">▶ Omarchy</button><button class="dr" data-drag="{e(k['shared'])}" title="a real file at your pointer: drop it into X">⇱ drag</button><button data-copy="{e(k['mp4'])}" title="copy the path, then Ctrl+L in an upload dialog">⧉ path</button><a href="file://{e(k['note'])}" title="source link, notes and transcript">note</a><a href="https://www.youtube.com/watch?v={lec['id']}&amp;t={src_t}s" title="the original lecture at this moment">source ↗</a></div>
<details><summary>what it teaches{', the human part' if c.get('human') else ''}</summary><p><b>What it teaches:</b> {e(c['learn'])}</p>{human}</details>
<details><summary>transcript</summary><p class="tx">{e(transcript(k['note']))}</p></details>
<figcaption class="small">notes on {c['id']}</figcaption></figure>""")
        out.append("</div></section>")
        n += 1
    out.append(f"""<div id="toast"></div>
<script>
const DRAG = {{port: 8779, token: {json.dumps(token)}}};
const PINS = 'cs329z-clip-pins';
let pins = JSON.parse(localStorage.getItem(PINS) || '[]');
const $$ = s => [...document.querySelectorAll(s)];
function toast(t, ms = 2200) {{ const el = document.getElementById('toast'); el.textContent = t; el.classList.add('on'); clearTimeout(el._t); el._t = setTimeout(() => el.classList.remove('on'), ms); }}
async function helper(verb, p, said) {{
  if (!DRAG.token) return toast('no drag helper token: build Cinema Delight\\'s index once (python3 tools/index.py)', 5000);
  const q = new URLSearchParams({{t: DRAG.token, p}});
  try {{ await fetch(`http://127.0.0.1:${{DRAG.port}}/${{verb}}?${{q}}`, {{mode: 'no-cors', cache: 'no-store'}}); toast(said, 3500); }}
  catch {{ toast('the drag helper is not running: systemctl --user start cinema-drag', 6000); }}
}}
async function copy(text) {{
  try {{ await navigator.clipboard.writeText(text); }}
  catch {{ const t = document.createElement('textarea'); t.value = text; document.body.append(t); t.select(); document.execCommand('copy'); t.remove(); }}
  toast('copied  ' + text);
}}
function paintPins() {{ for (const b of $$('[data-pin]')) {{ const on = pins.includes(b.dataset.pin); b.classList.toggle('on', on); b.textContent = on ? '★' : '☆'; }} }}
let mode = 'all';
function filter() {{
  const q = document.getElementById('q').value.trim().toLowerCase();
  for (const f of $$('figure.clip')) {{
    const d = f.dataset;
    const ok = (mode === 'all' || (mode === 'must' && d.must === '1') || (mode === 'x' && d.x === '1') || (mode === 'small' && d.small === '1') || (mode === 'pinned' && pins.includes(d.id)))
      && (!q || q.split(/\\s+/).every(w => d.s.includes(w)));
    f.hidden = !ok;
  }}
  for (const s of $$('section.lec')) s.hidden = !s.querySelector('figure.clip:not([hidden])');
}}
document.addEventListener('click', ev => {{
  const b = ev.target.closest('button'); if (!b) return;
  if (b.dataset.play) helper('play', b.dataset.play, '▶ opening in Omarchy\\'s player');
  else if (b.dataset.drag) helper('drag', b.dataset.drag, '⇱ the file is waiting at your pointer: drag it into X');
  else if (b.dataset.copy) copy(b.dataset.copy);
  else if (b.dataset.pin) {{ const id = b.dataset.pin; pins = pins.includes(id) ? pins.filter(x => x !== id) : [...pins, id]; localStorage.setItem(PINS, JSON.stringify(pins)); paintPins(); if (mode === 'pinned') filter(); }}
  else if (b.dataset.f) {{ mode = b.dataset.f; for (const p of $$('.pill')) p.classList.toggle('on', p === b); filter(); }}
}});
document.getElementById('q').addEventListener('input', filter);
document.addEventListener('keydown', ev => {{
  const q = document.getElementById('q');
  if (ev.key === '/' && document.activeElement !== q && !/INPUT|TEXTAREA/.test(document.activeElement.tagName)) {{ ev.preventDefault(); q.focus(); }}
  else if (ev.key === 'Escape' && document.activeElement === q) {{ q.value = ''; filter(); q.blur(); }}
}});
paintPins();
</script>
<footer><p>Primary artifact: this page. The cut list and the tools are in the LearnAgenticAI-stanford-cs329z repository; the clips are on this machine only.</p></footer></main>
<!--/brief-content-->
<!--BRIEF:notes--></body></html>""")
    (MEDIA / "watch.src.html").write_text("\n".join(out))
    print(f"wrote media/watch.src.html: {len(cards)} cards, {n_must} must-watch, {n_x} fit X, {n_small} under {SMALL_MB} MB; linked into {SHARED}")

if __name__ == "__main__":
    main()
