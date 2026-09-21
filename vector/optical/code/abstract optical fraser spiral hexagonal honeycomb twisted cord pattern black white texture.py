import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime

SIZE = 4000
DPI = 300
SEED = 42
DATE = datetime.now().strftime("%d%m%Y")

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR.parent / "output"
JPG_DIR = OUTPUT_DIR / "jpg"
SVG_DIR = OUTPUT_DIR / "svg"
JPG_DIR.mkdir(parents=True, exist_ok=True)
SVG_DIR.mkdir(parents=True, exist_ok=True)

np.random.seed(SEED)


def setup_ax():
    fig, ax = plt.subplots(figsize=(SIZE / DPI, SIZE / DPI), dpi=DPI)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.set_facecolor("white")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def save(fig, name):
    jpg_path = JPG_DIR / f"{name} {DATE}.jpg"
    svg_path = SVG_DIR / f"{name} {DATE}.svg"
    fig.savefig(jpg_path, dpi=DPI, pad_inches=0, facecolor="white")
    fig.savefig(svg_path, format="svg", pad_inches=0, facecolor="white")
    plt.close(fig)
    print(f"Tersimpan: {jpg_path} | {svg_path}")


def hex_points(cx, cy, r):
    ang = np.linspace(0, 2 * np.pi, 7)
    return cx + r * np.cos(ang), cy + r * np.sin(ang)


def generate():
    """Wild: Fraser twisted cords laid along a seamless hexagonal honeycomb."""
    fig, ax = setup_ax()

    r = 7.2
    dx = r * 1.5
    dy = r * np.sqrt(3)
    rows = int(100 / dy) + 3
    cols = int(100 / dx) + 3

    for row in range(-1, rows):
        for col in range(-1, cols):
            cx = col * dx + (r * 0.75 if row % 2 else 0)
            cy = row * dy
            xs, ys = hex_points(cx, cy, r)
            ax.plot(xs, ys, color="black", linewidth=0.55, alpha=0.55)
            for i in range(6):
                x1, y1 = xs[i], ys[i]
                x2, y2 = xs[i + 1], ys[i + 1]
                n_cords = 7
                for t in np.linspace(0.08, 0.92, n_cords):
                    mx = x1 + t * (x2 - x1)
                    my = y1 + t * (y2 - y1)
                    ang = np.arctan2(y2 - y1, x2 - x1) + np.pi / 2
                    tilt = 0.42 if (row + col + i) % 2 == 0 else -0.42
                    a = ang + tilt
                    L = 1.15
                    dxc, dyc = L * np.cos(a), L * np.sin(a)
                    ax.plot([mx - dxc, mx + dxc], [my - dyc, my + dyc], color="black", linewidth=1.7)
                    ax.plot(
                        [mx - dxc * 0.4, mx + dxc * 0.4],
                        [my - dyc * 0.4, my + dyc * 0.4],
                        color="white",
                        linewidth=0.7,
                    )

    save(
        fig,
        "abstract optical fraser spiral hexagonal honeycomb twisted cord pattern black white texture",
    )


if __name__ == "__main__":
    generate()
