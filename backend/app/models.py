"""
DB 모델 — 채용 공고
"""
from __future__ import annotations
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, Text, Index
from app.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)

    # 출처
    source = Column(String(50), nullable=False)      # wanted / publicdata / saramin
    source_id = Column(String(100), nullable=False)   # 원 사이트의 공고 ID
    url = Column(String(500), nullable=False)

    # 공고 내용
    company = Column(String(200), nullable=False, index=True)
    title = Column(String(500), nullable=False)
    description = Column(Text)
    location = Column(String(200))

    # 일정
    posted_at = Column(DateTime)
    deadline = Column(DateTime, index=True)

    # 분류
    category = Column(String(50), index=True)         # PUBLIC / DATA / ROBOT_MFG / OTHER
    match_score = Column(Float, default=0.0)          # 직무 적합도 0 ~ 100
    realistic_score = Column(Float, default=0.0)      # 현실적 합격 가능성 0 ~ 100

    # 기업 티어 (실질적 합격 가능 기업 판정용)
    company_tier = Column(String(30), index=True)     # PUBLIC_LARGE / SI_MID 등
    is_target_company = Column(Integer, default=0)    # 1 = 화이트리스트 기업
    is_hard_tier = Column(Integer, default=0)         # 1 = 학벌 컷 예상 대기업

    # 메타
    is_entry_level = Column(Integer, default=0)       # 1 = 신입 친화
    is_disqualified = Column(Integer, default=0)      # 1 = 경력/석사 요구로 제외
    crawled_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index("ix_source_source_id", "source", "source_id", unique=True),
        Index("ix_category_score", "category", "match_score"),
    )
