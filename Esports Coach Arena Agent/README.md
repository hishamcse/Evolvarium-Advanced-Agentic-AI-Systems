# Esports Coach Arena Agent

## What This Agent Does

This project implements a **persistent esports coaching war room** built on **LangGraph + MCP** using a local **Ollama** model. A player opens an arena session, picks a game title and role, and asks for help such as:

- `Prepare my team for a playoff series.`
- `The opponent plays fast. Give me a safer opener.`
- `I need a better draft and a stronger reset protocol.`
- `Build a practice block around our best comfort look.`

In plain language, this is an **AI coaching staff simulator**. It is not just one chatbot giving generic advice. A head coach orchestrates multiple specialist agents, each with a separate job:

- a **Meta Analyst** reads the current patch and dominant trends
- an **Opponent Scout** identifies punish windows and danger zones
- a **Draft Coach** builds pick-ban-veto logic
- a **Mechanics Coach** designs the practice block
- a **Mindset Coach** prepares the comms and reset plan

The head coach then combines all of that into one final match plan and saves it as a persistent arena session.

---

## Why This Is A Strong Visitor-Facing Agent

This one works because it creates a clear fantasy for the user:

- the user feels like they are entering a real analyst desk
- the output is practical and game-specific instead of generic motivation
- the architecture is visibly multi-agent, not just one hidden prompt
- the UI feels like an esports prep room instead of a normal dashboard
- it is replayable across different titles, roles, and pressure scenarios

---

## Architecture Pattern

This agent uses an **Orchestration / Supervisor Architecture**.

```text
User request / Start session
        |
        v
┌──────────────────────────────┐
│ Bootstrap Node               │  creates or reloads persistent arena state
│                              │  via custom MCP esports server
└──────────────┬───────────────┘
               |
               v
┌──────────────────────────────┐
│ Meta Analyst Agent           │  reads patch trends and current meta leverage
└──────────────┬───────────────┘
               |
               v
┌──────────────────────────────┐
│ Opponent Scout Agent         │  studies enemy tempo, tendencies, and punish windows
└──────────────┬───────────────┘
               |
               v
┌──────────────────────────────┐
│ Draft Coach Agent            │  builds draft, veto, or signature-game plan
└──────────────┬───────────────┘
               |
               v
┌──────────────────────────────┐
│ Mechanics Coach Agent        │  designs the warmup and training circuit
└──────────────┬───────────────┘
               |
               v
┌──────────────────────────────┐
│ Mindset Coach Agent          │  prepares comms discipline and reset rules
└──────────────┬───────────────┘
               |
               v
┌──────────────────────────────┐
│ Head Coach Agent             │  synthesizes one decisive match plan
└──────────────┬───────────────┘
               |
               v
┌──────────────────────────────┐
│ Arena Host Node              │  presents the final user-facing prep brief
└──────────────┬───────────────┘
               |
               v
┌──────────────────────────────┐
│ Critic + Persist             │  checks completeness and saves logs/snapshots
└──────────────────────────────┘
```

This is different from the previous single-director agents because the reasoning is intentionally divided by coaching specialty.

---

## What The Visitor Actually Experiences

Example flow:

1. The visitor chooses `Valorant`, `League of Legends`, or `Counter-Strike 2`.
2. They set a role, rank, and focus mode such as tournament prep or playoff week.
3. They ask for a match plan.
4. The hidden coaching staff runs specialist analyses across meta, scouting, drafting, training, and mindset.
5. The visitor sees an arena-style interface with:
   - a live series confidence board
   - a battlefield view for key maps or zones
   - a draft chamber
   - a practice circuit
   - a comms booth
   - a head-coach podium
6. The session is saved, so they can reload the same coaching room later.

---

## Key Features

| Feature | Description |
|---|---|
| **True orchestration architecture** | `esports_coach_arena.py` uses a LangGraph flow where a head coach supervises multiple specialist agents rather than relying on one hidden planner |
| **Custom MCP esports server** | `esports_server.py` stores persistent arena sessions and exposes tools/resources for meta reads, opponent scouting, draft logic, training design, mindset protocols, and session replay |
| **Persistent arena memory** | Every session is stored in `memory/arenas/<session_id>.json` with title, role, opponent profile, map pool, latest specialist reports, final match plan, and coach timeline |
| **Multi-title support** | The agent currently supports Valorant, League of Legends, and Counter-Strike 2 |
| **Distinct arena UI** | The Gradio interface is built as an esports prep room with a pressure board, battlefield, draft chamber, training circuit, comms booth, replay feed, and head-coach podium |
| **Session replay** | Saved sessions can be reloaded directly from the UI, so visitors can revisit the same series prep room |
| **Output snapshots** | Every run writes the latest arena brief, latest arena state, and session index into the `output/` folder |

---

## MCP Tools and Resources

### Tools

| Tool | Purpose |
|---|---|
| `create_arena_session` | Creates a new persistent coaching session |
| `analyze_meta` | Generates a title-specific meta report |
| `scout_opponent` | Produces scouting intel and punish windows |
| `build_draft_plan` | Builds the pick-ban-veto or signature game plan |
| `design_training_block` | Creates the warmup and practice circuit |
| `issue_mindset_protocol` | Generates a reset and communication plan |
| `lock_match_plan` | Persists the final head-coach plan |
| `append_coach_log` | Saves a timeline event to the session |
| `list_sessions` | Lists saved arena sessions for the UI |

### Resources

| Resource | Purpose |
|---|---|
| `arena://session/{session_id}` | Full saved arena session JSON |
| `arena://summary/{session_id}` | Compact session summary for prompting or dashboards |

---

## Setup Required

1. Create a `.env` file in this folder:

```bash
OLLAMA_BASE_URL=http://localhost:11434/v1
OLLAMA_BASE_MODEL=qwen3:8b
ARENA_TEMPERATURE=0.45
ARENA_MAX_RETRIES=2
```

2. Pull a local model:

```bash
ollama pull qwen3:8b
```

3. Install dependencies:

```bash
pip install gradio langgraph langchain-openai mcp python-dotenv
```

---

## Running The Agent

**CLI mode:**

```bash
python esports_coach_arena.py
```

**Gradio UI:**

```bash
python app.py
```

**Run the MCP esports server directly:**

```bash
python esports_server.py
```

---

## Files

| File | Description |
|---|---|
| `esports_coach_arena.py` | LangGraph orchestration workflow, MCP client, CLI entrypoint |
| `esports_server.py` | FastMCP persistent esports arena server |
| `app.py` | Gradio esports prep room UI |
| `memory/arenas/*.json` | Saved arena sessions |
| `output/latest_arena_brief.md` | Most recent final prep brief |
| `output/latest_arena_state.json` | Most recent saved arena state |
| `output/session_index.json` | Saved session list |

---

## Example Visitor Prompt Ideas

- `We are entering a playoff series and I need a full prep plan.`
- `This opponent plays too fast early. Give me a safer opener and reset rule.`
- `Build the plan around our best comfort look and tell me what to ban.`
- `I want a stronger practice circuit for mid-round decision making.`

---

## UI Arena

<img src="./images/arena 1.png" width="100%" alt="arena" />

<img src="./images/arena 2.png" width="100%" alt="arena" />

<img src="./images/arena 3.png" width="100%" alt="arena" />

<img src="./images/arena 4.png" width="100%" alt="arena" />

<img src="./images/arena 5.png" width="100%" alt="arena" />