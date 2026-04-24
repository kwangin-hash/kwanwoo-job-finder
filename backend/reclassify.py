# -*- coding: utf-8 -*-
"""
기존 DB 레코드 전부 재분류 (크롤 다시 안 돌리고 싶을 때 사용)
config.py 의 키워드 수정 후 돌리면 됨
"""
import sqlite3
from app.services import classifier

conn = sqlite3.connect("jobs.db")
c = conn.cursor()

rows = c.execute(
    "SELECT id, title, description, company FROM jobs"
).fetchall()

updated = 0
for row in rows:
    jid, title, desc, company = row
    category = classifier.classify(title, desc or "", company)
    entry = classifier.is_entry_level(title, desc or "")
    disqual = classifier.is_disqualified(title, desc or "")
    ms = classifier.match_score(title, desc or "", company, category)
    info = classifier.company_info(company)
    rs = classifier.realistic_score(company, title, desc or "", info, category)

    c.execute(
        """
        UPDATE jobs SET
          category=?, match_score=?, realistic_score=?,
          company_tier=?, is_target_company=?, is_hard_tier=?,
          is_entry_level=?, is_disqualified=?
        WHERE id=?
        """,
        (
            category, ms, rs,
            info["tier"], 1 if info["is_target"] else 0, 1 if info["is_hard"] else 0,
            1 if entry else 0, 1 if disqual else 0,
            jid,
        ),
    )
    updated += 1

conn.commit()
print(f"reclassified {updated} rows")
