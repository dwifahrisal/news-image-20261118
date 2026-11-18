"""news-image-20261118: one image summing up the world's news of 18 November 2026.

Renders a 1024x1024 PNG news collage with pure standard library (zlib + struct):
no PIL, no network, deterministic. The image names its day, shows the day's most
consequential stories across regions and fields, and reads at a glance.

Stories depicted (18 Nov 2026):
  - APEC summit, Shenzhen: Putin arrives, Xi on free trade, Xi-Carney Canada-China deal
  - Trump trilateral summit with Putin & Xi in China
  - US-Iran exchange fire: US strikes Iranian missile site; Iran targets US radar in Bahrain
  - Yemen war: 64 children killed since Sept, 800k cut off in Taiz
  - Russia An-12 military transport crash in Siberia, 17 dead
  - WHO superbug alert: Klebsiella resistance up 72% since 2019
  - Nvidia: Huang resignation scandal, strong quarterly results
  - Afghanistan: UN releases $18M emergency funding for 824k people

Each panel is drawn as a clean geometric icon + short label on a dark canvas.
"""

import zlib
import struct

W = H = 1024

# ---------------------------------------------------------------- PNG encoding
def write_png(path, pixels):
    """pixels: list of rows, each row a list of (r,g,b) tuples."""
    raw = bytearray()
    for row in pixels:
        raw.append(0)  # filter type 0 (None) per scanline
        for r, g, b in row:
            raw += bytes((r, g, b))
    def chunk(tag, data):
        return (struct.pack(">I", len(data)) + tag + data +
                struct.pack(">I", zlib.crc32(tag + data) & 0xffffffff))
    sig = b"\x89PNG\r\n\x1a\n"
    ihdr = struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0)  # 8-bit RGB
    idat = zlib.compress(bytes(raw), 9)
    with open(path, "wb") as f:
        f.write(sig)
        f.write(chunk(b"IHDR", ihdr))
        f.write(chunk(b"IDAT", idat))
        f.write(chunk(b"IEND", b""))

# ---------------------------------------------------------------- canvas
def new_canvas(bg):
    return [[bg for _ in range(W)] for _ in range(H)]

def fill_rect(px, x0, y0, x1, y1, color):
    x0, y0 = max(0, x0), max(0, y0)
    x1, y1 = min(W, x1), min(H, y1)
    for y in range(y0, y1):
        row = px[y]
        for x in range(x0, x1):
            row[x] = color

def draw_circle(px, cx, cy, r, color):
    r2 = r * r
    for y in range(max(0, cy - r), min(H, cy + r + 1)):
        dy = y - cy
        for x in range(max(0, cx - r), min(W, cx + r + 1)):
            dx = x - cx
            if dx * dx + dy * dy <= r2:
                px[y][x] = color

def draw_rect_outline(px, x0, y0, x1, y1, color, t=3):
    fill_rect(px, x0, y0, x1, y0 + t, color)
    fill_rect(px, x0, y1 - t, x1, y1, color)
    fill_rect(px, x0, y0, x0 + t, y1, color)
    fill_rect(px, x1 - t, y0, x1, y1, color)

# ---------------------------------------------------------------- 5x7 bitmap font
FONT = {
    'A': ["01110","10001","10001","11111","10001","10001","10001"],
    'B': ["11110","10001","10001","11110","10001","10001","11110"],
    'C': ["01110","10001","10000","10000","10000","10001","01110"],
    'D': ["11110","10001","10001","10001","10001","10001","11110"],
    'E': ["11111","10000","10000","11110","10000","10000","11111"],
    'F': ["11111","10000","10000","11110","10000","10000","10000"],
    'G': ["01110","10001","10000","10111","10001","10001","01110"],
    'H': ["10001","10001","10001","11111","10001","10001","10001"],
    'I': ["01110","00100","00100","00100","00100","00100","01110"],
    'J': ["00111","00010","00010","00010","00010","10010","01100"],
    'K': ["10001","10010","10100","11000","10100","10010","10001"],
    'L': ["10000","10000","10000","10000","10000","10000","11111"],
    'M': ["10001","11011","10101","10101","10001","10001","10001"],
    'N': ["10001","11001","10101","10011","10001","10001","10001"],
    'O': ["01110","10001","10001","10001","10001","10001","01110"],
    'P': ["11110","10001","10001","11110","10000","10000","10000"],
    'Q': ["01110","10001","10001","10001","10101","10010","01101"],
    'R': ["11110","10001","10001","11110","10100","10010","10001"],
    'S': ["01111","10000","10000","01110","00001","00001","11110"],
    'T': ["11111","00100","00100","00100","00100","00100","00100"],
    'U': ["10001","10001","10001","10001","10001","10001","01110"],
    'V': ["10001","10001","10001","10001","10001","01010","00100"],
    'W': ["10001","10001","10001","10101","10101","11011","10001"],
    'X': ["10001","10001","01010","00100","01010","10001","10001"],
    'Y': ["10001","10001","01010","00100","00100","00100","00100"],
    'Z': ["11111","00001","00010","00100","01000","10000","11111"],
    '0': ["01110","10001","10011","10101","11001","10001","01110"],
    '1': ["00100","01100","00100","00100","00100","00100","01110"],
    '2': ["01110","10001","00001","00110","01000","10000","11111"],
    '3': ["11110","00001","00001","01110","00001","00001","11110"],
    '4': ["00010","00110","01010","10010","11111","00010","00010"],
    '5': ["11111","10000","11110","00001","00001","10001","01110"],
    '6': ["01110","10000","10000","11110","10001","10001","01110"],
    '7': ["11111","00001","00010","00100","01000","01000","01000"],
    '8': ["01110","10001","10001","01110","10001","10001","01110"],
    '9': ["01110","10001","10001","01111","00001","00001","01110"],
    '.': ["00000","00000","00000","00000","00000","00110","00110"],
    ',': ["00000","00000","00000","00000","00110","00110","00100"],
    '-': ["00000","00000","00000","11111","00000","00000","00000"],
    ':': ["00000","00110","00110","00000","00110","00110","00000"],
    '/': ["00001","00010","00010","00100","01000","01000","10000"],
    '%': ["11001","11010","00100","01000","10110","00110","00000"],
    '$': ["00100","01111","10100","01110","00101","11110","00100"],
    '!': ["00100","00100","00100","00100","00100","00000","00100"],
    '?': ["01110","10001","00001","00110","00100","00000","00100"],
    ' ': ["00000","00000","00000","00000","00000","00000","00000"],
}

def draw_text(px, x, y, text, color, scale=3, spacing=1):
    cx = x
    for ch in text.upper():
        glyph = FONT.get(ch, FONT['?'])
        for ry, rowbits in enumerate(glyph):
            for rx, bit in enumerate(rowbits):
                if bit == '1':
                    fill_rect(px, cx + rx * scale, y + ry * scale,
                              cx + rx * scale + scale, y + ry * scale + scale, color)
        cx += (5 + spacing) * scale

def text_width(text, scale=3, spacing=1):
    return len(text) * (5 + spacing) * scale

# ---------------------------------------------------------------- panels
BG      = (15, 17, 26)
PANEL   = (28, 32, 48)
ACCENT  = (0, 200, 255)
RED     = (255, 80, 80)
GREEN   = (80, 220, 120)
YELLOW  = (255, 210, 80)
WHITE   = (240, 244, 250)
GREY    = (140, 150, 170)

def panel_icon(px, cx, cy, kind, color):
    """Draw a simple geometric icon centered at cx,cy."""
    if kind == 'globe':      # APEC / diplomacy
        draw_circle(px, cx, cy, 34, color)
        fill_rect(px, cx - 34, cy - 2, cx + 34, cy + 2, BG)
        fill_rect(px, cx - 2, cy - 34, cx + 2, cy + 34, BG)
    elif kind == 'summit':   # Trump-Putin-Xi: three figures
        for dx in (-30, 0, 30):
            draw_circle(px, cx + dx, cy - 12, 11, color)
            fill_rect(px, cx + dx - 13, cy + 2, cx + dx + 13, cy + 30, color)
    elif kind == 'missile':  # Iran-US exchange
        fill_rect(px, cx - 40, cy - 4, cx + 10, cy + 4, color)
        fill_rect(px, cx + 10, cy - 8, cx + 20, cy + 8, color)
        fill_rect(px, cx - 46, cy - 2, cx - 40, cy + 2, RED)
    elif kind == 'child':    # Yemen
        draw_circle(px, cx, cy - 18, 14, color)
        fill_rect(px, cx - 12, cy + 0, cx + 12, cy + 28, color)
    elif kind == 'plane':    # Russia crash
        fill_rect(px, cx - 40, cy - 3, cx + 30, cy + 3, color)
        fill_rect(px, cx - 6, cy - 22, cx + 6, cy + 22, color)
        fill_rect(px, cx + 18, cy - 12, cx + 30, cy + 12, color)
    elif kind == 'germ':     # WHO superbug
        draw_circle(px, cx, cy, 26, color)
        for ang in range(0, 360, 60):
            import math
            dx = int(30 * math.cos(math.radians(ang)))
            dy = int(30 * math.sin(math.radians(ang)))
            draw_circle(px, cx + dx, cy + dy, 5, color)
    elif kind == 'chip':     # Nvidia
        fill_rect(px, cx - 30, cy - 30, cx + 30, cy + 30, color)
        fill_rect(px, cx - 18, cy - 18, cx + 18, cy + 18, BG)
        for d in range(-2, 3):
            fill_rect(px, cx + d * 12 - 2, cy - 38, cx + d * 12 + 2, cy - 30, color)
            fill_rect(px, cx + d * 12 - 2, cy + 30, cx + d * 12 + 2, cy + 38, color)
    elif kind == 'aid':      # Afghanistan aid
        fill_rect(px, cx - 34, cy - 22, cx + 34, cy + 22, color)
        fill_rect(px, cx - 6, cy - 22, cx + 6, cy + 22, BG)
        fill_rect(px, cx - 34, cy - 6, cx + 34, cy + 6, BG)

def draw_panel(px, x0, y0, x1, y1, icon, color, headline, sub):
    fill_rect(px, x0, y0, x1, y1, PANEL)
    draw_rect_outline(px, x0, y0, x1, y1, (60, 70, 100), t=2)
    cx = x0 + 48
    cy = y0 + 48
    panel_icon(px, cx, cy, icon, color)
    # headline (wrap manually to fit width)
    tx = x0 + 100
    ty = y0 + 22
    maxw = x1 - tx - 14
    words = headline.split()
    line = ""
    lines = []
    for w in words:
        test = (line + " " + w).strip()
        if text_width(test, scale=3) <= maxw:
            line = test
        else:
            if line:
                lines.append(line)
            line = w
    if line:
        lines.append(line)
    for ln in lines[:3]:
        draw_text(px, tx, ty, ln, WHITE, scale=3)
        ty += 26
    if sub:
        # wrap sub-label to panel width (scale 2)
        sw = sub.split()
        sline = ""
        slines = []
        for w in sw:
            test = (sline + " " + w).strip()
            if text_width(test, scale=2) <= maxw:
                sline = test
            else:
                if sline:
                    slines.append(sline)
                sline = w
        if sline:
            slines.append(sline)
        sy = ty + 6
        for sl in slines[:2]:
            draw_text(px, tx, sy, sl, color, scale=2)
            sy += 18

def main():
    px = new_canvas(BG)

    # top banner: date + title
    fill_rect(px, 0, 0, W, 120, (10, 12, 20))
    draw_rect_outline(px, 0, 0, W, 120, ACCENT, t=3)
    draw_text(px, 40, 22, "18 NOVEMBER 2026", ACCENT, scale=5)
    draw_text(px, 40, 72, "WORLD NEWS IN ONE IMAGE", WHITE, scale=3)

    # 2 columns x 4 rows of panels
    gx, gy = 20, 16
    pw = (W - 3 * gx) // 2
    ph = 190
    panels = [
        ('globe',   ACCENT, 'APEC SUMMIT SHENZHEN',      'Putin arrives, Xi free trade'),
        ('summit',  YELLOW, 'TRUMP TRILATERAL SUMMIT',   'Trump, Putin, Xi in China'),
        ('missile', RED,    'US IRAN EXCHANGE FIRE',     'US strikes missile site, Iran radar'),
        ('child',   GREEN,  'YEMEN WAR CHILDREN',        '64 killed, 800k cut off Taiz'),
        ('plane',   GREY,   'RUSSIA AN-12 CRASH',        '17 dead in Siberia'),
        ('germ',    RED,    'WHO SUPERBUG ALERT',        'Klebsiella resistance up 72%'),
        ('chip',    GREEN,  'NVIDIA POST-HUANG',         'Strong results, CEO scandal'),
        ('aid',     YELLOW, 'AFGHANISTAN AID',           '$18M UN funding, 824k people'),
    ]
    for i, (icon, color, head, sub) in enumerate(panels):
        col = i % 2
        row = i // 2
        x0 = gx + col * (pw + gx)
        y0 = 120 + gy + row * (ph + gy)
        draw_panel(px, x0, y0, x0 + pw, y0 + ph, icon, color, head, sub)

    write_png('entry.png', px)
    print('entry.png written:', W, 'x', H)

if __name__ == '__main__':
    main()
