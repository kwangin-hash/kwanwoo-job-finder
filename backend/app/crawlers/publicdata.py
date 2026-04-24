"""
공공데이터포털 — 인사혁신처 공공취업정보 조회 서비스

API: https://apis.data.go.kr/1760000/PblJobService/getList
포맷: XML
전체 건수: 약 27만 건 (2008년부터 누적)

전략:
  - totalCount 먼저 얻어 마지막 페이지 번호 계산
  - 마지막 페이지부터 역순으로 N페이지 당겨옴 → 최신 공고 확보
  - 마감일(enddate)이 오늘 이후인 것만 채택
"""
from __future__ import annotations
import os
import ssl
import httpx
from datetime import datetime, date
from pathlib import Path
from bs4 import BeautifulSoup
from app.crawlers.base import BaseCrawler


def _load_env_key() -> str:
    env_key = os.getenv("PUBLIC_DATA_SERVICE_KEY", "").strip()
    if env_key:
        return env_key
    env_path = Path(__file__).resolve().parent.parent.parent / ".env"
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("PUBLIC_DATA_SERVICE_KEY="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    return ""


def _tls_ctx() -> ssl.SSLContext:
    ctx = ssl.create_default_context()
    ctx.set_ciphers("DEFAULT@SECLEVEL=1")
    return ctx


# 마지막 페이지부터 역순으로 몇 페이지 가져올지
# 이 API는 numOfRows=100 에서 뒷페이지 타임아웃 발생 → 20 으로 제한
RECENT_PAGES = 10
PAGE_SIZE = 20


class PublicDataCrawler(BaseCrawler):
    source = "publicdata"
    base = "https://apis.data.go.kr/1760000/PblJobService"

    def fetch(self) -> list[dict]:
        key = _load_env_key()
        if not key:
            return []

        jobs: list[dict] = []
        ctx = _tls_ctx()
        today = date.today()

        try:
            with httpx.Client(verify=ctx, timeout=90.0) as client:
                # 1) totalCount 얻기
                total = self._get_total(client, key)
                if total <= 0:
                    return []

                last_page = (total + PAGE_SIZE - 1) // PAGE_SIZE

                # 2) 마지막 페이지부터 역순으로 긁음
                for page in range(last_page, max(last_page - RECENT_PAGES, 0), -1):
                    try:
                        resp = client.get(
                            f"{self.base}/getList",
                            params={
                                "serviceKey": key,
                                "numOfRows": PAGE_SIZE,
                                "pageNo": page,
                            },
                        )
                        if resp.status_code != 200:
                            continue
                        parsed = self._parse_xml(resp.text, today)
                        jobs.extend(parsed)
                    except (httpx.HTTPError, ValueError):
                        continue
        except (httpx.HTTPError, ValueError):
            pass

        return jobs

    def _get_total(self, client: httpx.Client, key: str) -> int:
        resp = client.get(
            f"{self.base}/getList",
            params={"serviceKey": key, "numOfRows": 1, "pageNo": 1},
        )
        if resp.status_code != 200:
            return 0
        soup = BeautifulSoup(resp.text, "xml")
        tc = soup.find("totalCount")
        if not tc:
            return 0
        try:
            return int(tc.get_text(strip=True))
        except ValueError:
            return 0

    def _parse_xml(self, xml: str, today: date) -> list[dict]:
        results: list[dict] = []
        soup = BeautifulSoup(xml, "xml")

        # 에러 응답은 <errMsg> 등 다른 태그 구조 — 무시
        for item in soup.find_all("item"):
            try:
                idx = self._txt(item, "idx")
                title = self._txt(item, "title")
                company = self._txt(item, "insttname")
                if not idx or not title:
                    continue

                regdate = self._parse_ymd(self._txt(item, "regdate"))
                enddate = self._parse_ymd(self._txt(item, "enddate"))

                # 마감 지난 공고 제외
                if enddate and enddate.date() < today:
                    continue

                # 알리오 상세 링크
                url = f"https://job.alio.go.kr/recruitview.do?idx={idx}"

                results.append({
                    "source_id": idx,
                    "url": url,
                    "company": company or "(공공기관)",
                    "title": title,
                    "description": "",
                    "location": None,
                    "posted_at": regdate,
                    "deadline": enddate,
                })
            except (AttributeError, ValueError, KeyError):
                continue

        return results

    @staticmethod
    def _txt(item, tag: str) -> str:
        el = item.find(tag)
        return el.get_text(strip=True) if el else ""

    @staticmethod
    def _parse_ymd(s: str):
        if not s or len(s) != 8:
            return None
        try:
            return datetime(int(s[0:4]), int(s[4:6]), int(s[6:8]))
        except ValueError:
            return None
