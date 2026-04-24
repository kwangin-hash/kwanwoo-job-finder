"""
크롤러 실행 → 분류 → DB upsert (기업 티어·현실성 점수 포함)
"""
from __future__ import annotations
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.dialects.sqlite import insert as sqlite_insert
from app.crawlers import ALL_CRAWLERS
from app.database import SessionLocal
from app.models import Job
from app.services import classifier


def run_ingest() -> dict:
    stats: dict[str, dict] = {}
    db: Session = SessionLocal()

    try:
        for CrawlerCls in ALL_CRAWLERS:
            crawler = CrawlerCls()
            try:
                fetched = crawler.fetch()
            except Exception as e:
                stats[CrawlerCls.source] = {"fetched": 0, "new": 0, "error": str(e)[:200]}
                continue
            new_count = 0

            for item in fetched:
                category = classifier.classify(
                    item["title"], item.get("description", ""), item["company"]
                )
                entry = classifier.is_entry_level(
                    item["title"], item.get("description", "")
                )
                disqual = classifier.is_disqualified(
                    item["title"], item.get("description", "")
                )
                ms = classifier.match_score(
                    item["title"],
                    item.get("description", ""),
                    item["company"],
                    category,
                )
                info = classifier.company_info(item["company"])
                rs = classifier.realistic_score(
                    item["company"],
                    item["title"],
                    item.get("description", ""),
                    info,
                    category,
                )

                values = {
                    "source": crawler.source,
                    "source_id": item["source_id"],
                    "url": item["url"],
                    "company": item["company"],
                    "title": item["title"],
                    "description": item.get("description", ""),
                    "location": item.get("location"),
                    "posted_at": item.get("posted_at"),
                    "deadline": item.get("deadline"),
                    "category": category,
                    "match_score": ms,
                    "realistic_score": rs,
                    "company_tier": info["tier"],
                    "is_target_company": 1 if info["is_target"] else 0,
                    "is_hard_tier": 1 if info["is_hard"] else 0,
                    "is_entry_level": 1 if entry else 0,
                    "is_disqualified": 1 if disqual else 0,
                    "crawled_at": datetime.utcnow(),
                }

                stmt = sqlite_insert(Job).values(**values)
                stmt = stmt.on_conflict_do_update(
                    index_elements=["source", "source_id"],
                    set_={
                        "title": values["title"],
                        "description": values["description"],
                        "deadline": values["deadline"],
                        "category": values["category"],
                        "match_score": values["match_score"],
                        "realistic_score": values["realistic_score"],
                        "company_tier": values["company_tier"],
                        "is_target_company": values["is_target_company"],
                        "is_hard_tier": values["is_hard_tier"],
                        "is_entry_level": values["is_entry_level"],
                        "is_disqualified": values["is_disqualified"],
                        "crawled_at": values["crawled_at"],
                    },
                )
                result = db.execute(stmt)
                if result.rowcount == 1 and result.lastrowid:
                    new_count += 1

            db.commit()
            stats[crawler.source] = {
                "fetched": len(fetched),
                "new": new_count,
            }
    finally:
        db.close()

    return stats
