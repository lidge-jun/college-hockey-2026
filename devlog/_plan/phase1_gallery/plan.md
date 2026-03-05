# Phase 1: 경기 사진 갤러리

## 목표
경기별 사진을 Google Drive 공유 폴더에 올리면 웹사이트에서 자동으로 보여주는 갤러리.

## 의존성
- Phase 0에서 세팅 완료된 항목:
  - `photos.json` (경기 ID → Drive 폴더 ID 매핑)
  - Google Drive API Key
  - 경기 ID 체계 (`results.json`과 공유)
- Phase 1은 프론트엔드(gallery.html, gallery-detail.html) 구현만 담당

## 데이터 흐름

```
Google Drive 공유 폴더 (경기당 1개)
    ↓
photos.json에 폴더 ID 등록
    ↓
gallery.html이 Google Drive API로 이미지 목록 fetch
    ↓
썸네일 URL 자동 생성 → 가로 스크롤 스트립 렌더링
```

## 디자인 (프리뷰 v2 확정)

### 메인 갤러리 (gallery.html)
- 상단: Header + Nav (Schedule / Standings / **Gallery**)
- 팀 탭: All / Tigris / Titans / Kingo Leafs / Capitals / Unicorns
- Sticky 드롭다운: 경기 선택 → 해당 블록으로 스크롤 점프
- 20개 game blocks 세로 배치
  - 듀얼 컬러 스트라이프 (홈 위 / 어웨이 아래)
  - 양팀 이름 각각 팀 컬러
  - 날짜 · 시간 · 장소
  - 사진 개수 배지
  - 가로 스와이프 사진 스트립 (최대 10장)
  - `+` 버튼 → gallery-detail.html
- 블록 간 8px 간격
- backdrop-blur 드롭다운
- 사진 하단 그라데이션 오버레이
- 다크/라이트 테마 동기화

### 상세 페이지 (gallery-detail.html)
- 경기 정보 헤더 (듀얼 스트라이프, 팀명, 스코어(Phase0에서 가져옴))
- 전체 사진 그리드 (auto-fill, 4:3 비율)
- 라이트박스 슬라이드쇼
  - 키보드 ← → / ESC
  - 모바일 터치 스와이프
  - 사진 카운터 (3 / 12)
- 개별 다운로드 버튼
- ← 뒤로가기 → gallery.html

## 파일 변경 목록

| Action | File | Description |
|--------|------|-------------|
| NEW | `gallery.html` | 메인 갤러리 (~400줄) |
| NEW | `gallery-detail.html` | 경기별 상세 (~350줄) |
| NEW | `photos.json` | 경기 ID → Drive 폴더 ID 매핑 |
| MODIFY | `index.html` | nav에 Gallery 링크 추가 |
| MODIFY | `standings.html` | nav에 Gallery 링크 추가 |
| MODIFY | `README.md` | 사진 업로드 방법 문서 추가 |
| DELETE | `preview-gallery.html` | 프리뷰 파일 제거 |

## photos.json (NEW)
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

## Google Drive API 설정
1. Google Cloud Console → 프로젝트 생성
2. Google Drive API 활성화
3. API Key 생성
4. HTTP 리퍼러 제한 설정: `lidge-jun.github.io/*`
5. photos.json의 `apiKey`에 입력

## Google Drive 이미지 URL 패턴
- 목록: `https://www.googleapis.com/drive/v3/files?q='FOLDER_ID'+in+parents&fields=files(id,name,mimeType)&key=API_KEY`
- 썸네일: `https://drive.google.com/thumbnail?id=FILE_ID&sz=w400`
- 원본: `https://drive.google.com/uc?export=view&id=FILE_ID`
- 다운로드: `https://drive.google.com/uc?export=download&id=FILE_ID`

## 사진 올리는 방법 (README용)
1. Google Drive에 경기별 폴더 생성 (예: `0308 고려대vs성균관대`)
2. 폴더 우클릭 → 공유 → "링크가 있는 모든 사용자"에게 뷰어 권한
3. 폴더 URL에서 ID 추출:
   `https://drive.google.com/drive/folders/1ABCxyz...` → `1ABCxyz...`
4. `photos.json` 수정:
   ```json
   "0308-korea-skku": "1ABCxyz..."
   ```
5. commit & push → 자동 배포

## 반응형
- 모바일: 사진 스트립 160px/108px, 그리드 2열
- 데스크톱: 사진 스트립 200px/134px, 그리드 auto-fill
