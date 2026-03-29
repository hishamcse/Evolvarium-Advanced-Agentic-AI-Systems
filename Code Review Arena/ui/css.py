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