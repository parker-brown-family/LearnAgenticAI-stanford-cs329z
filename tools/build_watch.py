#!/usr/bin/env python3
"""Write media/watch.src.html: a page to watch every clip in place, with why each matters.

It is a briefing source (the house look and reader notes arrive when it is built), so build it with:

    python3 -I tools/build_watch.py
    python3 ~/.claude/skills/briefing/scripts/brief.py html media/watch.src.html media/watch.html

The page lives in media/ beside the clips it plays, and is never committed.
"""
import html, json, re
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
MEDIA = HERE / "media"

def secs(t):
    m, s = t.split(":"); return int(m) * 60 + int(float(s))

def slug(title):
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:60].rstrip("-")

def e(s):
    return html.escape(s, quote=True)

def main():
    cuts = json.loads((HERE / "cuts.json").read_text())
    lectures = sorted(json.loads((HERE / "lectures.json").read_text()),
                      key=lambda l: (l["course_order"] == "guest", 0 if l["course_order"] == "guest" else l["course_order"]))
    p1 = [c for c in cuts if c["priority"] == 1]
    mins = lambda cs: sum(secs(c["end"]) - secs(c["start"]) for c in cs) // 60
    out = []
    out.append(f"""<!doctype html>
<html lang="en"><head><title>CS329Z study clips</title><!-- briefing: {{"id": "cs329z-watch", "purpose": "summary"}} --><!--BRIEF:head-->
<style>
.small{{font-size:13px;color:var(--dim)}}
.clips{{display:grid;grid-template-columns:repeat(auto-fill,minmax(420px,1fr));gap:18px}}
figure.clip video{{width:100%;border-radius:10px;display:block;background:transparent}}
figure.clip .why{{margin:.5em 0 0}}
figure.clip .path{{font-family:var(--mono,monospace);font-size:12px;color:var(--dim);word-break:break-all}}
.must{{font-weight:700}}
ol.how li{{margin:.35em 0}}
</style></head><body>
<!--brief-content-->
<header class="top"><div class="wrap"><div class="eyebrow">LearnAgenticAI · Stanford CS329Z · study clips</div><div class="opening" id="top" data-brief-anchor="top"><h1>Watch the clips here, then record your reacts over them</h1> <p class="lede">{len(cuts)} clips, about {mins(cuts)} minutes, cut from Stanford's ten public lectures on engineering AI agents. Start with the {len(p1)} marked <b>must-watch</b> (about {mins(p1)} minutes). Each clip says why it matters for getting hired and what it teaches.</p></div><nav class="sections"></nav></div></header>
<main class="wrap">
<section class="pane"><h2 id="sec-how" data-brief-anchor="sec-how"><span class="n">01</span> How to use them</h2>
<p>The <b>.mp4 files</b> in the <code>clips</code> folder are the clips; everything else there is supporting material. Two ways to make a react video:</p>
<ol class="how">
<li><b>Record live in OBS.</b> Add the clip as a Media Source, your webcam and microphone beside it, press record, and talk over it, pausing the clip when you want to say more.</li>
<li><b>Edit afterwards in Kdenlive.</b> Drop the clip on the timeline, record a voiceover track, and cut in your camera or pause the clip where you speak.</li>
</ol>
<p>When you upload, the clip's note in <code>clips/notes/</code> has the link to the original lecture at that moment, for the description. Leave a note on any clip on this page to change its cut or say it is not worth keeping.</p></section>
""")
    n = 2
    for lec in lectures:
        mine = [c for c in cuts if c["lecture"] == lec["n"]]
        sec = f"sec-{mine[0]['id'].split('-')[0].lower()}"
        out.append(f"""<section class="pane"><h2 id="{sec}" data-brief-anchor="{sec}"><span class="n">{n:02d}</span> {e(lec['who'])}: {e(lec['title'])}</h2>
<p class="small">{len(mine)} clips, {sum(1 for c in mine if c['priority']==1)} must-watch. Full lecture: <a href="https://www.youtube.com/watch?v={lec['id']}">YouTube</a></p>
<div class="clips">""")
        for c in mine:
            f = f"{c['id']}-{slug(c['title'])}"
            m = (secs(c["end"]) - secs(c["start"])) / 60
            tag = ' <span class="tag must">must-watch</span>' if c["priority"] == 1 else ""
            human = f'<p class="small"><b>The human part:</b> {e(c["human"])}</p>' if c.get("human") else ""
            fid = f"fig-{c['id'].lower()}"
            out.append(f"""<figure class="clip" id="{fid}" data-brief-anchor="{fid}"><span class="lbl">{c['id']} · {m:.1f} min{tag}</span>
<video controls preload="none" poster="clips/posters/{c['id']}.jpg" src="clips/{f}.mp4"></video>
<figcaption><b>{e(c['title'])}</b></figcaption>
<p class="why"><b>For the job:</b> {e(c['job'])}</p>
<p class="small"><b>What it teaches:</b> {e(c['learn'])}</p>
{human}<p class="path">clips/{f}.mp4 · <a href="https://www.youtube.com/watch?v={lec['id']}&amp;t={secs(c['start'])}s">source at {c['start']}</a></p></figure>""")
        out.append("</div></section>")
        n += 1
    out.append("""<footer><p>Primary artifact: this page. The cut list and the tools are in the LearnAgenticAI-stanford-cs329z repository; the clips are on this machine only.</p></footer></main>
<!--/brief-content-->
<!--BRIEF:notes--></body></html>""")
    (MEDIA / "watch.src.html").write_text("\n".join(out))
    print("wrote media/watch.src.html")

if __name__ == "__main__":
    main()
