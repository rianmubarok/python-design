import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
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


def crescent(ax, cx, cy, r, point_dir=0):
    """Crescent pointing in point_dir radians (tip direction)."""
    offset = r * 0.58
    ax.add_patch(Circle((cx, cy), r, facecolor="white", edgecolor="none", zorder=2))
    cut_cx = cx + offset * np.cos(point_dir + np.pi)
    cut_cy = cy + offset * np.sin(point_dir + np.pi)
    ax.add_patch(Circle((cut_cx, cut_cy), r * 0.78, facecolor="black",
                        edgecolor="none", zorder=3))


def draw():
    """Crescents linked tip-to-tip in diagonal chains — each crescent faces the
    next one along the chain direction so horns point toward each other."""
    fig, ax = setup_ax()
    chain_angle = np.radians(45)   # diagonal chain direction
    r = 5.2
    # spacing along chain = ~2r  (tip-to-tip touching)
    spacing = r * 2.1
    # number of chains to fill canvas
    perp_spacing = r * 3.5
    cos_a, sin_a = np.cos(chain_angle), np.sin(chain_angle)

    for chain_idx in range(-4, 20):
        for pos_idx in range(-4, 24):
            u = pos_idx * spacing
            v = chain_idx * perp_spacing
            cx = u * cos_a - v * sin_a
            cy = u * sin_a + v * cos_a
            cx = cx % PERIOD
            cy = cy % PERIOD
            # alternate pointing along and against chain
            pt_dir = chain_angle if pos_idx % 2 == 0 else chain_angle + np.pi
            for ox, oy in WRAPS:
                crescent(ax, cx+ox, cy+oy, r, pt_dir)
    save(fig, "abstract halloween variation crescent moon tip to tip diagonal chain pattern black white texture")


if __name__ == "__main__":
    draw()
