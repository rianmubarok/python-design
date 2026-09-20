import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
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


def candy_corn(ax, cx, cy, h, angle_deg=0):
    """Three-banded triangle candy corn — tall tip at top.
    Rendered in b&w: white tip, mid grey (drawn as white outline triangle), black base."""
    a = np.radians(angle_deg)
    hw_base = h * 0.38  # half-width at base
    hw_mid = h * 0.20

    # raw points (vertical, tip up)
    tip = np.array([0, h * 0.50])
    mid_l = np.array([-hw_mid, h * 0.10])
    mid_r = np.array([hw_mid, h * 0.10])
    base_l = np.array([-hw_base, -h * 0.50])
    base_r = np.array([hw_base, -h * 0.50])

    def rot(pt):
        c, s_ = np.cos(a), np.sin(a)
        return np.array([c * pt[0] - s_ * pt[1] + cx,
                         s_ * pt[0] + c * pt[1] + cy])

    # Full outline (white fill)
    full = [rot(tip), rot(mid_l), rot(base_l), rot(base_r), rot(mid_r)]
    ax.add_patch(Polygon(full, closed=True, facecolor="white", edgecolor="none"))

    # Middle band (darker = white outline only)
    mid_pts = [rot(mid_l), rot(mid_r), rot(np.array([hw_mid, -h * 0.08])),
               rot(np.array([-hw_mid, -h * 0.08]))]
    ax.add_patch(Polygon(mid_pts, closed=True, facecolor="none",
                         edgecolor="black", linewidth=0.6))

    # Base band (black)
    base_pts = [rot(np.array([-hw_mid, -h * 0.08])),
                rot(np.array([hw_mid, -h * 0.08])),
                rot(base_r), rot(base_l)]
    ax.add_patch(Polygon(base_pts, closed=True, facecolor="black", edgecolor="none"))

    # thin outline
    ax.add_patch(Polygon(full, closed=True, facecolor="none",
                         edgecolor="white", linewidth=0.35))


def draw():
    """Scattered candy corns of varying sizes and orientations on black —
    density increases toward tile centre for an 'exploded' scatter look."""
    fig, ax = setup_ax()
    rng = np.random.default_rng(55)
    # Place candy corns on a jittered hex grid at multiple density levels
    cols, rows = 11, 11
    dx, dy = PERIOD / cols, PERIOD / rows

    for row in range(rows):
        for col in range(cols):
            n_per_cell = rng.integers(1, 4)
            for _ in range(n_per_cell):
                jx = rng.uniform(0.05, 0.95) * dx
                jy = rng.uniform(0.05, 0.95) * dy
                cx = col * dx + jx
                cy = row * dy + jy
                h = rng.uniform(2.2, 6.5)
                angle = rng.uniform(0, 360)
                for ox, oy in WRAPS:
                    candy_corn(ax, cx + ox, cy + oy, h, angle)
    save(fig, "abstract halloween variation candy corn scatter exploded black background pattern black white texture")


if __name__ == "__main__":
    draw()
