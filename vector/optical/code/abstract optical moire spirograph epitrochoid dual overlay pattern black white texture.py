import numpy as np
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
    ax.set_xlim(-50, 50)
    ax.set_ylim(-50, 50)
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


def generate():
    """Wild: Concentric ring Moire where each ring is a SPIROGRAPH (epitrochoid) not a circle."""
    fig, ax = setup_ax()

    theta = np.linspace(0, 20 * np.pi, 5000)
    n_sets = 2
    offsets = [(-2, -2), (2, 2)]

    for (ox, oy) in offsets:
        for k in range(30):
            R = 2 + k * 1.5  # Outer radius grows
            r_inner = R / 4.0
            d = R / 3.0

            x = ox + (R - r_inner) * np.cos(theta) + d * np.cos((R - r_inner) / r_inner * theta)
            y = oy + (R - r_inner) * np.sin(theta) - d * np.sin((R - r_inner) / r_inner * theta)

            ax.plot(x, y, color="black", linewidth=0.5)

    save(fig, "abstract optical moire spirograph epitrochoid dual overlay pattern black white texture")


if __name__ == "__main__":
    generate()
