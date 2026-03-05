# 2026 College Hockey — University Amateur Ice Hockey League

대한 대학 아마추어 아이스하키 리그 2026 시즌 웹사이트.
GitHub Pages로 배포되는 정적 사이트 (백엔드 없음).

**Live**: https://lidge-jun.github.io/college-hockey-2026/

---

## 프로젝트 구조

```
college-hockey-2026/
├── index.html          # 메인 일정 페이지 (캘린더 + 경기 목록)
├── standings.html      # 순위표 (팀 + 개인 통계)
├── gallery.html        # 사진 갤러리 (Phase 1에서 구현)
├── results.json        # ⭐ 경기 결과 데이터 (핵심 데이터 파일)
├── photos.json         # ⭐ 사진 갤러리 설정 (Google Drive 폴더 매핑)
├── cal/                # ICS 캘린더 구독 파일 (6개)
│   ├── all-games.ics
│   ├── tigris.ics
│   ├── titans.ics
│   ├── kingo-leafs.ics
│   ├── capitals.ics
│   └── ice-unicorns.ics
└── devlog/             # 개발 로그
    └── _plan/          # 구현 계획
```

## 팀 정보

| 팀명 | 영문명 | 약어 | 색상 | 홈 링크 |
|------|--------|------|------|---------|
| 고려대 | TIGRIS | `korea` | #9B2335 | 고려대 아이스링크 |
| 연세대 | TITANS | `yonsei` | #1764E8 | 목동 아이스링크 |
| 성균관대 | KINGO LEAFS | `skku` | #3DB06B | 수원 아이스하우스 |
| 서울대 | CAPITALS | `snu` | #2A6BBE | 목동 아이스링크 |
| 광운대 | ICE UNICORNS | `kwu` | #843DA0 | 광운대 아이스링크 |

---

## 경기 결과 기록 방법

### 개요
경기가 끝나면 `results.json`을 업데이트합니다.
커밋 & 푸시하면 GitHub Pages가 자동 배포되고, 순위표와 일정표에 즉시 반영됩니다.

### Game ID 규칙
```
MMDD-homeAbbr-awayAbbr
```
예시: 3월 8일 고려대(홈) vs 성균관대(원정) → `0308-korea-skku`

### Step 1: 기록지 준비

경기 기록지 사진을 찍거나, 다음 형식으로 텍스트를 작성합니다:

```
경기: 3/8 고려대 vs 성균관대
결과: 5-3 (2-1, 1-2, 2-0)
골: 김하키#10(고려대)x2, 이퍽#7(고려대)x1, 박골#3(성균관대)x2, 최슛#11(성균관대)x1
어시: 박어시#14(고려대)x2, 정패스#8(성균관대)x1
```

**필수 정보**:
- 최종 스코어
- 피리어드별 점수 (3피리어드)
- 연장 여부

**선택 정보** (있으면 좋음):
- 골 기록: 선수명, 등번호, 소속팀, 골 수
- 어시스트 기록: 선수명, 등번호, 소속팀, 어시 수

### Step 2: results.json 수정

해당 경기의 `id`를 찾아 아래와 같이 수정합니다.

#### Before (경기 전)
```json
{
  "id": "0308-korea-skku",
  "date": "2026-03-08",
  "home": "고려대",
  "away": "성균관대",
  "venue": "고대링크",
  "status": "scheduled",
  "score": null,
  "overtime": false,
  "periods": null,
  "players": null
}
```

#### After (경기 완료 — 일반 승부)
```json
{
  "id": "0308-korea-skku",
  "date": "2026-03-08",
  "home": "고려대",
  "away": "성균관대",
  "venue": "고대링크",
  "status": "final",
  "score": { "home": 5, "away": 3 },
  "overtime": false,
  "periods": [
    { "home": 2, "away": 1 },
    { "home": 1, "away": 2 },
    { "home": 2, "away": 0 }
  ],
  "players": {
    "goals": [
      { "name": "김하키", "num": "#10", "team": "고려대", "count": 2 },
      { "name": "이퍽", "num": "#7", "team": "고려대", "count": 1 },
      { "name": "박골", "num": "#3", "team": "성균관대", "count": 2 },
      { "name": "최슛", "num": "#11", "team": "성균관대", "count": 1 }
    ],
    "assists": [
      { "name": "박어시", "num": "#14", "team": "고려대", "count": 2 },
      { "name": "정패스", "num": "#8", "team": "성균관대", "count": 1 }
    ]
  }
}
```

#### After (연장전 승부)
연장전일 경우 `overtime`만 `true`로 변경합니다.
피리어드는 연장 피리어드까지 추가합니다.

```json
{
  "status": "final",
  "score": { "home": 4, "away": 3 },
  "overtime": true,
  "periods": [
    { "home": 1, "away": 2 },
    { "home": 1, "away": 0 },
    { "home": 1, "away": 1 },
    { "home": 1, "away": 0 }
  ]
}
```

**연장전 승점 규칙**:
- 이긴 팀: W +1 (3점)
- 진 팀: OTL +1 (1점) — 정규시간 패와 다름 (0점)

#### 개인 통계 없을 때
선수 기록이 없는 경우 `players`를 `null`로 두면 됩니다:

```json
{
  "status": "final",
  "score": { "home": 5, "away": 3 },
  "overtime": false,
  "periods": [
    { "home": 2, "away": 1 },
    { "home": 1, "away": 2 },
    { "home": 2, "away": 0 }
  ],
  "players": null
}
```

이 경우 팀 순위는 정상 반영되지만, 개인 통계(Points/Goals/Assists)에는 표시되지 않습니다.

### Step 3: 커밋 & 푸시

```bash
git add results.json
git commit -m "result: 0308 고려대 5-3 성균관대"
git push
```

1~2분 후 GitHub Pages 자동 배포 → 사이트에 반영

### 자동 합산 (코드 수정 불필요)

`standings.html`이 `results.json`을 fetch하여 자동 계산:
- **팀 순위**: GP, W, L, OTL, PTS(승점), GF(득점), GA(실점), DIFF(득실차)
- **개인 Points**: 전 경기 골+어시 합산
- **개인 Goals**: 전 경기 골 합산
- **개인 Assists**: 전 경기 어시 합산
- **정렬**: 승점 → 골득실 → 득점순 (팀), 포인트 → 골 순 (개인)

### 에이전트에게 기록 요청하기

기록지 사진이나 텍스트를 에이전트에게 전달하고 아래와 같이 요청합니다:

```
이 기록지를 파싱해서 results.json에 반영해줘.
Game ID: 0308-korea-skku
```

에이전트가 자동으로:
1. 기록지에서 스코어, 피리어드, 선수 통계 추출
2. `results.json`의 해당 경기 업데이트
3. `git commit & push`
4. 배포 확인

---

## 사진 갤러리 설정 방법

### 개요
경기 사진을 Google Drive에 올리고, `photos.json`에 폴더 ID를 등록하면
갤러리 페이지에 자동으로 표시됩니다.

### Step 1: Google Cloud 프로젝트 설정 (최초 1회)

1. [Google Cloud Console](https://console.cloud.google.com/) 접속
2. 새 프로젝트 생성 (이름: `college-hockey-2026`)
3. **APIs & Services** → **Library** → **Google Drive API** 검색 → **Enable**
4. **APIs & Services** → **Credentials** → **Create Credentials** → **API Key**
5. API Key 복사
6. **API Key 제한 설정** (보안):
   - **Application restrictions** → **HTTP referrers**
   - 허용 리퍼러 추가:
     ```
     lidge-jun.github.io/*
     localhost:*
     127.0.0.1:*
     ```
   - **API restrictions** → **Restrict key** → **Google Drive API**만 선택
7. `photos.json`의 `apiKey`에 붙여넣기

```json
{
  "apiKey": "AIzaSy_YOUR_API_KEY_HERE",
  "games": { ... }
}
```

### Step 2: 경기별 사진 업로드

1. **Google Drive에서 폴더 생성**
   - 최상위에 `college-hockey-photos` 폴더 생성 (정리용)
   - 그 안에 경기별 폴더 생성: `0308-korea-skku`

2. **사진 업로드**
   - 해당 폴더에 사진 드래그 & 드롭
   - 지원 형식: JPG, PNG, HEIC (Drive가 자동 변환)

3. **폴더 공유 설정**
   - 폴더 우클릭 → **Share** → **General access** → **Anyone with the link** → **Viewer**
   - 또는 최상위 `college-hockey-photos` 폴더만 공유하면 하위 폴더 전체 적용

4. **폴더 ID 추출**
   - 폴더 URL: `https://drive.google.com/drive/folders/1AbCdEfGhIjKlMnOpQrStUvWxYz`
   - 폴더 ID: `1AbCdEfGhIjKlMnOpQrStUvWxYz` (마지막 경로 부분)

### Step 3: photos.json에 등록

```json
{
  "apiKey": "AIzaSy...",
  "games": {
    "0308-korea-skku": "1AbCdEfGhIjKlMnOpQrStUvWxYz",
    "0308-yonsei-kwu": "",
    ...
  }
}
```

빈 문자열(`""`)은 아직 사진이 없는 경기. 갤러리에 표시되지 않음.

### Step 4: 커밋 & 푸시

```bash
git add photos.json
git commit -m "photos: 0308 고려대 vs 성균관대 사진 추가"
git push
```

### Google Drive API URL 패턴 (참고)

| 용도 | URL |
|------|-----|
| 파일 목록 | `https://www.googleapis.com/drive/v3/files?q='FOLDER_ID'+in+parents&fields=files(id,name,mimeType)&key=API_KEY` |
| 썸네일 (400px) | `https://drive.google.com/thumbnail?id=FILE_ID&sz=w400` |
| 원본 보기 | `https://drive.google.com/uc?export=view&id=FILE_ID` |
| 다운로드 | `https://drive.google.com/uc?export=download&id=FILE_ID` |

### 에이전트에게 사진 등록 요청하기

```
이 경기 사진들을 갤러리에 추가해줘.
Game ID: 0308-korea-skku
Google Drive 폴더 링크: https://drive.google.com/drive/folders/1AbCdEfGhIjKlMnOpQrStUvWxYz
```

에이전트가 자동으로:
1. URL에서 폴더 ID 추출
2. `photos.json` 업데이트
3. `git commit & push`

---

## 순위 계산 규칙

| 항목 | 규칙 |
|------|------|
| 승점 | W=3, OTL=1, L=0 |
| 팀 순위 | 승점 → 골득실(GF-GA) → 득점(GF) |
| 개인 포인트 | G + A |
| 연장전(OT) | 진 팀은 OTL (1점), 이긴 팀은 W (3점) |

---

## 개발 브랜치 전략

- `main`: 공개 배포 브랜치 (GitHub Pages 소스)
- `dev`: 개발 중인 기능 작업 브랜치

```bash
# 개발 시작
git checkout dev

# 작업 완료 후 main에 머지
git checkout main
git merge dev
git push
```

---

## 캘린더 구독

| 구독 대상 | URL |
|-----------|-----|
| 전체 경기 | `webcal://lidge-jun.github.io/college-hockey-2026/cal/all-games.ics` |
| 고려대 | `webcal://lidge-jun.github.io/college-hockey-2026/cal/tigris.ics` |
| 연세대 | `webcal://lidge-jun.github.io/college-hockey-2026/cal/titans.ics` |
| 성균관대 | `webcal://lidge-jun.github.io/college-hockey-2026/cal/kingo-leafs.ics` |
| 서울대 | `webcal://lidge-jun.github.io/college-hockey-2026/cal/capitals.ics` |
| 광운대 | `webcal://lidge-jun.github.io/college-hockey-2026/cal/ice-unicorns.ics` |

---

## 기술 스택

- **프론트엔드**: Vanilla HTML/CSS/JS (프레임워크 없음)
- **데이터**: JSON 파일 (results.json, photos.json)
- **사진 저장**: Google Drive + Drive API v3
- **배포**: GitHub Pages (main 브랜치)
- **캘린더**: 정적 ICS 파일 + webcal:// 프로토콜
