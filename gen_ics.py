import os
from datetime import datetime, timedelta

TEAMS = {
    '\uace0\ub824\ub300':   {'en': 'TIGRIS',       'file': 'tigris',       'rid': 'korea'},
    '\uc5f0\uc138\ub300':   {'en': 'TITANS',       'file': 'titans',       'rid': 'yonsei'},
    '\uc131\uade0\uad00\ub300': {'en': 'KINGO_LEAFS',  'file': 'kingo-leafs',  'rid': 'skku'},
    '\uc11c\uc6b8\ub300':   {'en': 'CAPITALS',     'file': 'capitals',     'rid': 'snu'},
    '\uad11\uc6b4\ub300':   {'en': 'ICE_UNICORNS', 'file': 'ice-unicorns', 'rid': 'kwu'},
}

VENUES = {
    'mokdong': '\ubaa9\ub3d9 \uc544\uc774\uc2a4\ub9c1\ud06c',
    'korea': '\uace0\ub824\ub300 \uc544\uc774\uc2a4\ub9c1\ud06c',
    'kwangwoon': '\uad11\uc6b4\ub300 \uc544\uc774\uc2a4\ub9c1\ud06c',
    'suwon': '\uc218\uc6d0 \uc544\uc774\uc2a4\ud558\uc6b0\uc2a4',
}

GAMES = [
    ('2026-03-08','\uace0\ub824\ub300','\uc131\uade0\uad00\ub300','korea','22:30','24:00'),
    ('2026-03-08','\uc5f0\uc138\ub300','\uad11\uc6b4\ub300','mokdong','07:30','09:00'),
    ('2026-03-13','\uc11c\uc6b8\ub300','\uad11\uc6b4\ub300','mokdong','23:00','01:00'),
    ('2026-03-31','\uad11\uc6b4\ub300','\uc11c\uc6b8\ub300','kwangwoon','20:30','22:00'),
    ('2026-03-14','\uc5f0\uc138\ub300','\uc11c\uc6b8\ub300','mokdong','00:30','02:00'),
    ('2026-03-15','\uc131\uade0\uad00\ub300','\uc5f0\uc138\ub300','suwon','22:00','23:30'),
    ('2026-03-15','\uace0\ub824\ub300','\uc11c\uc6b8\ub300','korea','22:30','24:00'),
    ('2026-03-20','\uc11c\uc6b8\ub300','\uc131\uade0\uad00\ub300','mokdong','23:00','01:00'),
    ('2026-03-22','\uace0\ub824\ub300','\uc5f0\uc138\ub300','korea','22:30','24:00'),
    ('2026-03-28','\uad11\uc6b4\ub300','\uc5f0\uc138\ub300','kwangwoon','17:30','19:00'),
    ('2026-03-29','\uc131\uade0\uad00\ub300','\uad11\uc6b4\ub300','suwon','22:00','23:30'),
    ('2026-04-17','\uc11c\uc6b8\ub300','\uc5f0\uc138\ub300','mokdong','23:00','01:00'),
    ('2026-04-04','\uc5f0\uc138\ub300','\uc131\uade0\uad00\ub300','mokdong','00:30','02:00'),
    ('2026-04-04','\uad11\uc6b4\ub300','\uace0\ub824\ub300','kwangwoon','17:30','19:00'),
    ('2026-04-05','\uc131\uade0\uad00\ub300','\uc11c\uc6b8\ub300','suwon','22:00','23:30'),
    ('2026-04-05','\uace0\ub824\ub300','\uad11\uc6b4\ub300','korea','22:30','24:00'),
    ('2026-04-24','\uc11c\uc6b8\ub300','\uace0\ub824\ub300','mokdong','23:00','01:00'),
    ('2026-04-19','\uc131\uade0\uad00\ub300','\uace0\ub824\ub300','suwon','22:00','23:30'),
    ('2026-04-25','\uad11\uc6b4\ub300','\uc131\uade0\uad00\ub300','kwangwoon','17:30','19:00'),
    ('2026-05-03','\uc5f0\uc138\ub300','\uace0\ub824\ub300','mokdong','07:30','09:00'),
]

VTIMEZONE = """BEGIN:VTIMEZONE
TZID:Asia/Seoul
X-LIC-LOCATION:Asia/Seoul
BEGIN:STANDARD
TZOFFSETFROM:+0900
TZOFFSETTO:+0900
TZNAME:KST
DTSTART:19700101T000000
END:STANDARD
END:VTIMEZONE"""

def make_dt(date_str, time_str, is_end=False, start_h=None):
    y, m, d = map(int, date_str.split('-'))
    h, mi = map(int, time_str.split(':'))
    dt = datetime(y, m, d)
    if h >= 24:
        dt += timedelta(days=1)
        h = h % 24
        if h == 0 and mi == 0:
            mi = 1
    elif is_end and start_h is not None and h < start_h:
        dt += timedelta(days=1)
        if h == 0 and mi == 0:
            mi = 1
    dt = dt.replace(hour=h, minute=mi)
    return dt

def fmt(dt):
    return dt.strftime('%Y%m%dT%H%M00')

def team_rid(name):
    return TEAMS[name]['rid']

outdir = '/tmp/college-hockey-2026/cal'
os.makedirs(outdir, exist_ok=True)

for team_name, info in TEAMS.items():
    lines = []
    lines.append('BEGIN:VCALENDAR')
    lines.append('VERSION:2.0')
    lines.append('PRODID:-//CollegeHockey2026//EN')
    lines.append('CALSCALE:GREGORIAN')
    lines.append('METHOD:PUBLISH')
    lines.append('X-WR-CALNAME:' + team_name + ' ' + info['en'] + ' 2026')
    lines.append('X-WR-TIMEZONE:Asia/Seoul')
    for vtz_line in VTIMEZONE.split('\n'):
        lines.append(vtz_line)
    for d, home, away, venue, t_start, t_end in GAMES:
        if home != team_name and away != team_name:
            continue
        sh = int(t_start.split(':')[0])
        start_dt = make_dt(d, t_start)
        end_dt = make_dt(d, t_end, is_end=True, start_h=sh)
        ha = 'HOME' if home == team_name else 'AWAY'
        opp = away if home == team_name else home
        title = team_name + ' vs ' + opp + ' (' + ha + ')'
        loc = VENUES[venue]
        uid = 'hockey2026-' + d + '-' + team_rid(home) + '-' + team_rid(away) + '@collegehockey2026'
        lines.append('BEGIN:VEVENT')
        lines.append('DTSTART;TZID=Asia/Seoul:' + fmt(start_dt))
        lines.append('DTEND;TZID=Asia/Seoul:' + fmt(end_dt))
        lines.append('SUMMARY:' + title)
        lines.append('LOCATION:' + loc)
        lines.append('UID:' + uid)
        lines.append('END:VEVENT')
    lines.append('END:VCALENDAR')
    path = os.path.join(outdir, info['file'] + '.ics')
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\r\n'.join(lines) + '\r\n')
    print('ok ' + info['file'] + '.ics')

lines = []
lines.append('BEGIN:VCALENDAR')
lines.append('VERSION:2.0')
lines.append('PRODID:-//CollegeHockey2026//EN')
lines.append('CALSCALE:GREGORIAN')
lines.append('METHOD:PUBLISH')
lines.append('X-WR-CALNAME:2026 College Hockey League')
lines.append('X-WR-TIMEZONE:Asia/Seoul')
for vtz_line in VTIMEZONE.split('\n'):
    lines.append(vtz_line)
for d, home, away, venue, t_start, t_end in GAMES:
    sh = int(t_start.split(':')[0])
    start_dt = make_dt(d, t_start)
    end_dt = make_dt(d, t_end, is_end=True, start_h=sh)
    title = home + ' vs ' + away
    loc = VENUES[venue]
    uid = 'hockey2026-' + d + '-' + team_rid(home) + '-' + team_rid(away) + '@collegehockey2026'
    lines.append('BEGIN:VEVENT')
    lines.append('DTSTART;TZID=Asia/Seoul:' + fmt(start_dt))
    lines.append('DTEND;TZID=Asia/Seoul:' + fmt(end_dt))
    lines.append('SUMMARY:' + title)
    lines.append('LOCATION:' + loc)
    lines.append('UID:' + uid)
    lines.append('END:VEVENT')
lines.append('END:VCALENDAR')
with open(os.path.join(outdir, 'all.ics'), 'w', encoding='utf-8') as f:
    f.write('\r\n'.join(lines) + '\r\n')
print('ok all.ics')
