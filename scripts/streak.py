"""Builds assets/streak.svg from GitHub's own contribution calendar.

Run locally:  GITHUB_TOKEN=$(gh auth token) python scripts/streak.py
With a PAT for the profile owner (ACCESS_TOKEN in CI) private contributions are included.
Without a token the existing SVG is left untouched.
"""
import os
import sys
from datetime import date, datetime, timedelta, timezone
from html import escape

from neofetch import ASSETS, USER, gql

BG, BORDER, FG, MUTED, BLUE, ORANGE = "#080808", "#1a1a1a", "#f5f5f5", "#6b6b6b", "#0066ff", "#ff5500"


def fetch_days(token):
    created = gql(token, "query($l:String!){user(login:$l){createdAt}}", {"l": USER})["user"]["createdAt"]
    first = datetime.fromisoformat(created.replace("Z", "+00:00")).year
    today = datetime.now(timezone.utc).date()
    days = {}
    for year in range(first, today.year + 1):
        weeks = gql(token, """
        query($l: String!, $from: DateTime!, $to: DateTime!) {
          user(login: $l) { contributionsCollection(from: $from, to: $to) {
            contributionCalendar { weeks { contributionDays { date contributionCount } } }
          } }
        }""", {"l": USER, "from": f"{year}-01-01T00:00:00Z", "to": f"{year}-12-31T23:59:59Z"}
        )["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
        for w in weeks:
            for d in w["contributionDays"]:
                day = date.fromisoformat(d["date"])
                if day.year == year and day <= today:
                    days[day] = d["contributionCount"]
    return days, today


def streaks(days, today):
    best, best_range, run, start = 0, None, 0, None
    for day in sorted(days):
        if days[day]:
            if run == 0:
                start = day
            run += 1
            if run > best:
                best, best_range = run, (start, day)
        else:
            run = 0
    # Today may not have a contribution yet; the streak is still alive until the day ends.
    end = today if days.get(today) else today - timedelta(days=1)
    cur, cur_start = 0, None
    day = end
    while days.get(day):
        cur, cur_start = cur + 1, day
        day -= timedelta(days=1)
    return cur, (cur_start, end) if cur else None, best, best_range


def span(r):
    if not r:
        return ""
    fmt = lambda d: f"{d:%b} {d.day}"
    return fmt(r[0]) if r[0] == r[1] else f"{fmt(r[0])} - {fmt(r[1])}"


def render(days, today):
    total = sum(days.values())
    first = min(days)
    cur, cur_r, best, best_r = streaks(days, today)
    cols = [(total, "Total Contributions", f"{first:%b} {first.day}, {first.year} - Present", FG),
            (cur, "Current Streak", span(cur_r) or "No active streak", BLUE),
            (best, "Longest Streak", span(best_r), FG)]
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="495" height="195" viewBox="0 0 495 195" '
           f'font-family="\'Segoe UI\', Ubuntu, sans-serif">',
           f'<rect x="0.5" y="0.5" width="494" height="194" rx="4.5" fill="{BG}" stroke="{BORDER}"/>']
    for i, (num, label, sub, color) in enumerate(cols):
        cx = 82.5 + i * 165
        if i:
            out.append(f'<line x1="{i * 165}" y1="28" x2="{i * 165}" y2="167" stroke="{BORDER}"/>')
        if i == 1:
            out.append(f'<circle cx="{cx}" cy="71" r="40" fill="none" stroke="{BLUE}" stroke-width="5"/>')
            out.append(f'<path d="M{cx} 21c4 6 7 9 7 14a7 7 0 0 1-14 0c0-3 2-5 3-7 1 3 3 4 4 4 0-4-2-7 0-11z" fill="{ORANGE}"/>')
        out.append(f'<text x="{cx}" y="82" text-anchor="middle" font-size="28" font-weight="700" fill="{FG}">{num:,}</text>')
        out.append(f'<text x="{cx}" y="{128 if i != 1 else 135}" text-anchor="middle" font-size="14" '
                   f'font-weight="{700 if i == 1 else 400}" fill="{color}">{escape(label)}</text>')
        out.append(f'<text x="{cx}" y="{153 if i != 1 else 157}" text-anchor="middle" font-size="12" fill="{MUTED}">{escape(sub)}</text>')
    out.append("</svg>")
    return "\n".join(out) + "\n"


def main():
    token = os.environ.get("ACCESS_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not token:
        print("no token; leaving assets/streak.svg as is", file=sys.stderr)
        return
    try:
        days, today = fetch_days(token)
    except Exception as e:
        print(f"warning: streak fetch failed ({e}); keeping existing card", file=sys.stderr)
        return
    (ASSETS / "streak.svg").write_text(render(days, today), encoding="utf-8")
    print(streaks(days, today)[::2], sum(days.values()))


if __name__ == "__main__":
    main()
