# 260305 — Naver Map Location Buttons

## Goal
Add a location pin SVG button next to each game's venue info that opens Naver Map for that venue.

## Research

### Naver Map URL Format
- Web: `https://map.naver.com/p/search/{URL_encoded_query}`
- Works on both desktop and mobile (auto-redirects to app on mobile)
- No API key needed, just URL encoding

### Venues & Naver Map URLs

| Venue Key | Name | Address | Naver Map URL |
|-----------|------|---------|---------------|
| mokdong | 목동 아이스링크 | 서울 양천구 안양천로 939 | `https://map.naver.com/p/search/목동 실내아이스링크` |
| korea | 고려대 아이스링크 | 서울 성북구 안암로 145 | `https://map.naver.com/p/search/고려대학교 아이스링크` |
| kwangwoon | 광운대 아이스링크 | 서울 노원구 광운로 21 | `https://map.naver.com/p/search/광운대학교 아이스링크` |
| suwon | 수원 아이스하우스 | 경기 수원시 권선구 효탑로16번길 20 | `https://map.naver.com/p/search/수원 아이스하우스` |

### SVG Icon
Small location pin (📍) inline SVG, ~16x16, matching the existing design.

## Plan

### MODIFY: `index.html`

**1. Add `naver` field to venue data (V object, ~line 643-646)**
```js
// Before:
const V = {
  mokdong:   { name:'목동 아이스링크', short:'목동' },
  korea:     { name:'고려대 아이스링크', short:'고대링크' },
  kwangwoon: { name:'광운대 아이스링크', short:'광운대' },
  suwon:     { name:'수원 아이스하우스', short:'수원' },
};

// After:
const V = {
  mokdong:   { name:'목동 아이스링크', short:'목동', naver:'https://map.naver.com/p/search/목동 실내아이스링크' },
  korea:     { name:'고려대 아이스링크', short:'고대링크', naver:'https://map.naver.com/p/search/고려대학교 아이스링크' },
  kwangwoon: { name:'광운대 아이스링크', short:'광운대', naver:'https://map.naver.com/p/search/광운대학교 아이스링크' },
  suwon:     { name:'수원 아이스하우스', short:'수원', naver:'https://map.naver.com/p/search/수원 아이스하우스' },
};
```

**2. Add location pin SVG button in game card render (renderGames function)**

Find where venue name is rendered next to the time, add a small clickable pin icon that links to `V[g.v].naver`:

```html
<a href="${V[g.v].naver}" target="_blank" class="map-link" title="네이버 지도">
  <svg>...</svg>
</a>
```

**3. Add CSS for `.map-link`**
- Inline with venue text
- Subtle gray, hover highlight
- Small size (~16px)

## Risks
- None significant. Pure additive change (new field + new element).
- Naver Map search URLs are stable and don't require API keys.
- SVG icon is self-contained, no external dependencies.
