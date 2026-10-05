<div align="center">

<img src="assets/header.svg" alt="Nandakishore Reddy: full-stack engineer, LSM engines, x86 kernels" width="100%"/>

<a href="https://git.io/typing-svg">
  <img src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=500&size=18&duration=2800&pause=900&color=0066FF&center=true&vCenter=true&width=720&lines=Shipping+production+platforms+at+Verge+Scales;Wrote+an+LSM-tree+database+from+scratch+in+Go;Booting+my+own+x86+kernel+in+QEMU;Wiring+LLMs+into+real+business+workflows" alt="typing intro"/>
</a>

<br/><br/>

<a href="https://personal-portfolio-five-liard-62.vercel.app"><img src="https://img.shields.io/badge/PORTFOLIO-080808?style=for-the-badge&logo=vercel&logoColor=0066FF" alt="Portfolio"/></a>
<a href="https://linkedin.com/in/gnandakishorereddy"><img src="https://img.shields.io/badge/LINKEDIN-080808?style=for-the-badge&logo=data:image/svg%2Bxml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI%2BPHBhdGggZmlsbD0iIzAwNjZGRiIgZD0iTTIwLjQ1IDIwLjQ1aC0zLjU2di01LjU3YzAtMS4zMy0uMDMtMy4wNC0xLjg1LTMuMDQtMS44NiAwLTIuMTQgMS40NS0yLjE0IDIuOTR2NS42N0g5LjM1VjloMy40MXYxLjU2aC4wNWMuNDgtLjkgMS42NC0xLjg1IDMuMzctMS44NSAzLjYgMCA0LjI3IDIuMzcgNC4yNyA1LjQ2djYuMjh6TTUuMzQgNy40M2EyLjA2IDIuMDYgMCAxIDEgMC00LjEzIDIuMDYgMi4wNiAwIDAgMSAwIDQuMTN6TTcuMTIgMjAuNDVIMy41NlY5aDMuNTZ2MTEuNDV6TTIyLjIyIDBIMS43N0MuNzkgMCAwIC43NyAwIDEuNzN2MjAuNTRDMCAyMy4yMy43OSAyNCAxLjc3IDI0aDIwLjQ1Yy45OCAwIDEuNzgtLjc3IDEuNzgtMS43M1YxLjczQzI0IC43NyAyMy4yIDAgMjIuMjIgMHoiLz48L3N2Zz4%3D" alt="LinkedIn"/></a>
<a href="https://dev.to/n9601"><img src="https://img.shields.io/badge/DEV.TO-080808?style=for-the-badge&logo=devdotto&logoColor=FF5500" alt="dev.to"/></a>
<a href="mailto:nandakishorereddyg@outlook.com"><img src="https://img.shields.io/badge/EMAIL-080808?style=for-the-badge&logo=maildotru&logoColor=FF1133" alt="Email"/></a>
<a href="https://personal-portfolio-five-liard-62.vercel.app/Nandakishore_Reddy_CV.pdf"><img src="https://img.shields.io/badge/RESUME-080808?style=for-the-badge&logo=readdotcv&logoColor=F5F5F5" alt="Resume"/></a>

</div>

<img src="assets/divider.svg" width="100%" alt=""/>

### `$ neofetch`

<p align="center">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/neofetch-dark.svg"/>
  <source media="(prefers-color-scheme: light)" srcset="assets/neofetch-light.svg"/>
  <img src="assets/neofetch-dark.svg" width="100%" alt="neofetch-style profile card: Nandakishore Reddy, full-stack and AI automation engineer at Verge Scales, with live GitHub stats"/>
</picture>
</p>

<sub><p align="center">stats refresh daily via GitHub Actions</p></sub>

<img src="assets/divider.svg" width="100%" alt=""/>

### `$ whoami`

```go
package main

type Engineer struct {
    Name      string
    Role      string
    Base      string
    Education []string
    Builds    []string
    Ships     []string
    OffClock  []string
}

var me = Engineer{
    Name: "Gadusatla Nandakishore Reddy",
    Role: "Software Engineer, Full-Stack & AI Automation @ Verge Scales",
    Base: "Hyderabad, IN (IST)",
    Education: []string{
        "B.Tech CSE @ VNR VJIET (2026 - present)",
        "Diploma CSE @ TRR, CGPA 9.18 / 10, top 1% of cohort",
    },
    Builds:   []string{"LSM-tree storage engines", "x86 kernels", "LLM pipelines"},
    Ships:    []string{"payroll", "order operations", "marketing intelligence"},
    OffClock: []string{"perf tuning", "custom Android ROMs", "music", "films", "photography"},
}
```

<img src="assets/divider.svg" width="100%" alt=""/>

### `$ cat ./now.log`

> Joined **Verge Scales** in Jan 2026 and stayed on the team as annual revenue grew from **5-figure to 8-figure**, splitting time between engineering, operations and customer support.

<table>
<tr>
<td width="50%" valign="top">

#### `OrderFlow` &nbsp;·&nbsp; order-operations platform
<sub>Jun 2026 - present &nbsp;·&nbsp; TypeScript, React, Express, Drizzle, Postgres, Vercel</sub>

- **Payroll module, end to end.** Attendance syncs nightly to RazorpayX in concurrent batches to fit Vercel's 30s limit; variable pay auto-computed from delivery, return and reshipment metrics; PDF payslips.
- **Reshipments workflow.** Schema, Shopify order creation, webhooks, audit trail and a six-status lifecycle, with fallbacks when Shopify is missing the parent order.
- **Nightly reconciliation** against Delhivery that detects and repairs stalled shipments across stores.

</td>
<td width="50%" valign="top">

#### `Creative Strategy HQ` &nbsp;·&nbsp; marketing platform
<sub>May - Jun 2026 &nbsp;·&nbsp; TypeScript, React, Supabase, n8n, OpenRouter</sub>

- **Viral-content discovery.** Swipe-to-approve queue refilled by n8n webhooks; rejects are blacklisted forever.
- **LLM scoring.** Gemini Flash via OpenRouter scores ads and generates keywords that feed every future scan.
- **Auth and RLS.** Email OTP, Google OAuth, role-based access, Postgres row-level security, expiring team invites.
- **n8n agents.** Claude-powered research briefs with web search, written to Google Docs atomically.

</td>
</tr>
</table>

<img src="assets/divider.svg" width="100%" alt=""/>

### `$ ls ./builds`

<table>
<tr>
<td><a href="https://github.com/N9601/SolderDB"><img src="assets/card-solderdb.svg" width="100%" alt="SolderDB"/></a></td>
<td><a href="https://github.com/N9601/PyroOS"><img src="assets/card-pyroos.svg" width="100%" alt="PyroOS"/></a></td>
</tr>
<tr>
<td><a href="https://github.com/N9601/FlowCAD"><img src="assets/card-flowcad.svg" width="100%" alt="FlowCAD"/></a></td>
<td><a href="https://github.com/N9601/algowizard"><img src="assets/card-algowizard.svg" width="100%" alt="AlgoWizard"/></a></td>
</tr>
<tr>
<td><a href="https://n9601.github.io/IQOO2k26/"><img src="assets/card-truthbox.svg" width="100%" alt="Truthbox"/></a></td>
<td><a href="https://github.com/N9601/Tarang"><img src="assets/card-tarang.svg" width="100%" alt="Tarang"/></a></td>
</tr>
</table>

<details>
<summary><b>Inside SolderDB</b> &nbsp;<sub>(click to expand)</sub></summary>
<br/>

```text
  write ──► WAL (CRC32C, torn-write recovery)
              │
              ▼
          memtable ──flush──► L0 SSTables ──leveled compaction──► L1 ... Ln
              ▲                    │
              │              bloom filters guard every disk read
  read  ──────┘
```

- PocketBase / Supabase-style backend on top: collections with access rules, bcrypt + HMAC-SHA256 auth, blob storage, realtime over SSE, REST API, JS and Go SDKs.
- Ships as a single Wails desktop executable with a React control center and a live memtable-flush visualizer.
- Compaction backs off under battery or thermal pressure.

</details>

<details>
<summary><b>More repos</b></summary>
<br/>

| Repo | What it is | Stack |
|---|---|---|
| [**Cinder**](https://github.com/N9601/Cinder) | Chrome extension that turns YouTube videos into Obsidian notes via Gemini, with `[[wikilinks]]` into your existing vault | JavaScript, Gemini, Chrome MV3 |
| [**Akashavani**](https://github.com/N9601/Skyscanner-Rebuild) &nbsp;<sub>[live](https://akashavani-mauve.vercel.app)</sub> | Travel meta-search rebuild for the RE:BUILD hackathon: flights, stays, cars, price alerts, AI assistant | React, TypeScript, TanStack Query, Zustand |
| [**Truthbox**](https://github.com/N9601/IQOO2k26) &nbsp;<sub>[live](https://n9601.github.io/IQOO2k26/)</sub> | Source for the card above, iQOO Hackathon 2026 | JavaScript, WebCrypto |
| [**Personal Portfolio**](https://github.com/N9601/personal-portfolio-final) &nbsp;<sub>[live](https://personal-portfolio-five-liard-62.vercel.app)</sub> | Exploded-motherboard hero in Three.js with hand-written GLSL PCB-trace shaders and cursor-magnetic physics | Next.js, Three.js, GLSL, GSAP |

</details>

<img src="assets/divider.svg" width="100%" alt=""/>

### `$ stack --all`

<p align="center">
  <img src="https://skillicons.dev/icons?i=go,ts,js,java,py,c,cpp,cs,bash,postgres,supabase,react,nextjs,nodejs,express,dotnet,threejs,tailwind,vercel,cloudflare,aws,docker,nginx,linux,git,githubactions,vscode&theme=dark&perline=9" alt="tech stack"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/x86_Assembly-080808?style=flat-square&logo=intel&logoColor=0066FF" alt="x86 Assembly"/>
  <img src="https://img.shields.io/badge/QEMU-080808?style=flat-square&logo=qemu&logoColor=FF5500" alt="QEMU"/>
  <img src="https://img.shields.io/badge/Wails-080808?style=flat-square&logo=wails&logoColor=FF1133" alt="Wails"/>
  <img src="https://img.shields.io/badge/Drizzle_ORM-080808?style=flat-square&logo=drizzle&logoColor=C5F74F" alt="Drizzle"/>
  <img src="https://img.shields.io/badge/n8n-080808?style=flat-square&logo=n8n&logoColor=EA4B71" alt="n8n"/>
  <img src="https://img.shields.io/badge/OpenRouter-080808?style=flat-square&logo=openai&logoColor=F5F5F5" alt="OpenRouter"/>
  <img src="https://img.shields.io/badge/Claude-080808?style=flat-square&logo=anthropic&logoColor=D97757" alt="Claude"/>
  <img src="https://img.shields.io/badge/Gemini-080808?style=flat-square&logo=googlegemini&logoColor=8E75B2" alt="Gemini"/>
  <img src="https://img.shields.io/badge/GLSL-080808?style=flat-square&logo=opengl&logoColor=0066FF" alt="GLSL"/>
  <img src="https://img.shields.io/badge/Shopify_API-080808?style=flat-square&logo=shopify&logoColor=7AB55C" alt="Shopify"/>
  <img src="https://img.shields.io/badge/RazorpayX-080808?style=flat-square&logo=razorpay&logoColor=3395FF" alt="RazorpayX"/>
</p>

<img src="assets/divider.svg" width="100%" alt=""/>

### `$ git log --stat`

<p align="center">
  <img src="https://github-readme-stats.vercel.app/api?username=N9601&show_icons=true&hide_border=true&bg_color=080808&title_color=0066FF&icon_color=FF5500&text_color=F5F5F5&ring_color=0066FF&include_all_commits=true&count_private=true" height="165" alt="GitHub stats"/>
  <img src="https://github-readme-stats.vercel.app/api/top-langs/?username=N9601&layout=compact&hide_border=true&bg_color=080808&title_color=0066FF&text_color=F5F5F5&langs_count=8" height="165" alt="Top languages"/>
</p>

<p align="center">
  <img src="https://streak-stats.demolab.com?user=N9601&hide_border=true&background=080808&ring=0066FF&fire=FF5500&currStreakLabel=0066FF&sideLabels=F5F5F5&currStreakNum=F5F5F5&sideNums=F5F5F5&dates=6B6B6B&stroke=1A1A1A" alt="Streak"/>
</p>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/N9601/N9601/output/snake-dark.svg"/>
  <img src="https://raw.githubusercontent.com/N9601/N9601/output/snake.svg" width="100%" alt="contribution snake"/>
</picture>

<img src="assets/divider.svg" width="100%" alt=""/>

<div align="center">

**Class Representative, all three years of diploma** &nbsp;·&nbsp; English, Telugu, Hindi

<sub>Open to interesting systems problems and teams that ship. Say hi at <a href="mailto:nandakishorereddyg@outlook.com">nandakishorereddyg@outlook.com</a>.</sub>

<br/><br/>

<img src="https://komarev.com/ghpvc/?username=N9601&color=0066ff&style=flat-square&label=PROFILE+VIEWS" alt="profile views"/>

</div>
