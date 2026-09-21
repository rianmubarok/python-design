import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from pathlib import Path
from datetime import datetime

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


def draw():
    """Isometric rhombus weave pattern transformed by a continuous sine twist wave field."""
    fig, ax = setup_ax()
    a = 6.5
    dx = a * np.sqrt(3)
    dy = a * 1.5

    cols, rows = 18, 18
    center_x = (cols - 1) * dx / 2.0
    center_y = (rows - 1) * dy / 2.0

    # Fungsi deformasi gelombang kontinyu untuk menjaga keutuhan kisi
    def warp(x, y):
        twist = 1.2 * np.sin(x * 0.08) + 0.9 * np.cos(y * 0.1)
        return x, y + twist

    for row in range(rows):
        for col in range(cols):
            cx = col * dx + (dx / 2.0 if row % 2 else 0.0)
            cy = row * dy

            # Pusat heksagon
            pcx, pcy = warp(cx, cy)

            # 6 Titik Sudut Heksagon Isometrik
            v_orig = [
                (cx, cy + a),
                (cx + a * np.sqrt(3) / 2, cy + a / 2),
                (cx + a * np.sqrt(3) / 2, cy - a / 2),
                (cx, cy - a),
                (cx - a * np.sqrt(3) / 2, cy - a / 2),
                (cx - a * np.sqrt(3) / 2, cy + a / 2),
            ]

            # Transformasi seluruh titik sudut agar kisi tetap tersambung rapat
            v = [warp(vx, vy) for vx, vy in v_orig]

            # 3 Belah Ketupat (Rhombus Face) pembentuk kubus/anyaman 3D
            r1 = [pcx, pcy], v[0], v[1], v[2]  # Atas / Kanan
            r2 = [pcx, pcy], v[2], v[3], v[4]  # Bawah
            r3 = [pcx, pcy], v[4], v[5], v[0]  # Kiri

            # Render 3 Muka Belah Ketupat dengan nuansa kontras untuk mempertegas anyaman
            ax.add_patch(
                Polygon(
                    r1,
                    closed=True,
                    facecolor="white",
                    edgecolor="black",
                    linewidth=0.9,
                    zorder=2,
                )
            )
            ax.add_patch(
                Polygon(
                    r2,
                    closed=True,
                    facecolor="white",
                    edgecolor="black",
                    linewidth=0.9,
                    hatch="///",
                    zorder=2,
                )
            )
            ax.add_patch(
                Polygon(
                    r3,
                    closed=True,
                    facecolor="black",
                    edgecolor="black",
                    linewidth=0.9,
                    zorder=2,
                )
            )

    # Tangkapan fokus area tengah
    pad = 36.0
    ax.set_xlim(center_x - pad, center_x + pad)
    ax.set_ylim(center_y - pad, center_y + pad)

    save(
        fig,
        "abstract grid tessellation isometric rhombus weave sine twist pattern black white texture",
    )


if __name__ == "__main__":
    draw()