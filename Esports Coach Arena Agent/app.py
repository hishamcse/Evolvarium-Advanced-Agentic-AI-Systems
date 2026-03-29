import html
import json
import re
from typing import Any, Dict, List, Optional, Tuple

import gradio as gr

from esports_coach_arena import EsportsCoachArenaEngine
from ui.css import APP_CSS


engine = EsportsCoachArenaEngine()

TITLE_CHOICES = ["valorant", "league", "cs2"]
ROLE_CHOICES = ["igl", "duelist", "support", "jungler", "mid", "adc", "entry", "awper", "rifler"]
RANK_CHOICES = ["gold", "platinum", "diamond", "ascendant", "immortal", "master", "grandmaster", "semi-pro"]
FOCUS_CHOICES = ["tournament", "solo queue climb", "scrim prep", "playoff week"]


def _escape(value: Any) -> str:
    return html.escape(str(value or ""))


def _inline_markdown_to_html(text: str) -> str:
    escaped = html.escape(text)
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"`(.+?)`", r"<code>\1</code>", escaped)
    return escaped


def _markdownish_to_html(text: Any) -> str:
    lines = str(text or "").splitlines()
    chunks: List[str] = []
    list_buffer: List[str] = []

    def flush_list() -> None:
        nonlocal list_buffer
        if list_buffer:
            chunks.append("<ul>" + "".join(list_buffer) + "</ul>")
            list_buffer = []

    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            flush_list()
            continue
        if line.startswith("#### "):
            flush_list()
            chunks.append(f"<h4>{_inline_markdown_to_html(line[5:])}</h4>")
            continue
        if line.startswith("### "):
            flush_list()
            chunks.append(f"<h3>{_inline_markdown_to_html(line[4:])}</h3>")
            continue
        if line.startswith("## "):
            flush_list()
            chunks.append(f"<h2>{_inline_markdown_to_html(line[3:])}</h2>")
            continue
        if line.startswith("# "):
            flush_list()
            chunks.append(f"<h1>{_inline_markdown_to_html(line[2:])}</h1>")
            continue
        if line.startswith(("- ", "* ")):
            list_buffer.append(f"<li>{_inline_markdown_to_html(line[2:])}</li>")
            continue
        flush_list()
        chunks.append(f"<p>{_inline_markdown_to_html(line)}</p>")

    flush_list()
    return "".join(chunks) if chunks else "<div class='arena-empty'>No replay items yet.</div>"


def _session_choices() -> List[str]:
    return [item["session_id"] for item in engine.list_sessions()]


def _normalize_dropdown_value(value: Any, valid_choices: List[str], default: str) -> str:
    text = str(value or "").strip().lower()
    return text if text in valid_choices else default


def _log_to_messages(state: Dict[str, Any]) -> List[Dict[str, str]]:
    messages: List[Dict[str, str]] = []
    for entry in state.get("coach_log", []):
        role = "assistant" if entry.get("actor") == "Arena Host" else "user"
        messages.append({"role": role, "content": entry.get("content", "")})
    return messages


def _render_banner(state: Dict[str, Any]) -> str:
    if not state:
        return "<div class='arena-panel arena-hero'><div class='arena-empty'>Start an arena session to load the match prep room.</div></div>"
    plan = state.get("latest_plan", {})
    confidence = int(max(0, min(float(plan.get("confidence", 0.0)) * 100, 100)))
    return f"""
    <div class="arena-panel arena-hero arena-shell">
      <div class="arena-split">
        <div>
          <div class="arena-kicker">Coach Arena</div>
          <div class="arena-title">{_escape(state.get("team_name"))} vs {_escape(state.get("opponent_name"))}</div>
          <div class="arena-subtitle">Live prep room for {_escape(state.get("title_label"))}. The staff is aligned around one clear win condition.</div>
          <div class="arena-chip-row">
            <div class="arena-chip">Player: {_escape(state.get("player_handle"))}</div>
            <div class="arena-chip">Role: {_escape(state.get("role"))}</div>
            <div class="arena-chip">Rank: {_escape(state.get("rank_tier"))}</div>
            <div class="arena-chip">Focus: {_escape(state.get("focus_mode"))}</div>
            <div class="arena-chip">Patch: {_escape(state.get("current_patch"))}</div>
          </div>
        </div>
        <div class="arena-scoreboard">
          <div class="arena-kicker">Series Signal</div>
          <div class="arena-score-big">{confidence}%</div>
          <div class="arena-score-meta">Current staff confidence in the match plan and prep direction.</div>
          <div class="arena-meter">
            <div class="arena-meter-track"><div class="arena-meter-fill" style="width:{confidence}%;"></div></div>
          </div>
          <div class="arena-subtitle" style="margin-bottom:0;">Series Type: {_escape(state.get("series_type"))}</div>
        </div>
      </div>
    </div>
    """


def _render_pressure_board(state: Dict[str, Any]) -> str:
    meter = state.get("latest_reports", {}).get("meta", {}).get("pressure_meter", {})
    if not meter:
        return "<div class='arena-panel'><div class='arena-kicker'>Pressure Pulse</div><div class='arena-empty'>Generate a plan to light up the series pressure board.</div></div>"
    labels = [("Early", meter.get("early", 0)), ("Mid", meter.get("mid", 0)), ("Clutch", meter.get("clutch", 0))]
    cols = []
    for label, value in labels:
        height = max(12, min(int(value), 100))
        cols.append(
            "<div class='arena-pressure-col'>"
            f"<div class='arena-pressure-bar'><div class='arena-pressure-fill' style='height:{height}%;'></div></div>"
            f"<div class='arena-pressure-value'>{int(value)}</div>"
            f"<div class='arena-pressure-label'>{_escape(label)}</div>"
            "</div>"
        )
    return f"<div class='arena-panel'><div class='arena-kicker'>Pressure Pulse</div><div class='arena-pressure-grid'>{''.join(cols)}</div></div>"


def _render_battlefield(state: Dict[str, Any]) -> str:
    zones = state.get("map_pool", [])[:3]
    scout = state.get("latest_reports", {}).get("scout", {})
    if not zones:
        return "<div class='arena-panel'><div class='arena-kicker'>Battlefield</div><div class='arena-empty'>No map or lane intelligence loaded yet.</div></div>"
    cards = []
    for zone in zones:
        tags = []
        if zone.get("name") == scout.get("best_target_map"):
            tags.append("Attack Window")
        if zone.get("name") == scout.get("danger_map"):
            tags.append("Danger Zone")
        if not tags:
            tags.append("Prep Board")
        cards.append(
            "<div class='arena-zone'>"
            f"<div class='arena-zone-name'>{_escape(zone.get('name'))}</div>"
            f"<div class='arena-zone-tag'>{_escape(tags[0])}</div>"
            f"<div class='arena-zone-note'><strong>Comfort:</strong> {_escape(zone.get('comfort'))} | <strong>Threat:</strong> {_escape(zone.get('enemy_threat'))}</div>"
            f"<div class='arena-zone-note' style='margin-top:10px;'>{_escape(zone.get('plan'))}</div>"
            "</div>"
        )
    return f"""
    <div class="arena-panel">
      <div class="arena-kicker">Battlefield</div>
      <div class="arena-battlefield">
        <div class="arena-battlefield-grid">{''.join(cards)}</div>
      </div>
    </div>
    """


def _render_draft_stage(state: Dict[str, Any]) -> str:
    draft = state.get("latest_reports", {}).get("draft", {})
    if not draft:
        return "<div class='arena-panel'><div class='arena-kicker'>Draft Chamber</div><div class='arena-empty'>No draft or veto call has been locked yet.</div></div>"
    bans = "".join(f"<div class='arena-pill'>{_escape(item)}</div>" for item in draft.get("ban_priority", []))
    locks = "".join(f"<div class='arena-pill'>{_escape(item)}</div>" for item in draft.get("lock_priority", []))
    return f"""
    <div class="arena-panel">
      <div class="arena-kicker">Draft Chamber</div>
      <div class="arena-stage">
        <div>
          <div class="arena-column-title">Remove</div>
          <div class="arena-pill-stack">{bans}</div>
        </div>
        <div class="arena-stage-core">
          <div>
            <div class="arena-core-kicker">Core Call</div>
            <div class="arena-core-title">{_escape(draft.get("key_map"))}</div>
            <div class="arena-core-meta">{_escape(draft.get("signature_pick"))}</div>
          </div>
        </div>
        <div>
          <div class="arena-column-title">Lean On</div>
          <div class="arena-pill-stack">{locks}</div>
        </div>
      </div>
      <div class="arena-subtitle" style="margin-top:14px; margin-bottom:0;">{_escape(draft.get('pivot_call'))}</div>
    </div>
    """


def _render_training_circuit(state: Dict[str, Any]) -> str:
    training = state.get("latest_reports", {}).get("training", {})
    lanes = training.get("focus_lanes", [])
    if not lanes:
        return "<div class='arena-panel'><div class='arena-kicker'>Practice Circuit</div><div class='arena-empty'>No practice circuit prepared yet.</div></div>"
    items = []
    for lane in lanes:
        items.append(
            "<div class='arena-lane'>"
            f"<div class='arena-lane-clock'>{_escape(lane.get('duration'))}</div>"
            "<div class='arena-lane-card'>"
            f"<div class='arena-lane-title'>{_escape(lane.get('name'))}</div>"
            f"<div>{_escape(lane.get('goal'))}</div>"
            "</div>"
            "</div>"
        )
    return f"""
    <div class="arena-panel">
      <div class="arena-kicker">Practice Circuit</div>
      <div class="arena-lanes">{''.join(items)}</div>
      <div class="arena-subtitle" style="margin-top:14px; margin-bottom:0;">Warmup call: {_escape(training.get('warmup_call'))}</div>
    </div>
    """


def _render_comms_booth(state: Dict[str, Any]) -> str:
    mindset = state.get("latest_reports", {}).get("mindset", {})
    if not mindset:
        return "<div class='arena-panel'><div class='arena-kicker'>Comms Booth</div><div class='arena-empty'>No reset protocol prepared yet.</div></div>"
    return f"""
    <div class="arena-panel">
      <div class="arena-kicker">Comms Booth</div>
      <div class="arena-comms">
        <div class="arena-comms-bubble">
          <div class="arena-comms-label">Opening</div>
          <div>{_escape(mindset.get("opening_comms"))}</div>
        </div>
        <div class="arena-comms-bubble">
          <div class="arena-comms-label">Reset</div>
          <div>{_escape(mindset.get("between_round_reset"))}</div>
        </div>
        <div class="arena-comms-bubble">
          <div class="arena-comms-label">Clutch Cue</div>
          <div>{_escape(mindset.get("clutch_cue"))}</div>
        </div>
      </div>
    </div>
    """


def _render_plan_podium(state: Dict[str, Any]) -> str:
    plan = state.get("latest_plan", {})
    if not plan:
        return "<div class='arena-panel'><div class='arena-kicker'>Head Coach Podium</div><div class='arena-empty'>Generate a match plan to fill the podium.</div></div>"
    return f"""
    <div class="arena-panel">
      <div class="arena-kicker">Head Coach Podium</div>
      <div class="arena-plan">
        <div class="arena-plan-hero">
          <div class="arena-plan-headline">{_escape(plan.get("headline"))}</div>
          <div>{_escape(plan.get("win_condition"))}</div>
        </div>
        <div class="arena-plan-grid">
          <div class="arena-plan-card">
            <div class="arena-plan-label">Danger Zone</div>
            <div>{_escape(plan.get("danger_zone"))}</div>
          </div>
          <div class="arena-plan-card">
            <div class="arena-plan-label">Tempo Call</div>
            <div>{_escape(plan.get("tempo_call"))}</div>
          </div>
          <div class="arena-plan-card">
            <div class="arena-plan-label">Key Zone</div>
            <div>{_escape(plan.get("key_map"))}</div>
          </div>
          <div class="arena-plan-card">
            <div class="arena-plan-label">Signature Lean</div>
            <div>{_escape(plan.get("signature_pick"))}</div>
          </div>
        </div>
        <div class="arena-plan-card">
          <div class="arena-plan-label">Fallback Switch</div>
          <div>{_escape(plan.get("bench_note"))}</div>
        </div>
      </div>
    </div>
    """


def _render_timeline(state: Dict[str, Any]) -> str:
    entries = state.get("coach_log", [])[-6:]
    if not entries:
        return "<div class='arena-panel'><div class='arena-kicker'>Replay Feed</div><div class='arena-empty'>Session calls will appear here after the first plan.</div></div>"
    items = []
    for entry in reversed(entries):
        items.append(
            "<div class='arena-timeline-item'>"
            f"<div class='arena-timeline-actor'>{_escape(entry.get('actor'))}</div>"
            f"<div class='arena-timeline-card'>{_markdownish_to_html(entry.get('content'))}</div>"
            "</div>"
        )
    return f"<div class='arena-panel'><div class='arena-kicker'>Replay Feed</div><div class='arena-timeline'>{''.join(items)}</div></div>"


def _dashboard_outputs(state: Dict[str, Any]) -> Tuple[str, str, str, str, str, str, str]:
    return (
        _render_banner(state),
        _render_pressure_board(state),
        _render_battlefield(state),
        _render_draft_stage(state),
        _render_training_circuit(state),
        _render_comms_booth(state),
        _render_plan_podium(state),
    )


def start_session(player_handle: str, team_name: str, title: str, role: str, rank_tier: str, focus_mode: str):
    result = engine.run_turn(
        "",
        player_handle=player_handle,
        team_name=team_name,
        title=title,
        role=role,
        rank_tier=rank_tier,
        focus_mode=focus_mode,
        session_id=None,
    )
    state = result["arena_state"]
    sessions = result["sessions"]
    panels = _dashboard_outputs(state)
    return (
        [{"role": "assistant", "content": result["response"]}],
        "",
        result["response"],
        *panels,
        _render_timeline(state),
        json.dumps(state, indent=2),
        result["session_id"],
        sessions,
        gr.update(choices=[item["session_id"] for item in sessions], value=result["session_id"]),
    )


def ask_coach(
    request: str,
    chat_history: Optional[List[Dict[str, str]]],
    session_id: str,
    player_handle: str,
    team_name: str,
    title: str,
    role: str,
    rank_tier: str,
    focus_mode: str,
):
    if not session_id:
        raise gr.Error("Start an arena session first.")
    if not request.strip():
        raise gr.Error("Enter a match-prep request for the coaching staff.")
    result = engine.run_turn(
        request,
        player_handle=player_handle,
        team_name=team_name,
        title=title,
        role=role,
        rank_tier=rank_tier,
        focus_mode=focus_mode,
        session_id=session_id,
    )
    state = result["arena_state"]
    history = list(chat_history or [])
    history.append({"role": "user", "content": request})
    history.append({"role": "assistant", "content": result["response"]})
    sessions = result["sessions"]
    panels = _dashboard_outputs(state)
    return (
        history,
        "",
        result["response"],
        *panels,
        _render_timeline(state),
        json.dumps(state, indent=2),
        session_id,
        sessions,
        gr.update(choices=[item["session_id"] for item in sessions], value=session_id),
    )


def load_session(session_id: str):
    if not session_id:
        raise gr.Error("Select a saved arena session.")
    state = engine.load_arena_state(session_id)
    sessions = engine.list_sessions()
    panels = _dashboard_outputs(state)
    return (
        _log_to_messages(state),
        "",
        state.get("coach_log", [{}])[-1].get("content", ""),
        *panels,
        _render_timeline(state),
        json.dumps(state, indent=2),
        state.get("session_id", session_id),
        sessions,
        gr.update(choices=[item["session_id"] for item in sessions], value=session_id),
        state.get("player_handle", "Player One"),
        state.get("team_name", "Arena Squad"),
        _normalize_dropdown_value(state.get("title"), TITLE_CHOICES, "valorant"),
        _normalize_dropdown_value(state.get("role"), ROLE_CHOICES, "igl"),
        _normalize_dropdown_value(state.get("rank_tier"), RANK_CHOICES, "ascendant"),
        _normalize_dropdown_value(state.get("focus_mode"), FOCUS_CHOICES, "tournament"),
    )


with gr.Blocks(theme=gr.themes.Base(), css=APP_CSS, title="Esports Coach Arena Agent") as demo:
    gr.Markdown(
        """
        # Esports Coach Arena Agent
        A multi-agent esports prep room where a head coach orchestrates specialist staff across meta, scouting, draft, practice, and mindset.
        """
    )

    session_id_state = gr.State("")

    with gr.Tab("Arena Floor"):
        with gr.Row(equal_height=False):
            with gr.Column(scale=4):
                arena_banner = gr.HTML(_render_banner({}))
            with gr.Column(scale=2):
                with gr.Group():
                    player_handle = gr.Textbox(label="Player Handle", value="Hisham")
                    team_name = gr.Textbox(label="Team Name", value="Neon Rift")
                    title = gr.Dropdown(label="Title", choices=TITLE_CHOICES, value="valorant")
                    role = gr.Dropdown(label="Role", choices=ROLE_CHOICES, value="igl")
                    rank_tier = gr.Dropdown(label="Rank Tier", choices=RANK_CHOICES, value="ascendant")
                    focus_mode = gr.Dropdown(label="Focus Mode", choices=FOCUS_CHOICES, value="tournament")
                    start_button = gr.Button("Open Arena Session", variant="primary")

        with gr.Row():
            coach_chat = gr.Chatbot(label="Analyst Desk", type="messages", height=360)
            latest_brief = gr.Markdown()

        with gr.Row():
            request_box = gr.Textbox(
                label="Ask The Staff",
                placeholder="Example: We are facing a fast-tempo opponent on a must-win Valorant match. Give me a safer opener and a reset protocol.",
                lines=3,
            )

        gr.Examples(
            examples=[
                "We are entering a playoff series and I need a full match plan.",
                "The opponent plays fast and snowballs early. Give me a safer draft and comms reset.",
                "I want a high-pressure prep plan built around our best comfort look.",
            ],
            inputs=request_box,
            label="Quick Calls",
        )

        run_button = gr.Button("Generate Match Plan", variant="primary")

        with gr.Row():
            pressure_board = gr.HTML(_render_pressure_board({}))
            battlefield = gr.HTML(_render_battlefield({}))

        with gr.Row():
            draft_stage = gr.HTML(_render_draft_stage({}))
            training_circuit = gr.HTML(_render_training_circuit({}))

        with gr.Row():
            comms_booth = gr.HTML(_render_comms_booth({}))
            plan_podium = gr.HTML(_render_plan_podium({}))

        replay_feed = gr.HTML(_render_timeline({}))

    with gr.Tab("Session Vault"):
        session_picker = gr.Dropdown(label="Load Saved Session", choices=_session_choices())
        load_button = gr.Button("Load Session")
        sessions_json = gr.JSON(label="Session Index", value=engine.list_sessions())

    with gr.Tab("Debug"):
        debug_state = gr.Code(label="Arena State JSON", language="json", value="{}")

    start_button.click(
        start_session,
        inputs=[player_handle, team_name, title, role, rank_tier, focus_mode],
        outputs=[
            coach_chat,
            request_box,
            latest_brief,
            arena_banner,
            pressure_board,
            battlefield,
            draft_stage,
            training_circuit,
            comms_booth,
            plan_podium,
            replay_feed,
            debug_state,
            session_id_state,
            sessions_json,
            session_picker,
        ],
    )

    run_button.click(
        ask_coach,
        inputs=[
            request_box,
            coach_chat,
            session_id_state,
            player_handle,
            team_name,
            title,
            role,
            rank_tier,
            focus_mode,
        ],
        outputs=[
            coach_chat,
            request_box,
            latest_brief,
            arena_banner,
            pressure_board,
            battlefield,
            draft_stage,
            training_circuit,
            comms_booth,
            plan_podium,
            replay_feed,
            debug_state,
            session_id_state,
            sessions_json,
            session_picker,
        ],
    )

    load_button.click(
        load_session,
        inputs=[session_picker],
        outputs=[
            coach_chat,
            request_box,
            latest_brief,
            arena_banner,
            pressure_board,
            battlefield,
            draft_stage,
            training_circuit,
            comms_booth,
            plan_podium,
            replay_feed,
            debug_state,
            session_id_state,
            sessions_json,
            session_picker,
            player_handle,
            team_name,
            title,
            role,
            rank_tier,
            focus_mode,
        ],
    )


if __name__ == "__main__":
    demo.launch()
