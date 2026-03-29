APP_CSS = """
:root {
  --bg:      radial-gradient(ellipse at 10% 0%, #141018 0%, #0c0910 45%, #070609 100%);
  --panel:   rgba(18, 14, 22, 0.92);
  --border:  rgba(180, 140, 60, 0.18);
  --border-hi: rgba(180, 140, 60, 0.38);
  --text:    #e8dfc8;
  --muted:   #7a6e5a;
  --amber:   #d4a843;
  --gold:    #f0c060;
  --red:     #c03030;
  --red-hi:  #e04040;
  --green:   #3a8a4a;
  --cyan:    #4a9aaa;
  --dim:     rgba(212,168,67,0.08);
}
.gradio-container {
  background: var(--bg) !important;
  color: var(--text) !important;
  font-family: 'Georgia', 'Times New Roman', serif !important;
}
footer { display: none !important; }

/* ── shell ── */
.csi-shell {
  border-radius: 24px;
  border: 1px solid rgba(255,255,255,0.05);
  background: linear-gradient(180deg, rgba(255,255,255,0.018) 0%, rgba(255,255,255,0.005) 100%);
  box-shadow: 0 28px 70px rgba(0,0,0,0.65);
  padding: 0 0 32px;
  overflow: hidden;
}

/* ── hero ── */
.csi-hero {
  border-radius: 24px 24px 0 0;
  padding: 36px 40px 30px;
  background:
    radial-gradient(ellipse at top left,  rgba(180,60,30,0.15) 0%, transparent 50%),
    radial-gradient(ellipse at top right, rgba(212,168,67,0.10) 0%, transparent 45%),
    linear-gradient(180deg, rgba(20,10,8,0.95) 0%, rgba(7,6,9,0.98) 100%);
  border-bottom: 1px solid var(--border);
}
.csi-kicker {
  text-transform: uppercase;
  letter-spacing: 0.28em;
  font-size: 10px;
  font-weight: 700;
  color: var(--amber);
  margin-bottom: 10px;
  font-family: 'Inter', system-ui, sans-serif;
}
.csi-title {
  font-size: 38px;
  font-weight: 400;
  font-style: italic;
  line-height: 1.1;
  margin: 0 0 8px;
  color: var(--gold);
  letter-spacing: 0.02em;
}
.csi-subtitle {
  color: var(--muted);
  font-size: 13px;
  margin: 0 0 20px;
  font-family: 'Inter', system-ui, sans-serif;
  font-style: normal;
}
.csi-badge-row { display: flex; flex-wrap: wrap; gap: 8px; }
.csi-badge {
  padding: 4px 13px;
  border-radius: 999px;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.06em;
  font-family: 'Inter', system-ui, sans-serif;
  background: rgba(212,168,67,0.09);
  border: 1px solid rgba(212,168,67,0.22);
  color: var(--amber);
}

/* ── panels ── */
.csi-panel {
  background: var(--panel);
  border: 1px solid var(--border);
  border-radius: 20px;
  padding: 22px 24px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.35);
}
.csi-panel-label {
  text-transform: uppercase;
  letter-spacing: 0.22em;
  font-size: 9px;
  font-weight: 700;
  font-family: 'Inter', system-ui, sans-serif;
  color: var(--muted);
  margin-bottom: 14px;
}

/* ── verdict ring ── */
.csi-verdict-wrap { text-align: center; padding: 12px 0 18px; }
.csi-verdict-ring {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 130px;
  height: 130px;
  border-radius: 50%;
  border: 3px solid var(--amber);
  font-size: 44px;
  font-weight: 900;
  font-family: 'Inter', system-ui, sans-serif;
  color: var(--amber);
  margin-bottom: 12px;
}
.csi-verdict-label {
  font-size: 13px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.18em;
  font-family: 'Inter', system-ui, sans-serif;
  margin-bottom: 6px;
}
.csi-confidence-track {
  width: 100%;
  height: 8px;
  border-radius: 999px;
  background: rgba(255,255,255,0.07);
  overflow: hidden;
  margin: 8px 0 4px;
}
.csi-confidence-fill { height: 100%; border-radius: 999px; }

/* ── evidence board ── */
.csi-evidence-board { display: grid; gap: 8px; }
.csi-evidence-item {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 10px;
  align-items: start;
  padding: 10px 13px;
  border-radius: 12px;
  background: rgba(255,255,255,0.03);
  border-left: 3px solid var(--amber);
  border-top: 0.5px solid rgba(255,255,255,0.06);
  border-right: 0.5px solid rgba(255,255,255,0.06);
  border-bottom: 0.5px solid rgba(255,255,255,0.06);
  border-radius: 0 12px 12px 0;
}
.csi-evidence-tag {
  font-size: 9px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.14em;
  font-family: 'Inter', system-ui, sans-serif;
  padding: 3px 8px;
  border-radius: 999px;
  white-space: nowrap;
}
.tag-physical      { background: rgba(192,48,48,0.15); color: var(--red-hi); border: 1px solid rgba(192,48,48,0.3); }
.tag-witness       { background: rgba(74,154,170,0.15); color: var(--cyan);  border: 1px solid rgba(74,154,170,0.3); }
.tag-digital       { background: rgba(58,138,74,0.15);  color: var(--green); border: 1px solid rgba(58,138,74,0.3);  }
.tag-circumstantial{ background: rgba(212,168,67,0.10); color: var(--amber); border: 1px solid rgba(212,168,67,0.25);}
.csi-evidence-text { font-size: 13px; font-family: 'Inter', system-ui, sans-serif; color: var(--text); }

/* ── argument cards ── */
.csi-debate-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
.csi-arg-card {
  border-radius: 18px;
  padding: 18px 20px;
  background: rgba(255,255,255,0.03);
  font-family: 'Inter', system-ui, sans-serif;
  font-size: 13px;
  line-height: 1.6;
}
.arg-prosecution { border: 1px solid rgba(192,48,48,0.30); }
.arg-defense     { border: 1px solid rgba(74,154,170,0.28); }
.csi-arg-header {
  font-size: 10px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.20em;
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 1px solid rgba(255,255,255,0.07);
}
.header-prosecution { color: var(--red-hi); }
.header-defense     { color: var(--cyan); }

/* ── doubt list ── */
.csi-doubt-list { display: grid; gap: 8px; }
.csi-doubt {
  padding: 10px 14px;
  border-radius: 12px;
  background: rgba(74,154,170,0.06);
  border: 1px solid rgba(74,154,170,0.18);
  font-size: 13px;
  font-family: 'Inter', system-ui, sans-serif;
  color: var(--text);
}
.csi-doubt::before {
  content: "?";
  font-weight: 800;
  color: var(--cyan);
  margin-right: 8px;
}

/* ── key evidence ── */
.csi-key-evidence { display: grid; gap: 8px; }
.csi-key-item {
  padding: 10px 14px;
  border-radius: 12px;
  background: rgba(192,48,48,0.06);
  border: 1px solid rgba(192,48,48,0.20);
  font-size: 13px;
  font-family: 'Inter', system-ui, sans-serif;
  color: var(--text);
}

/* ── session history ── */
.csi-history { display: grid; gap: 7px; }
.csi-case-row {
  display: grid;
  grid-template-columns: 80px 1fr auto;
  gap: 12px;
  align-items: center;
  padding: 9px 13px;
  border-radius: 12px;
  background: rgba(255,255,255,0.02);
  border: 1px solid var(--border);
  font-family: 'Inter', system-ui, sans-serif;
  font-size: 12px;
}
.csi-case-verdict { font-weight: 700; font-size: 10px; text-transform: uppercase; letter-spacing: 0.12em; }
.csi-case-title   { color: var(--text); }
.csi-case-conf    { font-weight: 700; color: var(--amber); }

/* ── load panel ── */
.csi-load-panel {
  border-radius: 20px;
  padding: 20px 24px;
  background: rgba(212,168,67,0.05);
  border: 1px solid rgba(212,168,67,0.20);
  margin-bottom: 2px;
}
.csi-load-badge {
  display: inline-block;
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.16em;
  font-family: 'Inter', system-ui, sans-serif;
  padding: 3px 10px;
  border-radius: 999px;
  background: rgba(212,168,67,0.12);
  border: 1px solid rgba(212,168,67,0.28);
  color: var(--amber);
  margin-bottom: 12px;
}
.csi-loaded-banner {
  padding: 10px 16px;
  border-radius: 12px;
  background: rgba(58,138,74,0.10);
  border: 1px solid rgba(58,138,74,0.25);
  color: #5aba6a;
  font-size: 12px;
  font-family: 'Inter', system-ui, sans-serif;
  font-weight: 600;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  margin-bottom: 14px;
}

/* ── forensics card ── */
.csi-forensics {
  border-radius: 18px;
  padding: 18px 20px;
  background: rgba(58,138,74,0.05);
  border: 1px solid rgba(58,138,74,0.20);
  font-family: 'Inter', system-ui, sans-serif;
  font-size: 13px;
  line-height: 1.65;
  color: var(--text);
  white-space: pre-wrap;
}

/* ── summary ── */
.csi-summary-quote {
  border-radius: 18px;
  padding: 20px 24px;
  background: rgba(212,168,67,0.08);
  border: 1px solid rgba(212,168,67,0.22);
  font-style: italic;
  font-size: 16px;
  line-height: 1.6;
  color: var(--gold);
  text-align: center;
}

/* ── gradio overrides ── */
.gr-button-primary {
  background: linear-gradient(135deg, #7a2020, #5a1010) !important;
  border: none !important;
  border-radius: 12px !important;
  font-weight: 700 !important;
  font-family: 'Inter', system-ui, sans-serif !important;
  letter-spacing: 0.08em !important;
  padding: 12px 28px !important;
  color: #f0d090 !important;
  text-transform: uppercase !important;
  font-size: 12px !important;
}
.gr-button-secondary {
  background: rgba(212,168,67,0.08) !important;
  border: 1px solid rgba(212,168,67,0.28) !important;
  border-radius: 12px !important;
  font-weight: 700 !important;
  font-family: 'Inter', system-ui, sans-serif !important;
  letter-spacing: 0.08em !important;
  padding: 12px 28px !important;
  color: var(--amber) !important;
  text-transform: uppercase !important;
  font-size: 12px !important;
}
.gr-button-secondary:hover {
  background: rgba(212,168,67,0.15) !important;
  border-color: rgba(212,168,67,0.45) !important;
}
textarea, input[type=text] {
  background: rgba(18,14,22,0.95) !important;
  border: 1px solid var(--border) !important;
  color: var(--text) !important;
  border-radius: 12px !important;
  font-family: 'Inter', system-ui, sans-serif !important;
}
label > span {
  color: var(--muted) !important;
  font-size: 11px !important;
  text-transform: uppercase !important;
  letter-spacing: 0.14em !important;
  font-family: 'Inter', system-ui, sans-serif !important;
}
@media (max-width: 800px) { .csi-debate-grid { grid-template-columns: 1fr; } }
"""