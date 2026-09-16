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
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
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
    """Wild: Bulging sphere but the distortion INVERTS — grid sinks inward (concave) instead of convex."""
    fig, ax = setup_ax()

    n_lines = 80
    pts = np.linspace(-1.2, 1.2, 500)

    def distort_concave(x, y):
        r = np.sqrt(x**2 + y**2)
        # Inverted: expand near center, compress at edges
        d = 1.0 + 0.5 * np.exp(-4 * r**2)
        return x * d, y * d

    for i in range(n_lines + 1):
        x0 = -1.2 + 2.4 * i / n_lines
        y_arr = pts.copy()
        x_arr = np.full_like(y_arr, x0)
        xd, yd = distort_concave(x_arr, y_arr)
        lw = 0.5 + 1.5 * np.exp(-4 * x0**2)
        ax.plot(xd, yd, color="black", linewidth=lw)

    for i in range(n_lines + 1):
        y0 = -1.2 + 2.4 * i / n_lines
        x_arr = pts.copy()
        y_arr = np.full_like(x_arr, y0)
        xd, yd = distort_concave(x_arr, y_arr)
        lw = 0.5 + 1.5 * np.exp(-4 * y0**2)
        ax.plot(xd, yd, color="black", linewidth=lw)

    save(fig, "abstract optical concave sink grid invert distortion pattern black white texture")


if __name__ == "__main__":
    generate()
