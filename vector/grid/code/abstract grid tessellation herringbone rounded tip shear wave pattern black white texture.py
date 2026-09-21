import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib.transforms import Affine2D
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
    """Herringbone bars with rounded caps and a sinusoidal shear wave offset."""
    fig, ax = setup_ax()

    # Proporsi kapsul disesuaikan agar saling mengunci pas (Herringbone grid)
    length, width = 11.2, 3.2
    step_x = 5.6
    step_y = 5.6

    n_rows = 20
    n_cols = 20

    # Pusat tampilan simetris
    center_x = (n_cols - 1) * step_x / 2.0
    center_y = (n_rows - 1) * step_y / 2.0

    for row in range(n_rows):
        for col in range(n_cols):
            # Gelombang pergeseran sinusoidal
            shear = 2.2 * np.sin(row * 0.4 + col * 0.2)
            
            cx = col * step_x + shear
            cy = row * step_y + (step_y * 0.5 if col % 2 else 0)

            # Sudut anyaman herringbone 45 vs -45 derajat
            ang = 45 if col % 2 == 0 else -45

            # Morphing kelengkungan sudut
            rnd = 0.4 + 0.8 * (0.5 + 0.5 * np.sin(col * 0.5 + row * 0.3))

            # Elemen Kapsul Utama (Garis Luar)
            patch_outer = FancyBboxPatch(
                (-length / 2, -width / 2),
                length,
                width,
                boxstyle=f"round,pad=0,rounding_size={rnd:.2f}",
                fill=False,
                edgecolor="black",
                linewidth=1.0,
                transform=Affine2D().rotate_deg(ang).translate(cx, cy) + ax.transData,
                zorder=2,
            )
            ax.add_patch(patch_outer)

            # Elemen Inti Dalam (Aksen Tekstur)
            patch_inner = FancyBboxPatch(
                (-length / 2.8, -width / 4.0),
                length / 1.4,
                width / 2.0,
                boxstyle=f"round,pad=0,rounding_size={rnd * 0.5:.2f}",
                fill=False,
                edgecolor="black",
                linewidth=0.5,
                transform=Affine2D().rotate_deg(ang).translate(cx, cy) + ax.transData,
                zorder=3,
            )
            ax.add_patch(patch_inner)

    # Tangkapan area tengah penuh
    pad = 38.0
    ax.set_xlim(center_x - pad, center_x + pad)
    ax.set_ylim(center_y - pad, center_y + pad)

    save(
        fig,
        "abstract grid tessellation herringbone rounded tip shear wave pattern black white texture",
    )


if __name__ == "__main__":
    draw()