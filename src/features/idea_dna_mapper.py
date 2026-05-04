from __future__ import annotations

from typing import Any, Dict, List


class DNAMapper:
    """Extract a compact 'idea DNA' profile from idea text + metadata."""

    def extract_idea_dna(self, idea_text: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        text = (idea_text or "").lower()
        urgency = self._score_urgency(text)
        complexity = self._score_complexity(text)

        audiences = metadata.get("audiences") or ["general"]
        locations = metadata.get("locations") or ["global"]
        engagement = float(metadata.get("engagement", 0.0))
        market_size = min(1.0, max(0.0, engagement / 1000.0))

        return {
            "problem": self._extract_problem_label(text),
            "solution_type": self._extract_solution_type(text),
            "target_audience": audiences,
            "urgency": urgency,
            "complexity": complexity,
            "market_size": market_size,
            "competition_level": self._estimate_competition(text),
            "geographical_scope": locations,
            "sentiment_profile": {
                "positive": float(metadata.get("sentiment_positive", 0.4)),
                "neutral": float(metadata.get("sentiment_neutral", 0.4)),
                "negative": float(metadata.get("sentiment_negative", 0.2)),
            },
            "platform_profile": metadata.get(
                "platform_profile",
                {"twitter": 0.35, "reddit": 0.25, "instagram": 0.2, "facebook": 0.2},
            ),
        }

    def _extract_problem_label(self, text: str) -> str:
        if any(k in text for k in ["expensive", "cost", "pricing"]):
            return "cost pressure"
        if any(k in text for k in ["slow", "time", "manual"]):
            return "workflow inefficiency"
        if any(k in text for k in ["hard", "difficult", "confusing"]):
            return "usability friction"
        return "general unmet need"

    def _extract_solution_type(self, text: str) -> str:
        if "app" in text or "mobile" in text:
            return "mobile app"
        if "platform" in text or "marketplace" in text:
            return "platform"
        if "automation" in text or "ai" in text:
            return "automation tool"
        return "software service"

    def _score_urgency(self, text: str) -> float:
        hits = sum(1 for k in ["urgent", "frustrated", "need", "asap", "pain"] if k in text)
        return min(1.0, 0.3 + hits * 0.15)

    def _score_complexity(self, text: str) -> float:
        hits = sum(1 for k in ["integration", "enterprise", "compliance", "security"] if k in text)
        return min(1.0, 0.2 + hits * 0.2)

    def _estimate_competition(self, text: str) -> float:
        crowded_hits = sum(1 for k in ["many tools", "saturated", "crowded", "competitive"] if k in text)
        return min(1.0, 0.35 + crowded_hits * 0.2)

