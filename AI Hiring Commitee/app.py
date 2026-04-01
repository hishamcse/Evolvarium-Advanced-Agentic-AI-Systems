"""
AI Hiring Committee — Gradio UI
Corporate committee room aesthetic: clean, clinical, dramatic scorecard reveal.
"""
import html
from typing import Any

import gradio as gr
import io
from pathlib import Path
from graph import HiringEngine

import pypdf
from docx import Document

from ui.css import APP_CSS
from ui.html import HERO_HTML, EMPTY_HTML

def _extract_text_from_file(file_path: str) -> str:
    if not file_path:
        return ""
    ext = Path(file_path).suffix.lower()
    try:
        if ext == ".pdf":
            reader = pypdf.PdfReader(file_path)
            return "\n".join(p.extract_text() or "" for p in reader.pages).strip()
        elif ext in (".docx", ".doc"):
            doc = Document(file_path)
            return "\n".join(p.text for p in doc.paragraphs if p.text.strip())
        else:
            with open(file_path, "r", errors="ignore") as f:
                return f.read()
    except Exception as e:
        return f"[Error reading file: {e}]"


def _handle_cv_upload(file_obj):
    if file_obj is None:
        return gr.update()
    path = file_obj if isinstance(file_obj, str) else file_obj.name
    text = _extract_text_from_file(path)
    return gr.update(value=text)

engine = HiringEngine()


SAMPLE_CV = """Sarah Chen
Senior Software Engineer

EXPERIENCE
Staff Engineer — Stripe (2021–Present)
Led payment infrastructure reliability initiative, reducing P99 latency by 40%.
Managed a team of 6 engineers across 3 time zones.
Designed and shipped Stripe's internal rate-limiting framework now used by 200+ services.

Senior Engineer — Airbnb (2018–2021)
Built real-time pricing engine handling 2M requests/day.
Migrated legacy monolith to microservices — reduced deploy time from 4 hours to 12 minutes.
Mentored 4 junior engineers, 2 of whom were promoted within 18 months.

Software Engineer — StartupXYZ (2015–2018)
Full-stack engineer on a 3-person founding team. Built initial product from scratch.
Grew platform from 0 to 50,000 users.

SKILLS
Python, Go, Kubernetes, Postgres, Redis, Kafka, React, distributed systems,
system design, technical leadership, hiring

EDUCATION
BS Computer Science — UC Berkeley (2015)"""

SAMPLE_JOB = """Staff Software Engineer — Platform Infrastructure

We are looking for a Staff Engineer to own our core platform infrastructure.

Requirements:
- 8+ years of software engineering experience
- Deep expertise in distributed systems and reliability engineering
- Experience leading engineering teams or technical initiatives
- Strong proficiency in Go or Python
- Experience with Kubernetes and cloud infrastructure (AWS/GCP)
- Track record of shipping high-impact technical projects
- Excellent communication skills — you will work closely with product and leadership

Nice to have:
- Experience at high-growth companies
- Open source contributions
- Background in fintech or payments"""

CURRENT_SESSION_ID = None


# ── helpers ────────────────────────────────────────────────────────────────────

def _esc(v: Any) -> str:
    return html.escape(str(v or ""))

def _decision_color(decision: str) -> str:
    d = decision.upper()
    if "STRONG HIRE" in d:   return "var(--green)"
    if d == "HIRE":          return "var(--cyan)"
    if "NO HIRE" in d:       return "var(--red)"
    return "var(--amber)"

def _verdict_color(verdict: str) -> str:
    v = verdict.upper()
    if "STRONG HIRE" in v:    return ("rgba(64,176,96,0.15)",  "rgba(64,176,96,0.35)",  "var(--green)")
    if "LEAN HIRE" in v:      return ("rgba(64,192,208,0.12)", "rgba(64,192,208,0.30)", "var(--cyan)")
    if "HIRE" in v and "NO" not in v:
                              return ("rgba(64,176,96,0.10)",  "rgba(64,176,96,0.28)",  "var(--green)")
    if "LEAN NO" in v:        return ("rgba(208,160,48,0.12)", "rgba(208,160,48,0.28)", "var(--amber)")
    return ("rgba(208,64,64,0.12)", "rgba(208,64,64,0.28)", "var(--red)")

def _list_items(items: list, cls: str) -> str:
    if not items:
        return f"<div style='color:var(--muted);font-size:12px'>None identified.</div>"
    return "".join(f'<div class="hc-list-item {cls}">{_esc(i)}</div>' for i in items)

def _eval_card(key: str, display: str, result: dict, name_cls: str, card_cls: str) -> str:
    score   = result.get("score", 0)
    verdict = result.get("verdict", "")
    bg, border, color = _verdict_color(verdict)
    pct = int((score / 10) * 100)
    note = "(higher = more red flags)" if key == "advocate" else ""

    strengths = _list_items(result.get("strengths", []), "item-strength")
    concerns  = _list_items(result.get("concerns",  []), "item-concern")
    qs        = _list_items(result.get("interview_qs", []), "item-q")

    return f"""
<div class="hc-eval-card {card_cls}">
  <div class="hc-eval-header">
    <div>
      <div class="hc-eval-name {name_cls}">{display}</div>
      <div style="font-size:11px;color:var(--muted);margin-top:2px">{note}</div>
    </div>
    <div style="text-align:right">
      <div class="hc-eval-score" style="color:{color}">{score:.1f}</div>
      <div class="hc-eval-verdict" style="background:{bg};border:1px solid {border};color:{color}">{verdict}</div>
    </div>
  </div>
  <div class="hc-score-track"><div class="hc-score-fill" style="width:{pct}%;background:{color}"></div></div>
  <div style="font-size:12px;color:var(--muted);font-style:italic;margin:10px 0 8px">{_esc(result.get('reasoning',''))}</div>

  <div style="font-size:9px;text-transform:uppercase;letter-spacing:.14em;color:var(--green);margin:10px 0 5px;font-weight:700">Strengths</div>
  <div class="hc-list">{strengths}</div>

  <div style="font-size:9px;text-transform:uppercase;letter-spacing:.14em;color:var(--red);margin:10px 0 5px;font-weight:700">Concerns</div>
  <div class="hc-list">{concerns}</div>

  <div style="font-size:9px;text-transform:uppercase;letter-spacing:.14em;color:var(--amber);margin:10px 0 5px;font-weight:700">Would ask</div>
  <div class="hc-list">{qs}</div>
</div>"""


def _render_decision(result: dict) -> str:
    score    = result.get("overall_score", 0)
    decision = result.get("decision", "")
    color    = _decision_color(decision)
    pct      = int((score / 10) * 100)
    name     = result.get("candidate_name", "Candidate")
    role     = result.get("role_title", "")

    agreements    = _list_items(result.get("key_agreements",    []), "item-agree")
    disagreements = _list_items(result.get("key_disagreements", []), "item-disagree")
    flags         = _list_items(result.get("red_flags",         []), "item-flag")
    top_qs        = _list_items(result.get("top_interview_qs",  []), "item-q")

    return f"""
<div class="hc-panel">
  <div class="hc-panel-label">Committee decision — {_esc(name)} · {_esc(role)}</div>

  <div class="hc-decision" style="background:rgba(255,255,255,0.02);border:1px solid {color}33;margin-bottom:18px">
    <div class="hc-decision-label">Final verdict</div>
    <div class="hc-decision-verdict" style="color:{color}">{_esc(decision)}</div>
    <div class="hc-decision-score" style="color:{color}">{score:.1f}<span style="font-size:18px;color:var(--muted)">/10</span></div>
    <div class="hc-score-label">Weighted committee score</div>
    <div class="hc-score-track" style="margin-top:12px">
      <div class="hc-score-fill" style="width:{pct}%;background:{color}"></div>
    </div>
  </div>

  <div style="font-size:13px;color:var(--text);line-height:1.65;margin-bottom:18px;padding:14px 16px;border-radius:12px;background:rgba(255,255,255,0.03);border-left:3px solid {color}">
    {_esc(result.get('chair_reasoning',''))}
  </div>

  <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:18px">
    <div>
      <div style="font-size:9px;text-transform:uppercase;letter-spacing:.14em;color:var(--blue);margin-bottom:8px;font-weight:700">Where the committee agrees</div>
      <div class="hc-list">{agreements}</div>
    </div>
    <div>
      <div style="font-size:9px;text-transform:uppercase;letter-spacing:.14em;color:var(--purple);margin-bottom:8px;font-weight:700">Points of disagreement</div>
      <div class="hc-list">{disagreements}</div>
    </div>
  </div>

  <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px">
    <div>
      <div style="font-size:9px;text-transform:uppercase;letter-spacing:.14em;color:var(--red);margin-bottom:8px;font-weight:700">Red flags</div>
      <div class="hc-list">{flags}</div>
    </div>
    <div>
      <div style="font-size:9px;text-transform:uppercase;letter-spacing:.14em;color:var(--amber);margin-bottom:8px;font-weight:700">Top interview questions</div>
      <div class="hc-list">{top_qs}</div>
    </div>
  </div>
</div>"""


def _render_scorecards(result: dict) -> str:
    cards = [
        _eval_card("technical", "Technical Lead",   result.get("technical", {}), "name-technical", "eval-technical"),
        _eval_card("manager",   "Hiring Manager",   result.get("manager",   {}), "name-manager",   "eval-manager"),
        _eval_card("culture",   "Culture Screener", result.get("culture",   {}), "name-culture",   "eval-culture"),
        _eval_card("advocate",  "Devil's Advocate", result.get("advocate",  {}), "name-advocate",  "eval-advocate"),
    ]
    return f"""
<div class="hc-panel">
  <div class="hc-panel-label">Individual scorecards — blind evaluation revealed</div>
  <div class="hc-eval-grid">{"".join(cards)}</div>
</div>"""


def _render_archive() -> str:
    sessions = engine.list_sessions()
    if not sessions:
        return """<div class="hc-panel"><div class="hc-panel-label">Session archive</div>
<div style="color:var(--muted);font-size:13px;text-align:center;padding:16px">No sessions yet.</div></div>"""
    rows = []
    for s in sessions:
        color = _decision_color(s.get("decision", ""))
        rows.append(f"""
<div class="hc-session-row">
  <div>
    <div class="hc-session-name">{_esc(s.get('candidate_name','Unknown'))}</div>
    <div class="hc-session-role">{_esc(s.get('role_title',''))}</div>
  </div>
  <div class="hc-session-decision" style="background:{color}18;border:1px solid {color}44;color:{color}">
    {_esc(s.get('decision',''))}
  </div>
  <div style="font-weight:700;color:{color};font-size:14px">{s.get('overall_score',0):.1f}</div>
</div>""")
    return f"""<div class="hc-panel"><div class="hc-panel-label">Session archive</div>{"".join(rows)}</div>"""


def _session_choices() -> list[str]:
    sessions = engine.list_sessions()
    return [f"{s['session_id']} — {s.get('candidate_name','?')} · {s.get('role_title','?')}"
            for s in sessions] or ["No saved sessions"]


# ── handlers ───────────────────────────────────────────────────────────────────

def run_evaluation(cv_text: str, job_spec: str, role_title: str):
    global CURRENT_SESSION_ID
    empty = gr.update(value="")
    if not cv_text.strip() or not job_spec.strip():
        err = "<div class='hc-panel' style='color:var(--red);padding:24px;text-align:center'>Provide both a CV and a job description.</div>"
        return gr.update(value=err), empty, gr.update(value=_render_archive())

    result = engine.evaluate(
        cv_text    = cv_text.strip(),
        job_spec   = job_spec.strip(),
        role_title = role_title.strip() or "Open Role",
    )

    CURRENT_SESSION_ID = result.get("session_id")

    return (
        gr.update(value=_render_decision(result)),
        gr.update(value=_render_scorecards(result)),
        gr.update(value=_render_archive()),
    )


def load_session(choice: str):
    global CURRENT_SESSION_ID
    empty = gr.update(value="")
    if not choice or "—" not in choice:
        return empty, empty, gr.update(value=_render_archive())

    session_id = choice.split("—")[0].strip()
    CURRENT_SESSION_ID = session_id
    result = engine.load_session(session_id)
    if not result:
        return empty, empty, gr.update(value=_render_archive())

    banner = f"<div style='padding:8px 14px;border-radius:10px;background:rgba(64,176,96,0.10);border:1px solid rgba(64,176,96,0.25);color:var(--green);font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.10em;margin-bottom:14px'>Session {session_id} loaded from archive</div>"

    return (
        gr.update(value=banner + _render_decision(result)),
        gr.update(value=_render_scorecards(result)),
        gr.update(value=_render_archive()),
    )


# ── extension helpers ─────────────────────────────────────────────────────────

_comparison_store: dict = {}


def _generate_summary():
    global CURRENT_SESSION_ID
    sessions = engine.list_sessions()
    if not sessions or not CURRENT_SESSION_ID:
        return gr.update(value="<div class='hc-panel' style='padding:24px;color:var(--muted);text-align:center'>Run an evaluation first.</div>")
    result = engine.load_session(CURRENT_SESSION_ID)
    if not result:
        return gr.update(value="")

    name     = result.get("candidate_name", "Candidate")
    role     = result.get("role_title", "")
    decision = result.get("decision", "")
    score    = float(result.get("overall_score", 0))
    color    = _decision_color(decision)
    tech     = result.get("technical", {})
    mgr      = result.get("manager",   {})
    cult     = result.get("culture",   {})
    adv      = result.get("advocate",  {})

    strengths = (tech.get("strengths", [])[:1]
               + mgr.get("strengths",  [])[:1]
               + cult.get("strengths", [])[:1])
    str_html  = "".join(f'<div class="hc-list-item item-strength">{_esc(s)}</div>' for s in strengths)
    flags_html = "".join(f'<div class="hc-list-item item-flag">{_esc(f)}</div>'
                          for f in result.get("red_flags", []))
    qs_html   = "".join(f'<div class="hc-list-item item-q">{_esc(q)}</div>'
                         for q in result.get("top_interview_qs", []))
    reasoning = _esc(result.get("chair_reasoning", ""))

    html = f"""<div class="hc-panel">
  <div class="hc-panel-label">Screening summary</div>
  <div style="border:1px solid {color}44;border-radius:14px;padding:16px 20px;margin-bottom:16px;background:{color}0a">
    <div style="font-size:17px;font-weight:800;color:var(--text)">{_esc(name)}</div>
    <div style="font-size:12px;color:var(--muted);margin:2px 0 10px">{_esc(role)}</div>
    <div style="font-size:24px;font-weight:900;color:{color}">{_esc(decision)}</div>
    <div style="font-size:12px;color:var(--muted)">Score: <strong style="color:{color}">{score:.1f}/10</strong></div>
  </div>
  <div style="display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:10px;margin-bottom:16px">
    <div style="text-align:center;padding:10px;border-radius:10px;background:rgba(64,128,224,0.07);border:1px solid rgba(64,128,224,0.18)">
      <div style="font-size:9px;text-transform:uppercase;letter-spacing:.12em;color:var(--blue);margin-bottom:4px">Technical</div>
      <div style="font-size:20px;font-weight:900;color:var(--blue)">{float(tech.get("score",0)):.1f}</div>
    </div>
    <div style="text-align:center;padding:10px;border-radius:10px;background:rgba(144,96,192,0.07);border:1px solid rgba(144,96,192,0.18)">
      <div style="font-size:9px;text-transform:uppercase;letter-spacing:.12em;color:var(--purple);margin-bottom:4px">Manager</div>
      <div style="font-size:20px;font-weight:900;color:var(--purple)">{float(mgr.get("score",0)):.1f}</div>
    </div>
    <div style="text-align:center;padding:10px;border-radius:10px;background:rgba(64,192,208,0.07);border:1px solid rgba(64,192,208,0.18)">
      <div style="font-size:9px;text-transform:uppercase;letter-spacing:.12em;color:var(--cyan);margin-bottom:4px">Culture</div>
      <div style="font-size:20px;font-weight:900;color:var(--cyan)">{float(cult.get("score",0)):.1f}</div>
    </div>
    <div style="text-align:center;padding:10px;border-radius:10px;background:rgba(208,64,64,0.07);border:1px solid rgba(208,64,64,0.18)">
      <div style="font-size:9px;text-transform:uppercase;letter-spacing:.12em;color:var(--red);margin-bottom:4px">Red flags</div>
      <div style="font-size:20px;font-weight:900;color:var(--red)">{float(adv.get("score",0)):.1f}</div>
    </div>
  </div>
  <div style="font-size:12px;color:var(--text);line-height:1.65;padding:12px 14px;border-radius:10px;background:rgba(255,255,255,0.03);border-left:2px solid {color};margin-bottom:14px">{reasoning}</div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:14px">
    <div>
      <div style="font-size:9px;text-transform:uppercase;letter-spacing:.14em;color:var(--green);margin-bottom:6px;font-weight:700">Strengths</div>
      <div class="hc-list">{str_html}</div>
    </div>
    <div>
      <div style="font-size:9px;text-transform:uppercase;letter-spacing:.14em;color:var(--red);margin-bottom:6px;font-weight:700">Red flags</div>
      <div class="hc-list">{flags_html}</div>
    </div>
  </div>
  <div style="font-size:9px;text-transform:uppercase;letter-spacing:.14em;color:var(--amber);margin-bottom:6px;font-weight:700">Interview questions</div>
  <div class="hc-list">{qs_html}</div>
</div>"""
    return gr.update(value=html)


def _store_candidate(slot: str):
    global CURRENT_SESSION_ID
    sessions = engine.list_sessions()
    if not sessions or not CURRENT_SESSION_ID:
        return gr.update(value="<div style='color:var(--muted);font-size:12px;padding:8px'>No sessions yet. Run an evaluation first.</div>")
    _comparison_store[slot] = engine.load_session(CURRENT_SESSION_ID)
    name = _comparison_store[slot].get("candidate_name", "?")
    return gr.update(value=f"<div style='padding:7px 12px;border-radius:8px;background:rgba(64,176,96,0.10);border:1px solid rgba(64,176,96,0.25);color:var(--green);font-size:11px;font-weight:700'>Slot {slot}: {_esc(name)} stored</div>")


def _run_comparison():
    a = _comparison_store.get("A")
    b = _comparison_store.get("B")
    if not a or not b:
        return gr.update(value="<div class='hc-panel' style='padding:24px;color:var(--muted);text-align:center'>Store two candidates first using the A / B buttons.</div>")

    dims = [
        ("Technical", "technical", "var(--blue)"),
        ("Manager",   "manager",   "var(--purple)"),
        ("Culture",   "culture",   "var(--cyan)"),
        ("Red flags", "advocate",  "var(--red)"),
        ("Overall",   "overall",   "var(--amber)"),
    ]
    rows = []
    for label, key, color in dims:
        if key == "overall":
            sa = float(a.get("overall_score", 0))
            sb = float(b.get("overall_score", 0))
        else:
            sa = float(a.get(key, {}).get("score", 0))
            sb = float(b.get(key, {}).get("score", 0))
        # advocate: lower raw score = fewer red flags = better
        if key == "advocate":
            sa, sb = 10 - sa, 10 - sb

        wa = sa > sb
        wb = sb > sa
        col_a = color if wa else "var(--muted)"
        col_b = color if wb else "var(--muted)"
        arrow = "<span style='font-size:10px;color:var(--green)'>&#9650;</span>"

        rows.append(f"""
<div style="display:grid;grid-template-columns:1fr 80px 1fr;gap:10px;align-items:center;padding:9px 0;border-bottom:1px solid rgba(255,255,255,0.06)">
  <div style="text-align:right">
    <span style="font-size:18px;font-weight:900;color:{col_a}">{sa:.1f}</span>
    {arrow if wa else ""}
  </div>
  <div style="text-align:center;font-size:9px;text-transform:uppercase;letter-spacing:.12em;color:var(--muted);font-weight:700">{label}</div>
  <div>
    {arrow if wb else ""}
    <span style="font-size:18px;font-weight:900;color:{col_b}">{sb:.1f}</span>
  </div>
</div>""")

    col_a = _decision_color(a.get("decision", ""))
    col_b = _decision_color(b.get("decision", ""))
    winner = (a.get("candidate_name", "Candidate A")
              if float(a.get("overall_score", 0)) >= float(b.get("overall_score", 0))
              else b.get("candidate_name", "Candidate B"))

    html = f"""<div class="hc-panel">
  <div class="hc-panel-label">Candidate comparison</div>
  <div style="display:grid;grid-template-columns:1fr 60px 1fr;gap:10px;margin-bottom:14px;text-align:center">
    <div style="padding:12px;border-radius:12px;background:{col_a}0f;border:1px solid {col_a}33">
      <div style="font-size:13px;font-weight:800;color:var(--text)">{_esc(a.get("candidate_name","A"))}</div>
      <div style="font-size:10px;font-weight:700;text-transform:uppercase;color:{col_a}">{_esc(a.get("decision",""))}</div>
    </div>
    <div style="display:flex;align-items:center;justify-content:center;font-size:11px;color:var(--muted);font-weight:700">VS</div>
    <div style="padding:12px;border-radius:12px;background:{col_b}0f;border:1px solid {col_b}33">
      <div style="font-size:13px;font-weight:800;color:var(--text)">{_esc(b.get("candidate_name","B"))}</div>
      <div style="font-size:10px;font-weight:700;text-transform:uppercase;color:{col_b}">{_esc(b.get("decision",""))}</div>
    </div>
  </div>
  {"".join(rows)}
  <div style="margin-top:14px;padding:12px 14px;border-radius:10px;background:rgba(208,160,48,0.07);border:1px solid rgba(208,160,48,0.20);font-size:13px;color:var(--text)">
    Recommend advancing <strong>{_esc(winner)}</strong> to first-round interview.
  </div>
</div>"""
    return gr.update(value=html)


# ── UI ──────────────────────────────────────────────────────────────────────────

def build_ui():
    with gr.Blocks(css=APP_CSS, title="AI Hiring Committee") as demo:
        with gr.Column(elem_classes="hc-shell"):
            gr.HTML(HERO_HTML)

            # ── Load panel ──
            with gr.Column(elem_classes="hc-panel"):
                gr.HTML("<div class='hc-panel-label'>Session archive — load previous evaluation</div>")
                session_selector = gr.Dropdown(
                    label="Select a saved session",
                    choices=_session_choices(),
                    value=None, interactive=True,
                )
                with gr.Row():
                    refresh_btn = gr.Button("Refresh list",  variant="secondary", scale=1)
                    load_btn    = gr.Button("Load session  ▶", variant="primary",   scale=1)

            # ── Input ──
            with gr.Row(equal_height=False):
                with gr.Column(scale=3):
                    role_input = gr.Textbox(
                        label="Role title",
                        placeholder="e.g. Staff Software Engineer — Platform Infrastructure",
                        value="Staff Software Engineer — Platform Infrastructure",
                    )
                    cv_upload = gr.File(
                        label="Upload CV  (PDF / DOCX / TXT)",
                        file_types=[".pdf", ".docx", ".doc", ".txt"],
                        type="filepath",
                    )
                    cv_input = gr.Textbox(
                        label="CV text  (auto-filled on upload, or paste directly)",
                        placeholder="Upload above or paste CV text here...",
                        value=SAMPLE_CV,
                        lines=12,
                    )
                    job_input = gr.Textbox(
                        label="Job description",
                        placeholder="Paste the job description here...",
                        value=SAMPLE_JOB,
                        lines=14,
                    )
                    evaluate_btn = gr.Button("Convene the committee  ▶", variant="primary")

                with gr.Column(scale=2):
                    decision_panel = gr.HTML(value=EMPTY_HTML)

            # ── Scorecards ──
            scorecards_panel = gr.HTML(value="")

            # -- Extensions --
            with gr.Row(equal_height=False):
                with gr.Column(scale=1):
                    gr.HTML("<div class='hc-panel-label' style='padding:4px 0 2px'>Screening summary</div>")
                    summary_btn   = gr.Button("Generate screening summary", variant="secondary")
                    summary_panel = gr.HTML(value="")
                with gr.Column(scale=1):
                    gr.HTML("<div class='hc-panel-label' style='padding:4px 0 2px'>Candidate comparison  (evaluate two, store each, then compare)</div>")
                    with gr.Row():
                        store_a_btn = gr.Button("Store as A", variant="secondary", scale=1)
                        store_b_btn = gr.Button("Store as B", variant="secondary", scale=1)
                        compare_btn = gr.Button("Compare A vs B", variant="primary", scale=1)
                    store_status     = gr.HTML(value="")
                    comparison_panel = gr.HTML(value="")

            # ── Archive ──
            archive_panel = gr.HTML(value=_render_archive())
            gr.Button("Refresh archive", size="sm").click(
                fn=_render_archive, outputs=[archive_panel]
            )

        # ── Events ──
        evaluate_btn.click(
            fn=run_evaluation,
            inputs=[cv_input, job_input, role_input],
            outputs=[decision_panel, scorecards_panel, archive_panel],
        )
        load_btn.click(
            fn=load_session,
            inputs=[session_selector],
            outputs=[decision_panel, scorecards_panel, archive_panel],
        )
        refresh_btn.click(fn=_session_choices, outputs=[session_selector])

        cv_upload.change(fn=_handle_cv_upload, inputs=[cv_upload], outputs=[cv_input])
        summary_btn.click(fn=_generate_summary, inputs=[], outputs=[summary_panel])
        store_a_btn.click(fn=lambda: _store_candidate("A"), inputs=[], outputs=[store_status])
        store_b_btn.click(fn=lambda: _store_candidate("B"), inputs=[], outputs=[store_status])
        compare_btn.click(fn=_run_comparison, inputs=[], outputs=[comparison_panel])

    return demo


if __name__ == "__main__":
    build_ui().launch(server_name="0.0.0.0", server_port=7864, show_error=True)