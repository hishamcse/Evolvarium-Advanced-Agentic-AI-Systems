APP_CSS = """
:root {
  --launch-bg: radial-gradient(circle at top left, #16211b 0%, #0c1311 42%, #060908 100%);
  --launch-panel: rgba(10, 16, 14, 0.86);
  --launch-panel-soft: rgba(128, 255, 203, 0.08);
  --launch-border: rgba(137, 255, 204, 0.18);
  --launch-text: #eef8f2;
  --launch-muted: #a9b9b0;
  --launch-mint: #89ffcc;
  --launch-amber: #ffbf69;
  --launch-red: #ff7979;
}
.gradio-container {
  background: var(--launch-bg);
  color: var(--launch-text);
}
.launch-shell {
  border-radius: 24px;
  border: 1px solid rgba(255,255,255,0.08);
  background: linear-gradient(180deg, rgba(255,255,255,0.03), rgba(255,255,255,0.01));
  box-shadow: 0 24px 60px rgba(0, 0, 0, 0.32);
}
.launch-panel {
  background: var(--launch-panel);
  border: 1px solid var(--launch-border);
  border-radius: 20px;
  padding: 16px 18px;
  box-shadow: 0 14px 42px rgba(0,0,0,0.24);
}
.launch-hero {
  background:
    radial-gradient(circle at top right, rgba(137, 255, 204, 0.14), transparent 30%),
    radial-gradient(circle at bottom left, rgba(255, 191, 105, 0.12), transparent 26%),
    linear-gradient(140deg, rgba(20,90,67,0.30), rgba(10,16,14,0.88));
}
.launch-kicker {
  text-transform: uppercase;
  letter-spacing: 0.18em;
  font-size: 11px;
  color: var(--launch-mint);
  margin-bottom: 10px;
}
.launch-title {
  font-size: 32px;
  line-height: 1.08;
  margin: 0 0 8px 0;
}
.launch-subtitle {
  color: var(--launch-muted);
  margin-bottom: 14px;
}
.launch-chip-row {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
.launch-chip {
  border-radius: 999px;
  padding: 6px 10px;
  font-size: 12px;
  background: rgba(137, 255, 204, 0.08);
  border: 1px solid rgba(137, 255, 204, 0.18);
}
.launch-grid-2 {
  display: grid;
  grid-template-columns: 1.25fr 0.95fr;
  gap: 16px;
}
.launch-metric {
  border-radius: 18px;
  padding: 16px;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.08);
}
.launch-metric-big {
  font-size: 38px;
  font-weight: 800;
  color: var(--launch-amber);
}
.launch-mini-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
  margin-top: 14px;
}
.launch-mini-metric {
  border-radius: 14px;
  padding: 10px 12px;
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.08);
  display: flex;
  justify-content: space-between;
  gap: 10px;
  font-size: 12px;
}
.launch-mini-metric strong {
  color: var(--launch-mint);
}
.launch-card-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}
.launch-card {
  border-radius: 18px;
  padding: 14px;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.08);
}
.launch-card-title {
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.14em;
  color: var(--launch-muted);
  margin-bottom: 8px;
}
.launch-card strong {
  color: var(--launch-mint);
}
.launch-secondary-line {
  color: var(--launch-muted);
  margin-bottom: 12px;
}
.launch-list {
  display: grid;
  gap: 12px;
}
.launch-list-item {
  border-radius: 18px;
  padding: 14px;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.08);
}
.launch-signal-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
}
.launch-signal-card {
  border-radius: 18px;
  padding: 14px;
  background: linear-gradient(180deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02));
  border: 1px solid rgba(255,255,255,0.08);
}
.launch-signal-value {
  font-size: 28px;
  font-weight: 800;
  color: var(--launch-amber);
  margin-bottom: 10px;
}
.launch-signal-track {
  width: 100%;
  height: 10px;
  border-radius: 999px;
  background: rgba(255,255,255,0.08);
  overflow: hidden;
}
.launch-signal-fill {
  height: 100%;
  border-radius: 999px;
  background: linear-gradient(90deg, var(--launch-mint), var(--launch-amber));
}
.launch-channel-row {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}
.launch-channel-pill {
  border-radius: 999px;
  padding: 12px 14px;
  background:
    radial-gradient(circle at top left, rgba(137,255,204,0.16), transparent 45%),
    rgba(255,255,255,0.04);
  border: 1px solid rgba(137,255,204,0.22);
  min-width: 140px;
  text-align: center;
}
.launch-proof-board {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}
.launch-proof-item {
  border-radius: 18px;
  padding: 16px;
  background:
    linear-gradient(135deg, rgba(255,191,105,0.12), rgba(137,255,204,0.04)),
    rgba(255,255,255,0.03);
  border: 1px solid rgba(255,191,105,0.16);
}
.launch-operator-hero {
  background:
    radial-gradient(circle at top right, rgba(255,191,105,0.12), transparent 30%),
    radial-gradient(circle at bottom left, rgba(137,255,204,0.12), transparent 34%),
    linear-gradient(145deg, rgba(16,26,23,0.94), rgba(10,16,14,0.90));
}
.launch-operator-title {
  font-size: 28px;
  font-weight: 800;
  line-height: 1.1;
  margin-bottom: 10px;
}
.launch-next-action {
  margin-top: 16px;
  border-radius: 16px;
  padding: 14px 16px;
  background: rgba(137,255,204,0.08);
  border: 1px solid rgba(137,255,204,0.18);
  color: var(--launch-text);
}
.launch-log {
  display: grid;
  gap: 10px;
}
.launch-log-item {
  display: grid;
  grid-template-columns: 120px 1fr;
  gap: 12px;
}
.launch-log-actor {
  border-radius: 14px;
  padding: 10px;
  text-align: center;
  background: rgba(137, 255, 204, 0.08);
  border: 1px solid rgba(137, 255, 204, 0.16);
  font-size: 12px;
}
.launch-log-body {
  border-radius: 16px;
  padding: 12px 14px;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.08);
}
.launch-empty {
  color: var(--launch-muted);
  font-style: italic;
}
@media (max-width: 980px) {
  .launch-grid-2,
  .launch-card-grid,
  .launch-signal-grid,
  .launch-proof-board,
  .launch-mini-grid {
    grid-template-columns: 1fr;
  }
}
"""
