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
    print(f"Saved: {jpg_path}")


def hourglass(ax, cx, cy, w, h, fill="black", inv="white"):
    """Classic hourglass silhouette with top/bottom caps and sand fill."""
    hw = w / 2
    hh = h / 2
    neck = hw * 0.10  # narrow neck half-width

    # outer silhouette
    pts = np.array([
        [-hw,      hh],       # top-left
        [ hw,      hh],       # top-right
        [ neck,    0.04*hh],  # neck-right
        [ neck,   -0.04*hh],
        [ hw,     -hh],       # bottom-right
        [-hw,     -hh],       # bottom-left
        [-neck,   -0.04*hh],
        [-neck,    0.04*hh],  # neck-left
    ]) + [cx, cy]
    ax.add_patch(Polygon(pts, closed=True, facecolor=fill, edgecolor="none"))

    # top/bottom cap bars
    for sign in (1, -1):
        ax.add_patch(FancyBboxPatch(
            (cx - hw * 1.12, cy + sign * hh - (0.06*h if sign > 0 else 0)),
            hw * 2.24, 0.06 * h,
            boxstyle=f"round,pad=0,rounding_size={0.015*h:.4f}",
            facecolor=fill, edgecolor="none"))

    # glass body outline (inner hollow upper half)
    inner_pts_top = np.array([
        [-hw * 0.86,  hh * 0.86],
        [ hw * 0.86,  hh * 0.86],
        [ neck * 1.4, 0.12 * hh],
        [-neck * 1.4, 0.12 * hh],
    ]) + [cx, cy]
    ax.add_patch(Polygon(inner_pts_top, closed=True, facecolor=inv, edgecolor="none"))

    # inner hollow lower half
    inner_pts_bot = np.array([
        [-neck * 1.4, -0.12 * hh],
        [ neck * 1.4, -0.12 * hh],
        [ hw * 0.86,  -hh * 0.86],
        [-hw * 0.86,  -hh * 0.86],
    ]) + [cx, cy]
    ax.add_patch(Polygon(inner_pts_bot, closed=True, facecolor=inv, edgecolor="none"))

    # sand level in lower half (black fill)
    sand_h = hh * 0.55
    sand_top_w = hw * 0.86 * (sand_h / (hh * 0.86))
    sand_pts = np.array([
        [-sand_top_w, -hh * 0.86 + sand_h],
        [ sand_top_w, -hh * 0.86 + sand_h],
        [ hw * 0.86,  -hh * 0.86],
        [-hw * 0.86,  -hh * 0.86],
    ]) + [cx, cy]
    ax.add_patch(Polygon(sand_pts, closed=True, facecolor=fill, edgecolor="none"))

    # falling sand stream
    ax.plot([cx, cx], [cy - 0.10 * hh, cy - hh * 0.86 + sand_h],
            color=fill, linewidth=0.8)

    # skull engraved on upper glass
    skull_cx, skull_cy = cx, cy + hh * 0.42
    sk = w * 0.16
    ax.add_patch(Ellipse((skull_cx, skull_cy + 0.1*sk), sk*0.9, sk*0.8,
                         facecolor=fill, edgecolor="none"))
    for ex in (-sk*0.22, sk*0.22):
        ax.add_patch(Circle((skull_cx+ex, skull_cy+0.15*sk), sk*0.16,
                            facecolor=inv, edgecolor="none"))


def draw():
    """Seamless hourglass tessellation — 5×6 staggered, alternating black/white."""
    fig, ax = setup_ax()
    cols, rows = 5, 6
    dx, dy = PERIOD / cols, PERIOD / rows
    w = dx * 0.82
    h = dy * 0.88
    for row in range(rows):
        for col in range(cols):
            cx = (col + 0.5) * dx + (dx * 0.5 if row % 2 else 0)
            cy = (row + 0.5) * dy
            fill = "black" if (row + col) % 2 == 0 else "white"
            inv = "white" if fill == "black" else "black"
            bg = inv
            ax.add_patch(Polygon([
                [cx-dx/2, cy-dy/2],[cx+dx/2, cy-dy/2],
                [cx+dx/2, cy+dy/2],[cx-dx/2, cy+dy/2]
            ], closed=True, facecolor=bg, edgecolor="none"))
            for ox, oy in WRAPS:
                hourglass(ax, cx+ox, cy+oy, w, h, fill=fill, inv=inv)
    save(fig, "abstract halloween tessellation hourglass silhouette death time motif pattern black white texture")


if __name__ == "__main__":
    draw()
