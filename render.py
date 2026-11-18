#!/usr/bin/env python3
"""Render the 18 Nov 2026 world-news image as HTML, screenshot to PNG via Chrome.

A full one-page international front page for "The Daily Brief": masthead, lead
story with a labelled map graphic, three secondary stories, six briefs, a
markets strip, an inside-the-paper index, a weather/sport rail, and a bottom
feature well with body copy.

Real print typography (Liberation Serif / Liberation Sans / DejaVu). Stdlib-only
program; Chrome headless rasterises, main.py copies the PNG to /output/entry.png.
"""
import subprocess, tempfile, os, sys

W, H = 1024, 1024

LEAD_ART = '''<svg viewBox="0 0 320 210" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="sea" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#eaf0f6"/><stop offset="1" stop-color="#d2dee9"/>
    </linearGradient>
  </defs>
  <rect width="320" height="210" fill="url(#sea)"/>
  <path d="M0 118 Q80 100 160 118 T320 118 L320 210 L0 210 Z" fill="#cddae6" opacity=".7"/>
  <path d="M0 138 Q90 120 180 138 T320 138 L320 210 L0 210 Z" fill="#bdccd9" opacity=".6"/>
  <circle cx="160" cy="96" r="58" fill="#f8fafc" stroke="#8fa3b5" stroke-width="1.5"/>
  <path d="M102 96h116M160 38c19 21 19 95 0 116M160 38c-19 21-19 95 0 116" fill="none" stroke="#bccad7" stroke-width="1.3"/>
  <path d="M160 42c24 6 42 20 46 54" fill="none" stroke="#8a1c1c" stroke-width="2.2" stroke-dasharray="4 3"/>
  <circle cx="206" cy="96" r="4.4" fill="#8a1c1c"/>
  <circle cx="160" cy="96" r="3.8" fill="#0e7490"/>
  <circle cx="114" cy="96" r="2.8" fill="#b45309"/>
  <text x="206" y="82" font-family="Liberation Sans, sans-serif" font-size="7.5" fill="#3a3a3a" text-anchor="middle">SHENZHEN</text>
  <text x="160" y="124" font-family="Liberation Sans, sans-serif" font-size="7.5" fill="#3a3a3a" text-anchor="middle">PACIFIC</text>
  <text x="160" y="196" font-family="Liberation Sans, sans-serif" font-size="8" fill="#5b6b7a" text-anchor="middle" letter-spacing="2">APEC 2026 · TRILATERAL</text>
</svg>'''

LEAD = dict(
    kicker="DIPLOMACY · SHENZHEN",
    head="Putin lands in Shenzhen as Xi, Trump and world leaders gather for APEC",
    dek="Putin arrived on Wednesday for the APEC summit, hours before a <b>historic trilateral meeting</b> with Trump and Xi. Xi pressed his case for <b>&quot;free and open trade&quot;</b> and met Canada&rsquo;s Mark Carney, who announced tariff cuts on pork and seafood.",
    byline="By Elena Marchetti in Shenzhen",
)

SIDE = [
    ("MIDDLE EAST", "US and Iran trade fire despite mediation",
     "US strikes an Iranian missile site; Iran says it hit a US radar system in Bahrain.", "#8a1c1c"),
    ("YEMEN", "64 children killed since September as war reignites",
     "800,000 are cut off in Taiz; UNICEF warns schools and clinics have been hit.", "#15803d"),
    ("HEALTH", "Superbugs now resist last-resort antibiotics",
     "WHO and ECDC find resistance in half of European samples; first-line drugs are failing.", "#b91c1c"),
]

BRIEFS = [
    ("RUSSIA", "Military An-12 crash in Siberia kills all 17 aboard",
     "The transport aircraft came down in the Kemerovo region; Izvestia reported no survivors.", "#475569"),
    ("MARKETS", "NVIDIA beats forecasts as board turmoil unsettles investors",
     "The chipmaker guided higher than Wall Street expectations, easing concern over its corporate shake-up.", "#15803d"),
    ("AFGHANISTAN", "UN releases $18m for 824,000 Afghans facing winter",
     "The pooled fund is a stopgap against a $1.2bn shortfall, prioritising returnees and displaced families.", "#b45309"),
    ("RED SEA", "Saudi forces strike Houthi positions in major attack",
     "Riyadh says the response came after attacks on southern routes; casualties are not yet confirmed.", "#0e7490"),
    ("ALASKA", "Peltola wins Alaska Senate race in final recount",
     "The incumbent holds the seat after a marathon count that swung twice on overseas ballots.", "#6d28d9"),
    ("EUROPE", "Geneva talks open with ceasefire proposal on the table",
     "Negotiators from 14 states meet for two days with no guarantee of a deal.", "#334155"),
]

MARKETS = [
    ("S&amp;P 500", "6,412.18", "+0.42%"),
    ("NASDAQ", "20,884.77", "+0.61%"),
    ("BTC/USD", "63,260", "-2.72%"),
    ("EUR/USD", "1.0842", "-0.13%"),
    ("BRENT", "74.18", "+1.05%"),
    ("GOLD", "2,318.4", "+0.31%"),
]

INDEX = [
    ("CLIMATE", "Philippines braces for storm as Haiyan anniversary nears"),
    ("BUSINESS", "Chip stocks rally ahead of the Shenzhen summit"),
    ("OPINION", "Why the trilateral meeting matters more than it looks"),
    ("SPORT", "Mbappe injury clouds Real Madrid trip"),
    ("SCIENCE", "Deep-sea vents map redrawn after new survey"),
]

FEATURE = dict(
    kicker="THE SUMMIT IN PERSPECTIVE",
    head="Three leaders, one table, and a trade order nobody has read",
    body=[
        "The trilateral meeting convened for Thursday is the first of its kind. The three aides who negotiated the "
        "final agenda described a format deliberately loose: no communique, no signing ceremony, and a closing "
        "session that officials expect could run past midnight.",
        "That informality is the point. Officials from all three delegations say the talks are designed to deliver "
        "nothing binding, which lowers the cost of saying things out loud in a year when tariff schedules are being "
        "revised every quarter.",
        "Market economists were split on the implications. Some read the meeting as a signal that export controls "
        "will not tighten further before the year ends. Others cautioned that a photo opportunity carries no "
        "authority of its own, and that the substance will be tested in shipping manifests rather than in remarks.",
        "The delegations arrived with different mandates. Beijing has insisted that any broader agreement would "
        "require a public gesture on technology restrictions; Washington has resisted tying trade talk to security "
        "matters; and Moscow, attending for the first time, has pushed for language on grain and energy corridors "
        "that its envoys call a matter of basic stability.",
        "Aides on all sides described the agenda as deliberately narrow: energy pricing, agricultural access, and a "
        "framework for resuming low-level working groups that have been frozen since the spring. No delegation "
        "expected a signed document, and officials said the closing session was designed as an exchange of "
        "positions rather than a negotiation.",
        "Economists who have followed the tariff file for years said the more important signal was the seating "
        "chart. The three leaders had not appeared at the same table since the last round of sanctions, and the "
        "scheduling of a private session on the second day, without staff present, was described by two officials "
        "as the clearest indication that something beyond protocol was being attempted.",
    ],
    byline="By Tomas Rehn and Aiko Tanaka",
)


def side_html(k, h, d, c):
    return f'''<div class="side" style="--c:{c}">
      <div class="k">{k}</div><h3>{h}</h3><p>{d}</p></div>'''


def brief_html(k, h, d, c):
    return f'''<div class="brief" style="--c:{c}">
      <div class="k">{k}</div><h4>{h}</h4><p>{d}</p></div>'''


HTML = f'''<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
  @page {{ margin:0; }}
  * {{ box-sizing:border-box; margin:0; padding:0; }}
  html,body {{ width:{W}px; height:{H}px; overflow:hidden; }}
  body {{ width:{W}px; height:{H}px; overflow:hidden; background:#f8f6f1; color:#121212;
          padding:16px 26px 13px; display:flex; flex-direction:column;
          font-family:"Liberation Serif","DejaVu Serif",Georgia,serif; }}

  .top {{ display:flex; justify-content:space-between; align-items:flex-end;
          border-bottom:3px solid #121212; padding-bottom:4px; }}
  .name {{ font-size:40px; font-weight:700; letter-spacing:-.022em; line-height:.9; }}
  .name .thin {{ font-weight:400; font-style:italic; }}
  .meta {{ text-align:right; font-family:"Liberation Sans","DejaVu Sans",sans-serif;
           font-size:9px; line-height:1.5; color:#3a3a3a; letter-spacing:.03em; }}
  .meta b {{ color:#121212; }}
  .dateline {{ display:flex; justify-content:space-between; align-items:center;
               font-family:"Liberation Sans","DejaVu Sans",sans-serif; font-size:9px;
               letter-spacing:.14em; text-transform:uppercase; color:#3a3a3a;
               border-bottom:1px solid #121212; padding:3px 0 4px; margin-bottom:7px; }}
  .dateline .vol {{ color:#8a1c1c; font-weight:700; }}

  .lead {{ display:grid; grid-template-columns: 1.2fr 1fr; gap:14px;
           border-bottom:1px solid #bdbdbd; padding-bottom:8px; margin-bottom:7px; }}
  .lead-main .kicker {{ font-family:"Liberation Sans",sans-serif; font-size:9px; font-weight:700;
                        letter-spacing:.14em; text-transform:uppercase; color:#8a1c1c; margin-bottom:1px; }}
  .lead-main h1 {{ font-size:28px; line-height:1.05; font-weight:700; letter-spacing:-.014em; margin-bottom:4px; }}
  .lead-main .dek {{ font-size:12px; line-height:1.38; color:#2a2a2a; }}
  .lead-main .dek b {{ color:#121212; }}
  .byline {{ font-family:"Liberation Sans",sans-serif; font-size:8.5px; color:#6a6a6a;
             font-style:italic; margin-top:3px; }}
  .lead-art svg {{ width:100%; height:auto; border:1px solid #cfd6dd; display:block; }}

  .band3 {{ display:grid; grid-template-columns:1fr 1fr 1fr; gap:13px;
            border-bottom:1px solid #bdbdbd; padding-bottom:7px; margin-bottom:7px; }}
  .side {{ border-left:3px solid var(--c); padding-left:6px; }}
  .side .k {{ font-family:"Liberation Sans",sans-serif; font-size:8px; font-weight:700;
              letter-spacing:.1em; text-transform:uppercase; color:var(--c); }}
  .side h3 {{ font-size:12.5px; line-height:1.12; font-weight:700; margin-top:1px; }}
  .side p {{ font-family:"Liberation Sans",sans-serif; font-size:9px; line-height:1.28;
             color:#444; margin-top:1px; }}

  .band6 {{ display:grid; grid-template-columns:1fr 1fr 1fr; gap:8px 17px;
            border-bottom:1px solid #bdbdbd; padding-bottom:7px; margin-bottom:7px; }}
  .brief {{ border-top:2px solid #121212; padding-top:3px; }}
  .brief .k {{ font-family:"Liberation Sans",sans-serif; font-size:8px; font-weight:700;
               letter-spacing:.1em; text-transform:uppercase; color:var(--c); }}
  .brief h4 {{ font-size:12px; line-height:1.12; font-weight:700; margin:1px 0 2px; }}
  .brief p {{ font-family:"Liberation Sans",sans-serif; font-size:9px; line-height:1.28; color:#444; }}

  .bot {{ display:grid; grid-template-columns: 1.15fr 1fr 1fr; gap:16px; flex:0 0 auto;
          border-bottom:1px solid #bdbdbd; padding-bottom:7px; margin-bottom:7px; }}
  .mkt, .idx, .wx {{ border-top:2px solid #121212; padding-top:3px; }}
  .mkt .hd, .idx .hd, .wx .hd {{ font-family:"Liberation Sans",sans-serif; font-size:8px; font-weight:700;
      letter-spacing:.12em; text-transform:uppercase; color:#121212;
      border-bottom:1px solid #bdbdbd; padding-bottom:2px; margin-bottom:2px; }}
  .mkt table {{ width:100%; border-collapse:collapse; font-family:"Liberation Sans",sans-serif; font-size:9px; }}
  .mkt td {{ padding:1px 0; border-bottom:1px dotted #ccc; color:#333; }}
  .mkt td.n {{ text-align:right; font-variant-numeric:tabular-nums; color:#121212; }}
  .mkt td.up {{ text-align:right; color:#15803d; }}
  .mkt td.dn {{ text-align:right; color:#b91c1c; }}

  .idx .it {{ display:flex; gap:5px; padding:2px 0; border-bottom:1px dotted #ccc;
              font-family:"Liberation Sans",sans-serif; font-size:9px; line-height:1.22; }}
  .idx .it b {{ color:#8a1c1c; font-weight:700; flex:0 0 auto; }}
  .idx .it span {{ color:#333; }}

  .wx .row {{ display:flex; justify-content:space-between; align-items:center;
              font-family:"Liberation Sans",sans-serif; font-size:9px; padding:1.5px 0;
              border-bottom:1px dotted #ccc; color:#333; }}
  .wx .row b {{ color:#121212; }}
  .wx .fc {{ font-family:"Liberation Serif",serif; font-size:9.5px; color:#444; line-height:1.3; margin-top:3px; font-style:italic; }}

  .feature {{ flex:1; display:grid; grid-template-columns: 1fr 1fr 1fr; gap:0 18px;
              border-top:2px solid #121212; padding-top:5px; overflow:hidden; align-content:start; }}
  .feature .leadcol {{ padding-right:18px; border-right:1px solid #ccc; }}
  .feature .kicker {{ font-family:"Liberation Sans",sans-serif; font-size:8.5px; font-weight:700;
                      letter-spacing:.13em; text-transform:uppercase; color:#8a1c1c; margin-bottom:2px; }}
  .feature h2 {{ font-size:19px; line-height:1.08; font-weight:700; letter-spacing:-.008em; margin-bottom:4px; }}
  .feature .first {{ font-size:11px; line-height:1.42; color:#2a2a2a; text-align:justify; }}
  .feature .first::first-letter {{ float:left; font-size:40px; line-height:.82; padding:2px 5px 0 0; color:#8a1c1c; }}
  .feature .col {{ font-size:9.5px; line-height:1.42; color:#333; text-align:justify; }}
  .feature .col p {{ margin-bottom:5px; }}
  .feature .byline {{ font-family:"Liberation Sans",sans-serif; font-size:8.5px; color:#6a6a6a;
                      font-style:italic; margin-top:4px; }}
  .feature .pull {{ font-family:"Liberation Serif",serif; font-size:11px; line-height:1.32;
                    font-style:italic; color:#121212; border-left:3px solid #8a1c1c;
                    padding-left:8px; margin:7px 0; }}

  .foot {{ margin-top:5px; border-top:1px solid #121212; padding-top:3px;
           font-family:"Liberation Sans",sans-serif; font-size:8px; color:#6a6a6a;
           display:flex; justify-content:space-between; letter-spacing:.04em; }}
</style></head>
<body>
  <div class="top">
    <div class="name">The Daily <span class="thin">Brief</span></div>
    <div class="meta">INTERNATIONAL EDITION &nbsp;·&nbsp; ONE PAGE<br>
      <b>18 NOVEMBER 2026</b> &nbsp;·&nbsp; 08:00 GMT</div>
  </div>
  <div class="dateline">
    <span>Volume 1 &nbsp;·&nbsp; No. 1 &nbsp;·&nbsp; 18 November 2026</span>
    <span class="vol">TODAY &mdash; 14 STORIES, ONE PAGE</span>
  </div>

  <div class="lead">
    <div class="lead-main">
      <div class="kicker">{LEAD['kicker']}</div>
      <h1>{LEAD['head']}</h1>
      <p class="dek">{LEAD['dek']}</p>
      <div class="byline">{LEAD['byline']}</div>
    </div>
    <div class="lead-art">{LEAD_ART}</div>
  </div>

  <div class="band3">{''.join(side_html(*s) for s in SIDE)}</div>

  <div class="band6">{''.join(brief_html(*b) for b in BRIEFS)}</div>

  <div class="bot">
    <div class="mkt">
      <div class="hd">Markets at the close</div>
      <table>
        {''.join(f'<tr><td>{n}</td><td class="n">{v}</td><td class="{"up" if u.startswith("+") else "dn"}">{u}</td></tr>' for n,v,u in MARKETS)}
      </table>
    </div>
    <div class="idx">
      <div class="hd">Inside today&rsquo;s brief</div>
      {''.join(f'<div class="it"><b>{t}</b><span>{d}</span></div>' for t,d in INDEX)}
    </div>
    <div class="wx">
      <div class="hd">Weather &amp; sport</div>
      <div class="row"><span><b>Beijing</b> · China</span><span>2&deg; / -3&deg;</span></div>
      <div class="row"><span><b>Shenzhen</b> · China</span><span>21&deg; / 16&deg;</span></div>
      <div class="row"><span><b>Sydney</b> · Australia</span><span>24&deg; / 18&deg;</span></div>
      <div class="row"><span><b>Manila</b> · Philippines</span><span>27&deg; / 25&deg;</span></div>
      <div class="row"><span><b>London</b> · UK</span><span>9&deg; / 5&deg;</span></div>
      <div class="fc">Storm warning for the northern Philippines; Real Madrid await Mbappe&rsquo;s fitness test.</div>
    </div>
  </div>

  <div class="feature">
    <div class="leadcol">
      <div class="kicker">{FEATURE['kicker']}</div>
      <h2>{FEATURE['head']}</h2>
      <p class="first">{FEATURE['body'][0]}</p>
      <p class="col" style="margin-top:6px">{FEATURE['body'][1]}</p>
      <div class="byline">{FEATURE['byline']}</div>
    </div>
    <div class="col">
      <p>{FEATURE['body'][2]}</p>
      <p>{FEATURE['body'][3]}</p>
      <p class="pull">No communique. No signing ceremony. A closing session that could run past midnight &mdash; and, aides say, a private meeting with no staff in the room.</p>
    </div>
    <div class="col">
      <p>{FEATURE['body'][4]}</p>
      <p>{FEATURE['body'][5]}</p>
    </div>
  </div>

  <div class="foot">
    <span>THE DAILY BRIEF &mdash; 18 NOVEMBER 2026 &mdash; 14 STORIES, ONE PAGE</span>
    <span>01 / 01</span>
  </div>
</body></html>'''


def render(out_png):
    with tempfile.NamedTemporaryFile('w', suffix='.html', delete=False, encoding='utf-8') as f:
        f.write(HTML)
        html_path = f.name
    try:
        subprocess.run([
            'google-chrome', '--headless=new', '--disable-gpu', '--no-sandbox',
            '--hide-scrollbars', '--force-device-scale-factor=1',
            f'--window-size={W},{H}',
            f'--screenshot={out_png}',
            f'file://{html_path}',
        ], check=True, capture_output=True, timeout=60)
    finally:
        os.unlink(html_path)
    return out_png


if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else 'entry.png'
    render(out)
    print(f'rendered {out} ({os.path.getsize(out)} bytes)')
