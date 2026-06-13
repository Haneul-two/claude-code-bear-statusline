"""Generate assets/demo.gif: the bear cycling through all 10 moods.
Local asset-generation tool (not a project dependency). Requires Pillow + Windows fonts.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_GIF = os.path.join(HERE, "assets", "demo.gif")
OUT_PNG = os.path.join(HERE, "assets", "_frame0.png")

# ── colors (terminal-ish on GitHub dark bg)
BG = (13, 17, 23)
GREEN = (63, 185, 80)
YELLOW = (210, 168, 75)
RED = (248, 81, 73)
CYAN = (86, 182, 194)
MAGENTA = (198, 120, 221)
DIM = (110, 118, 129)
DEFAULT = (201, 209, 217)

MOODS = [
    ("◕ᴥ◕", GREEN),    ("≧ᴥ≦", GREEN),   ("-ᴥ◕", MAGENTA),
    ("•ᴥ•", DEFAULT),  ("-ᴥ-", DIM),      ("◉ᴥ◉", YELLOW),
    ("@ᴥ@", YELLOW),   ("´•ᴥ•`", YELLOW), (";ᴥ;", CYAN),
    ("òᴥó", RED),
]

FS = 30
mono = ImageFont.truetype(r"C:\Windows\Fonts\consola.ttf", FS)
sym = ImageFont.truetype(r"C:\Windows\Fonts\cambria.ttc", FS)  # full kaomoji glyph coverage
emoji = ImageFont.truetype(r"C:\Windows\Fonts\seguiemj.ttf", FS)

PAD = 24
LINE_H = FS + 12
COL_X = PAD + 200  # info column start
W = 940
H = PAD * 2 + LINE_H * 3

def seg_w(draw, text, font):
    b = draw.textbbox((0, 0), text, font=font)
    return b[2] - b[0]

def draw_line(draw, y, segs):
    """segs: list of (text, font, color, embedded_color_bool); drawn left->right."""
    x = PAD
    for text, font, color, emb in segs:
        if emb:
            draw.text((x, y), text, font=font, embedded_color=True)
        else:
            draw.text((x, y), text, font=font, fill=color)
        x += seg_w(draw, text, font)

def draw_at(draw, x, y, segs):
    for text, font, color, emb in segs:
        if emb:
            draw.text((x, y), text, font=font, embedded_color=True)
        else:
            draw.text((x, y), text, font=font, fill=color)
        x += seg_w(draw, text, font)

def render(eyes, color):
    img = Image.new("RGBA", (W, H), BG + (255,))
    d = ImageDraw.Draw(img)
    ears = " ∩" + ("─" * (len(eyes) + 2)) + "∩"
    face = f"ʕ  {eyes}  ʔ"
    body = " (  u u  )"
    y0, y1, y2 = PAD, PAD + LINE_H, PAD + LINE_H * 2
    # bear column (use symbol font so all face glyphs render)
    draw_at(d, PAD, y0, [(ears, sym, color, False)])
    draw_at(d, PAD, y1, [(face, sym, color, False)])
    draw_at(d, PAD, y2, [(body, sym, color, False)])
    # info column
    cx = int(COL_X)
    draw_at(d, cx, y0, [("[Fable 5]", mono, CYAN, False), (" | ", mono, DEFAULT, False),
                        ("\U0001F4B0", emoji, None, True), (" $1.23", mono, DEFAULT, False)])
    draw_at(d, cx, y1, [("⏳", emoji, None, True), (" session ", mono, DEFAULT, False),
                        ("24%", mono, GREEN, False), ("  (resets 10:55)", mono, DIM, False)])
    draw_at(d, cx, y2, [("\U0001F4C5", emoji, None, True), (" weekly ", mono, DEFAULT, False),
                        ("81%", mono, YELLOW, False), ("  (resets Thu 6/18)", mono, DIM, False)])
    return img.convert("RGB")

def build_default():
    frames = [render(eyes, color) for eyes, color in MOODS]
    frames[0].save(OUT_GIF, save_all=True, append_images=frames[1:],
                   duration=750, loop=0, optimize=True)
    print("wrote", OUT_GIF, "frames:", len(frames))


if __name__ == "__main__":
    build_default()
