from datetime import datetime
from pathlib import Path
from matplotlib.patches import (
    Arc,
    Circle,
    Ellipse,
    FancyBboxPatch,
    Polygon,
    RegularPolygon,
)
from matplotlib.transforms import Affine2D
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


def squircle(cx, cy, rx, ry, p, n=72):
    t = np.linspace(0, 2 * np.pi, n)
    ct, st = np.cos(t), np.sin(t)
    x = cx + rx * np.sign(ct) * (np.abs(ct) ** (2 / p))
    y = cy + ry * np.sign(st) * (np.abs(st) ** (2 / p))
    return x, y


def draw():
    """Houndstooth as concentric outlines with a positional offset wave."""
    fig, ax = setup_ax()

    p0 = np.array(
        [
            [-1, 1],
            [0, 1],
            [0, 2],
            [1, 1],
            [1, 0],
            [2, 0],
            [1, -1],
            [0, -1],
            [-1, -2],
            [-1, -1],
            [-2, -1],
            [-1, 0],
        ],
        dtype=float,
    )

    mid = p0.mean(axis=0)

    # Perluas rentang iterasi agar menutupi seluruh kanvas tanpa celah di tepi
    for row in range(-4, 22):
        for col in range(-4, 22):
            # Skala dan gelombang offset
            s = 3.2 * (0.9 + 0.1 * np.sin(col * 0.4))
            cx = (col * 2 + (row % 2)) * 3.8 + 0.6 * np.sin(row * 0.45)
            cy = row * 6.8 + 0.6 * np.cos(col * 0.4)

            # 1. Lapisan Terluar (Dasar) - Menggunakan isian putih padat
            # Ini berfungsi menutupi objek di belakangnya agar garis tidak bertabrakan secara acak
            pts_outer = (p0 - mid) * s * 1.0 + [cx, cy]
            ax.add_patch(
                Polygon(
                    pts_outer,
                    closed=True,
                    facecolor="white",
                    edgecolor="black",
                    linewidth=1.1,
                    zorder=row * 100 + col,
                )
            )

            # 2. Lapisan Dalam Konseintris (Hanya kontur garis tanpa isian)
            for k, sc in enumerate((0.65, 0.35)):
                pts_inner = (p0 - mid) * s * sc + [cx, cy]
                ax.add_patch(
                    Polygon(
                        pts_inner,
                        closed=True,
                        fill=False,
                        edgecolor="black",
                        linewidth=1.0 - (k + 1) * 0.2,
                        zorder=row * 100 + col + k + 1,
                    )
                )

    save(
        fig,
        "abstract grid tessellation houndstooth outline concentric offset pattern black white texture",
    )


if __name__ == "__main__":
    draw()