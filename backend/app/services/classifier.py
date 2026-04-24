"""
공고 분류기 + 2단 점수 시스템

1. match_score        — 직무가 아드님에게 맞는가 (기존 로직 유지)
2. realistic_score    — **실질적으로 합격 가능한 기업인가** (신규, 기본 정렬 기준)

이 둘을 함께 계산해서 "직무가 맞으면서 붙을 가능성도 있는" 공고만
상위에 뜨게 한다.
"""
from __future__ import annotations
from app.config import (
    CATEGORIES,
    DISQUALIFY_KEYWORDS,
    ENTRY_LEVEL_KEYWORDS,
    PUBLIC_DEV_KEYWORDS,
)
from app.data.target_companies import find_tier, is_hard_tier


# 티어별 현실성 베이스 점수
TIER_BASE_SCORE: dict[str, float] = {
    "PUBLIC_LARGE":   70,
    "PUBLIC_MID":     75,
    "FINANCE_IT":     55,
    "CARD_INSURANCE": 65,
    "SI_MID":         70,
    "SME_IT":         80,
    "FINTECH":        55,
    "ECOMMERCE":      55,
    "TELCO_IT":       60,
    "ROBOT_MID":      65,  # 로봇·임베디드 중견
    "UNKNOWN":        35,
    "HARD":           15,
}


def _text_of(title: str, description: str, company: str) -> str:
    return f"{company} {title} {description or ''}".lower()


def classify(title: str, description: str, company: str) -> str:
    text = _text_of(title, description, company)
    best_cat, best_hits = "OTHER", 0
    for cat_key, cat_def in CATEGORIES.items():
        hits = sum(
            1 for kw in cat_def["positive_keywords"] if kw.lower() in text
        )
        if hits > best_hits:
            best_cat, best_hits = cat_key, hits

    if best_hits < 1:
        return "OTHER"

    # PUBLIC 특별 규칙: 공공기관 키워드 + 개발 관련 키워드 동시에 있어야 PUBLIC
    # (없으면 일반 공무원·조리사·안전관리자 등 비개발 공고 → OTHER)
    if best_cat == "PUBLIC":
        dev_hits = sum(
            1 for kw in PUBLIC_DEV_KEYWORDS if kw.lower() in text
        )
        if dev_hits < 1:
            return "OTHER"

    return best_cat


def is_entry_level(title: str, description: str) -> bool:
    text = f"{title} {description or ''}".lower()
    return any(kw.lower() in text for kw in ENTRY_LEVEL_KEYWORDS)


def is_disqualified(title: str, description: str) -> bool:
    text = f"{title} {description or ''}".lower()
    return any(kw.lower() in text for kw in DISQUALIFY_KEYWORDS)


def company_info(company: str) -> dict:
    """기업 정보 — 티어·가점·hard tier 여부"""
    if is_hard_tier(company):
        return {
            "tier": "HARD",
            "cert_bonus": 0,
            "is_target": False,
            "is_hard": True,
        }
    tier, bonus = find_tier(company)
    return {
        "tier": tier,
        "cert_bonus": bonus,
        "is_target": tier != "UNKNOWN",
        "is_hard": False,
    }


def match_score(
    title: str, description: str, company: str, category: str
) -> float:
    """직무 적합도 (0~100) — 카테고리 키워드 + 자격증 + 신입 친화"""
    text = _text_of(title, description, company)
    score = 0.0

    if category in CATEGORIES:
        cat_def = CATEGORIES[category]
        hits = sum(
            1 for kw in cat_def["positive_keywords"] if kw.lower() in text
        )
        score += min(hits * 8, 50)

    cert_weight = {
        "정보처리기사": 5,
        "adsp": 5,
        "데이터분석": 8,
        "sqld": 4,
        "빅데이터분석기사": 6,
    }
    for kw, w in cert_weight.items():
        if kw.lower() in text:
            score += w
    score = min(score, 65)

    if is_entry_level(title, description):
        score += 20

    if is_disqualified(title, description):
        score -= 40

    return max(min(score, 100), 0.0)


def realistic_score(
    company: str,
    title: str,
    description: str,
    info: dict,
    category: str = "OTHER",
) -> float:
    """
    **실질적 합격 가능성 점수 (0~100)**

    앱의 기본 정렬 기준. "직무가 맞아도 못 붙을 곳"을 아래로 밀어낸다.

      기업 티어 베이스          : 15 ~ 80
      자격증 가점 (화이트리스트): +0 ~ +15
      카테고리 명확 보너스      : +8 (OTHER 아니면)
      신입 친화 가산            : +10
      경력/석사 요구 감점       : -30
    """
    base = TIER_BASE_SCORE.get(info["tier"], 35)
    score = float(base)

    score += info.get("cert_bonus", 0)

    # 카테고리가 OTHER 가 아니면(= 3개 트랙 중 하나에 해당) 보너스
    # 화이트리스트 외 회사라도 직무가 맞으면 볼 만함
    if category and category != "OTHER":
        score += 8

    if is_entry_level(title, description):
        score += 10

    if is_disqualified(title, description):
        score -= 30

    return max(min(score, 100), 0.0)
