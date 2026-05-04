from dataclasses import dataclass, field
from typing import List


@dataclass
class Settings:
    app_name: str = "IdeaMiner"
    version: str = "1.0.0"
    description: str = "Discover what people want before they know it themselves!"
    host: str = "0.0.0.0"
    port: int = 8000
    top_k_ideas: int = 10
    default_queries: List[str] = field(
        default_factory=lambda: [
            "problem",
            "need",
            "wish",
            "frustrated",
            "annoying",
            "would be nice",
            "missing",
            "better way",
            "solution",
        ]
    )


settings = Settings()

