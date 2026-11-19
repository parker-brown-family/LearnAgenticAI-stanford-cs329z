# Stanford CS329Z, cut for study

A study guide to Stanford's public lectures for **CS329Z: Engineering AI Agents**, and the tools to cut them into short clips for re-recording with your own commentary.

**[CUTS.md](CUTS.md)** is the guide: 61 cuts (about four hours, 29 marked must-watch), each with why it matters for getting hired into agent-engineering work, what it teaches, and the human part. Every cut links to the original lecture at the moment it starts.

The cuts were chosen with one assumption in mind. Anyone building AI now uses AI to build it, and the AI will often build it better than the person. What the person still brings is taste, constraints, knowledge of the system, and a sense of the customer. So the cuts favour the moments that teach those judgments (what to evaluate, when not to use an agent, how much harness a model needs) over the moments that teach mechanics a model can already handle.

Part of [LearnAgenticAI](https://github.com/parker-brown-family/LearnAgenticAI). For personal use. If you find something useful in here, by all means use it.

## What is here, and what is not

| Here | Not here |
|---|---|
| `cuts.json`: every cut, its times and its notes | The lecture video |
| `CUTS.md`: the guide, built from `cuts.json` | The clips |
| `lectures.json`: the ten lectures and their YouTube ids | The captions and transcripts |
| `data/window-scores.json`: the machine pass that ranked every two-minute window | |
| `tools/`: download, transcribe, score, read and cut | |

The lectures belong to Stanford and are on [Stanford Online's YouTube channel](https://www.youtube.com/@stanfordonline). Everything in the right-hand column is made on your own machine under `media/`, which git ignores.

## Rebuilding the clips

Needs `yt-dlp`, `ffmpeg` and Python 3.

```bash
yt-dlp -f "bv*[height<=720][ext=mp4]+ba[ext=m4a]/b[height<=720]" --merge-output-format mp4 -o "media/video/%(playlist_index)02d-%(id)s.%(ext)s" "https://www.youtube.com/playlist?list=PLPRcF5HR02_U"
```
```bash
yt-dlp --skip-download --write-subs --write-auto-subs --sub-langs "en.*,en" --sub-format json3 -o "media/subs/%(playlist_index)02d-%(id)s.%(ext)s" "https://www.youtube.com/playlist?list=PLPRcF5HR02_U"
```
```bash
python3 tools/transcripts.py media/subs media/transcripts
```
```bash
python3 tools/cut.py
```

Each clip starts half a second before its in point and runs to the end of the sentence being spoken at its out point (at most ten seconds later). The clips land in `media/clips/`, one `.mp4` per cut with a `.txt` beside it carrying the source link, the notes and the transcript of what is said. `tools/cut.py L5-i L4-b` cuts only those. YouTube rate-limits caption downloads; if some fail, wait a few minutes and run the second command again.

`python3 tools/read.py media/transcripts 6 42:00 48:00` prints any stretch of a lecture with timestamps, which is how the in and out points were chosen. Change a time in `cuts.json` and run `tools/cut.py` again: a clip whose cut moved is made again, and the rest are left alone. `python3 tools/build_guide.py --local` writes `media/clips/INDEX.md`, the guide with each cut linked to its clip on your machine.

## How the cuts were chosen

Every lecture was split into two-minute windows, 421 in all, and each window was scored by [Jev](https://docs.typesafe.ai), a model that answers typed questions with probabilities. It answered four questions per window: how much the passage teaches what agent-engineering jobs ask for (a score from 0 to 3), how much it builds lasting understanding (0 to 3), whether it is about a judgment the person makes (a probability), and whether a viewer could start watching there (a probability). `tools/score_windows.py` asks those questions, and `data/window-scores.json` holds the answers.

The scores only set the reading order. Nearly every window of a course on agents scores as job-relevant, so the cuts themselves were chosen by reading the transcripts and setting each in and out point by hand. The skills that agent job postings name most often (evaluation, retrieval, tool use and MCP, frameworks such as LangGraph, multi-agent work, memory, context engineering, guardrails, observability, cost) set what counted.

The tools and notes are MIT licensed (LICENSE). The lectures themselves are Stanford's and are not covered by it.
