"""Builds assets/stats-card.svg and assets/langs-card.svg from the GitHub GraphQL API.

Run locally:  GITHUB_TOKEN=$(gh auth token) python scripts/cards.py
With a PAT for the profile owner (ACCESS_TOKEN in CI) private repos are included.
Without a token, or if the fetch fails, the existing SVGs are left untouched.
"""
import json
import os
import sys
from html import escape

from neofetch import ASSETS, USER, gql
from streak import BG, BLUE, BORDER, FG, MUTED, ORANGE

LANG_COLORS = {"TypeScript": "#3178c6", "JavaScript": "#f1e05a", "Python": "#3572a5", "Go": "#00add8",
               "C": "#8a8a8a", "C++": "#f34b7d", "CSS": "#7952b3", "HTML": "#e34c26", "Java": "#b07219",
               "Assembly": "#6e4c13", "Shell": "#89e051", "C#": "#178600", "Makefile": "#427819"}
EXTRA = ["#ff5500", "#0066ff", "#5c9bff", "#3fb950"]


def fetch(token):
    d = gql(token, """
    query($l: String!) { user(login: $l) {
      pullRequests { totalCount }
      issues { totalCount }
      repositoriesContributedTo(contributionTypes: [COMMIT, PULL_REQUEST, REPOSITORY]) { totalCount }
      repositories(ownerAffiliations: OWNER, isFork: false, first: 100) { nodes {
        stargazerCount
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) { edges { size node { name } } }
      } }
    } }""", {"l": USER})["user"]
    langs = {}
    for repo in d["repositories"]["nodes"]:
        for e in repo["languages"]["edges"]:
            langs[e["node"]["name"]] = langs.get(e["node"]["name"], 0) + e["size"]
    return {"prs": d["pullRequests"]["totalCount"], "issues": d["issues"]["totalCount"],
            "contributed": d["repositoriesContributedTo"]["totalCount"],
            "stars": sum(r["stargazerCount"] for r in d["repositories"]["nodes"]), "langs": langs}


def svg(w, h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'font-family="\'Segoe UI\', Ubuntu, sans-serif">\n'
            f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="4.5" fill="{BG}" stroke="{BORDER}"/>\n'
            f'{body}\n</svg>\n')


def stats_card(s, commits):
    rows = [("Total Stars Earned", s["stars"]), ("Total Commits", commits), ("Total PRs", s["prs"]),
            ("Total Issues", s["issues"]), ("Contributed to", s["contributed"])]
    body = [f'<text x="25" y="35" font-size="18" font-weight="600" fill="{BLUE}">GitHub Stats</text>']
    for i, (k, v) in enumerate(rows):
        y = 65 + i * 25
        body.append(f'<circle cx="31" cy="{y - 5}" r="4" fill="{ORANGE}"/>'
                    f'<text x="46" y="{y}" font-size="14" font-weight="600" fill="{FG}">{k}:</text>'
                    f'<text x="215" y="{y}" font-size="14" font-weight="600" fill="{FG}">{v:,}</text>')
    return svg(300, 195, "\n".join(body))


def langs_card(langs):
    total = sum(langs.values()) or 1
    top = sorted(langs.items(), key=lambda kv: -kv[1])[:8]
    body = [f'<text x="25" y="35" font-size="18" font-weight="600" fill="{BLUE}">Most Used Languages</text>']
    x, bar = 25, []
    for i, (name, size) in enumerate(top):
        color = LANG_COLORS.get(name, EXTRA[i % len(EXTRA)])
        w = 250 * size / total
        bar.append(f'<rect x="{x:.1f}" y="52" width="{max(w, 1):.1f}" height="8" fill="{color}"/>')
        x += w
    body.append(f'<clipPath id="c"><rect x="25" y="52" width="250" height="8" rx="4"/></clipPath>'
                f'<g clip-path="url(#c)">{"".join(bar)}</g>')
    for i, (name, size) in enumerate(top):
        color = LANG_COLORS.get(name, EXTRA[i % len(EXTRA)])
        cx, y = 31 + (i % 2) * 130, 85 + (i // 2) * 24
        body.append(f'<circle cx="{cx}" cy="{y - 4}" r="5" fill="{color}"/>'
                    f'<text x="{cx + 12}" y="{y}" font-size="12" fill="{FG}">{escape(name)} '
                    f'<tspan fill="{MUTED}">{100 * size / total:.1f}%</tspan></text>')
    return svg(300, 195, "\n".join(body))


def main():
    token = os.environ.get("ACCESS_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not token:
        print("no token; leaving cards as is", file=sys.stderr)
        return
    try:
        s = fetch(token)
    except Exception as e:
        print(f"warning: cards fetch failed ({e}); keeping existing cards", file=sys.stderr)
        return
    commits = json.loads((ASSETS / "stats.json").read_text(encoding="utf-8"))["commits"]
    (ASSETS / "stats-card.svg").write_text(stats_card(s, commits), encoding="utf-8")
    (ASSETS / "langs-card.svg").write_text(langs_card(s["langs"]), encoding="utf-8")
    print({k: v for k, v in s.items() if k != "langs"}, len(s["langs"]))


if __name__ == "__main__":
    main()
