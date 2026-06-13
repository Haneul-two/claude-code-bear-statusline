"""Build assets/demo-react.gif: BEAR_MOOD=react in action — as session/weekly
usage climbs, the bear's mood follows it (excited -> calm -> gloomy -> teary -> grumpy).
Reuses fonts/helpers from make_demo_gif.
"""
import os
from PIL import Image, ImageDraw
from make_demo_gif import (
    mono, sym, emoji, draw_at, BG, PAD, LINE_H, COL_X, W, H, HERE,
    GREEN, YELLOW, RED, CYAN, DIM, DEFAULT, MOODS,
)

def pct_color(p):
    return RED if p >= 90 else YELLOW if p >= 70 else GREEN

# (session%, weekly%, cost, mood_index) — mood follows the react band of max(session, weekly)
SEQ = [
    (8, 12, 0.20, 0),    # excited
    (20, 30, 0.75, 1),   # happy
    (35, 48, 1.60, 3),   # calm
    (50, 64, 2.40, 4),   # sleepy
    (60, 78, 3.30, 7),   # gloomy
    (70, 86, 4.10, 5),   # surprised
    (80, 93, 5.00, 8),   # teary
    (88, 98, 5.80, 9),   # grumpy
]

def render(sess, week, cost, mi):
    eyes, mcolor = MOODS[mi]
    color = mcolor if mcolor else DEFAULT
    img = Image.new("RGBA", (W, H), BG + (255,))
    d = ImageDraw.Draw(img)
    ears = " ∩" + ("─" * (len(eyes) + 2)) + "∩"
    face = f"ʕ  {eyes}  ʔ"
    body = " (  u u  )"
    y0, y1, y2 = PAD, PAD + LINE_H, PAD + LINE_H * 2
    draw_at(d, PAD, y0, [(ears, sym, color, False)])
    draw_at(d, PAD, y1, [(face, sym, color, False)])
    draw_at(d, PAD, y2, [(body, sym, color, False)])
    cx = int(COL_X)
    draw_at(d, cx, y0, [("[Fable 5]", mono, CYAN, False), (" | ", mono, DEFAULT, False),
                        ("\U0001F4B0", emoji, None, True), (f" ${cost:.2f}", mono, DEFAULT, False)])
    draw_at(d, cx, y1, [("⏳", emoji, None, True), (" session ", mono, DEFAULT, False),
                        (f"{sess}%", mono, pct_color(sess), False), ("  (resets 10:55)", mono, DIM, False)])
    draw_at(d, cx, y2, [("\U0001F4C5", emoji, None, True), (" weekly ", mono, DEFAULT, False),
                        (f"{week}%", mono, pct_color(week), False), ("  (resets Thu 6/18)", mono, DIM, False)])
    return img.convert("RGB")

frames = [render(*f) for f in SEQ]
# slower than the random demo so the progression reads; hold first & last longer
durations = [1700] + [950] * (len(frames) - 2) + [2200]
out = os.path.join(HERE, "assets", "demo-react.gif")
frames[0].save(out, save_all=True, append_images=frames[1:],
               duration=durations, loop=0, optimize=True)
print("wrote", out, "frames:", len(frames))
