from typing import Dict, List, Optional

from typing_extensions import TypedDict


class LaunchState(TypedDict):
    session_id: Optional[str]
    startup_name: str
    product_name: str
    product_type: str
    stage: str
    budget_band: str
    launch_goal: str
    user_request: str
    session_json: str
    plan_json: str
    step_order: List[str]
    execution_cursor: int
    market_report: str
    icp_report: str
    messaging_report: str
    timeline_report: str
    final_board_json: str
    final_response: str
    feedback: str
    retry_count: int
    max_retries: int
    step_outputs: Dict[str, str]
