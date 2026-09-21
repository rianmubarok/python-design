import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon, Arc, Rectangle
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
    """Octagon-square grid fused with connected Wang pipe elbow joints."""
    fig, ax = setup_ax()

    step = 10.0
    # Radius oktagon agar bersinggungan membentuk kisi persegi-oktagon
    r_oct = step / (2 * np.cos(np.pi / 8))

    n_rows, n_cols = 10, 10
    center_x = (n_cols - 1) * step / 2.0
    center_y = (n_rows - 1) * step / 2.0

    for r in range(n_rows):
        for c in range(n_cols):
            cx, cy = c * step, r * step

            # 1. Oktagon Luar & Dalam (Struktur Node)
            ax.add_patch(
                RegularPolygon(
                    (cx, cy),
                    8,
                    radius=r_oct,
                    orientation=np.pi / 8,
                    fill=False,
                    edgecolor="black",
                    linewidth=1.2,
                    zorder=1,
                )
            )
            ax.add_patch(
                RegularPolygon(
                    (cx, cy),
                    8,
                    radius=r_oct * 0.55,
                    orientation=np.pi / 8,
                    fill=False,
                    edgecolor="black",
                    linewidth=0.6,
                    zorder=1,
                )
            )

            # 2. Pipa Wang Tiles (Jalur Siku & Lurus Terhubung Presisi)
            lw = 1.8 + 0.6 * np.sin(c * 0.6 + r * 0.4)

            # Pola sambungan pipa selang-seling (Wang tile elbows)
            tile_type = (r + c) % 4

            if tile_type == 0:
                # Siku Kiri-Bawah ke Kanan-Atas
                ax.add_patch(
                    Arc(
                        (cx + step / 2, cy + step / 2),
                        step,
                        step,
                        theta1=180,
                        theta2=270,
                        color="black",
                        linewidth=lw,
                        zorder=2,
                    )
                )
                ax.add_patch(
                    Arc(
                        (cx - step / 2, cy - step / 2),
                        step,
                        step,
                        theta1=0,
                        theta2=90,
                        color="black",
                        linewidth=lw,
                        zorder=2,
                    )
                )
            elif tile_type == 1:
                # Garis Lurus Horizontal & Vertikal (Persilangan)
                ax.plot(
                    [cx - step / 2, cx + step / 2],
                    [cy, cy],
                    color="black",
                    linewidth=lw,
                    zorder=2,
                )
                ax.plot(
                    [cx, cx],
                    [cy - step / 2, cy + step / 2],
                    color="black",
                    linewidth=lw,
                    zorder=2,
                )
            elif tile_type == 2:
                # Siku Kiri-Atas ke Kanan-Bawah
                ax.add_patch(
                    Arc(
                        (cx - step / 2, cy + step / 2),
                        step,
                        step,
                        theta1=270,
                        theta2=360,
                        color="black",
                        linewidth=lw,
                        zorder=2,
                    )
                )
                ax.add_patch(
                    Arc(
                        (cx + step / 2, cy - step / 2),
                        step,
                        step,
                        theta1=90,
                        theta2=180,
                        color="black",
                        linewidth=lw,
                        zorder=2,
                    )
                )
            else:
                # Koneksi Persegi Kecil di Persimpangan
                sq_w = step * 0.35
                ax.add_patch(
                    Rectangle(
                        (cx - sq_w / 2, cy - sq_w / 2),
                        sq_w,
                        sq_w,
                        fill=False,
                        edgecolor="black",
                        linewidth=lw,
                        zorder=2,
                    )
                )

    # Menyesuaikan batas tampilan agar simetris di tengah
    pad = 38.0
    ax.set_xlim(center_x - pad, center_x + pad)
    ax.set_ylim(center_y - pad, center_y + pad)

    save(
        fig,
        "abstract grid tessellation octagon wang pipe joint fusion pattern black white texture",
    )


if __name__ == "__main__":
    draw()