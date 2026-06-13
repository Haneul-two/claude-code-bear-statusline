"""Build social-media-sized variants by compositing the statusline
(from make_demo_gif / make_react_gif) centered on a larger canvas.

  assets/demo-x-16x9.gif         1280x720  (X / Twitter 16:9, random moods)
  assets/demo-reddit.gif         1080x1080 (Reddit feed thumbnail, square)
  assets/demo-react-x-16x9.gif   1280x720  (X / Twitter 16:9, react mode)
"""
import os
from PIL import Image
from make_demo_gif import render as render_random, MOODS, BG, HERE
import make_react_gif


def composite(content_frames, W, H, target_w):
    out = []
    for c in content_frames:
        scale = target_w / c.width
        scaled = c.resize((target_w, max(1, round(c.height * scale))), Image.LANCZOS)
        canvas = Image.new("RGB", (W, H), BG)
        canvas.paste(scaled, ((W - scaled.width) // 2, (H - scaled.height) // 2))
        out.append(canvas)
    return out


def save_gif(frames, name, duration):
    out = os.path.join(HERE, "assets", name)
    frames[0].save(out, save_all=True, append_images=frames[1:],
                   duration=duration, loop=0, optimize=True)
    print("wrote", out, f"{frames[0].width}x{frames[0].height}", "frames:", len(frames))


# ── random-mood demo variants
random_content = [render_random(eyes, color) for eyes, color in MOODS]
save_gif(composite(random_content, 1280, 720, 1160), "demo-x-16x9.gif", 750)
save_gif(composite(random_content, 1080, 1080, 1000), "demo-reddit.gif", 750)

# ── react-mode demo, 16:9 (keeps its custom per-frame durations)
react_content = [make_react_gif.render(*f) for f in make_react_gif.SEQ]
save_gif(composite(react_content, 1280, 720, 1160), "demo-react-x-16x9.gif", make_react_gif.DURATIONS)
