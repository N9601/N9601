"""Generates the SVG art in ../assets. Run: python scripts/gen.py"""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets"
OUT.mkdir(exist_ok=True)

BG, FG, MUTED, GRID = "#080808", "#f5f5f5", "#6b6b6b", "#1a1a1a"
BLUE, ORANGE, RED = "#0066ff", "#ff5500", "#ff1133"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
SANS = "'Space Grotesk', 'Segoe UI', Helvetica, Arial, sans-serif"


def header():
    # PCB traces that run into the chip from the left; each draws itself in a loop.
    traces = [
        ("M760 70 H820 V120 H870", BLUE, 0.0),
        ("M740 180 H870", ORANGE, 0.6),
        ("M760 290 H820 V240 H870", RED, 1.2),
        ("M1150 90 H1090 V130 H1030", BLUE, 1.8),
        ("M1170 180 H1030", ORANGE, 0.3),
        ("M1150 270 H1090 V230 H1030", RED, 0.9),
        ("M950 20 V100", BLUE, 1.5),
        ("M950 340 V260", ORANGE, 2.1),
    ]
    trace_svg = "\n".join(
        f'<path d="{d}" class="t" stroke="{c}" style="animation-delay:{delay}s"/>'
        f'<path d="{d}" class="tb" stroke="{c}"/>'
        for d, c, delay in traces
    )
    pins = []
    for i in range(6):
        y = 116 + i * 26
        pins.append(f'<rect x="860" y="{y}" width="10" height="4" fill="{MUTED}"/>')
        pins.append(f'<rect x="1030" y="{y}" width="10" height="4" fill="{MUTED}"/>')
    for i in range(6):
        x = 886 + i * 26
        pins.append(f'<rect x="{x}" y="90" width="4" height="10" fill="{MUTED}"/>')
        pins.append(f'<rect x="{x}" y="260" width="4" height="10" fill="{MUTED}"/>')

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 360" width="1200" height="360">
<style>
  .t {{ fill:none; stroke-width:2; stroke-dasharray:140 600; stroke-dashoffset:740; animation: run 3.2s linear infinite; }}
  .tb {{ fill:none; stroke-width:1; opacity:.18; }}
  @keyframes run {{ to {{ stroke-dashoffset:0; }} }}
  .pulse {{ animation: pulse 1.6s ease-in-out infinite; transform-origin:center; transform-box:fill-box; }}
  @keyframes pulse {{ 0%,100% {{ opacity:1; }} 50% {{ opacity:.25; }} }}
  .core {{ animation: core 2.4s ease-in-out infinite; }}
  @keyframes core {{ 0%,100% {{ fill-opacity:.10; }} 50% {{ fill-opacity:.32; }} }}
  .caret {{ animation: blink 1s steps(1) infinite; }}
  @keyframes blink {{ 50% {{ opacity:0; }} }}
  .rise {{ animation: rise 1s cubic-bezier(.2,.7,.2,1) both; }}
  @keyframes rise {{ from {{ opacity:0; transform:translateY(18px); }} to {{ opacity:1; transform:none; }} }}
  .scan {{ animation: scan 6s linear infinite; }}
  @keyframes scan {{ from {{ transform:translateY(-40px); }} to {{ transform:translateY(400px); }} }}
</style>
<defs>
  <pattern id="g" width="40" height="40" patternUnits="userSpaceOnUse">
    <path d="M40 0H0V40" fill="none" stroke="{GRID}" stroke-width="1"/>
  </pattern>
  <radialGradient id="glow" cx="0.8" cy="0.5" r="0.55">
    <stop offset="0" stop-color="{BLUE}" stop-opacity="0.30"/>
    <stop offset="0.5" stop-color="{ORANGE}" stop-opacity="0.10"/>
    <stop offset="1" stop-color="{BG}" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="scanline" x1="0" x2="0" y1="0" y2="1">
    <stop offset="0" stop-color="{BLUE}" stop-opacity="0"/>
    <stop offset="1" stop-color="{BLUE}" stop-opacity="0.10"/>
  </linearGradient>
  <clipPath id="frame"><rect width="1200" height="360" rx="14"/></clipPath>
</defs>
<g clip-path="url(#frame)">
<rect width="1200" height="360" fill="{BG}"/>
<rect width="1200" height="360" fill="url(#g)"/>
<rect width="1200" height="360" fill="url(#glow)"/>
<rect class="scan" width="1200" height="40" fill="url(#scanline)"/>

<g transform="translate(48,44)">
  <rect width="14" height="14" fill="{BLUE}"/>
  <text x="26" y="12" font-family="{MONO}" font-size="13" letter-spacing="4" fill="{FG}">N9601 / FULL-STACK + SYSTEMS</text>
  <text x="26" y="32" font-family="{MONO}" font-size="11" letter-spacing="3" fill="{MUTED}">// HYDERABAD, IN  ·  IST UTC+5:30</text>
</g>

<g transform="translate(48,0)">
  <text class="rise" x="0" y="190" font-family="{SANS}" font-size="84" font-weight="300" letter-spacing="-4" fill="{FG}">NANDAKISHORE<tspan fill="{BLUE}">.</tspan></text>
  <text class="rise" style="animation-delay:.2s" x="4" y="232" font-family="{MONO}" font-size="17" letter-spacing="3" fill="{BLUE}">FULL-STACK ENGINEER  <tspan fill="{MUTED}">/</tspan>  <tspan fill="{ORANGE}">LSM ENGINES</tspan>  <tspan fill="{MUTED}">/</tspan>  <tspan fill="{RED}">x86 KERNELS</tspan></text>
  <text class="rise" style="animation-delay:.4s" x="4" y="300" font-family="{MONO}" font-size="14" fill="{MUTED}">&gt; <tspan fill="{FG}">shipping orderflow at verge scales, building solderdb + pyroos</tspan><tspan class="caret" fill="{BLUE}"> _</tspan></text>
</g>

{trace_svg}

<g>
  {"".join(pins)}
  <rect x="870" y="100" width="160" height="160" rx="6" fill="#0d0d0d" stroke="#2a2a2a"/>
  <rect class="core" x="884" y="114" width="132" height="132" rx="3" fill="{BLUE}" stroke="{BLUE}" stroke-opacity=".5"/>
  <circle cx="882" cy="112" r="3" fill="{MUTED}"/>
  <text x="950" y="172" text-anchor="middle" font-family="{MONO}" font-size="22" font-weight="700" letter-spacing="2" fill="{FG}">NKR</text>
  <text x="950" y="194" text-anchor="middle" font-family="{MONO}" font-size="10" letter-spacing="3" fill="{MUTED}">GO · TS · C · ASM</text>
  <text x="950" y="214" text-anchor="middle" font-family="{MONO}" font-size="9" letter-spacing="2" fill="{BLUE}">REV 2026</text>
</g>

<g transform="translate(1000,44)">
  <circle class="pulse" cx="6" cy="6" r="6" fill="{RED}"/>
  <text x="20" y="11" font-family="{MONO}" font-size="12" letter-spacing="3" fill="{FG}">ONLINE</text>
</g>

<rect x="0.5" y="0.5" width="1199" height="359" rx="14" fill="none" stroke="#222"/>
</g>
</svg>
'''
    (OUT / "header.svg").write_text(svg, encoding="utf-8")


def card(slug, idx, title, kind, accent, blurb, tags, status):
    lines = "".join(
        f'<text x="28" y="{118 + i * 20}" font-family="{MONO}" font-size="12.5" fill="#b8b8b8">{line}</text>'
        for i, line in enumerate(blurb)
    )
    x = 28
    chips = []
    for t in tags:
        w = 14 + len(t) * 7.2
        chips.append(
            f'<rect x="{x}" y="196" width="{w:.0f}" height="22" rx="3" fill="none" stroke="{accent}" stroke-opacity=".55"/>'
            f'<text x="{x + w / 2:.0f}" y="211" text-anchor="middle" font-family="{MONO}" font-size="11" fill="{FG}">{t}</text>'
        )
        x += w + 8
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 240" width="440" height="240">
<style>
  .bar {{ animation: bar 2.8s ease-in-out infinite; transform-origin:left; transform-box:fill-box; }}
  @keyframes bar {{ 0% {{ transform:scaleX(.15); }} 50% {{ transform:scaleX(1); }} 100% {{ transform:scaleX(.15); }} }}
  .dot {{ animation: d 1.6s ease-in-out infinite; }}
  @keyframes d {{ 50% {{ opacity:.2; }} }}
</style>
<defs>
  <pattern id="g" width="22" height="22" patternUnits="userSpaceOnUse">
    <path d="M22 0H0V22" fill="none" stroke="#141414" stroke-width="1"/>
  </pattern>
  <radialGradient id="r" cx="1" cy="0" r="0.9">
    <stop offset="0" stop-color="{accent}" stop-opacity=".22"/>
    <stop offset="1" stop-color="{BG}" stop-opacity="0"/>
  </radialGradient>
</defs>
<rect width="440" height="240" rx="12" fill="{BG}"/>
<rect width="440" height="240" rx="12" fill="url(#g)"/>
<rect width="440" height="240" rx="12" fill="url(#r)"/>
<rect class="bar" x="0" y="0" width="440" height="3" fill="{accent}"/>
<text x="28" y="40" font-family="{MONO}" font-size="11" letter-spacing="3" fill="{MUTED}">{idx} / {kind}</text>
<circle class="dot" cx="404" cy="36" r="4" fill="{accent}"/>
<text x="392" y="40" text-anchor="end" font-family="{MONO}" font-size="10" letter-spacing="2" fill="{MUTED}">{status}</text>
<text x="26" y="84" font-family="{SANS}" font-size="32" font-weight="600" letter-spacing="-1" fill="{FG}">{title}<tspan fill="{accent}">.</tspan></text>
{lines}
{"".join(chips)}
<rect x="0.5" y="0.5" width="439" height="239" rx="12" fill="none" stroke="#232323"/>
</svg>
'''
    (OUT / f"card-{slug}.svg").write_text(svg, encoding="utf-8")


def divider():
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 24" width="1200" height="24">
<style>
  .p {{ animation: p 4s linear infinite; }}
  @keyframes p {{ from {{ transform:translateX(-200px); }} to {{ transform:translateX(1200px); }} }}
</style>
<defs>
  <linearGradient id="l" x1="0" x2="1">
    <stop offset="0" stop-color="{BLUE}" stop-opacity="0"/>
    <stop offset=".5" stop-color="{BLUE}"/>
    <stop offset="1" stop-color="{ORANGE}" stop-opacity="0"/>
  </linearGradient>
</defs>
<line x1="0" y1="12" x2="1200" y2="12" stroke="#2a2a2a" stroke-width="1"/>
<rect class="p" x="0" y="11" width="200" height="2" fill="url(#l)"/>
<rect x="596" y="8" width="8" height="8" fill="{BG}" stroke="{BLUE}"/>
</svg>
'''
    (OUT / "divider.svg").write_text(svg, encoding="utf-8")


header()
divider()
card("solderdb", "01", "SolderDB", "SYSTEMS · DATABASE", BLUE,
     ["From-scratch LSM-tree engine in Go: WAL with", "CRC32C recovery, SSTables, leveled compaction,",
      "bloom filters. PocketBase-style backend on top."],
     ["Go", "Wails", "React", "SSE"], "SHIPPED")
card("pyroos", "02", "PyroOS", "SYSTEMS · KERNEL", RED,
     ["x86 hobby OS. Assembly bootloader flips real", "mode to protected mode, sets up GDT and IDT,",
      "then hands off to a C kernel with VGA output."],
     ["x86 ASM", "C", "QEMU"], "BOOTING")
card("algowizard", "03", "AlgoWizard", "FULL-STACK · EDTECH", ORANGE,
     ["Real-time visualizations of data structures and", "algorithms, with Supabase auth and per-user",
      "progress. Smooth even at high step counts."],
     ["Next.js", "TypeScript", "Supabase"], "LIVE")
card("coefficient", "04", "Coefficient", "FRONTEND · SIMULATOR", BLUE,
     ["Browser-based logic-gate and architecture", "simulator built from reusable logic components,",
      "server-rendered for a fast first load."],
     ["Next.js", "React", "SSR"], "LIVE")
print("wrote", sorted(p.name for p in OUT.iterdir()))
