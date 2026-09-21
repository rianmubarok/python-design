from datetime import datetime
from pathlib import Path
from matplotlib.patches import FancyBboxPatch
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


def fit_view(ax, pad=40):
    """Memfokuskan tampilan simetris tepat di tengah kanvas."""
    ax.set_xlim(50 - pad, 50 + pad)
    ax.set_ylim(50 - pad, 50 + pad)


def draw():
    """Two slightly rotated rounded-square lattices overlaid for a moire grid."""
    fig, ax = setup_ax()

    def lattice(step, rot_deg, rnd, lw, shift):
        # Perluas n agar ubin menutupi seluruh bidang hingga tepi
        n = 15
        ca, sa = np.cos(np.deg2rad(rot_deg)), np.sin(np.deg2rad(rot_deg))
        R = np.array([[ca, -sa], [sa, ca]])

        for r in range(n):
            for c in range(n):
                # Posisi pusat ubin relatif terhadap pusat kanvas (50, 50)
                pos_local = np.array([(c - n / 2 + 0.5) * step, (r - n / 2 + 0.5) * step])
                p = R @ pos_local + np.array([50 + shift[0], 50 + shift[1]])

                # Ukuran kotak dibikin presisi agar garis ubin bersebelahan saling bersentuhan rapat
                box_size = step * 0.98

                ax.add_patch(
                    FancyBboxPatch(
                        (p[0] - box_size / 2, p[1] - box_size / 2),
                        box_size,
                        box_size,
                        boxstyle=f"round,pad=0,rounding_size={rnd}",
                        fill=False,
                        edgecolor="black",
                        linewidth=lw,
                    )
                )

    # Kisi Utama (Dasar)
    lattice(step=7.5, rot_deg=0, rnd=1.2, lw=0.95, shift=(0, 0))

    # Kisi Sekunder (Dirotasi dan digeser sedikit untuk efek Moiré yang kontras)
    lattice(step=7.2, rot_deg=6.5, rnd=1.8, lw=0.65, shift=(0.8, -0.5))

    # Atur area fokus kanvas
    fit_view(ax, pad=38)

    save(
        fig,
        "abstract grid tessellation rounded square offset moire dual lattice pattern black white texture",
    )


if __name__ == "__main__":
    draw()