"""Build social-media-sized variants of the demo GIF by compositing the
statusline (from make_demo_gif.render) centered on a larger canvas.

  assets/demo-x-16x9.gif   1280x720  (X / Twitter recommended 16:9)
  assets/demo-reddit.gif   1080x1080 (Reddit feed thumbnail, square)
"""
import os
from PIL import Image
from make_demo_gif import render, MOODS, BG, HERE

VARIANTS = [
    # (out_name, canvas_w, canvas_h, content_target_w)
    ("demo-x-16x9.gif", 1280, 720, 1160),
    ("demo-reddit.gif", 1080, 1080, 1000),
]

# render content frames once (each ~940x174 RGB)
content = [render(eyes, color) for eyes, color in MOODS]

for name, W, H, target_w in VARIANTS:
    frames = []
    for c in content:
        scale = target_w / c.width
        scaled = c.resize((target_w, max(1, round(c.height * scale))), Image.LANCZOS)
        canvas = Image.new("RGB", (W, H), BG)
        canvas.paste(scaled, ((W - scaled.width) // 2, (H - scaled.height) // 2))
        frames.append(canvas)
    out = os.path.join(HERE, "assets", name)
    frames[0].save(out, save_all=True, append_images=frames[1:],
                   duration=750, loop=0, optimize=True)
    print("wrote", out, f"{W}x{H}", "frames:", len(frames))
