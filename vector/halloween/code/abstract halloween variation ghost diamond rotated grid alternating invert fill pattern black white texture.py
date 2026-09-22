import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch, Ellipse, Polygon
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


def draw_ghost(ax, cx, cy, s, fill="black"):
    """Ghost silhouette with wavy bottom hem."""
    inv = "white" if fill == "black" else "black"

    t_r = np.linspace(np.pi / 2, 0, 20)
    x_r = cx + s * 0.28 * np.cos(t_r)
    y_r = cy + s * 0.25 + s * 0.28 * np.sin(t_r)

    x_br = np.array([cx + s * 0.28, cx + s * 0.36, cx + s * 0.38])
    y_br = np.array([cy + s * 0.25, cy, cy - s * 0.28])

    x_wave = np.linspace(cx + s * 0.38, cx - s * 0.38, 50)
    y_wave = (cy - s * 0.28) + s * 0.06 * np.sin((x_wave - cx) / (s * 0.38) * 2.5 * np.pi)

    x_bl = np.array([cx - s * 0.38, cx - s * 0.36, cx - s * 0.28])
    y_bl = np.array([cy - s * 0.28, cy, cy + s * 0.25])

    t_l = np.linspace(np.pi, np.pi / 2, 20)
    x_l = cx + s * 0.28 * np.cos(t_l)
    y_l = cy + s * 0.25 + s * 0.28 * np.sin(t_l)

    pts_x = np.concatenate([x_r, x_br, x_wave, x_bl, x_l])
    pts_y = np.concatenate([y_r, y_br, y_wave, y_bl, y_l])
    pts = np.column_stack([pts_x, pts_y])
    codes = [MPath.MOVETO] + [MPath.LINETO] * (len(pts) - 2) + [MPath.CLOSEPOLY]
    path = MPath(pts, codes)
    # Both fills get an outline: white ghost → black outline, black ghost → white outline
    ec = "black" if fill == "white" else "white"
    ax.add_patch(PathPatch(path, facecolor=fill, edgecolor=ec, linewidth=0.8, zorder=2))

    for ex in (-s * 0.10, s * 0.10):
        ax.add_patch(Ellipse((cx + ex, cy + s * 0.23), s * 0.08, s * 0.11,
                             facecolor=inv, edgecolor="none", zorder=3))
    ax.add_patch(Ellipse((cx, cy + s * 0.09), s * 0.065, s * 0.09,
                         facecolor=inv, edgecolor="none", zorder=3))


def draw():
    """Ghost on a 45°-rotated diamond grid. Cell centres sit on a diagonal lattice.
    Alternating diamonds are filled black so ghosts swap black/white fills.
    Seamless: the diamond grid tiles perfectly at PERIOD."""
    fig, ax = setup_ax()

    # Diamond grid: tile with basis vectors (d, d) and (d, -d)
    # Cell spacing along X and Y axis
    n = 6          # number of diamonds per row/column
    d = PERIOD / n # half-diagonal length → diamond cell size

    # Fill alternating background diamonds black
    for row in range(-1, n + 1):
        for col in range(-1, n + 1):
            if (row + col) % 2 == 0:
                cx = (col + 0.5) * d
                cy = (row + 0.5) * d
                diamond = np.array([
                    [cx,      cy + d],
                    [cx + d,  cy    ],
                    [cx,      cy - d],
                    [cx - d,  cy    ],
                ])
                ax.add_patch(Polygon(diamond, closed=True,
                                     facecolor="black", edgecolor="none", zorder=0))

    s = d * 0.62  # ghost scale relative to diamond cell

    for row in range(-1, n + 2):
        for col in range(-1, n + 2):
            cx = (col + 0.5) * d
            cy = (row + 0.5) * d
            fill = "white" if (row + col) % 2 == 0 else "black"
            for ox, oy in WRAPS:
                px, py = cx + ox, cy + oy
                if -20 <= px <= PERIOD + 20 and -20 <= py <= PERIOD + 20:
                    draw_ghost(ax, px, py, s, fill=fill)

    save(fig, "abstract halloween variation ghost diamond rotated grid alternating invert fill pattern black white texture")


if __name__ == "__main__":
    draw()
