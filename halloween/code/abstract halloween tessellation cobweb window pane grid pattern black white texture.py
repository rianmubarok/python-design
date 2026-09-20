import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import (
    Arc, Circle, Ellipse, FancyBboxPatch, Polygon, Rectangle,
)
from matplotlib.transforms import Affine2D
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
    ax.set_facecolor("white")
    ax.set_xlim(0, PERIOD)
    ax.set_ylim(0, PERIOD)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_clip_on(True)
    return fig, ax


def save(fig, name):
    jpg_path = JPG_DIR / f"{name} {DATE}.jpg"
    svg_path = SVG_DIR / f"{name} {DATE}.svg"
    fig.savefig(jpg_path, dpi=DPI, pad_inches=0, facecolor="white")
    fig.savefig(svg_path, format="svg", pad_inches=0, facecolor="white")
    eps_path = EPS_DIR / f\"{name} {DATE}.eps\"
    orig_size = fig.get_size_inches()
    fig.set_size_inches(30, 30)
    fig.savefig(eps_path, format=\"eps\", pad_inches=0, facecolor=\"white\", dpi=DPI)
    fig.set_size_inches(orig_size[0], orig_size[1])
    plt.close(fig)
    print(f"Tersimpan: {jpg_path} | {svg_path}")

def draw():
    """Seamless cobweb window panes (cells fill the tile exactly)."""
    fig, ax = setup_ax()
    n = 6
    cell = PERIOD / n
    rng = np.random.default_rng(31)
    for r in range(n):
        for c in range(n):
            x0, y0 = c * cell, r * cell
            ax.add_patch(Rectangle((x0, y0), cell, cell, fill=False, edgecolor="black", linewidth=1.2))
            corner = int(rng.integers(0, 4))
            ox = x0 + (0.15 if corner in (0, 3) else cell - 0.15)
            oy = y0 + (0.15 if corner in (0, 1) else cell - 0.15)
            base_ang = [0, 90, 180, 270][corner]
            for k in range(7):
                a = np.deg2rad(base_ang + 8 + k * 10.5)
                L = cell * 0.88
                ax.plot([ox, ox + L * np.cos(a)], [oy, oy + L * np.sin(a)], color="black", linewidth=0.5)
            for sc in (0.2, 0.38, 0.56, 0.74):
                xs, ys = [], []
                for k in range(7):
                    a = np.deg2rad(base_ang + 8 + k * 10.5)
                    xs.append(ox + cell * sc * np.cos(a))
                    ys.append(oy + cell * sc * np.sin(a))
                ax.plot(xs, ys, color="black", linewidth=0.65)
    save(fig, "abstract halloween tessellation cobweb window pane grid pattern black white texture")


if __name__ == "__main__":
    draw()
