from typing import Any, Dict, List

from fastapi import FastAPI, HTTPException
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

@app.get("/")
def read_root():
    return {
        "message": "Welcome to IdeaMiner API - Discover what people want before they know it themselves!",
        "version": "1.0.0",
        "endpoints": {
            "/ideas/current": "Get the current top 10 ideas identified by the system",
            "/ideas/predictive": "Get ideas predicted to gain traction in the next 30-90 days",
            "/ideas/visualization/{idea_id}": "Get 3D visualization data for how an idea moves across platforms",
            "/ideas/simulate": "Run the Idea Incubation Simulator for a given idea"
        }
    }


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

