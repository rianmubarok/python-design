import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, FancyBboxPatch, Polygon
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


def pumpkin(ax, cx, cy, s, fill="black", inv="white"):
    """Jack-o-lantern: pumpkin body + stem + triangular eyes + jagged mouth."""
    # pumpkin body — three overlapping ellipses
    for ox in (-s * 0.25, 0, s * 0.25):
        ax.add_patch(Ellipse((cx + ox, cy), s * 0.62, s * 0.80,
                             facecolor=fill, edgecolor="none"))
    # ribbing lines (vertical creases)
    for ox in (-s * 0.25, 0, s * 0.25):
        ax.plot([cx + ox, cx + ox], [cy - s * 0.39, cy + s * 0.39],
                color=inv, linewidth=0.7, solid_capstyle="round")
    # stem
    ax.add_patch(FancyBboxPatch(
        (cx - s * 0.06, cy + s * 0.38), s * 0.12, s * 0.20,
        boxstyle=f"round,pad=0,rounding_size={s*0.04:.4f}",
        facecolor=fill, edgecolor="none"))
    # left triangle eye
    eye_pts_l = np.array([
        [cx - s * 0.26, cy + s * 0.16],
        [cx - s * 0.38, cy - s * 0.04],
        [cx - s * 0.14, cy - s * 0.04],
    ])
    ax.add_patch(Polygon(eye_pts_l, closed=True, facecolor=inv, edgecolor="none"))
    # right triangle eye
    eye_pts_r = eye_pts_l.copy()
    eye_pts_r[:, 0] = cx + (eye_pts_l[:, 0] - cx) * -1
    ax.add_patch(Polygon(eye_pts_r, closed=True, facecolor=inv, edgecolor="none"))
    # jagged smile
    mouth_y_top = cy - s * 0.10
    mouth_y_bot = cy - s * 0.28
    teeth_x = np.linspace(cx - s * 0.32, cx + s * 0.32, 9)
    mouth_pts = [(teeth_x[0], mouth_y_top)]
    for i, x in enumerate(teeth_x):
        mouth_pts.append((x, mouth_y_bot if i % 2 == 0 else mouth_y_top))
    mouth_pts.append((teeth_x[-1], mouth_y_top))
    ax.add_patch(Polygon(mouth_pts, closed=True, facecolor=inv, edgecolor="none"))


def draw():
    """Seamless jack-o-lantern face tessellation, 5x6 grid."""
    fig, ax = setup_ax()
    cols, rows = 5, 6
    dx, dy = PERIOD / cols, PERIOD / rows
    s = min(dx, dy) * 0.84
    for row in range(rows):
        for col in range(cols):
            cx = (col + 0.5) * dx + (dx * 0.5 if row % 2 else 0)
            cy = (row + 0.5) * dy
            fill = "black" if (row + col) % 2 == 0 else "white"
            inv = "white" if fill == "black" else "black"
            edge = "none" if fill == "black" else "black"
            for ox, oy in WRAPS:
                pumpkin(ax, cx + ox, cy + oy, s, fill=fill, inv=inv)
    save(fig, "abstract halloween tessellation jack o lantern face repeating grid pattern black white texture")


if __name__ == "__main__":
    draw()
