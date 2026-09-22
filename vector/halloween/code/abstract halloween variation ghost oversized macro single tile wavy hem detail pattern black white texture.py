import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch, Ellipse, Circle
from matplotlib.path import Path as MPath
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


def draw_ghost_macro(ax, cx, cy, s):
    """Oversized ghost with deeply pronounced wavy hem — 5-wave undulation."""
    fill = "white"
    inv = "black"

    # Dome head arc
    t_r = np.linspace(np.pi / 2, 0, 40)
    x_r = cx + s * 0.38 * np.cos(t_r)
    y_r = cy + s * 0.30 + s * 0.38 * np.sin(t_r)

    # right body side, slightly bowed outward
    x_br = np.array([cx + s * 0.38, cx + s * 0.45, cx + s * 0.48])
    y_br = np.array([cy + s * 0.30, cy + s * 0.02, cy - s * 0.28])

    # Deep wavy hem — 5 full waves with large amplitude
    x_wave = np.linspace(cx + s * 0.48, cx - s * 0.48, 120)
    y_wave = (cy - s * 0.28) + s * 0.10 * np.sin((x_wave - cx) / (s * 0.48) * 5 * np.pi)

    # Left body side
    x_bl = np.array([cx - s * 0.48, cx - s * 0.45, cx - s * 0.38])
    y_bl = np.array([cy - s * 0.28, cy + s * 0.02, cy + s * 0.30])

    t_l = np.linspace(np.pi, np.pi / 2, 40)
    x_l = cx + s * 0.38 * np.cos(t_l)
    y_l = cy + s * 0.30 + s * 0.38 * np.sin(t_l)

    pts_x = np.concatenate([x_r, x_br, x_wave, x_bl, x_l])
    pts_y = np.concatenate([y_r, y_br, y_wave, y_bl, y_l])
    pts = np.column_stack([pts_x, pts_y])
    codes = [MPath.MOVETO] + [MPath.LINETO] * (len(pts) - 2) + [MPath.CLOSEPOLY]
    ax.add_patch(PathPatch(MPath(pts, codes), facecolor=fill, edgecolor="none", zorder=2))

    # Eyes — large oval
    for ex in (-s * 0.14, s * 0.14):
        ax.add_patch(Ellipse((cx + ex, cy + s * 0.28), s * 0.13, s * 0.18,
                             facecolor=inv, edgecolor="none", zorder=3))
    # Mouth — wide open O
    ax.add_patch(Ellipse((cx, cy + s * 0.06), s * 0.12, s * 0.14,
                         facecolor=inv, edgecolor="none", zorder=3))

    # Decorative inner wavy line outline hint along hem (thin stroke)
    x_wave2 = np.linspace(cx + s * 0.44, cx - s * 0.44, 120)
    y_wave2 = (cy - s * 0.22) + s * 0.10 * np.sin((x_wave2 - cx) / (s * 0.48) * 5 * np.pi)
    ax.plot(x_wave2, y_wave2, color=inv, linewidth=1.5, zorder=4, alpha=0.5)


def draw():
    """2×2 macro ghost tiles — each ghost nearly fills the full tile.
    Only 4 per canvas so the figure reads as giant close-up silhouettes.
    Seamless grid tiling."""
    fig, ax = setup_ax()

    cols, rows = 2, 2
    dx, dy = PERIOD / cols, PERIOD / rows
    s = min(dx, dy) * 0.88

    for row in range(-1, rows + 1):
        for col in range(-1, cols + 1):
            cx = (col + 0.5) * dx
            cy = (row + 0.5) * dy
            for ox, oy in WRAPS:
                px, py = cx + ox, cy + oy
                if -s <= px <= PERIOD + s and -s <= py <= PERIOD + s:
                    draw_ghost_macro(ax, px, py, s)

    save(fig, "abstract halloween variation ghost oversized macro single tile wavy hem detail pattern black white texture")


if __name__ == "__main__":
    draw()
