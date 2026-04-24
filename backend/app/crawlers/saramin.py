"""
사람인 크롤러 (공공·신입 중심)

사람인은 공식 오픈API가 있지만 신청 승인 필요.
여기서는 공개 검색 결과 페이지 HTML 파싱 방식 사용 (완전 비로그인).

주의:
  - 과도한 요청은 차단됨 → 키워드당 최대 2페이지, 요청 간 2초 지연
  - HTML 구조 변경 시 셀렉터 수정 필요
  - 운영 전환 시 사람인 오픈API(https://oapi.saramin.co.kr/) 로 교체 권장
"""
from __future__ import annotations
import time
import re
from urllib.parse import quote
import httpx
from bs4 import BeautifulSoup
from app.crawlers.base import BaseCrawler


class SaraminCrawler(BaseCrawler):
    source = "saramin"
    list_url = "https://www.saramin.co.kr/zf_user/search/recruit"

    keywords = [
        # PUBLIC
        "공공기관 전산",
        "공기업 전산",
        "공공 데이터",
        # FINANCE_DATA
        "카드 데이터",
        "보험 데이터",
        "손해보험 IT",
        # SW_DEV (백엔드·서버 중심)
        "신입 개발자",
        "Java 신입",
        "Spring 신입",
        "백엔드 신입",
        "서버 개발 신입",
        "API 신입",
        "ERP 신입",
        "MES 신입",
        "QA 신입",
        # ROBOT_DEV
        "로봇 SW",
        "로봇 개발자",
        "임베디드 신입",
        "자율주행 개발",
        "컴퓨터비전 신입",
        "C++ 신입",
        # 드론
        "드론 개발",
        "드론 SW",
        "드론 엔지니어",
        "UAV 개발",
        "무인기 개발",
        # DATA_ANALYST
        "데이터분석 신입",
        "BI 신입",
        "데이터 엔지니어 신입",
    ]

    def fetch(self) -> list[dict]:
        jobs: list[dict] = []
        seen: set[str] = set()

        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "ko-KR,ko;q=0.9",
        }

        with httpx.Client(timeout=15.0, headers=headers, follow_redirects=True) as c:
            for kw in self.keywords:
                for page in (1, 2):
                    try:
                        resp = c.get(
                            self.list_url,
                            params={
                                "search_optional_item": "n",
                                "searchword": kw,
                                "recruitPage": page,
                                "recruitSort": "reg_dt",
                                "exp_cd": "1",  # 신입
                            },
                        )
                        if resp.status_code != 200:
                            break
                        parsed = self._parse_list(resp.text)
                        for p in parsed:
                            if p["source_id"] in seen:
                                continue
                            seen.add(p["source_id"])
                            jobs.append(p)
                        time.sleep(2.0)  # 차단 방지
                    except (httpx.HTTPError, ValueError):
                        break

        return jobs

    def _parse_list(self, html: str) -> list[dict]:
        items: list[dict] = []
        soup = BeautifulSoup(html, "lxml")

        # 사람인 리스트 카드. 클래스명은 가끔 바뀌므로 여러 케이스 방어적 처리.
        cards = soup.select(".item_recruit") or soup.select("[class*=list_item]")
        for card in cards:
            try:
                a_title = card.select_one(".job_tit a") or card.select_one("a[href*='/zf_user/jobs']")
                if not a_title:
                    continue
                href = a_title.get("href", "")
                if not href:
                    continue
                if href.startswith("/"):
                    href = "https://www.saramin.co.kr" + href

                m = re.search(r"rec_idx=(\d+)", href)
                if not m:
                    continue
                jid = m.group(1)

                title = a_title.get_text(strip=True)
                comp_el = card.select_one(".corp_name a") or card.select_one(".corp_name")
                company = comp_el.get_text(strip=True) if comp_el else "(미상)"

                cond_els = card.select(".job_condition span")
                location = cond_els[0].get_text(strip=True) if cond_els else None

                deadline_el = card.select_one(".job_date .date")
                deadline_text = deadline_el.get_text(strip=True) if deadline_el else ""
                deadline = self._parse_deadline(deadline_text)

                items.append({
                    "source_id": jid,
                    "url": href,
                    "company": company,
                    "title": title,
                    "description": "",  # 상세페이지 안 긁음 (차단 위험)
                    "location": location,
                    "posted_at": None,
                    "deadline": deadline,
                })
            except (AttributeError, IndexError, KeyError):
                continue

        return items

    @staticmethod
    def _parse_deadline(text: str):
        """'~ 06/30(월)' 또는 '상시채용' 형태 → datetime"""
        if not text or "상시" in text:
            return None
        m = re.search(r"(\d{1,2})[/.-](\d{1,2})", text)
        if not m:
            return None
        from datetime import datetime
        month, day = int(m.group(1)), int(m.group(2))
        year = datetime.now().year
        try:
            d = datetime(year, month, day)
            # 월이 현재보다 작으면 내년 마감
            if d < datetime.now():
                d = datetime(year + 1, month, day)
            return d
        except ValueError:
            return None
