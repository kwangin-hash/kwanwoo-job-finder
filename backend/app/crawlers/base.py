"""
크롤러 공통 베이스 클래스.
각 크롤러는 fetch() → List[dict] 반환.
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional


class BaseCrawler(ABC):
    source: str = "unknown"

    @abstractmethod
    def fetch(self) -> list[dict]:
        """
        공고 dict 리스트 반환. 각 dict 키:
          source_id, url, company, title, description, location,
          posted_at, deadline (datetime or None)
        """
        ...

    @staticmethod
    def parse_dt(raw: Optional[str]) -> Optional[datetime]:
        if not raw:
            return None
        try:
            return datetime.fromisoformat(raw.replace("Z", "+00:00"))
        except (ValueError, AttributeError):
            return None
