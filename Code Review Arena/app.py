"""
Code Review Arena — Gradio UI
Beautiful dark arena-style interface with rich HTML panels.
"""
import html
import json
import re
from collections import Counter
from typing import Any, Dict, List, Optional

import gradio as gr

from ui.css import APP_CSS
from ui.html import HERO_HTML

from graph import CodeReviewEngine

engine = CodeReviewEngine()

SAMPLE = '''import sqlite3, subprocess, pickle

def get_user(username):
    conn = sqlite3.connect("users.db")
    query = f"SELECT * FROM users WHERE name = \'{username}\'"
    return conn.execute(query).fetchall()

def run_report(name):
    return subprocess.run(f"generate {name}", shell=True, capture_output=True).stdout

def load_data(filename):
    with open(filename, "rb") as f:
        return pickle.load(f)

def fibonacci(n):
    if n <= 0:
        return []
    result = []
    for i in range(n):
        a, b, fib = 0, 1, []
        for j in range(i + 1):
            fib.append(a); a, b = b, a + b
        result.append(fib[-1])
    return result

SECRET_KEY = "hardcoded_secret_abc123"
API_TOKEN  = "tok_live_xyz987654321"
'''


# ── Helpers ────────────────────────────────────────────────────────────────────

def _esc(v):
    return html.escape(str(v or ""))

def _score_color(s):
    if s >= 8: return "var(--green)"
    if s >= 5: return "var(--gold)"
    return "var(--red)"

def _md_to_html(text):
    lines = str(text or "").splitlines()
    chunks, li_buf = [], []

    def flush():
        if li_buf:
            chunks.append("<ul style='padding-left:18px;margin:6px 0'>" + "".join(li_buf) + "</ul>")
            li_buf.clear()

    def inline(t):
        t = html.escape(t)
        t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
        t = re.sub(r"`(.+?)`", r"<code>\1</code>", t)
        return t

    for raw in lines:
        l = raw.strip()
        if not l: flush(); continue
        if l.startswith("### "): flush(); chunks.append(f"<div style='font-size:10px;text-transform:uppercase;letter-spacing:.14em;color:var(--cyan);margin:12px 0 5px;font-weight:700'>{inline(l[4:])}</div>"); continue
        if l.upper().startswith("SCORE:"): flush(); continue
        if l.upper().startswith("ISSUES:"): flush(); chunks.append("<div style='font-size:10px;text-transform:uppercase;letter-spacing:.14em;color:var(--muted);margin:10px 0 5px;font-weight:700'>Issues found</div>"); continue
        if l.upper().startswith("RECOMMENDATION:"): flush(); chunks.append("<div style='font-size:10px;text-transform:uppercase;letter-spacing:.14em;color:var(--gold);margin:10px 0 5px;font-weight:700'>Recommendation</div>"); continue
        if l.startswith(("- ", "* ")): li_buf.append(f"<li style='margin-bottom:5px'>{inline(l[2:])}</li>"); continue
        flush()
        chunks.append(f"<p style='margin:0 0 7px'>{inline(l)}</p>")
    flush()
    return "".join(chunks) or "<span style='color:var(--muted);font-style:italic'>No output.</span>"

def _dim_bar(label, score, color):
    pct = int((score / 10) * 100)
    return f"""
<div class="cra-dim">
  <div class="cra-dim-header">
    <span class="cra-dim-name">{label}</span>
    <span class="cra-dim-score" style="color:{color}">{score:.1f}</span>
  </div>
  <div class="cra-dim-track">
    <div class="cra-dim-fill" style="width:{pct}%;background:{color}"></div>
  </div>
</div>"""

def _chip(sev, count):
    cls = {"CRITICAL":"chip-critical","HIGH":"chip-high","MEDIUM":"chip-medium","LOW":"chip-low"}.get(sev,"chip-low")
    return f'<span class="cra-chip {cls}">{sev} &nbsp;{count}</span>'

def _severity_chips(issues):
    counts = Counter(i["severity"] for i in issues)
    return "".join(_chip(s, counts[s]) for s in ["CRITICAL","HIGH","MEDIUM","LOW"] if s in counts)

def _issue_list(issues):
    if not issues:
        return "<div style='color:var(--green);font-size:13px;padding:10px 0'>No issues detected — code looks clean!</div>"
    rows = []
    for iss in issues[:16]:
        sev = iss["severity"]
        cls = {"CRITICAL":"chip-critical","HIGH":"chip-high","MEDIUM":"chip-medium","LOW":"chip-low"}.get(sev,"chip-low")
        role_cls = f"actor-{iss['role']}"
        rows.append(f"""<div class="cra-issue">
  <span class="cra-chip {cls}" style="font-size:10px;padding:3px 9px">{sev}</span>
  <span class="cra-timeline-actor {role_cls}" style="padding:3px 9px;border-radius:8px;font-size:10px;border-width:1px">{iss['role']}</span>
  <span class="cra-issue-desc">{_esc(iss['description'])}</span>
</div>""")
    return f'<div class="cra-issue-list">{"".join(rows)}</div>'

def _agent_card(role, review_text, score):
    color = _score_color(score)
    body = _md_to_html(review_text)
    return f"""<div class="cra-timeline-row">
  <div class="cra-timeline-actor actor-{role}">
    {role.upper()}<br>
    <span class="cra-timeline-score" style="color:{color}">{score:.1f}</span>
  </div>
  <div class="cra-timeline-card">{body}</div>
</div>"""


# ── Render panels ──────────────────────────────────────────────────────────────

def _render_empty_score():
    return """<div class="cra-panel" style="text-align:center;padding:48px 20px">
  <div style="color:var(--muted);font-size:14px;margin-bottom:10px">Awaiting review</div>
  <div style="font-size:48px;color:var(--border-hi)">&#9655;</div>
  <div style="color:var(--muted);font-size:12px;margin-top:10px">Paste code, then click Run Arena Review</div>
</div>"""

def _render_score_panel(overall, scores, lang, session_id, issues):
    color = _score_color(overall)
    dims = "".join(_dim_bar(r.capitalize(), scores.get(r, 0), _score_color(scores.get(r, 0)))
                   for r in ["security","performance","logic","style"])
    chips = _severity_chips(issues)
    return f"""<div class="cra-panel">
  <div class="cra-score-wrap">
    <div class="cra-score-ring" style="border-color:{color};color:{color}">{overall:.1f}</div>
    <div class="cra-score-label">Overall Quality Score</div>
  </div>
  <div style="text-align:center;margin-bottom:16px">
    <span class="cra-badge">{lang.upper()}</span>&nbsp;
    <span class="cra-badge" style="font-family:monospace;font-size:11px;color:var(--muted);background:rgba(255,255,255,0.04);border-color:rgba(255,255,255,0.10)">{session_id}</span>
  </div>
  <div class="cra-chips">{chips}</div>
  <div style="margin-top:18px">
    <div class="cra-panel-label">Dimension scores</div>
    {dims}
  </div>
</div>"""

def _render_summary(summary, overall, top_issues):
    critical = sum(1 for i in top_issues if i["severity"] == "CRITICAL")
    high     = sum(1 for i in top_issues if i["severity"] == "HIGH")
    total    = len(top_issues)
    grade    = "A" if overall >= 9 else "B" if overall >= 7.5 else "C" if overall >= 6 else "D" if overall >= 4 else "F"
    color    = _score_color(overall)
    return f"""<div class="cra-panel">
  <div class="cra-panel-label">Executive Summary</div>
  <div class="cra-summary-hero">{_esc(summary)}</div>
  <div class="cra-plan-grid" style="margin-top:14px">
    <div class="cra-stat-card">
      <div class="cra-stat-label">Grade</div>
      <div style="font-size:48px;font-weight:900;color:{color};line-height:1">{grade}</div>
    </div>
    <div class="cra-stat-card">
      <div class="cra-stat-label">Issues found</div>
      <div class="cra-stat-value">
        <span style="color:var(--red);font-weight:700;font-size:15px">{critical}</span>
        <span style="color:var(--muted);font-size:12px"> critical&nbsp;&nbsp;</span>
        <span style="color:var(--orange);font-weight:700;font-size:15px">{high}</span>
        <span style="color:var(--muted);font-size:12px"> high</span><br>
        <span style="color:var(--muted);font-size:13px;margin-top:4px;display:block">{total - critical - high} medium / low</span>
      </div>
    </div>
  </div>
</div>"""

def _render_agents(state):
    scores = state.get("scores", {})
    rows = "".join(
        _agent_card(r, state.get(f"{r}_review",""), scores.get(r,0))
        for r in ["security","performance","logic","style"]
    )
    return f"""<div class="cra-panel">
  <div class="cra-panel-label">Agent reports — parallel review</div>
  <div class="cra-timeline">{rows}</div>
</div>"""

def _render_issues(issues):
    return f"""<div class="cra-panel">
  <div class="cra-panel-label">All findings</div>
  {_issue_list(issues)}
</div>"""

def _render_history():
    sessions = engine.list_sessions()
    if not sessions:
        return """<div class="cra-panel">
  <div class="cra-panel-label">Recent sessions</div>
  <div style="color:var(--muted);font-size:13px;text-align:center;padding:20px">No sessions yet.</div>
</div>"""
    rows = []
    for s in sessions:
        color = _score_color(s.get("score", 0))
        rows.append(f"""<div class="cra-session">
  <div class="cra-session-score" style="color:{color}">{s.get('score',0):.1f}</div>
  <div class="cra-session-lang">{_esc(s.get('language','?')).upper()}</div>
  <div class="cra-session-desc">{_esc(s.get('summary',''))[:90]}…</div>
</div>""")
    return f"""<div class="cra-panel">
  <div class="cra-panel-label">Recent sessions</div>
  <div class="cra-history">{"".join(rows)}</div>
</div>"""


# ── Review handler ─────────────────────────────────────────────────────────────

def run_review(code, filename):
    if not code.strip():
        err = "<div class='cra-panel' style='color:var(--red);text-align:center;padding:24px'>Please paste some code to review.</div>"
        return gr.update(value=err), gr.update(value=""), gr.update(value=""), gr.update(value=""), gr.update(value=_render_history())

    result     = engine.review(code, filename)
    scores     = result.get("scores", {})
    overall    = result.get("overall_score", 0.0)
    top_issues = result.get("top_issues", [])
    summary    = result.get("summary", "")
    lang       = result.get("language", "unknown")
    session_id = result.get("session_id", "")

    return (
        gr.update(value=_render_score_panel(overall, scores, lang, session_id, top_issues)),
        gr.update(value=_render_summary(summary, overall, top_issues)),
        gr.update(value=_render_agents(result)),
        gr.update(value=_render_issues(top_issues)),
        gr.update(value=_render_history()),
    )


# ── Build UI ───────────────────────────────────────────────────────────────────

def build_ui():
    with gr.Blocks(css=APP_CSS, title="Code Review Arena") as demo:
        with gr.Column(elem_classes="cra-shell"):
            gr.HTML(HERO_HTML)

            with gr.Row(equal_height=False):
                with gr.Column(scale=5, min_width=340):
                    code_input = gr.Code(
                        label="Paste your code",
                        language="python",
                        value=SAMPLE,
                        lines=26,
                    )
                    with gr.Row():
                        filename_input = gr.Textbox(
                            label="Filename (optional — helps language detection)",
                            placeholder="e.g. utils.py, main.go, App.java",
                            scale=3,
                        )
                        review_btn = gr.Button("Run Arena Review  ▶", variant="primary", scale=2)

                with gr.Column(scale=3, min_width=260):
                    score_panel = gr.HTML(value=_render_empty_score())

            summary_panel = gr.HTML(value="")

            with gr.Row(equal_height=False):
                with gr.Column(scale=1):
                    issues_panel = gr.HTML(value="")
                with gr.Column(scale=1):
                    agents_panel = gr.HTML(value="")

            history_panel = gr.HTML(value=_render_history())
            refresh_btn = gr.Button("↻  Refresh history", size="sm")

        review_btn.click(
            fn=run_review,
            inputs=[code_input, filename_input],
            outputs=[score_panel, summary_panel, agents_panel, issues_panel, history_panel],
        )
        refresh_btn.click(fn=_render_history, outputs=[history_panel])

    return demo


if __name__ == "__main__":
    build_ui().launch(server_name="0.0.0.0", server_port=7860, show_error=True)