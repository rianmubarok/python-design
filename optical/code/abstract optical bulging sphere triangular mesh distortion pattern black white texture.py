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
    """Wild: Bulging sphere grid with TRIANGULAR mesh instead of rectangular grid."""
    fig, ax = setup_ax()

    n = 60
    pts = np.linspace(-1.2, 1.2, 400)

    def distort(x, y):
        r = np.sqrt(x**2 + y**2)
        d = 1.0 - 0.65 * np.exp(-3 * r**2)
        return x * d, y * d

    # Horizontal lines
    for i in range(n + 1):
        y0 = -1.2 + 2.4 * i / n
        x_arr = pts.copy()
        y_arr = np.full_like(x_arr, y0)
        xd, yd = distort(x_arr, y_arr)
        ax.plot(xd, yd, color="black", linewidth=0.7)

    # Diagonal lines going upper-right
    for i in range(-n, n + 1):
        offset = i * 2.4 / n
        x_arr = pts.copy()
        y_arr = x_arr + offset
        mask = (y_arr >= -1.3) & (y_arr <= 1.3)
        x_arr = x_arr[mask]
        y_arr = y_arr[mask]
        if len(x_arr) > 2:
            xd, yd = distort(x_arr, y_arr)
            ax.plot(xd, yd, color="black", linewidth=0.7)

    # Diagonal lines going upper-left
    for i in range(-n, n + 1):
        offset = i * 2.4 / n
        x_arr = pts.copy()
        y_arr = -x_arr + offset
        mask = (y_arr >= -1.3) & (y_arr <= 1.3)
        x_arr = x_arr[mask]
        y_arr = y_arr[mask]
        if len(x_arr) > 2:
            xd, yd = distort(x_arr, y_arr)
            ax.plot(xd, yd, color="black", linewidth=0.7)

    save(fig, "abstract optical bulging sphere triangular mesh distortion pattern black white texture")


if __name__ == "__main__":
    generate()
