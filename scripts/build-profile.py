from __future__ import annotations

import base64
import html
import json
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent
PROFILE_DIR = REPO_ROOT / "profile"
OUT = REPO_ROOT / "assets"
OUT.mkdir(exist_ok=True)

PROFILE = json.loads((PROFILE_DIR / "profile.json").read_text())

HANDLE = html.escape(PROFILE["handle"].upper())
NAME_TEXT = html.escape(PROFILE["name"])
ROLE_TEXT = html.escape(PROFILE["role"])
LOCATION_TEXT = html.escape(PROFILE["location"])
NAME = html.escape(PROFILE["name"].upper())
ROLE = html.escape(PROFILE["role"].upper())
LOCATION = html.escape(PROFILE["location"].upper())
VERSION = html.escape(PROFILE["version"])
HEADLINE = [html.escape(line) for line in PROFILE["headline"]]
MOBILE_HEADLINE = [html.escape(line) for line in PROFILE["mobileHeadline"]]
TAGLINE = html.escape(PROFILE["tagline"])
DOMAINS = " / ".join(html.escape(domain) for domain in PROFILE["domains"])
FOCUS = [
    {
        "label": html.escape(item["label"]),
        "title": html.escape(item["title"]),
        "description": html.escape(item["description"]),
    }
    for item in PROFILE["focus"]
]
LOOP = [html.escape(step) for step in PROFILE["loop"]]

if len(HEADLINE) != 4:
    raise ValueError("profile.headline must contain exactly four lines")
if len(MOBILE_HEADLINE) != 4:
    raise ValueError("profile.mobileHeadline must contain exactly four lines")
if len(FOCUS) != 3:
    raise ValueError("profile.focus must contain exactly three items")
if len(LOOP) != 4:
    raise ValueError("profile.loop must contain exactly four steps")


def data_url(path: Path, mime: str) -> str:
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode()}"


BIG_SHOULDERS = data_url(PROFILE_DIR / "fonts/big-shoulders-display.woff2", "font/woff2")
OUTFIT = data_url(PROFILE_DIR / "fonts/outfit.woff2", "font/woff2")
MONOGRAM = data_url(PROFILE_DIR / "monogram.png", "image/png")

THEMES = {
    "dark": {
        "background": "#080D09",
        "foreground": "#F1EADC",
        "muted": "#A19E96",
        "grid": "#F1EADC",
        "coral": "#FF5C35",
        "acid": "#D9FF43",
        "mark": "#F1EADC",
    },
    "light": {
        "background": "#F1EADC",
        "foreground": "#111612",
        "muted": "#666A64",
        "grid": "#111612",
        "coral": "#E64A28",
        "acid": "#9DBE16",
        "mark": "#111612",
    },
}


def common_defs(theme: dict[str, str], mobile: bool) -> str:
    motion = (
        "@keyframes signal{0%{transform:translateX(-180px);opacity:0}8%{opacity:1}92%{opacity:1}100%{transform:translateX(1180px);opacity:0}}"
        if not mobile
        else "@keyframes signal{0%{transform:translateX(-120px);opacity:0}8%{opacity:1}92%{opacity:1}100%{transform:translateX(650px);opacity:0}}"
    )
    resting = (
        "transform:translateX(360px)"
        if not mobile
        else "transform:translateX(220px)"
    )
    return f"""
  <defs>
    <style>
      @font-face {{ font-family: 'Big Shoulders'; src: url('{BIG_SHOULDERS}') format('woff2'); font-weight: 100 900; }}
      @font-face {{ font-family: 'Outfit'; src: url('{OUTFIT}') format('woff2'); font-weight: 100 900; }}
      .display {{ font-family: 'Big Shoulders', 'Arial Narrow', sans-serif; font-weight: 820; letter-spacing: -0.018em; }}
      .body {{ font-family: 'Outfit', Arial, sans-serif; }}
      .utility {{ font-family: 'Outfit', Arial, sans-serif; font-weight: 650; letter-spacing: 0.14em; }}
      .signal {{ {resting}; opacity: 1; }}
      @media (prefers-reduced-motion: no-preference) {{
        .signal {{ animation: signal 4.2s linear infinite; will-change: transform, opacity; }}
        {motion}
      }}
    </style>
    <mask id="tr-mark" maskUnits="objectBoundingBox" maskContentUnits="objectBoundingBox" style="mask-type:luminance">
      <image href="{MONOGRAM}" x="0" y="0" width="1" height="1" preserveAspectRatio="xMidYMid meet" />
    </mask>
    <linearGradient id="signal-gradient" x1="0" x2="1">
      <stop offset="0" stop-color="{theme['acid']}" stop-opacity="0" />
      <stop offset="0.35" stop-color="{theme['acid']}" stop-opacity="0.4" />
      <stop offset="0.7" stop-color="{theme['acid']}" />
      <stop offset="1" stop-color="{theme['acid']}" stop-opacity="0" />
    </linearGradient>
  </defs>"""


def desktop(theme: dict[str, str]) -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 1040" role="img" aria-labelledby="title desc" text-rendering="geometricPrecision" shape-rendering="geometricPrecision">
  <title id="title">{' '.join(HEADLINE).title()}</title>
  <desc id="desc">{NAME_TEXT} is a {ROLE_TEXT.lower()} in {LOCATION_TEXT} working on AI agent systems, reusable engineering workflows, and product platforms.</desc>
{common_defs(theme, False)}
  <rect width="1280" height="1040" fill="{theme['background']}" />
  <rect x="0.5" y="0.5" width="1279" height="1039" fill="none" stroke="{theme['grid']}" stroke-opacity="0.12" />

  <g stroke="{theme['grid']}" stroke-opacity="0.10" stroke-width="1">
    <path d="M64 0V1040M352 0V1040M640 0V1040M928 0V1040M1216 0V1040" />
    <path d="M0 92H1280M0 706H1280M0 914H1280" />
  </g>

  <g class="utility" font-size="15" fill="{theme['muted']}">
    <text x="64" y="57">{HANDLE} / PROFILE {VERSION}</text>
    <text x="1216" y="57" text-anchor="end">{ROLE} · {LOCATION}</text>
  </g>
  <rect x="64" y="78" width="1152" height="4" fill="{theme['coral']}" />
  <rect x="64" y="82" width="1152" height="3" fill="{theme['acid']}" />

  <g class="display" font-size="148" fill="{theme['foreground']}">
    <text x="64" y="232">{HEADLINE[0]}</text>
    <text x="64" y="356" fill="{theme['coral']}">{HEADLINE[1]}</text>
    <text x="64" y="480">{HEADLINE[2]}</text>
    <text x="64" y="604">{HEADLINE[3]}</text>
  </g>

  <rect x="958" y="160" width="238" height="238" fill="{theme['mark']}" opacity="0.92" mask="url(#tr-mark)" />
  <g class="utility" font-size="13" fill="{theme['muted']}">
    <text x="960" y="440">{NAME}</text>
    <text x="960" y="468">@{HANDLE}</text>
  </g>

  <g class="body" fill="{theme['foreground']}">
    <text x="64" y="662" font-size="28" font-weight="540">{TAGLINE}</text>
    <text x="1216" y="660" text-anchor="end" font-size="15" font-weight="620" letter-spacing="0.12em" fill="{theme['muted']}">{DOMAINS}</text>
  </g>

  <g class="body">
    <g transform="translate(64 750)">
      <text class="utility" y="0" font-size="14" fill="{theme['coral']}">01 / {FOCUS[0]['label']}</text>
      <text y="46" font-size="24" font-weight="620" fill="{theme['foreground']}">{FOCUS[0]['title']}</text>
      <text y="80" font-size="18" fill="{theme['muted']}">{FOCUS[0]['description']}</text>
    </g>
    <g transform="translate(448 750)">
      <text class="utility" y="0" font-size="14" fill="{theme['coral']}">02 / {FOCUS[1]['label']}</text>
      <text y="46" font-size="24" font-weight="620" fill="{theme['foreground']}">{FOCUS[1]['title']}</text>
      <text y="80" font-size="18" fill="{theme['muted']}">{FOCUS[1]['description']}</text>
    </g>
    <g transform="translate(832 750)">
      <text class="utility" y="0" font-size="14" fill="{theme['coral']}">03 / {FOCUS[2]['label']}</text>
      <text y="46" font-size="24" font-weight="620" fill="{theme['foreground']}">{FOCUS[2]['title']}</text>
      <text y="80" font-size="18" fill="{theme['muted']}">{FOCUS[2]['description']}</text>
    </g>
  </g>

  <g class="utility" font-size="15" fill="{theme['foreground']}">
    <text x="64" y="966">{LOOP[0]}</text>
    <text x="388" y="966">{LOOP[1]}</text>
    <text x="780" y="966">{LOOP[2]}</text>
    <text x="1134" y="966">{LOOP[3]}</text>
  </g>
  <path d="M64 995H1216" stroke="{theme['grid']}" stroke-opacity="0.24" stroke-width="2" />
  <g fill="{theme['background']}" stroke="{theme['foreground']}" stroke-width="2">
    <circle cx="64" cy="995" r="6" /><circle cx="448" cy="995" r="6" /><circle cx="832" cy="995" r="6" /><circle cx="1216" cy="995" r="6" />
  </g>
  <g clip-path="url(#signal-clip)">
    <clipPath id="signal-clip"><rect x="64" y="984" width="1152" height="22" /></clipPath>
    <rect class="signal" x="64" y="990" width="180" height="10" rx="5" fill="url(#signal-gradient)" />
  </g>
</svg>"""


def mobile(theme: dict[str, str]) -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 1380" role="img" aria-labelledby="title desc" text-rendering="geometricPrecision" shape-rendering="geometricPrecision">
  <title id="title">{' '.join(HEADLINE).title()}</title>
  <desc id="desc">{NAME_TEXT} is a {ROLE_TEXT.lower()} in {LOCATION_TEXT} working on AI agent systems, reusable engineering workflows, and product platforms.</desc>
{common_defs(theme, True)}
  <rect width="720" height="1380" fill="{theme['background']}" />
  <rect x="0.5" y="0.5" width="719" height="1379" fill="none" stroke="{theme['grid']}" stroke-opacity="0.12" />
  <g stroke="{theme['grid']}" stroke-opacity="0.10" stroke-width="1">
    <path d="M36 0V1380M360 0V1380M684 0V1380" />
    <path d="M0 88H720M0 726H720M0 1194H720" />
  </g>

  <g class="utility" font-size="12" fill="{theme['muted']}">
    <text x="36" y="48">{HANDLE} / PROFILE {VERSION}</text>
    <text x="684" y="48" text-anchor="end">{LOCATION} · DE</text>
  </g>
  <rect x="36" y="68" width="648" height="4" fill="{theme['coral']}" />
  <rect x="36" y="72" width="648" height="3" fill="{theme['acid']}" />

  <rect x="548" y="104" width="120" height="120" fill="{theme['mark']}" opacity="0.9" mask="url(#tr-mark)" />
  <text class="utility" x="36" y="132" font-size="13" fill="{theme['muted']}">{ROLE}</text>

  <g class="display" font-size="106" fill="{theme['foreground']}">
    <text x="36" y="258">{MOBILE_HEADLINE[0]}</text>
    <text x="36" y="356" fill="{theme['coral']}">{MOBILE_HEADLINE[1]}</text>
    <text x="36" y="454">{MOBILE_HEADLINE[2]}</text>
    <text x="36" y="552">{MOBILE_HEADLINE[3]}</text>
  </g>
  <text class="body" x="38" y="624" font-size="27" font-weight="540" fill="{theme['foreground']}">{TAGLINE}</text>
  <text class="utility" x="38" y="674" font-size="12" fill="{theme['muted']}">{DOMAINS}</text>

  <g class="body">
    <g transform="translate(36 780)">
      <text class="utility" y="0" font-size="13" fill="{theme['coral']}">01 / {FOCUS[0]['label']}</text>
      <text y="42" font-size="27" font-weight="650" fill="{theme['foreground']}">{FOCUS[0]['title']}</text>
      <text y="78" font-size="20" fill="{theme['muted']}">{FOCUS[0]['description']}</text>
    </g>
    <path d="M36 890H684" stroke="{theme['grid']}" stroke-opacity="0.16" />
    <g transform="translate(36 938)">
      <text class="utility" y="0" font-size="13" fill="{theme['coral']}">02 / {FOCUS[1]['label']}</text>
      <text y="42" font-size="27" font-weight="650" fill="{theme['foreground']}">{FOCUS[1]['title']}</text>
      <text y="78" font-size="20" fill="{theme['muted']}">{FOCUS[1]['description']}</text>
    </g>
    <path d="M36 1048H684" stroke="{theme['grid']}" stroke-opacity="0.16" />
    <g transform="translate(36 1096)">
      <text class="utility" y="0" font-size="13" fill="{theme['coral']}">03 / {FOCUS[2]['label']}</text>
      <text y="42" font-size="27" font-weight="650" fill="{theme['foreground']}">{FOCUS[2]['title']}</text>
      <text y="78" font-size="20" fill="{theme['muted']}">{FOCUS[2]['description']}</text>
    </g>
  </g>

  <g class="utility" font-size="12" fill="{theme['foreground']}">
    <text x="36" y="1254">{LOOP[0]}</text>
    <text x="196" y="1254">{LOOP[1]}</text>
    <text x="438" y="1254">{LOOP[2]}</text>
    <text x="650" y="1254" text-anchor="end">{LOOP[3]}</text>
  </g>
  <path d="M36 1292H684" stroke="{theme['grid']}" stroke-opacity="0.24" stroke-width="2" />
  <g fill="{theme['background']}" stroke="{theme['foreground']}" stroke-width="2">
    <circle cx="36" cy="1292" r="6" /><circle cx="252" cy="1292" r="6" /><circle cx="468" cy="1292" r="6" /><circle cx="684" cy="1292" r="6" />
  </g>
  <g clip-path="url(#signal-mobile-clip)">
    <clipPath id="signal-mobile-clip"><rect x="36" y="1281" width="648" height="22" /></clipPath>
    <rect class="signal" x="36" y="1287" width="120" height="10" rx="5" fill="url(#signal-gradient)" />
  </g>
</svg>"""


generated = []
for name, theme in THEMES.items():
    desktop_path = OUT / f"profile-poster-{name}.svg"
    mobile_path = OUT / f"profile-poster-mobile-{name}.svg"
    desktop_path.write_text(desktop(theme))
    mobile_path.write_text(mobile(theme))
    generated.extend((desktop_path.name, mobile_path.name))

print("generated", *sorted(generated))
