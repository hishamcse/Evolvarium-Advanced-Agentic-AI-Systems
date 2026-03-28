from typing import Any, Dict


PRODUCT_TEMPLATES: Dict[str, Dict[str, Any]] = {
    "ai_tool": {
        "market_signal": "AI buyers are increasingly skeptical of broad claims and respond better to narrow workflow wins.",
        "competitor_pressure": "Crowded category with fast copycat positioning.",
        "buyer_mindset": "Users want a concrete time-saving or revenue-moving outcome in the first demo.",
        "channels": ["X", "LinkedIn", "waitlist landing page", "product community demos"],
        "proof_assets": ["before/after workflow demo", "customer quote", "short teardown video"],
        "primary_segments": ["technical founders", "ops-heavy teams", "AI-forward solo builders"],
        "promise_shape": "one painful workflow turned into one sharp visible win",
        "urgency_hooks": ["ship faster than manual workflow", "replace vague AI with a measurable outcome"],
        "launch_motion": "founder-led proof drop",
        "message_tone": ["specific", "confident", "credible"],
    },
    "saas": {
        "market_signal": "SaaS launches are landing better when the value story is very operational and role-specific.",
        "competitor_pressure": "Mid-market incumbents move slower but own trust by default.",
        "buyer_mindset": "Operators want predictable gains, low switching pain, and clear team adoption paths.",
        "channels": ["LinkedIn", "email list", "founder-led outbound", "partner communities"],
        "proof_assets": ["ROI calculator", "playbook PDF", "pilot case study"],
        "primary_segments": ["revenue operators", "customer success leads", "ops managers"],
        "promise_shape": "less operational drag and more predictable throughput",
        "urgency_hooks": ["recover wasted operator hours", "reduce team bottlenecks before the next quarter"],
        "launch_motion": "problem-solution case study rollout",
        "message_tone": ["practical", "trustworthy", "role-aware"],
    },
    "devtool": {
        "market_signal": "Developer products spread fastest when the setup path is obvious and the demo is instantly legible.",
        "competitor_pressure": "Open-source alternatives shape expectations around speed and clarity.",
        "buyer_mindset": "Developers reward sharp workflows and punish vague value language.",
        "channels": ["GitHub", "X", "Discord communities", "technical launch post"],
        "proof_assets": ["quickstart repo", "benchmark chart", "architecture diagram"],
        "primary_segments": ["indie hackers", "staff engineers", "platform teams"],
        "promise_shape": "a faster path from setup to first working output",
        "urgency_hooks": ["ship the first working path in one sitting", "remove setup friction from the toolchain"],
        "launch_motion": "technical demo plus public build log",
        "message_tone": ["precise", "fast", "builder-first"],
    },
    "consumer_app": {
        "market_signal": "Consumer launches work best when the first use case is emotionally obvious and easy to share.",
        "competitor_pressure": "Retention pressure is high unless the first session creates a memorable payoff.",
        "buyer_mindset": "Users need a fast wow moment before they care about depth.",
        "channels": ["TikTok", "Instagram", "creator partnerships", "landing page"],
        "proof_assets": ["UGC clips", "social proof", "challenge or referral loop"],
        "primary_segments": ["social-first early adopters", "creator audiences", "habit-driven mobile users"],
        "promise_shape": "one instantly satisfying action that people want to repeat or share",
        "urgency_hooks": ["feel the payoff in the first session", "give people something worth showing friends"],
        "launch_motion": "creator-driven reveal burst",
        "message_tone": ["punchy", "visual", "shareable"],
    },
}

STAGE_PLAYBOOKS: Dict[str, Dict[str, Any]] = {
    "idea": {
        "readiness_focus": "validate the promise before scaling attention",
        "proof_requirement": "concept proof and narrative clarity",
        "asset_priority": ["explainer mockup", "founder story", "waitlist hook"],
        "tempo": "tight and exploratory",
        "runway_days": 10,
    },
    "alpha": {
        "readiness_focus": "show that the product works for a narrow audience",
        "proof_requirement": "early demos and implementation confidence",
        "asset_priority": ["live walkthrough", "early tester note", "use-case breakdown"],
        "tempo": "focused and iterative",
        "runway_days": 12,
    },
    "beta": {
        "readiness_focus": "turn early trust into signups or pilots",
        "proof_requirement": "clear before/after evidence and audience fit",
        "asset_priority": ["use-case demo", "proof snippet", "landing page CTA"],
        "tempo": "confident and sequenced",
        "runway_days": 14,
    },
    "live": {
        "readiness_focus": "convert attention into revenue or sustained adoption",
        "proof_requirement": "repeatable proof and buyer trust",
        "asset_priority": ["customer story", "comparison proof", "conversion asset"],
        "tempo": "measured and scalable",
        "runway_days": 21,
    },
}

BUDGET_PLAYBOOKS: Dict[str, Dict[str, Any]] = {
    "lean": {
        "channel_bias": "organic channels and founder energy",
        "asset_depth": "lightweight but sharp assets",
        "paid_support": "minimal paid support",
        "team_shape": "founder-led execution",
    },
    "moderate": {
        "channel_bias": "organic channels with targeted amplification",
        "asset_depth": "balanced proof and campaign assets",
        "paid_support": "light paid experiments",
        "team_shape": "small cross-functional launch pod",
    },
    "aggressive": {
        "channel_bias": "multi-channel launch with coordinated push",
        "asset_depth": "full stack of proof, visuals, and follow-up assets",
        "paid_support": "strong paid support",
        "team_shape": "dedicated launch squad",
    },
}

GOAL_PLAYBOOKS: Dict[str, Dict[str, Any]] = {
    "beta waitlist": {
        "north_star": "qualified waitlist signups",
        "primary_cta": "join the waitlist",
        "proof_bias": "show the first compelling use case",
        "preferred_channels": ["waitlist landing page", "X", "LinkedIn"],
    },
    "early revenue": {
        "north_star": "revenue and qualified demos",
        "primary_cta": "book a demo or start paying",
        "proof_bias": "show ROI and switching confidence",
        "preferred_channels": ["LinkedIn", "email list", "founder-led outbound"],
    },
    "pilot signups": {
        "north_star": "pilot commitments",
        "primary_cta": "apply for a pilot",
        "proof_bias": "show implementation confidence and support",
        "preferred_channels": ["LinkedIn", "partner communities", "email list"],
    },
    "community growth": {
        "north_star": "repeat engagement and community participation",
        "primary_cta": "join the community",
        "proof_bias": "show belonging and momentum",
        "preferred_channels": ["Discord communities", "X", "creator partnerships"],
    },
}


def normalize_product_type(product_type: str) -> str:
    key = (product_type or "ai_tool").strip().lower()
    return key if key in PRODUCT_TEMPLATES else "ai_tool"


def normalize_stage(stage: str) -> str:
    key = (stage or "beta").strip().lower()
    return key if key in STAGE_PLAYBOOKS else "beta"


def normalize_budget(budget_band: str) -> str:
    key = (budget_band or "lean").strip().lower()
    return key if key in BUDGET_PLAYBOOKS else "lean"


def normalize_goal(launch_goal: str) -> str:
    key = (launch_goal or "beta waitlist").strip().lower()
    return key if key in GOAL_PLAYBOOKS else "beta waitlist"


def build_context_profile(state: Dict[str, Any]) -> Dict[str, Any]:
    product_type = normalize_product_type(state.get("product_type", "ai_tool"))
    stage = normalize_stage(state.get("stage", "beta"))
    budget = normalize_budget(state.get("budget_band", "lean"))
    goal = normalize_goal(state.get("launch_goal", "beta waitlist"))
    return {
        "product": PRODUCT_TEMPLATES[product_type],
        "stage": STAGE_PLAYBOOKS[stage],
        "budget": BUDGET_PLAYBOOKS[budget],
        "goal": GOAL_PLAYBOOKS[goal],
    }
