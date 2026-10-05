"""Builds assets/neofetch-dark.svg and assets/neofetch-light.svg.

Run locally:  GITHUB_TOKEN=$(gh auth token) python scripts/neofetch.py
In CI the workflow passes ACCESS_TOKEN (a PAT, sees private repos) or GITHUB_TOKEN.
Without a token the stats block falls back to the last values in assets/stats.json.
"""
import json
import os
import urllib.request
from datetime import date, datetime, timezone
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
USER = "N9601"
# Birthday drives the "Uptime" line. Leave as None to count from GitHub join date.
BIRTHDAY = None  # e.g. date(2007, 1, 1)

WIDTH = 60  # characters in the info column

INFO = [
    ("title", "nanda@kishore"),
    ("kv", "OS", "Windows 11, Android, Linux (WSL)"),
    ("kv", "Uptime", "{uptime}"),
    ("kv", "Host", "Verge Scales"),
    ("kv", "Kernel", "Full-Stack & AI Automation Engineer"),
    ("kv", "IDE", "VS Code, Claude Code"),
    ("gap",),
    ("kv", "Languages.Programming", "Go, TypeScript, Java, Python"),
    ("kv", "Languages.Systems", "C, C++, x86 Assembly, SQL"),
    ("kv", "Languages.Real", "English, Telugu, Hindi"),
    ("gap",),
    ("kv", "Building", "OrderFlow, SolderDB, PyroOS"),
    ("kv", "Hobbies.Software", "Android ROMs, Perf Tuning"),
    ("kv", "Hobbies.Analog", "Music, Films, Photography"),
    ("gap",),
    ("section", "Education"),
    ("kv", "B.Tech CSE", "VNR VJIET, 2026 - now"),
    ("kv", "Diploma CSE", "CGPA 9.18, top 1%"),
    ("gap",),
    ("section", "Contact"),
    ("kv", "Email", "nandakishorereddyg@outlook.com"),
    ("kv", "LinkedIn", "gnandakishorereddy"),
    ("kv", "dev.to", "n9601"),
    ("gap",),
    ("section", "GitHub Stats"),
    ("stats",),
]

THEMES = {
    "dark": dict(bg="#0b0b0b", border="#222", bar="#141414", fg="#c9d1d9", key="#ff7a33",
                 val="#5c9bff", dot="#3a3a3a", head="#f5f5f5", ascii="#8fb4ff",
                 add="#3fb950", rem="#ff4d5e", muted="#6b6b6b"),
    "light": dict(bg="#f6f8fa", border="#d0d7de", bar="#eaeef2", fg="#24292f", key="#c2410c",
                  val="#0047b3", dot="#c0c6cc", head="#111", ascii="#3b4a66",
                  add="#1a7f37", rem="#cf222e", muted="#8c959f"),
}


def gql(token, query, variables=None):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query, "variables": variables or {}}).encode(),
        headers={"Authorization": f"bearer {token}", "User-Agent": USER},
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        out = json.load(r)
    if "errors" in out:
        raise RuntimeError(out["errors"])
    return out["data"]


def fetch_stats(token):
    d = gql(token, """
    query($login: String!) {
      user(login: $login) {
        id createdAt
        followers { totalCount }
        repositories(ownerAffiliations: OWNER, first: 100) { totalCount nodes { stargazerCount } }
        repositoriesContributedTo(contributionTypes: [COMMIT, PULL_REQUEST, REPOSITORY]) { totalCount }
      }
    }""", {"login": USER})["user"]
    uid = d["id"]

    # Every repo the user can push to, then the user's own commits on each default branch.
    repos, cursor = [], None
    while True:
        page = gql(token, """
        query($login: String!, $after: String) {
          user(login: $login) {
            repositories(first: 50, after: $after,
                         ownerAffiliations: [OWNER, COLLABORATOR, ORGANIZATION_MEMBER]) {
              pageInfo { hasNextPage endCursor }
              nodes { name owner { login } isFork }
            }
          }
        }""", {"login": USER, "after": cursor})["user"]["repositories"]
        repos += [n for n in page["nodes"] if not n["isFork"]]
        if not page["pageInfo"]["hasNextPage"]:
            break
        cursor = page["pageInfo"]["endCursor"]

    commits = adds = dels = 0
    for repo in repos:
        cursor = None
        while True:
            ref = gql(token, """
            query($owner: String!, $name: String!, $uid: ID!, $after: String) {
              repository(owner: $owner, name: $name) {
                defaultBranchRef { target { ... on Commit {
                  history(first: 100, after: $after, author: { id: $uid }) {
                    totalCount pageInfo { hasNextPage endCursor }
                    nodes { additions deletions }
                  }
                } } }
              }
            }""", {"owner": repo["owner"]["login"], "name": repo["name"], "uid": uid, "after": cursor})
            branch = ref["repository"]["defaultBranchRef"]
            if not branch:
                break
            hist = branch["target"]["history"]
            if cursor is None:
                commits += hist["totalCount"]
            for n in hist["nodes"]:
                adds += n["additions"]
                dels += n["deletions"]
            if not hist["pageInfo"]["hasNextPage"]:
                break
            cursor = hist["pageInfo"]["endCursor"]

    return {
        "created": d["createdAt"],
        "repos": d["repositories"]["totalCount"],
        "contributed": d["repositoriesContributedTo"]["totalCount"],
        "stars": sum(n["stargazerCount"] for n in d["repositories"]["nodes"]),
        "followers": d["followers"]["totalCount"],
        "commits": commits,
        "additions": adds,
        "deletions": dels,
    }


def uptime(start, today):
    y = today.year - start.year
    m = today.month - start.month
    dd = today.day - start.day
    if dd < 0:
        m -= 1
        prev = (today.replace(day=1) - date.resolution)
        dd += prev.day
    if m < 0:
        y -= 1
        m += 12
    plural = lambda n, w: f"{n} {w}{'' if n == 1 else 's'}"
    return f"{plural(y, 'year')}, {plural(m, 'month')}, {plural(dd, 'day')}"


def kv_line(key, value, t, width=WIDTH):
    """'. Key: ....... value' padded to width, as SVG tspans."""
    dots = width - len(key) - len(value) - 5
    return (f'<tspan fill="{t["dot"]}">. </tspan><tspan fill="{t["key"]}">{escape(key)}</tspan>'
            f'<tspan fill="{t["fg"]}">:</tspan><tspan fill="{t["dot"]}"> {"." * max(dots, 1)} </tspan>'
            f'<tspan fill="{t["val"]}">{escape(value)}</tspan>')


def render(theme, stats, ascii_lines, up):
    t = THEMES[theme]
    fs, lh, cw = 14, 19, 8.43  # font size, line height, approx monospace advance
    pad_x, top = 28, 62
    ascii_w = max(len(l) for l in ascii_lines)
    info_x = pad_x + (ascii_w + 3) * cw

    rows = []
    for item in INFO:
        kind = item[0]
        if kind == "title":
            rule = "-" * (WIDTH - len(item[1]) - 1)
            rows.append(f'<tspan fill="{t["head"]}" font-weight="700">{item[1]}</tspan>'
                        f'<tspan fill="{t["dot"]}"> {rule}</tspan>')
        elif kind == "section":
            rule = "-" * (WIDTH - len(item[1]) - 3)
            rows.append(f'<tspan fill="{t["dot"]}">- </tspan><tspan fill="{t["head"]}" font-weight="700">'
                        f'{item[1]}</tspan><tspan fill="{t["dot"]}"> {rule}</tspan>')
        elif kind == "gap":
            rows.append("")
        elif kind == "kv":
            rows.append(kv_line(item[1], item[2].format(uptime=up), t))
        elif kind == "stats":
            sep = f'<tspan fill="{t["dot"]}"> | </tspan>'
            lw, rw = 33, WIDTH - 33 - 3
            rows.append(kv_line("Repos", f'{stats["repos"]} {{Contributed: {stats["contributed"]}}}', t, lw)
                        + sep + kv_line("Stars", f'{stats["stars"]:,}', t, rw))
            rows.append(kv_line("Commits", f'{stats["commits"]:,}', t, lw)
                        + sep + kv_line("Followers", f'{stats["followers"]:,}', t, rw))
            total = stats["additions"] - stats["deletions"]
            a, r = f'{stats["additions"]:,}++', f'{stats["deletions"]:,}--'
            loc_val = f'{total:,} ( {a}, {r} )'
            dots = WIDTH - len("Lines of Code") - len(loc_val) - 5
            rows.append(
                f'<tspan fill="{t["dot"]}">. </tspan><tspan fill="{t["key"]}">Lines of Code</tspan>'
                f'<tspan fill="{t["fg"]}">:</tspan><tspan fill="{t["dot"]}"> {"." * max(dots, 1)} </tspan>'
                f'<tspan fill="{t["val"]}">{total:,}</tspan><tspan fill="{t["fg"]}"> ( </tspan>'
                f'<tspan fill="{t["add"]}">{a}</tspan><tspan fill="{t["fg"]}">, </tspan>'
                f'<tspan fill="{t["rem"]}">{r}</tspan><tspan fill="{t["fg"]}"> )</tspan>'
                f'<tspan class="caret" fill="{t["val"]}"> _</tspan>')

    n = max(len(rows), len(ascii_lines))
    height = top + n * lh + 30
    width = int(info_x + (WIDTH + 1) * cw + pad_x)
    a_off = top + max(0, (len(rows) - len(ascii_lines)) // 2) * lh

    ascii_svg = "\n".join(
        f'<text x="{pad_x}" y="{a_off + i * lh}" class="a" xml:space="preserve">{escape(l).replace(" ", " ")}</text>'
        for i, l in enumerate(ascii_lines))
    info_svg = "\n".join(
        f'<text x="{info_x:.1f}" y="{top + i * lh}">{r}</text>' for i, r in enumerate(rows) if r)
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" font-family="ConsolasFallback, Consolas, 'SFMono-Regular', Menlo, 'Courier New', monospace" font-size="{fs}px">
<style>
  text {{ white-space: pre; fill: {t["fg"]}; }}
  .a {{ fill: {t["ascii"]}; }}
  .caret {{ animation: blink 1s steps(1) infinite; }}
  @keyframes blink {{ 50% {{ opacity: 0; }} }}
</style>
<rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="12" fill="{t["bg"]}" stroke="{t["border"]}"/>
<path d="M12.5 0.5 H{width - 12.5} a12 12 0 0 1 12 12 V34 H0.5 V12.5 a12 12 0 0 1 12 -12 Z" fill="{t["bar"]}"/>
<line x1="0" y1="34" x2="{width}" y2="34" stroke="{t["border"]}"/>
<circle cx="22" cy="17.5" r="6" fill="#ff5f57"/><circle cx="42" cy="17.5" r="6" fill="#febc2e"/><circle cx="62" cy="17.5" r="6" fill="#28c840"/>
<text x="{width / 2}" y="22" text-anchor="middle" font-size="12px" fill="{t["muted"]}" style="fill:{t["muted"]}">nanda@kishore: ~ $ neofetch</text>
<text x="{width - 16}" y="22" text-anchor="end" font-size="11px" style="fill:{t["muted"]}">{stamp}</text>
{ascii_svg}
{info_svg}
</svg>
'''


def main():
    cache = ASSETS / "stats.json"
    token = os.environ.get("ACCESS_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if token:
        stats = fetch_stats(token)
        cache.write_text(json.dumps(stats, indent=2) + "\n", encoding="utf-8")
    else:
        stats = json.loads(cache.read_text(encoding="utf-8"))

    today = date.today()
    start = BIRTHDAY or datetime.fromisoformat(stats["created"].replace("Z", "+00:00")).date()
    up = uptime(start, today) + ("" if BIRTHDAY else " (GitHub)")

    ascii_lines = (ASSETS / "ascii.txt").read_text(encoding="utf-8").rstrip("\n").split("\n")
    for theme in THEMES:
        (ASSETS / f"neofetch-{theme}.svg").write_text(render(theme, stats, ascii_lines, up), encoding="utf-8")
    print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    main()
