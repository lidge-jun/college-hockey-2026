# Phase 0: 데이터 시스템 + 갤러리 백엔드 세팅

## 목표
1. 경기 결과를 JSON에 기록하면 순위표가 자동 합산되는 시스템 구축
2. 사진 갤러리용 Google Drive API + photos.json 세팅

백엔드/DB 없이 정적 JSON 파일 + Google Drive API만으로 동작.

## 왜 JSON인가 (SQLite가 아닌 이유)
- GitHub Pages = 정적 사이트 → 서버 없음 → SQLite 읽기 불가
- 20경기 5팀 규모 → JSON이면 충분
- Git에 커밋되므로 히스토리 자동 추적
- 에이전트가 기록지 받으면 → JSON 수정 → commit/push → 끝

## 데이터 구조

### `results.json` (NEW)
```json
{
  "games": [
    {
      "id": "0308-korea-skku",
      "date": "2026-03-08",
      "home": "고려대",
      "away": "성균관대",
      "venue": "고대링크",
      "status": "scheduled",
      "score": null,
      "periods": null,
      "players": null
    },
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
          { "name": "이퍽", "num": "#7", "team": "고려대", "count": 1 }
        ],
        "assists": [
          { "name": "박어시", "num": "#14", "team": "고려대", "count": 2 }
        ]
      }
    }
  ]
}
```

### `photos.json` (NEW)
```json
{
  "apiKey": "",
  "games": {
    "0308-korea-skku": "",
    "0308-yonsei-kwu": "",
    "0313-snu-kwu": "",
    "0313-kwu-snu": "",
    "0314-yonsei-snu": "",
    "0315-skku-yonsei": "",
    "0315-korea-snu": "",
    "0320-snu-skku": "",
    "0322-korea-yonsei": "",
    "0328-kwu-yonsei": "",
    "0329-skku-kwu": "",
    "0403-snu-yonsei": "",
    "0404-yonsei-skku": "",
    "0404-kwu-korea": "",
    "0405-skku-snu": "",
    "0405-korea-kwu": "",
    "0410-snu-korea": "",
    "0419-skku-korea": "",
    "0425-kwu-skku": "",
    "0503-yonsei-korea": ""
  }
}
```

### 경기 기록 워크플로우

```
기록지 (사진/텍스트)
    ↓
에이전트가 파싱
    ↓
results.json 업데이트 (status: "final", score, players 채움)
    ↓
git commit & push
    ↓
GitHub Pages 자동 배포
    ↓
standings.html이 results.json fetch → 자동 합산 렌더링
```

### 에이전트에게 줄 기록지 형식 예시
```
경기: 3/8 고려대 vs 성균관대
결과: 5-3 (2-1, 1-2, 2-0)
골: 김하키#10(고려대)x2, 이퍽#7(고려대)x1, 박골#3(성균관대)x2, ...
어시: 박어시#14(고려대)x2, ...
```

### 사진 올리는 워크플로우
```
Google Drive에 경기별 폴더 생성 + 사진 업로드
    ↓
폴더를 "링크가 있는 모든 사용자"에게 뷰어 공유
    ↓
폴더 URL에서 ID 추출
    ↓
photos.json에 폴더 ID 등록
    ↓
commit & push → 갤러리에 자동 표시
```

## 파일 변경 목록

| Action | File | Description |
|--------|------|-------------|
| NEW | `results.json` | 20경기 데이터 (초기값: 모두 scheduled) |
| NEW | `photos.json` | 20경기 → Google Drive 폴더 ID 매핑 |
| MODIFY | `standings.html` | JS 하드코딩 → results.json fetch 후 자동 합산 |
| MODIFY | `index.html` | 경기 카드에 스코어 표시 (완료된 경기만) |
| NEW | `README.md` | 프로젝트 구조, 경기 기록 방법, 사진 업로드 방법, API 세팅 상세 문서 |

## standings.html 변경 상세

### Before (현재)
```js
const TEAMS = [
  { name:'고려대', en:'TIGRIS', c:'#9B2335', gp:0, w:0, l:0, otl:0, gf:0, ga:0 },
  // ... 하드코딩
];
```

### After
```js
async function loadResults() {
  const res = await fetch('results.json');
  const data = await res.json();
  const finals = data.games.filter(g => g.status === 'final');

  // 팀별 자동 합산
  const teams = {}; // gp, w, l, otl, gf, ga 계산
  // 선수별 자동 합산
  const playerGoals = {};   // 경기별 골 합산
  const playerAssists = {}; // 경기별 어시 합산

  renderTeam(teams);
  renderPoints(playerGoals, playerAssists);
}
```

### 자동 합산 로직
- **승점**: W=3, OTL=1, L=0
- **팀 순위**: 승점 → 골득실 → 득점순
- **개인 통계**: 경기별 골/어시 합산 → 포인트(G+A) 자동 계산
- **Overtime**: `overtime: true`이면 진 팀에 OTL +1

## index.html 변경 상세
- `results.json` fetch
- 완료된 경기 카드에 스코어 배지 표시: `5 - 3 FINAL`
- 예정된 경기는 현재와 동일

## Google Drive API 세팅
1. Google Cloud Console → 프로젝트 생성
2. Google Drive API 활성화
3. API Key 생성
4. HTTP 리퍼러 제한: `lidge-jun.github.io/*`
5. photos.json의 `apiKey`에 입력

## Google Drive URL 패턴
- 목록: `googleapis.com/drive/v3/files?q='FOLDER_ID'+in+parents&key=KEY`
- 썸네일: `drive.google.com/thumbnail?id=FILE_ID&sz=w400`
- 원본: `drive.google.com/uc?export=view&id=FILE_ID`
- 다운로드: `drive.google.com/uc?export=download&id=FILE_ID`

## 의존성
- 없음 (순수 HTML/CSS/JS + JSON fetch)
- 외부 라이브러리 없음
