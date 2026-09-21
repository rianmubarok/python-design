from datetime import datetime
from pathlib import Path
from matplotlib.patches import FancyBboxPatch, RegularPolygon
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


def fit_view(ax, pad=50):
    """Memfokuskan tampilan simetris tepat di tengah kanvas (50, 50)."""
    ax.set_xlim(50 - pad, 50 + pad)
    ax.set_ylim(50 - pad, 50 + pad)


def draw():
    """Octagon-square tiling with twisting octagons and waving square corner radii."""
    fig, ax = setup_ax()
    step = 14.0
    rows, cols = 8, 8

    # Menghitung offset kisi agar titik pusat pola berada tepat di (50, 50)
    grid_size = cols * step
    offset_x = 50.0 - (grid_size / 2.0)
    offset_y = 50.0 - (grid_size / 2.0)

    # Iterasi dari -1 hingga rows+1 untuk memastikan tidak ada celah kosong di tepi
    for r in range(-1, rows + 1):
        for c in range(-1, cols + 1):
            cx = (c + 0.5) * step + offset_x
            cy = (r + 0.5) * step + offset_y

            twist = np.deg2rad(8 * np.sin(c * 0.7) + 8 * np.cos(r * 0.55))
            ro = 5.2 + 0.7 * np.sin(c * 0.4 + r * 0.4)

            # Oktagon Luar
            ax.add_patch(
                RegularPolygon(
                    (cx, cy),
                    numVertices=8,
                    radius=ro,
                    orientation=np.pi / 8 + twist,
                    fill=False,
                    edgecolor="black",
                    linewidth=1.2,
                    zorder=1,
                )
            )

            # Oktagon Dalam
            ax.add_patch(
                RegularPolygon(
                    (cx, cy),
                    numVertices=8,
                    radius=ro * 0.58,
                    orientation=np.pi / 8 - twist,
                    fill=False,
                    edgecolor="black",
                    linewidth=0.6,
                    zorder=2,
                )
            )

            # Persegi Sudut dengan Pembulatan Dinamis (Waving Corner Radius)
            rnd = 0.3 + 1.1 * (0.5 + 0.5 * np.sin(r * 0.8) * np.cos(c * 0.8))
            sw = 4.4
            ax.add_patch(
                FancyBboxPatch(
                    (cx + step / 2 - sw / 2, cy + step / 2 - sw / 2),
                    sw,
                    sw,
                    boxstyle=f"round,pad=0,rounding_size={rnd}",
                    fill=False,
                    edgecolor="black",
                    linewidth=0.9,
                    zorder=3,
                )
            )

    fit_view(ax, pad=50)
    save(
        fig,
        "abstract grid tessellation octagonal square twist radius wave pattern black white texture",
    )


if __name__ == "__main__":
    draw()