"""
원티드 크롤러

원티드는 공개 JSON 엔드포인트가 있어 신입·데이터·로봇 키워드로 검색 가능.
endpoint: https://www.wanted.co.kr/api/chaos/navigation/v1/results

주의: 실제 키/파라미터는 사이트 업데이트에 따라 바뀔 수 있음.
이 크롤러는 공개 검색 API 호출 예시이며, 차단되면 query 파라미터 조정 필요.
"""
from __future__ import annotations
import httpx
from datetime import datetime
from app.crawlers.base import BaseCrawler


def _extract_items(data) -> list:
    """
    원티드 응답은 시기·엔드포인트에 따라 여러 형태.
    가능한 모든 경로를 탐색해서 '공고 아이템 리스트'만 뽑아온다.
    """
    if isinstance(data, list):
        return data
    if not isinstance(data, dict):
        return []

    # 흔한 경로들
    for path in (
        ("data", "jobs"),
        ("data",),
        ("jobs",),
        ("results",),
        ("data", "wantedPlus"),
        ("data", "jobList"),
    ):
        cur = data
        ok = True
        for k in path:
            if isinstance(cur, dict) and k in cur:
                cur = cur[k]
            else:
                ok = False
                break
        if ok and isinstance(cur, list):
            return cur
    return []


class WantedCrawler(BaseCrawler):
    source = "wanted"
    base_url = "https://www.wanted.co.kr/api/chaos/navigation/v1/results"

    # 5개 실질 트랙 키워드 (웹개발 제외, 로봇 포함)
    search_queries = [
        # PUBLIC
        "공공기관 전산", "공기업 전산", "공공 데이터",
        # FINANCE_DATA
        "카드사 신입", "보험사 신입",
        # SW_DEV (백엔드·서버)
        "신입 개발자", "주니어 백엔드", "Java 신입", "Spring 신입",
        "서버 개발 신입", "SI 신입", "ERP 신입", "QA 엔지니어 신입",
        # ROBOT_DEV
        "로봇", "로보틱스", "임베디드", "자율주행",
        "컴퓨터비전", "C++ 개발",
        # DATA_ANALYST
        "데이터분석 신입", "Data Analyst", "BI 신입",
        "데이터 엔지니어 신입",
    ]

    def fetch(self) -> list[dict]:
        jobs: list[dict] = []
        seen_ids: set[str] = set()

        with httpx.Client(
            timeout=15.0,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                ),
                "Accept": "application/json",
                "Referer": "https://www.wanted.co.kr/",
            },
        ) as client:
            for query in self.search_queries:
                try:
                    resp = client.get(
                        self.base_url,
                        params={
                            "1": query,
                            "job_sort": "job.latest_order",
                            "locations": "all",
                            "years": "0",
                            "limit": 50,
                        },
                    )
                    if resp.status_code != 200:
                        continue
                    try:
                        data = resp.json()
                    except ValueError:
                        continue
                    items = _extract_items(data)
                    for item in items:
                        if not isinstance(item, dict):
                            continue
                        job = self._parse(item)
                        if job and job["source_id"] not in seen_ids:
                            seen_ids.add(job["source_id"])
                            jobs.append(job)
                except (httpx.HTTPError, ValueError, KeyError, AttributeError, TypeError):
                    continue

        return jobs

    def _parse(self, item: dict) -> dict | None:
        try:
            jid = str(item.get("id") or item.get("position_id") or "")
            if not jid:
                return None
            company = (
                item.get("company", {}).get("name")
                if isinstance(item.get("company"), dict)
                else item.get("company_name")
            ) or "(미상)"

            return {
                "source_id": jid,
                "url": f"https://www.wanted.co.kr/wd/{jid}",
                "company": company,
                "title": item.get("position") or item.get("title") or "",
                "description": item.get("intro") or item.get("description") or "",
                "location": item.get("address", {}).get("location")
                    if isinstance(item.get("address"), dict)
                    else item.get("location"),
                "posted_at": self.parse_dt(item.get("confirm_time") or item.get("created_at")),
                "deadline": self.parse_dt(item.get("due_time") or item.get("deadline")),
            }
        except (KeyError, TypeError):
            return None
