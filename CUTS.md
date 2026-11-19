# Stanford CS329Z, cut for study

61 cuts from the ten public lectures of Stanford's *CS329Z: Engineering AI Agents* (about 238 minutes in all). 29 are marked **must-watch** (about 130 minutes).

Each cut says why it matters for getting hired into agent-engineering work, what it teaches, and, where it applies, the human part: the taste, constraints, system knowledge and customer sense a person brings when AI does most of the building. Every link opens the original lecture at the moment the cut starts.

Lectures are listed in course order. The guest lecture on Terminal-Bench comes last.

## Lecture 1, Diyi Yang: What Are AI Agents? Agentic Systems Explained

https://www.youtube.com/watch?v=DGI4vucR71w

### L1-a · Homework up, exams down: use AI to learn how to learn

5:50 to 7:40, 1.8 min · learning, human-role

https://www.youtube.com/watch?v=DGI4vucR71w&t=350s

- **For the job:** Why understanding still matters when AI writes the code: Anthropic's own engineers finished faster and scored lower on mastery.
- **What it teaches:** The gap between output and understanding.
- **The human part:** The person has to understand enough to judge the output.

### L1-b · Will capability saturate? Recursive self-improvement, and why better costs more

18:40 to 21:30, 2.8 min · self-improvement, cost

https://www.youtube.com/watch?v=DGI4vucR71w&t=1120s

- **For the job:** Context for the price-and-accuracy curves every agent benchmark now plots.
- **What it teaches:** Recursive self-improvement as an accelerant, and thinking longer as the reason better runs cost more.

### L1-c · The agent that kept deleting email: compaction dropped "confirm with me" **must-watch**

52:01 to 53:29, 1.5 min · memory, guardrails, context-engineering

https://www.youtube.com/watch?v=DGI4vucR71w&t=3121s

- **For the job:** A real failure story about memory compression and safety rules.
- **What it teaches:** An instruction the user gave at the start was not judged important when the context was compressed.
- **The human part:** Rules that must survive compaction belong outside the model's judgment.

### L1-d · Three layers: system, data, evaluation. Ask which one failed **must-watch**

53:29 to 56:05, 2.6 min · evaluation, design-patterns

https://www.youtube.com/watch?v=DGI4vucR71w&t=3209s

- **For the job:** A debugging frame that works in any interview: is it the system, the data, or the metric?
- **What it teaches:** "Choosing the wrong metric can make a weak agent look nice."

### L1-e · The most capable agent is not the most reliable **must-watch**

61:20 to 63:54, 2.6 min · evaluation, reliability

https://www.youtube.com/watch?v=DGI4vucR71w&t=3680s

- **For the job:** Reliability is the production bar. Consistency, robustness and predictability are its three measures.
- **What it teaches:** Princeton's finding that reliability does not track accuracy, and harness audits where safety lags completion.

### L1-f · Agents failing in the wild: a shopping agent that never asked, distraction attacks, access control

63:54 to 69:40, 5.8 min · safety, guardrails

https://www.youtube.com/watch?v=DGI4vucR71w&t=3834s

- **For the job:** Stories for "how would you make an agent safe on customer data?"
- **What it teaches:** Operator buying milk in Iowa, pop-ups that derail agents 87% of the time, missing access control, and misalignment.
- **The human part:** Knowing what the customer would have wanted asked is customer intuition, not model capability.

## Lecture 2, Michael Ryan: LLMs for Agent Builders: Context Engineering

https://www.youtube.com/watch?v=Vr1NzH8bT44

### L2-a · Why builders should know the model's internals

2:40 to 3:50, 1.2 min · llm-internals

https://www.youtube.com/watch?v=Vr1NzH8bT44&t=160s

- **For the job:** Knowing the KV cache and attention lets you choose the right model.
- **What it teaches:** Where agent builders sit on the stack.

### L2-b · Sampling and temperature

7:38 to 11:56, 4.3 min · llm-internals

https://www.youtube.com/watch?v=Vr1NzH8bT44&t=458s

- **For the job:** "Why isn't temperature 0 deterministic?" starts here.
- **What it teaches:** Greedy, top-k, top-p, temperature and beam search.

### L2-c · Full or linear attention: choosing a model for long context

33:38 to 36:40, 3.0 min · llm-internals, context-engineering

https://www.youtube.com/watch?v=Vr1NzH8bT44&t=2018s

- **For the job:** A model-choice argument grounded in architecture.
- **What it teaches:** O(n squared) against O(n), and why linear attention forgets the needle.

### L2-d · Training models for agent work: synthetic coding tasks

47:27 to 50:39, 3.2 min · llm-internals, training

https://www.youtube.com/watch?v=Vr1NzH8bT44&t=2847s

- **For the job:** Vocabulary for the training side of agent roles, without training models yourself.
- **What it teaches:** Synthetic repository tasks lifting a 32B model on SWE-bench Verified from about 9% to 40%.

### L2-e · Prefill and decode: why inference is memory-bound

54:57 to 58:11, 3.2 min · llm-internals, cost

https://www.youtube.com/watch?v=Vr1NzH8bT44&t=3297s

- **For the job:** Cost and latency questions rest on this.
- **What it teaches:** Compute-bound prefill, memory-bound decode, batching and speculative decoding.

### L2-f · Reasoning and inference-time scaling

60:18 to 65:36, 5.3 min · llm-internals, cost

https://www.youtube.com/watch?v=Vr1NzH8bT44&t=3618s

- **For the job:** Reasoning budgets are a cost dial you will be asked about.
- **What it teaches:** Thinking longer, reasoning effort settings, budget-aware training, and self-consistency as a verifier.

### L2-g · Constrained decoding and structured output **must-watch**

65:36 to 68:50, 3.2 min · llm-internals, tools

https://www.youtube.com/watch?v=Vr1NzH8bT44&t=3936s

- **For the job:** Structured outputs are how agents talk to code; broken JSON is a classic failure.
- **What it teaches:** Forcing a schema at decode time, and why it is faster and more reliable.

### L2-h · What goes into the context, the harness tax, and avoiding compaction **must-watch**

70:57 to 77:22, 6.4 min · context-engineering, harness, cost

https://www.youtube.com/watch?v=Vr1NzH8bT44&t=4257s

- **For the job:** Context engineering in practice, with the Harness Tax comparison of Codex, Claude Code and Pi.
- **What it teaches:** System prompt, history, tools and retrieved data; ordering for the KV cache; putting the prompt in a variable instead of the window.

## Lecture 3, Diyi Yang: RAG Explained: From BM25 to Agentic RAG

https://www.youtube.com/watch?v=psLc-46GqY0

### L3-a · Why RAG: an answer you can check

6:36 to 8:46, 2.2 min · rag

https://www.youtube.com/watch?v=psLc-46GqY0&t=396s

- **For the job:** The one-line motivation for retrieval.
- **What it teaches:** A fluent answer versus one that carries its evidence.

### L3-b · How RAG grew up, and when you need it

18:42 to 22:50, 4.1 min · rag

https://www.youtube.com/watch?v=psLc-46GqY0&t=1122s

- **For the job:** Naive, advanced and modular RAG, and the private-data case that makes retrieval necessary.
- **What it teaches:** Modules such as search, routing, rewrite, rerank, memory and fusion composed into patterns.

### L3-c · Chunking, contextual retrieval and hybrid search **must-watch**

26:20 to 34:10, 7.8 min · rag

https://www.youtube.com/watch?v=psLc-46GqY0&t=1580s

- **For the job:** The practical core of a RAG system design question.
- **What it teaches:** Fixed and semantic chunking, Anthropic's contextual retrieval, and combining BM25 with embeddings.

### L3-d · Hierarchical and graph RAG, chosen by cost

37:14 to 44:47, 7.5 min · rag, cost

https://www.youtube.com/watch?v=psLc-46GqY0&t=2234s

- **For the job:** When a question needs the whole corpus, not one chunk.
- **What it teaches:** RAPTOR-style trees, knowledge graphs and communities, traded against retrieval quality, LLM cost and speed.

### L3-e · Measuring retrieval: hit@k, nDCG, recall@k **must-watch**

55:50 to 59:14, 3.4 min · rag, evaluation

https://www.youtube.com/watch?v=psLc-46GqY0&t=3350s

- **For the job:** You will be asked how you would know retrieval works.
- **What it teaches:** What each metric rewards, and training the retriever on more data.

### L3-f · Agentic RAG, and is RAG out of date? **must-watch**

68:10 to 76:30, 8.3 min · rag, agents

https://www.youtube.com/watch?v=psLc-46GqY0&t=4090s

- **For the job:** Agentic RAG is the current form, and "is RAG dead?" is a live interview question.
- **What it teaches:** Self-RAG, corrective RAG, search agents trained with RL, and the risks: compounding errors and injection.

## Lecture 4, Diyi Yang: How AI Agents Use Tools: Function Calling & MCP

https://www.youtube.com/watch?v=s0S38lz6O7M

### L4-a · How RAG fails, and lost in the middle

1:12 to 7:23, 6.2 min · rag, context-engineering

https://www.youtube.com/watch?v=s0S38lz6O7M&t=72s

- **For the job:** RAG appears in two-thirds of harness postings; its failure list is interview material.
- **What it teaches:** Permission leaks, distraction, conflicting evidence, injection, and the U-shaped accuracy curve over document position.

### L4-b · Citations can be hallucinated too

7:23 to 11:34, 4.2 min · rag, evaluation

https://www.youtube.com/watch?v=s0S38lz6O7M&t=443s

- **For the job:** Grounding is not proven by a citation. Know the numbers.
- **What it teaches:** Users rate generative search highly while citation precision and recall stay low.

### L4-c · Change the tool description, not the model: REST, function calling, MCP **must-watch**

62:00 to 69:09, 7.2 min · tools, mcp

https://www.youtube.com/watch?v=s0S38lz6O7M&t=3720s

- **For the job:** MCP is a named must-have. This is the history that explains why it exists.
- **What it teaches:** Three generations: docs for humans, JSON schemas for models, a protocol for an ecosystem.

### L4-d · How MCP works, and who gets which tools **must-watch**

69:09 to 75:08, 6.0 min · tools, mcp, guardrails

https://www.youtube.com/watch?v=s0S38lz6O7M&t=4149s

- **For the job:** Production MCP is about permissions as much as tools. This covers hosts, clients, servers and access control.
- **What it teaches:** tools/list and tools/call, FastMCP, and a course server that gates who may post grades while neither side sees the other's token.
- **The human part:** Who may call which tool is a policy a person sets.

## Lecture 5, Michael Ryan: DSPy vs. LangGraph: AI Agent Frameworks Explained

https://www.youtube.com/watch?v=q0Q-Hy8TTps

### L5-a · Building an agent versus engineering one, and the framework map

2:36 to 6:15, 3.6 min · frameworks, evaluation

https://www.youtube.com/watch?v=q0Q-Hy8TTps&t=156s

- **For the job:** Places LangGraph, DSPy, Temporal and observability tools on one map.
- **What it teaches:** You can build without data or evals; you cannot engineer without them.

### L5-b · LangGraph in five minutes: state, nodes, edges **must-watch**

42:21 to 47:43, 5.4 min · frameworks, langgraph

https://www.youtube.com/watch?v=q0Q-Hy8TTps&t=2541s

- **For the job:** LangGraph is named in about a third of harness postings and as a must-have in some.
- **What it teaches:** Shared state, nodes that read and write it, edges for control flow, and why a graph helps retries and observability.

### L5-c · Conditional edges, LangGraph agents, and LangGraph versus DSPy **must-watch**

47:43 to 54:27, 6.7 min · frameworks, langgraph

https://www.youtube.com/watch?v=q0Q-Hy8TTps&t=2863s

- **For the job:** The comparison question you will be asked, answered by someone who uses both.
- **What it teaches:** Routing functions, create_agent, different models per node, and composing DSPy inside LangGraph.

### L5-d · Durable execution with Temporal, and observability tools **must-watch**

64:00 to 67:39, 3.6 min · frameworks, durable-execution, observability

https://www.youtube.com/watch?v=q0Q-Hy8TTps&t=3840s

- **For the job:** Reliability, durable execution and observability are production must-haves; Temporal, LangSmith and Langfuse are the names.
- **What it teaches:** Retries under a flaky worker shown in Temporal's history; what LangSmith and Langfuse show you.

### L5-e · Best practices: keep it simple, make failures observable, build the eval first **must-watch**

67:39 to 73:45, 6.1 min · evaluation, observability, human-role

https://www.youtube.com/watch?v=q0Q-Hy8TTps&t=4059s

- **For the job:** Close to a checklist of what agent-engineering job descriptions ask for.
- **What it teaches:** Workflows before agents, trace everything, retries and timeouts, meta-agents that watch, and evals on your own domain rather than public benchmarks.
- **The human part:** Choosing the metric and the representative cases is the person's work.

### L5-f · The cost of frameworks: show me the prompt

73:45 to 76:34, 2.8 min · frameworks

https://www.youtube.com/watch?v=q0Q-Hy8TTps&t=4425s

- **For the job:** A mature answer to "would you use a framework?": dependencies, longevity, and knowing what runs underneath.
- **What it teaches:** Abstractions hide failures; look at the traces.

## Lecture 6, Michael Ryan: AI Agent Design Patterns: ReAct, CodeAct & More

https://www.youtube.com/watch?v=JC_pLC5EX_w

### L6-a · Workflow or agent: where the control flow lives **must-watch**

3:30 to 6:41, 3.2 min · design-patterns

https://www.youtube.com/watch?v=JC_pLC5EX_w&t=210s

- **For the job:** "Do you know when not to use an agent?" Workflows are predictable; agents are adaptable and harder to evaluate.
- **What it teaches:** The predictability and agency trade-off, with a support-ticket example of each.
- **The human part:** Choosing how much control to hand the model is a design decision about risk.

### L6-b · Five workflow patterns: chain, route, parallelize, orchestrate, evaluate-optimize **must-watch**

6:41 to 14:54, 8.2 min · design-patterns, cost

https://www.youtube.com/watch?v=JC_pLC5EX_w&t=401s

- **For the job:** Anthropic's "Building effective agents" taxonomy is a standard system-design vocabulary.
- **What it teaches:** Each pattern with what it trades: latency for accuracy, cost-aware routing to small models, guardrails run in parallel, and when an evaluator loop is worth it.

### L6-c · Self-reflection often makes it worse; external verifiers help **must-watch**

40:50 to 45:10, 4.3 min · design-patterns, evaluation

https://www.youtube.com/watch?v=JC_pLC5EX_w&t=2450s

- **For the job:** The "ask it to check its own work" trap, with the paper that answers it.
- **What it teaches:** "Large Language Models Cannot Self-Correct Reasoning Yet", and CRITIC: a verifier with tools beats self-review.

### L6-d · CodeAct: code as the action

45:10 to 48:48, 3.6 min · tools, design-patterns

https://www.youtube.com/watch?v=JC_pLC5EX_w&t=2710s

- **For the job:** Tool-call design comes up in harness interviews; code-as-action wins on success and turns.
- **What it teaches:** One program with loops and min() instead of a dozen JSON tool calls.

### L6-e · Context engineering: keep it focused, keep it continuous

55:40 to 58:49, 3.1 min · context-engineering

https://www.youtube.com/watch?v=JC_pLC5EX_w&t=3340s

- **For the job:** Prompt and context engineering appears in four of ten harness postings.
- **What it teaches:** Lost in the middle, keeping only what the task needs, and preserving goals, constraints and the KV cache.

### L6-f · Keep a persistent event log

58:49 to 61:42, 2.9 min · context-engineering, observability

https://www.youtube.com/watch?v=JC_pLC5EX_w&t=3529s

- **For the job:** The design behind auditability and observability in production agents.
- **What it teaches:** OpenHands rebuilds every prompt from a full event stream, so compaction never loses the record and hooks can observe.

### L6-g · Compaction or observation masking **must-watch**

63:07 to 67:27, 4.3 min · context-engineering, cost

https://www.youtube.com/watch?v=JC_pLC5EX_w&t=3787s

- **For the job:** A scenario question waiting to happen: context is too long, what do you drop?
- **What it teaches:** Observations are most of the tokens; masking them is simpler than summarizing and about as good, with KV-cache trade-offs.

### L6-h · Context isolation: sub-agents, skills and progressive disclosure

67:27 to 71:09, 3.7 min · context-engineering, skills

https://www.youtube.com/watch?v=JC_pLC5EX_w&t=4047s

- **For the job:** How skills differ from tools, a question people get wrong.
- **What it teaches:** Sub-agents flood their own context and report back; skills list names up front and load contents on demand.

### L6-i · Pi, the minimal harness: strong models need simple harnesses, weak ones need better ones **must-watch**

72:12 to 76:35, 4.4 min · harness, safety

https://www.youtube.com/watch?v=JC_pLC5EX_w&t=4332s

- **For the job:** Harness engineering in one sentence, and the safety cost of having no permission prompts.
- **What it teaches:** Four default tools, an event-log tree, skills, compaction, no safeguards, and why it works anyway.
- **The human part:** "The best models need a very simple harness, but bad models need better harnesses." Deciding how much harness a model needs is a measured judgment.

## Lecture 7, Michael Ryan: How AI Agent Memory Works: MemGPT & Memory Types

https://www.youtube.com/watch?v=qh5tP6PBZ6U

### L7-a · Why agents need memory

2:43 to 6:32, 3.8 min · memory

https://www.youtube.com/watch?v=qh5tP6PBZ6U&t=163s

- **For the job:** Context layers and customer memory are named in agent postings. This is the problem statement.
- **What it teaches:** Lost procedure, lost knowledge, lost progress; personalization, learning from experience, statefulness.

### L7-b · Four kinds of memory: working, episodic, semantic, procedural **must-watch**

6:32 to 11:30, 5.0 min · memory

https://www.youtube.com/watch?v=qh5tP6PBZ6U&t=392s

- **For the job:** The vocabulary an interviewer expects when you describe a memory system.
- **What it teaches:** The context window is working memory; logs are episodic; facts are semantic; skill files are procedural.

### L7-c · When memories conflict, and when memory belongs in the weights

18:31 to 20:44, 2.2 min · memory, optimization

https://www.youtube.com/watch?v=qh5tP6PBZ6U&t=1111s

- **For the job:** A good follow-up answer: context usually overrides weights; facts go in context, skills can go in weights.
- **What it teaches:** Why fine-tuning facts needs thousands of documents and is lossy, while RL on a task can improve procedure.

### L7-d · Often the best memory is just a file system

27:40 to 28:22, 0.7 min · memory, harness

https://www.youtube.com/watch?v=qh5tP6PBZ6U&t=1660s

- **For the job:** The simple answer that strong models make possible, and the trade-off (latency).
- **What it teaches:** Set up the simplest thing and let the model run the show; reach for fancier systems only for a reason.

### L7-e · Skills as procedural memory: Voyager's skill library

31:38 to 36:13, 4.6 min · memory, skills

https://www.youtube.com/watch?v=qh5tP6PBZ6U&t=1898s

- **For the job:** Skills, the format Claude Code and others now use, have a research lineage. Know it.
- **What it teaches:** Write code for a task, keep it if the environment confirms success, retrieve it by description later.

### L7-f · On MemoryArena, the memory agents scored worst

72:00 to 73:48, 1.8 min · memory, evaluation

https://www.youtube.com/watch?v=qh5tP6PBZ6U&t=4320s

- **For the job:** Evidence that "add a memory system" is not automatically better. Measure it.
- **What it teaches:** Long context, memory agents and RAG compared on group travel planning with growing constraints.

### L7-g · Open problems in memory: what to keep, poisoned memories, privacy, over-personalization **must-watch**

74:31 to 78:30, 4.0 min · memory, safety

https://www.youtube.com/watch?v=qh5tP6PBZ6U&t=4471s

- **For the job:** An agent that remembers customer data needs answers to exactly these questions.
- **What it teaches:** Ambiguous things to remember, memory injection attacks, leaking private context, and the model that over-uses what it remembers.
- **The human part:** What should be remembered, and what must never be shared, is a call about the customer that a person makes.

## Lecture 8, Michael Ryan: Multi-Agent Systems: When More Agents Help or Hurt

https://www.youtube.com/watch?v=TlX_ft_PQIM

### L8-a · What multi-agent buys you, and what it costs

5:14 to 10:29, 5.2 min · multi-agent

https://www.youtube.com/watch?v=TlX_ft_PQIM&t=314s

- **For the job:** Multi-agent orchestration is a named requirement. Know the benefits and the five drawbacks.
- **What it teaches:** Parallelism, specialization and isolated context against coordination overhead, information loss, conflicting actions, error propagation and complexity.

### L8-b · One agent often beats many: start with a strong single-agent baseline **must-watch**

10:29 to 13:17, 2.8 min · multi-agent, evaluation

https://www.youtube.com/watch?v=TlX_ft_PQIM&t=629s

- **For the job:** The trap interviewers set is "add more agents". Google's scaling study says single agents often win.
- **What it teaches:** When to prefer one agent (dependent steps, coupled work, already good enough) and when to try many (parallel, divisible work).
- **The human part:** Deciding whether the work divides is a judgment about the task, made before any agent runs.

### L8-c · Who decides to spawn sub-agents, and why it always costs more **must-watch**

13:17 to 15:04, 1.8 min · multi-agent, cost

https://www.youtube.com/watch?v=TlX_ft_PQIM&t=797s

- **For the job:** Cost and latency show up in a third of harness postings. Every sub-agent reloads the whole context.
- **What it teaches:** Today you still have to tell a coding agent to fan out; multi-agent almost always costs more than single-agent.

### L8-d · The architecture depends on the task, and so does the bill

23:15 to 24:45, 1.5 min · multi-agent, cost

https://www.youtube.com/watch?v=TlX_ft_PQIM&t=1395s

- **For the job:** A one-minute answer to "which orchestration pattern?": it depends on the task, and the cost ladder runs single, orchestrator, swarm.
- **What it teaches:** Decentralized agents won on finance documents and fell apart on planning tasks.

### L8-e · Why multi-agent systems fail **must-watch**

69:10 to 73:51, 4.7 min · multi-agent, evaluation

https://www.youtube.com/watch?v=TlX_ft_PQIM&t=4150s

- **For the job:** Failure modes are what scenario interviews are made of.
- **What it teaches:** The failure taxonomy (system design, inter-agent misalignment, verification) and CooperBench's expectation, commitment and communication failures.

### L8-f · Swarms that all build ray tracers, and one that kicks the others off

73:51 to 77:20, 3.5 min · multi-agent, safety

https://www.youtube.com/watch?v=TlX_ft_PQIM&t=4431s

- **For the job:** A memorable safety story for an interview about agents acting with permissions.
- **What it teaches:** Conformity (no diversity of thought) and conflicting goals settled by force, passivity or truce.

## Lecture 9, Michael Ryan: Optimizing AI Agents: Prompts vs. Weights (GEPA, GRPO)

https://www.youtube.com/watch?v=e_m99aR7_3Q

### L9-a · Is prompt work still needed? Last-mile adaptation

4:21 to 7:28, 3.1 min · optimization, context-engineering

https://www.youtube.com/watch?v=e_m99aR7_3Q&t=261s

- **For the job:** A common interview question: "won't better models make this unnecessary?" Here is a defensible answer.
- **What it teaches:** The three pillars (system, data, metric), and context optimization as last-mile adaptation rather than fiddling with wording.

### L9-b · When to optimize: evals carry intent you could not write down **must-watch**

7:28 to 10:14, 2.8 min · optimization, evaluation, human-role

https://www.youtube.com/watch?v=e_m99aR7_3Q&t=448s

- **For the job:** Explains when automatic optimization pays: reliability, domain fit, cheaper models, and re-optimizing when a new model ships.
- **What it teaches:** Examples and feedback communicate requirements a prompt leaves out.
- **The human part:** Your taste and hidden requirements get into the system through the eval set.

### L9-c · Agents that rewrite their own harness: meta-harness and autoresearch **must-watch**

76:31 to 78:38, 2.1 min · optimization, self-improvement, harness

https://www.youtube.com/watch?v=e_m99aR7_3Q&t=4591s

- **For the job:** Harness engineering pointed at itself. Know the meta-harness and autoresearch ideas by name.
- **What it teaches:** An agent proposing, running and keeping or reverting its own changes, scored on Terminal-Bench.
- **The human part:** "The metric and eval become the most critical part to control." When the AI improves the AI, the person owns the metric.

### L9-d · Prompts or weights: how to choose

78:38 to 80:31, 1.9 min · optimization

https://www.youtube.com/watch?v=e_m99aR7_3Q&t=4718s

- **For the job:** A crisp decision list for the "fine-tune or prompt?" question.
- **What it teaches:** Context optimization for API models, frequent re-runs and expensive rollouts; weights for small models, distillation and contexts that keep growing.

## Guest lecture, Alex Shaw & Ryan Marten: Terminal-Bench: Evaluating AI Agents

https://www.youtube.com/watch?v=7GW-9ug2nvw

### G1-a · Outputs are the new source of truth **must-watch**

12:30 to 16:44, 4.2 min · evaluation

https://www.youtube.com/watch?v=7GW-9ug2nvw&t=750s

- **For the job:** Every harness posting asks for evaluation. This is the argument for why: generated code is judged by what it does, not by reading it.
- **What it teaches:** Chollet's point that agentic coding is a form of machine learning, and the shift of the developer's job from specifying toward evaluating.
- **The human part:** The person's work moves from writing the program to deciding what correct looks like.

### G1-b · Writing an eval task: the instruction and the environment

30:40 to 34:13, 3.5 min · evaluation

https://www.youtube.com/watch?v=7GW-9ug2nvw&t=1840s

- **For the job:** "Every agent you own has an eval suite" is a must-have in agent roles. This is how Terminal-Bench writes one task.
- **What it teaches:** Fully specified, concise, natural instructions; environments that match production; internet access as a trade-off; baking state in to cut flakiness.

### G1-c · Verifiers are the hardest part, and reward hacking **must-watch**

37:02 to 41:40, 4.6 min · evaluation, guardrails

https://www.youtube.com/watch?v=7GW-9ug2nvw&t=2222s

- **For the job:** Interviewers probe evals that agents game. This names the defences: one-to-one requirement coverage, separate verifier containers, judges that are themselves evaluated.
- **What it teaches:** A verifier is a classifier with false positives and negatives; model-based verifiers trade away determinism; reward hacking never ends.

### G1-d · Where a person has the most leverage: the verifier's decision boundary **must-watch**

68:42 to 71:55, 3.2 min · evaluation, human-role

https://www.youtube.com/watch?v=7GW-9ug2nvw&t=4122s

- **For the job:** The best answer to "what do you bring when the AI writes the code?": you decide what passes.
- **What it teaches:** Offline evals from online observation, why one observed example is one data point, and why a little human work on a verifier pays across thousands of trials.
- **The human part:** "This job of the evaluator is probably the point of highest leverage for people." A health-care front desk is the student's example.

### G1-e · Publish the traces, not a score

71:55 to 73:05, 1.2 min · evaluation, observability

https://www.youtube.com/watch?v=7GW-9ug2nvw&t=4315s

- **For the job:** Observability and honest reporting: agent behaviour is high-dimensional, and a single score hides reward hacks and slop.
- **What it teaches:** Why the community found reward hacks and bloated code only because full traces were released.
