# Launchpad Strategist Agent

## What This Agent Does

This project is a **launch mission-control copilot** for founders, indie hackers, and product teams. It runs on **LangGraph + MCP + Ollama** and turns a rough launch request into a sharper launch board with:

- a launch plan
- a market angle
- a target audience lock
- a messaging stack
- a rollout timeline
- a final operator brief

The point is not to behave like one general chatbot. This agent uses a **Plan-and-Execute architecture**:

- the **Planner** decides the execution sequence
- specialist executors handle market, ICP, messaging, and timeline work
- the **Launch Operator** merges everything into one launch board
- a **Critic** checks whether the final brief is clear and actionable

---

## Architecture Pattern

```text
User request / startup setup
        |
        v
┌──────────────────────────────┐
│ Bootstrap Node               │  creates or reloads persistent launch state
└──────────────┬───────────────┘
               |
               v
┌──────────────────────────────┐
│ Planner Agent                │  decides the execution order
└──────────────┬───────────────┘
               |
               v
┌──────────────────────────────┐
│ Market Mapper                │  finds whitespace and competitive pressure
└──────────────┬───────────────┘
               |
               v
┌──────────────────────────────┐
│ ICP Builder                  │  defines the sharpest early audience
└──────────────┬───────────────┘
               |
               v
┌──────────────────────────────┐
│ Messaging Writer             │  builds the message stack
└──────────────┬───────────────┘
               |
               v
┌──────────────────────────────┐
│ Timeline Builder             │  creates the launch runway
└──────────────┬───────────────┘
               |
               v
┌──────────────────────────────┐
│ Launch Operator              │  locks one final launch board
└──────────────┬───────────────┘
               |
               v
┌──────────────────────────────┐
│ Critic + Persist             │  reviews clarity and saves the session
└──────────────────────────────┘
```

---

## Visitor Experience

The visitor enters:

- startup name
- product name
- product type
- current stage
- budget posture
- launch goal

Then they ask for help such as:

- `Plan a beta waitlist launch for our AI product.`
- `We need sharper positioning for technical founders.`
- `Give me a low-budget launch sequence with stronger proof.`

The UI responds like a launch war room with:

- a mission banner
- strategy radar
- audience lock panel
- message lab
- runway timeline
- operator command feed

---

## Key Features

| Feature | Description |
|---|---|
| **Plan-and-Execute graph** | the planner decides the execution sequence before specialist nodes run |
| **Custom MCP server** | persistent sessions and reusable launch-analysis tools |
| **Stage-aware launch playbooks** | strategy shifts based on product type, stage, budget posture, launch goal, and request cues like proof-heavy or fast rollout |
| **Mission-control UI** | distinct Gradio interface with strategy radar, signal strip, audience lock, channel mix, proof stack, runway, and operator command board |
| **Persistent memory** | each session is stored and can be reloaded |
| **Standalone structure** | modular `src/` package with smaller files and separated responsibilities |

---

## Setup

1. Create a `.env` file from `.env.example`
2. Make sure Ollama is running locally
3. Pull a local model such as:

```bash
ollama pull qwen3:8b
```

4. Install dependencies if needed (if using uv, skip this):

```bash
pip install gradio langgraph langchain-openai mcp python-dotenv
```

---

## Running

**CLI**

```bash
python run_cli.py
```

**Gradio UI**

```bash
python app.py
```

**MCP server**

```bash
python server.py
```

OR, using uv
```bash
uv run app.py
```

---

## Main Files

| File | Description |
|---|---|
| `app.py` | Gradio entrypoint |
| `run_cli.py` | CLI entrypoint |
| `server.py` | MCP server entrypoint |
| `src/launchpad_strategist/services/engine.py` | main LangGraph execution engine |
| `src/launchpad_strategist/graph/` | graph builder, routing, and node modules |
| `src/launchpad_strategist/mcp/` | MCP client, server, tools, resources |
| `src/launchpad_strategist/ui/` | theme, actions, layout, and dashboard views |
