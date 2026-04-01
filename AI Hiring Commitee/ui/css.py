APP_CSS = """
:root {
  --bg:       radial-gradient(ellipse at 15% 0%, #0d1117 0%, #090d12 55%, #060810 100%);
  --panel:    rgba(13, 17, 24, 0.92);
  --border:   rgba(60, 120, 220, 0.16);
  --border-hi:rgba(60, 120, 220, 0.35);
  --text:     #d0ddf0;
  --muted:    #5a7090;
  --blue:     #4080e0;
  --cyan:     #40c0d0;
  --green:    #40b060;
  --red:      #d04040;
  --amber:    #d0a030;
  --purple:   #9060c0;
}
.gradio-container {
  background: var(--bg) !important;
  color: var(--text) !important;
  font-family: 'Inter', system-ui, sans-serif !important;
}
footer { display: none !important; }

.hc-shell {
  border-radius: 24px;
  border: 1px solid rgba(255,255,255,0.05);
  background: linear-gradient(180deg, rgba(255,255,255,0.018) 0%, rgba(255,255,255,0.005) 100%);
  box-shadow: 0 28px 70px rgba(0,0,0,0.65);
  padding: 0 0 36px;
  overflow: hidden;
}

/* ── hero ── */
.hc-hero {
  border-radius: 24px 24px 0 0;
  padding: 36px 40px 30px;
  background:
    radial-gradient(ellipse at top right, rgba(64,128,224,0.13) 0%, transparent 50%),
    radial-gradient(ellipse at bottom left, rgba(144,96,192,0.10) 0%, transparent 45%),
    linear-gradient(180deg, rgba(10,14,22,0.96) 0%, rgba(6,8,16,0.98) 100%);
  border-bottom: 1px solid var(--border);
}
.hc-kicker {
  text-transform: uppercase; letter-spacing: 0.26em; font-size: 10px;
  font-weight: 700; color: var(--blue); margin-bottom: 10px;
}
.hc-title {
  font-size: 36px; font-weight: 800; line-height: 1.08; margin: 0 0 8px;
  background: linear-gradient(90deg, #d0ddf0 30%, #4080e0 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.hc-subtitle { color: var(--muted); font-size: 13px; margin: 0 0 20px; line-height: 1.6; }
.hc-badge-row { display: flex; flex-wrap: wrap; gap: 8px; }
.hc-badge {
  padding: 4px 13px; border-radius: 999px; font-size: 11px; font-weight: 600;
  background: rgba(64,128,224,0.09); border: 1px solid rgba(64,128,224,0.22); color: var(--blue);
}

/* ── panels ── */
.hc-panel {
  background: var(--panel); border: 1px solid var(--border);
  border-radius: 20px; padding: 22px 24px; box-shadow: 0 8px 32px rgba(0,0,0,0.35);
}
.hc-panel-label {
  text-transform: uppercase; letter-spacing: 0.22em; font-size: 9px;
  font-weight: 700; color: var(--muted); margin-bottom: 14px;
}

/* ── decision banner ── */
.hc-decision {
  border-radius: 20px; padding: 22px 28px; text-align: center;
}
.hc-decision-label {
  font-size: 10px; text-transform: uppercase; letter-spacing: 0.22em;
  font-weight: 700; color: var(--muted); margin-bottom: 10px;
}
.hc-decision-verdict {
  font-size: 32px; font-weight: 900; letter-spacing: 0.04em; margin-bottom: 8px;
}
.hc-decision-score {
  font-size: 48px; font-weight: 900; margin-bottom: 6px;
}
.hc-score-label { font-size: 11px; color: var(--muted); text-transform: uppercase; letter-spacing: 0.12em; }

/* ── score track ── */
.hc-score-track {
  width: 100%; height: 8px; border-radius: 999px;
  background: rgba(255,255,255,0.07); overflow: hidden; margin: 10px 0 4px;
}
.hc-score-fill { height: 100%; border-radius: 999px; }

/* ── evaluator cards ── */
.hc-eval-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.hc-eval-card {
  border-radius: 16px; padding: 16px 18px;
  background: rgba(255,255,255,0.03);
  font-size: 13px; line-height: 1.55;
}
.hc-eval-header {
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: 12px; padding-bottom: 10px;
  border-bottom: 1px solid rgba(255,255,255,0.07);
}
.hc-eval-name {
  font-size: 10px; font-weight: 800; text-transform: uppercase;
  letter-spacing: 0.16em;
}
.hc-eval-score { font-size: 24px; font-weight: 900; }
.hc-eval-verdict {
  font-size: 9px; font-weight: 700; text-transform: uppercase;
  letter-spacing: 0.12em; padding: 3px 9px; border-radius: 999px;
}

/* evaluator colour themes */
.eval-technical { border: 1px solid rgba(64,128,224,0.30); }
.eval-manager   { border: 1px solid rgba(144,96,192,0.28); }
.eval-culture   { border: 1px solid rgba(64,192,208,0.28); }
.eval-advocate  { border: 1px solid rgba(208,64,64,0.28);  }

.name-technical { color: var(--blue);   }
.name-manager   { color: var(--purple); }
.name-culture   { color: var(--cyan);   }
.name-advocate  { color: var(--red);    }

/* ── list items ── */
.hc-list { display: grid; gap: 6px; margin-top: 8px; }
.hc-list-item {
  padding: 7px 12px; border-radius: 9px;
  font-size: 12px; line-height: 1.4;
  background: rgba(255,255,255,0.03);
  border-left: 2px solid;
}
.item-strength { border-color: var(--green);  color: var(--text); }
.item-concern  { border-color: var(--red);    color: var(--text); }
.item-q        { border-color: var(--amber);  color: var(--text); }
.item-agree    { border-color: var(--blue);   color: var(--text); }
.item-disagree { border-color: var(--purple); color: var(--text); }
.item-flag     { border-color: var(--red);    color: var(--text); }

/* ── session archive ── */
.hc-session-row {
  display: grid; grid-template-columns: 1fr auto auto;
  gap: 12px; align-items: center;
  padding: 10px 14px; border-radius: 12px; margin-bottom: 6px;
  background: rgba(255,255,255,0.02); border: 1px solid var(--border);
  font-size: 12px;
}
.hc-session-name { font-weight: 700; color: var(--text); font-size: 13px; }
.hc-session-role { color: var(--muted); font-size: 11px; }
.hc-session-decision {
  font-size: 9px; font-weight: 800; text-transform: uppercase;
  letter-spacing: 0.10em; padding: 3px 9px; border-radius: 999px;
}

/* ── gradio overrides ── */
.gr-button-primary {
  background: linear-gradient(135deg, #1a50c0, #0f3090) !important;
  border: none !important; border-radius: 12px !important;
  font-weight: 700 !important; letter-spacing: 0.06em !important;
  padding: 12px 28px !important; color: #d0ddf0 !important;
  text-transform: uppercase !important; font-size: 12px !important;
}
.gr-button-secondary {
  background: rgba(64,128,224,0.08) !important;
  border: 1px solid rgba(64,128,224,0.28) !important;
  border-radius: 12px !important; font-weight: 700 !important;
  padding: 12px 20px !important; color: var(--blue) !important;
  text-transform: uppercase !important; font-size: 12px !important;
}
textarea, input[type=text] {
  background: rgba(13,17,24,0.95) !important;
  border: 1px solid var(--border) !important;
  color: var(--text) !important; border-radius: 12px !important;
}
label > span {
  color: var(--muted) !important; font-size: 11px !important;
  text-transform: uppercase !important; letter-spacing: 0.14em !important;
}
@media (max-width: 860px) { .hc-eval-grid { grid-template-columns: 1fr; } }
"""