# College Hockey 2026

2026 Korean university amateur ice hockey league schedule & standings website.

## Tech Stack
- Static HTML/CSS/JS (single-file pages)
- GitHub Pages deployment
- Python script for .ics calendar generation

## Project Structure
- `index.html` — Schedule page (calendar view, game list, venue info, team filter, calendar export)
- `standings.html` — Standings page (Team/Points/Goals/Assists tabs)
- `cal/` — Static .ics files per team for calendar subscription
- `gen_ics.py` — Python script to regenerate .ics files
- `.github/workflows/pages.yml` — GitHub Pages CI

## Teams (5)
| Korean | English | Color | ICS file |
|--------|---------|-------|----------|
| 고려대 | TIGRIS | #9B2335 (Crimson) | tigris.ics |
| 연세대 | TITANS | #1764E8 (Yonsei Blue) | titans.ics |
| 성균관대 | KINGO LEAFS | #3DB06B (Green) | kingo-leafs.ics |
| 서울대 | CAPITALS | #2A6BBE (SNU Blue) | capitals.ics |
| 광운대 | ICE UNICORNS | #843DA0 (Purple) | ice-unicorns.ics |

## Conventions
- ES Module style (no build step, vanilla JS)
- Dark/light theme via CSS variables + localStorage
- Calendar export: static .ics files with webcal:// (Apple) and Google Calendar subscribe URLs
- All times in KST (Asia/Seoul)

## Deployment
- Repo: `lidge-jun/college-hockey-2026`
- Live: https://lidge-jun.github.io/college-hockey-2026/
