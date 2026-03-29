APP_CSS = """
:root {
  --arena-bg: radial-gradient(circle at top left, #16223f 0%, #0b1220 38%, #070b13 100%);
  --arena-panel: rgba(8, 13, 23, 0.86);
  --arena-panel-soft: rgba(52, 110, 255, 0.10);
  --arena-border: rgba(96, 168, 255, 0.24);
  --arena-text: #edf3ff;
  --arena-muted: #9bb2d1;
  --arena-cyan: #6be4ff;
  --arena-gold: #ffc765;
  --arena-red: #ff6d72;
  --arena-green: #78f3a9;
}
.gradio-container {
  background: var(--arena-bg);
  color: var(--arena-text);
}
.arena-shell {
  border-radius: 24px;
  border: 1px solid rgba(255,255,255,0.08);
  background: linear-gradient(180deg, rgba(255,255,255,0.03), rgba(255,255,255,0.01));
  box-shadow: 0 24px 60px rgba(0, 0, 0, 0.32);
}
.arena-panel {
  background: var(--arena-panel);
  border: 1px solid var(--arena-border);
  border-radius: 20px;
  padding: 16px 18px;
  box-shadow: 0 14px 42px rgba(0,0,0,0.24);
}
.arena-hero {
  background:
    radial-gradient(circle at top right, rgba(107, 228, 255, 0.16), transparent 30%),
    radial-gradient(circle at bottom left, rgba(255, 199, 101, 0.14), transparent 26%),
    linear-gradient(140deg, rgba(52,110,255,0.18), rgba(8,13,23,0.88));
}
.arena-kicker {
  text-transform: uppercase;
  letter-spacing: 0.18em;
  font-size: 11px;
  color: var(--arena-cyan);
  margin-bottom: 10px;
}
.arena-title {
  font-size: 32px;
  line-height: 1.08;
  margin: 0 0 8px 0;
}
.arena-subtitle {
  color: var(--arena-muted);
  margin-bottom: 14px;
}
.arena-chip-row {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
.arena-chip {
  border-radius: 999px;
  padding: 6px 10px;
  font-size: 12px;
  background: rgba(107, 228, 255, 0.10);
  border: 1px solid rgba(107, 228, 255, 0.20);
}
.arena-split {
  display: grid;
  grid-template-columns: 1.3fr 0.9fr;
  gap: 16px;
}
.arena-scoreboard {
  display: grid;
  gap: 12px;
  align-content: start;
}
.arena-score-big {
  font-size: 42px;
  font-weight: 800;
  color: var(--arena-gold);
}
.arena-score-meta {
  color: var(--arena-muted);
}
.arena-meter {
  margin-top: 10px;
}
.arena-meter-track {
  width: 100%;
  height: 12px;
  border-radius: 999px;
  overflow: hidden;
  background: rgba(255,255,255,0.08);
}
.arena-meter-fill {
  height: 100%;
  border-radius: 999px;
  background: linear-gradient(90deg, var(--arena-cyan), var(--arena-gold));
}
.arena-pressure-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 14px;
  align-items: end;
  min-height: 230px;
}
.arena-pressure-col {
  display: grid;
  gap: 10px;
  justify-items: center;
}
.arena-pressure-bar {
  width: 100%;
  min-height: 140px;
  border-radius: 18px;
  border: 1px solid rgba(255,255,255,0.08);
  background: linear-gradient(180deg, rgba(255,255,255,0.04), rgba(255,255,255,0.02));
  display: flex;
  align-items: end;
  overflow: hidden;
}
.arena-pressure-fill {
  width: 100%;
  background: linear-gradient(180deg, rgba(107,228,255,0.94), rgba(255,109,114,0.94));
  border-radius: 18px 18px 0 0;
}
.arena-pressure-label {
  font-size: 12px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--arena-muted);
}
.arena-pressure-value {
  font-size: 22px;
  font-weight: 800;
}
.arena-battlefield {
  position: relative;
  min-height: 260px;
  overflow: hidden;
  border-radius: 22px;
  border: 1px solid rgba(255,255,255,0.08);
  background:
    radial-gradient(circle at center, rgba(107,228,255,0.12), transparent 26%),
    linear-gradient(180deg, rgba(255,255,255,0.03), rgba(255,255,255,0.01));
}
.arena-battlefield-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 14px;
  padding: 18px;
}
.arena-zone {
  min-height: 160px;
  border-radius: 18px;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.08);
  padding: 12px;
}
.arena-zone-name {
  font-weight: 800;
  margin-bottom: 8px;
}
.arena-zone-tag {
  display: inline-block;
  margin-bottom: 10px;
  padding: 4px 8px;
  border-radius: 999px;
  font-size: 11px;
  background: rgba(255,199,101,0.12);
  border: 1px solid rgba(255,199,101,0.20);
  color: var(--arena-gold);
}
.arena-zone-note {
  color: var(--arena-muted);
  font-size: 13px;
  line-height: 1.4;
}
.arena-stage {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  gap: 14px;
  align-items: center;
}
.arena-column-title {
  text-transform: uppercase;
  letter-spacing: 0.16em;
  font-size: 11px;
  color: var(--arena-muted);
  margin-bottom: 8px;
}
.arena-pill-stack {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
.arena-pill {
  border-radius: 14px;
  padding: 9px 12px;
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.10);
}
.arena-stage-core {
  width: 170px;
  height: 170px;
  border-radius: 50%;
  display: grid;
  place-items: center;
  text-align: center;
  padding: 18px;
  background:
    radial-gradient(circle at center, rgba(107,228,255,0.18), rgba(255,199,101,0.10) 60%, rgba(8,13,23,0.88));
  border: 1px solid rgba(107,228,255,0.26);
  box-shadow: inset 0 0 28px rgba(107,228,255,0.12);
}
.arena-core-kicker {
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.18em;
  color: var(--arena-cyan);
}
.arena-core-title {
  font-size: 18px;
  font-weight: 800;
  margin: 6px 0;
}
.arena-core-meta {
  color: var(--arena-muted);
  font-size: 12px;
}
.arena-lanes {
  display: grid;
  gap: 12px;
}
.arena-lane {
  display: grid;
  grid-template-columns: 88px 1fr;
  gap: 12px;
  align-items: start;
}
.arena-lane-clock {
  border-radius: 16px;
  padding: 14px 10px;
  text-align: center;
  background: rgba(107,228,255,0.08);
  border: 1px solid rgba(107,228,255,0.18);
  font-weight: 700;
}
.arena-lane-card {
  border-radius: 16px;
  padding: 14px;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.08);
}
.arena-lane-title {
  font-weight: 700;
  margin-bottom: 6px;
}
.arena-comms {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}
.arena-comms-bubble {
  border-radius: 18px;
  padding: 14px;
  background: linear-gradient(160deg, rgba(107,228,255,0.10), rgba(255,255,255,0.04));
  border: 1px solid rgba(107,228,255,0.18);
}
.arena-comms-label {
  text-transform: uppercase;
  letter-spacing: 0.14em;
  font-size: 11px;
  color: var(--arena-cyan);
  margin-bottom: 8px;
}
.arena-plan {
  display: grid;
  gap: 14px;
}
.arena-plan-hero {
  border-radius: 20px;
  padding: 18px;
  background: linear-gradient(135deg, rgba(255,199,101,0.16), rgba(107,228,255,0.08));
  border: 1px solid rgba(255,199,101,0.18);
}
.arena-plan-headline {
  font-size: 24px;
  font-weight: 800;
  margin-bottom: 8px;
}
.arena-plan-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}
.arena-plan-card {
  border-radius: 16px;
  padding: 14px;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.08);
}
.arena-plan-label {
  text-transform: uppercase;
  letter-spacing: 0.14em;
  font-size: 11px;
  color: var(--arena-muted);
  margin-bottom: 8px;
}
.arena-timeline {
  display: grid;
  gap: 10px;
}
.arena-timeline-item {
  display: grid;
  grid-template-columns: 96px 1fr;
  gap: 12px;
  align-items: start;
}
.arena-timeline-actor {
  border-radius: 14px;
  padding: 10px;
  background: rgba(107,228,255,0.08);
  border: 1px solid rgba(107,228,255,0.16);
  text-align: center;
  font-size: 12px;
}
.arena-timeline-card {
  border-radius: 16px;
  padding: 12px 14px;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.08);
}
.arena-timeline-card p,
.arena-timeline-card ul,
.arena-timeline-card h1,
.arena-timeline-card h2,
.arena-timeline-card h3,
.arena-timeline-card h4 {
  margin: 0 0 10px 0;
}
.arena-timeline-card ul {
  padding-left: 18px;
}
.arena-timeline-card li {
  margin-bottom: 6px;
}
.arena-timeline-card strong {
  color: var(--arena-cyan);
}
.arena-empty {
  color: var(--arena-muted);
  font-style: italic;
}
@media (max-width: 980px) {
  .arena-split,
  .arena-stage,
  .arena-comms,
  .arena-plan-grid {
    grid-template-columns: 1fr;
  }
  .arena-battlefield-grid {
    grid-template-columns: 1fr;
  }
}
"""