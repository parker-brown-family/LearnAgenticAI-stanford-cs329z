#!/usr/bin/env python3
"""Turn YouTube json3 caption files into one timed transcript per lecture.

Prefers the human caption track (the id-suffixed `en-…` file) over YouTube's auto captions.
Writes media/transcripts/<NN>-<id>.json: [{"start": s, "end": s, "text": str}, ...]

    python3 -I tools/transcripts.py media/subs media/transcripts
"""
import json, re, sys
from pathlib import Path

def rank(name: str) -> int:
    # human track first, then auto "en", then "en-orig"
    if re.search(r"\.en-(en-)?[A-Za-z0-9_-]{8,}\.json3$", name):
        return 0 if ".en-en-" not in name else 1
    if name.endswith(".en.json3"):
        return 2
    return 3

def segments(path: Path):
    data = json.loads(path.read_text())
    out = []
    for ev in data.get("events", []):
        if "segs" not in ev:
            continue
        text = "".join(s.get("utf8", "") for s in ev["segs"]).replace("\n", " ").strip()
        if not text:
            continue
        start = ev.get("tStartMs", 0) / 1000
        out.append({"start": round(start, 2), "end": round(start + ev.get("dDurationMs", 0) / 1000, 2), "text": text})
    return out

def main(src, dst):
    src, dst = Path(src), Path(dst)
    dst.mkdir(parents=True, exist_ok=True)
    best = {}
    for f in sorted(src.glob("*.json3")):
        key = f.name.split(".")[0]
        if key not in best or rank(f.name) < rank(best[key].name):
            best[key] = f
    for key, f in sorted(best.items()):
        segs = segments(f)
        (dst / f"{key}.json").write_text(json.dumps({"source": f.name, "segments": segs}, ensure_ascii=False))
        words = sum(len(s["text"].split()) for s in segs)
        print(f"{key}  {f.name:45s} {len(segs):5d} segments  {words:6d} words  ends {segs[-1]['end']/60:.0f} min")

if __name__ == "__main__":
    main(*sys.argv[1:3])
