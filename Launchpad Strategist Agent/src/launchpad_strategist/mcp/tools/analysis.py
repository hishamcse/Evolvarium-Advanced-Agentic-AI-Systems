import json

from launchpad_strategist.mcp.server_app import mcp
from launchpad_strategist.persistence.store import load_launch_state, save_launch_state
from launchpad_strategist.mcp.tools.context_helpers import context_for, request_signals, step_order_for


@mcp.tool()
def plan_launch(session_id: str, objective: str = "balanced", request: str = "") -> str:
    """Create the top-level launch execution plan."""

    state, profile = context_for(session_id)
    signals = request_signals(request)
    step_order = step_order_for(state, signals)
    launch_angle = (
        "Lead with a narrow outcome, visible proof, and a clear reason to trust this now."
        if objective == "proof" or signals["proof"]
        else f"Lead with {profile['product']['promise_shape']} for {profile['goal']['north_star']}."
    )
    payload = {
        "objective": state["launch_goal"],
        "launch_angle": launch_angle,
        "rationale": (
            f"Start with {step_order[0]} because the current stage needs {profile['stage']['readiness_focus']}. "
            f"Budget posture favors {profile['budget']['channel_bias']}, while the launch goal optimizes for {profile['goal']['north_star']}."
        ),
        "step_order": step_order,
        "confidence": 0.84 if state["stage"] in {"beta", "live"} else 0.76,
        "execution_mode": profile["product"]["launch_motion"],
        "signal_scores": {
            "clarity": 86 if objective == "proof" or signals["proof"] else 78,
            "proof": 82 if signals["proof"] else 70,
            "distribution": 74 if state["budget_band"] == "lean" else 83,
            "urgency": 81 if signals["fast"] else 68,
        },
        "channel_bias": profile["goal"]["preferred_channels"],
    }
    state["latest_plan"] = payload
    state["latest_reports"]["planner"] = payload
    save_launch_state(state)
    return json.dumps(payload, indent=2)


@mcp.tool()
def map_market(session_id: str, focus: str = "balanced", request: str = "") -> str:
    """Map the market window and pressure points."""

    state, profile = context_for(session_id)
    signals = request_signals(request)
    urgency_hook = profile["product"]["urgency_hooks"][1 if signals["proof"] else 0]
    payload = {
        "market_window": profile["product"]["market_signal"],
        "competitive_pressure": profile["product"]["competitor_pressure"],
        "whitespace": (
            "Own a narrower promise than bigger rivals and show the first win faster."
            if focus == "focused"
            else f"Position around {profile['product']['promise_shape']} instead of broad category language."
        ),
        "positioning_wedge": f"{state['product_name']} should feel more concrete, faster to understand, and easier to trust than the usual alternatives.",
        "urgency_hook": urgency_hook,
        "best_channels": profile["goal"]["preferred_channels"],
        "signal_lights": {"market_heat": 82, "timing": 76 if state["stage"] == "idea" else 88, "proof_gap": 72 if signals["proof"] else 61},
    }
    state["latest_reports"]["market"] = payload
    save_launch_state(state)
    return json.dumps(payload, indent=2)


@mcp.tool()
def build_icp(session_id: str, segment: str = "default", request: str = "") -> str:
    """Build the most promising early audience profile."""

    state, profile = context_for(session_id)
    signals = request_signals(request)
    primary = profile["product"]["primary_segments"][0]
    if signals["technical"] and len(profile["product"]["primary_segments"]) > 1:
        primary = profile["product"]["primary_segments"][0]
    secondary = profile["product"]["primary_segments"][1]
    payload = {
        "primary_audience": primary,
        "secondary_audience": secondary,
        "jobs_to_be_done": [
            "understand the promise in seconds",
            "see a believable first payoff",
            "feel low adoption friction",
        ],
        "buying_triggers": [
            profile["product"]["buyer_mindset"],
            "evidence that the product is simpler than the alternatives",
            f"a path to {profile['goal']['north_star']}",
        ],
        "persona_traits": ["high-context", "impatient with fluff", "responds to strong proof"],
        "resistance_points": ["switching cost fear", "skepticism of broad claims", "unclear implementation path"],
        "segment_note": (
            "Start narrower than feels comfortable, then expand after the first traction signal."
            if segment == "default"
            else "Bias toward the most impatient and highest-context users first."
        ),
    }
    state["latest_reports"]["icp"] = payload
    save_launch_state(state)
    return json.dumps(payload, indent=2)


@mcp.tool()
def craft_message_stack(session_id: str, tone: str = "bold", request: str = "") -> str:
    """Craft the messaging stack for the launch."""

    state, profile = context_for(session_id)
    product = state["product_name"]
    hero_message = (
        f"{product} turns {profile['product']['promise_shape']} into a faster, more believable first result."
        if tone == "bold"
        else f"{product} gives teams a simpler path to a real early result."
    )
    payload = {
        "hero_message": hero_message,
        "supporting_messages": [
            f"Built for {profile['product']['primary_segments'][0]} who care about speed and clarity.",
            f"Lead with {profile['goal']['proof_bias']}.",
            f"Match the launch tone to {', '.join(profile['product']['message_tone'])}.",
        ],
        "proof_points": profile["product"]["proof_assets"] + profile["stage"]["asset_priority"][:1],
        "objection_handle": "Show the first win, lower perceived switching cost, and let proof do the heavy lifting.",
        "cta": profile["goal"]["primary_cta"].capitalize(),
        "tone_words": profile["product"]["message_tone"],
    }
    state["latest_reports"]["messaging"] = payload
    save_launch_state(state)
    return json.dumps(payload, indent=2)


@mcp.tool()
def build_launch_timeline(session_id: str, pace: str = "steady", request: str = "") -> str:
    """Build the launch runway timeline."""

    state, profile = context_for(session_id)
    base_days = profile["stage"]["runway_days"]
    prelaunch = f"T-{max(3, base_days // 2)}"
    launch_minus = "T-2" if pace == "fast" else "T-4"
    sequence: list[dict] = [
        {"phase": prelaunch, "move": "Publish teaser with one clear promise and proof seed", "channel": profile["goal"]["preferred_channels"][0]},
        {"phase": launch_minus, "move": "Drop audience-specific message and strongest proof asset", "channel": profile["goal"]["preferred_channels"][1]},
        {"phase": "Launch Day", "move": f"Ship core announcement with CTA to {profile['goal']['primary_cta']}", "channel": profile["goal"]["preferred_channels"][0]},
        {"phase": "T+3", "move": "Follow up with customer proof, objections, and next-action prompt", "channel": profile["goal"]["preferred_channels"][2]},
    ]
    if pace == "fast":
        sequence[0]["move"] = "Compress teaser and proof into one sharper prelaunch reveal"
    payload = {
        "runway": sequence,
        "launch_mode": profile["product"]["launch_motion"],
        "cadence_note": f"Keep the story consistent across every touchpoint and stay {profile['stage']['tempo']}.",
        "asset_checklist": profile["stage"]["asset_priority"],
        "channel_stack": profile["goal"]["preferred_channels"],
        "measurement_focus": profile["goal"]["north_star"],
    }
    state["latest_reports"]["timeline"] = payload
    save_launch_state(state)
    return json.dumps(payload, indent=2)


@mcp.tool()
def lock_launch_board(
    session_id: str,
    headline: str,
    launch_angle: str,
    primary_audience: str,
    hero_message: str,
    channel_focus: list[str],
    launch_sequence: list[str],
    proof_stack: list[str],
    risk_watch: str,
    next_best_action: str,
) -> str:
    """Persist the final launch board."""

    state = load_launch_state(session_id)
    payload = {
        "headline": headline,
        "launch_angle": launch_angle,
        "primary_audience": primary_audience,
        "hero_message": hero_message,
        "channel_focus": channel_focus,
        "launch_sequence": launch_sequence,
        "proof_stack": proof_stack,
        "risk_watch": risk_watch,
        "next_best_action": next_best_action,
    }
    state["latest_board"] = payload
    save_launch_state(state)
    return json.dumps(payload, indent=2)
