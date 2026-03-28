from typing import List

from pydantic import BaseModel, Field


class ExecutionPlan(BaseModel):
    objective: str = Field(description="The core launch objective.")
    launch_angle: str = Field(description="The strongest framing angle for the launch.")
    rationale: str = Field(description="Why this execution sequence makes sense.")
    step_order: List[str] = Field(description="Execution steps in order using market, icp, messaging, timeline.")
    confidence: float = Field(description="Confidence score between 0 and 1.")


class LaunchBoard(BaseModel):
    headline: str = Field(description="Short launch-board headline.")
    launch_angle: str = Field(description="Main positioning direction.")
    primary_audience: str = Field(description="Most important audience segment.")
    hero_message: str = Field(description="Best top-line message.")
    channel_focus: List[str] = Field(description="Best channels to prioritize first.")
    launch_sequence: List[str] = Field(description="Ordered launch actions.")
    proof_stack: List[str] = Field(description="Key proof points or trust builders.")
    risk_watch: str = Field(description="Primary launch risk to watch.")
    next_best_action: str = Field(description="Most important next move.")


class LaunchReview(BaseModel):
    approved: bool = Field(description="Whether the final brief is clear and actionable.")
    feedback: str = Field(description="Brief revision feedback when not approved.")
