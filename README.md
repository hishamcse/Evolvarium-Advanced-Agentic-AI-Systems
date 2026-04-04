<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0a0d12,50:1a2a4a,100:2b6cb0&height=200&section=header&text=Evolvarium%20Agent%20Forge&fontSize=42&fontColor=63b3ed&fontAlignY=38&desc=7%20Advanced%20Agentic%20AI%20Systems%20%C2%B7%207%20Distinct%20Architectures&descAlignY=58&descSize=16&descColor=6b7a99" width="100%"/>

<br/>

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![LangGraph](https://img.shields.io/badge/LangGraph-0.2+-1C3A5E?style=for-the-badge&logo=langchain&logoColor=white)](https://langchain-ai.github.io/langgraph/)
[![Ollama](https://img.shields.io/badge/Ollama-Local_LLM-000000?style=for-the-badge&logo=ollama&logoColor=white)](https://ollama.ai)
[![Gradio](https://img.shields.io/badge/Gradio-UI-FF7C00?style=for-the-badge&logo=gradio&logoColor=white)](https://gradio.app)
[![MCP](https://img.shields.io/badge/MCP-Tool_Servers-6B46C1?style=for-the-badge)](https://modelcontextprotocol.io)

<br/>

> **Not a prompt wrapper collection.**
> Every agent here runs a real graph topology — fan-out, genetic loop, adversarial debate, Bayesian cascade, orchestration, plan-then-execute. Each one is a self-contained product with its own MCP tool server, persistent memory, and a purpose-built UI.

<br/>

[**Explore Agents ↓**](#-agents) · [**Architecture Patterns ↓**](#-architecture-patterns) · [**Quick Start ↓**](#-quick-start)

</div>

---

## What This Is

A hands-on collection of advanced agentic AI systems — every agent uses a **different graph topology** — orchestration, parallel blind evaluation, plan-then-execute, parallel fan-out, genetic loops, adversarial debate, and cascading Bayesian refinement. The repo is designed to be a reference for real-world agentic patterns, not just prompt wrappers.

Each agent also ships with:
- A **custom MCP tool server** it calls during graph execution
- **Persistent JSON memory** so sessions survive restarts
- A **rich Gradio UI** designed specifically for that agent's domain — not a generic chat box
- A **full README** explaining the architecture, graph nodes, and design decisions

No cloud API required. Everything runs on a local **Ollama** model. Paid models (GPT-4o, Claude) produce sharper output but are not needed to run.

---

## 🎯 What You Can Actually Do With This

This is not just a learning repo. You can use these today:

- 👨‍💼 Evaluate candidates with a multi-agent hiring committee
- 🧬 Improve code using a genetic mutation loop
- 🔍 Run structured multi-agent code reviews
- ⚖️ Simulate debates and decision systems
- 🩺 Explore AI-assisted differential diagnosis (research)
- 🎮 Generate esports match strategies
- 🚀 Plan and validate a startup launch strategy

Each system is interactive, visual, and stateful — not a CLI toy.

---

## 🤖 Agents

| # | Agent | Architecture Pattern | Domain |
|---|---|---|---|
| 1 | [AI Hiring Committee](#1--ai-hiring-committee) | Parallel Blind Evaluation + Aggregator | HR / Talent |
| 2 | [Code Mutation Lab](#2--code-mutation-lab) | Genetic / Evolutionary Loop | Code Quality |
| 3 | [Code Review Arena](#3--code-review-arena) | Parallel Fan-out + Aggregator | Code Review |
| 4 | [Crime Scene Investigator](#4--crime-scene-investigator) | Adversarial Debate + Jury Vote | Investigation |
| 5 | [Medical Differential Engine](#5--medical-differential-engine) | Cascading Bayesian Refinement | Clinical Reasoning |
| 6 | [Esports Coach Arena](#6--esports-coach-arena) | Orchestration / Supervisor | Esports Coaching |
| 7 | [Launchpad Strategist](#7--launchpad-strategist) | Plan-then-Execute | Startup Strategy |

---

## 🏛 Architecture Patterns

The entire point of this repo is to show that **topology matters**. Here is how the seven patterns differ:

```
┌────────────────────────────────────────────────────────────────────────────────┐
│  PATTERN                    GRAPH SHAPE           WHEN TO USE                  │
├────────────────────────────────────────────────────────────────────────────────┤
│  Parallel Blind Eval    [A]─[B]─[C]─[D] → AGG    Independent scoring, no bias  │
│  Parallel Fan-out       [A]─[B]─[C]─[D] → AGG    Parallel specialist review    │
│  Genetic Loop            SEED → MUT → EVAL → SEL  Iterative optimisation       │
│                               ↑____________|                                   │
│  Adversarial Debate     FOR → AGN → FOR → JUDGE   Structured opposing views    │
│  Bayesian Cascade       L0→L1→L2→L3→L4→L5        Probability narrowing         │
│  Orchestration          HEAD→[S1→S2→S3→S4→S5]    Supervisor + specialists      │
│  Plan-then-Execute      PLAN→[E1→E2→E3→E4]→CRIT  Planned execution order       │
└────────────────────────────────────────────────────────────────────────────────┘
```

The key distinction between **Parallel Blind Evaluation** (Hiring) and **Parallel Fan-out** (Code Review) is isolation: in the hiring committee, evaluators never see each other's output. In code review, the aggregator synthesises all outputs simultaneously. Same graph shape, different information flow — different result quality.

---

## ⚡ Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/hishamcse/Evolvarium-Advanced-Agentic-AI-Systems
cd Evolvarium-Advanced-Agentic-AI-Systems

# 2. Install uv (if not already installed)
pip install uv
uv sync

# 3. Start Ollama and pull a model
ollama serve
ollama pull qwen3:8b      # or llama3.1:8b, mistral, etc.

# 4. Pick any agent and run it
cd "Crime Scene Investigator"
uv run app.py             # opens at http://localhost:7860
```

Each agent is fully self-contained. No shared dependencies to manage.

### Environment

```env
# .env inside any agent folder
OLLAMA_BASE_URL=http://localhost:11434/v1
OLLAMA_BASE_MODEL=qwen3:8b
......
...... Other Fields ........
```

---

## 1 · AI Hiring Committee

> **Pattern:** Parallel Blind Evaluation + Chair Aggregation

Four specialist evaluators score a candidate simultaneously — without seeing each other's output. Blind isolation prevents anchoring bias. A chair agent then synthesises all four perspectives into a final hiring decision with a weighted score and full reasoning.

**Why the architecture matters:** If evaluators saw each other's scores, the first score would anchor everything else. Parallel blind evaluation eliminates this and produces genuinely independent signal.

**Graph:**
```
bootstrap ──→ [technical ‖ manager ‖ culture ‖ advocate]  (parallel, blind)
                              ↓
                           chair  ──→  persist
```

**Agents:** Technical Lead · Hiring Manager · Culture Fit · Devil's Advocate · Chair

<p align="center"><img src="./AI Hiring Commitee/images/hiring_committee_architecture.svg" width="72%"/></p>

→ [Full architecture deep-dive](./AI%20Hiring%20Commitee/README.md) &nbsp;·&nbsp; `cd "AI Hiring Commitee" && uv run app.py`

<details>
<summary><b>View UI screenshots</b></summary>

<img src="./AI Hiring Commitee/images/hire 1.png" width="100%"/>
<img src="./AI Hiring Commitee/images/hire 2.png" width="100%"/>
<img src="./AI Hiring Commitee/images/hire 3.png" width="100%"/>
<img src="./AI Hiring Commitee/images/hire 4.png" width="100%"/>
<img src="./AI Hiring Commitee/images/hire 5.png" width="100%"/>

</details>

---

## 2 · Code Mutation Lab

> **Pattern:** Genetic / Evolutionary Loop

Code enters as a seed. Each generation, three variants compete using distinct mutation strategies. They are each scored by three independent evaluator agents across performance, readability, and simplicity. The fittest variant becomes the seed for the next generation. Repeat.

**Why the architecture matters:** A single rewrite prompt has no selection pressure. The loop does. Fitness scores are tracked across every generation — you can watch the code improve (or regress) round by round.

**Graph:**
```
seed ──→ mutator ──→ [perf_eval ‖ read_eval ‖ simp_eval]  (per variant)
              ↑              ↓
           selector ←── scored_variants
              ↓
         controller ──→ continue | end
```

**Mutation strategies (6 total, 3 per generation, no repeats):**
`performance` · `readability` · `memory reduction` · `pythonic refactor` · `logic simplify` · `functional style`

<p align="center"><img src="./Code Mutation Lab/images/code_mutation_lab_architecture.svg" width="100%"/></p>

→ [Full architecture deep-dive](./Code%20Mutation%20Lab/README.md) &nbsp;·&nbsp; `cd "Code Mutation Lab" && uv run app.py`

<details>
<summary><b>View UI screenshots</b></summary>

<img src="./Code Mutation Lab/images/lab 1.png" width="100%"/>
<img src="./Code Mutation Lab/images/lab 2.png" width="100%"/>
<img src="./Code Mutation Lab/images/lab 3.png" width="100%"/>
<img src="./Code Mutation Lab/images/lab 4.png" width="100%"/>

</details>

---

## 3 · Code Review Arena

> **Pattern:** Parallel Fan-out + Aggregator

Four specialist agents review code simultaneously — each owns one domain and nothing else. The aggregator reads all four outputs and produces a single weighted report with severity classification, a composite score, and an executive summary.

**Why the architecture matters:** Sequential review means each agent is influenced by what the previous agent found. Parallel execution means four truly independent signals. The aggregator's job is synthesis, not review — that separation is what produces coherent output.

**Graph:**
```
bootstrap ──→ [security ‖ performance ‖ logic ‖ style]  (parallel)
                              ↓
                         aggregator ──→ persist
```

**Agents:** Security Reviewer · Performance Reviewer · Logic Reviewer · Style Reviewer · Aggregator

<p align="center"><img src="./Code Review Arena/images/code_review_arena_architecture.svg" width="72%"/></p>

→ [Full architecture deep-dive](./Code%20Review%20Arena/README.md) &nbsp;·&nbsp; `cd "Code Review Arena" && uv run app.py`

<details>
<summary><b>View UI screenshots</b></summary>

<img src="./Code Review Arena/images/code review 1.png" width="100%"/>
<img src="./Code Review Arena/images/code review 2.png" width="100%"/>
<img src="./Code Review Arena/images/code review 3.png" width="100%"/>

</details>

---

## 4 · Crime Scene Investigator

> **Pattern:** Adversarial Debate + Jury Vote

Four agents argue a criminal case. The forensics agent analyses evidence with zero bias. The prosecutor builds the case for guilt. The defense agent reads the prosecution's argument and systematically dismantles it. The judge weighs both sides independently and returns a structured JSON verdict — confidence score, key evidence, reasonable doubts, and a closing statement. Noir UI.

**Why the architecture matters:** The sequential dependency between prosecution and defense is intentional. Defense can only be effective if it directly reads and challenges the prosecution's argument. The judge then weighs a real debate, not two independent monologues.

**Graph:**
```
bootstrap ──→ forensics ──→ prosecution ──→ defense ──→ judge ──→ persist
```

**Agents:** Forensics · Prosecutor · Defense · Judge

<p align="center"><img src="./Crime Scene Investigator/images/csi_architecture.svg" width="72%"/></p>

→ [Full architecture deep-dive](./Crime%20Scene%20Investigator/README.md) &nbsp;·&nbsp; `cd "Crime Scene Investigator" && uv run app.py`

<details>
<summary><b>View UI screenshots</b></summary>

<img src="./Crime Scene Investigator/images/crime 1.png" width="100%"/>
<img src="./Crime Scene Investigator/images/crime 2.png" width="100%"/>
<img src="./Crime Scene Investigator/images/crime 3.png" width="100%"/>
<img src="./Crime Scene Investigator/images/crime 4.png" width="100%"/>
<img src="./Crime Scene Investigator/images/crime 5.png" width="100%"/>

</details>

---

## 5 · Medical Differential Engine

> **Pattern:** Cascading Bayesian Refinement ← unique to this repo

The only agent in this collection with a genuinely novel architecture. Symptoms enter as a signal. A probability distribution is initialised and then updated at each layer — prior probabilities from epidemiology, rare disease injection, comorbidity likelihood ratio modifiers, and finally a full posterior update from the clinical examination. Each agent reads and updates the shared distribution before passing it forward. The differential collapses to a ranked, confidence-scored assessment.

**Why the architecture matters:** This is not fan-out. This is not a sequential chain. Each node changes the probability distribution that the next node receives. The cascade is the architecture. Compare what L1 believes versus what L5 believes — the delta is the reasoning.

**Graph (cascade — each node mutates shared P(dx)):**
```
bootstrap → symptom_parser → prior_scorer → rare_probe
         → comorbidity_mapper → evidence_weigher → ranker → persist

L0: feature extraction (no probabilities yet)
L1: P(dx) = epidemiological prior
L2: P(dx) updated with rare disease injection
L3: P(dx) × comorbidity likelihood ratios
L4: P(dx) updated with examination posterior
L5: ranked differential + workup plan + disposition
```

**Agents:** Symptom Parser · Prior Scorer · Rare Disease Probe · Comorbidity Mapper · Evidence Weigher · Differential Ranker

**UI tabs:** Differential · Workup & Flags · Cascade Trace · Probability Evolution

<p align="center"><img src="./Medical Differential Engine/images/mde_architecture.svg" width="100%"/></p>

> ⚠️ Research tool demonstrating LangGraph patterns. Not a medical device. Not for clinical use.

→ [Full architecture deep-dive](./Medical%20Differential%20Engine/README.md) &nbsp;·&nbsp; `cd "Medical Differential Engine" && uv run app.py`

<details>
<summary><b>View UI screenshots</b></summary>

<img src="./Medical Differential Engine/images/medical 1.png" width="100%"/>
<img src="./Medical Differential Engine/images/medical 2.png" width="100%"/>
<img src="./Medical Differential Engine/images/medical 3.png" width="100%"/>
<img src="./Medical Differential Engine/images/medical 4.png" width="100%"/>
<img src="./Medical Differential Engine/images/medical 5.png" width="100%"/>

</details>

---

## 6 · Esports Coach Arena

> **Pattern:** Orchestration / Supervisor

A head coach activates five specialist sub-agents in sequence, each owning one domain of match preparation. No agent works without the previous one completing first — each output feeds the next. The head coach then synthesises everything into one decisive match plan, saved as a persistent arena session. Supports Valorant, League of Legends, and CS2.

**Why the architecture matters:** This is not the same as a sequential chain. The head coach decides which specialist to activate and in what context — it is a supervisor directing specialists, not a pipeline processing a document. The MCP esports tool server gives agents structured access to game-specific data.

**Graph:**
```
bootstrap → meta_analyst → opponent_scout → draft_coach
         → mechanics_coach → mindset_coach → head_coach → persist
```

**Agents:** Meta Analyst · Opponent Scout · Draft Coach · Mechanics Coach · Mindset Coach · Head Coach

<p align="center"><img src="./Esports Coach Arena Agent/images/esports_coach_architecture.svg" width="100%"/></p>

→ [Full architecture deep-dive](./Esports%20Coach%20Arena%20Agent/README.md) &nbsp;·&nbsp; `cd "Esports Coach Arena Agent" && uv run app.py`

<details>
<summary><b>View UI screenshots</b></summary>

<img src="./Esports Coach Arena Agent/images/arena 1.png" width="100%"/>
<img src="./Esports Coach Arena Agent/images/arena 2.png" width="100%"/>
<img src="./Esports Coach Arena Agent/images/arena 3.png" width="100%"/>
<img src="./Esports Coach Arena Agent/images/arena 4.png" width="100%"/>
<img src="./Esports Coach Arena Agent/images/arena 5.png" width="100%"/>

</details>

---

## 7 · Launchpad Strategist

> **Pattern:** Plan-then-Execute

The key distinction from orchestration: here, a **planner agent runs first** and decides the execution sequence before any executor fires. The planner produces a structured plan; executors carry it out in planned order. A critic then validates the final brief before it is persisted. Startup founders get a full launch board — market angle, ICP, messaging, and a go-live runway.

**Why the architecture matters:** In orchestration, the supervisor directs as it goes. In plan-then-execute, the plan is committed upfront. This matters because it allows the plan to be inspected, overridden, or modified before execution begins — a critical property for high-stakes output.

**Graph:**
```
bootstrap → planner → market_mapper → icp_builder
         → messaging_writer → timeline_builder → launch_operator → critic → persist
```

**Agents:** Planner · Market Mapper · ICP Builder · Messaging Writer · Timeline Builder · Launch Operator · Critic

<p align="center"><img src="./Launchpad Strategist Agent/images/launchpad_strategist_architecture.svg" width="100%"/></p>

→ [Full architecture deep-dive](./Launchpad%20Strategist%20Agent/README.md) &nbsp;·&nbsp; `cd "Launchpad Strategist Agent" && uv run app.py`

<details>
<summary><b>View UI screenshots</b></summary>

<img src="./Launchpad Strategist Agent/images/launch 1.png" width="100%"/>
<img src="./Launchpad Strategist Agent/images/launch 2.png" width="100%"/>
<img src="./Launchpad Strategist Agent/images/launch 3.png" width="100%"/>
<img src="./Launchpad Strategist Agent/images/launch 4.png" width="100%"/>
<img src="./Launchpad Strategist Agent/images/launch 5.png" width="100%"/>

</details>

---

## 📐 Architecture Comparison

| Agent | Graph Shape | Parallel? | Loop? | Debate? | Bayesian? | MCP? |
|---|---|---|---|---|---|---|
| AI Hiring Committee | Fan-out → aggregator | ✅ blind parallel | — | — | — | ✅ |
| Code Review Arena | Fan-out → aggregator | ✅ open parallel | — | — | — | ✅ |
| Code Mutation Lab | Cycle | — | ✅ genetic | — | — | — |
| Crime Scene Investigator | Sequential chain | — | — | ✅ | — | ✅ |
| Medical Differential Engine | Sequential cascade | — | — | — | ✅ | ✅ |
| Esports Coach Arena | Supervisor chain | — | — | — | — | ✅ |
| Launchpad Strategist | Plan + exec chain | — | — | — | — | ✅ |

**Difference between the two fan-out agents:** In AI Hiring Committee, evaluators run in parallel and are completely isolated — no agent sees another's output before forming its own score. In Code Review Arena, agents also run in parallel but the aggregator synthesises all four outputs simultaneously. Same graph shape, different information access pattern.

---

## Video Explanation by NotebookLM

https://github.com/user-attachments/assets/a0cd1b4c-af48-4425-a04d-e474e95bde37

---

## ⛯ Mind Map

<img src="./NotebookLM%20Mind%20Map.png" alt="mind-map" />

---

## 📁 Project Structure

```
evolvarium-agent-forge/
│
├── AI Hiring Commitee/
│   ├── app.py                        # Committee room Gradio UI
│   ├── graph.py                      # Parallel blind scoring + chair aggregation
│   ├── mcp_server.py                 # CV parsing, job spec extraction, session storage
│   ├── agents/                       # technical · manager · culture · advocate · chair
│   ├── memory/                       # Persisted sessions (JSON)
│   └── README.md
│
├── Code Mutation Lab/
│   ├── app.py                        # Lab Gradio UI
│   ├── graph/
│   │   ├── builder.py                # LangGraph genetic loop
│   │   ├── state.py                  # MutationState TypedDict
│   │   └── nodes/                    # mutator · evaluator · selector · controller
│   ├── agents/                       # mutate · evaluate · select + evaluators/
│   └── README.md
│
├── Code Review Arena/
│   ├── app.py                        # Arena Gradio UI
│   ├── graph.py                      # Parallel fan-out graph
│   ├── mcp_server.py                 # lint · AST · language detect
│   ├── agents/                       # security · performance · logic · style
│   └── README.md
│
├── Crime Scene Investigator/
│   ├── app.py                        # Noir Gradio UI
│   ├── graph.py                      # Adversarial debate graph
│   ├── mcp_server.py                 # evidence tagging · timeline · case storage
│   ├── agents/                       # forensics · prosecutor · defense · judge
│   └── README.md
│
├── Medical Differential Engine/
│   ├── app.py                        # Clinical dark UI — 4 output tabs
│   ├── graph.py                      # LangGraph Bayesian cascade
│   ├── mcp_server.py                 # red flags · ICD hints · drug interactions
│   ├── agents/
│   │   ├── symptom_parser_agent.py   # L0 — structured feature extraction
│   │   ├── prior_scorer_agent.py     # L1 — epidemiological priors
│   │   ├── rare_disease_probe_agent.py  # L2 — zebra injection
│   │   ├── comorbidity_mapper_agent.py  # L3 — LR modifiers from PMH/meds
│   │   ├── evidence_weigher_agent.py    # L4 — posterior from examination
│   │   └── differential_ranker_agent.py # L5 — final synthesis
│   └── README.md
│
├── Esports Coach Arena Agent/
│   ├── app.py                        # War room Gradio UI
│   ├── esports_coach_arena.py        # LangGraph engine + MCP client
│   ├── esports_server.py             # Custom MCP esports tools server
│   └── README.md
│
├── Launchpad Strategist Agent/
│   ├── app.py                        # Mission control Gradio UI
│   ├── src/launchpad_strategist/
│   │   ├── graph/                    # LangGraph nodes + builder
│   │   ├── mcp/                      # Custom MCP launch tools server
│   │   ├── models/                   # State + schema definitions
│   │   └── prompts/                  # System prompts
│   └── README.md
│
├── requirements.txt
└── README.md
```

---

## 🔧 Tech Stack

| Component | Technology | Purpose |
|---|---|---|
| Graph engine | [LangGraph](https://langchain-ai.github.io/langgraph/) | Agent topology, state, routing |
| LLM backend | [Ollama](https://ollama.ai) (local) | Runs any GGUF model locally |
| LLM interface | [langchain-openai](https://python.langchain.com/docs/integrations/llms/openai/) | OpenAI-compatible API calls to Ollama |
| Tool servers | [MCP](https://modelcontextprotocol.io) | Modular tool exposure per agent |
| UI | [Gradio](https://gradio.app) | Per-agent custom interfaces |
| Persistence | JSON files | Session / case / memory storage |
| Package manager | [uv](https://github.com/astral-sh/uv) | Fast, reproducible Python environments |

---

## 💡 What You Can Learn From This Repo

This isn't a tutorial. It's a reference implementation. The things worth studying:

**Graph topology design** — why does the hiring committee use parallel blind evaluation instead of sequential? Why does the crime scene investigator use sequential instead of parallel? Topology is not aesthetic — it determines what information each agent has access to and when.

**State design** — every agent uses a `TypedDict` state. The Medical Differential Engine's state carries a `List[DiagnosisCandidate]` that is mutated in place across six layers. The Hiring Committee's state carries four independent `eval` dicts that only the chair reads. Good state design makes graph logic trivial.

**MCP tool server pattern** — every agent with an MCP server exposes domain-specific tools that the graph calls synchronously. The CSI server does evidence tagging and timeline extraction. The hiring server does CV parsing and session management. Tools are not decorators on a chat model — they are callable services the graph controls.

**When to loop vs when to chain** — the Code Mutation Lab loops because each generation needs the output of the previous generation as its seed. Every other agent chains because it only needs one pass. Knowing when a loop adds value versus adds latency is a real engineering decision.

---

## Other Related Works

- https://github.com/hishamcse/agentarium-multi-framework-agents
- https://github.com/hishamcse/LinkGenius-AI

---

<div align="center">

**Built by [Syed Jarullah Hisham](https://github.com/hishamcse)**
SDE @ IQVIA · .NET & Agentic AI

<br/>

*If this helped you understand agent systems, consider starring ⭐*

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:2b6cb0,50:1a2a4a,100:0a0d12&height=100&section=footer" width="100%"/>

</div>
