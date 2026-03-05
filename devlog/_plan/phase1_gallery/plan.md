# Phase 1: 경기 사진 갤러리

## 목표
경기별 사진을 Google Drive 공유 폴더에 올리면 웹사이트에서 자동으로 보여주는 갤러리.
**경기당 여러 폴더(촬영자) 지원** — 서로 다른 팀/사람이 각자 폴더 공유 가능.

## 의존성
- Phase 0에서 세팅 완료:
  - `photos.json` (경기 ID → Drive 폴더 배열 매핑) — **구조 변경 필요**
  - Google Drive API Key
  - 경기 ID 체계 (`results.json`과 공유)
- Phase 1은 프론트엔드(gallery.html, gallery-detail.html) 구현 + photos.json 구조 변경

## photos.json 구조 변경 (단일 문자열 → 배열)

### Before (Phase 0 현재)
```json
{
  "apiKey": "",
  "games": {
    "0308-korea-skku": ""
  }
}
```

### After (멀티 폴더)
```json
{
  "apiKey": "",
  "games": {
    "0308-korea-skku": [
      { "folderId": "1AbCdEfGhIjKlMnOpQrSt", "label": "고려대 촬영팀" },
      { "folderId": "1XyZaBcDeFgHiJkLmNoPq", "label": "성균관대 매니저" }
    ],
    "0308-yonsei-kwu": []
  }
}
```
- 빈 배열 `[]` = 아직 사진 없음 → 갤러리에 미표시
- label = 촬영자/출처 (Drive 폴더 공유 링크 텍스트로도 대체 가능)

## 데이터 흐름

```
여러 Google Drive 공유 폴더 (경기당 1~N개)
    ↓
photos.json에 폴더 배열 등록
    ↓
gallery.html이 각 폴더별 Drive API fetch
    ↓
메인: 전 폴더 사진 합쳐서 랜덤 10장 → 스와이프 스트립
상세: 폴더(촬영자)별 섹션 분리 → 그리드 표시
```

## 디자인

### 메인 갤러리 (gallery.html)
- 상단: Header + Nav (Schedule / Standings / **Gallery**)
- 팀 탭: All / Tigris / Titans / Kingo Leafs / Capitals / Unicorns
- Sticky 드롭다운: 경기 선택 → 해당 블록으로 스크롤 점프
- 사진이 있는 경기만 블록 표시
  - 듀얼 컬러 스트라이프 (홈 위 / 어웨이 아래)
  - 양팀 이름 각각 팀 컬러
  - 날짜 · 장소
  - 사진 개수 배지 (모든 폴더 합산)
  - 가로 스와이프 사진 스트립 (전 폴더 합쳐서 랜덤 최대 10장, scroll-snap)
  - `+` 버튼 → gallery-detail.html?game=GAME_ID
- 블록 간 8px 간격
- backdrop-blur 드롭다운
- 사진 하단 그라데이션 오버레이
- 다크/라이트 테마 동기화

### 상세 페이지 (gallery-detail.html)
- URL: `gallery-detail.html?game=0308-korea-skku`
- 경기 정보 헤더 (듀얼 스트라이프, 팀명, 스코어)
- **폴더(촬영자)별 섹션 분리**:
  ```
  ┌──────────────────────────────────┐
  │ 📁 고려대 촬영팀 (20장)          │
  │ drive.google.com/drive/folders/… │
  │ 📷 📷 📷 📷 📷 📷 📷 📷        │
  │ 📷 📷 📷 📷 📷 📷 📷 📷        │
  │                                  │
  │ 📁 성균관대 매니저 (12장)         │
  │ drive.google.com/drive/folders/… │
  │ 📷 📷 📷 📷 📷 📷 📷 📷        │
  │ 📷 📷 📷 📷                     │
  └──────────────────────────────────┘
  ```
  - 각 섹션 헤더: label + Drive 폴더 링크 (클릭 가능)
  - 사진 그리드 (auto-fill, 3:2 비율)
- 라이트박스 슬라이드쇼
  - 키보드 ← → / ESC
  - 모바일 터치 스와이프
  - 사진 카운터 (3 / 12)
- 개별 다운로드 버튼
- ← 뒤로가기 → gallery.html

## 파일 변경 목록

| Action | File | Description |
|--------|------|-------------|
| REWRITE | `gallery.html` | Firebase 갤러리 → Google Drive 멀티폴더 갤러리 |
| NEW | `gallery-detail.html` | 경기별 상세 (폴더별 섹션) |
| MODIFY | `photos.json` | 문자열 값 → 배열 구조 + game ID 변경 반영 |
| MODIFY | `index.html` | 일정 변경: 광운대vs고려대 4/4→4/11, 연대vs성균관 note 제거 |
| MODIFY | `results.json` | game ID 변경: 0404-kwu-korea → 0411-kwu-korea, 날짜 수정 |
| MODIFY | `cal/*.ics` | ICS 파일 일정 반영 (all-games, tigris, ice-unicorns) |
| DELETE | `preview-gallery.html` | 프로토타입 삭제 |
| DELETE | `preview-photo-manager.html` | 매니저 프리뷰 삭제 |

*Note: nav에 Gallery 링크는 이미 추가되어 있음 (Phase 0 이전)*

## 일정 변경 사항 (2026-03-05 확인)

### 변경 1: 광운대(홈) vs 고려대(어웨이)
- **Before**: `{ d:'2026-04-04', home:'광운대', away:'고려대', v:'kwangwoon', time:'17:30–19:00' }`
- **After**: `{ d:'2026-04-11', home:'광운대', away:'고려대', v:'kwangwoon', time:'17:30–19:00' }`
- Game ID: `0404-kwu-korea` → `0411-kwu-korea`
- 수정 대상: index.html (G 배열), results.json, photos.json, cal/all-games.ics, cal/tigris.ics, cal/ice-unicorns.ics

### 변경 2: 연세대(홈) vs 성균관대(어웨이) note 제거
- **Before**: `{ d:'2026-04-04', home:'연세대', away:'성균관대', v:'mokdong', time:'00:30–02:00', note:'4/11 가능' }`
- **After**: `{ d:'2026-04-04', home:'연세대', away:'성균관대', v:'mokdong', time:'00:30–02:00' }`
- Game ID 변경 없음
- 수정 대상: index.html (G 배열), cal/all-games.ics, cal/titans.ics, cal/kingo-leafs.ics

## Google Drive API 패턴
- 목록: `https://www.googleapis.com/drive/v3/files?q='FOLDER_ID'+in+parents+and+trashed=false+and+mimeType+contains+'image/'&fields=files(id,name,mimeType),nextPageToken&pageSize=100&key=API_KEY`
- 페이지네이션: 응답에 `nextPageToken`이 있으면 `&pageToken=TOKEN` 추가하여 반복 요청
- 썸네일: `https://drive.google.com/thumbnail?id=FILE_ID&sz=w400`
- 원본: `https://drive.google.com/uc?export=view&id=FILE_ID`
- 다운로드: `https://drive.google.com/uc?export=download&id=FILE_ID`

## results.json 스코어 연동 스키마
상세 페이지에서 스코어 표시 시 사용하는 필드:
```js
// results.json의 game 객체에서:
game.status    // "scheduled" | "final"
game.score     // { home: number, away: number } | null
game.overtime  // boolean
```
- `status !== 'final'` 이면 스코어 미표시
- `overtime === true` 이면 "OT" 라벨 추가

## photos.json 스키마 가드
gallery.html 로딩 시 normalizer 적용:
```js
function normalizePhotos(games) {
  const result = {};
  for (const [id, val] of Object.entries(games)) {
    if (Array.isArray(val)) result[id] = val;
    else if (typeof val === 'string' && val) result[id] = [{ folderId: val, label: '' }];
    else result[id] = [];
  }
  return result;
}
```
- 문자열(legacy) → 단일 폴더 배열로 자동 변환
- 빈 문자열/null → 빈 배열
- 이미 배열 → 그대로 사용

## 반응형
- 모바일: 사진 스트립 160px, 그리드 2열
- 데스크톱: 사진 스트립 200px, 그리드 auto-fill(min 180px)
