import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse
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
    print(f"Saved: {jpg_path}")


def eyeball(ax, cx, cy, r, iris_angle=0.0):
    """Detailed eyeball: sclera, iris, pupil, veins, highlight."""
    # sclera (white of eye)
    ax.add_patch(Circle((cx, cy), r, facecolor="white", edgecolor="none", zorder=2))

    # veins — thin red-like (black) lines radiating from edges
    rng = np.random.default_rng(abs(int(cx * 100 + cy * 7)) % (2**31))
    for _ in range(rng.integers(4, 8)):
        start_ang = rng.uniform(0, 2 * np.pi)
        sx = cx + r * 0.85 * np.cos(start_ang)
        sy = cy + r * 0.85 * np.sin(start_ang)
        # meander inward
        mid_x = cx + r * 0.45 * np.cos(start_ang + rng.uniform(-0.4, 0.4))
        mid_y = cy + r * 0.45 * np.sin(start_ang + rng.uniform(-0.4, 0.4))
        ax.plot([sx, mid_x], [sy, mid_y], color="black", linewidth=0.35, alpha=0.55, zorder=3)

    # iris
    iris_r = r * 0.55
    ax.add_patch(Circle((cx, cy), iris_r, facecolor="black", edgecolor="none", zorder=4))
    # iris ring detail
    for ring_r in np.linspace(iris_r * 0.6, iris_r * 0.95, 4):
        ax.add_patch(Circle((cx, cy), ring_r, facecolor="none",
                            edgecolor="white", linewidth=0.3, zorder=5))

    # pupil (shifted slightly in iris_angle direction for gaze effect)
    shift = iris_r * 0.18
    px = cx + shift * np.cos(iris_angle)
    py = cy + shift * np.sin(iris_angle)
    ax.add_patch(Circle((px, py), iris_r * 0.5, facecolor="black", edgecolor="none", zorder=6))

    # highlight
    ax.add_patch(Circle((cx + r * 0.28, cy + r * 0.28), r * 0.12,
                        facecolor="white", edgecolor="none", zorder=7))


def draw():
    """Scattered seamless eyeball field — varied sizes and gaze directions on black."""
    fig, ax = setup_ax()
    np.random.seed(42)
    # Poisson-disk-like placement: place eyes on a jittered grid
    cols, rows = 9, 9
    dx, dy = PERIOD / cols, PERIOD / rows
    gaze_angles = np.linspace(0, 2 * np.pi, cols * rows, endpoint=False)
    idx = 0
    for row in range(rows):
        for col in range(cols):
            jx = np.random.uniform(0.15, 0.85) * dx
            jy = np.random.uniform(0.15, 0.85) * dy
            cx = col * dx + jx
            cy = row * dy + jy
            r = np.random.uniform(0.30, 0.52) * min(dx, dy)
            iris_angle = gaze_angles[idx % len(gaze_angles)]
            idx += 1
            for ox, oy in WRAPS:
                eyeball(ax, cx + ox, cy + oy, r, iris_angle)
    save(fig, "abstract halloween variation eyeball scattered field organic pattern black white texture")


if __name__ == "__main__":
    draw()
