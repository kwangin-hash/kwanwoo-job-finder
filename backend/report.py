# -*- coding: utf-8 -*-
"""Top 실질 타겟 공고 리포트를 UTF-8 파일로 출력"""
import sqlite3

conn = sqlite3.connect("jobs.db")
c = conn.cursor()

lines = []
lines.append("=" * 60)
lines.append("   아들 취업찾기 — 실질 타겟 공고 리포트")
lines.append("   (로봇 제거, 자격증+학력 스펙 기반 실질 4트랙)")
lines.append("=" * 60)
lines.append("")

total = c.execute("SELECT COUNT(*) FROM jobs").fetchone()[0]
entry = c.execute("SELECT COUNT(*) FROM jobs WHERE is_entry_level=1").fetchone()[0]
target = c.execute("SELECT COUNT(*) FROM jobs WHERE is_target_company=1").fetchone()[0]
lines.append(f"총 수집             : {total}건")
lines.append(f"신입 친화           : {entry}건")
lines.append(f"화이트리스트 기업   : {target}건")
lines.append("")

lines.append("--- 트랙별 (신입 + 카테고리 매칭) ---")
for row in c.execute(
    "SELECT category, COUNT(*) FROM jobs "
    "WHERE is_entry_level=1 AND category!='OTHER' "
    "GROUP BY category ORDER BY COUNT(*) DESC"
):
    lines.append(f"  {row[0]:14} : {row[1]}건")
lines.append("")

lines.append("=" * 60)
lines.append("  Top 20 실질 타겟 공고 (현실성 점수 내림차순)")
lines.append("=" * 60)
lines.append("")

rows = c.execute("""
    SELECT realistic_score, match_score, company_tier, category,
           company, title, url, deadline
    FROM jobs
    WHERE is_entry_level=1 AND is_disqualified=0 AND is_hard_tier=0
      AND (is_target_company=1 OR category!='OTHER')
    ORDER BY is_target_company DESC, realistic_score DESC, match_score DESC
    LIMIT 20
""").fetchall()

for i, r in enumerate(rows, 1):
    mark = "★" if r[2] != "UNKNOWN" else " "
    dl = (r[7] or "")[:10] if r[7] else "(마감 없음)"
    lines.append(
        f"{i:2}. {mark} 현실성 {int(r[0]):2} / 직무 {int(r[1]):2}  "
        f"[{r[2]}] [{r[3]}]"
    )
    lines.append(f"      회사: {r[4]}")
    lines.append(f"      공고: {r[5][:90]}")
    lines.append(f"      마감: {dl}")
    lines.append(f"      URL : {r[6][:100]}")
    lines.append("")

lines.append("=" * 60)
lines.append("  화이트리스트 매칭된 기업 전체")
lines.append("=" * 60)
for row in c.execute(
    "SELECT DISTINCT company_tier, company FROM jobs "
    "WHERE is_target_company=1 ORDER BY company_tier, company"
):
    lines.append(f"  [{row[0]:15}] {row[1]}")
lines.append("")

with open("top_results.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print("done, lines:", len(lines))
