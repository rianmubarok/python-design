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
JPG_DIR.mkdir(parents=True, exist_ok=True)
SVG_DIR.mkdir(parents=True, exist_ok=True)


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
    plt.close(fig)
    print(f"Saved: {jpg_path} | {svg_path}")


def ghost_layer(ax, cx, cy, s, alpha=1.0, fill="white"):
    """Ghost silhouette at given alpha — for overlap layering effect."""
    head_r = s * 0.34
    body_h = s * 0.48
    body_w = s * 0.66
    body_cy = cy + s * 0.04

    # body ellipse
    ax.add_patch(Ellipse((cx, body_cy), body_w, body_h,
                         facecolor=fill, edgecolor="none", alpha=alpha))
    # dome
    theta = np.linspace(0, np.pi, 60)
    dome_pts = np.column_stack([
        cx + head_r * np.cos(theta),
        body_cy + body_h * 0.26 + head_r * np.sin(theta)
    ])
    dome_pts = np.vstack([[cx - head_r, body_cy + body_h * 0.26],
                           dome_pts,
                           [cx + head_r, body_cy + body_h * 0.26]])
    ax.add_patch(Polygon(dome_pts, closed=True, facecolor=fill,
                         edgecolor="none", alpha=alpha))
    # wavy skirt
    bottom_y = body_cy - body_h * 0.44
    n_bumps = 4
    half_w = body_w * 0.5
    xs = np.linspace(cx - half_w, cx + half_w, 200)
    wave_amp = s * 0.09
    wave_y = bottom_y - wave_amp * 0.5 - wave_amp * np.sin(
        (xs - cx + half_w) / body_w * n_bumps * np.pi)
    skirt_pts = [(cx - half_w, bottom_y)]
    skirt_pts += list(zip(xs, wave_y))
    skirt_pts += [(cx + half_w, bottom_y)]
    ax.add_patch(Polygon(skirt_pts, closed=True, facecolor=fill,
                         edgecolor="none", alpha=alpha))
    # eyes
    for ex in (-s * 0.13, s * 0.13):
        ax.add_patch(Ellipse((cx + ex, body_cy + s * 0.24), s * 0.10, s * 0.13,
                             facecolor="black", edgecolor="none", alpha=min(alpha * 1.5, 1.0)))
    ax.add_patch(Circle((cx, body_cy + s * 0.09), s * 0.07,
                        facecolor="black", edgecolor="none", alpha=min(alpha * 1.5, 1.0)))


def draw():
    """Large sparse ghost field — 3×4 primary ghosts, each surrounded by 2 smaller
    ghost echoes at reduced alpha, creating a layered ethereal overlap effect."""
    fig, ax = setup_ax()
    rng = np.random.default_rng(17)
    cols, rows = 3, 4
    dx, dy = PERIOD / cols, PERIOD / rows
    primary_s = min(dx, dy) * 0.82

    for row in range(rows):
        for col in range(cols):
            cx = (col + 0.5) * dx
            cy = (row + 0.5) * dy
            for ox, oy in WRAPS:
                # two ghost echoes behind
                for i in range(2):
                    offset_x = rng.uniform(-dx * 0.28, dx * 0.28)
                    offset_y = rng.uniform(-dy * 0.22, dy * 0.22)
                    echo_s = primary_s * rng.uniform(0.55, 0.78)
                    ghost_layer(ax, cx + ox + offset_x, cy + oy + offset_y,
                                echo_s, alpha=0.28, fill="white")
                # primary ghost
                ghost_layer(ax, cx + ox, cy + oy, primary_s, alpha=0.92)
    save(fig, "abstract halloween variation ghost large sparse overlapping layered pattern black white texture")


if __name__ == "__main__":
    draw()
