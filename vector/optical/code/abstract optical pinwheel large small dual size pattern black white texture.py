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


def draw_pinwheel(ax, cx, cy, max_r, n_spokes, twist_rate, lw_thin, lw_thick):
    t = np.linspace(0, max_r, 150)
    for i in range(n_spokes):
        base_angle = i * 2 * np.pi / n_spokes
        angle = base_angle + twist_rate * t
        x = cx + t * np.cos(angle)
        y = cy + t * np.sin(angle)
        lw = lw_thin if i % 2 == 0 else lw_thick
        ax.plot(x, y, color="black", linewidth=lw)


def generate():
    """Tweak: Central large pinwheel + 6 satellites at ring positions."""
    fig, ax = setup_ax()

    # Large central
    draw_pinwheel(ax, 50, 50, 28, 60, 0.05, 0.5, 1.8)

    # 6 smaller satellites
    n_sats = 6
    orbit_r = 36
    for k in range(n_sats):
        angle = k * 2 * np.pi / n_sats
        cx = 50 + orbit_r * np.cos(angle)
        cy = 50 + orbit_r * np.sin(angle)
        draw_pinwheel(ax, cx, cy, 12, 30, -0.08, 0.4, 1.2)

    save(fig, "abstract optical pinwheel large small dual size pattern black white texture")


if __name__ == "__main__":
    generate()
