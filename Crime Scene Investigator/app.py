"""
Crime Scene Investigator — Gradio UI
Noir detective aesthetic: dark slate, amber accents, red verdict flashes.
"""
import html
import re
from typing import Any

import gradio as gr
from graph import CSIEngine

from ui.css import APP_CSS
from ui.html import HERO_HTML, EMPTY_HTML

engine = CSIEngine()

SAMPLE_BRIEF = """Marcus Webb, 42, was found dead in his home office at 11:30 PM on a Thursday.
The victim was discovered by his business partner, Daniel Cho, who claims he came to discuss
an urgent contract dispute. The time of death is estimated between 9:00 PM and 11:00 PM.
Marcus had recently changed his will, removing his wife Elena from the primary beneficiary
position and replacing her with a charity. Elena was reportedly furious and the couple had
a public argument at a restaurant three days prior. A neighbour heard shouting from the
house around 9:30 PM. The study window was broken from the outside."""

SAMPLE_EVIDENCE = """Victim's whisky glass — wiped clean of fingerprints, unusual for a home setting
Elena Webb's car spotted by CCTV two streets away at 9:15 PM
Broken window glass found inside the room, suggesting staged break-in
Victim's laptop open to a legal document revoking Elena's inheritance
Neighbour testimony: heard a woman's voice shouting at 9:30 PM
Elena claims she was at her sister's house from 8 PM — sister confirms alibi
Muddy footprints outside the broken window — size 8 women's shoe
Elena's shoe size is 7. The sister's shoe size is 8
No forced entry at the front door — victim likely knew the attacker
Life insurance policy worth £2.4 million names Elena as sole beneficiary"""


def _esc(v: Any) -> str:
    return html.escape(str(v or ""))

def _verdict_color(verdict: str, confidence: float) -> str:
    v = verdict.lower()
    if "guilty" in v and "not" not in v:
        return "var(--red-hi)" if confidence >= 75 else "var(--amber)"
    if "not guilty" in v:
        return "var(--cyan)"
    return "var(--muted)"

def _tag_evidence(evidence_list: str) -> list[tuple[str,str]]:
    tagged = []
    for line in evidence_list.splitlines():
        line = line.strip().lstrip("-•* ")
        if not line:
            continue
        lo = line.lower()
        if any(w in lo for w in ["witness", "saw", "heard", "testimony", "claims", "confirms"]):
            tag = "WITNESS"
        elif any(w in lo for w in ["fingerprint","dna","blood","glass","weapon","footprint","shoe","mud"]):
            tag = "PHYSICAL"
        elif any(w in lo for w in ["cctv","phone","laptop","email","digital","record","camera"]):
            tag = "DIGITAL"
        else:
            tag = "CIRCUMSTANTIAL"
        tagged.append((tag, line))
    return tagged

def _md_brief(text: str) -> str:
    """Light markdown to HTML for agent report text."""
    lines, chunks, li = str(text or "").splitlines(), [], []
    def flush():
        if li:
            chunks.append("<ul style='margin:6px 0;padding-left:18px'>" + "".join(li) + "</ul>")
            li.clear()
    def inline(t):
        t = html.escape(t)
        t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
        return t
    for raw in lines:
        l = raw.strip()
        if not l: flush(); continue
        if l.startswith(("- ","* ")): li.append(f"<li style='margin-bottom:4px'>{inline(l[2:])}</li>"); continue
        if l.isupper() and l.endswith(":"): flush(); chunks.append(f"<div style='font-size:10px;text-transform:uppercase;letter-spacing:.16em;color:var(--amber);margin:10px 0 5px;font-weight:700'>{_esc(l)}</div>"); continue
        flush()
        chunks.append(f"<p style='margin:0 0 7px'>{inline(l)}</p>")
    flush()
    return "".join(chunks)


# ── render functions ───────────────────────────────────────────────────────────

def _render_verdict(result: dict) -> str:
    verdict     = result.get("verdict", "")
    confidence  = float(result.get("confidence", 0))
    final_sum   = result.get("final_summary", "")
    color       = _verdict_color(verdict, confidence)
    pct         = int(confidence)
    label       = verdict.upper().replace("_", " ")

    key_ev  = result.get("key_evidence", [])
    doubts  = result.get("reasonable_doubts", [])

    key_html = "".join(f'<div class="csi-key-item">{_esc(e)}</div>' for e in key_ev) or "<div style='color:var(--muted);font-size:13px'>None identified.</div>"
    dbt_html = "".join(f'<div class="csi-doubt">{_esc(d)}</div>' for d in doubts) or "<div style='color:var(--muted);font-size:13px'>No doubts raised.</div>"

    return f"""
<div class="csi-panel">
  <div class="csi-verdict-wrap">
    <div class="csi-score-ring" style="width:130px;height:130px;border-radius:50%;border:3px solid {color};display:inline-flex;align-items:center;justify-content:center;font-size:40px;font-weight:900;font-family:'Inter',sans-serif;color:{color}">{pct}%</div>
    <div class="csi-verdict-label" style="color:{color};margin-top:10px">{label}</div>
    <div style="font-size:11px;color:var(--muted);font-family:'Inter',sans-serif">Judge confidence</div>
    <div class="csi-confidence-track">
      <div class="csi-confidence-fill" style="width:{pct}%;background:{color}"></div>
    </div>
  </div>

  <div style="margin-bottom:18px">
    <div class="csi-summary-quote">{_esc(final_sum)}</div>
  </div>

  <div class="csi-panel-label">Key incriminating evidence</div>
  <div class="csi-key-evidence" style="margin-bottom:18px">{key_html}</div>

  <div class="csi-panel-label">Reasonable doubts</div>
  <div class="csi-doubt-list">{dbt_html}</div>
</div>"""


def _render_evidence_board(evidence_list: str) -> str:
    tagged = _tag_evidence(evidence_list)
    if not tagged:
        return EMPTY_HTML
    tag_cls = {"PHYSICAL":"tag-physical","WITNESS":"tag-witness",
               "DIGITAL":"tag-digital","CIRCUMSTANTIAL":"tag-circumstantial"}
    items = []
    for tag, text in tagged:
        cls = tag_cls.get(tag, "tag-circumstantial")
        items.append(f"""
<div class="csi-evidence-item">
  <span class="csi-evidence-tag {cls}">{tag}</span>
  <span class="csi-evidence-text">{_esc(text)}</span>
</div>""")
    return f"""
<div class="csi-panel">
  <div class="csi-panel-label">Evidence board</div>
  <div class="csi-evidence-board">{"".join(items)}</div>
</div>"""


def _render_debate(result: dict) -> str:
    pros = _md_brief(result.get("prosecution_argument", ""))
    defs = _md_brief(result.get("defense_argument", ""))
    return f"""
<div class="csi-debate-grid">
  <div class="csi-arg-card arg-prosecution">
    <div class="csi-arg-header header-prosecution">Prosecution</div>
    {pros}
  </div>
  <div class="csi-arg-card arg-defense">
    <div class="csi-arg-header header-defense">Defense</div>
    {defs}
  </div>
</div>"""


def _render_forensics(result: dict) -> str:
    text = result.get("forensics_report", "")
    return f"""
<div class="csi-panel">
  <div class="csi-panel-label">Forensic science report</div>
  <div class="csi-forensics">{_esc(text)}</div>
</div>"""


def _render_history() -> str:
    cases = engine.list_cases()
    if not cases:
        return f"""
<div class="csi-panel">
  <div class="csi-panel-label">Case archive</div>
  <div style="color:var(--muted);font-size:13px;font-family:'Inter',sans-serif;text-align:center;padding:16px">No cases filed yet.</div>
</div>"""
    rows = []
    for c in cases:
        v = c.get("verdict", "unknown")
        conf = c.get("confidence", 0)
        color = _verdict_color(v, conf)
        rows.append(f"""
<div class="csi-case-row">
  <span class="csi-case-verdict" style="color:{color}">{_esc(v.upper()[:14])}</span>
  <span class="csi-case-title">{_esc(c.get('case_title','Unknown'))}</span>
  <span class="csi-case-conf">{int(conf)}%</span>
</div>""")
    return f"""
<div class="csi-panel">
  <div class="csi-panel-label">Case archive</div>
  <div class="csi-history">{"".join(rows)}</div>
</div>"""


# ── run handler ────────────────────────────────────────────────────────────────

def run_investigation(title: str, brief: str, evidence: str):
    empty = gr.update(value="")
    if not brief.strip() or not evidence.strip():
        err = "<div class='csi-panel' style='color:var(--red-hi);text-align:center;padding:24px;font-family:Inter,sans-serif'>Provide both a case brief and evidence list.</div>"
        return gr.update(value=err), empty, empty, empty, gr.update(value=_render_history())

    result = engine.investigate(
        case_title    = title.strip() or "Untitled Case",
        case_brief    = brief.strip(),
        evidence_list = evidence.strip(),
    )

    return (
        gr.update(value=_render_verdict(result)),
        gr.update(value=_render_evidence_board(evidence)),
        gr.update(value=_render_debate(result)),
        gr.update(value=_render_forensics(result)),
        gr.update(value=_render_history()),
    )


# ── load handler ──────────────────────────────────────────────────────────────

def _case_choices() -> list[str]:
    """Return list of 'ID — Title' strings for the dropdown."""
    cases = engine.list_cases()
    return [f"{c['case_id']} — {c.get('case_title','Untitled')}" for c in cases] or ["No saved cases"]


def load_saved_case(choice: str):
    """Load all panels from a persisted case — zero agent calls."""
    empty = gr.update(value="")
    if not choice or "—" not in choice:
        return empty, empty, empty, empty, empty, empty, empty, gr.update(value=_render_history())

    case_id = choice.split("—")[0].strip()
    result  = engine.load_case(case_id)

    if not result:
        err = "<div class='csi-panel' style='color:var(--red-hi);padding:20px;font-family:Inter,sans-serif;text-align:center'>Case file not found.</div>"
        return empty, empty, empty, gr.update(value=err), empty, empty, empty, gr.update(value=_render_history())

    evidence = result.get("evidence_list", "")
    loaded_banner = f"""<div class='csi-loaded-banner'>
      Case #{case_id} loaded from archive — no agents re-run
    </div>"""

    return (
        gr.update(value=result.get("case_title", "Untitled Case")),
        gr.update(value=result.get("case_brief", "")),
        gr.update(value=result.get("evidence_list", "")),
        gr.update(value=loaded_banner + _render_verdict(result)),
        gr.update(value=_render_evidence_board(result.get("evidence_list", ""))),
        gr.update(value=_render_debate(result)),
        gr.update(value=_render_forensics(result)),
        gr.update(value=_render_history()),
    )


# ── build UI ───────────────────────────────────────────────────────────────────

def build_ui():
    with gr.Blocks(css=APP_CSS, title="Crime Scene Investigator") as demo:
        with gr.Column(elem_classes="csi-shell"):
            gr.HTML(HERO_HTML)

            # ── Load saved case ──
            with gr.Column(elem_classes="csi-load-panel"):
                gr.HTML("<div class='csi-load-badge'>Case archive — load without re-running</div>")
                case_selector = gr.Dropdown(
                    label="Select a saved case",
                    choices=_case_choices(),
                    value=None,
                    interactive=True,
                )
                with gr.Row():
                    refresh_dropdown_btn = gr.Button("Refresh list", variant="secondary", scale=1)
                    load_btn = gr.Button("Load case  ▶", variant="primary", scale=1)

            # ── Input section ──
            with gr.Row(equal_height=False):
                with gr.Column(scale=3):
                    case_title = gr.Textbox(
                        label="Case title",
                        placeholder="e.g. The Webb Manor Homicide",
                        value="The Webb Manor Homicide",
                    )
                    case_brief = gr.Textbox(
                        label="Case brief",
                        placeholder="Describe the crime, scene, suspects, timeline...",
                        value=SAMPLE_BRIEF,
                        lines=8,
                    )
                    evidence_input = gr.Textbox(
                        label="Evidence list — one item per line",
                        placeholder="Each line is one piece of evidence...",
                        value=SAMPLE_EVIDENCE,
                        lines=12,
                    )
                    investigate_btn = gr.Button(
                        "Open the Investigation  ▶",
                        variant="primary",
                    )

                with gr.Column(scale=2):
                    verdict_panel = gr.HTML(value=EMPTY_HTML)

            # ── Evidence board ──
            evidence_panel = gr.HTML(value="")

            # ── Debate + Forensics ──
            with gr.Row(equal_height=False):
                with gr.Column(scale=3):
                    debate_panel = gr.HTML(value="")
                with gr.Column(scale=2):
                    forensics_panel = gr.HTML(value="")

            # ── Case archive ──
            history_panel = gr.HTML(value=_render_history())
            gr.Button("Refresh archive", size="sm").click(
                fn=_render_history, outputs=[history_panel]
            )

        investigate_btn.click(
            fn=run_investigation,
            inputs=[case_title, case_brief, evidence_input],
            outputs=[verdict_panel, evidence_panel, debate_panel,
                     forensics_panel, history_panel],
        )

        load_btn.click(
            fn=load_saved_case,
            inputs=[case_selector],
            outputs=[case_title, case_brief, evidence_input,
                     verdict_panel, evidence_panel, debate_panel,
                     forensics_panel, history_panel],
        )

        refresh_dropdown_btn.click(
            fn=_case_choices,
            outputs=[case_selector],
        )

    return demo


if __name__ == "__main__":
    build_ui().launch(server_name="0.0.0.0", server_port=7862, show_error=True)