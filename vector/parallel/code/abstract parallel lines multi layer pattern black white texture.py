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


def abstract_parallel_lines_multi_layer_pattern_black_white_texture():
    """Garis paralel berlapis dengan orientasi berbeda"""
    fig, ax = setup_ax()
    layers = [
        {"angle": 0, "spacing": 4, "lw": 1.5, "alpha": 0.8},
        {"angle": 60, "spacing": 6, "lw": 1.0, "alpha": 0.5},
        {"angle": 120, "spacing": 8, "lw": 0.8, "alpha": 0.3},
    ]
    for layer in layers:
        angle = layer["angle"]
        rad = np.radians(angle)
        cos_a = np.cos(rad)
        sin_a = np.sin(rad)
        for offset in np.arange(-150, 250, layer["spacing"]):
            if abs(sin_a) > 0.001:
                x = np.array([-20, 120])
                y = (x - offset) * sin_a / cos_a
            else:
                x = np.array([offset, offset])
                y = np.array([-20, 120])
            ax.plot(x, y, color="black", linewidth=layer["lw"], alpha=layer["alpha"])
    save(fig, "abstract parallel lines multi layer pattern black white texture")


if __name__ == "__main__":
    abstract_parallel_lines_multi_layer_pattern_black_white_texture()
