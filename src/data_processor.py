from __future__ import annotations

from typing import Any, Dict, List

from src.features.idea_dna_mapper import DNAMapper
from src.features.idea_incubator import IdeaIncubator
from src.features.momentum_visualizer import MomentumVisualizer
from src.features.predictive_trend_engine import PredictiveTrendEngine
from src.models import Idea


class DataProcessor:
    """Compose feature engines into one API-facing insight pipeline."""

    def __init__(self) -> None:
        self.predictive_engine = PredictiveTrendEngine()
        self.dna_mapper = DNAMapper()
        self.visualizer = MomentumVisualizer()
        self.incubator = IdeaIncubator()

    def process_raw_data(self, raw_data: List[Dict[str, Any]]) -> List[Idea]:
        ideas: List[Idea] = []
        for idx, item in enumerate(raw_data):
            text = item.get("text") or item.get("description") or ""
            sentiment = float(item.get("sentiment_score", item.get("metadata", {}).get("sentiment_hint", 0.0)))
            velocity = float(item.get("velocity", item.get("metadata", {}).get("engagement", 50.0)))

            ideas.append(
                Idea(
                    id=str(item.get("id", f"idea_{idx + 1:03d}")),
                    title=str(item.get("title", "Untitled Idea")),
                    description=str(text),
                    sentiment_score=max(-1.0, min(1.0, sentiment)),
                    velocity=max(0.0, velocity),
                    market_potential=max(0.0, min(1.0, float(item.get("market_potential", 0.6)))),
                )
            )
        return ideas

    def rank_top_ideas(self, ideas: List[Idea], limit: int = 10) -> List[Idea]:
        ranked = sorted(
            ideas,
            key=lambda x: (x.velocity * 0.6 + x.market_potential * 0.25 + (x.sentiment_score + 1) * 0.15),
            reverse=True,
        )
        return ranked[:limit]

    def generate_idea_insights(self, idea: Idea) -> Dict[str, Any]:
        trend_data = [
            {
                "id": idea.id,
                "topic": idea.title,
                "current_volume": idea.velocity * 10,
                "previous_volume": idea.velocity * 8,
                "current_sentiment": idea.sentiment_score,
                "previous_sentiment": idea.sentiment_score * 0.9,
                "engagements": idea.velocity * 6,
                "platforms": ["twitter", "reddit", "instagram"],
                "locations": ["US", "CA", "UK"],
            }
        ]

        predictive_score = self.predictive_engine.predict_trend_potential(trend_data)[0]

        metadata = {
            "engagement": idea.velocity * 10,
            "locations": ["US", "CA", "UK"],
            "audiences": ["consumers", "small-business"],
            "sentiment_positive": max(0.0, (idea.sentiment_score + 1.0) / 2.0),
            "sentiment_neutral": 0.3,
            "sentiment_negative": max(0.0, 1.0 - ((idea.sentiment_score + 1.0) / 2.0) - 0.3),
        }

        idea_dna = self.dna_mapper.extract_idea_dna(idea.description, metadata)

        idea_data = {
            "timestamps": list(range(8)),
            "platform_data": {
                "twitter": [i * idea.velocity * 1.0 for i in range(8)],
                "reddit": [i * idea.velocity * 0.8 for i in range(8)],
                "instagram": [i * idea.velocity * 0.6 for i in range(8)],
            },
        }
        visualization_data = self.visualizer.generate_visualization_data(idea_data, metadata)
        incubation_simulation = self.incubator.simulate(idea.model_dump())

        return {
            "idea": idea,
            "predictive_score": predictive_score,
            "idea_dna": idea_dna,
            "visualization_data": visualization_data,
            "incubation_simulation": incubation_simulation,
        }

