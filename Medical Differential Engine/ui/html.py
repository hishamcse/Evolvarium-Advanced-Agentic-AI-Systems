HERO_HTML = """
<div class="mde-hero">
  <div class="mde-kicker">Cascading Bayesian Refinement &nbsp;·&nbsp; LangGraph + MCP + Ollama</div>
  <div class="mde-title">Medical <span>Differential</span> Engine</div>
  <div class="mde-subtitle">
    Symptoms enter as a signal. Five specialist agents cascade through a Bayesian
    probability pipeline — parsing features, scoring priors, probing rare diagnoses,
    mapping comorbidities, and weighing evidence — until the differential collapses
    to a ranked, confidence-scored clinical assessment.
  </div>
  <div class="mde-badge-row">
    <span class="mde-badge">Symptom Parser</span>
    <span class="mde-badge">Prior Scorer</span>
    <span class="mde-badge">Rare Disease Probe</span>
    <span class="mde-badge">Comorbidity Mapper</span>
    <span class="mde-badge">Evidence Weigher</span>
    <span class="mde-badge">Differential Ranker</span>
    <span class="mde-badge red">Bayesian cascade</span>
    <span class="mde-badge amber">Probability tree</span>
    <span class="mde-badge green">Session memory</span>
  </div>
</div>
"""

EMPTY_HTML = """
<div class="mde-panel">
  <div class="mde-empty">
    <div class="mde-empty-icon">⚕</div>
    <div>The differential engine is idle.</div>
    <div style="margin-top:6px;opacity:0.6">Submit a case to begin the Bayesian cascade.</div>
  </div>
</div>
"""

CASCADE_HTML = """
<div class="mde-panel" style="margin-bottom:16px">
  <div class="mde-panel-label">Bayesian cascade — 5 layers</div>
  <div class="mde-cascade">
    <div class="mde-cascade-step">
      <div class="mde-step-circle done">L0</div>
      <div class="mde-step-label">Symptom<br>Parser</div>
    </div>
    <div class="mde-cascade-line"></div>
    <div class="mde-cascade-step">
      <div class="mde-step-circle done">L1</div>
      <div class="mde-step-label">Prior<br>Scorer</div>
    </div>
    <div class="mde-cascade-line"></div>
    <div class="mde-cascade-step">
      <div class="mde-step-circle done">L2</div>
      <div class="mde-step-label">Rare<br>Probe</div>
    </div>
    <div class="mde-cascade-line"></div>
    <div class="mde-cascade-step">
      <div class="mde-step-circle done">L3</div>
      <div class="mde-step-label">Comorbidity<br>Mapper</div>
    </div>
    <div class="mde-cascade-line"></div>
    <div class="mde-cascade-step">
      <div class="mde-step-circle done">L4</div>
      <div class="mde-step-label">Evidence<br>Weigher</div>
    </div>
    <div class="mde-cascade-line"></div>
    <div class="mde-cascade-step">
      <div class="mde-step-circle done">L5</div>
      <div class="mde-step-label">Differential<br>Ranker</div>
    </div>
  </div>
</div>
"""