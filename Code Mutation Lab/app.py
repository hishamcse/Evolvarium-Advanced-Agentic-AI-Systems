"""
Code Mutation Lab — Gradio UI
Evolutionary code improvement through strategy-driven AI mutations.
Beautiful dark lab-style interface with live generation tracking.
"""
import html
import re
from typing import Any, Dict, List

import gradio as gr

from ui.css import APP_CSS
from ui.html import HERO_HTML, EMPTY_STATE_HTML

from graph.builder import build_graph

graph = build_graph()

SAMPLE_CODE = '''def find_duplicates(lst):
    duplicates = []
    for i in range(len(lst)):
        for j in range(i + 1, len(lst)):
            if lst[i] == lst[j]:
                if lst[i] not in duplicates:
                    duplicates.append(lst[i])
    return duplicates


def flatten_nested(nested_list):
    result = []
    for item in nested_list:
        if type(item) == list:
            for sub in flatten_nested(item):
                result.append(sub)
        else:
            result.append(item)
    return result


def count_words(text):
    word_count = {}
    words = text.split(" ")
    for word in words:
        word = word.lower()
        if word in word_count:
            word_count[word] = word_count[word] + 1
        else:
            word_count[word] = 1
    return word_count
'''

# ── Helpers ────────────────────────────────────────────────────────────────────

def _esc(v: Any) -> str:
    return html.escape(str(v or ""))

def _score_color(s: float) -> str:
    if s >= 8: return "var(--green)"
    if s >= 6: return "var(--lime)"
    if s >= 4: return "var(--gold)"
    return "var(--red)"

def _strategy_chip_class(strategy: str) -> str:
    s = strategy.lower()
    if "performance" in s or "time" in s or "complex" in s: return "strat-perf"
    if "readab" in s or "structure" in s:                   return "strat-read"
    if "memory" in s:                                        return "strat-mem"
    if "pythonic" in s or "python" in s:                    return "strat-pyth"
    if "simplif" in s or "redundan" in s or "clean" in s:  return "strat-simp"
    if "functional" in s:                                    return "strat-func"
    return ""

def _score_bar(score: float, color: str) -> str:
    pct = int((score / 10) * 100)
    return f"""
<div class="lab-score-bar">
  <div class="lab-score-bar-track">
    <div class="lab-score-bar-fill" style="width:{pct}%;background:{color}"></div>
  </div>
</div>"""

def _improvement_chip(delta: float) -> str:
    if delta > 0.05:
        return f'<span class="lab-gen-improvement improvement-up">+{delta:.2f} ▲</span>'
    if delta < -0.05:
        return f'<span class="lab-gen-improvement improvement-down">{delta:.2f} ▼</span>'
    return f'<span class="lab-gen-improvement improvement-same">= {delta:+.2f}</span>'


# ── Render: score summary panel ────────────────────────────────────────────────

def _render_summary_panel(history: List[Dict]) -> str:
    if not history:
        return EMPTY_STATE_HTML

    first_score = history[0]["selected"]["score"]
    last        = history[-1]["selected"]
    final_score = last["score"]
    delta       = final_score - first_score
    total_vars  = sum(len(r["variants"]) for r in history)
    best_strat  = last.get("strategy", "N/A")
    breakdown   = last.get("breakdown", {})
    gens        = len(history)

    delta_color = "var(--green)" if delta >= 0 else "var(--red)"
    delta_sign  = "+" if delta >= 0 else ""
    color       = _score_color(final_score)

    p_score = breakdown.get("performance", 0)
    r_score = breakdown.get("readability", 0)
    s_score = breakdown.get("simplicity", 0)

    strat_cls = _strategy_chip_class(best_strat)

    return f"""
<div class="lab-panel">
  <div class="lab-panel-label">Evolution result</div>

  <div style="display:flex;align-items:center;gap:20px;margin-bottom:20px">
    <div>
      <div class="lab-score-ring" style="border-color:{color};color:{color}">{final_score:.1f}</div>
    </div>
    <div style="flex:1">
      <div style="font-size:11px;color:var(--muted);text-transform:uppercase;letter-spacing:.12em;margin-bottom:4px">Final fitness score</div>
      <div style="font-size:13px;color:var(--text);margin-bottom:8px">
        Started at <strong style="color:var(--muted)">{first_score:.1f}</strong> &nbsp;→&nbsp;
        <strong style="color:{color}">{final_score:.1f}</strong> &nbsp;
        <span style="color:{delta_color};font-weight:700;font-size:13px">({delta_sign}{delta:.2f})</span>
      </div>
      <div class="lab-strategy-chips">
        <span class="lab-strategy-chip {strat_cls}">{_esc(best_strat)}</span>
      </div>
    </div>
  </div>

  <div class="lab-control-grid">
    <div class="lab-stat-card">
      <div class="lab-stat-label">Generations run</div>
      <div class="lab-stat-value">{gens}</div>
      <div class="lab-stat-sub">{total_vars} total variants tested</div>
    </div>
    <div class="lab-stat-card">
      <div class="lab-stat-label">Score improvement</div>
      <div class="lab-stat-value" style="color:{delta_color}">{delta_sign}{delta:.2f}</div>
      <div class="lab-stat-sub">{abs(delta/first_score*100):.0f}% change from seed</div>
    </div>
  </div>

  <div class="lab-panel-label" style="margin-top:16px">Dimension breakdown — final generation</div>
  <div class="lab-dim-row">
    <div class="lab-dim-cell">
      <div class="lab-dim-cell-label">Performance</div>
      <div class="lab-dim-cell-value" style="color:{_score_color(p_score)}">{p_score:.1f}</div>
      {_score_bar(p_score, _score_color(p_score))}
    </div>
    <div class="lab-dim-cell">
      <div class="lab-dim-cell-label">Readability</div>
      <div class="lab-dim-cell-value" style="color:{_score_color(r_score)}">{r_score:.1f}</div>
      {_score_bar(r_score, _score_color(r_score))}
    </div>
    <div class="lab-dim-cell">
      <div class="lab-dim-cell-label">Simplicity</div>
      <div class="lab-dim-cell-value" style="color:{_score_color(s_score)}">{s_score:.1f}</div>
      {_score_bar(s_score, _score_color(s_score))}
    </div>
  </div>
</div>"""


# ── Render: fitness chart ──────────────────────────────────────────────────────

def _render_fitness_chart(history: List[Dict]) -> str:
    if not history:
        return ""
    max_score = max((r["selected"]["score"] for r in history), default=10)
    max_score = max(max_score, 0.1)

    rows = []
    prev_score = None
    for rec in history:
        gen   = rec["generation"]
        score = rec["selected"]["score"]
        pct   = int((score / 10) * 100)
        color = _score_color(score)
        delta = (score - prev_score) if prev_score is not None else 0
        chip  = _improvement_chip(delta) if prev_score is not None else ""
        prev_score = score

        rows.append(f"""
<div class="lab-fitness-row">
  <div class="lab-fitness-gen">Gen {gen}</div>
  <div class="lab-fitness-track">
    <div class="lab-fitness-bar" style="width:{pct}%;background:{color}"></div>
  </div>
  <div class="lab-fitness-score" style="color:{color}">{score:.1f}</div>
</div>
{f'<div style="padding:0 0 4px 70px">{chip}</div>' if chip else ""}""")

    return f"""
<div class="lab-panel">
  <div class="lab-panel-label">Fitness across generations</div>
  <div class="lab-fitness">{"".join(rows)}</div>
</div>"""


# ── Render: generation timeline ────────────────────────────────────────────────

def _render_timeline(history: List[Dict]) -> str:
    if not history:
        return EMPTY_STATE_HTML
    rows = []
    for rec in history:
        gen    = rec["generation"]
        best   = rec["selected"]
        score  = best["score"]
        strat  = best.get("strategy", "N/A")
        color  = _score_color(score)
        bd     = best.get("breakdown", {})
        cls    = _strategy_chip_class(strat)

        rows.append(f"""
<div class="lab-gen-row">
  <div class="lab-gen-badge">
    Gen {gen}<br>
    <span class="lab-gen-score" style="color:{color}">{score:.1f}</span>
  </div>
  <div class="lab-gen-card">
    <div class="lab-strategy-chips" style="margin-bottom:10px">
      <span class="lab-strategy-chip {cls}">{_esc(strat)}</span>
    </div>
    <div class="lab-dim-row" style="grid-template-columns:repeat(3,1fr)">
      <div class="lab-dim-cell">
        <div class="lab-dim-cell-label">Perf</div>
        <div class="lab-dim-cell-value" style="color:{_score_color(bd.get('performance',0))}">{bd.get('performance',0):.1f}</div>
      </div>
      <div class="lab-dim-cell">
        <div class="lab-dim-cell-label">Read</div>
        <div class="lab-dim-cell-value" style="color:{_score_color(bd.get('readability',0))}">{bd.get('readability',0):.1f}</div>
      </div>
      <div class="lab-dim-cell">
        <div class="lab-dim-cell-label">Simp</div>
        <div class="lab-dim-cell-value" style="color:{_score_color(bd.get('simplicity',0))}">{bd.get('simplicity',0):.1f}</div>
      </div>
    </div>
    <div style="font-size:12px;color:var(--muted);margin-top:10px;line-height:1.5">{_esc(best.get('feedback',''))[:220]}</div>
  </div>
</div>""")

    return f"""
<div class="lab-panel">
  <div class="lab-panel-label">Generation timeline</div>
  <div class="lab-gen-timeline">{"".join(rows)}</div>
</div>"""


# ── Render: variant explorer ───────────────────────────────────────────────────

def _render_variants(history: List[Dict]) -> str:
    if not history:
        return EMPTY_STATE_HTML
    sections = []
    for rec in history:
        gen      = rec["generation"]
        variants = rec["variants"]
        best_idx = max(range(len(variants)), key=lambda i: variants[i].get("score", 0)) if variants else -1

        cards = []
        for i, v in enumerate(variants):
            score  = v.get("score", 0)
            strat  = v.get("strategy", "N/A")
            bd     = v.get("breakdown", {})
            color  = _score_color(score)
            winner = i == best_idx
            cls    = _strategy_chip_class(strat)
            pct    = int((score / 10) * 100)

            crown = '<span class="lab-winner-crown">&#9651; Selected</span>' if winner else ""
            card_cls = "lab-variant-card" + (" lab-variant-winner" if winner else "")

            code_preview = _esc(v.get("code","")[:300]).replace("\n","<br>").replace(" ","&nbsp;")

            cards.append(f"""
<div class="{card_cls}">
  <div class="lab-variant-header">
    <div class="lab-strategy-chips" style="margin:0">
      <span class="lab-strategy-chip {cls}">{_esc(strat)}</span>
    </div>
    <div style="display:flex;align-items:center;gap:10px">
      {crown}
      <span style="font-size:22px;font-weight:900;color:{color}">{score:.1f}</span>
    </div>
  </div>
  <div class="lab-score-bar-track" style="margin-bottom:12px">
    <div class="lab-score-bar-fill" style="width:{pct}%;background:{color}"></div>
  </div>
  <div class="lab-dim-row">
    <div class="lab-dim-cell">
      <div class="lab-dim-cell-label">Performance</div>
      <div class="lab-dim-cell-value" style="color:{_score_color(bd.get('performance',0))}">{bd.get('performance',0):.1f}</div>
    </div>
    <div class="lab-dim-cell">
      <div class="lab-dim-cell-label">Readability</div>
      <div class="lab-dim-cell-value" style="color:{_score_color(bd.get('readability',0))}">{bd.get('readability',0):.1f}</div>
    </div>
    <div class="lab-dim-cell">
      <div class="lab-dim-cell-label">Simplicity</div>
      <div class="lab-dim-cell-value" style="color:{_score_color(bd.get('simplicity',0))}">{bd.get('simplicity',0):.1f}</div>
    </div>
  </div>
  <div style="margin-top:12px;font-size:12px;color:var(--muted);line-height:1.5">{_esc(v.get('feedback',''))[:200]}</div>
</div>""")

        sections.append(f"""
<div style="margin-bottom:24px">
  <div class="lab-panel-label" style="margin-bottom:12px">Generation {gen} — {len(variants)} variants competed</div>
  <div class="lab-variant-grid">{"".join(cards)}</div>
</div>""")

    return f'<div class="lab-panel">{"".join(sections)}</div>'


# ── Render: diff view ──────────────────────────────────────────────────────────

def _render_diff_labels() -> str:
    return """
<div class="lab-diff-header">
  <span class="lab-diff-label diff-original">Original seed</span>
  <span style="color:var(--muted);font-size:13px">→</span>
  <span class="lab-diff-label diff-evolved">Final evolved</span>
</div>"""


# ── Core run function ──────────────────────────────────────────────────────────

def run_mutation(code: str, generations: int):
    if not code or not code.strip():
        empty = gr.update(value=EMPTY_STATE_HTML)
        return "", empty, empty, empty, empty

    initial_state = {
        "original_code": code,
        "current_code":  code,
        "generation":    0,
        "max_generations": int(generations),
        "variants":      [],
        "history":       [],
    }

    result   = graph.invoke(initial_state)
    history  = result.get("history", [])
    best     = result.get("current_code", code)

    summary_html  = _render_summary_panel(history)
    fitness_html  = _render_fitness_chart(history)
    timeline_html = _render_timeline(history)
    variants_html = _render_variants(history)

    return (
        best,
        gr.update(value=summary_html),
        gr.update(value=fitness_html),
        gr.update(value=timeline_html),
        gr.update(value=variants_html),
    )


# ── Build UI ───────────────────────────────────────────────────────────────────

def build_ui():
    with gr.Blocks(css=APP_CSS, title="Code Mutation Lab") as demo:
        with gr.Column(elem_classes="lab-shell"):
            gr.HTML(HERO_HTML)

            # ── Input row ──
            with gr.Row(equal_height=False):
                with gr.Column(scale=5, min_width=340):
                    gr.HTML('<div style="padding:4px 0 2px"><span class="lab-panel-label">Seed code</span></div>')
                    code_input = gr.Code(
                        label="",
                        language="python",
                        value=SAMPLE_CODE,
                        lines=22,
                    )
                    with gr.Row():
                        gen_slider = gr.Slider(
                            minimum=1, maximum=6, value=3, step=1,
                            label="Generations",
                            scale=3,
                        )
                        run_btn = gr.Button("Evolve Code  ▶", variant="primary", scale=2)

                with gr.Column(scale=4, min_width=280):
                    summary_panel = gr.HTML(value=EMPTY_STATE_HTML)

            # ── Fitness chart + evolved code side by side ──
            with gr.Row(equal_height=False):
                with gr.Column(scale=1):
                    fitness_panel = gr.HTML(value="")
                with gr.Column(scale=1):
                    gr.HTML(_render_diff_labels())
                    evolved_code = gr.Code(
                        label="",
                        language="python",
                        lines=18,
                        interactive=False,
                    )

            # ── Tabs: timeline + variants ──
            with gr.Tabs():
                with gr.Tab("Generation timeline"):
                    timeline_panel = gr.HTML(value="")
                with gr.Tab("Variant explorer"):
                    variants_panel = gr.HTML(value="")

        # ── Events ──
        run_btn.click(
            fn=run_mutation,
            inputs=[code_input, gen_slider],
            outputs=[evolved_code, summary_panel, fitness_panel, timeline_panel, variants_panel],
        )

    return demo


if __name__ == "__main__":
    build_ui().launch(server_name="0.0.0.0", server_port=7861, show_error=True)