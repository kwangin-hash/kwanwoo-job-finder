# 아들 취업찾기 (Son Job Finder)

아드님(청운대 컴공 4학년, 정보처리기사 보유 · ADsP 2026-08-08 · 데이터분석기사 2026-11-28)을 위해 **실질적으로 합격 가능한 기업**만 골라 매일 알려주는 앱.

## 핵심 철학: 현실성 점수 기준 정렬

대부분 채용앱이 "직무 매칭"만 본다면, 이 앱은 **두 가지 점수**를 동시에 본다:

- **현실성 점수 (realistic_score)** — 청운대 CS 스펙으로 실제 붙을 가능성
- **직무 점수 (match_score)** — 자격증·기술스택과 직무 적합도

정렬은 현실성 점수 우선. **네카라쿠배·삼성SDS 같은 대기업 공채는 "참고용 탭"으로 분리**해 실제 지원 가능한 공고가 메인에 뜨도록 했다.

## 실질 타겟 기업군 (화이트리스트 내장 160+ 사)

| 티어 | 예시 | 왜 현실적인가 |
|---|---|---|
| **대형 공기업** | 한전·LH·수공·건보·국민연금 | 자격증 가점제 · NCS 시험 |
| **공공·진흥원** | KISA·NIA·K-DATA·KERIS | 진입 가장 쉬운 공공 |
| **2금융** | 롯데·하나·BC카드, 한화생명 등 | 학벌 덜 보수적 |
| **중견 SI** | 쌍용정보통신·CJ올리브·롯데정보통신 | 신입 대량 채용 |
| **중소 IT** | 더존·티맥스·안랩·이글루 | 진입 가장 쉬움 |
| **핀테크** | 뱅크샐러드·핀다·자비스앤빌런즈 | 실력주의 |
| **이커머스** | 위메프·무신사·29CM·오늘의집 | 데이터 직군 수요 |
| **로봇 중견** | 레인보우·로보티즈·뉴로메카·두산로보틱스 | 꿈 트랙 연결 |

## 3개 트랙 × 실질 타겟 필터

| 트랙 | 타겟 |
|---|---|
| **공공·공기업** | 자격증 가점 극대화 |
| **데이터 분석** | 이커머스·2금융·핀테크·게임사 |
| **로봇·제조** | 아드님 관심사 연결 — 물류로봇·스마트팩토리 |

## 전체 구조

```
[백엔드 (Python)] --- 매일 06:00 크롤 ---> [SQLite DB]
       ↑                                       |
       |                                   REST API
       |                                       ↓
       +---------- [안드로이드 앱] --- 매일 07:00 알림
```

---

## 실행 방법 (처음 한 번)

### 1단계 — 백엔드 (부모님 PC에서 실행)

**1-1. Python 설치 확인** (3.10 이상)
```bash
python --version
```

**1-2. 가상환경 + 의존성 설치**
```bash
cd C:\Project\Private_Project\Employment\backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

**1-3. (선택) 공공데이터포털 API 키 발급**
- https://www.data.go.kr 로그인
- "공공기관 채용정보" 검색 → 활용신청 → 승인 후 인증키 복사
- 환경변수 설정:
```bash
set PUBLIC_DATA_SERVICE_KEY=발급받은키
```
키 없어도 원티드 크롤러만으로 동작합니다.

**1-4. 서버 실행**
```bash
python run.py
```
→ `http://localhost:8000` 에서 동작. 브라우저에서 `http://localhost:8000/docs` 열면 API 문서 확인 가능.

**1-5. 초기 데이터 한 번 수집**
```bash
# 다른 터미널에서
curl -X POST http://localhost:8000/ingest/run
```
→ 원티드에서 신입 공고 긁어와 DB에 저장.

**1-6. (중요) 앱이 접속할 IP 확인**
```bash
ipconfig
```
→ "IPv4 주소" 항목 (예: `192.168.0.10`) 기억.

---

### 2단계 — 안드로이드 앱 빌드

**2-1. Android Studio 설치** — https://developer.android.com/studio

**2-2. 프로젝트 열기**
- Android Studio → Open → `C:\Project\Private_Project\Employment\android` 선택
- Gradle sync 완료까지 대기 (첫 실행 5~15분)

**2-3. 서버 IP 설정**
- 파일 열기: `android/app/build.gradle.kts`
- 아래 줄을 찾아서
```kotlin
buildConfigField("String", "API_BASE_URL", "\"http://10.0.2.2:8000/\"")
```
  - **에뮬레이터**면 그대로 (`10.0.2.2` 가 PC를 가리킴)
  - **실제 폰**이면 `http://192.168.0.10:8000/` (1-6 에서 확인한 IP) 로 변경

**2-4. 실행**
- 폰을 USB로 연결 + 개발자 옵션·USB 디버깅 켜기
- Android Studio 상단 초록 ▶ 버튼
- 앱이 폰에 설치되고 자동 실행됨

---

## 매일 자동 동작

한 번 설정 후엔:

- **매일 06:00** — 백엔드가 크롤러 자동 실행 (PC가 켜져 있어야 함)
- **매일 07:00** — 앱이 서버에서 오늘의 Top 5 받아와 알림 표시

---

## 아드님이 앱에서 보는 것

1. **홈 헤더** — 오늘 신규 공고 수 (공공 / 데이터 / 로봇 3개 카테고리)
2. **탭 전환** — 트랙별 공고 리스트
3. **카드 탭** — 원티드·공공채용 사이트로 바로 이동
4. **점수 배지** — 녹색(70+, 강추) · 주황(50~69, 검토) · 회색(낮음)

---

## 구조 요약

```
backend/
  app/
    config.py              — 아드님 프로필 + 3개 카테고리 키워드
    data/
      target_companies.py  — 실질 타겟 기업 화이트리스트 (160+사) + HARD 리스트
    crawlers/
      wanted.py            — 원티드 신입 공고
      saramin.py           — 사람인 공공·신입 공고
      publicdata.py        — 공공데이터포털 공공기관 채용 API
    services/
      classifier.py        — 직무 점수 + 현실성 점수 계산
      ingest.py            — 크롤 → 분류 → DB upsert
    main.py                — FastAPI + 스케줄러
    models.py              — Job 테이블
android/
  app/src/main/java/com/employment/jobfinder/
    MainActivity.kt
    data/                  — Retrofit · DTO
    ui/                    — Compose 화면, 티어 뱃지, 점수 Pill
    worker/                — 매일 07:00 알림 (WorkManager)
```

## Phase 3 예정 (다음 세션)

- [ ] FCM 푸시 (PC 꺼져 있어도 받기)
- [ ] 자격증 시험 D-day 카운트다운 화면 (ADsP 8/8, 데이터분석기사 11/28)
- [ ] 갭 분석 화면 — 타겟 기업 JD 빈도 분석 Top 10
- [ ] 공공기관 NCS 시험 일정 캘린더
- [ ] 지원 상태 트래커 (서류/필기/면접/최종)
- [ ] APK 서명 + 배포

---

## 알려진 한계 (솔직히)

- **원티드 API는 비공식**: 사이트 개편 시 크롤러 수정 필요
- **사람인·잡코리아는 아직 미포함**: 봇 차단이 강해서 작업 필요
- **PC가 꺼져 있으면 크롤 안 돌아감**: 추후 클라우드(Railway·Render 무료티어) 배포 권장
- **로컬 네트워크만 지원**: 외부에서 폰으로 쓰려면 ngrok 또는 도메인 필요
