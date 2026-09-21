import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
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
    """True Apollonian packing nested in a symmetric hexagonal lattice grid."""
    fig, ax = setup_ax()
    
    r_outer = 8.0
    dx = r_outer * np.sqrt(3)
    dy = r_outer * 1.5

    n_rows = 12
    n_cols = 12

    # Hitung pusat kanvas agar teselasi simetris penuh
    center_x = (n_cols - 1) * dx / 2.0
    center_y = (n_rows - 1) * dy / 2.0

    for row in range(n_rows):
        for col in range(n_cols):
            cx = col * dx + (dx / 2.0 if row % 2 else 0.0)
            cy = row * dy

            # 1. Lingkaran luar kisi
            ax.add_patch(Circle((cx, cy), r_outer, fill=False, edgecolor="black", linewidth=1.1, zorder=1))

            # 2. Lingkaran dalam dengan variasi modulasi halus
            r_inner = r_outer * (0.35 + 0.12 * np.sin(col * 0.6 + row * 0.4))
            ax.add_patch(Circle((cx, cy), r_inner, fill=False, edgecolor="black", linewidth=0.8, zorder=2))

            # 3. Apollonian Tangent Circles (Satelit bersentuhan presisi)
            # Radius lingkaran satelit agar tepat bersentuhan antara r_outer dan r_inner
            r_sat = (r_outer - r_inner) / 2.0
            r_pos = r_inner + r_sat

            n_sat = 6
            phase = (col + row) * 0.1  # Variasi rotasi halus

            for k in range(n_sat):
                angle = k * (2 * np.pi / n_sat) + phase
                px = cx + r_pos * np.cos(angle)
                py = cy + r_pos * np.sin(angle)

                # Satelit Utama
                ax.add_patch(Circle((px, py), r_sat, fill=False, edgecolor="black", linewidth=0.6, zorder=3))

                # Micro-Apollonian inner circle
                r_micro = r_sat * 0.38
                ax.add_patch(Circle((px, py), r_micro, fill=False, edgecolor="black", linewidth=0.4, zorder=4))

    # Atur batas tampilan presisi simetris di tengah
    pad = 38.0
    ax.set_xlim(center_x - pad, center_x + pad)
    ax.set_ylim(center_y - pad, center_y + pad)

    save(fig, "abstract grid tessellation apollonian packing hex lattice overlay pattern black white texture")


if __name__ == "__main__":
    draw()