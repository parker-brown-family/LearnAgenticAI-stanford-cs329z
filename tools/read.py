#!/usr/bin/env python3
"""Print a stretch of one lecture's transcript with a timestamp every ~20 seconds.

    python3 -I tools/read.py media/transcripts 6 50:00 54:30
"""
import json, sys
from pathlib import Path

def secs(t):
    m, s = t.split(":"); return int(m) * 60 + float(s)

def main(tdir, lec, a, b):
    f = next(Path(tdir).glob(f"{int(lec):02d}-*.json"))
    segs = [s for s in json.loads(f.read_text())["segments"] if secs(a) <= s["start"] <= secs(b)]
    line, mark = [], None
    for s in segs:
        if mark is None or s["start"] - mark >= 20:
            if line: print(" ".join(line))
            mark = s["start"]; line = [f"[{int(mark//60)}:{int(mark%60):02d}]"]
        line.append(s["text"])
    if line: print(" ".join(line))

if __name__ == "__main__":
    main(*sys.argv[1:5])
