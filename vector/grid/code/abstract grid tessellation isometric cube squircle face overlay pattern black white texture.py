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
    """Isometric cube grid tessellation with aligned squircle overlays on top faces."""
    fig, ax = setup_ax()

    s = 5.0  # Ukuran dasar rusuk kubus isometrik
    dx = s * np.sqrt(3)
    dy = s * 1.5

    cols, rows = 18, 18

    # Vektor proyeksi isometrik 3D ke 2D
    p1 = np.array([0, s])
    p2 = np.array([s * np.sqrt(3) / 2, s / 2])
    p3 = np.array([s * np.sqrt(3) / 2, -s / 2])
    p4 = np.array([0, -s])
    p5 = np.array([-s * np.sqrt(3) / 2, -s / 2])
    p6 = np.array([-s * np.sqrt(3) / 2, s / 2])

    center_x = (cols - 1) * (dx / 2.0) / 2.0
    center_y = (rows - 1) * dy / 2.0

    for row in range(rows):
        for col in range(cols):
            cx = col * (dx / 2.0)
            cy = row * dy + (dy / 3.0 if col % 2 else 0)

            o = np.array([cx, cy])

            # 1. Muka Atas (Putih dengan pola Squircle)
            ax.add_patch(
                Polygon(
                    o + np.array([[0, 0], p2 - p1, p2, p1]),
                    closed=True,
                    facecolor="white",
                    edgecolor="black",
                    linewidth=1.0,
                    zorder=2,
                )
            )

            # 2. Muka Kanan (Arsir Hatch)
            ax.add_patch(
                Polygon(
                    o + np.array([[0, 0], p2, p3, p3 - p2]),
                    closed=True,
                    facecolor="white",
                    edgecolor="black",
                    linewidth=1.0,
                    hatch="///",
                    zorder=2,
                )
            )

            # 3. Muka Kiri (Hitam Solid)
            ax.add_patch(
                Polygon(
                    o + np.array([[0, 0], p3 - p2, p5, p6]),
                    closed=True,
                    facecolor="black",
                    edgecolor="black",
                    linewidth=1.0,
                    zorder=2,
                )
            )

            # 4. Squircle Aksen terproyeksi di muka atas
            p_val = 1.8 + 1.5 * (0.5 + 0.5 * np.sin((col + row) * 0.4))
            t = np.linspace(0, 2 * np.pi, 60)
            rx, ry = s * 0.32, s * 0.18

            sq_x = rx * np.sign(np.cos(t)) * (np.abs(np.cos(t)) ** (2 / p_val))
            sq_y = ry * np.sign(np.sin(t)) * (np.abs(np.sin(t)) ** (2 / p_val))

            # Posisi di tengah muka atas kubus
            sq_cx = cx
            sq_cy = cy + s * 0.5

            ax.plot(
                sq_cx + sq_x,
                sq_cy + sq_y,
                color="black",
                linewidth=0.8,
                zorder=3,
            )

    # Tangkapan area tengah simetris penuh
    pad = 35.0
    ax.set_xlim(center_x - pad, center_x + pad)
    ax.set_ylim(center_y - pad, center_y + pad)

    save(
        fig,
        "abstract grid tessellation isometric cube squircle face overlay pattern black white texture",
    )


if __name__ == "__main__":
    draw()