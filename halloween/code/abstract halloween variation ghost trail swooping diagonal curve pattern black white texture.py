import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, Polygon
from pathlib import Path
from datetime import datetime

SIZE = 4000
DPI = 300
PERIOD = 100.0
DATE = datetime.now().strftime("%d%m%Y")
WRAPS = [(i * PERIOD, j * PERIOD) for i in (-1, 0, 1) for j in (-1, 0, 1)]

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR.parent / "output"
JPG_DIR = OUTPUT_DIR / "jpg"
SVG_DIR = OUTPUT_DIR / "svg"
EPS_DIR = OUTPUT_DIR / \"eps\"
JPG_DIR.mkdir(parents=True, exist_ok=True)
SVG_DIR.mkdir(parents=True, exist_ok=True)
EPS_DIR.mkdir(parents=True, exist_ok=True)


def setup_ax():
    fig, ax = plt.subplots(figsize=(SIZE / DPI, SIZE / DPI), dpi=DPI)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.set_facecolor("black")
    ax.set_xlim(0, PERIOD)
    ax.set_ylim(0, PERIOD)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def save(fig, name):
    jpg_path = JPG_DIR / f"{name} {DATE}.jpg"
    svg_path = SVG_DIR / f"{name} {DATE}.svg"
    fig.savefig(jpg_path, dpi=DPI, pad_inches=0, facecolor="black")
    fig.savefig(svg_path, format="svg", pad_inches=0, facecolor="black")
    eps_path = EPS_DIR / f\"{name} {DATE}.eps\"
    orig_size = fig.get_size_inches()
    fig.set_size_inches(30, 30)
    fig.savefig(eps_path, format=\"eps\", pad_inches=0, facecolor=\"white\", dpi=DPI)
    fig.set_size_inches(orig_size[0], orig_size[1])
    plt.close(fig)
    print(f"Saved: {jpg_path} | {svg_path} | {eps_path}")


def ghost(ax, cx, cy, s, alpha=1.0):
    head_r = s*0.34; body_h = s*0.48; body_w = s*0.66; body_cy = cy+s*0.04
    ax.add_patch(Ellipse((cx, body_cy), body_w, body_h,
                         facecolor="white", edgecolor="none", alpha=alpha))
    theta = np.linspace(0, np.pi, 60)
    dome = np.column_stack([cx+head_r*np.cos(theta), body_cy+body_h*0.26+head_r*np.sin(theta)])
    dome = np.vstack([[cx-head_r, body_cy+body_h*0.26], dome, [cx+head_r, body_cy+body_h*0.26]])
    ax.add_patch(Polygon(dome, closed=True, facecolor="white", edgecolor="none", alpha=alpha))
    xs = np.linspace(cx-body_w*0.5, cx+body_w*0.5, 200)
    bot_y = body_cy-body_h*0.44
    wave_y = bot_y-s*0.05-s*0.09*np.sin((xs-cx+body_w*0.5)/body_w*4*np.pi)
    skirt = [(cx-body_w*0.5, bot_y)]+list(zip(xs,wave_y))+[(cx+body_w*0.5, bot_y)]
    ax.add_patch(Polygon(skirt, closed=True, facecolor="white", edgecolor="none", alpha=alpha))
    for ex in (-s*0.13, s*0.13):
        ax.add_patch(Ellipse((cx+ex, body_cy+s*0.24), s*0.10, s*0.13,
                             facecolor="black", edgecolor="none", alpha=min(alpha*1.5,1)))
    ax.add_patch(Circle((cx, body_cy+s*0.09), s*0.07,
                        facecolor="black", edgecolor="none", alpha=min(alpha*1.5,1)))


def draw():
    """Ghosts arranged along sinusoidal diagonal trails — shrinking as trail fades."""
    fig, ax = setup_ax()
    n_trails = 5
    ghosts_per_trail = 7
    trail_spacing = PERIOD / n_trails

    for t in range(n_trails):
        trail_offset = t * trail_spacing
        for g in range(ghosts_per_trail):
            frac = g / (ghosts_per_trail - 1)
            # sinusoidal diagonal path
            u = frac * PERIOD * 1.1 - PERIOD * 0.05
            v = trail_offset + 8.0 * np.sin(u * 0.18) + frac * 6.0
            # rotate to diagonal
            angle = np.radians(30)
            cx = u * np.cos(angle) - v * np.sin(angle)
            cy = u * np.sin(angle) + v * np.cos(angle)
            cx = cx % PERIOD
            cy = cy % PERIOD
            s = 5.0 + 5.0 * (1-frac)          # shrink toward tail
            alpha = 0.35 + 0.65 * (1-frac)    # fade toward tail
            for ox, oy in WRAPS:
                ghost(ax, cx+ox, cy+oy, s, alpha)
    save(fig, "abstract halloween variation ghost trail swooping diagonal curve pattern black white texture")


if __name__ == "__main__":
    draw()
