"""
워크넷(work.go.kr) 크롤러

고용노동부 공식 채용 포털. 공공·민간·공기업 모두 포괄.
한국 공공사이트 TLS 설정 이슈 때문에 SECLEVEL=1 필요.

엔드포인트:
  https://www.work.go.kr/empInfo/empInfoSrch/list/dtlEmpSrchList.do
상세 URL:
  https://www.work24.go.kr/wk/a/b/1500/empDetailAuthView.do?wantedAuthNo=...&infoTypeCd=V
"""
from __future__ import annotations
import re
import ssl
import time
import httpx
from datetime import datetime
from bs4 import BeautifulSoup
from app.crawlers.base import BaseCrawler


def _tls_context() -> ssl.SSLContext:
    """한국 공공사이트 호환 TLS 설정"""
    ctx = ssl.create_default_context()
    ctx.set_ciphers("DEFAULT@SECLEVEL=1")
    ctx.minimum_version = ssl.TLSVersion.TLSv1_2
    return ctx


class WorknetCrawler(BaseCrawler):
    source = "worknet"
    list_url = "https://www.work.go.kr/empInfo/empInfoSrch/list/dtlEmpSrchList.do"

    # 실질 4트랙 + 공공 강화 키워드
    keywords = [
        # PUBLIC
        "공공기관 전산",
        "공기업 전산",
        "공공기관 데이터",
        "공단 전산",
        "전자정부",
        # FINANCE_DATA
        "카드사 신입",
        "보험사 IT",
        # SW_DEV (백엔드·서버)
        "Java 신입",
        "Spring 신입",
        "백엔드 신입",
        "서버 개발 신입",
        "SI 신입",
        "QA 신입",
        "ERP 신입",
        "MES 개발",
        # ROBOT_DEV
        "로봇 개발",
        "임베디드 신입",
        "자율주행",
        "C++ 개발",
        # DATA_ANALYST
        "데이터분석 신입",
        "BI 신입",
    ]

    def fetch(self) -> list[dict]:
        jobs: list[dict] = []
        seen: set[str] = set()

        ctx = _tls_context()
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "ko-KR,ko;q=0.9",
        }

        with httpx.Client(
            verify=ctx, headers=headers, timeout=25.0, follow_redirects=True
        ) as c:
            for kw in self.keywords:
                try:
                    resp = c.get(
                        self.list_url,
                        params={
                            "keyword": kw,
                            "srcKeyword": kw,
                            "resultCnt": "50",
                            "empWantedTypeCd": "1",  # 1 = 신입
                            "searchMode": "Y",
                        },
                    )
                    if resp.status_code != 200:
                        time.sleep(1.5)
                        continue
                    parsed = self._parse_list(resp.text)
                    for p in parsed:
                        if p["source_id"] in seen:
                            continue
                        seen.add(p["source_id"])
                        jobs.append(p)
                    time.sleep(1.5)
                except (httpx.HTTPError, ValueError, AttributeError, TypeError):
                    continue

        return jobs

    def _parse_list(self, html: str) -> list[dict]:
        soup = BeautifulSoup(html, "lxml")
        table = soup.select_one("table.board-list")
        if not table:
            return []

        items: list[dict] = []
        for tr in table.find_all("tr"):
            cells = tr.find_all("td")
            if len(cells) < 5:
                continue
            try:
                # 회사명 — 첫 a 태그의 텍스트
                company_a = cells[1].find("a")
                company = (
                    company_a.get_text(strip=True) if company_a else ""
                )
                # 마지막 a 태그 = 상세 페이지
                anchors = tr.find_all("a", href=True)
                detail = None
                for a in anchors:
                    href = a.get("href", "")
                    if "wantedAuthNo=" in href:
                        detail = a
                        break
                if not detail:
                    continue

                url = detail.get("href", "")
                title = detail.get_text(strip=True)

                m = re.search(r"wantedAuthNo=([A-Za-z0-9]+)", url)
                if not m:
                    continue
                jid = m.group(1)

                location = cells[2].get_text(" ", strip=True)[:200]

                # 날짜: "26/04/24 등록 26/05/08 마감"
                date_text = cells[4].get_text(" ", strip=True)
                posted_at = self._parse_ko_date(
                    re.search(r"(\d{2}/\d{2}/\d{2}).*?등록", date_text)
                )
                deadline = self._parse_ko_date(
                    re.search(r"(\d{2}/\d{2}/\d{2}).*?마감", date_text)
                )

                items.append({
                    "source_id": jid,
                    "url": url,
                    "company": company,
                    "title": title,
                    "description": "",
                    "location": location,
                    "posted_at": posted_at,
                    "deadline": deadline,
                })
            except (AttributeError, IndexError, KeyError, ValueError):
                continue

        return items

    @staticmethod
    def _parse_ko_date(match) -> datetime | None:
        if not match:
            return None
        raw = match.group(1)  # "26/04/24"
        try:
            yy, mm, dd = raw.split("/")
            year = 2000 + int(yy)
            return datetime(year, int(mm), int(dd))
        except (ValueError, IndexError):
            return None
