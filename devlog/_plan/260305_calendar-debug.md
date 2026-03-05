# 260305 — Calendar Subscription Debug

## Problem
Google Calendar shows "Unable to add calendar. Check the URL." when clicking the Google Cal button.
Apple Calendar also fails from local file:// but that's expected.

## Root Cause Investigation

### Evidence Collected
1. **ICS file is valid**: `curl -sI` returns HTTP 200, `content-type: text/calendar`, CORS enabled
2. **VTIMEZONE present**: ✅ Asia/Seoul timezone block included
3. **CRLF line endings**: ✅ Verified with `xxd`
4. **ASCII UIDs**: ✅ No Korean in UID fields
5. **GitHub Pages serving correctly**: `access-control-allow-origin: *`

### Root Cause: Google Calendar `cid=` rejects HTTPS URLs
- **Known Google bug** (confirmed on Stack Overflow, multiple reports 2023-2025)
- `cid=https://...` → "Unable to add calendar"
- `cid=webcal://...` → may work (needs URL encoding)
- Manual "Settings → Add Calendar → From URL" with same HTTPS URL → works fine
- Reference: https://stackoverflow.com/questions/79772521

### Fix Options
1. **Use `webcal://` in `cid` parameter** + URL encode: `cid=webcal%3A%2F%2Flidge-jun.github.io%2F...`
2. **Link to "From URL" settings page** instead: `https://calendar.google.com/calendar/u/0/r/settings/addbyurl`
3. **Combine both**: webcal:// cid link + fallback instruction text

### Apple Calendar
- `webcal://` links work only from HTTPS pages (not file://)
- GitHub Pages should work correctly
- Status: needs live verification after fix
