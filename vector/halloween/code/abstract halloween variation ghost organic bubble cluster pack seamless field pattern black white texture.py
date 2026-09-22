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


def draw_ghost(ax, cx, cy, s, fill="white"):
    """Ghost silhouette — round head, wavy hem."""
    inv = "black" if fill == "white" else "white"

    t_r = np.linspace(np.pi / 2, 0, 20)
    x_r = cx + s * 0.28 * np.cos(t_r)
    y_r = cy + s * 0.24 + s * 0.28 * np.sin(t_r)

    x_br = np.array([cx + s*0.28, cx + s*0.36, cx + s*0.37])
    y_br = np.array([cy + s*0.24, cy + s*0.02, cy - s*0.26])

    x_wave = np.linspace(cx + s*0.37, cx - s*0.37, 44)
    y_wave = (cy - s*0.26) + s*0.055 * np.sin((x_wave - cx) / (s*0.37) * 2.5 * np.pi)

    x_bl = np.array([cx - s*0.37, cx - s*0.36, cx - s*0.28])
    y_bl = np.array([cy - s*0.26, cy + s*0.02, cy + s*0.24])

    t_l = np.linspace(np.pi, np.pi / 2, 20)
    x_l = cx + s*0.28 * np.cos(t_l)
    y_l = cy + s*0.24 + s*0.28 * np.sin(t_l)

    pts_x = np.concatenate([x_r, x_br, x_wave, x_bl, x_l])
    pts_y = np.concatenate([y_r, y_br, y_wave, y_bl, y_l])
    pts = np.column_stack([pts_x, pts_y])
    codes = [MPath.MOVETO] + [MPath.LINETO]*(len(pts)-2) + [MPath.CLOSEPOLY]
    ax.add_patch(PathPatch(MPath(pts, codes),
                           facecolor=fill, edgecolor="none", zorder=2))

    for ex in (-s*0.09, s*0.09):
        ax.add_patch(Ellipse((cx+ex, cy+s*0.22), s*0.07, s*0.10,
                             facecolor=inv, edgecolor="none", zorder=3))
    ax.add_patch(Ellipse((cx, cy+s*0.08), s*0.06, s*0.08,
                         facecolor=inv, edgecolor="none", zorder=3))


def draw():
    """Organic bubble-pack layout: ghosts of 3 different sizes scattered to fill space.
    Uses a fixed jittered hexagonal packing to get a dense, varied organic feel.
    White ghosts on black. No regular grid — looks like a floating cluster."""
    fig, ax = setup_ax()

    rng = np.random.default_rng(99)

    # Three size classes
    entries = []
    for s, n in [(7.0, 10), (4.5, 18), (2.8, 30)]:
        for _ in range(n):
            x = rng.uniform(0, PERIOD)
            y = rng.uniform(0, PERIOD)
            entries.append((x, y, s))

    # Sort by size descending so small ghosts are drawn on top
    entries.sort(key=lambda e: -e[2])

    for cx, cy, s in entries:
        for ox, oy in WRAPS:
            px, py = cx + ox, cy + oy
            if -12 <= px <= PERIOD + 12 and -12 <= py <= PERIOD + 12:
                draw_ghost(ax, px, py, s, fill="white")

    save(fig, "abstract halloween variation ghost organic bubble cluster pack seamless field pattern black white texture")


if __name__ == "__main__":
    draw()
