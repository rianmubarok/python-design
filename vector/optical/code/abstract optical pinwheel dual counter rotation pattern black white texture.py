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
    ax.set_xlim(-5, 105)
    ax.set_ylim(-5, 105)
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
    """Tweak: Two counter-rotating pinwheel layers creating opposing spin illusion."""
    fig, ax = setup_ax()

    t = np.linspace(0, 45, 200)

    # Layer A: CW twist, thin spokes
    n_spokes_a = 40
    for i in range(n_spokes_a):
        base_angle = i * 2 * np.pi / n_spokes_a
        angle = base_angle + 0.06 * t
        x = 50 + t * np.cos(angle)
        y = 50 + t * np.sin(angle)
        lw = 0.6 if i % 2 == 0 else 2.2
        ax.plot(x, y, color="black", linewidth=lw)

    # Layer B: CCW twist, sparse spokes
    n_spokes_b = 20
    for i in range(n_spokes_b):
        base_angle = i * 2 * np.pi / n_spokes_b + np.pi / n_spokes_b
        angle = base_angle - 0.09 * t
        x = 50 + t * np.cos(angle)
        y = 50 + t * np.sin(angle)
        ax.plot(x, y, color="black", linewidth=1.0)

    save(fig, "abstract optical pinwheel dual counter rotation pattern black white texture")


if __name__ == "__main__":
    generate()
