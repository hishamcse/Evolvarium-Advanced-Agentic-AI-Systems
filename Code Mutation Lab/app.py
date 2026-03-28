"""
Code Mutation Lab — Gradio UI
Evolutionary code improvement through strategy-driven AI mutations.
Beautiful dark lab-style interface with live generation tracking.
"""
import html
import re
from typing import Any, Dict, List

import gradio as gr
from graph.builder import build_graph

graph = build_graph()

# ── CSS ────────────────────────────────────────────────────────────────────────

APP_CSS = """
:root {
  --bg:        radial-gradient(ellipse at 15% 0%, #0e1a12 0%, #07100a 50%, #040a06 100%);
  --panel:     rgba(8, 18, 10, 0.90);
  --panel-alt: rgba(255, 255, 255, 0.03);
  --border:    rgba(60, 200, 100, 0.16);
  --border-hi: rgba(60, 200, 100, 0.34);
  --text:      #d6f0df;
  --muted:     #5a8c6a;
  --green:     #3ddd7a;
  --lime:      #a8f060;
  --cyan:      #5ee8c8;
  --gold:      #ffc940;
  --red:       #ff5a5e;
  --purple:    #c4aaff;
  --orange:    #ff9d3d;
  --dna-1:     rgba(61,221,122,0.55);
  --dna-2:     rgba(94,232,200,0.40);
}
.gradio-container {
  background: var(--bg) !important;
  color: var(--text) !important;
  font-family: 'Inter', system-ui, sans-serif !important;
}
footer { display: none !important; }

/* ── shell ── */
.lab-shell {
  border-radius: 28px;
  border: 1px solid rgba(255,255,255,0.06);
  background: linear-gradient(180deg, rgba(255,255,255,0.022) 0%, rgba(255,255,255,0.006) 100%);
  box-shadow: 0 32px 80px rgba(0,0,0,0.55);
  padding: 0 0 36px;
  overflow: hidden;
}

/* ── hero ── */
.lab-hero {
  border-radius: 28px 28px 0 0;
  padding: 34px 38px 30px;
  background:
    radial-gradient(ellipse at top right,  rgba(61,221,122,0.14) 0%, transparent 50%),
    radial-gradient(ellipse at bottom left, rgba(168,240,96,0.09) 0%, transparent 45%),
    linear-gradient(160deg, rgba(20,80,40,0.28) 0%, rgba(4,10,6,0.94) 100%);
  border-bottom: 1px solid var(--border);
}
.lab-kicker {
  text-transform: uppercase;
  letter-spacing: 0.22em;
  font-size: 11px;
  font-weight: 700;
  color: var(--green);
  margin-bottom: 10px;
}
.lab-title {
  font-size: 36px;
  font-weight: 900;
  line-height: 1.06;
  margin: 0 0 8px;
  background: linear-gradient(90deg, #d6f0df 30%, var(--green) 70%, var(--lime) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
.lab-subtitle { color: var(--muted); font-size: 14px; margin: 0 0 20px; line-height: 1.6; }
.lab-badge-row { display: flex; flex-wrap: wrap; gap: 8px; }
.lab-badge {
  padding: 5px 14px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 600;
  background: rgba(61,221,122,0.09);
  border: 1px solid rgba(61,221,122,0.22);
  color: var(--green);
}

/* ── panels ── */
.lab-panel {
  background: var(--panel);
  border: 1px solid var(--border);
  border-radius: 22px;
  padding: 22px 24px;
  box-shadow: 0 10px 36px rgba(0,0,0,0.30);
}
.lab-panel-label {
  text-transform: uppercase;
  letter-spacing: 0.16em;
  font-size: 10px;
  font-weight: 700;
  color: var(--muted);
  margin-bottom: 14px;
}

/* ── control section ── */
.lab-control-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-bottom: 14px;
}
.lab-stat-card {
  border-radius: 16px;
  padding: 14px 16px;
  background: rgba(61,221,122,0.06);
  border: 1px solid rgba(61,221,122,0.14);
}
.lab-stat-label { font-size: 10px; text-transform: uppercase; letter-spacing: 0.14em; color: var(--muted); margin-bottom: 6px; }
.lab-stat-value { font-size: 28px; font-weight: 900; color: var(--green); line-height: 1; }
.lab-stat-sub   { font-size: 11px; color: var(--muted); margin-top: 3px; }

/* ── dna strand / score ring ── */
.lab-score-ring {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 110px;
  height: 110px;
  border-radius: 50%;
  border: 3px solid var(--green);
  background: radial-gradient(circle, rgba(61,221,122,0.12) 0%, transparent 70%);
  font-size: 40px;
  font-weight: 900;
  color: var(--green);
}

/* ── strategy chips ── */
.lab-strategy-chips { display: flex; flex-wrap: wrap; gap: 7px; margin-bottom: 14px; }
.lab-strategy-chip {
  padding: 5px 13px;
  border-radius: 999px;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.03em;
  background: rgba(61,221,122,0.08);
  border: 1px solid rgba(61,221,122,0.20);
  color: var(--green);
}
.strat-perf   { background: rgba(255,157,61,0.10); border-color: rgba(255,157,61,0.28); color: var(--orange); }
.strat-read   { background: rgba(94,232,200,0.10); border-color: rgba(94,232,200,0.28); color: var(--cyan);   }
.strat-mem    { background: rgba(255,90,94,0.10);  border-color: rgba(255,90,94,0.28);  color: var(--red);    }
.strat-pyth   { background: rgba(61,221,122,0.10); border-color: rgba(61,221,122,0.28); color: var(--lime);   }
.strat-simp   { background: rgba(196,170,255,0.10);border-color: rgba(196,170,255,0.28);color: var(--purple); }
.strat-func   { background: rgba(255,201,64,0.10); border-color: rgba(255,201,64,0.28); color: var(--gold);   }

/* ── generation timeline ── */
.lab-gen-timeline { display: grid; gap: 10px; }
.lab-gen-row {
  display: grid;
  grid-template-columns: 90px 1fr;
  gap: 12px;
  align-items: start;
}
.lab-gen-badge {
  border-radius: 14px;
  padding: 12px 8px;
  text-align: center;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.10em;
  background: rgba(61,221,122,0.08);
  border: 1px solid rgba(61,221,122,0.20);
  color: var(--green);
}
.lab-gen-card {
  border-radius: 16px;
  padding: 14px 16px;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.08);
  font-size: 13px;
  line-height: 1.55;
}
.lab-gen-score { font-size: 22px; font-weight: 900; margin-top: 4px; }
.lab-gen-improvement {
  font-size: 11px;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 999px;
  display: inline-block;
  margin-top: 4px;
}
.improvement-up   { background: rgba(61,221,122,0.15); color: var(--green); border: 1px solid rgba(61,221,122,0.30); }
.improvement-down { background: rgba(255,90,94,0.12);  color: var(--red);   border: 1px solid rgba(255,90,94,0.28);  }
.improvement-same { background: rgba(255,255,255,0.06);color: var(--muted); border: 1px solid rgba(255,255,255,0.12);}

/* ── variant cards ── */
.lab-variant-grid { display: grid; gap: 14px; }
.lab-variant-card {
  border-radius: 18px;
  padding: 18px 20px;
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.08);
}
.lab-variant-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}
.lab-variant-winner {
  border-color: rgba(61,221,122,0.35) !important;
  background: rgba(61,221,122,0.05) !important;
}
.lab-winner-crown {
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.14em;
  color: var(--lime);
  border: 1px solid rgba(168,240,96,0.30);
  background: rgba(168,240,96,0.10);
  padding: 3px 10px;
  border-radius: 999px;
}
.lab-dim-row { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-top: 12px; }
.lab-dim-cell {
  border-radius: 12px;
  padding: 10px 12px;
  text-align: center;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.07);
}
.lab-dim-cell-label { font-size: 9px; text-transform: uppercase; letter-spacing: 0.12em; color: var(--muted); margin-bottom: 4px; }
.lab-dim-cell-value { font-size: 20px; font-weight: 800; }

/* ── score bar ── */
.lab-score-bar { margin-top: 10px; }
.lab-score-bar-track { width: 100%; height: 7px; border-radius: 999px; background: rgba(255,255,255,0.07); overflow: hidden; }
.lab-score-bar-fill  { height: 100%; border-radius: 999px; }

/* ── fitness chart ── */
.lab-fitness { display: grid; gap: 8px; align-items: end; }
.lab-fitness-row {
  display: grid;
  grid-template-columns: 60px 1fr 44px;
  gap: 10px;
  align-items: center;
}
.lab-fitness-gen { font-size: 11px; color: var(--muted); text-align: right; }
.lab-fitness-track { height: 22px; border-radius: 6px; background: rgba(255,255,255,0.06); overflow: hidden; position: relative; }
.lab-fitness-bar { height: 100%; border-radius: 6px; position: relative; }
.lab-fitness-score { font-size: 13px; font-weight: 700; text-align: right; }

/* ── summary hero ── */
.lab-summary-hero {
  border-radius: 20px;
  padding: 20px 24px;
  background: linear-gradient(135deg, rgba(61,221,122,0.13), rgba(94,232,200,0.07));
  border: 1px solid rgba(61,221,122,0.22);
  font-size: 14px;
  line-height: 1.65;
  color: var(--text);
}

/* ── code diff view ── */
.lab-diff-header {
  display: flex;
  gap: 10px;
  margin-bottom: 10px;
}
.lab-diff-label {
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.14em;
  font-weight: 700;
  padding: 4px 12px;
  border-radius: 999px;
}
.diff-original { background: rgba(255,90,94,0.12);  color: var(--red);   border: 1px solid rgba(255,90,94,0.25); }
.diff-evolved  { background: rgba(61,221,122,0.12); color: var(--green); border: 1px solid rgba(61,221,122,0.25); }

/* ── gradio overrides ── */
.gr-button-primary {
  background: linear-gradient(135deg, #1a7a3a, #0f5228) !important;
  border: none !important;
  border-radius: 14px !important;
  font-weight: 700 !important;
  letter-spacing: 0.04em !important;
  padding: 13px 32px !important;
  color: #d6f0df !important;
  box-shadow: 0 4px 20px rgba(20,100,50,0.40) !important;
  font-size: 14px !important;
}
.gr-button-primary:hover { opacity: 0.88 !important; }
textarea, input[type=text], input[type=number] {
  background: rgba(8,18,10,0.92) !important;
  border: 1px solid var(--border) !important;
  color: var(--text) !important;
  border-radius: 14px !important;
}
label > span { color: var(--muted) !important; font-size: 12px !important; }
.gr-slider { accent-color: var(--green) !important; }
"""

# ── Static HTML ────────────────────────────────────────────────────────────────

HERO_HTML = """
<div class="lab-hero">
  <div class="lab-kicker">Evolutionary Code Optimization &nbsp;·&nbsp; LangGraph + Ollama &nbsp;·&nbsp; Genetic Loop Architecture</div>
  <div class="lab-title">Code Mutation Lab</div>
  <div class="lab-subtitle">
    Your code enters as a seed. Each generation, strategy-driven AI agents mutate it into 3 competing variants —
    evaluated on performance, readability &amp; simplicity — and only the fittest survives to breed the next generation.
  </div>
  <div class="lab-badge-row">
    <span class="lab-badge">Genetic Loop</span>
    <span class="lab-badge">3 Variants / Generation</span>
    <span class="lab-badge">6 Mutation Strategies</span>
    <span class="lab-badge" style="background:rgba(94,232,200,0.09);border-color:rgba(94,232,200,0.22);color:#5ee8c8">Parallel Evaluation</span>
    <span class="lab-badge" style="background:rgba(168,240,96,0.09);border-color:rgba(168,240,96,0.22);color:#a8f060">Fitness Tracking</span>
    <span class="lab-badge" style="background:rgba(255,201,64,0.09);border-color:rgba(255,201,64,0.22);color:#ffc940">Full Variant History</span>
  </div>
</div>
"""

EMPTY_STATE_HTML = """
<div class="lab-panel" style="text-align:center;padding:52px 24px">
  <div style="font-size:42px;margin-bottom:12px">&#10010;</div>
  <div style="color:var(--muted);font-size:14px;margin-bottom:6px">Lab is idle</div>
  <div style="color:var(--muted);font-size:12px">Paste your code, set generations, and click Evolve to begin</div>
</div>
"""

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