# Evolvarium Agent Forge - Advanced Agentic AI Systems
 
A hands-on collection of advanced agentic AI systems — each one a fully self-contained product with a distinct architecture, a custom MCP tool server, persistent memory, and a rich Gradio UI. Built with **LangGraph** and **local Ollama models**. No paid API keys required. But these agents will work much better and impressive with paid API keys.
 
Every agent uses a **different graph topology** — orchestration, plan-then-execute, parallel fan-out, and genetic loops. The repo is designed to be a reference for real-world agentic patterns, not just prompt wrappers.

---

## Agents

| Agent | Architecture | Tech Stack | What It Does |
|---|---|---|---|
| [Code Mutation Lab](#code-mutation-lab) | Genetic / Evolutionary Loop | LangGraph · Ollama · Gradio | Code enters as a seed. Each generation, 3 strategy-driven variants are mutated, evaluated across performance, readability, and simplicity, and only the fittest survives to seed the next generation. A full fitness timeline and variant explorer track every decision. |
| [Esports Coach Arena](#esports-coach-arena-agent) | Orchestration / Supervisor | LangGraph · MCP (custom esports server) · Ollama · Gradio · JSON persistence | A persistent multi-agent esports war room. A head coach orchestrates 5 specialist agents — meta analyst, opponent scout, draft coach, mechanics coach, and mindset coach — before locking one decisive match plan. Supports Valorant, League of Legends, and CS2. |
| [Code Review Arena](#code-review-arena) | Parallel Fan-out + Aggregator | LangGraph · MCP (lint/AST server) · Ollama · Gradio · JSON persistence | 4 specialist reviewer agents fire in parallel — security, performance, logic, and style — then an aggregator merges all findings into a weighted score, severity-classified issue list, and executive summary. |
| [Launchpad Strategist](#launchpad-strategist-agent) | Plan-then-Execute | LangGraph · MCP (custom launch server) · Ollama · Gradio · JSON persistence | A startup launch copilot. A planner agent sequences execution, then specialist agents handle market mapping, ICP definition, messaging, and timeline. A critic validates the final brief before it is saved as a persistent launch board. |

---

## Architecture patterns used

```
Orchestration / Supervisor   →  Esports Coach Arena
Plan-then-Execute            →  Launchpad Strategist
Parallel Fan-out + Aggregator→  Code Review Arena
Genetic / Evolutionary Loop  →  Code Mutation Lab
```

---

## Details & UI for Agents

### Code Review Arena

> **Architecture:** Parallel Fan-out + Aggregator — 4 reviewer agents run simultaneously via LangGraph's parallel node execution, cutting review time ~4× vs sequential. An aggregator merges all outputs into one weighted report.

<img src="./Code Review Arena/images/code_review_arena_architecture.svg" width="100%" alt="architecture" />

<img src="./Code Review Arena/images/code review 1.png" width="100%" alt="review 1" />

<img src="./Code Review Arena/images/code review 2.png" width="100%" alt="review 2" />

<img src="./Code Review Arena/images/code review 3.png" width="100%" alt="review 3" />

**Run:**
```bash
cd "Code Review Arena"
uv run app.py
```

→ [Full README & architecture](./Code%20Review%20Arena/README.md)

---

### Code Mutation Lab

> **Architecture:** Genetic / Evolutionary Loop — code evolves across generations. Each generation spawns 3 competing variants using distinct mutation strategies, evaluates them in parallel across 3 fitness dimensions, selects the fittest, and uses it as the seed for the next generation.

<img src="./Code Mutation Lab/images/lab 1.png" width="100%" alt="lab 1" />

<img src="./Code Mutation Lab/images/lab 2.png" width="100%" alt="lab 2" />

<img src="./Code Mutation Lab/images/lab 3.png" width="100%" alt="lab 3" />

<img src="./Code Mutation Lab/images/lab 4.png" width="100%" alt="lab 4" />


**Run:**
```bash
cd "Code Mutation Lab"
uv run app.py
```

→ [Full README & architecture](./Code%20Mutation%20Lab/README.md)

---

### Esports Coach Arena Agent

> **Architecture:** Orchestration / Supervisor — a head coach sequentially activates 5 specialist sub-agents, each owning a distinct domain of match preparation.

<img src="./Esports Coach Arena Agent/images/arena 1.png" width="100%" alt="Esports Coach Arena — hero banner" />

<img src="./Esports Coach Arena Agent/images/arena 2.png" width="100%" alt="Esports Coach Arena — pressure board" />

<img src="./Esports Coach Arena Agent/images/arena 3.png" width="100%" alt="Esports Coach Arena — battlefield view" />

<img src="./Esports Coach Arena Agent/images/arena 4.png" width="100%" alt="Esports Coach Arena — match plan" />

<img src="./Esports Coach Arena Agent/images/arena 5.png" width="100%" alt="Esports Coach Arena — agent timeline" />

**Run:**
```bash
cd "Esports Coach Arena Agent"
uv run app.py
```

→ [Full README & architecture](./Esports%20Coach%20Arena%20Agent/README.md)

---

### Launchpad Strategist Agent

> **Architecture:** Plan-then-Execute — a planner agent decides the execution sequence, then individual specialist executors carry out each phase before a critic validates the output.

<img src="./Launchpad Strategist Agent/images/launch 1.png" width="100%" alt="Launchpad Strategist — mission control" />

<img src="./Launchpad Strategist Agent/images/launch 2.png" width="100%" alt="Launchpad Strategist — market analysis" />

<img src="./Launchpad Strategist Agent/images/launch 3.png" width="100%" alt="Launchpad Strategist — ICP definition" />

<img src="./Launchpad Strategist Agent/images/launch 4.png" width="100%" alt="Launchpad Strategist — messaging stack" />

<img src="./Launchpad Strategist Agent/images/launch 5.png" width="100%" alt="Launchpad Strategist — launch board" />

**Run:**
```bash
cd "Launchpad Strategist Agent"
uv run app.py
```

→ [Full README & architecture](./Launchpad%20Strategist%20Agent/README.md)

---

## Project structure

```
agentarium/
├── Esports Coach Arena Agent/
│   ├── app.py                        # Gradio UI
│   ├── esports_coach_arena.py        # LangGraph engine + MCP client
│   ├── esports_server.py             # Custom MCP esports tools server
│   ├── memory/                       # Persistent arena sessions
│   └── README.md
│
├── Launchpad Strategist Agent/
│   ├── app.py                        # Gradio UI
│   ├── src/launchpad_strategist/
│   │   ├── graph/                    # LangGraph nodes + builder
│   │   ├── mcp/                      # Custom MCP launch tools server
│   │   ├── models/                   # State + schema definitions
│   │   ├── prompts/                  # System prompts
│   │   └── services/                 # Engine + model factory
│   ├── memory/                       # Persistent launch sessions
│   └── README.md
│
├── Code Review Arena/
│   ├── app.py                        # Gradio UI
│   ├── graph.py                      # LangGraph graph (parallel fan-out)
│   ├── mcp_server.py                 # MCP tools: lint, AST, language detect
│   ├── agents/                       # 4 specialist reviewer agents
│   ├── state.py                      # LangGraph TypedDict state
│   ├── config.py                     # Env + model config
│   ├── memory/                       # Persisted review sessions
│   └── README.md
│
├── Code Mutation Lab/
│   ├── app.py                        # Gradio UI
│   ├── graph/
│   │   ├── builder.py                # LangGraph graph (genetic loop)
│   │   ├── state.py                  # MutationState TypedDict
│   │   └── nodes/                    # mutator, evaluator, selector, controller
│   ├── agents/
│   │   ├── mutate_agent.py           # Spawns 3 strategy-driven variants
│   │   ├── evaluate_agent.py         # Orchestrates 3 evaluator sub-agents
│   │   ├── select_agent.py           # Picks the fittest variant
│   │   ├── mutation_strategies.py    # 6 named mutation strategies
│   │   └── evaluators/              # performance, readability, simplicity agents
│   ├── llm/model.py                  # Ollama LLM factory
│   └── README.md
|
|── Crime Scene Investigator/
|   ├── config.py
|   ├── state.py
|   ├── mcp_server.py          # case file storage, evidence tools
|   ├── agents/
|   │   ├── prosecutor_agent.py
|   │   ├── defense_agent.py
|   │   ├── forensics_agent.py
|   │   └── judge_agent.py
|   ├── graph.py               # debate flow + jury vote
|   ├── app.py                 # noir Gradio UI
|   └── README.md
|
├── requirements.txt
└── README.md
```
