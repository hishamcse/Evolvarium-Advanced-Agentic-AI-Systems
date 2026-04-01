"""
Medical Differential Engine — Gradio UI
Clinical dark theme: deep navy, cyan accents, probability heat ramp.
Architecture: Cascading Bayesian Refinement
"""
import html
import json
from typing import Any

import gradio as gr
from graph import DifferentialEngine

from ui.css  import APP_CSS
from ui.html import HERO_HTML, EMPTY_HTML, CASCADE_HTML

engine = DifferentialEngine()

# ── sample cases ───────────────────────────────────────────────────────────────

SAMPLE_CASES = {
    "Chest Pain (Classic)": {
        "age": "58", "sex": "Male",
        "complaint": "Crushing chest pain",
        "symptoms": """Severe crushing chest pain for 45 minutes, 9/10 severity.
Radiates to left arm and jaw. Associated with profuse diaphoresis and nausea.
Dyspnoea at rest. Patient feels a sense of impending doom.
No pleuritic component. Not affected by position or palpation.""",
        "vitals": "BP 158/96 | HR 112 bpm | RR 22 | Temp 37.1°C | SpO2 94% on air",
        "history": """PMH: Hypertension (10 years), Type 2 diabetes, hypercholesterolaemia.
Meds: Metformin 1g BD, Amlodipine 5mg, Atorvastatin 40mg, Aspirin 75mg.
Allergies: None known.
Social: 30 pack-year smoker, occasional alcohol. Sedentary job.""",
        "exam": """General: Distressed, diaphoretic, pale. Clutching chest.
Cardiovascular: Tachycardic, regular rhythm, no murmurs. JVP not elevated.
Respiratory: Bilateral fine crackles at bases. No wheeze.
Abdomen: Soft, non-tender.
Neuro: GCS 15. No focal deficits.""",
    },
    "Headache (Thunderclap)": {
        "age": "34", "sex": "Female",
        "complaint": "Worst headache of life — thunderclap onset",
        "symptoms": """Sudden-onset severe headache, described as a bat hitting the skull.
Reached maximum intensity within seconds. 10/10 severity.
Associated vomiting x3. Neck stiffness developing.
Photophobia and phonophobia. No preceding aura.
No history of similar headaches. Not relieved by paracetamol.""",
        "vitals": "BP 172/104 | HR 88 bpm | RR 16 | Temp 37.6°C | SpO2 99%",
        "history": """PMH: Migraines (last episode 2 years ago, different character).
Oral contraceptive pill. No anticoagulants. No family history of aneurysms.
Social: Non-smoker, social drinker. Works as a teacher.""",
        "exam": """General: Alert but in severe pain. Lying still, avoids movement.
Neuro: GCS 15. Kernig sign positive. Brudzinski sign positive.
Pupils: Equal and reactive 4mm bilaterally.
Fundoscopy: No papilloedema seen. No focal motor or sensory deficit.""",
    },
    "Dyspnoea (Decompensation)": {
        "age": "72", "sex": "Female",
        "complaint": "Progressive breathlessness over 3 days",
        "symptoms": """Gradually worsening dyspnoea over 3 days. Now breathless at rest.
Orthopnoea — needs 3 pillows to sleep. Paroxysmal nocturnal dyspnoea last night.
Bilateral ankle swelling over 2 weeks. Reduced exercise tolerance.
No chest pain. Mild non-productive cough. No haemoptysis. No fever.""",
        "vitals": "BP 148/88 | HR 96 bpm irregular | RR 24 | Temp 36.8°C | SpO2 91% on air",
        "history": """PMH: Atrial fibrillation, hypertension, previous DVT (2018).
Meds: Warfarin 5mg, Bisoprolol 5mg, Ramipril 5mg, Furosemide 40mg.
Recent: Missed 3 days of Furosemide due to urinary incontinence.
Social: Lives alone, independent. Non-smoker.""",
        "exam": """Cardiovascular: Irregularly irregular. JVP elevated 5cm.
Peripheral oedema bilateral to knees. Displaced apex beat.
Respiratory: Bibasal dull to percussion. Fine inspiratory crackles bilaterally.
Abdomen: Hepatomegaly 3cm. No ascites detected.""",
    },
}


# ── helpers ────────────────────────────────────────────────────────────────────

def _esc(v: Any) -> str:
    return html.escape(str(v or ""))

def _prob_color(prob: float) -> str:
    if prob < 10:  return "#4a5568"
    if prob < 25:  return "#667eea"
    if prob < 45:  return "#38b2ac"
    if prob < 65:  return "#d69e2e"
    if prob < 80:  return "#ed8936"
    return "#e53e3e"

def _confidence_label(prob: float) -> str:
    if prob < 5:   return "EXCLUDED"
    if prob < 25:  return "UNLIKELY"
    if prob < 50:  return "POSSIBLE"
    if prob < 70:  return "PROBABLE"
    if prob < 85:  return "LIKELY"
    return "HIGHLY LIKELY"

def _urgency_class(urgency: str) -> str:
    u = urgency.upper()
    if "EMERGENCY" in u: return "urg-emergency"
    if "URGENT" in u:    return "urg-urgent"
    return "urg-routine"


# ── render functions ───────────────────────────────────────────────────────────

def _render_differential(result: dict) -> str:
    differential = result.get("differential", [])
    if not differential:
        return EMPTY_HTML
    ranked = sorted(differential, key=lambda x: x.get("probability", 0), reverse=True)
    cards = []
    for i, dx in enumerate(ranked[:8]):
        prob    = float(dx.get("probability", 0))
        color   = _prob_color(prob)
        conf    = _confidence_label(prob)
        urgency = dx.get("urgency", "ROUTINE")
        urg_cls = _urgency_class(urgency)
        rare    = dx.get("rare_flag", False)
        rank_cls = f"rank-{i+1}" if i < 3 else ""
        emg_cls  = "emergency-dx" if urgency.upper() == "EMERGENCY" else ""
        sup_tags = "".join(
            f'<span class="mde-feature-tag feat-for">+ {_esc(s[:40])}</span>'
            for s in dx.get("supporting", [])[:3]
        )
        against_tags = "".join(
            f'<span class="mde-feature-tag feat-against">− {_esc(a[:40])}</span>'
            for a in dx.get("against", [])[:2]
        )
        rare_tag = '<span class="mde-rare-flag">ZEBRA</span>' if rare else ""
        key_test = dx.get("key_test", "")
        lr_note  = dx.get("likelihood_ratio_note", "")
        cards.append(f"""
<div class="mde-dx-card {rank_cls} {emg_cls}">
  <div>
    <div class="mde-dx-name">#{i+1} — {_esc(dx.get('name','?'))}</div>
    <div class="mde-dx-icd">{_esc(dx.get('icd_hint',''))}</div>
    <div class="mde-dx-features">{sup_tags}{against_tags}{rare_tag}</div>
    {'<div style="margin-top:8px;font-family:var(--mono);font-size:10px;color:#63b3ed">⌬ KEY TEST: ' + _esc(key_test) + '</div>' if key_test else ''}
    {'<div style="margin-top:4px;font-family:var(--mono);font-size:9px;color:var(--muted)">LR: ' + _esc(lr_note[:80]) + '</div>' if lr_note else ''}
  </div>
  <div class="mde-prob-wrap">
    <div class="mde-prob-pct" style="color:{color}">{prob:.0f}%</div>
    <div class="mde-confidence-label" style="color:{color}">{conf}</div>
    <div class="mde-prob-bar">
      <div class="mde-prob-fill" style="width:{min(prob,100):.0f}%;background:{color}"></div>
    </div>
    <div class="mde-urgency-tag {urg_cls}">{_esc(urgency)}</div>
  </div>
</div>""")
    return f"""
{CASCADE_HTML}
<div class="mde-panel">
  <div class="mde-panel-label">Ranked differential — posterior probabilities</div>
  <div class="mde-dx-grid">{''.join(cards)}</div>
</div>"""


def _render_workup(result: dict) -> str:
    red_flags   = result.get("red_flags", [])
    workup      = result.get("workup_plan", [])
    disposition = result.get("disposition", "ROUTINE")
    disp_color  = {"EMERGENCY": "#fc8181", "URGENT": "#f6ad55", "ROUTINE": "#68d391"}.get(
        disposition.upper(), "#68d391"
    )
    dispo_html = f"""
<div class="mde-disposition {disposition.upper()}">
  <div class="mde-dispo-label" style="color:{disp_color}">Clinical Disposition</div>
  <div class="mde-dispo-value" style="color:{disp_color}">{_esc(disposition.upper())}</div>
</div>"""
    rf_items = "".join(
        f'<div class="mde-redflag"><div class="redflag-dot"></div>{_esc(f)}</div>'
        for f in red_flags
    ) if red_flags else '<div style="font-family:var(--mono);font-size:11px;color:var(--muted)">No emergency flags identified.</div>'

    def _workup_item(line: str) -> str:
        line = str(line)
        lu = line.upper()
        if lu.startswith("STAT"):
            return f'<div class="mde-workup-item"><span class="workup-stat">STAT</span>{_esc(line[4:].lstrip(":— "))}</div>'
        if lu.startswith("URGENT"):
            return f'<div class="mde-workup-item"><span class="workup-urgent">URGENT</span>{_esc(line[6:].lstrip(":— "))}</div>'
        return f'<div class="mde-workup-item"><span class="workup-routine">ROUTINE</span>{_esc(line.lstrip("ROUTINErouting:— "))}</div>'

    workup_html = "".join(_workup_item(w) for w in workup) if workup else \
        '<div style="font-family:var(--mono);font-size:11px;color:var(--muted)">No workup generated.</div>'
    return f"""
<div style="display:grid;gap:14px">
  {dispo_html}
  <div class="mde-panel">
    <div class="mde-panel-label">Red flags — immediate action required</div>
    {rf_items}
  </div>
  <div class="mde-panel">
    <div class="mde-panel-label">Diagnostic workup plan</div>
    {workup_html}
  </div>
</div>"""


def _render_cascade_timeline(result: dict) -> str:
    parsed    = result.get("parsed_features", {})
    prior     = result.get("prior_candidates", [])
    refined   = result.get("refined_candidates", [])
    flags     = result.get("comorbidity_flags", [])
    weighted  = result.get("weighted_candidates", [])
    narrative = result.get("probability_narrative", "")
    summary   = result.get("clinical_summary", "")

    def _top3(cands):
        top = sorted(cands, key=lambda x: x.get("probability", 0), reverse=True)[:3]
        return " → ".join(f"{c['name']} ({c.get('probability',0):.0f}%)" for c in top) or "No candidates"

    flag_html = "".join(
        f'<div class="mde-comorbidity">{_esc(f)}</div>' for f in flags
    ) if flags else '<div style="font-family:var(--mono);font-size:11px;color:var(--muted)">No significant comorbidity interactions.</div>'

    pos_systems = ', '.join(k for k, v in parsed.get('system_review', {}).items() if v == 'pos')
    rows = [
        ("L0 · PARSER",
         f"Onset={_esc(parsed.get('onset','?'))}, red flags={len(parsed.get('red_flag_features',[]))}, "
         f"systems pos: {pos_systems[:60] or 'none'}"),
        ("L1 · PRIOR",       f"Initial distribution: {_top3(prior)}"),
        ("L2 · RARE PROBE",  f"After rare/zebra injection: {_top3(refined)}"),
        ("L3 · COMORBIDITY", f"{len(flags)} interaction flag(s) applied to probabilities"),
        ("L4 · WEIGHER",     f"Final posterior from exam: {_top3(weighted)}"),
        ("L5 · RANKER",      narrative[:200] if narrative else "Final differential locked."),
    ]
    rows_html = "".join(f"""
<div class="mde-cascade-row">
  <div class="mde-cascade-actor">{_esc(actor)}</div>
  <div class="mde-cascade-body">{_esc(body)}</div>
</div>""" for actor, body in rows)

    summary_html = f"""
<div class="mde-panel" style="margin-top:16px">
  <div class="mde-panel-label">Clinical summary</div>
  <div class="mde-summary">{_esc(summary)}</div>
</div>""" if summary else ""

    return f"""
<div class="mde-panel">
  <div class="mde-panel-label">Cascade trace — how probabilities evolved</div>
  <div class="mde-cascade-timeline">{rows_html}</div>
</div>
<div class="mde-panel" style="margin-top:14px">
  <div class="mde-panel-label">Comorbidity & drug interaction flags</div>
  {flag_html}
</div>
{summary_html}"""


def _render_prior_evolution(result: dict) -> str:
    prior    = result.get("prior_candidates", [])
    refined  = result.get("refined_candidates", [])
    weighted = result.get("weighted_candidates", [])
    final    = result.get("differential", [])
    top6     = sorted(final, key=lambda x: x.get("probability", 0), reverse=True)[:6]
    names    = [dx.get("name", "?") for dx in top6]

    def _prob_in(cands, name):
        for c in cands:
            if c.get("name", "").lower() == name.lower():
                return float(c.get("probability", 0))
        return 0.0

    layers = [("Prior", prior), ("+ Rare", refined), ("+ Comorbid", weighted), ("Final", final)]
    rows = []
    for name in names:
        color = _prob_color(_prob_in(final, name))
        bars = "".join(f"""
<div style="display:flex;align-items:center;gap:8px;margin-bottom:3px">
  <div style="font-family:var(--mono);font-size:9px;color:var(--muted);width:72px;text-align:right">{lname}</div>
  <div style="flex:1;height:12px;background:rgba(255,255,255,0.05);border-radius:999px;overflow:hidden">
    <div style="height:100%;width:{min(_prob_in(cands,name),100):.0f}%;background:{color};border-radius:999px"></div>
  </div>
  <div style="font-family:var(--mono);font-size:9px;color:var(--muted);width:36px">{_prob_in(cands,name):.0f}%</div>
</div>""" for lname, cands in layers)
        rows.append(f"""
<div style="margin-bottom:16px">
  <div style="font-family:var(--sans);font-size:12px;font-weight:500;color:{color};margin-bottom:6px">{_esc(name)}</div>
  {bars}
</div>""")
    if not rows:
        return EMPTY_HTML
    return f"""
<div class="mde-panel">
  <div class="mde-panel-label">Probability evolution — top diagnoses across cascade layers</div>
  {''.join(rows)}
</div>"""


def _render_archive() -> str:
    cases = engine.list_cases()
    if not cases:
        return '<div class="mde-empty"><div class="mde-empty-icon">📂</div><div>No saved cases yet.</div></div>'
    items = []
    for c in cases[:12]:
        disp = c.get("disposition", "")
        disp_color = {"EMERGENCY": "#fc8181", "URGENT": "#f6ad55", "ROUTINE": "#68d391"}.get(
            disp.upper(), "#68d391"
        )
        items.append(f"""
<div class="mde-archive-item">
  <div class="mde-archive-cc">{_esc(c.get('chief_complaint','Unknown complaint'))}</div>
  <div class="mde-archive-meta">
    {_esc(c.get('patient_age','?'))}y {_esc(c.get('patient_sex','?'))} ·
    Case {_esc(c.get('case_id','?')[:8])} ·
    <span style="color:{disp_color}">{_esc(disp)}</span>
  </div>
</div>""")
    return "".join(items)


def _case_choices() -> list[str]:
    cases = engine.list_cases()
    return [
        f"{c['case_id']} — {c.get('chief_complaint','?')} ({c.get('patient_age','?')}y {c.get('patient_sex','?')})"
        for c in cases
    ] or ["No saved cases"]


# ── run handler — streaming progress via generator ─────────────────────────────

def run_analysis(patient_age, patient_sex, chief_complaint,
                 symptoms, vitals, history, exam_findings):
    if not chief_complaint.strip():
        yield EMPTY_HTML, EMPTY_HTML, EMPTY_HTML, EMPTY_HTML, _render_archive()
        return

    def _status(step: str, pct: int) -> str:
        filled = "█" * (pct // 10)
        empty  = "░" * (10 - pct // 10)
        return f"""
<div class="mde-panel" style="padding:40px 24px;text-align:center">
  <div style="font-family:var(--mono);font-size:10px;letter-spacing:.18em;color:#63b3ed;
              margin-bottom:20px;text-transform:uppercase">{step}</div>
  <div style="font-family:var(--mono);font-size:22px;color:#63b3ed;
              letter-spacing:.08em;margin-bottom:12px">{filled}{empty}</div>
  <div style="font-family:var(--mono);font-size:12px;color:var(--muted)">{pct}% complete</div>
</div>"""

    steps = [
        ("L0 — Parsing symptom features",          10),
        ("L1 — Scoring epidemiological priors",     25),
        ("L2 — Probing for rare / zebra diagnoses", 42),
        ("L3 — Mapping comorbidity modifiers",      60),
        ("L4 — Weighing examination evidence",      76),
        ("L5 — Ranking final differential",         92),
    ]
    for label, pct in steps:
        yield _status(label, pct), EMPTY_HTML, EMPTY_HTML, EMPTY_HTML, _render_archive()

    result = engine.analyse(
        patient_age=patient_age,
        patient_sex=patient_sex,
        chief_complaint=chief_complaint,
        symptoms=symptoms,
        vitals=vitals,
        history=history,
        exam_findings=exam_findings,
    )

    yield (
        _render_differential(result),
        _render_workup(result),
        _render_cascade_timeline(result),
        _render_prior_evolution(result),
        _render_archive(),
    )


# ── load saved case ────────────────────────────────────────────────────────────

def load_saved_case(choice: str):
    if not choice or "—" not in choice:
        return (
            gr.update(), gr.update(), gr.update(), gr.update(),
            gr.update(), gr.update(), gr.update(),
            gr.update(), gr.update(), gr.update(), gr.update(),
            gr.update(value=_render_archive()),
        )
    case_id = choice.split("—")[0].strip()
    result  = engine.load_case(case_id)
    if not result:
        err = "<div class='mde-panel' style='color:#fc8181;padding:24px;text-align:center;font-family:var(--mono)'>Case not found in archive.</div>"
        return (
            gr.update(), gr.update(), gr.update(), gr.update(),
            gr.update(), gr.update(), gr.update(),
            gr.update(value=err), gr.update(), gr.update(), gr.update(),
            gr.update(value=_render_archive()),
        )
    banner = f"""<div style="margin-bottom:12px;padding:8px 14px;border-radius:10px;
background:rgba(99,179,237,0.10);border:1px solid rgba(99,179,237,0.25);
color:#63b3ed;font-family:var(--mono);font-size:10px;letter-spacing:.1em;text-transform:uppercase">
Case {case_id[:8]} loaded from archive — agents not re-run</div>"""
    return (
        gr.update(value=result.get("patient_age", "")),
        gr.update(value=result.get("patient_sex", "Male")),
        gr.update(value=result.get("chief_complaint", "")),
        gr.update(value=result.get("symptoms", "")),
        gr.update(value=result.get("vitals", "")),
        gr.update(value=result.get("history", "")),
        gr.update(value=result.get("exam_findings", "")),
        gr.update(value=banner + _render_differential(result)),
        gr.update(value=_render_workup(result)),
        gr.update(value=_render_cascade_timeline(result)),
        gr.update(value=_render_prior_evolution(result)),
        gr.update(value=_render_archive()),
    )


# ── sample loaders ─────────────────────────────────────────────────────────────

def _load_chest():
    c = SAMPLE_CASES["Chest Pain (Classic)"]
    return c["age"], c["sex"], c["complaint"], c["symptoms"], c["vitals"], c["history"], c["exam"]

def _load_headache():
    c = SAMPLE_CASES["Headache (Thunderclap)"]
    return c["age"], c["sex"], c["complaint"], c["symptoms"], c["vitals"], c["history"], c["exam"]

def _load_dyspnoea():
    c = SAMPLE_CASES["Dyspnoea (Decompensation)"]
    return c["age"], c["sex"], c["complaint"], c["symptoms"], c["vitals"], c["history"], c["exam"]


# ── Gradio layout ──────────────────────────────────────────────────────────────

with gr.Blocks(css=APP_CSS, title="Medical Differential Engine") as demo:

    with gr.Column(elem_classes="mde-shell"):

        gr.HTML(HERO_HTML)

        # ── Case archive loader ──────────────────────────────────────────────
        with gr.Row(elem_classes="mde-panel"):
            gr.HTML('<div class="mde-panel-label" style="margin-bottom:0;margin-right:12px;white-space:nowrap">Load saved case</div>')
            case_selector = gr.Dropdown(
                label="",
                choices=_case_choices(),
                value=None,
                interactive=True,
                scale=4,
                show_label=False,
            )
            refresh_cases_btn = gr.Button("↺ Refresh", variant="secondary", scale=1, size="sm")
            load_case_btn     = gr.Button("Load case  ▶", variant="primary", scale=1, size="sm")

        with gr.Row():
            # ── LEFT: input form ──────────────────────────────────────────────
            with gr.Column(scale=2):
                with gr.Column(elem_classes="mde-panel"):

                    gr.HTML('<div class="mde-panel-label">Quick load sample case</div>')
                    with gr.Row():
                        sample_chest_btn    = gr.Button("💔 Chest Pain",       size="sm")
                        sample_head_btn     = gr.Button("🧠 Thunderclap HA",   size="sm")
                        sample_dyspnoea_btn = gr.Button("🫁 Dyspnoea",         size="sm")

                    gr.HTML('<div style="height:1px;background:var(--border);margin:14px 0"></div>')
                    gr.HTML('<div class="mde-panel-label">Patient details</div>')

                    with gr.Row():
                        patient_age = gr.Textbox(label="Age", placeholder="e.g. 58", scale=1)
                        patient_sex = gr.Dropdown(
                            label="Sex",
                            choices=["Male", "Female", "Other"],
                            value="Male", scale=1,
                        )
                    chief_complaint = gr.Textbox(
                        label="Chief Complaint",
                        placeholder="Primary presenting complaint…",
                        lines=1,
                    )
                    symptoms = gr.Textbox(
                        label="Symptoms & History of Presenting Complaint",
                        placeholder="Onset, character, severity, timing, modifying factors…",
                        lines=5,
                    )
                    vitals = gr.Textbox(
                        label="Vital Signs",
                        placeholder="BP | HR | RR | Temp | SpO2",
                        lines=1,
                    )
                    history = gr.Textbox(
                        label="PMH, Medications & Social History",
                        placeholder="PMH, medications, allergies, smoking/alcohol…",
                        lines=4,
                    )
                    exam_findings = gr.Textbox(
                        label="Physical Examination Findings",
                        placeholder="Findings by system…",
                        lines=4,
                    )

                    run_btn = gr.Button(
                        "▶  RUN BAYESIAN CASCADE",
                        variant="primary",
                        size="lg",
                    )

                # ── Archive panel ─────────────────────────────────────────────
                with gr.Column(elem_classes="mde-panel"):
                    gr.HTML('<div class="mde-panel-label">Case archive</div>')
                    archive_out = gr.HTML(value=_render_archive())

            # ── RIGHT: results ────────────────────────────────────────────────
            with gr.Column(scale=3):
                with gr.Tabs():
                    with gr.Tab("🩺 Differential"):
                        diff_out = gr.HTML(value=EMPTY_HTML)
                    with gr.Tab("🔬 Workup & Flags"):
                        workup_out = gr.HTML(value=EMPTY_HTML)
                    with gr.Tab("🔄 Cascade Trace"):
                        cascade_out = gr.HTML(value=EMPTY_HTML)
                    with gr.Tab("📊 Probability Evolution"):
                        evolution_out = gr.HTML(value=EMPTY_HTML)

    # ── references ─────────────────────────────────────────────────────────────
    inputs_list  = [patient_age, patient_sex, chief_complaint, symptoms, vitals, history, exam_findings]
    outputs_list = [diff_out, workup_out, cascade_out, evolution_out, archive_out]

    # ── run button (streaming generator) ──────────────────────────────────────
    run_btn.click(fn=run_analysis, inputs=inputs_list, outputs=outputs_list)

    # ── sample loaders ─────────────────────────────────────────────────────────
    sample_chest_btn.click(fn=_load_chest,      inputs=[], outputs=inputs_list)
    sample_head_btn.click(fn=_load_headache,    inputs=[], outputs=inputs_list)
    sample_dyspnoea_btn.click(fn=_load_dyspnoea,inputs=[], outputs=inputs_list)

    # ── load saved case ────────────────────────────────────────────────────────
    load_case_btn.click(
        fn=load_saved_case,
        inputs=[case_selector],
        outputs=inputs_list + [diff_out, workup_out, cascade_out, evolution_out, archive_out],
    )
    refresh_cases_btn.click(fn=_case_choices, outputs=[case_selector])

    # ── on page load ────────────────────────────────────────────────────────────
    demo.load(fn=_render_archive, outputs=[archive_out])
    demo.load(fn=_case_choices,   outputs=[case_selector])


if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)