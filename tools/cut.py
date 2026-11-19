#!/usr/bin/env python3
"""Cut every clip in cuts.json out of the downloaded lectures, ready to re-edit.

Each clip is re-encoded (H.264 + AAC, NVENC when available) so it starts exactly where the
cut says rather than at the previous keyframe, with half a second of air either side.
Beside each clip goes a .txt with its source link and the transcript of what is said.
Existing clips are skipped, so editing one cut and re-running only re-makes that one.

    python3 -I tools/cut.py                  # all cuts
    python3 -I tools/cut.py 05-i 06-b        # just these
"""
import json, re, shutil, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
MEDIA = HERE / "media"
PAD_IN, PAD_OUT = 0.5, 0.5

def secs(t):
    m, s = t.split(":"); return int(m) * 60 + float(s)

def slug(title):
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:60].rstrip("-")

def encoder():
    out = subprocess.run(["ffmpeg", "-hide_banner", "-encoders"], capture_output=True, text=True).stdout
    return ["-c:v", "h264_nvenc", "-preset", "p5", "-cq", "21"] if "h264_nvenc" in out else ["-c:v", "libx264", "-preset", "veryfast", "-crf", "20"]

def main(only):
    cuts = json.loads((HERE / "cuts.json").read_text())
    lectures = {l["n"]: l for l in json.loads((HERE / "lectures.json").read_text())}
    out_dir = MEDIA / "clips"; out_dir.mkdir(parents=True, exist_ok=True)
    venc = encoder()
    for c in cuts:
        if only and c["id"] not in only:
            continue
        lec = lectures[c["lecture"]]
        src = next((MEDIA / "video").glob(f"{c['lecture']:02d}-{lec['id']}.mp4"), None)
        if src is None:
            print(f"{c['id']}: lecture video not downloaded yet, skipped"); continue
        a, b = max(0.0, secs(c["start"]) - PAD_IN), secs(c["end"]) + PAD_OUT
        name = f"{c['id']}-{slug(c['title'])}"
        mp4, txt = out_dir / f"{name}.mp4", out_dir / f"{name}.txt"
        if not mp4.exists():
            tmp = mp4.with_suffix(".part.mp4")
            cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", f"{a:.2f}", "-i", str(src),
                   "-t", f"{b - a:.2f}", *venc, "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", str(tmp)]
            subprocess.run(cmd, check=True)
            shutil.move(tmp, mp4)
        tf = next((MEDIA / "transcripts").glob(f"{c['lecture']:02d}-*.json"))
        segs = json.loads(tf.read_text())["segments"]
        said = " ".join(s["text"] for s in segs if secs(c["start"]) <= s["start"] < secs(c["end"]))
        txt.write_text(
            f"{c['title']}\n{lec['who']}: {lec['title']}\n"
            f"Source: https://www.youtube.com/watch?v={lec['id']}&t={int(secs(c['start']))}s  ({c['start']} to {c['end']})\n\n"
            f"Why it matters for the job: {c['job']}\nWhat it teaches: {c['learn']}\n"
            + (f"The human part: {c['human']}\n" if c.get("human") else "")
            + f"\n--- transcript ---\n{said}\n")
        print(f"{c['id']}  {b - a:6.0f}s  {mp4.name}")

if __name__ == "__main__":
    main(set(sys.argv[1:]))
