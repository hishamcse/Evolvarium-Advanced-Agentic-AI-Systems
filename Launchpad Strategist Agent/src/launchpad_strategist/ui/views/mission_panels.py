from typing import Any, Dict

from launchpad_strategist.ui.views.common import escape_html as _escape


def render_strategy_board(state: Dict[str, Any]) -> str:
    if not state:
        return "<div class='launch-panel'><div class='launch-kicker'>Strategy Radar</div><div class='launch-empty'>The market and plan signals will appear here after the first run.</div></div>"
    plan = state.get("latest_plan", {})
    market = state.get("latest_reports", {}).get("market", {})
    cards = [
        ("Launch Angle", plan.get("launch_angle", "Waiting for planner lock.")),
        ("Positioning Wedge", market.get("positioning_wedge", state.get("promise_shape", ""))),
        ("Urgency Hook", market.get("urgency_hook", "")),
    ]
    body = "".join(
        f"<div class='launch-card'><div class='launch-card-title'>{_escape(title)}</div><div>{_escape(value)}</div></div>"
        for title, value in cards
    )
    return f"<div class='launch-panel'><div class='launch-kicker'>Strategy Radar</div><div class='launch-card-grid'>{body}</div></div>"


def render_signal_strip(state: Dict[str, Any]) -> str:
    planner = state.get("latest_plan", {})
    market = state.get("latest_reports", {}).get("market", {})
    scores = planner.get("signal_scores", {})
    market_lights = market.get("signal_lights", {})
    if not scores and not market_lights:
        return "<div class='launch-panel'><div class='launch-kicker'>Signal Strip</div><div class='launch-empty'>Planner signals will light up here after the first run.</div></div>"
    items = [
        ("Clarity", scores.get("clarity", 0)),
        ("Proof", scores.get("proof", 0)),
        ("Timing", market_lights.get("timing", 0)),
        ("Market Heat", market_lights.get("market_heat", 0)),
    ]
    cards = []
    for label, value in items:
        cards.append(
            "<div class='launch-signal-card'>"
            f"<div class='launch-card-title'>{_escape(label)}</div>"
            f"<div class='launch-signal-value'>{int(value)}</div>"
            "<div class='launch-signal-track'>"
            f"<div class='launch-signal-fill' style='width:{max(8, min(int(value), 100))}%;'></div>"
            "</div>"
            "</div>"
        )
    return f"<div class='launch-panel'><div class='launch-kicker'>Signal Strip</div><div class='launch-signal-grid'>{''.join(cards)}</div></div>"


def render_audience_panel(state: Dict[str, Any]) -> str:
    icp = state.get("latest_reports", {}).get("icp", {})
    if not icp:
        return "<div class='launch-panel'><div class='launch-kicker'>Audience Lock</div><div class='launch-empty'>No ICP lock yet.</div></div>"
    jobs = "".join(f"<div class='launch-list-item'>{_escape(job)}</div>" for job in icp.get("jobs_to_be_done", []))
    traits = "".join(f"<div class='launch-chip'>{_escape(item)}</div>" for item in icp.get("persona_traits", []))
    return f"""
    <div class="launch-panel">
      <div class="launch-kicker">Audience Lock</div>
      <div class="launch-subtitle"><strong>{_escape(icp.get('primary_audience'))}</strong></div>
      <div class="launch-secondary-line">Secondary edge: {_escape(icp.get('secondary_audience'))}</div>
      <div class="launch-list">{jobs}</div>
      <div class="launch-chip-row" style="margin-top:12px;">{traits}</div>
    </div>
    """


def render_channel_mix(state: Dict[str, Any]) -> str:
    board = state.get("latest_board", {})
    market = state.get("latest_reports", {}).get("market", {})
    timeline = state.get("latest_reports", {}).get("timeline", {})
    channels = board.get("channel_focus") or timeline.get("channel_stack") or market.get("best_channels", [])
    if not channels:
        return "<div class='launch-panel'><div class='launch-kicker'>Channel Mix</div><div class='launch-empty'>Channel priorities will appear here after the first run.</div></div>"
    pills = "".join(f"<div class='launch-channel-pill'>{_escape(channel)}</div>" for channel in channels)
    return f"""
    <div class="launch-panel">
      <div class="launch-kicker">Channel Mix</div>
      <div class="launch-channel-row">{pills}</div>
      <div class="launch-subtitle" style="margin-top:14px; margin-bottom:0;">Bias the early push toward the highest-context channels before broadening reach.</div>
    </div>
    """


def render_message_lab(state: Dict[str, Any]) -> str:
    messaging = state.get("latest_reports", {}).get("messaging", {})
    if not messaging:
        return "<div class='launch-panel'><div class='launch-kicker'>Message Lab</div><div class='launch-empty'>No message stack yet.</div></div>"
    support = "".join(f"<div class='launch-list-item'>{_escape(item)}</div>" for item in messaging.get("supporting_messages", []))
    tone = "".join(f"<div class='launch-chip'>{_escape(item)}</div>" for item in messaging.get("tone_words", []))
    return f"""
    <div class="launch-panel">
      <div class="launch-kicker">Message Lab</div>
      <div class="launch-subtitle">{_escape(messaging.get('hero_message'))}</div>
      <div class="launch-list">{support}</div>
      <div class="launch-chip-row" style="margin-top:12px;">{tone}</div>
    </div>
    """


def render_proof_stack(state: Dict[str, Any]) -> str:
    messaging = state.get("latest_reports", {}).get("messaging", {})
    timeline = state.get("latest_reports", {}).get("timeline", {})
    proof_items = messaging.get("proof_points", []) or state.get("proof_assets", [])
    asset_items = timeline.get("asset_checklist", [])
    items = proof_items[:3] + [item for item in asset_items if item not in proof_items][:2]
    if not items:
        return "<div class='launch-panel'><div class='launch-kicker'>Proof Stack</div><div class='launch-empty'>Proof assets will appear here after the first run.</div></div>"
    cards = "".join(f"<div class='launch-proof-item'>{_escape(item)}</div>" for item in items)
    return f"<div class='launch-panel'><div class='launch-kicker'>Proof Stack</div><div class='launch-proof-board'>{cards}</div></div>"


def render_timeline_panel(state: Dict[str, Any]) -> str:
    timeline = state.get("latest_reports", {}).get("timeline", {})
    runway = timeline.get("runway", [])
    if not runway:
        return "<div class='launch-panel'><div class='launch-kicker'>Launch Runway</div><div class='launch-empty'>No launch runway yet.</div></div>"
    cards = []
    for item in runway:
        cards.append(
            "<div class='launch-card'>"
            f"<div class='launch-card-title'>{_escape(item.get('phase'))}</div>"
            f"<div><strong>{_escape(item.get('move'))}</strong></div>"
            f"<div style='margin-top:8px'>{_escape(item.get('channel'))}</div>"
            "</div>"
        )
    return f"""
    <div class='launch-panel'>
      <div class='launch-kicker'>Launch Runway</div>
      <div class='launch-secondary-line'>Mode: {_escape(timeline.get('launch_mode'))} | Metric: {_escape(timeline.get('measurement_focus'))}</div>
      <div class='launch-card-grid'>{''.join(cards)}</div>
    </div>
    """


def render_operator_board(state: Dict[str, Any]) -> str:
    board = state.get("latest_board", {})
    if not board:
        return "<div class='launch-panel'><div class='launch-kicker'>Operator Call</div><div class='launch-empty'>No final launch board locked yet.</div></div>"
    sequence = "".join(f"<div class='launch-list-item'>{_escape(item)}</div>" for item in board.get("launch_sequence", []))
    proof = "".join(f"<div class='launch-chip'>{_escape(item)}</div>" for item in board.get("proof_stack", []))
    channels = "".join(f"<div class='launch-chip'>{_escape(item)}</div>" for item in board.get("channel_focus", []))
    return f"""
    <div class="launch-panel launch-operator-hero">
      <div class="launch-kicker">Operator Call</div>
      <div class="launch-operator-title">{_escape(board.get('headline'))}</div>
      <div class="launch-subtitle">{_escape(board.get('launch_angle'))}</div>
      <div class="launch-card-grid">
        <div class="launch-card"><div class="launch-card-title">Audience</div><div>{_escape(board.get('primary_audience'))}</div></div>
        <div class="launch-card"><div class="launch-card-title">Hero Message</div><div>{_escape(board.get('hero_message'))}</div></div>
        <div class="launch-card"><div class="launch-card-title">Risk Watch</div><div>{_escape(board.get('risk_watch'))}</div></div>
      </div>
      <div class="launch-kicker" style="margin-top:16px;">Channel Focus</div>
      <div class="launch-chip-row">{channels}</div>
      <div class="launch-kicker" style="margin-top:16px;">Proof Stack</div>
      <div class="launch-chip-row">{proof}</div>
      <div class="launch-kicker" style="margin-top:16px;">Sequence</div>
      <div class="launch-list">{sequence}</div>
      <div class="launch-next-action">Next Best Action: {_escape(board.get('next_best_action'))}</div>
    </div>
    """
