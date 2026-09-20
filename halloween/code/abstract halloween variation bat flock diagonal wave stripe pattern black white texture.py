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


def bat_poly(cx, cy, s, angle=0.0):
    pts = np.array([
        [0.00,  0.08], [0.12,  0.18], [0.10,  0.05], [0.42,  0.22], [0.78,  0.38],
        [0.62,  0.08], [0.95,  0.12], [0.55, -0.08], [0.72, -0.28], [0.28, -0.10],
        [0.18, -0.22], [0.08, -0.08], [0.00, -0.18],
        [-0.08,-0.08], [-0.18,-0.22], [-0.28,-0.10], [-0.72,-0.28],
        [-0.55,-0.08], [-0.95, 0.12], [-0.62, 0.08], [-0.78, 0.38],
        [-0.42, 0.22], [-0.10, 0.05], [-0.12, 0.18],
    ]) * s
    c, s_ = np.cos(angle), np.sin(angle)
    R = np.array([[c, -s_], [s_, c]])
    return (R @ pts.T).T + [cx, cy]


def draw():
    """Diagonal wave flock — bats arranged along sinusoidal diagonal stripes,
    size decreasing toward stripe edges to mimic depth/perspective."""
    fig, ax = setup_ax()
    np.random.seed(3)
    stripe_angle = np.radians(35)
    stripe_spacing = 16.0
    along_spacing = 8.0

    cos_a, sin_a = np.cos(stripe_angle), np.sin(stripe_angle)

    positions = []
    for n_stripe in range(-4, 20):
        for n_along in range(-4, 24):
            u = n_along * along_spacing
            v = n_stripe * stripe_spacing
            wave_offset = 2.5 * np.sin(u * 0.28)
            v_actual = v + wave_offset
            wx = u * cos_a - v_actual * sin_a
            wy = u * sin_a + v_actual * cos_a
            wx = wx % PERIOD
            wy = wy % PERIOD
            v_frac = abs((v % stripe_spacing) - stripe_spacing / 2) / (stripe_spacing / 2)
            size = 3.0 + 2.5 * (1 - v_frac)
            fly_angle = stripe_angle + np.random.uniform(-0.2, 0.2)
            positions.append((wx, wy, size, fly_angle))

    for (cx, cy, s, ang) in positions:
        for ox, oy in WRAPS:
            ax.add_patch(Polygon(bat_poly(cx + ox, cy + oy, s, ang),
                                 closed=True, facecolor="white", edgecolor="none"))

    save(fig, "abstract halloween variation bat flock diagonal wave stripe pattern black white texture")


if __name__ == "__main__":
    draw()
