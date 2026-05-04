from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List


class BaseScraper(ABC):
    """Base contract for all source scrapers."""

    source_name: str = "unknown"

    @abstractmethod
    def scrape(self, query: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Scrape normalized items for a query."""

    @abstractmethod
    def authenticate(self, credentials: Dict[str, str]) -> bool:
        """Authenticate scraper with source provider."""

    def preprocess_text(self, text: str) -> str:
        return " ".join((text or "").split())


class MockCommunityScraper(BaseScraper):
    """Offline-safe scraper that returns realistic sample pain points."""

    source_name = "mock-community"

    def authenticate(self, credentials: Dict[str, str]) -> bool:
        return True

    def scrape(self, query: str, limit: int = 100) -> List[Dict[str, Any]]:
        seed = [
            {
                "source": self.source_name,
                "query": query,
                "title": f"People are frustrated with {query} workflows",
                "text": f"I wish there was a better way to solve {query} quickly for small teams.",
                "url": "https://example.com/post/1",
                "metadata": {"sentiment_hint": -0.2, "engagement": 120},
            },
            {
                "source": self.source_name,
                "query": query,
                "title": f"Need easier {query} automation",
                "text": f"Current {query} tools are too expensive and difficult to configure.",
                "url": "https://example.com/post/2",
                "metadata": {"sentiment_hint": -0.1, "engagement": 95},
            },
            {
                "source": self.source_name,
                "query": query,
                "title": f"Love the concept, hate execution for {query}",
                "text": f"Users want an affordable service around {query} with clear onboarding.",
                "url": "https://example.com/post/3",
                "metadata": {"sentiment_hint": 0.1, "engagement": 140},
            },
        ]
        return seed[: max(1, min(limit, len(seed)))]

