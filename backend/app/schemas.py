"""
Pydantic 스키마 — API 응답
"""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class JobOut(BaseModel):
    id: int
    source: str
    url: str
    company: str
    title: str
    location: Optional[str] = None
    posted_at: Optional[datetime] = None
    deadline: Optional[datetime] = None

    category: str
    match_score: float
    realistic_score: float

    company_tier: str
    is_target_company: int
    is_hard_tier: int
    is_entry_level: int

    class Config:
        from_attributes = True


class CategorySummary(BaseModel):
    category: str
    label: str
    total: int
    new_today: int
    top_jobs: List[JobOut]
