"""
FastAPI 메인 — 실질적 합격 가능 기업 중심 정렬
"""
from __future__ import annotations
from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from typing import List, Optional
from pathlib import Path
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, or_, and_
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from app.config import CATEGORIES, SON_PROFILE
from app.data.target_companies import TIER_LABELS
from app.database import Base, engine, get_db
from app.models import Job
from app.schemas import JobOut, CategorySummary
from app.services.ingest import run_ingest


scheduler = BackgroundScheduler()


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    scheduler.add_job(
        run_ingest,
        CronTrigger(hour=6, minute=0),
        id="daily_ingest",
        replace_existing=True,
    )
    scheduler.start()
    yield
    scheduler.shutdown()


app = FastAPI(
    title="Son Job Finder API",
    description="아들 취업 추천 — 실질적 합격 가능 기업 중심",
    version="0.2.0",
    lifespan=lifespan,
)


@app.get("/", response_class=HTMLResponse)
def home():
    """웹 대시보드 — 브라우저에서 공고 보기"""
    html_path = Path(__file__).resolve().parent / "static" / "index.html"
    return html_path.read_text(encoding="utf-8")


@app.get("/health")
def health():
    return {"status": "ok", "time": datetime.utcnow().isoformat()}


@app.get("/stats")
def stats(db: Session = Depends(get_db)):
    """대시보드 헤더용 — 마지막 크롤 시각, 총 건수, 오늘 신규 수"""
    from sqlalchemy import func as F
    last = db.query(F.max(Job.crawled_at)).scalar()
    total = db.query(F.count(Job.id)).scalar() or 0
    cutoff = datetime.utcnow() - timedelta(hours=24)
    new24 = (
        db.query(F.count(Job.id)).filter(Job.crawled_at >= cutoff).scalar() or 0
    )
    # 다음 크롤 예정: 오늘 06:00 지났으면 내일 06:00
    now = datetime.utcnow()
    next_6 = now.replace(hour=21, minute=0, second=0, microsecond=0)  # UTC 21:00 = KST 06:00
    if next_6 <= now:
        next_6 = next_6 + timedelta(days=1)
    return {
        "last_crawled_at": last.isoformat() if last else None,
        "total": total,
        "new_24h": new24,
        "next_scheduled_kst": "매일 06:00",
    }


@app.get("/profile")
def profile():
    return SON_PROFILE


@app.get("/tier-labels")
def tier_labels():
    """기업 티어 한글 라벨 — 앱 뱃지 표시용"""
    return TIER_LABELS


@app.post("/ingest/run")
def trigger_ingest():
    stats = run_ingest()
    return {"ok": True, "stats": stats}


# 다른 지역 키워드 — 이 중 하나라도 location에 포함되면 제외
NON_CAPITAL_REGIONS = [
    "부산", "대구", "광주", "인천", "울산", "대전", "세종",
    "강원", "충북", "충남", "전북", "전남", "경북", "경남", "제주",
    "원주", "춘천", "청주", "천안", "전주", "목포", "창원", "포항",
    "진주", "김해", "구미", "제천",
]


def _apply_region_filter(q, only_capital: bool):
    """
    서울/경기만 허용. location·title·company 3곳 모두에서 타 지역 키워드 제외.
    (location null이어도 title에 '부산교육청'이면 제외)
    """
    if not only_capital:
        return q
    for region in NON_CAPITAL_REGIONS:
        kw = f"%{region}%"
        q = q.filter(
            and_(
                or_(Job.location.is_(None), ~Job.location.like(kw)),
                ~Job.title.like(kw),
                ~Job.company.like(kw),
            )
        )
    return q


def _base_query(
    db: Session,
    category: Optional[str],
    only_realistic: bool,
    only_entry: bool,
    exclude_hard: bool,
    only_capital: bool = True,
):
    """공통 필터"""
    q = db.query(Job).filter(Job.is_disqualified == 0)
    if category:
        q = q.filter(Job.category == category)
    if only_realistic:
        # 4개 트랙(PUBLIC/SW_DEV/ROBOT_DEV/DATA_ANALYST) 중 하나로 분류된 공고만
        # OR 화이트리스트 기업은 OTHER 여도 예외 허용
        q = q.filter(
            (Job.is_target_company == 1)
            | (Job.category != "OTHER")
        )
    if only_entry:
        q = q.filter(Job.is_entry_level == 1)
    if exclude_hard:
        q = q.filter(Job.is_hard_tier == 0)
    q = _apply_region_filter(q, only_capital)
    now = datetime.utcnow()
    # 마감일 있으면 마감까지 유지
    # 마감일 없으면 마지막 크롤 후 14일까지만 유지(출처에서 내려간 공고 자동 숨김)
    stale_cutoff = now - timedelta(days=14)
    q = q.filter(
        or_(
            Job.deadline >= now,
            and_(Job.deadline.is_(None), Job.crawled_at >= stale_cutoff),
        )
    )
    return q


@app.get("/jobs", response_model=List[JobOut])
def list_jobs(
    category: Optional[str] = Query(None),
    only_realistic: bool = Query(True),
    only_entry: bool = Query(True),
    exclude_hard: bool = Query(True),
    only_capital: bool = Query(
        True, description="서울/경기만 (location 미상 포함)"
    ),
    tier: Optional[str] = Query(None),
    limit: int = Query(100, ge=1, le=300),
    db: Session = Depends(get_db),
):
    """공고 리스트. 기본: 서울/경기 + 신입 + 대기업 제외 + 실질 타겟."""
    q = _base_query(db, category, only_realistic, only_entry, exclude_hard, only_capital)
    if tier:
        q = q.filter(Job.company_tier == tier)
    q = q.order_by(
        desc(Job.realistic_score),
        desc(Job.match_score),
        desc(Job.posted_at),
    )
    return q.limit(limit).all()


@app.get("/jobs/today", response_model=List[JobOut])
def today_jobs(db: Session = Depends(get_db)):
    """오늘 신규 Top 20 — 아침 알림용 (실질 타겟 기업 우선)"""
    cutoff = datetime.utcnow() - timedelta(hours=24)
    q = (
        _base_query(db, None, True, True, True)
        .filter(Job.crawled_at >= cutoff)
        .order_by(desc(Job.realistic_score), desc(Job.match_score))
        .limit(20)
    )
    return q.all()


@app.get("/jobs/hard", response_model=List[JobOut])
def hard_tier_jobs(db: Session = Depends(get_db)):
    """
    대기업 공채 (학벌 컷 있음). 참고용.
    """
    q = (
        db.query(Job)
        .filter(Job.is_hard_tier == 1)
        .filter(Job.is_entry_level == 1)
        .filter(Job.is_disqualified == 0)
        .order_by(desc(Job.match_score), desc(Job.posted_at))
        .limit(30)
    )
    now = datetime.utcnow()
    q = q.filter((Job.deadline.is_(None)) | (Job.deadline >= now))
    return q.all()


@app.get("/summary", response_model=List[CategorySummary])
def summary(db: Session = Depends(get_db)):
    """3개 트랙 요약 — 실질적 기업만 카운트"""
    cutoff = datetime.utcnow() - timedelta(hours=24)
    now = datetime.utcnow()
    result = []

    for key, meta in CATEGORIES.items():
        base = (
            db.query(Job)
            .filter(Job.category == key)
            .filter(Job.is_disqualified == 0)
            .filter(Job.is_hard_tier == 0)
            .filter(Job.is_entry_level == 1)
            .filter(
                (Job.is_target_company == 1)
                | (Job.realistic_score >= 45)
                | (Job.category != "OTHER")
            )
            .filter((Job.deadline.is_(None)) | (Job.deadline >= now))
        )
        base = _apply_region_filter(base, True)
        total = base.with_entities(func.count(Job.id)).scalar() or 0
        new_today = (
            base.filter(Job.crawled_at >= cutoff)
            .with_entities(func.count(Job.id))
            .scalar()
            or 0
        )
        top = (
            base.order_by(desc(Job.realistic_score), desc(Job.match_score))
            .limit(3)
            .all()
        )
        result.append(
            CategorySummary(
                category=key,
                label=meta["label"],
                total=total,
                new_today=new_today,
                top_jobs=[JobOut.model_validate(j) for j in top],
            )
        )

    return result


@app.get("/jobs/{job_id}", response_model=JobOut)
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(404, "Job not found")
    return job
