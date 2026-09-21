import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
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


def generate():
    """Wild hybrid: Café wall tiles whose mortar is a Fraser twisted cord, seamless."""
    fig, ax = setup_ax()

    n_rows = 16
    n_cols = 14
    row_h = 100.0 / n_rows
    col_w = 100.0 / n_cols
    offsets = [0.0, 0.28, 0.56, 0.28]

    for r in range(n_rows):
        y = r * row_h
        shift = offsets[r % len(offsets)] * col_w
        for c in range(-2, n_cols + 3):
            if (c + r) % 2 == 0:
                ax.add_patch(
                    Rectangle((c * col_w + shift, y), col_w, row_h, facecolor="black", edgecolor="none")
                )

        for k, y_m in enumerate([y, y + row_h] if r == n_rows - 1 else [y]):
            tilt = 0.55 if (r + k) % 2 == 0 else -0.55
            # Twisted cord: black/white alternating short slashes along mortar
            n_cords = 90
            for t in np.linspace(-6, 106, n_cords):
                dx = 1.15
                dy = tilt * 1.05
                ax.plot([t - dx, t + dx], [y_m - dy, y_m + dy], color="black", linewidth=1.55)
                ax.plot(
                    [t - dx * 0.4, t + dx * 0.4],
                    [y_m - dy * 0.4, y_m + dy * 0.4],
                    color="white",
                    linewidth=0.7,
                )

    save(
        fig,
        "abstract optical cafe wall fraser twisted cord mortar hybrid pattern black white texture",
    )


if __name__ == "__main__":
    generate()
