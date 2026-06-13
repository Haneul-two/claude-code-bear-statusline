"""Side-by-side comparison GIF: same climbing usage, BEAR_MOOD=random (left,
bear ignores it) vs BEAR_MOOD=react (right, bear reacts).

  assets/demo-compare-x-16x9.gif   1280x720  (X / Twitter)
  assets/demo-compare-reddit.gif   1200x900  (Reddit, landscape 4:3)
"""
import os
from PIL import Image, ImageDraw
from make_demo_gif import mono, BG, HERE, DIM, CYAN, DEFAULT
import make_react_gif

PANEL_W, PANEL_H = make_react_gif.W, make_react_gif.H  # native panel size (940x174)

# shared usage progression (strip the mood index from the react SEQ)
SHARED = [(s, w, c) for (s, w, c, _mi) in make_react_gif.SEQ]
REACT_MI = [mi for (_s, _w, _c, mi) in make_react_gif.SEQ]
# a deliberately "random-looking" mood order for the left panel: never matches the
# react mood, and stays cheerful at high usage to show it ignores the limit
RANDOM_MI = [5, 2, 8, 0, 1, 9, 3, 1]

cap = ImageFont = None
cap_font = mono.font_variant(size=24)


def panel(sess, week, cost, mi):
    return make_react_gif.render(sess, week, cost, mi)  # 940x174 RGB


def caption(draw, cx, y, text, color):
    b = draw.textbbox((0, 0), text, font=cap_font)
    draw.text((cx - (b[2] - b[0]) / 2, y), text, font=cap_font, fill=color)


def build(name, W, H, target_w, gap):
    scaled_h = round(PANEL_H * target_w / PANEL_W)
    cap_h = 30
    group_h = cap_h + 14 + scaled_h
    top = (H - group_h) // 2
    panel_y = top + cap_h + 14
    total_w = 2 * target_w + gap
    left_x = (W - total_w) // 2
    right_x = left_x + target_w + gap
    lcx = left_x + target_w // 2
    rcx = right_x + target_w // 2

    frames = []
    for i, (s, w, c) in enumerate(SHARED):
        left = panel(s, w, c, RANDOM_MI[i % len(RANDOM_MI)]).resize((target_w, scaled_h), Image.LANCZOS)
        right = panel(s, w, c, REACT_MI[i]).resize((target_w, scaled_h), Image.LANCZOS)
        canvas = Image.new("RGB", (W, H), BG)
        canvas.paste(left, (left_x, panel_y))
        canvas.paste(right, (right_x, panel_y))
        d = ImageDraw.Draw(canvas)
        # divider
        dx = (left_x + target_w + right_x) // 2
        d.line([(dx, panel_y - 6), (dx, panel_y + scaled_h + 6)], fill=DIM, width=2)
        caption(d, lcx, top, "BEAR_MOOD=random", DIM)
        caption(d, rcx, top, "BEAR_MOOD=react", CYAN)
        frames.append(canvas)

    out = os.path.join(HERE, "assets", name)
    frames[0].save(out, save_all=True, append_images=frames[1:],
                   duration=make_react_gif.DURATIONS, loop=0, optimize=True)
    print("wrote", out, f"{W}x{H}", "frames:", len(frames))


build("demo-compare-x-16x9.gif", 1280, 720, 560, 60)
build("demo-compare-reddit.gif", 1200, 900, 540, 56)
