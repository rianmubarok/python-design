from datetime import datetime
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import matplotlib

matplotlib.use("Agg")

SIZE = 4000
DPI = 300
DATE = datetime.now().strftime("%d%m%Y")

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR.parent / "output"
JPG_DIR = OUTPUT_DIR / "jpg"
SVG_DIR = OUTPUT_DIR / "svg"
JPG_DIR.mkdir(parents=True, exist_ok=True)
SVG_DIR.mkdir(parents=True, exist_ok=True)


def setup_ax():
    fig, ax = plt.subplots(figsize=(SIZE / DPI, SIZE / DPI), dpi=DPI)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.set_facecolor("white")
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


def spiral_square_fibonacci():
    """Spiral Fibonacci dengan susunan persegi presisi dan kurva spiral emas kontinu yang menyatu sempurna."""
    fig, ax = setup_ax()

    # Urutan Fibonacci
    fib = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]

    min_x, max_x = 0.0, 1.0
    min_y, max_y = 0.0, 1.0

    # S0: Persegi Pertama (1x1)
    squares = [(0.0, 0.0, 1.0, 1.0, 1.0, np.pi, 1.5 * np.pi)]

    # Penempelan berurutan: RIGHT -> TOP -> LEFT -> BOTTOM
    for i in range(1, len(fib)):
        s = float(fib[i])
        mod = i % 4
        if mod == 1:  # RIGHT
            bx, by = max_x, min_y
            arc_cx, arc_cy = max_x, max_y
            t1, t2 = 1.5 * np.pi, 2.0 * np.pi
            max_x += s
        elif mod == 2:  # TOP
            bx, by = min_x, max_y
            arc_cx, arc_cy = min_x, max_y
            t1, t2 = 0.0, 0.5 * np.pi
            max_y += s
        elif mod == 3:  # LEFT
            bx, by = min_x - s, min_y
            arc_cx, arc_cy = min_x, min_y
            t1, t2 = 0.5 * np.pi, np.pi
            min_x -= s
        elif mod == 0:  # BOTTOM
            bx, by = min_x, min_y - s
            arc_cx, arc_cy = max_x, min_y
            t1, t2 = np.pi, 1.5 * np.pi
            min_y -= s
        squares.append((bx, by, s, arc_cx, arc_cy, t1, t2))

    # 1. Gambar Kotak-Kotak Persegi Fibonacci
    for idx, (bx, by, s, arc_cx, arc_cy, t1, t2) in enumerate(squares):
        square_x = [bx, bx + s, bx + s, bx, bx]
        square_y = [by, by, by + s, by + s, by]
        ax.plot(
            square_x,
            square_y,
            color="black",
            linewidth=1.2,
            solid_capstyle="round",
            zorder=1,
        )

    # 2. Gambar Kurva Busur Spiral Emas Kontinu
    for idx, (bx, by, s, arc_cx, arc_cy, t1, t2) in enumerate(squares):
        t = np.linspace(t1, t2, 100)
        arc_x = arc_cx + s * np.cos(t)
        arc_y = arc_cy + s * np.sin(t)
        ax.plot(
            arc_x,
            arc_y,
            color="black",
            linewidth=2.8,
            solid_capstyle="round",
            zorder=2,
        )

    # Memfokuskan tampilan simetris tepat di tengah kanvas
    center_x = (min_x + max_x) / 2.0
    center_y = (min_y + max_y) / 2.0
    width = max_x - min_x
    height = max_y - min_y
    pad = max(width, height) / 2.0 * 1.08

    ax.set_xlim(center_x - pad, center_x + pad)
    ax.set_ylim(center_y - pad, center_y + pad)

    save(fig, "spiral square fibonacci")


if __name__ == "__main__":
    spiral_square_fibonacci()