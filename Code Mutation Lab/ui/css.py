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