from typing import Any, Dict, List, Tuple

from launchpad_strategist.ui.views.mission_panels import (
    render_audience_panel,
    render_channel_mix,
    render_message_lab,
    render_operator_board,
    render_proof_stack,
    render_signal_strip,
    render_strategy_board,
    render_timeline_panel,
)
from launchpad_strategist.ui.views.common import escape_html as _escape
from launchpad_strategist.ui.views.common import parse_state_payload as _parse_state


def render_banner(state: Dict[str, Any]) -> str:
    if not state:
        return "<div class='launch-panel launch-hero launch-shell'><div class='launch-empty'>Open a launch session to activate mission control.</div></div>"
    plan = state.get("latest_plan", {})
    signals = plan.get("signal_scores", {})
    confidence = int(plan.get("confidence", 0.0) * 100) if plan else 0
    mode = plan.get("execution_mode", state.get("launch_motion", "launch plan"))
    return f"""
    <div class="launch-panel launch-hero launch-shell">
      <div class="launch-grid-2">
        <div>
          <div class="launch-kicker">Launch Mission Control</div>
          <div class="launch-title">{_escape(state.get('startup_name'))} / {_escape(state.get('product_name'))}</div>
          <div class="launch-subtitle">A mission-control room for sharper positioning, clearer proof, and a launch runway that matches the product stage.</div>
          <div class="launch-chip-row">
            <div class="launch-chip">Type: {_escape(state.get('product_type'))}</div>
            <div class="launch-chip">Stage: {_escape(state.get('stage'))}</div>
            <div class="launch-chip">Budget: {_escape(state.get('budget_band'))}</div>
            <div class="launch-chip">Goal: {_escape(state.get('launch_goal'))}</div>
            <div class="launch-chip">Mode: {_escape(mode)}</div>
          </div>
        </div>
        <div class="launch-metric">
          <div class="launch-kicker">Launch Readiness</div>
          <div class="launch-metric-big">{confidence}%</div>
          <div class="launch-subtitle">Current planner confidence in the locked launch direction.</div>
          <div class="launch-mini-grid">
            <div class="launch-mini-metric"><span>Clarity</span><strong>{_escape(signals.get('clarity', '--'))}</strong></div>
            <div class="launch-mini-metric"><span>Proof</span><strong>{_escape(signals.get('proof', '--'))}</strong></div>
            <div class="launch-mini-metric"><span>Distribution</span><strong>{_escape(signals.get('distribution', '--'))}</strong></div>
            <div class="launch-mini-metric"><span>Urgency</span><strong>{_escape(signals.get('urgency', '--'))}</strong></div>
          </div>
        </div>
      </div>
    </div>
    """


def render_log(state: Dict[str, Any]) -> str:
    entries = state.get("launch_log", [])[-6:]
    if not entries:
        return "<div class='launch-panel'><div class='launch-kicker'>Command Feed</div><div class='launch-empty'>Session actions will appear here after the first launch brief.</div></div>"
    rows = []
    for entry in reversed(entries):
        rows.append(
            "<div class='launch-log-item'>"
            f"<div class='launch-log-actor'>{_escape(entry.get('actor'))}</div>"
            f"<div class='launch-log-body'>{_escape(entry.get('content'))}</div>"
            "</div>"
        )
    return f"<div class='launch-panel'><div class='launch-kicker'>Command Feed</div><div class='launch-log'>{''.join(rows)}</div></div>"


def dashboard_outputs(state_payload: Any) -> Tuple[str, str, str, str, str, str, str, str, str]:
    state = _parse_state(state_payload)
    return (
        render_banner(state),
        render_strategy_board(state),
        render_signal_strip(state),
        render_audience_panel(state),
        render_channel_mix(state),
        render_message_lab(state),
        render_proof_stack(state),
        render_timeline_panel(state),
        render_operator_board(state),
    )
