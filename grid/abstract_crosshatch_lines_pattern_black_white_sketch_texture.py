import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

SIZE = 4000
DPI = 300
SEED = 42

PNG_DIR = Path("output/png")
SVG_DIR = Path("output/svg")
PNG_DIR.mkdir(parents=True, exist_ok=True)
SVG_DIR.mkdir(parents=True, exist_ok=True)

np.random.seed(SEED)


def setup_ax():
    fig, ax = plt.subplots(figsize=(SIZE/DPI, SIZE/DPI), dpi=DPI)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.set_facecolor("white")
    ax.set_xlim(-5, 105)
    ax.set_ylim(-5, 105)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def save(fig, name):
    png_path = PNG_DIR / f"{name}.png"
    svg_path = SVG_DIR / f"{name}.svg"
    fig.savefig(png_path, dpi=DPI, pad_inches=0, facecolor="white")
    fig.savefig(svg_path, format="svg", pad_inches=0, facecolor="white")
    plt.close(fig)
    print(f"Tersimpan: {png_path} | {svg_path}")


def crosshatch():
    fig, ax = setup_ax()
    angles = [0, 30, 60, 90, 120, 150]
    for angle in angles:
        rad = np.radians(angle)
        cos_a = np.cos(rad)
        sin_a = np.sin(rad)
        for offset in np.arange(-150, 250, 6):
            if angle == 90:
                ax.plot([offset, offset], [-10, 110], color="black", linewidth=0.8)
            else:
                denom = sin_a if abs(sin_a) > 0.001 else 0.001
                t_vals = np.array([-10, 110])
                x_line = offset + t_vals * cos_a / denom
                y_line = t_vals
                ax.plot(x_line, y_line, color="black", linewidth=0.6, alpha=0.6)
    save(fig, "crosshatch")


if __name__ == "__main__":
    crosshatch()
