from __future__ import annotations

from typing import Any, Dict, List


class MomentumVisualizer:
    """Build visualization-friendly structures from idea activity data."""

    def generate_3d_trajectory(self, idea_data: Dict[str, Any]) -> Dict[str, Any]:
        timestamps = list(idea_data.get("timestamps", []))
        platform_data = idea_data.get("platform_data", {}) or {}
        platforms = list(platform_data.keys())
        platform_index = {name: idx for idx, name in enumerate(platforms)}

        points: List[Dict[str, Any]] = []
        connections: List[Dict[str, Any]] = []

        for p in platforms:
            series = list(platform_data.get(p, []))
            for i, t in enumerate(timestamps):
                z = float(series[i]) if i < len(series) else 0.0
                point = [float(t), float(platform_index[p]), z]
                points.append({"point": point, "platform": p, "mentions": z})
                if i > 0:
                    prev_z = float(series[i - 1]) if (i - 1) < len(series) else 0.0
                    connections.append(
                        {
                            "start": [float(timestamps[i - 1]), float(platform_index[p]), prev_z],
                            "end": point,
                            "platform": p,
                        }
                    )

        return {"points": points, "connections": connections}

    def build_influencer_network(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        influencers = metadata.get("influencers") or [
            {"id": "creator_1", "name": "Early Adopter", "followers": 25000, "influence_score": 0.72},
            {"id": "creator_2", "name": "Domain Expert", "followers": 54000, "influence_score": 0.83},
        ]
        edges = metadata.get("influencer_edges") or [
            {"source": influencers[0]["id"], "target": influencers[1]["id"], "weight": 0.64, "type": "amplifies"}
        ]
        return {"nodes": influencers, "edges": edges}

    def build_geographic_heatmap(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "locations": metadata.get("geo_locations")
            or [
                {"id": "US", "name": "United States", "latitude": 37.0902, "longitude": -95.7129, "mentions": 320, "sentiment": 0.62},
                {"id": "CA", "name": "Canada", "latitude": 56.1304, "longitude": -106.3468, "mentions": 120, "sentiment": 0.58},
            ]
        }

    def generate_visualization_data(self, idea_data: Dict[str, Any], metadata: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "3d_trajectory": self.generate_3d_trajectory(idea_data),
            "influencer_network": self.build_influencer_network(metadata),
            "geographic_heatmap": self.build_geographic_heatmap(metadata),
        }

