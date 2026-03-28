import gradio as gr

from launchpad_strategist.ui.actions import (
    BUDGETS,
    GOALS,
    PRODUCT_TYPES,
    STAGES,
    engine,
    load_session,
    run_launch,
    start_session,
)
from launchpad_strategist.ui.theme import APP_CSS
from launchpad_strategist.ui.views.dashboard import render_banner, render_log
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


def build_demo():
    with gr.Blocks(theme=gr.themes.Base(), css=APP_CSS, title="Launchpad Strategist Agent") as demo:
        gr.Markdown(
            """
            # Launchpad Strategist Agent
            A plan-and-execute launch mission-control room for product positioning, audience lock, messaging, and rollout planning.
            """
        )

        session_id_state = gr.State("")

        with gr.Tab("Mission Control"):
            with gr.Row(equal_height=False):
                with gr.Column(scale=4):
                    banner = gr.HTML(render_banner({}))
                with gr.Column(scale=2):
                    with gr.Group():
                        startup_name = gr.Textbox(label="Startup Name", value="Northstar Labs")
                        product_name = gr.Textbox(label="Product Name", value="SignalForge")
                        product_type = gr.Dropdown(label="Product Type", choices=PRODUCT_TYPES, value="ai_tool")
                        stage = gr.Dropdown(label="Stage", choices=STAGES, value="beta")
                        budget_band = gr.Dropdown(label="Budget Band", choices=BUDGETS, value="lean")
                        launch_goal = gr.Dropdown(label="Launch Goal", choices=GOALS, value="beta waitlist")
                        start_button = gr.Button("Open Launch Room", variant="primary")

            with gr.Row():
                strategist_chat = gr.Chatbot(label="Mission Console", type="messages", height=340)
                latest_brief = gr.Markdown()

            request_box = gr.Textbox(
                label="Ask Mission Control",
                placeholder="Example: Plan a lean beta waitlist launch for technical founders with stronger proof and a faster launch runway.",
                lines=3,
            )

            gr.Examples(
                examples=[
                    "Plan a lean beta waitlist launch for our AI tool.",
                    "We need sharper positioning for technical founders and a stronger message stack.",
                    "Give me a low-budget launch sequence with clearer proof and urgency.",
                ],
                inputs=request_box,
                label="Quick Launch Calls",
            )

            run_button = gr.Button("Generate Launch Board", variant="primary")

            with gr.Row():
                strategy_board = gr.HTML(render_strategy_board({}))
                signal_strip = gr.HTML(render_signal_strip({}))

            with gr.Row():
                audience_panel = gr.HTML(render_audience_panel({}))
                channel_mix = gr.HTML(render_channel_mix({}))

            with gr.Row():
                message_lab = gr.HTML(render_message_lab({}))
                proof_stack = gr.HTML(render_proof_stack({}))

            timeline_panel = gr.HTML(render_timeline_panel({}))
            operator_board = gr.HTML(render_operator_board({}))
            command_feed = gr.HTML(render_log({}))

        with gr.Tab("Session Vault"):
            session_picker = gr.Dropdown(label="Load Saved Session", choices=[item["session_id"] for item in engine.list_sessions()])
            load_button = gr.Button("Load Session")
            sessions_json = gr.JSON(label="Session Index", value=engine.list_sessions())

        with gr.Tab("Debug"):
            debug_state = gr.Code(label="Launch State JSON", language="json", value="{}")

        start_button.click(
            start_session,
            inputs=[startup_name, product_name, product_type, stage, budget_band, launch_goal],
            outputs=[
                strategist_chat,
                request_box,
                latest_brief,
                banner,
                strategy_board,
                signal_strip,
                audience_panel,
                channel_mix,
                message_lab,
                proof_stack,
                timeline_panel,
                operator_board,
                command_feed,
                debug_state,
                session_id_state,
                sessions_json,
                session_picker,
            ],
        )

        run_button.click(
            run_launch,
            inputs=[
                request_box,
                strategist_chat,
                session_id_state,
                startup_name,
                product_name,
                product_type,
                stage,
                budget_band,
                launch_goal,
            ],
            outputs=[
                strategist_chat,
                request_box,
                latest_brief,
                banner,
                strategy_board,
                signal_strip,
                audience_panel,
                channel_mix,
                message_lab,
                proof_stack,
                timeline_panel,
                operator_board,
                command_feed,
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
                strategist_chat,
                request_box,
                latest_brief,
                banner,
                strategy_board,
                signal_strip,
                audience_panel,
                channel_mix,
                message_lab,
                proof_stack,
                timeline_panel,
                operator_board,
                command_feed,
                debug_state,
                session_id_state,
                sessions_json,
                session_picker,
                startup_name,
                product_name,
                product_type,
                stage,
                budget_band,
                launch_goal,
            ],
        )
    return demo
