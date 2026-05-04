from __future__ import annotations

from typing import Any, Dict, List


class PredictiveTrendEngine:
    """Deterministic trend scoring engine for MVP use-cases."""

    def predict_trend_potential(self, trend_data: List[Dict[str, Any]]) -> List[float]:
        scores: List[float] = []
        for item in trend_data:
            current_volume = float(item.get("current_volume", 0.0))
            previous_volume = float(item.get("previous_volume", 0.0))
            current_sentiment = float(item.get("current_sentiment", 0.0))
            previous_sentiment = float(item.get("previous_sentiment", 0.0))
            engagements = float(item.get("engagements", 0.0))
            platforms = item.get("platforms", []) or []
            locations = item.get("locations", []) or []

            volume_growth = max(0.0, current_volume - previous_volume)
            sentiment_delta = max(-1.0, min(1.0, current_sentiment - previous_sentiment))
            engagement_rate = engagements / max(current_volume, 1.0)
            diversity = min(1.0, len(platforms) / 6.0)
            geography = min(1.0, len(locations) / 10.0)

            raw = (
                0.35 * min(1.0, volume_growth / 1000.0)
                + 0.25 * ((current_sentiment + 1.0) / 2.0)
                + 0.15 * ((sentiment_delta + 1.0) / 2.0)
                + 0.15 * min(1.0, engagement_rate)
                + 0.05 * diversity
                + 0.05 * geography
            )
            scores.append(max(0.0, min(1.0, raw)))
        return scores

    def identify_emerging_trends(
        self, trend_data: List[Dict[str, Any]], threshold: float = 0.7
    ) -> List[Dict[str, Any]]:
        predictions = self.predict_trend_potential(trend_data)
        emerging: List[Dict[str, Any]] = []
        for i, trend in enumerate(trend_data):
            score = predictions[i]
            if score >= threshold:
                enriched = dict(trend)
                enriched["predicted_popularity"] = score
                emerging.append(enriched)
        return sorted(emerging, key=lambda x: x["predicted_popularity"], reverse=True)

