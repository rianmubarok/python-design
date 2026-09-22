import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, FancyBboxPatch, Polygon
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


def draw_skull_mini(ax, cx, cy, s):
    """Tiny skull silhouette — solid black, no outline."""
    skull_cy = cy + 0.06 * s
    ax.add_patch(Ellipse((cx, skull_cy + 0.09 * s), 0.72 * s, 0.62 * s,
                         facecolor="black", edgecolor="none", zorder=2))
    ax.add_patch(FancyBboxPatch(
        (cx - 0.22 * s, skull_cy - 0.20 * s), 0.44 * s, 0.18 * s,
        boxstyle=f"round,pad=0,rounding_size={0.035 * s:.4f}",
        facecolor="black", edgecolor="none", zorder=2))
    eye_y = skull_cy + 0.12 * s
    for ex in (-0.15 * s, 0.15 * s):
        ax.add_patch(Ellipse((cx + ex, eye_y), 0.15 * s, 0.16 * s,
                             facecolor="white", edgecolor="none", zorder=3))
    ax.add_patch(Polygon(
        [[cx, skull_cy - 0.01 * s],
         [cx - 0.05 * s, skull_cy - 0.08 * s],
         [cx + 0.05 * s, skull_cy - 0.08 * s]],
        closed=True, facecolor="white", edgecolor="none", zorder=3))
    for tx in (-0.085 * s, 0.0, 0.085 * s):
        ax.add_patch(FancyBboxPatch(
            (cx + tx - 0.018 * s, skull_cy - 0.175 * s),
            0.036 * s, 0.080 * s,
            boxstyle="round,pad=0,rounding_size=0.003",
            facecolor="white", edgecolor="none", zorder=3))


def draw():
    """Skulls placed on a crosshatch diagonal grid:
    two overlapping diagonal grids (+45° and -45°) at fine spacing.
    Every intersection gets a small skull — dense micro-fill texture."""
    fig, ax = setup_ax()

    spacing = 8.5       # grid spacing in units
    s = spacing * 0.48  # skull size relative to grid cell

    # Two diagonal grid directions: +45 and -45 deg
    # Grid 1: direction (1,1)/sqrt2, spacing = spacing
    # Grid 2: direction (1,-1)/sqrt2, spacing = spacing
    # Intersections of both grids → regular square grid rotated 45°
    # but we place skulls at EVERY node of BOTH grids combined
    # → rich crosshatch feel

    def grid_points(angle_deg, sp, margin=10):
        """Generate all grid points for one diagonal direction."""
        pts = []
        angle = np.radians(angle_deg)
        perp = angle + np.pi / 2
        # step along direction and perpendicular
        for i in range(int(-(margin + PERIOD) / sp), int((2 * PERIOD + margin) / sp) + 1):
            for j in range(int(-(margin + PERIOD) / sp), int((2 * PERIOD + margin) / sp) + 1):
                x = i * sp * np.cos(angle) + j * sp * np.cos(perp)
                y = i * sp * np.sin(angle) + j * sp * np.sin(perp)
                if -margin <= x <= PERIOD + margin and -margin <= y <= PERIOD + margin:
                    pts.append((x, y))
        return pts

    pts1 = grid_points(45, spacing)
    pts2 = grid_points(-45, spacing)

    # Draw diagonal grid lines for the crosshatch texture
    lw = 0.35
    for angle in (45, -45):
        ang = np.radians(angle)
        perp = ang + np.pi / 2
        n_lines = int(PERIOD * 1.6 / spacing) + 6
        for k in range(-3, n_lines):
            base_x = k * spacing * np.cos(perp)
            base_y = k * spacing * np.sin(perp)
            x0 = base_x - 1.5 * PERIOD * np.cos(ang)
            y0 = base_y - 1.5 * PERIOD * np.sin(ang)
            x1 = base_x + 1.5 * PERIOD * np.cos(ang)
            y1 = base_y + 1.5 * PERIOD * np.sin(ang)
            ax.plot([x0, x1], [y0, y1], color="black", lw=lw,
                    alpha=0.25, zorder=1)

    # Place skulls at grid intersections
    all_pts = set()
    for px, py in pts1 + pts2:
        key = (round(px / 0.5), round(py / 0.5))
        all_pts.add(key)

    for key in all_pts:
        px, py = key[0] * 0.5, key[1] * 0.5
        draw_skull_mini(ax, px, py, s)

    save(fig, "abstract halloween variation skull crosshatch diagonal micro dense fill pattern black white texture")


if __name__ == "__main__":
    draw()
