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
    eps_path = EPS_DIR / f\"{name} {DATE}.eps\"
    orig_size = fig.get_size_inches()
    fig.set_size_inches(30, 30)
    fig.savefig(eps_path, format=\"eps\", pad_inches=0, facecolor=\"white\", dpi=DPI)
    fig.set_size_inches(orig_size[0], orig_size[1])
    plt.close(fig)
    print(f"Saved: {jpg_path} | {svg_path} | {eps_path}")


def vein_network(ax, cx, cy, r, rng):
    """Sclera circle with dense radiating vein tree, no iris."""
    ax.add_patch(Circle((cx, cy), r, facecolor="white", edgecolor="black",
                        linewidth=0.5, zorder=2))
    n_primary = rng.integers(8, 14)
    for _ in range(n_primary):
        start_a = rng.uniform(0, 2*np.pi)
        sx = cx + r*0.92*np.cos(start_a)
        sy = cy + r*0.92*np.sin(start_a)
        # meander toward centre
        n_segs = rng.integers(3, 7)
        cur_x, cur_y = sx, sy
        cur_a = start_a + np.pi  # points inward
        lw = rng.uniform(0.5, 1.1)
        for seg in range(n_segs):
            cur_a += rng.uniform(-0.5, 0.5)
            seg_len = r * rng.uniform(0.08, 0.22)
            # don't go past centre
            dist_to_cen = np.hypot(cur_x-cx, cur_y-cy)
            if dist_to_cen < r*0.12:
                break
            ex = cur_x + seg_len*np.cos(cur_a)
            ey = cur_y + seg_len*np.sin(cur_a)
            ax.plot([cur_x, ex], [cur_y, ey], color="black",
                    linewidth=lw*(1-seg/n_segs*0.5), solid_capstyle="round",
                    alpha=0.75, zorder=3)
            # branch
            if rng.random() < 0.35 and seg < n_segs-1:
                ba = cur_a + rng.choice([-1,1]) * rng.uniform(0.3, 0.9)
                bl = seg_len * 0.5
                bex = cur_x + bl*np.cos(ba)
                bey = cur_y + bl*np.sin(ba)
                ax.plot([cur_x, bex],[cur_y, bey], color="black",
                        linewidth=lw*0.55, solid_capstyle="round", alpha=0.6, zorder=3)
            cur_x, cur_y = ex, ey
    # tiny pupil dot only
    ax.add_patch(Circle((cx, cy), r*0.10, facecolor="black", edgecolor="none", zorder=4))


def draw():
    """Dense bloodshot vein network eyeballs — no iris colour, just veins and a tiny pupil."""
    fig, ax = setup_ax()
    rng = np.random.default_rng(99)
    cols, rows = 7, 7
    dx, dy = PERIOD/cols, PERIOD/rows
    for row in range(rows):
        for col in range(cols):
            jx = rng.uniform(0.1, 0.9)*dx
            jy = rng.uniform(0.1, 0.9)*dy
            cx = col*dx+jx; cy = row*dy+jy
            r = rng.uniform(0.28, 0.48)*min(dx,dy)
            for ox, oy in WRAPS:
                vein_network(ax, cx+ox, cy+oy, r, rng)
    save(fig, "abstract halloween variation eyeball bloodshot vein network texture field pattern black white texture")


if __name__ == "__main__":
    draw()
