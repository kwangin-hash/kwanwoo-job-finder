"""
청운대 CS + 정보처리기사/ADsP/데이터분석기사 스펙으로
**실질적 합격 가능성이 있는** 기업 화이트리스트.

로봇·로보틱스 회사는 전부 제외 (자격증·스펙과 무관 직무).

티어:
  PUBLIC_LARGE  : 대형 공기업·공공기관 (자격증 가점제, NCS)
  PUBLIC_MID    : 중견 공공기관·재단·진흥원 (진입 가장 쉬움)
  FINANCE_IT    : 금융권 IT직군
  CARD_INSURANCE: 카드·보험 2금융 IT/데이터
  SI_MID        : 중견 SI·IT서비스
  SME_IT        : 중소 IT 개발사
  FINTECH       : 핀테크
  ECOMMERCE     : 이커머스·유통
  TELCO_IT      : 통신사 IT 자회사

제외:
  - 로봇 전 영역
  - 대기업 공채 직고용 (별도 HARD 리스트)
"""
from __future__ import annotations

TARGET_COMPANIES: list[dict] = [
    # ─────────────── 대형 공기업·공공기관 ───────────────
    {"name": "한국전력공사", "tier": "PUBLIC_LARGE", "cert_bonus": 10},
    {"name": "한국수력원자력", "tier": "PUBLIC_LARGE", "cert_bonus": 10},
    {"name": "한국가스공사", "tier": "PUBLIC_LARGE", "cert_bonus": 8},
    {"name": "한국수자원공사", "tier": "PUBLIC_LARGE", "cert_bonus": 8},
    {"name": "한국도로공사", "tier": "PUBLIC_LARGE", "cert_bonus": 8},
    {"name": "한국철도공사", "tier": "PUBLIC_LARGE", "cert_bonus": 8},
    {"name": "한국토지주택공사", "tier": "PUBLIC_LARGE", "cert_bonus": 8},
    {"name": "인천국제공항공사", "tier": "PUBLIC_LARGE", "cert_bonus": 8},
    {"name": "한국공항공사", "tier": "PUBLIC_LARGE", "cert_bonus": 7},
    {"name": "한국지역난방공사", "tier": "PUBLIC_LARGE", "cert_bonus": 7},
    {"name": "한국남동발전", "tier": "PUBLIC_LARGE", "cert_bonus": 8},
    {"name": "한국남부발전", "tier": "PUBLIC_LARGE", "cert_bonus": 8},
    {"name": "한국동서발전", "tier": "PUBLIC_LARGE", "cert_bonus": 8},
    {"name": "한국서부발전", "tier": "PUBLIC_LARGE", "cert_bonus": 8},
    {"name": "한국중부발전", "tier": "PUBLIC_LARGE", "cert_bonus": 8},
    {"name": "국민건강보험공단", "tier": "PUBLIC_LARGE", "cert_bonus": 10},
    {"name": "국민연금공단", "tier": "PUBLIC_LARGE", "cert_bonus": 10},
    {"name": "건강보험심사평가원", "tier": "PUBLIC_LARGE", "cert_bonus": 12},
    {"name": "근로복지공단", "tier": "PUBLIC_LARGE", "cert_bonus": 8},
    {"name": "예탁결제원", "tier": "PUBLIC_LARGE", "cert_bonus": 9},
    {"name": "한국자산관리공사", "tier": "PUBLIC_LARGE", "cert_bonus": 9},
    {"name": "주택금융공사", "tier": "PUBLIC_LARGE", "cert_bonus": 9},
    {"name": "신용보증기금", "tier": "PUBLIC_LARGE", "cert_bonus": 9},
    {"name": "기술보증기금", "tier": "PUBLIC_LARGE", "cert_bonus": 9},
    {"name": "한국무역보험공사", "tier": "PUBLIC_LARGE", "cert_bonus": 8},
    {"name": "한국농어촌공사", "tier": "PUBLIC_LARGE", "cert_bonus": 7},
    {"name": "한국석유공사", "tier": "PUBLIC_LARGE", "cert_bonus": 7},
    {"name": "한국관광공사", "tier": "PUBLIC_LARGE", "cert_bonus": 7},

    # ─────────────── 중견 공공기관·진흥원 ───────────────
    {"name": "한국인터넷진흥원", "tier": "PUBLIC_MID", "cert_bonus": 10},
    {"name": "한국지능정보사회진흥원", "tier": "PUBLIC_MID", "cert_bonus": 10},
    {"name": "정보통신산업진흥원", "tier": "PUBLIC_MID", "cert_bonus": 9},
    {"name": "한국전자통신연구원", "tier": "PUBLIC_MID", "cert_bonus": 8},
    {"name": "한국데이터산업진흥원", "tier": "PUBLIC_MID", "cert_bonus": 15},
    {"name": "한국산업기술시험원", "tier": "PUBLIC_MID", "cert_bonus": 7},
    {"name": "한국방송통신전파진흥원", "tier": "PUBLIC_MID", "cert_bonus": 7},
    {"name": "한국사회보장정보원", "tier": "PUBLIC_MID", "cert_bonus": 10},
    {"name": "한국교육학술정보원", "tier": "PUBLIC_MID", "cert_bonus": 8},
    {"name": "사회보장정보원", "tier": "PUBLIC_MID", "cert_bonus": 10},
    {"name": "한국보건의료정보원", "tier": "PUBLIC_MID", "cert_bonus": 9},
    {"name": "한국산업인력공단", "tier": "PUBLIC_MID", "cert_bonus": 6},

    # ─────────────── 금융 IT 1금융 전산 ───────────────
    {"name": "IBK기업은행", "tier": "FINANCE_IT", "cert_bonus": 8},
    {"name": "농협은행", "tier": "FINANCE_IT", "cert_bonus": 7},
    {"name": "Sh수협은행", "tier": "FINANCE_IT", "cert_bonus": 7},
    {"name": "한국산업은행", "tier": "FINANCE_IT", "cert_bonus": 9},
    {"name": "한국수출입은행", "tier": "FINANCE_IT", "cert_bonus": 9},

    # ─────────────── 2금융 (카드·보험·캐피탈·저축) ───────────────
    {"name": "롯데카드", "tier": "CARD_INSURANCE", "cert_bonus": 6},
    {"name": "BC카드", "tier": "CARD_INSURANCE", "cert_bonus": 6},
    {"name": "NH농협카드", "tier": "CARD_INSURANCE", "cert_bonus": 6},
    {"name": "우리카드", "tier": "CARD_INSURANCE", "cert_bonus": 6},
    {"name": "하나카드", "tier": "CARD_INSURANCE", "cert_bonus": 6},
    {"name": "신한카드", "tier": "CARD_INSURANCE", "cert_bonus": 6},
    {"name": "DB손해보험", "tier": "CARD_INSURANCE", "cert_bonus": 6},
    {"name": "메리츠화재", "tier": "CARD_INSURANCE", "cert_bonus": 6},
    {"name": "KB손해보험", "tier": "CARD_INSURANCE", "cert_bonus": 6},
    {"name": "한화생명", "tier": "CARD_INSURANCE", "cert_bonus": 6},
    {"name": "교보생명", "tier": "CARD_INSURANCE", "cert_bonus": 6},
    {"name": "NH농협생명", "tier": "CARD_INSURANCE", "cert_bonus": 6},
    {"name": "롯데손해보험", "tier": "CARD_INSURANCE", "cert_bonus": 6},
    {"name": "흥국화재", "tier": "CARD_INSURANCE", "cert_bonus": 5},
    {"name": "흥국생명", "tier": "CARD_INSURANCE", "cert_bonus": 5},
    {"name": "AIA생명", "tier": "CARD_INSURANCE", "cert_bonus": 5},
    {"name": "현대캐피탈", "tier": "CARD_INSURANCE", "cert_bonus": 6},
    {"name": "JB우리캐피탈", "tier": "CARD_INSURANCE", "cert_bonus": 5},
    {"name": "OK저축은행", "tier": "CARD_INSURANCE", "cert_bonus": 5},
    {"name": "SBI저축은행", "tier": "CARD_INSURANCE", "cert_bonus": 5},
    {"name": "웰컴저축은행", "tier": "CARD_INSURANCE", "cert_bonus": 5},
    {"name": "페퍼저축은행", "tier": "CARD_INSURANCE", "cert_bonus": 4},
    {"name": "신한저축은행", "tier": "CARD_INSURANCE", "cert_bonus": 5},
    {"name": "미래에셋증권", "tier": "CARD_INSURANCE", "cert_bonus": 6},
    {"name": "NH투자증권", "tier": "CARD_INSURANCE", "cert_bonus": 6},

    # ─────────────── 중견 SI·IT서비스 ───────────────
    {"name": "쌍용정보통신", "tier": "SI_MID", "cert_bonus": 5},
    {"name": "대우정보시스템", "tier": "SI_MID", "cert_bonus": 5},
    {"name": "아이티센", "tier": "SI_MID", "cert_bonus": 5},
    {"name": "CJ올리브네트웍스", "tier": "SI_MID", "cert_bonus": 5},
    {"name": "LG헬로비전", "tier": "SI_MID", "cert_bonus": 5},
    {"name": "롯데정보통신", "tier": "SI_MID", "cert_bonus": 6},
    {"name": "GS ITM", "tier": "SI_MID", "cert_bonus": 6},
    {"name": "신세계I&C", "tier": "SI_MID", "cert_bonus": 5},
    {"name": "KCC정보통신", "tier": "SI_MID", "cert_bonus": 5},
    {"name": "오픈베이스", "tier": "SI_MID", "cert_bonus": 4},
    {"name": "현대오토에버", "tier": "SI_MID", "cert_bonus": 6},
    {"name": "NHN클라우드", "tier": "SI_MID", "cert_bonus": 5},
    {"name": "메가존클라우드", "tier": "SI_MID", "cert_bonus": 5},
    {"name": "베스핀글로벌", "tier": "SI_MID", "cert_bonus": 4},
    {"name": "유라클", "tier": "SI_MID", "cert_bonus": 4},
    {"name": "아이씨티케이", "tier": "SI_MID", "cert_bonus": 4},

    # ─────────────── 통신사 IT 자회사 ───────────────
    {"name": "KTds", "tier": "TELCO_IT", "cert_bonus": 5},
    {"name": "SK텔링크", "tier": "TELCO_IT", "cert_bonus": 5},
    {"name": "KT skylife", "tier": "TELCO_IT", "cert_bonus": 4},

    # ─────────────── 중소 IT 개발사 (진입 가장 쉬움) ───────────────
    {"name": "영림원소프트랩", "tier": "SME_IT", "cert_bonus": 5},
    {"name": "더존비즈온", "tier": "SME_IT", "cert_bonus": 6},
    {"name": "티맥스소프트", "tier": "SME_IT", "cert_bonus": 5},
    {"name": "티맥스데이터", "tier": "SME_IT", "cert_bonus": 6},
    {"name": "티맥스에이앤씨", "tier": "SME_IT", "cert_bonus": 5},
    {"name": "이글루코퍼레이션", "tier": "SME_IT", "cert_bonus": 5},
    {"name": "이글루시큐리티", "tier": "SME_IT", "cert_bonus": 5},
    {"name": "안랩", "tier": "SME_IT", "cert_bonus": 5},
    {"name": "시큐아이", "tier": "SME_IT", "cert_bonus": 4},
    {"name": "파이오링크", "tier": "SME_IT", "cert_bonus": 4},
    {"name": "그리드원", "tier": "SME_IT", "cert_bonus": 4},
    {"name": "마크애니", "tier": "SME_IT", "cert_bonus": 4},
    {"name": "웨이버스", "tier": "SME_IT", "cert_bonus": 4},
    {"name": "투비소프트", "tier": "SME_IT", "cert_bonus": 4},
    {"name": "엑셈", "tier": "SME_IT", "cert_bonus": 5},
    {"name": "이노룰스", "tier": "SME_IT", "cert_bonus": 4},
    {"name": "아이퀘스트", "tier": "SME_IT", "cert_bonus": 4},
    {"name": "누리플렉스", "tier": "SME_IT", "cert_bonus": 4},
    {"name": "영우디지털", "tier": "SME_IT", "cert_bonus": 4},
    {"name": "쿠콘", "tier": "SME_IT", "cert_bonus": 4},
    {"name": "인프라웨어", "tier": "SME_IT", "cert_bonus": 4},
    {"name": "한글과컴퓨터", "tier": "SME_IT", "cert_bonus": 4},
    {"name": "한컴MDS", "tier": "SME_IT", "cert_bonus": 4},
    {"name": "더블유게임즈", "tier": "SME_IT", "cert_bonus": 4},

    # ─────────────── 핀테크 (실력주의) ───────────────
    {"name": "뱅크샐러드", "tier": "FINTECH", "cert_bonus": 5},
    {"name": "핀다", "tier": "FINTECH", "cert_bonus": 5},
    {"name": "레이니스트", "tier": "FINTECH", "cert_bonus": 5},
    {"name": "자비스앤빌런즈", "tier": "FINTECH", "cert_bonus": 5},
    {"name": "웰로", "tier": "FINTECH", "cert_bonus": 4},
    {"name": "NHN KCP", "tier": "FINTECH", "cert_bonus": 5},
    {"name": "페이히어", "tier": "FINTECH", "cert_bonus": 4},
    {"name": "다날", "tier": "FINTECH", "cert_bonus": 4},
    {"name": "갤럭시아머니트리", "tier": "FINTECH", "cert_bonus": 4},

    # ─────────────── 이커머스·유통 ───────────────
    {"name": "위메프", "tier": "ECOMMERCE", "cert_bonus": 5},
    {"name": "티몬", "tier": "ECOMMERCE", "cert_bonus": 4},
    {"name": "인터파크", "tier": "ECOMMERCE", "cert_bonus": 5},
    {"name": "이랜드리테일", "tier": "ECOMMERCE", "cert_bonus": 4},
    {"name": "무신사", "tier": "ECOMMERCE", "cert_bonus": 5},
    {"name": "29CM", "tier": "ECOMMERCE", "cert_bonus": 4},
    {"name": "오늘의집", "tier": "ECOMMERCE", "cert_bonus": 5},
    {"name": "지그재그", "tier": "ECOMMERCE", "cert_bonus": 4},
    {"name": "마켓컬리", "tier": "ECOMMERCE", "cert_bonus": 5},
    {"name": "SSG닷컴", "tier": "ECOMMERCE", "cert_bonus": 5},
    {"name": "11번가", "tier": "ECOMMERCE", "cert_bonus": 5},
    {"name": "G마켓", "tier": "ECOMMERCE", "cert_bonus": 5},
    {"name": "Gmarket", "tier": "ECOMMERCE", "cert_bonus": 5},
    {"name": "에이블리", "tier": "ECOMMERCE", "cert_bonus": 4},
    {"name": "브랜디", "tier": "ECOMMERCE", "cert_bonus": 4},
    {"name": "카페24", "tier": "ECOMMERCE", "cert_bonus": 4},
    {"name": "이마트", "tier": "ECOMMERCE", "cert_bonus": 5},
    {"name": "CJ올리브영", "tier": "ECOMMERCE", "cert_bonus": 4},
    {"name": "아성다이소", "tier": "ECOMMERCE", "cert_bonus": 4},

    # ─────────────── 로봇·임베디드·자율주행 (개발 직군) ───────────────
    {"name": "레인보우로보틱스", "tier": "ROBOT_MID", "cert_bonus": 4},
    {"name": "로보티즈", "tier": "ROBOT_MID", "cert_bonus": 4},
    {"name": "유진로봇", "tier": "ROBOT_MID", "cert_bonus": 4},
    {"name": "로보스타", "tier": "ROBOT_MID", "cert_bonus": 4},
    {"name": "두산로보틱스", "tier": "ROBOT_MID", "cert_bonus": 6},
    {"name": "현대로보틱스", "tier": "ROBOT_MID", "cert_bonus": 6},
    {"name": "현대위아", "tier": "ROBOT_MID", "cert_bonus": 5},
    {"name": "뉴로메카", "tier": "ROBOT_MID", "cert_bonus": 4},
    {"name": "트위니", "tier": "ROBOT_MID", "cert_bonus": 4},
    {"name": "클로봇", "tier": "ROBOT_MID", "cert_bonus": 4},
    {"name": "힐스로보틱스", "tier": "ROBOT_MID", "cert_bonus": 4},
    {"name": "시스콘", "tier": "ROBOT_MID", "cert_bonus": 4},
    {"name": "모라이", "tier": "ROBOT_MID", "cert_bonus": 4},
    {"name": "서울로보틱스", "tier": "ROBOT_MID", "cert_bonus": 4},
    {"name": "한화로보틱스", "tier": "ROBOT_MID", "cert_bonus": 5},
    {"name": "LS ITC", "tier": "ROBOT_MID", "cert_bonus": 5},
    {"name": "포스코DX", "tier": "ROBOT_MID", "cert_bonus": 7},
    {"name": "로보로보", "tier": "ROBOT_MID", "cert_bonus": 3},
    {"name": "이지로보틱스", "tier": "ROBOT_MID", "cert_bonus": 3},
    {"name": "아진엑스텍", "tier": "ROBOT_MID", "cert_bonus": 4},

    # ─────────────── 드론·UAV ───────────────
    {"name": "드로젠", "tier": "ROBOT_MID", "cert_bonus": 4},
    {"name": "유콘시스템", "tier": "ROBOT_MID", "cert_bonus": 4},
    {"name": "파블로항공", "tier": "ROBOT_MID", "cert_bonus": 5},
    {"name": "유비파이", "tier": "ROBOT_MID", "cert_bonus": 4},
    {"name": "나르마", "tier": "ROBOT_MID", "cert_bonus": 4},
    {"name": "디스이즈엔지니어링", "tier": "ROBOT_MID", "cert_bonus": 4},
    {"name": "케이씨엔컴퍼니", "tier": "ROBOT_MID", "cert_bonus": 3},
    {"name": "숨비", "tier": "ROBOT_MID", "cert_bonus": 3},
    {"name": "한국항공우주산업", "tier": "ROBOT_MID", "cert_bonus": 6},
    {"name": "한화에어로스페이스", "tier": "ROBOT_MID", "cert_bonus": 6},
    {"name": "LIG넥스원", "tier": "ROBOT_MID", "cert_bonus": 6},
    {"name": "켄코아에어로스페이스", "tier": "ROBOT_MID", "cert_bonus": 5},
    {"name": "베셀", "tier": "ROBOT_MID", "cert_bonus": 3},
    {"name": "성우엔지니어링", "tier": "ROBOT_MID", "cert_bonus": 3},
]


# 학벌 컷이 현실적으로 어려운 기업 (별도 표시·우선순위 낮춤)
HARD_TIER_COMPANIES: set[str] = {
    "네이버", "카카오", "라인", "우아한형제들", "배달의민족",
    "쿠팡", "토스", "비바리퍼블리카", "카카오페이", "카카오뱅크",
    "삼성전자", "LG전자", "SK하이닉스", "현대자동차", "기아",
    "삼성SDS", "LG CNS", "SK C&C", "삼성SDI", "LG디스플레이",
    "넥슨", "엔씨소프트", "넷마블", "크래프톤",
    "당근마켓", "당근", "두나무", "업비트",
    "NAVER", "KAKAO", "LINE",
}


def _normalize(name: str) -> str:
    """회사명 정규화 — 접두어·기호·공백 제거"""
    if not name:
        return ""
    s = name
    for token in ("(주)", "(유)", "(재)", "(사)", "㈜", "주식회사", "유한회사", "재단법인", "사단법인"):
        s = s.replace(token, "")
    for ch in (" ", "\t", "[", "]", "【", "】", "《", "》", "<", ">", "(", ")"):
        s = s.replace(ch, "")
    return s.lower()


def find_tier(company: str) -> tuple[str, int]:
    """
    공고 회사명 → (tier, cert_bonus). 매칭 실패 시 ("UNKNOWN", 0).

    매칭 규칙 (오탐 방지):
      - target 이 normalized 에 포함될 때만 매칭 (한 방향)
      - target 길이 4자 이상 (너무 짧으면 오탐 위험)
      - 회사명이 너무 짧으면(3자 이하) 매칭 시도 안함
    """
    normalized = _normalize(company)
    if len(normalized) < 3:
        return "UNKNOWN", 0

    for entry in TARGET_COMPANIES:
        target = _normalize(entry["name"])
        if len(target) < 4:
            continue
        if target in normalized:
            return entry["tier"], entry["cert_bonus"]

    return "UNKNOWN", 0


def is_hard_tier(company: str) -> bool:
    normalized = _normalize(company)
    if len(normalized) < 3:
        return False
    for hard in HARD_TIER_COMPANIES:
        h = _normalize(hard)
        if len(h) < 4:
            continue
        if h in normalized:
            return True
    return False


TIER_LABELS: dict[str, str] = {
    "PUBLIC_LARGE": "대형 공기업",
    "PUBLIC_MID": "공공·진흥원",
    "FINANCE_IT": "금융 IT",
    "CARD_INSURANCE": "카드·보험",
    "SI_MID": "중견 SI",
    "SME_IT": "중소 IT",
    "FINTECH": "핀테크",
    "ECOMMERCE": "이커머스",
    "TELCO_IT": "통신 IT",
    "ROBOT_MID": "로봇·제조",
    "UNKNOWN": "기타",
    "HARD": "대기업(경쟁↑)",
}
