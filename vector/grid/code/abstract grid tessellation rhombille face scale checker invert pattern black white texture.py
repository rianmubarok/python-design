from datetime import datetime
from pathlib import Path
from matplotlib.patches import Polygon
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


def draw():
    """Seamless rhombille grid tessellation with continuous wave deformation."""
    fig, ax = setup_ax()

    scale = 5.8
    dx = scale * np.sqrt(3)
    dy = scale * 1.5

    cols, rows = 18, 18
    center_x = (cols - 1) * (dx / 2.0) / 2.0
    center_y = (rows - 1) * dy / 2.0

    # Fungsi deformasi gelombang kontinu pada kisi
    def warp(x, y):
        w = 1.0 * np.sin(x * 0.08) + 0.8 * np.cos(y * 0.1)
        return x, y + w

    for row in range(-2, rows + 2):
        for col in range(-2, cols + 2):
            cx = col * (dx / 2.0)
            cy = row * dy + (dy / 3.0 if col % 2 else 0)

            # 1. Deformasi titik pusat DULU
            pcx, pcy = warp(cx, cy)

            # 2. Hitung titik sudut sebagai offset tetap dari titik pusat yang baru
            # Ini memastikan setiap sudut terhubung sempurna tanpa celah/patahan
            v0 = (pcx, pcy + scale)  # Top
            v1 = (pcx + scale * np.sqrt(3) / 2, pcy + scale / 2)  # Top Right
            v2 = (pcx + scale * np.sqrt(3) / 2, pcy - scale / 2)  # Bottom Right
            v3 = (pcx, pcy - scale)  # Bottom
            v4 = (pcx - scale * np.sqrt(3) / 2, pcy - scale / 2)  # Bottom Left
            v5 = (pcx - scale * np.sqrt(3) / 2, pcy + scale / 2)  # Top Left

            # 3 Sisi Ketupat (Rhombus Faces)
            f_top = [[pcx, pcy], v1, v0, v5]
            f_right = [[pcx, pcy], v2, v3, v1]
            f_left = [[pcx, pcy], v4, v3, v5]

            # Inversi warna papan catur
            invert = (row + col) % 2 == 0

            # Memberikan facecolor "white" pada hatch agar tidak transparan
            styles = [
                {"facecolor": "white" if invert else "black", "zorder": 2},
                {
                    "facecolor": "white",
                    "hatch": "////",
                    "zorder": 1,
                },  # Latar putih + arsir
                {"facecolor": "black" if invert else "white", "zorder": 3},
            ]

            faces = [f_top, f_right, f_left]

            for face, st in zip(faces, styles):
                ax.add_patch(
                    Polygon(
                        face,
                        closed=True,
                        edgecolor="black",
                        linewidth=0.9,
                        **st,
                    )
                )

    # Potong tampilan pas di tengah
    pad = 34.0
    ax.set_xlim(center_x - pad, center_x + pad)
    ax.set_ylim(center_y - pad, center_y + pad)

    save(
        fig,
        "abstract grid tessellation rhombille face scale checker invert pattern black white texture",
    )


if __name__ == "__main__":
    draw()