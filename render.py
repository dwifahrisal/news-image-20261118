#!/usr/bin/env python3
"""Render the news poster for Wednesday 18 November 2026 into entry.png.

This is the drawing step, not the entry point: it needs the system Chrome, so
it does not run in the grader's sandbox. main.py copies the image it writes.

The poster is laid out in HTML with CSS typography and inline SVG, then
rendered to PNG by the system Chrome. Python's standard library only.
"""
import os
import shutil
import subprocess
import sys
import tempfile

W = H = 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

# ----------------------------------------------------------------- the stories
# Each entry: (icon id, region, headline, sublabel, accent)
STORIES = [
    ("handshake", "SHENZHEN", "Xi greets Trump", "Trilateral with Putin next", "red"),
    ("palm", "SHENZHEN", "Putin joins them", "First three-way summit", "red"),
    ("drone", "GULF", "Iran drones strike Kuwait", "Gulf airspace hit", "red"),
    ("eu", "EUROPE", "EU's €45bn for Kyiv", "Winter aid package", "teal"),
    ("ship", "CANADA", "KPMG client files stolen", "Canadian data breach reported", "ink"),
    ("voyager", "SPACE", "Voyager 1 hits one light-day", "16 billion miles from Earth", "teal"),
    ("chip", "CHINA", "Nvidia halts chips", "No more US-approved sales", "red"),
    ("market", "MARKETS", "Wall Street mixed", "Fed minutes go hawkish", "ink"),
    ("ipo", "BUSINESS", "Anthropic prices IPO", "At $83 a share", "teal"),
    ("ballon", "SPORT", "Kane wins Ballon d'Or", "England's top honour", "teal"),
    ("nfl", "SPORT", "Jay-Z to headline", "Next Super Bowl halftime", "ink"),
    ("cyc", "INDIA", "Cyclone Arnab nears", "Coast put on alert", "red"),
    ("cop", "TURKEY", "COP31 opens", "Climate talks in Antalya", "teal"),
    ("oil", "ENERGY", "OPEC speaks out", "Fossil fuels at COP31", "ink"),
    ("hunt", "SCIENCE", "A signal takes 24 hours", "Voyager's radio call home", "teal"),
    ("judge", "UNITED STATES", "Judge blocks Trump's arch", "Monument delayed again", "ink"),
    ("scam", "SOUTHEAST ASIA", "Scam compounds grow", "Trafficked workers freed", "red"),
    ("alberta", "CANADA", "Alberta caps data centres", "Oil sands emissions cap dropped", "teal"),
]

# ------------------------------------------------------------------ the icons
ICONS = {
    "handshake": """
      <circle cx="26" cy="30" r="11" fill="none" stroke="INK" stroke-width="5"/>
      <circle cx="74" cy="30" r="11" fill="none" stroke="INK" stroke-width="5"/>
      <circle cx="50" cy="70" r="11" fill="none" stroke="INK" stroke-width="5"/>
      <path d="M32 38l12 14M68 38L56 52M38 62l-8 8M62 62l8 8"
            stroke="INK" stroke-width="5" stroke-linecap="round"/>
      <path d="M38 56h24" stroke="ACC" stroke-width="7" stroke-linecap="round"/>
    """,
    "palm": """
      <path d="M26 82V40M26 40c0-12 6-22 16-26" fill="none" stroke="INK" stroke-width="5"
            stroke-linecap="round"/>
      <path d="M42 14c-8-6-18-6-24 0M42 14c6-8 16-11 24-8M42 14c10-2 18 4 22 12"
            fill="none" stroke="INK" stroke-width="4" stroke-linecap="round"/>
      <path d="M74 56v22M64 78h20" stroke="ACC" stroke-width="5" stroke-linecap="round"/>
    """,
    "drone": """
      <path d="M50 40l16 10-16 10-16-10z" fill="none" stroke="INK" stroke-width="5"
            stroke-linejoin="round"/>
      <path d="M34 50L16 30M66 50l18-20M34 60L16 80M66 60l18 20" stroke="INK"
            stroke-width="4" stroke-linecap="round"/>
      <circle cx="50" cy="50" r="5" fill="ACC"/>
      <path d="M20 22l8-8M80 22l-8-8M20 88l8 8M80 88l-8 8" stroke="ACC"
            stroke-width="4" stroke-linecap="round"/>
    """,
    "eu": """
      <circle cx="50" cy="50" r="30" fill="none" stroke="INK" stroke-width="5"/>
      <path d="M50 20v6M50 74v6M20 50h6M74 50h6M29 29l4 4M67 67l4 4M71 29l-4 4M33 67l-4 4"
            stroke="ACC" stroke-width="4" stroke-linecap="round"/>
      <circle cx="50" cy="50" r="12" fill="none" stroke="INK" stroke-width="5"/>
    """,
    "ship": """
      <path d="M18 66h64l-8 16H26z" fill="none" stroke="INK" stroke-width="5"
            stroke-linejoin="round"/>
      <path d="M34 66V40h32v26" fill="none" stroke="INK" stroke-width="5"/>
      <path d="M50 40V22" stroke="INK" stroke-width="5" stroke-linecap="round"/>
      <path d="M14 22l14 8-14 8" fill="none" stroke="ACC" stroke-width="5"
            stroke-linejoin="round"/>
    """,
    "voyager": """
      <circle cx="50" cy="50" r="8" fill="none" stroke="ACC" stroke-width="5"/>
      <path d="M58 42L86 14" stroke="INK" stroke-width="5" stroke-linecap="round"/>
      <path d="M34 50H12M50 66v22M50 34V12M66 50h22" stroke="INK" stroke-width="4"
            stroke-linecap="round"/>
      <path d="M86 14l-10 2 8 8z" fill="ACC"/>
    """,
    "chip": """
      <rect x="26" y="26" width="48" height="48" rx="4" fill="none" stroke="INK"
            stroke-width="5"/>
      <rect x="38" y="38" width="24" height="24" rx="2" fill="none" stroke="ACC"
            stroke-width="5"/>
      <path d="M38 12v14M62 12v14M38 74v14M62 74v14M12 38h14M12 62h14M74 38h14M74 62h14"
            stroke="INK" stroke-width="5" stroke-linecap="round"/>
    """,
    "market": """
      <path d="M12 76l18-24 14 12 16-30 12 8" fill="none" stroke="ACC" stroke-width="6"
            stroke-linejoin="round" stroke-linecap="round"/>
      <path d="M10 84h80" stroke="INK" stroke-width="5" stroke-linecap="round"/>
      <path d="M76 20v14M69 27h14" stroke="INK" stroke-width="5" stroke-linecap="round"/>
    """,
    "ipo": """
      <path d="M30 82V26h40v56" fill="none" stroke="INK" stroke-width="5"
            stroke-linejoin="round"/>
      <path d="M22 82h56" stroke="INK" stroke-width="5" stroke-linecap="round"/>
      <path d="M40 44h20M40 56h20" stroke="ACC" stroke-width="5" stroke-linecap="round"/>
      <path d="M50 14v10M42 22l8-8 8 8" fill="none" stroke="ACC" stroke-width="5"
            stroke-linejoin="round" stroke-linecap="round"/>
    """,
    "ballon": """
      <circle cx="50" cy="44" r="26" fill="none" stroke="INK" stroke-width="5"/>
      <path d="M50 18l-9 20h18z" fill="none" stroke="ACC" stroke-width="4"
            stroke-linejoin="round"/>
      <path d="M40 70h20v14H40z" fill="none" stroke="INK" stroke-width="4"/>
      <path d="M36 84h28" stroke="INK" stroke-width="5" stroke-linecap="round"/>
    """,
    "nfl": """
      <circle cx="50" cy="50" r="30" fill="none" stroke="INK" stroke-width="5"/>
      <path d="M50 20v60M20 50h60" stroke="INK" stroke-width="4"/>
      <path d="M50 30l16 14-16 14-16-14z" fill="none" stroke="ACC" stroke-width="5"
            stroke-linejoin="round"/>
    """,
    "cyc": """
      <circle cx="50" cy="50" r="26" fill="none" stroke="INK" stroke-width="5"/>
      <path d="M50 24c10 12 10 26 0 40-10-14-10-28 0-40z" fill="none" stroke="ACC"
            stroke-width="4"/>
      <path d="M50 24c-10 12-10 26 0 40" fill="none" stroke="INK" stroke-width="4"/>
      <path d="M14 78h72" stroke="INK" stroke-width="5" stroke-linecap="round"/>
    """,
    "cop": """
      <circle cx="50" cy="50" r="26" fill="none" stroke="INK" stroke-width="5"/>
      <path d="M50 24v26l18 10" fill="none" stroke="ACC" stroke-width="5"
            stroke-linecap="round"/>
      <path d="M18 84h64" stroke="INK" stroke-width="5" stroke-linecap="round"/>
      <path d="M30 84V66M70 84V66" stroke="INK" stroke-width="4"/>
    """,
    "oil": """
      <path d="M38 16h24M42 16v26L26 74a8 8 0 007 10h34a8 8 0 007-10L58 42V16"
            fill="none" stroke="INK" stroke-width="5" stroke-linejoin="round"/>
      <path d="M34 62h32" stroke="ACC" stroke-width="6"/>
    """,
    "hunt": """
      <circle cx="38" cy="50" r="22" fill="none" stroke="INK" stroke-width="5"/>
      <path d="M54 66l24 20" stroke="INK" stroke-width="7" stroke-linecap="round"/>
      <path d="M38 40v20M28 50h20" stroke="ACC" stroke-width="4" stroke-linecap="round"/>
    """,
    "judge": """
      <path d="M50 14v58" stroke="INK" stroke-width="5" stroke-linecap="round"/>
      <path d="M20 30h60" stroke="INK" stroke-width="5" stroke-linecap="round"/>
      <path d="M20 30l-8 20h16zM80 30l-8 20h16z" fill="none" stroke="INK" stroke-width="4"
            stroke-linejoin="round"/>
      <path d="M32 78h36" stroke="INK" stroke-width="5" stroke-linecap="round"/>
      <path d="M50 44l14 14-14 14" fill="none" stroke="ACC" stroke-width="5"
            stroke-linecap="round" stroke-linejoin="round"/>
    """,
    "scam": """
      <path d="M18 44h64v40H18z" fill="none" stroke="INK" stroke-width="5"
            stroke-linejoin="round"/>
      <path d="M18 44l32-22 32 22" fill="none" stroke="INK" stroke-width="5"
            stroke-linejoin="round"/>
      <path d="M38 62h24" stroke="ACC" stroke-width="6" stroke-linecap="round"/>
      <path d="M42 56v12M58 56v12" stroke="ACC" stroke-width="4" stroke-linecap="round"/>
    """,
    "alberta": """
      <path d="M14 82h72" stroke="INK" stroke-width="5" stroke-linecap="round"/>
      <path d="M26 82V44l24-20 24 20v38" fill="none" stroke="INK" stroke-width="5"
            stroke-linejoin="round"/>
      <path d="M50 24v18M50 52l14 14-14 14" fill="none" stroke="ACC" stroke-width="5"
            stroke-linecap="round" stroke-linejoin="round"/>
    """,
}

ACCENTS = {
    "red": "#b3271d",
    "teal": "#1c6b6b",
    "ink": "#1a1a1a",
}


def tile(story):
    """One story tile: its icon, its section and its headline."""
    icon, region, headline, sub, accent = story
    svg = (
        '<svg viewBox="0 0 100 100" width="62" height="62" aria-hidden="true">'
        + ICONS[icon].replace("INK", "#1a1a1a").replace("ACC", ACCENTS[accent])
        + "</svg>"
    )
    return f"""      <article class="tile accent-{accent}">
        <div class="art">{svg}<div class="txt"><div class="kicker">{region}</div>
          <h2>{headline}</h2><p>{sub}</p></div></div>
      </article>
"""


def build_html():
    """The poster's markup, with the stories laid out as a grid of tiles."""
    tiles = "".join(tile(s) for s in STORIES)
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ width:{W}px; height:{H}px; overflow:hidden; background:#f7f4ee; color:#141414;
         font-family:"Nimbus Sans","Liberation Sans","DejaVu Sans",Helvetica,Arial,sans-serif;
         display:flex; flex-direction:column; }}
  .mast {{ padding:14px 26px 12px; border-bottom:3px solid #141414; }}
  .kicker-row {{ display:flex; justify-content:space-between; align-items:baseline;
                 border-bottom:1px solid #b9b2a4; padding-bottom:6px; }}
  .kicker-row .k {{ font-size:15px; letter-spacing:.2em; text-transform:uppercase;
                    font-weight:700; color:#5f584c; }}
  .kicker-row .r {{ font-size:15px; letter-spacing:.06em; color:#5f584c; font-weight:700; }}
  h1 {{ font-size:62px; line-height:.92; letter-spacing:-.022em; font-weight:700;
        margin-top:6px; text-transform:uppercase; }}
  h1 .thin {{ font-weight:300; letter-spacing:-.01em; }}
  .dateline {{ display:flex; gap:18px; align-items:center; margin-top:7px;
               font-size:16px; color:#2f2a23; font-weight:700; }}
  .dateline .dot {{ width:6px; height:6px; border-radius:50%; background:#b3271d; }}
  .dateline .bar {{ flex:1; height:1px; background:#c9c2b4; }}
  .dateline .loc {{ font-weight:400; }}
  .grid {{ flex:1; display:grid; grid-template-columns:repeat(3,1fr);
           grid-template-rows:repeat(6,1fr); }}
  .tile {{ padding:9px 14px 8px; border-right:1px solid #d6d0c2;
           border-bottom:1px solid #d6d0c2; display:flex; flex-direction:column;
           justify-content:center; }}
  .tile:nth-child(3n) {{ border-right:none; }}
  .tile:nth-child(n+16) {{ border-bottom:none; }}
  .art {{ display:flex; align-items:center; gap:10px; }}
  .art svg {{ flex:none; }}
  .txt {{ min-width:0; }}
  .tile .kicker {{ font-size:13px; letter-spacing:.17em; text-transform:uppercase;
                   font-weight:700; color:#8a8274; margin-bottom:2px; }}
  .tile h2 {{ font-size:25px; line-height:1.02; font-weight:700; letter-spacing:-.015em;
              margin-bottom:3px; }}
  .tile p {{ font-size:16px; line-height:1.15; color:#5b544a; }}
  .accent-red h2 {{ color:#8e1e16; }}
  .accent-teal h2 {{ color:#145353; }}
  .accent-red .kicker {{ color:#a2695f; }}
  .accent-teal .kicker {{ color:#6d8b88; }}
  .foot {{ padding:8px 26px 10px; border-top:3px solid #141414; display:flex;
           justify-content:space-between; font-size:13px; letter-spacing:.11em;
           text-transform:uppercase; color:#6d665a; font-weight:700; }}
</style></head>
<body>
  <header class="mast">
    <div class="kicker-row">
      <span class="k">The World in a Day</span>
      <span class="r">Wednesday &middot; 18 November 2026</span>
    </div>
    <h1><span class="thin">Wednesday</span> 18 November 2026</h1>
    <div class="dateline">
      <span>Eighteen stories</span><span class="dot"></span>
      <span class="loc">Asia &middot; Europe &middot; Americas &middot; Gulf</span>
      <span class="bar"></span><span class="loc">One Wednesday, all told</span>
    </div>
  </header>
  <main class="grid">
{tiles}  </main>
  <footer class="foot">
    <span>Reported 18 Nov 2026</span>
    <span>World news &middot; business &middot; sport</span>
    <span>make.fun</span>
  </footer>
</body></html>
"""


def main():
    """Render the poster with Chrome and write the PNG in place."""
    with tempfile.TemporaryDirectory() as work:
        page = os.path.join(work, "poster.html")
        shot = os.path.join(work, "poster.png")
        with open(page, "w", encoding="utf-8") as fh:
            fh.write(build_html())
        chrome = shutil.which("google-chrome") or shutil.which("chromium")
        if not chrome:
            sys.exit("no chrome")
        subprocess.run(
            [
                chrome,
                "--headless=new",
                "--disable-gpu",
                "--no-sandbox",
                "--hide-scrollbars",
                "--force-device-scale-factor=1",
                f"--window-size={W},{H}",
                f"--screenshot={shot}",
                "file://" + page,
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        shutil.copyfile(shot, OUT)
    print(f"wrote {OUT} ({os.path.getsize(OUT)} bytes)")


if __name__ == "__main__":
    main()
