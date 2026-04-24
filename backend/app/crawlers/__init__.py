"""
크롤러 레지스트리
"""
from app.crawlers.wanted import WantedCrawler
from app.crawlers.publicdata import PublicDataCrawler
from app.crawlers.saramin import SaraminCrawler
from app.crawlers.worknet import WorknetCrawler

ALL_CRAWLERS = [WantedCrawler, PublicDataCrawler, SaraminCrawler, WorknetCrawler]
