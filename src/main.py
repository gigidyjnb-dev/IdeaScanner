from typing import Any, Dict, List

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from src.data_processor import DataProcessor
from src.models import Idea, IdeaResponse

app = FastAPI(title="IdeaMiner API", version="1.0.0")

# Initialize our components
data_processor = DataProcessor()

def _build_responses(sample_ideas: List[Idea]) -> List[IdeaResponse]:
    responses: List[IdeaResponse] = []
    for idea in sample_ideas:
        try:
            insight = data_processor.generate_idea_insights(idea)
            responses.append(
                IdeaResponse(
                    idea=insight["idea"],
                    predictive_score=insight["predictive_score"],
                    idea_dna=insight["idea_dna"],
                    visualization_data=insight["visualization_data"],
                    incubation_simulation=insight["incubation_simulation"],
                )
            )
        except Exception as e:
            logger.exception("Error generating insights for idea %s", idea.id)
            raise HTTPException(status_code=500, detail=f"Insight generation failed: {e}") from e
    return responses

@app.get("/", response_class=HTMLResponse)
def read_root() -> str:
    return """
    <html>
      <head>
        <title>IdeaMiner Dashboard</title>
        <style>
          :root {
            --bg: #070b1a;
            --card: #111936;
            --card-2: #0f1530;
            --text: #e8eeff;
            --muted: #aab7e4;
            --accent: #5eead4;
            --accent-2: #60a5fa;
            --accent-3: #f472b6;
          }
          * { box-sizing: border-box; }
          body {
            margin: 0;
            font-family: Inter, ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
            color: var(--text);
            background: radial-gradient(900px 500px at 90% -10%, rgba(96,165,250,0.35), transparent 55%),
                        radial-gradient(700px 450px at -10% -20%, rgba(244,114,182,0.25), transparent 50%),
                        var(--bg);
          }
          .container { max-width: 1180px; margin: 0 auto; padding: 28px 18px 40px; }
          .hero {
            background: linear-gradient(120deg, rgba(94,234,212,0.14), rgba(96,165,250,0.18));
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 20px;
            padding: 28px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.35);
          }
          h1 { font-size: 2rem; margin: 0 0 10px; }
          .subtitle { margin: 0; color: var(--muted); font-size: 1.05rem; }
          .actions { display: flex; gap: 12px; flex-wrap: wrap; margin-top: 18px; }
          .btn {
            text-decoration: none;
            display: inline-block;
            border-radius: 10px;
            padding: 10px 14px;
            font-weight: 700;
            border: 1px solid transparent;
          }
          .btn-primary { background: linear-gradient(90deg, var(--accent), var(--accent-2)); color: #061022; }
          .btn-ghost { color: var(--text); border-color: rgba(255,255,255,0.25); }
          .grid { display: grid; grid-template-columns: repeat(12, 1fr); gap: 14px; margin-top: 18px; }
          .card {
            background: linear-gradient(180deg, rgba(255,255,255,0.04), rgba(255,255,255,0.02));
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 16px;
            padding: 16px;
          }
          .kpi { grid-column: span 3; }
          .kpi .label { color: var(--muted); font-size: 0.85rem; }
          .kpi .value { font-size: 1.45rem; font-weight: 800; margin-top: 4px; }
          .panel { grid-column: span 6; }
          .panel-wide { grid-column: span 12; }
          .list { margin: 0; padding-left: 18px; color: var(--muted); }
          .list li { margin-bottom: 6px; }
          .table { width: 100%; border-collapse: collapse; font-size: 0.94rem; }
          .table th, .table td { padding: 10px; border-bottom: 1px solid rgba(255,255,255,0.1); text-align: left; }
          .pill { padding: 2px 8px; border-radius: 999px; font-weight: 700; font-size: 0.75rem; }
          .pill-up { background: rgba(94,234,212,0.2); color: #5eead4; }
          .pill-mid { background: rgba(96,165,250,0.2); color: #93c5fd; }
          code { background: rgba(255,255,255,0.08); padding: 2px 6px; border-radius: 6px; color: #d1fae5; }
          .footer { color: var(--muted); margin-top: 18px; font-size: 0.9rem; }
          @media (max-width: 980px) {
            .kpi, .panel { grid-column: span 12; }
          }
        </style>
      </head>
      <body>
        <div class="container">
          <section class="hero">
            <h1>IdeaMiner Intelligence Dashboard</h1>
            <p class="subtitle">Bright, fast, and insight-driven. Track signals, identify breakout opportunities, and simulate go-to-market ideas in one place.</p>
            <div class="actions">
              <a class="btn btn-primary" href="/docs">Open API Console</a>
              <a class="btn btn-ghost" href="/ideas/current">Live Current Ideas</a>
              <a class="btn btn-ghost" href="/ideas/predictive">Predictive Feed</a>
            </div>
          </section>

          <section class="grid">
            <article class="card kpi"><div class="label">API Status</div><div class="value" id="kpi-status">Checking...</div></article>
            <article class="card kpi"><div class="label">Current Ideas</div><div class="value" id="kpi-current">--</div></article>
            <article class="card kpi"><div class="label">Predictive Ideas</div><div class="value" id="kpi-predictive">--</div></article>
            <article class="card kpi"><div class="label">Model Version</div><div class="value">v1.0.0</div></article>

            <article class="card panel">
              <h3>Capability Stack</h3>
              <ul class="list">
                <li>Predictive trend scoring across growth, sentiment, and engagement</li>
                <li>Idea DNA fingerprinting for audience and market-fit framing</li>
                <li>Momentum visualization with trajectory + geo + influencer layers</li>
                <li>Incubation simulations to estimate path and success probability</li>
              </ul>
            </article>

            <article class="card panel">
              <h3>Quick API Routes</h3>
              <ul class="list">
                <li><a href="/healthz">/healthz</a> and <a href="/readyz">/readyz</a></li>
                <li><a href="/ideas/current">/ideas/current</a></li>
                <li><a href="/ideas/predictive">/ideas/predictive</a></li>
                <li><a href="/ideas/visualization/idea_001">/ideas/visualization/{idea_id}</a></li>
                <li><code>POST /ideas/simulate</code></li>
              </ul>
            </article>

            <article class="card panel-wide">
              <h3>Current Ideas Snapshot</h3>
              <table class="table" id="ideas-table">
                <thead>
                  <tr><th>Idea</th><th>Predictive Score</th><th>Velocity</th><th>Sentiment</th><th>Signal</th></tr>
                </thead>
                <tbody><tr><td colspan="5">Loading…</td></tr></tbody>
              </table>
            </article>
          </section>

          <p class="footer">IdeaMiner API • Professional Dashboard Layer • Built for Render deployment</p>
        </div>

        <script>
          async function loadDashboard() {
            const statusEl = document.getElementById('kpi-status');
            const currentEl = document.getElementById('kpi-current');
            const predictiveEl = document.getElementById('kpi-predictive');
            const tableBody = document.querySelector('#ideas-table tbody');

            try {
              const health = await fetch('/healthz').then(r => r.json());
              statusEl.textContent = health.status === 'ok' ? 'Live' : 'Degraded';

              const current = await fetch('/ideas/current').then(r => r.json());
              const predictive = await fetch('/ideas/predictive').then(r => r.json());
              currentEl.textContent = String(current.length);
              predictiveEl.textContent = String(predictive.length);

              tableBody.innerHTML = '';
              current.slice(0, 6).forEach(item => {
                const idea = item.idea || {};
                const score = Number(item.predictive_score || 0).toFixed(2);
                const signal = item.predictive_score >= 0.75
                  ? '<span class="pill pill-up">Breakout</span>'
                  : '<span class="pill pill-mid">Emerging</span>';
                const row = document.createElement('tr');
                row.innerHTML = `
                  <td>${idea.title || 'Untitled'}</td>
                  <td>${score}</td>
                  <td>${Number(idea.velocity || 0).toFixed(1)}</td>
                  <td>${Number(idea.sentiment_score || 0).toFixed(2)}</td>
                  <td>${signal}</td>
                `;
                tableBody.appendChild(row);
              });

              if (!current.length) {
                tableBody.innerHTML = '<tr><td colspan="5">No current ideas available.</td></tr>';
              }
            } catch (e) {
              statusEl.textContent = 'Unavailable';
              tableBody.innerHTML = '<tr><td colspan="5">Dashboard data unavailable. Check API deployment status.</td></tr>';
            }
          }
          loadDashboard();
        </script>
      </body>
    </html>
    """


@app.get("/healthz")
def healthz() -> Dict[str, str]:
    return {"status": "ok"}


@app.get("/readyz")
def readyz() -> Dict[str, str]:
    return {"status": "ready"}

@app.get("/ideas/current")
def get_current_trending_ideas() -> List[IdeaResponse]:
    """
    Get the current top 10 ideas identified by the system
    """
    # In a real implementation, this would retrieve data from storage
    # For now, we'll use sample data
    sample_ideas = [
        Idea(
            id="idea_001",
            title="AI-Powered Personal Finance Assistant",
            description="An AI system that helps users manage personal finances by analyzing spending patterns and providing personalized saving recommendations.",
            sentiment_score=0.85,
            velocity=75.5,
            market_potential=0.9
        ),
        Idea(
            id="idea_002",
            title="Sustainable Packaging Solution",
            description="Biodegradable packaging materials made from agricultural waste that can decompose within 30 days.",
            sentiment_score=0.92,
            velocity=88.2,
            market_potential=0.85
        )
    ]

    return _build_responses(sample_ideas)


@app.get("/ideas/predictive")
def get_predictive_trends() -> List[IdeaResponse]:
    """
    Get ideas predicted to gain traction in the next 30-90 days
    """
    # In a real implementation, this would use the predictive engine with historical data
    # For now, we'll return the same sample ideas but with predictive scores
    sample_ideas = [
        Idea(
            id="idea_003",
            title="Mental Health Micro-Coaching Platform",
            description="A mobile app that provides personalized micro-coaching sessions throughout the day based on user mood tracking.",
            sentiment_score=0.78,
            velocity=65.2,
            market_potential=0.88
        ),
        Idea(
            id="idea_004",
            title="Hyperlocal Skill Sharing Network",
            description="A platform connecting neighbors to exchange services and skills without monetary transactions.",
            sentiment_score=0.82,
            velocity=72.1,
            market_potential=0.82
        )
    ]

    return _build_responses(sample_ideas)


@app.get("/ideas/visualization/{idea_id}")
def get_idea_visualization(idea_id: str):
    """
    Get 3D visualization data for how an idea moves across platforms
    """
    logger.info(f"Fetching visualization for idea ID: {idea_id}")
    idea = Idea(
        id=idea_id,
        title="Visualization Probe",
        description="Diagnostic visualization generation for an idea",
        sentiment_score=0.5,
        velocity=50.0,
        market_potential=0.7,
    )
    insight = data_processor.generate_idea_insights(idea)
    return {"idea_id": idea_id, **insight["visualization_data"]}

@app.post("/ideas/simulate")
def simulate_idea_incubation(idea: Idea):
    """
    Run the Idea Incubation Simulator for a given idea
    """
    insight = data_processor.generate_idea_insights(idea)
    return {
        "idea_id": idea.id,
        "concept": idea.title,
        "simulation": insight["incubation_simulation"],
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
