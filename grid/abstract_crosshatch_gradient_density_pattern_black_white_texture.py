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


def crosshatch_gradient():
    fig, ax = setup_ax()
    angles = [45, 135]
    for angle in angles:
        rad = np.radians(angle)
        cos_a = np.cos(rad)
        sin_a = np.sin(rad)
        for offset in np.arange(-150, 250, 5):
            x_line = np.array([-10, 110])
            y_line = (x_line - offset) * sin_a / cos_a if abs(cos_a) > 0.001 else np.array([offset, offset])
            if angle == 90:
                y_line = np.array([-10, 110])
                x_line = np.array([offset, offset])
            mask = (y_line >= -10) & (y_line <= 110)
            if mask.any():
                cx_mid = np.mean(x_line[mask])
                cy_mid = np.mean(y_line[mask])
                dist = np.sqrt((cx_mid - 50)**2 + (cy_mid - 50)**2)
                lw = 0.3 + 1.5 * (1 - dist / 80)
                ax.plot(x_line[mask], y_line[mask], color="black", linewidth=lw, alpha=0.7)
    save(fig, "crosshatch_gradient")


if __name__ == "__main__":
    crosshatch_gradient()
