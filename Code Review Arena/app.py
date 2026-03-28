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

from graph import CodeReviewEngine

engine = CodeReviewEngine()

# ── CSS ────────────────────────────────────────────────────────────────────────

APP_CSS = """
:root {
  --bg:        radial-gradient(ellipse at 20% 0%, #111827 0%, #080d14 55%, #040710 100%);
  --panel:     rgba(10, 16, 30, 0.88);
  --panel-alt: rgba(255, 255, 255, 0.03);
  --border:    rgba(80, 160, 255, 0.16);
  --border-hi: rgba(80, 160, 255, 0.32);
  --text:      #ddeaff;
  --muted:     #6a90bb;
  --cyan:      #5ee8ff;
  --gold:      #ffc940;
  --red:       #ff5a5e;
  --green:     #3ddfa0;
  --purple:    #c4aaff;
  --orange:    #ff9d3d;
}
.gradio-container { background: var(--bg); color: var(--text); font-family: 'Inter', system-ui, sans-serif; }
footer { display: none !important; }

.cra-shell {
  border-radius: 28px;
  border: 1px solid rgba(255,255,255,0.06);
  background: linear-gradient(180deg, rgba(255,255,255,0.025) 0%, rgba(255,255,255,0.008) 100%);
  box-shadow: 0 32px 80px rgba(0,0,0,0.5);
  padding: 0 0 32px;
}
.cra-hero {
  border-radius: 28px 28px 0 0;
  padding: 32px 36px 28px;
  background:
    radial-gradient(ellipse at top right, rgba(94,232,255,0.13) 0%, transparent 45%),
    radial-gradient(ellipse at bottom left, rgba(255,201,64,0.11) 0%, transparent 40%),
    linear-gradient(160deg, rgba(60,120,255,0.15) 0%, rgba(8,13,24,0.92) 100%);
  border-bottom: 1px solid var(--border);
}
.cra-kicker {
  text-transform: uppercase; letter-spacing: 0.20em; font-size: 11px;
  color: var(--cyan); margin-bottom: 10px; font-weight: 600;
}
.cra-title {
  font-size: 34px; font-weight: 800; line-height: 1.08; margin: 0 0 8px;
  background: linear-gradient(90deg, #fff 40%, var(--cyan) 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.cra-subtitle { color: var(--muted); font-size: 14px; margin: 0 0 20px; }
.cra-badge-row { display: flex; flex-wrap: wrap; gap: 8px; }
.cra-badge {
  padding: 5px 13px; border-radius: 999px; font-size: 12px; font-weight: 500;
  background: rgba(94,232,255,0.08); border: 1px solid rgba(94,232,255,0.20); color: var(--cyan);
}
.cra-panel {
  background: var(--panel); border: 1px solid var(--border);
  border-radius: 22px; padding: 20px 22px; box-shadow: 0 12px 40px rgba(0,0,0,0.28);
}
.cra-panel-label {
  text-transform: uppercase; letter-spacing: 0.15em; font-size: 10px;
  font-weight: 700; color: var(--muted); margin-bottom: 14px;
}
.cra-score-wrap { text-align: center; padding: 8px 0 16px; }
.cra-score-ring {
  display: inline-flex; align-items: center; justify-content: center;
  width: 120px; height: 120px; border-radius: 50%; border: 3px solid var(--gold);
  background: radial-gradient(circle, rgba(255,201,64,0.10) 0%, transparent 70%);
  font-size: 46px; font-weight: 900; color: var(--gold); margin-bottom: 10px;
}
.cra-score-label { font-size: 11px; color: var(--muted); text-transform: uppercase; letter-spacing: 0.12em; }
.cra-dim { margin-bottom: 14px; }
.cra-dim-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px; }
.cra-dim-name { font-size: 12px; font-weight: 600; color: var(--text); text-transform: uppercase; letter-spacing: 0.10em; }
.cra-dim-score { font-size: 18px; font-weight: 800; }
.cra-dim-track { width: 100%; height: 9px; border-radius: 999px; background: rgba(255,255,255,0.07); overflow: hidden; }
.cra-dim-fill { height: 100%; border-radius: 999px; }
.cra-chips { display: flex; flex-wrap: wrap; gap: 7px; margin: 10px 0 6px; }
.cra-chip { padding: 5px 13px; border-radius: 999px; font-size: 12px; font-weight: 700; letter-spacing: 0.04em; }
.chip-critical { background: rgba(255,90,94,0.16);  color: var(--red);    border: 1px solid rgba(255,90,94,0.35); }
.chip-high     { background: rgba(255,157,61,0.15); color: var(--orange); border: 1px solid rgba(255,157,61,0.35); }
.chip-medium   { background: rgba(94,232,255,0.12); color: var(--cyan);   border: 1px solid rgba(94,232,255,0.28); }
.chip-low      { background: rgba(61,223,160,0.12); color: var(--green);  border: 1px solid rgba(61,223,160,0.28); }
.cra-issue-list { display: grid; gap: 8px; }
.cra-issue {
  display: grid; grid-template-columns: auto auto 1fr; gap: 10px;
  align-items: start; padding: 11px 14px; border-radius: 14px;
  background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.07);
}
.cra-issue-role { font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.12em; color: var(--muted); padding-top: 2px; }
.cra-issue-desc { font-size: 13px; color: var(--text); line-height: 1.45; }
.cra-timeline { display: grid; gap: 10px; }
.cra-timeline-row { display: grid; grid-template-columns: 110px 1fr; gap: 12px; align-items: start; }
.cra-timeline-actor {
  border-radius: 16px; padding: 12px 10px; text-align: center;
  font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.10em;
}
.actor-security    { background: rgba(255,90,94,0.12);  border: 1px solid rgba(255,90,94,0.25);  color: var(--red); }
.actor-performance { background: rgba(255,157,61,0.12); border: 1px solid rgba(255,157,61,0.25); color: var(--orange); }
.actor-logic       { background: rgba(94,232,255,0.10); border: 1px solid rgba(94,232,255,0.22); color: var(--cyan); }
.actor-style       { background: rgba(196,170,255,0.12);border: 1px solid rgba(196,170,255,0.25);color: var(--purple); }
.cra-timeline-card {
  border-radius: 16px; padding: 14px 16px;
  background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08);
  font-size: 13px; line-height: 1.55; color: var(--text);
}
.cra-timeline-card strong { color: var(--cyan); }
.cra-timeline-card code {
  background: rgba(94,232,255,0.10); border: 1px solid rgba(94,232,255,0.20);
  border-radius: 5px; padding: 1px 5px; font-size: 12px; color: var(--cyan);
}
.cra-timeline-score { font-size: 22px; font-weight: 800; text-align: center; margin-top: 4px; }
.cra-summary-hero {
  border-radius: 20px; padding: 20px 22px;
  background: linear-gradient(135deg, rgba(255,201,64,0.12), rgba(94,232,255,0.07));
  border: 1px solid rgba(255,201,64,0.20); font-size: 14px; line-height: 1.65; color: var(--text);
}
.cra-history { display: grid; gap: 8px; }
.cra-session {
  display: grid; grid-template-columns: 48px 52px 1fr; gap: 12px;
  align-items: center; padding: 10px 14px; border-radius: 14px;
  background: rgba(255,255,255,0.03); border: 1px solid var(--border);
  cursor: pointer; transition: background 0.15s, border-color 0.15s;
}
.cra-session:hover { background: rgba(80,160,255,0.07); border-color: var(--border-hi); }
.cra-session-score { font-size: 20px; font-weight: 800; text-align: center; }
.cra-session-lang  { font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.14em; color: var(--cyan); font-family: monospace; }
.cra-session-desc  { font-size: 12px; color: var(--muted); }
.cra-plan-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; }
.cra-stat-card { border-radius: 18px; padding: 16px 18px; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); }
.cra-stat-label { text-transform: uppercase; letter-spacing: 0.13em; font-size: 10px; color: var(--muted); margin-bottom: 8px; }
.cra-stat-value { font-size: 14px; line-height: 1.5; }
.gr-button-primary {
  background: linear-gradient(135deg, #1a5cff, #0f3dbf) !important;
  border: none !important; border-radius: 14px !important; font-weight: 700 !important;
  letter-spacing: 0.04em !important; padding: 12px 28px !important;
  box-shadow: 0 4px 20px rgba(26,92,255,0.35) !important;
}
textarea, input[type=text] {
  background: rgba(10,16,30,0.9) !important; border: 1px solid var(--border) !important;
  color: var(--text) !important; border-radius: 14px !important;
}
label > span { color: var(--muted) !important; font-size: 12px !important; }
"""

HERO_HTML = """
<div class="cra-hero">
  <div class="cra-kicker">Multi-Agent System &nbsp;·&nbsp; LangGraph + MCP + Ollama &nbsp;·&nbsp; Parallel fan-out architecture</div>
  <div class="cra-title">Code Review Arena</div>
  <div class="cra-subtitle">4 specialist AI agents review your code simultaneously — security, performance, logic &amp; style — then an aggregator merges findings into one scored report.</div>
  <div class="cra-badge-row">
    <span class="cra-badge">Security</span>
    <span class="cra-badge">Performance</span>
    <span class="cra-badge">Logic</span>
    <span class="cra-badge">Style</span>
    <span class="cra-badge" style="background:rgba(255,201,64,0.10);border-color:rgba(255,201,64,0.25);color:var(--gold)">Parallel fan-out</span>
    <span class="cra-badge" style="background:rgba(196,170,255,0.10);border-color:rgba(196,170,255,0.25);color:var(--purple)">Session memory</span>
    <span class="cra-badge" style="background:rgba(61,223,160,0.10);border-color:rgba(61,223,160,0.25);color:var(--green)">MCP tools</span>
  </div>
</div>
"""

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