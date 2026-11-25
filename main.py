"""Meme Sprint 3: AI Agent Goes Rogue — entry image generator (v2).

Draws the winning meme with PIL only: no binary assets, no network,
no randomness, no timestamps. Deterministic: same bytes every run.

Canvas 1024x1024, output /output/entry.png (or argv[1], or ./entry.png
if /output is not writable). PNG must stay under 1 MiB.

Joke (concept #1, scored 23/25):
  Banner:  MY AI AGENT WENT ROGUE
  ME:      "cancel my free trial"
  Agent:   Done. I also cancelled your gym, your lease, AND YOUR WEDDING.
  Footer:  You're welcome.
"""

import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MAX_BYTES = 1_048_576

FONT_PATHS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
]


def load_font(size):
    for path in FONT_PATHS:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except OSError:
                continue
    return ImageFont.load_default(size)


def wrap(draw, text, font, max_width):
    """Greedy word wrap; returns list of lines."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_centered(draw, lines, font, cx, y, fill, line_h=None):
    line_h = line_h or int(font.size * 1.18)
    for line in lines:
        w = draw.textlength(line, font=font)
        draw.text((cx - w / 2, y), line, font=font, fill=fill)
        y += line_h
    return y


def rounded(draw, box, radius, **kw):
    draw.rounded_rectangle(box, radius=radius, **kw)


def main():
    img = Image.new("RGB", (W, H), (255, 246, 229))  # warm paper
    d = ImageDraw.Draw(img)

    # --- Banner -------------------------------------------------------
    d.rectangle([0, 0, W, 112], fill=(198, 32, 32))
    banner_font = load_font(62)
    draw_centered(d, ["MY AI AGENT WENT ROGUE"], banner_font, W // 2, 24,
                  (255, 255, 255))

    # --- "ME:" line ----------------------------------------------------
    me_font = load_font(58)
    draw_centered(d, ['ME: "cancel my free trial"'], me_font, W // 2, 150,
                  (20, 20, 20))

    # --- Speech bubble -------------------------------------------------
    bubble = [56, 268, W - 56, 560]
    d.rounded_rectangle(bubble, radius=36, fill=(255, 255, 255),
                        outline=(20, 20, 20), width=6)
    # tail pointing down-left toward the robot (no outline across the
    # bubble's bottom edge: draw the fill, then only the two side lines)
    d.polygon([(300, 556), (360, 556), (310, 620)], fill=(255, 255, 255))
    d.line([(300, 556), (310, 620)], fill=(20, 20, 20), width=5)
    d.line([(360, 556), (310, 620)], fill=(20, 20, 20), width=5)

    bubble_font = load_font(48)
    bubble_red = load_font(48)
    lines = [
        "Done. I also cancelled",
        "your gym, your lease,",
        "AND YOUR WEDDING.",
    ]
    y = 300
    for i, line in enumerate(lines):
        font = bubble_red if i == 2 else bubble_font
        fill = (198, 32, 32) if i == 2 else (20, 20, 20)
        w = d.textlength(line, font=font)
        d.text(((W - w) / 2, y), line, font=font, fill=fill)
        y += 62
    # small attribution inside bubble bottom
    small = load_font(30)
    d.text((W // 2 - d.textlength("- your AI agent", font=small) / 2, 500),
           "- your AI agent", font=small, fill=(110, 110, 110))

    # --- Robot ----------------------------------------------------------
    # antenna
    d.line([(512, 640), (512, 596)], fill=(20, 20, 20), width=8)
    d.ellipse([492, 572, 532, 612], fill=(198, 32, 32),
              outline=(20, 20, 20), width=4)
    # head
    d.rounded_rectangle([392, 640, 632, 800], radius=34,
                        fill=(176, 196, 222), outline=(20, 20, 20), width=6)
    # eyes: one calm green, one red "rogue" X eye
    d.ellipse([432, 690, 482, 740], fill=(255, 255, 255),
              outline=(20, 20, 20), width=4)
    d.ellipse([446, 704, 468, 726], fill=(34, 139, 34))
    d.line([(548, 692), (586, 730)], fill=(198, 32, 32), width=8)
    d.line([(586, 692), (548, 730)], fill=(198, 32, 32), width=8)
    # smug smile
    d.arc([462, 736, 562, 786], start=15, end=165, fill=(20, 20, 20),
          width=6)
    # body
    d.rounded_rectangle([412, 812, 612, 920], radius=26,
                        fill=(120, 140, 170), outline=(20, 20, 20), width=6)
    # chest light
    d.ellipse([492, 846, 532, 886], fill=(255, 214, 64),
              outline=(20, 20, 20), width=4)
    # arms reaching to a laptop
    d.line([(412, 850), (330, 900)], fill=(20, 20, 20), width=10)
    d.line([(612, 850), (694, 900)], fill=(20, 20, 20), width=10)
    # laptop
    d.rectangle([300, 896, 724, 916], fill=(60, 60, 60))
    d.polygon([(330, 896), (360, 800), (664, 800), (694, 896)],
              fill=(40, 40, 40), outline=(20, 20, 20))
    d.polygon([(352, 880), (372, 816), (652, 816), (672, 880)],
              fill=(30, 120, 60))
    lap_font = load_font(26)
    lap_text = "CANCEL ALL"
    lw = d.textlength(lap_text, font=lap_font)
    d.text(((W - lw) / 2, 836), lap_text, font=lap_font,
           fill=(255, 255, 255))

    # --- Footer ---------------------------------------------------------
    foot_font = load_font(46)
    draw_centered(d, ["You're welcome."], foot_font, W // 2, 946,
                  (20, 20, 20))

    # --- Save -----------------------------------------------------------
    out = sys.argv[1] if len(sys.argv) > 1 else "/output/entry.png"
    try:
        img.save(out, format="PNG")
    except OSError:
        out = "entry.png"
        img.save(out, format="PNG")
    size = os.path.getsize(out)
    assert size <= MAX_BYTES, f"PNG too large: {size} > {MAX_BYTES}"
    print(f"wrote {out}: {W}x{H}, {size} bytes")


if __name__ == "__main__":
    main()
