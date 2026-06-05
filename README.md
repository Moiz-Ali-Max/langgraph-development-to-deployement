# LangGraph — From Fundamentals to Production

A structured covering LangGraph end-to-end. Each topic lives in its own folder with working code, explanations, and notes

---

## What This Repository Covers

| # | Topic | Folder |
|---|-------|--------|
| 01 | Core Concepts — Nodes, Edges, States | `01-core-concepts/` |
| 02 | LLM with Tool Calling, Chains & Reducers | `02-llm-tools-chains/` |
| 03 | Router and Simple ReAct Agent | `03-router-react-agent/` |
| 04 | Memory, RAG, Fine-Tuning, GraphRAG, AI Agents | `04-memory-rag-agents/` |
| 05 | Agent Deployment, State Schema, State Reducers | `05-deployment-state-schema/` |
| 06 | Multiple Schemas, Filter & Trim Messages, Intro to RAG | `06-schemas-messages-rag/` |
| 07 | Message Summarization, Short-Term Memory with Threads & Checkpointers | `07-summarization-checkpointers/` |
| 08 | External Memory with External DB, Intro to Agentic RAG | `08-external-memory-agentic-rag/` |
| 09 | Streaming in LangGraph, LangGraph Studio, Studio on Windows | `09-streaming-studio/` |
| 10 | Deploying Graphs, Human-in-the-Loop, Breakpoints | `10-deployment-hitl-breakpoints/` |
| 11 | Dynamic Breakpoints, Time Travel, Forking | `11-dynamic-breakpoints-time-travel/` |
| 12 | Command Tool, Parallelization | `12-command-tool-parallelization/` |
| 13 | Sub-Graphs, Map-Reduce in LangGraph | `13-subgraphs-map-reduce/` |
| 14 | Human-in-the-Loop with Interrupt, Long-Term Memory with Store | `14-interrupt-long-term-memory/` |
| 15 | Long-Term Memory, Memory Schema with TrustCall | `15-memory-schema-trustcall/` |
| 16 | Agent with Semantic Memory + Procedural Memory | `16-semantic-procedural-memory/` |
| 17 | Deploying Agent in LangGraph Server | `17-langgraph-server-deploy/` |
| 18 | Dentist Appointment Agent — Dev to Deployment | `18-dentist-agent-full-project/` |
| 19 | Functional API — Basic Workflow & Agentic Patterns | `19-functional-api-basics/` |
| 20 | Functional API — Router & Parallelization Patterns | `20-functional-api-router-parallel/` |
| 21 | Functional API — Orchestrator-Worker, Evaluator-Optimizer, ReAct | `21-functional-api-advanced-patterns/` |

---

## Folder Structure

Each folder follows the same layout:

```
XX-topic-name/
    README.md          # Concept explanation, what the code does, and why
    main.py            # Runnable example (or notebook)
    requirements.txt   # Dependencies specific to this section
    notes.md           # Additional notes, gotchas, and references
```

---

## Prerequisites

- Python 3.10+
- Basic familiarity with Python and async concepts
- An OpenAI or Anthropic API key (noted per section where required)
- LangChain / LangGraph installed (`pip install langgraph langchain`)

---

## How to Use This Repo

Clone the repo and work through folders in order. Each folder is self-contained, you can run its code independently without needing the others. The README inside each folder explains the concept before the code, so read that first.

```bash
git clone https://github.com/Moiz-Ali-Max/langgraph-development-to-deployement.git
```

There is no single entry point navigate to the topic you want and follow its README.

---

## Progression Overview

The content is split into three rough phases:

**Foundations (01–06)**: How LangGraph works: nodes, edges, state, tools, reducers, and basic RAG. No assumptions made; everything is built from first principles.

**Memory & Retrieval (07–09)**: Short-term memory via checkpointers, external databases, agentic RAG, streaming, and working with LangGraph Studio.

**Production & Advanced Patterns (10–21)**: Human-in-the-loop, time travel, long-term memory, sub-graphs, the Functional API, and two end-to-end deployment walkthroughs.

---

## License

MIT