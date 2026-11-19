#!/usr/bin/env python3
"""Score every ~2-minute window of every lecture with Jev, so a person reads only the best.

Code owns the windowing, the arithmetic and the ranking. Jev owns four judgments a keyword list
cannot make: does this passage teach what agent-engineering jobs ask for, does it build real
understanding, is it about the human's judgment, and can a viewer start watching here.
One batched request per window. Answers are cached by window text, so re-runs only ask what changed.

    python3 -I tools/score_windows.py media/transcripts media/jev/jev-windows.json
"""
from __future__ import annotations
import hashlib, json, sys, threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

JI = Path.home() / "Work/jev-integrations"
sys.path.insert(0, str(JI))
from jev import JevClient                      # noqa: E402
from jev.dotenv import load as load_dotenv     # noqa: E402
from jev.ports.hosted import HostedPort        # noqa: E402

HERE = Path(__file__).resolve().parent.parent
WINDOW_S = 110

QUESTIONS = {
    "job_value": {
        "type": "score",
        "instructions": (
            "How much `passage` (from the lecture named in `lecture`) teaches something employers hiring AI agent engineers ask candidates to know, "
            "build or discuss in interviews: evaluating agents, retrieval (RAG), tool use and MCP, agent "
            "frameworks such as LangGraph or DSPy, multi-agent orchestration, memory, context engineering, "
            "guardrails and safety, observability, cost and latency, and running agents in production."
        ),
        "criteria": [
            "nothing a hiring manager would ask about: logistics, introductions, audio checks, jokes or setup",
            "names a relevant topic in passing without explaining it",
            "explains a relevant concept or technique clearly enough that a listener could discuss it",
            "gives practical guidance, a trade-off, a failure mode or a result an engineer would use when building an agent system or defending one in an interview",
        ],
    },
    "understanding": {
        "type": "score",
        "instructions": (
            "How much `passage` builds a lasting understanding of how and why AI agents and language models "
            "behave as they do, rather than listing names or details that will soon change."
        ),
        "criteria": [
            "no explanatory content",
            "surface only: names, definitions or details without the reason behind them",
            "explains a mechanism or the reason something works or fails",
            "a key insight that changes how a builder thinks about agents",
        ],
    },
    "human_judgment": {
        "type": "noul",
        "instructions": (
            "`passage` discusses a judgment a person directing an AI build has to make: what to build, which "
            "design or trade-off to choose, how to tell whether it works, what constraints to set, or when an "
            "agent or a model is the wrong tool."
        ),
        "criteria": {
            "true": "The speaker weighs options, names a trade-off, says how to evaluate, or says when to use or not use an approach.",
            "false": "The passage only describes how a technique works, recounts history, or handles course logistics.",
        },
    },
    "self_contained": {
        "type": "noul",
        "instructions": (
            "A viewer who starts watching at the first sentence of `passage`, without having seen the earlier "
            "part of the lecture, can follow what is being said."
        ),
        "criteria": {
            "true": "It opens a topic or makes a point that is clear from the passage itself; references to the slide on screen are fine.",
            "false": "It starts mid-argument or depends on something defined earlier in the lecture that the passage does not explain.",
        },
    },
}

def windows(segs):
    cur, out = [], []
    for s in segs:
        cur.append(s)
        if cur[-1]["end"] - cur[0]["start"] >= WINDOW_S:
            out.append(cur); cur = []
    if cur:
        out.append(cur)
    return [{"start": w[0]["start"], "end": w[-1]["end"], "text": " ".join(x["text"] for x in w)} for w in out]

def mmss(s):
    return f"{int(s//60)}:{int(s%60):02d}"

def flat(v):
    # keep absence as None: an abstained answer is not a zero
    return {"value": v.value, "probabilities": v.probabilities, "confidence": v.confidence,
            "abstained": v.abstained, "reason": v.reason}

def main(tdir, out):
    load_dotenv(JI / ".env")
    client = JevClient("https://openrouter.ai/api", port=HostedPort("jev-latest"),
                       api_key_env="OPENROUTER_API_KEY", timeout_s=60.0, lint="warn")
    lectures = {l["id"]: l for l in json.loads((HERE / "lectures.json").read_text())}
    out = Path(out); out.parent.mkdir(parents=True, exist_ok=True)
    cache = {r["hash"]: r for r in json.loads(out.read_text())} if out.exists() else {}
    todo, allw = [], []
    for f in sorted(Path(tdir).glob("*.json")):
        n, vid = f.stem.split("-", 1)
        lec = lectures[vid]
        for w in windows(json.loads(f.read_text())["segments"]):
            h = hashlib.sha1((vid + w["text"]).encode()).hexdigest()[:16]
            rec = {"hash": h, "lecture": int(n), "id": vid, "start": w["start"], "end": w["end"], "text": w["text"]}
            allw.append(rec)
            if h not in cache:
                todo.append((rec, lec))
    print(f"{len(allw)} windows, {len(allw)-len(todo)} cached, {len(todo)} to ask")
    lock = threading.Lock()
    def run(item):
        rec, lec = item
        state = {"lecture": f"Stanford CS329Z, {lec['who']}: {lec['title']}", "passage": rec["text"]}
        ans = client.ask_many(state, QUESTIONS)
        rec = dict(rec, jev={k: flat(v) for k, v in ans.items()})
        with lock:
            cache[rec["hash"]] = rec
    with ThreadPoolExecutor(8) as ex:
        for i, _ in enumerate(ex.map(run, todo), 1):
            if i % 50 == 0:
                print(f"  {i}/{len(todo)}")
    keep = [cache[r["hash"]] for r in allw if r["hash"] in cache]
    out.write_text(json.dumps(keep, ensure_ascii=False, indent=0))
    print(f"wrote {out} ({len(keep)} windows)")

if __name__ == "__main__":
    main(*sys.argv[1:3])
