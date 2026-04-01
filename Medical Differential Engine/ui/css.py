APP_CSS = """
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:ital,wght@0,400;0,600;1,400&family=Instrument+Serif:ital@0;1&family=DM+Sans:wght@300;400;500&display=swap');

:root {
  --bg:         #0a0d12;
  --surface:    #111520;
  --surface-2:  #161c28;
  --border:     rgba(99,179,237,0.12);
  --border-hi:  rgba(99,179,237,0.28);
  --text:       #e2e8f4;
  --muted:      #6b7a99;
  --dim:        #3d4a63;

  /* probability colour ramp — cool → warm */
  --p-excluded:      #4a5568;
  --p-unlikely:      #667eea;
  --p-possible:      #38b2ac;
  --p-probable:      #d69e2e;
  --p-likely:        #ed8936;
  --p-highly:        #e53e3e;

  /* urgency */
  --emergency:  #fc4444;
  --urgent:     #f6ad55;
  --routine:    #68d391;

  --mono: 'IBM Plex Mono', monospace;
  --serif: 'Instrument Serif', Georgia, serif;
  --sans: 'DM Sans', system-ui, sans-serif;
}

.gradio-container {
  background: var(--bg) !important;
  color: var(--text) !important;
  font-family: var(--sans) !important;
}
footer { display: none !important; }

/* ── shell ── */
.mde-shell {
  border-radius: 20px;
  border: 1px solid rgba(255,255,255,0.04);
  background: linear-gradient(180deg, rgba(255,255,255,0.015) 0%, rgba(255,255,255,0.004) 100%);
  box-shadow: 0 32px 80px rgba(0,0,0,0.7);
  overflow: hidden;
}

/* ── hero ── */
.mde-hero {
  padding: 40px 44px 32px;
  background:
    radial-gradient(ellipse at top left,  rgba(66,153,225,0.12) 0%, transparent 50%),
    radial-gradient(ellipse at top right, rgba(99,179,237,0.06) 0%, transparent 45%),
    linear-gradient(180deg, rgba(14,22,38,0.98) 0%, rgba(10,13,18,0.99) 100%);
  border-bottom: 1px solid var(--border);
}
.mde-kicker {
  font-family: var(--mono);
  font-size: 10px;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: #63b3ed;
  margin-bottom: 14px;
}
.mde-title {
  font-family: var(--serif);
  font-size: 42px;
  font-style: italic;
  font-weight: 400;
  line-height: 1.05;
  margin: 0 0 10px;
  color: var(--text);
}
.mde-title span { color: #63b3ed; }
.mde-subtitle {
  font-family: var(--sans);
  font-size: 13px;
  color: var(--muted);
  margin: 0 0 22px;
  line-height: 1.6;
  max-width: 600px;
}
.mde-badge-row { display: flex; flex-wrap: wrap; gap: 8px; }
.mde-badge {
  padding: 4px 14px;
  border-radius: 999px;
  font-family: var(--mono);
  font-size: 10px;
  letter-spacing: 0.06em;
  background: rgba(99,179,237,0.07);
  border: 1px solid rgba(99,179,237,0.18);
  color: #63b3ed;
}
.mde-badge.red { background:rgba(229,62,62,0.07); border-color:rgba(229,62,62,0.2); color:#fc8181; }
.mde-badge.green { background:rgba(104,211,145,0.07); border-color:rgba(104,211,145,0.2); color:#68d391; }
.mde-badge.amber { background:rgba(246,173,85,0.07); border-color:rgba(246,173,85,0.2); color:#f6ad55; }

/* ── panels ── */
.mde-panel {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 18px;
  padding: 20px 22px;
  box-shadow: 0 4px 24px rgba(0,0,0,0.25);
}
.mde-panel-label {
  font-family: var(--mono);
  font-size: 9px;
  letter-spacing: 0.24em;
  text-transform: uppercase;
  color: var(--muted);
  margin-bottom: 14px;
}

/* ── cascade progress indicator ── */
.mde-cascade {
  display: flex;
  align-items: center;
  gap: 0;
  margin-bottom: 24px;
  overflow-x: auto;
}
.mde-cascade-step {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
  min-width: 90px;
}
.mde-step-circle {
  width: 34px;
  height: 34px;
  border-radius: 50%;
  border: 1.5px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--mono);
  font-size: 11px;
  color: var(--muted);
  background: var(--surface);
}
.mde-step-circle.active {
  border-color: #63b3ed;
  color: #63b3ed;
  background: rgba(99,179,237,0.1);
}
.mde-step-circle.done {
  border-color: #68d391;
  color: #68d391;
  background: rgba(104,211,145,0.1);
}
.mde-step-label {
  font-family: var(--mono);
  font-size: 9px;
  letter-spacing: 0.06em;
  color: var(--muted);
  text-align: center;
  line-height: 1.3;
}
.mde-cascade-line {
  flex: 1;
  height: 1px;
  background: var(--border);
  min-width: 20px;
  margin-bottom: 18px;
}

/* ── diagnosis cards ── */
.mde-dx-grid { display: grid; gap: 10px; }
.mde-dx-card {
  display: grid;
  grid-template-columns: 3fr 1fr;
  gap: 12px;
  align-items: start;
  padding: 14px 16px;
  border-radius: 14px;
  background: var(--surface-2);
  border: 1px solid var(--border);
  transition: border-color 0.2s;
}
.mde-dx-card:hover { border-color: var(--border-hi); }
.mde-dx-card.rank-1 { border-left: 3px solid #e53e3e; }
.mde-dx-card.rank-2 { border-left: 3px solid #ed8936; }
.mde-dx-card.rank-3 { border-left: 3px solid #d69e2e; }
.mde-dx-card.emergency-dx { border-color: rgba(252,68,68,0.35); }
.mde-dx-name {
  font-family: var(--sans);
  font-size: 14px;
  font-weight: 500;
  color: var(--text);
  margin-bottom: 4px;
}
.mde-dx-icd {
  font-family: var(--mono);
  font-size: 10px;
  color: var(--muted);
  margin-bottom: 8px;
}
.mde-dx-features { display: flex; flex-wrap: wrap; gap: 5px; }
.mde-feature-tag {
  font-family: var(--mono);
  font-size: 9px;
  padding: 2px 7px;
  border-radius: 4px;
}
.feat-for  { background:rgba(104,211,145,0.1); color:#68d391; border:0.5px solid rgba(104,211,145,0.2); }
.feat-against { background:rgba(229,62,62,0.08); color:#fc8181; border:0.5px solid rgba(229,62,62,0.15); }
.mde-rare-flag {
  font-family: var(--mono);
  font-size: 9px;
  padding: 2px 7px;
  border-radius: 4px;
  background: rgba(159,122,234,0.12);
  color: #b794f4;
  border: 0.5px solid rgba(159,122,234,0.2);
}

/* ── probability bar ── */
.mde-prob-wrap { text-align: right; }
.mde-prob-pct {
  font-family: var(--mono);
  font-size: 22px;
  font-weight: 600;
  margin-bottom: 4px;
}
.mde-confidence-label {
  font-family: var(--mono);
  font-size: 9px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  margin-bottom: 8px;
}
.mde-prob-bar {
  width: 100%;
  height: 5px;
  border-radius: 999px;
  background: rgba(255,255,255,0.07);
  overflow: hidden;
}
.mde-prob-fill { height: 100%; border-radius: 999px; }
.mde-urgency-tag {
  display: inline-block;
  font-family: var(--mono);
  font-size: 9px;
  letter-spacing: 0.1em;
  padding: 3px 8px;
  border-radius: 4px;
  margin-top: 6px;
}
.urg-emergency { background: rgba(252,68,68,0.12); color: var(--emergency); border: 0.5px solid rgba(252,68,68,0.25); }
.urg-urgent    { background: rgba(246,173,85,0.10); color: var(--urgent);    border: 0.5px solid rgba(246,173,85,0.22); }
.urg-routine   { background: rgba(104,211,145,0.08);color: var(--routine);   border: 0.5px solid rgba(104,211,145,0.18); }

/* ── workup plan ── */
.mde-workup-item {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 10px 12px;
  border-radius: 10px;
  background: rgba(255,255,255,0.025);
  border: 0.5px solid var(--border);
  margin-bottom: 7px;
  font-family: var(--mono);
  font-size: 12px;
  color: var(--text);
}
.workup-stat   { color: var(--emergency); font-weight: 600; min-width: 50px; }
.workup-urgent { color: var(--urgent);    font-weight: 600; min-width: 50px; }
.workup-routine{ color: var(--routine);   font-weight: 600; min-width: 50px; }

/* ── red flags ── */
.mde-redflag {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 14px;
  border-radius: 10px;
  background: rgba(229,62,62,0.07);
  border: 1px solid rgba(229,62,62,0.2);
  margin-bottom: 7px;
  font-family: var(--mono);
  font-size: 12px;
  color: #fc8181;
}
.redflag-dot { width: 6px; height: 6px; border-radius: 50%; background: var(--emergency); flex-shrink: 0; }

/* ── disposition banner ── */
.mde-disposition {
  border-radius: 14px;
  padding: 18px 20px;
  text-align: center;
  margin-bottom: 16px;
}
.mde-disposition.EMERGENCY {
  background: rgba(229,62,62,0.10);
  border: 1px solid rgba(229,62,62,0.35);
}
.mde-disposition.URGENT {
  background: rgba(246,173,85,0.08);
  border: 1px solid rgba(246,173,85,0.28);
}
.mde-disposition.ROUTINE {
  background: rgba(104,211,145,0.06);
  border: 1px solid rgba(104,211,145,0.20);
}
.mde-dispo-label {
  font-family: var(--mono);
  font-size: 11px;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  margin-bottom: 4px;
}
.mde-dispo-value {
  font-family: var(--serif);
  font-style: italic;
  font-size: 28px;
}

/* ── cascade timeline ── */
.mde-cascade-timeline { display: grid; gap: 8px; }
.mde-cascade-row {
  display: grid;
  grid-template-columns: 140px 1fr;
  gap: 10px;
  align-items: start;
}
.mde-cascade-actor {
  font-family: var(--mono);
  font-size: 10px;
  letter-spacing: 0.06em;
  color: #63b3ed;
  padding: 8px 10px;
  background: rgba(99,179,237,0.07);
  border: 0.5px solid rgba(99,179,237,0.15);
  border-radius: 8px;
  text-align: center;
}
.mde-cascade-body {
  font-family: var(--sans);
  font-size: 12px;
  color: var(--muted);
  padding: 8px 12px;
  background: rgba(255,255,255,0.025);
  border: 0.5px solid var(--border);
  border-radius: 8px;
  line-height: 1.5;
}

/* ── comorbidity flags ── */
.mde-comorbidity {
  padding: 8px 12px;
  border-radius: 8px;
  background: rgba(246,173,85,0.07);
  border: 0.5px solid rgba(246,173,85,0.18);
  font-family: var(--mono);
  font-size: 11px;
  color: #f6ad55;
  margin-bottom: 6px;
}

/* ── clinical summary ── */
.mde-summary {
  font-family: var(--serif);
  font-style: italic;
  font-size: 15px;
  line-height: 1.7;
  color: var(--text);
  padding: 20px 22px;
  border-left: 3px solid #63b3ed;
  background: rgba(99,179,237,0.04);
  border-radius: 0 12px 12px 0;
}

/* ── form elements ── */
.gradio-container input, .gradio-container textarea, .gradio-container select {
  background: var(--surface) !important;
  color: var(--text) !important;
  border: 1px solid var(--border) !important;
  border-radius: 10px !important;
  font-family: var(--sans) !important;
}
.gradio-container input:focus, .gradio-container textarea:focus {
  border-color: rgba(99,179,237,0.4) !important;
  box-shadow: 0 0 0 2px rgba(99,179,237,0.08) !important;
  outline: none !important;
}
.gradio-container label, .gradio-container .label-wrap span {
  font-family: var(--mono) !important;
  font-size: 10px !important;
  letter-spacing: 0.16em !important;
  text-transform: uppercase !important;
  color: var(--muted) !important;
}
.gradio-container button.primary {
  background: linear-gradient(135deg, #2b6cb0, #1a4a8a) !important;
  border: 1px solid rgba(99,179,237,0.25) !important;
  color: #e2e8f4 !important;
  font-family: var(--mono) !important;
  font-size: 11px !important;
  letter-spacing: 0.12em !important;
  border-radius: 10px !important;
  padding: 12px 24px !important;
}
.gradio-container button.primary:hover {
  background: linear-gradient(135deg, #3182ce, #2b6cb0) !important;
}

/* ── case archive ── */
.mde-archive-item {
  padding: 12px 14px;
  border-radius: 12px;
  background: var(--surface-2);
  border: 1px solid var(--border);
  margin-bottom: 8px;
  cursor: pointer;
  transition: border-color 0.15s;
}
.mde-archive-item:hover { border-color: var(--border-hi); }
.mde-archive-cc {
  font-family: var(--sans);
  font-size: 13px;
  font-weight: 500;
  color: var(--text);
  margin-bottom: 4px;
}
.mde-archive-meta {
  font-family: var(--mono);
  font-size: 10px;
  color: var(--muted);
}

/* ── empty state ── */
.mde-empty {
  text-align: center;
  padding: 64px 24px;
  color: var(--muted);
  font-family: var(--mono);
  font-size: 12px;
  letter-spacing: 0.08em;
}
.mde-empty-icon {
  font-size: 32px;
  margin-bottom: 14px;
  opacity: 0.4;
}
"""