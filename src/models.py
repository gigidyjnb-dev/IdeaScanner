from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class Idea(BaseModel):
    id: str
    title: str
    description: str
    sentiment_score: float = Field(ge=-1.0, le=1.0)
    velocity: float = Field(ge=0.0)
    market_potential: float = Field(ge=0.0, le=1.0)


class IdeaResponse(BaseModel):
    idea: Idea
    predictive_score: float
    idea_dna: Dict[str, Any]
    visualization_data: Dict[str, Any]
    incubation_simulation: Dict[str, Any]


class ScrapedItem(BaseModel):
    source: str
    query: str
    title: str
    text: str
    url: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class PipelineResult(BaseModel):
    ideas: List[IdeaResponse]
