import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from mcp.server.fastmcp import FastMCP


BASE_DIR = Path(__file__).resolve().parent
ARENA_DIR = BASE_DIR / "memory" / "arenas"
ARENA_DIR.mkdir(parents=True, exist_ok=True)

mcp = FastMCP("esports_coach_arena_server")


TITLE_LABELS = {
    "valorant": "Valorant",
    "league": "League of Legends",
    "cs2": "Counter-Strike 2",
}


TITLE_TEMPLATES: Dict[str, Dict[str, Any]] = {
    "valorant": {
        "series_type": "Bo3",
        "opponent_name": "Nova Reclaim",
        "current_patch": "Patch 11.03",
        "meta_snapshot": [
            {"name": "Double-initiate pressure", "weight": 93, "reason": "Early info tools are winning map control fights."},
            {"name": "Fast B contact", "weight": 88, "reason": "Teams are collapsing sites before second-rotator timing."},
            {"name": "Late lurk punish", "weight": 82, "reason": "Aggressive anchors are overextending for info."},
        ],
        "map_pool": [
            {"name": "Ascent", "comfort": 92, "enemy_threat": 76, "plan": "Punish mid contest with layered utility."},
            {"name": "Lotus", "comfort": 84, "enemy_threat": 83, "plan": "Attack rotating sites with late fake pressure."},
            {"name": "Sunset", "comfort": 74, "enemy_threat": 89, "plan": "Avoid dry mid pivots against operator setups."},
        ],
        "signature_pool": [
            {"name": "Sova", "fit": "Best for info-led pace changes."},
            {"name": "Omen", "fit": "Lets the IGL hide timing shifts."},
            {"name": "Raze", "fit": "Converts early space into explosive site hits."},
        ],
        "opponent_profile": {
            "tempo": "fast-openings, slow-closes",
            "style": "They love forcing defenders to burn utility early, then pivoting late.",
            "tendencies": [
                "Hit B quickly after a timeout to reset momentum.",
                "Over-fight for orb control when their entry has confidence.",
                "Save weak-buy rounds if the opener fails."
            ],
        },
        "practice_modules": [
            {"name": "Exec layering", "duration": "18 min", "goal": "Stack drone, smoke, and satchel timing cleanly."},
            {"name": "Retake chain", "duration": "14 min", "goal": "Tighten second-wave utility after first contact."},
            {"name": "Clutch reset", "duration": "12 min", "goal": "Rebuild comm clarity after lost anti-ecos."},
        ],
        "pressure_profile": {"early": 86, "mid": 73, "clutch": 79},
    },
    "league": {
        "series_type": "Bo3",
        "opponent_name": "Iron Rift",
        "current_patch": "Patch 26.7",
        "meta_snapshot": [
            {"name": "Skirmish junglers", "weight": 91, "reason": "Fast tempo jungle paths are snowballing first objectives."},
            {"name": "Mid priority wave-lock", "weight": 87, "reason": "Roam windows are controlled by early push mid lanes."},
            {"name": "Double-frontline teamfights", "weight": 80, "reason": "Reliable engage is outlasting poke comps."},
        ],
        "map_pool": [
            {"name": "Top-River", "comfort": 79, "enemy_threat": 70, "plan": "Play for first herald timing and top-side vision."},
            {"name": "Mid-Priority", "comfort": 88, "enemy_threat": 84, "plan": "Lock mid wave to open support roams."},
            {"name": "Dragon Setups", "comfort": 76, "enemy_threat": 90, "plan": "Avoid blind face-checks into layered engage."},
        ],
        "signature_pool": [
            {"name": "Orianna", "fit": "Stable mid priority with strong teamfight scaling."},
            {"name": "Sejuani", "fit": "Reliable front line and easy engage timing."},
            {"name": "Kai'Sa", "fit": "Lets the team convert dive windows into kills."},
        ],
        "opponent_profile": {
            "tempo": "slow-lanes, explosive-objectives",
            "style": "They absorb lane pressure and then collapse hard around dragon timers.",
            "tendencies": [
                "Support roams first after mid gets push.",
                "They draft one comfort blind pick early every series.",
                "Their top laner burns teleport aggressively for second fight tempo."
            ],
        },
        "practice_modules": [
            {"name": "First-objective setup", "duration": "20 min", "goal": "Vision line and engage path for early dragon."},
            {"name": "Side-wave discipline", "duration": "15 min", "goal": "Stop giving free picks before Baron windows."},
            {"name": "Front-to-back teamfight", "duration": "16 min", "goal": "Protect carries while maintaining engage threat."},
        ],
        "pressure_profile": {"early": 74, "mid": 88, "clutch": 68},
    },
    "cs2": {
        "series_type": "Bo3",
        "opponent_name": "Hex Protocol",
        "current_patch": "Spring Meta 2026",
        "meta_snapshot": [
            {"name": "Mid-round re-clears", "weight": 89, "reason": "Teams are winning off information resets after default."},
            {"name": "Utility-starved late executes", "weight": 84, "reason": "Economy pressure is making late hits fragile."},
            {"name": "Fast-contact anti-eco", "weight": 81, "reason": "Clean spacing is crushing force-buy gambles."},
        ],
        "map_pool": [
            {"name": "Mirage", "comfort": 90, "enemy_threat": 78, "plan": "Own mid timings and deny connector lurks."},
            {"name": "Ancient", "comfort": 82, "enemy_threat": 86, "plan": "Respect cave pressure and late donut pivots."},
            {"name": "Nuke", "comfort": 70, "enemy_threat": 91, "plan": "Avoid it unless veto order breaks perfectly."},
        ],
        "signature_pool": [
            {"name": "Mirage default", "fit": "Best map for spacing into mid-round calls."},
            {"name": "Late A split", "fit": "Punishes stacked anchors after quiet defaults."},
            {"name": "Aggressive CT re-clear", "fit": "Matches a confident rifler's timing."},
        ],
        "opponent_profile": {
            "tempo": "measured-defaults, explosive-finishes",
            "style": "They gather info patiently, then burst with layered flashes once a weakness appears.",
            "tendencies": [
                "Their AWPer re-peeks after first utility contact.",
                "They lean heavily on late lurks on gun rounds.",
                "On low economy they often double-stack the weaker site."
            ],
        },
        "practice_modules": [
            {"name": "Default spacing", "duration": "18 min", "goal": "Stop over-swinging after first mid info."},
            {"name": "Execute freeze review", "duration": "12 min", "goal": "Clean the flash-smoke-entry timing."},
            {"name": "Timeout conversion", "duration": "10 min", "goal": "Turn tactical pauses into one decisive mid-round plan."},
        ],
        "pressure_profile": {"early": 77, "mid": 86, "clutch": 83},
    },
}


def _now() -> str:
    return datetime.utcnow().isoformat(timespec="seconds") + "Z"


def _normalize_title(title: str) -> str:
    value = (title or "valorant").strip().lower()
    return value if value in TITLE_TEMPLATES else "valorant"


def _arena_path(session_id: str) -> Path:
    return ARENA_DIR / f"{session_id}.json"


def _load_state(session_id: str) -> Dict[str, Any]:
    path = _arena_path(session_id)
    if not path.exists():
        raise FileNotFoundError(f"Unknown session_id: {session_id}")
    return json.loads(path.read_text())


def _save_state(state: Dict[str, Any]) -> None:
    state["updated_at"] = _now()
    _arena_path(state["session_id"]).write_text(json.dumps(state, indent=2))


def _top_signal_sign(summary: Dict[str, Any]) -> str:
    signals = summary.get("top_signals", [])
    if not signals:
        return ""
    return signals[0].get("name", "")


@mcp.tool()
def create_arena_session(
    player_handle: str,
    team_name: str,
    title: str = "valorant",
    role: str = "igl",
    rank_tier: str = "ascendant",
    focus_mode: str = "tournament",
) -> str:
    """Create a persistent esports coaching arena session."""

    title_key = _normalize_title(title)
    template = TITLE_TEMPLATES[title_key]
    session_id = uuid.uuid4().hex[:10]
    state = {
        "session_id": session_id,
        "player_handle": player_handle.strip() or "Player One",
        "team_name": team_name.strip() or "Arena Squad",
        "title": title_key,
        "title_label": TITLE_LABELS[title_key],
        "role": (role or "igl").strip().lower(),
        "rank_tier": (rank_tier or "ascendant").strip(),
        "focus_mode": (focus_mode or "tournament").strip().lower(),
        "series_type": template["series_type"],
        "opponent_name": template["opponent_name"],
        "current_patch": template["current_patch"],
        "meta_snapshot": template["meta_snapshot"],
        "map_pool": template["map_pool"],
        "signature_pool": template["signature_pool"],
        "opponent_profile": template["opponent_profile"],
        "practice_modules": template["practice_modules"],
        "pressure_profile": template["pressure_profile"],
        "latest_reports": {},
        "latest_plan": {},
        "coach_log": [],
        "created_at": _now(),
        "updated_at": _now(),
    }
    _save_state(state)
    payload = {
        "session_id": session_id,
        "title": state["title"],
        "title_label": state["title_label"],
        "team_name": state["team_name"],
        "opponent_name": state["opponent_name"],
        "current_patch": state["current_patch"],
    }
    return json.dumps(payload, indent=2)


@mcp.tool()
def analyze_meta(session_id: str, priority: str = "balanced") -> str:
    """Create a current meta read for the selected title."""

    state = _load_state(session_id)
    priority_mode = (priority or "balanced").strip().lower()
    signals = list(state["meta_snapshot"])
    if priority_mode == "aggressive":
        signals.sort(key=lambda item: (item["weight"], "fast" in item["name"].lower()), reverse=True)
    elif priority_mode == "control":
        signals.sort(key=lambda item: ("late" in item["name"].lower(), item["weight"]), reverse=True)
    else:
        signals.sort(key=lambda item: item["weight"], reverse=True)
    top_signals = signals[:3]
    anchor = state["signature_pool"][0]["name"]
    report = {
        "priority": priority_mode,
        "top_signals": [
            {
                "name": item["name"],
                "weight": item["weight"],
                "reason": item["reason"],
                "leverage": f"Use {anchor} style setups to exploit {item['name'].lower()}."
            }
            for item in top_signals
        ],
        "power_play": f"Lean into {anchor} as the confidence pick if the opener feels stable.",
        "trap_to_avoid": "Do not copy the most popular fast look without a reset branch behind it.",
        "pressure_meter": state["pressure_profile"],
    }
    state.setdefault("latest_reports", {})["meta"] = report
    _save_state(state)
    return json.dumps(report, indent=2)


@mcp.tool()
def scout_opponent(session_id: str, emphasis: str = "default") -> str:
    """Scout the seeded opponent tendencies and find punish windows."""

    state = _load_state(session_id)
    maps = list(state["map_pool"])
    maps.sort(key=lambda item: (item["comfort"] - item["enemy_threat"]), reverse=True)
    best_map = maps[0]
    danger_map = sorted(maps, key=lambda item: item["enemy_threat"], reverse=True)[0]
    profile = state["opponent_profile"]
    emphasis_mode = (emphasis or "default").strip().lower()
    punish_windows = list(profile["tendencies"])[:2]
    if emphasis_mode == "tempo":
        punish_windows = [f"Break their rhythm when they {profile['tendencies'][0].lower()}"] + punish_windows[:1]
    report = {
        "emphasis": emphasis_mode,
        "tempo_profile": profile["tempo"],
        "style_summary": profile["style"],
        "punish_windows": punish_windows,
        "best_target_map": best_map["name"],
        "danger_map": danger_map["name"],
        "map_plan": best_map["plan"],
        "mental_note": "If they lose two clean rounds in a row, their pacing usually becomes predictable.",
    }
    state.setdefault("latest_reports", {})["scout"] = report
    _save_state(state)
    return json.dumps(report, indent=2)


@mcp.tool()
def build_draft_plan(session_id: str, style: str = "balanced") -> str:
    """Build a title-aware draft, veto, or signature-game plan."""

    state = _load_state(session_id)
    title = state["title"]
    style_mode = (style or "balanced").strip().lower()
    key_map = sorted(state["map_pool"], key=lambda item: item["comfort"], reverse=True)[0]["name"]
    signature_pick = state["signature_pool"][0]["name"]

    if title == "valorant":
        plan = {
            "style": style_mode,
            "ban_priority": ["Sunset", "Breach denial", "Operator comfort angles"],
            "lock_priority": [signature_pick, state["signature_pool"][1]["name"]],
            "pivot_call": "If the opener stalls, pivot into late mid split pressure instead of forcing contact.",
            "key_map": key_map,
            "signature_pick": signature_pick,
        }
    elif title == "league":
        plan = {
            "style": style_mode,
            "ban_priority": ["Primary comfort blind pick", "High-tempo jungler", "Backline dive enabler"],
            "lock_priority": [signature_pick, state["signature_pool"][1]["name"]],
            "pivot_call": "If first dragon is weak, trade top pressure instead of hard-contesting a bad setup.",
            "key_map": key_map,
            "signature_pick": signature_pick,
        }
    else:
        plan = {
            "style": style_mode,
            "ban_priority": ["Nuke", "Opponent comfort opener", "Fragile low-utility executes"],
            "lock_priority": [signature_pick, state["signature_pool"][1]["name"]],
            "pivot_call": "If defaults stall, call one fast contact before they can reset utility.",
            "key_map": key_map,
            "signature_pick": signature_pick,
        }

    state.setdefault("latest_reports", {})["draft"] = plan
    _save_state(state)
    return json.dumps(plan, indent=2)


@mcp.tool()
def design_training_block(session_id: str, intensity: str = "balanced") -> str:
    """Build a scrim and practice block for the upcoming match."""

    state = _load_state(session_id)
    mode = (intensity or "balanced").strip().lower()
    modules = list(state["practice_modules"])
    if mode == "high":
        focus_lanes = modules
    elif mode == "light":
        focus_lanes = modules[:2]
    else:
        focus_lanes = modules[:3]
    report = {
        "intensity": mode,
        "focus_lanes": [
            {
                "name": item["name"],
                "duration": item["duration"],
                "goal": item["goal"],
            }
            for item in focus_lanes
        ],
        "warmup_call": "Start with one confidence rep, then move immediately into the hardest scenario.",
        "vod_assignment": "Review the last lost mid-game sequence and identify the first communication drop.",
        "mechs_note": "Do not overload mechanics work if the bigger issue is timing discipline.",
    }
    state.setdefault("latest_reports", {})["training"] = report
    _save_state(state)
    return json.dumps(report, indent=2)


@mcp.tool()
def issue_mindset_protocol(session_id: str, pressure: str = "standard") -> str:
    """Create a mental reset and comms protocol for pressure moments."""

    state = _load_state(session_id)
    mode = (pressure or "standard").strip().lower()
    report = {
        "pressure": mode,
        "opening_comms": "First thirty seconds: short calls only, no second-guessing the opener.",
        "between_round_reset": "One breath, one fact, one next call.",
        "timeout_script": "Name the problem, choose one adjustment, commit to it with no debate.",
        "clutch_cue": "Play the numbers, not the noise.",
        "anti_tilt_rule": "No emotional review mid-series. Save blame for the VOD room.",
    }
    state.setdefault("latest_reports", {})["mindset"] = report
    _save_state(state)
    return json.dumps(report, indent=2)


@mcp.tool()
def lock_match_plan(
    session_id: str,
    headline: str,
    win_condition: str,
    danger_zone: str,
    tempo_call: str,
    confidence: float,
    key_map: str = "",
    signature_pick: str = "",
    bench_note: str = "",
) -> str:
    """Persist the main head-coach plan into arena state."""

    state = _load_state(session_id)
    latest_reports = state.get("latest_reports", {})
    state["latest_plan"] = {
        "headline": headline.strip(),
        "win_condition": win_condition.strip(),
        "danger_zone": danger_zone.strip(),
        "tempo_call": tempo_call.strip(),
        "confidence": float(confidence),
        "key_map": key_map.strip() or latest_reports.get("draft", {}).get("key_map", ""),
        "signature_pick": signature_pick.strip() or latest_reports.get("draft", {}).get("signature_pick", ""),
        "bench_note": bench_note.strip(),
        "meta_anchor": _top_signal_sign(latest_reports.get("meta", {})),
        "generated_at": _now(),
    }
    _save_state(state)
    return json.dumps(state["latest_plan"], indent=2)


@mcp.tool()
def append_coach_log(session_id: str, actor: str, content: str) -> str:
    """Append a timeline entry to the arena session."""

    state = _load_state(session_id)
    state.setdefault("coach_log", []).append(
        {"actor": actor.strip() or "Coach", "content": content.strip(), "timestamp": _now()}
    )
    _save_state(state)
    return json.dumps({"ok": True, "entries": len(state["coach_log"])}, indent=2)


@mcp.tool()
def list_sessions() -> str:
    """List saved arena sessions."""

    sessions: List[Dict[str, Any]] = []
    for path in sorted(ARENA_DIR.glob("*.json")):
        state = json.loads(path.read_text())
        sessions.append(
            {
                "session_id": state["session_id"],
                "player_handle": state["player_handle"],
                "team_name": state["team_name"],
                "title": state["title"],
                "title_label": state["title_label"],
                "opponent_name": state["opponent_name"],
                "focus_mode": state["focus_mode"],
                "updated_at": state["updated_at"],
            }
        )
    sessions.sort(key=lambda item: item["updated_at"], reverse=True)
    return json.dumps(sessions, indent=2)


@mcp.resource("arena://session/{session_id}")
def read_arena_state(session_id: str) -> str:
    """Read full arena session state."""

    return json.dumps(_load_state(session_id), indent=2)


@mcp.resource("arena://summary/{session_id}")
def read_arena_summary(session_id: str) -> str:
    """Read a compact arena session summary."""

    state = _load_state(session_id)
    payload = {
        "session_id": state["session_id"],
        "player_handle": state["player_handle"],
        "team_name": state["team_name"],
        "title": state["title"],
        "title_label": state["title_label"],
        "role": state["role"],
        "rank_tier": state["rank_tier"],
        "focus_mode": state["focus_mode"],
        "opponent_name": state["opponent_name"],
        "current_patch": state["current_patch"],
        "latest_reports": state["latest_reports"],
        "latest_plan": state["latest_plan"],
    }
    return json.dumps(payload, indent=2)


if __name__ == "__main__":
    mcp.run(transport="stdio")
