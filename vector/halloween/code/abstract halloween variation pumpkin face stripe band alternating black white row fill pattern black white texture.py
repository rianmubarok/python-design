import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, FancyBboxPatch, Polygon, Rectangle
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
    ax.set_facecolor("white")
    ax.set_xlim(0, PERIOD)
    ax.set_ylim(0, PERIOD)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def save(fig, name):
    jpg_path = JPG_DIR / f"{name} {DATE}.jpg"
    svg_path = SVG_DIR / f"{name} {DATE}.svg"
    fig.savefig(jpg_path, dpi=DPI, pad_inches=0, facecolor="white")
    fig.savefig(svg_path, format="svg", pad_inches=0, facecolor="white")
    plt.close(fig)
    print(f"Saved: {jpg_path} | {svg_path}")


def draw_pumpkin(ax, cx, cy, s, body_fill, face_fill):
    """Pumpkin body with three lobes and jack-o'-lantern face cutouts."""
    for lobe_ox in (-s * 0.22, 0, s * 0.22):
        ax.add_patch(Ellipse((cx + lobe_ox, cy), s * 0.56, s * 0.74,
                             facecolor=body_fill, edgecolor="none", zorder=2))

    # Stem
    ax.add_patch(FancyBboxPatch(
        (cx - s * 0.055, cy + s * 0.35), s * 0.11, s * 0.17,
        boxstyle=f"round,pad=0,rounding_size={s * 0.03:.4f}",
        facecolor=body_fill, edgecolor="none", zorder=2))

    # Triangle eyes
    eye_l = np.array([[cx - s * 0.24, cy + s * 0.14],
                      [cx - s * 0.35, cy - s * 0.04],
                      [cx - s * 0.13, cy - s * 0.04]])
    eye_r = eye_l.copy()
    eye_r[:, 0] = cx + (eye_l[:, 0] - cx) * -1
    for eye in [eye_l, eye_r]:
        ax.add_patch(Polygon(eye, closed=True, facecolor=face_fill,
                             edgecolor="none", zorder=3))

    # Jagged mouth
    teeth_x = np.linspace(cx - s * 0.28, cx + s * 0.28, 7)
    mouth_pts = [(teeth_x[0], cy - s * 0.10)]
    for k, x in enumerate(teeth_x):
        mouth_pts.append((x, cy - s * 0.24 if k % 2 == 0 else cy - s * 0.10))
    mouth_pts.append((teeth_x[-1], cy - s * 0.10))
    ax.add_patch(Polygon(mouth_pts, closed=True, facecolor=face_fill,
                         edgecolor="none", zorder=3))


def draw():
    """Alternating horizontal stripe rows:
       Even rows  → black background, white pumpkins with black face cutouts.
       Odd rows   → white background, black pumpkins with white face cutouts.
       Pumpkins are staggered (brick offset) between rows. Fully seamless."""
    fig, ax = setup_ax()

    rows = 6
    cols = 5
    dy = PERIOD / rows
    dx = PERIOD / cols
    s = dy * 0.48

    for row in range(rows):
        bg = "black" if row % 2 == 0 else "white"
        body = "white" if bg == "black" else "black"
        face = "black" if body == "white" else "white"

        # Draw stripe (seamless)
        for ox, oy in WRAPS:
            ax.add_patch(Rectangle(
                (0 + ox, row * dy + oy), PERIOD, dy,
                facecolor=bg, edgecolor="none", zorder=0))

        shift = (dx * 0.5) if row % 2 else 0.0
        cy = (row + 0.5) * dy

        for col in range(-1, cols + 2):
            cx = col * dx + shift + dx * 0.5
            for ox, oy in WRAPS:
                px, py = cx + ox, cy + oy
                if -15 <= px <= PERIOD + 15 and -10 <= py <= PERIOD + 10:
                    draw_pumpkin(ax, px, py, s, body_fill=body, face_fill=face)

    save(fig, "abstract halloween variation pumpkin face stripe band alternating black white row fill pattern black white texture")


if __name__ == "__main__":
    draw()
