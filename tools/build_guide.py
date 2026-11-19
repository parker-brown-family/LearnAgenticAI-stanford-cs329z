#!/usr/bin/env python3
"""Write CUTS.md, the study guide: every cut, linked to the moment in the original lecture.

With --local, also write media/clips/INDEX.md: the same guide, linking each cut to its clip on
this machine (file:// URLs), for watching and recording over. It is never committed.

    python3 -I tools/build_guide.py [--local]
"""
import json, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent

def secs(t):
    m, s = t.split(":"); return int(m) * 60 + int(float(s))

def slug(title):
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:60].rstrip("-")

def main(local=False):
    cuts = json.loads((HERE / "cuts.json").read_text())
    lectures = sorted(json.loads((HERE / "lectures.json").read_text()),
                      key=lambda l: (l["course_order"] == "guest", l["course_order"] if l["course_order"] != "guest" else 0))
    total = sum(secs(c["end"]) - secs(c["start"]) for c in cuts)
    p1 = [c for c in cuts if c["priority"] == 1]
    lines = [
        "# Stanford CS329Z, cut for study",
        "",
        f"{len(cuts)} cuts from the ten public lectures of Stanford's *CS329Z: Engineering AI Agents* "
        f"(about {total // 60} minutes in all). {len(p1)} are marked **must-watch** "
        f"(about {sum(secs(c['end']) - secs(c['start']) for c in p1) // 60} minutes).",
        "",
        "Each cut says why it matters for getting hired into agent-engineering work, what it teaches, and, where it applies, the human part: the taste, constraints, system knowledge and customer sense a person brings when AI does most of the building. Every link opens the original lecture at the moment the cut starts.",
        "",
        "Lectures are listed in course order. The guest lecture on Terminal-Bench comes last.",
        "",
    ]
    for lec in lectures:
        mine = [c for c in cuts if c["lecture"] == lec["n"]]
        lines += [f"## {lec['who']}: {lec['title']}", "",
                  f"https://www.youtube.com/watch?v={lec['id']}", ""]
        for c in mine:
            mins = (secs(c["end"]) - secs(c["start"])) / 60
            star = " **must-watch**" if c["priority"] == 1 else ""
            lines += [f"### {c['id']} · {c['title']}{star}", "",
                      f"{c['start']} to {c['end']}, {mins:.1f} min · {', '.join(c['tags'])}", "",
                      f"https://www.youtube.com/watch?v={lec['id']}&t={secs(c['start'])}s", "",
                      *([f"file://{HERE / 'media' / 'clips' / (c['id'] + '-' + slug(c['title']) + '.mp4')}", ""] if local else []),
                      f"- **For the job:** {c['job']}",
                      f"- **What it teaches:** {c['learn']}"]
            if c.get("human"):
                lines.append(f"- **The human part:** {c['human']}")
            lines.append("")
    out = HERE / ("media/clips/INDEX.md" if local else "CUTS.md")
    out.write_text("\n".join(lines))
    print(f"wrote {out.relative_to(HERE)}: {len(cuts)} cuts, {total // 60} min")

if __name__ == "__main__":
    main()
    if "--local" in sys.argv:
        main(local=True)
