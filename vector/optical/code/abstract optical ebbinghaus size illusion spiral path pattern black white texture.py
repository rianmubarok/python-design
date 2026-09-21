import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from pathlib import Path
from datetime import datetime

SIZE = 4000
DPI = 300
SEED = 42
DATE = datetime.now().strftime("%d%m%Y")

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR.parent / "output"
JPG_DIR = OUTPUT_DIR / "jpg"
SVG_DIR = OUTPUT_DIR / "svg"
JPG_DIR.mkdir(parents=True, exist_ok=True)
SVG_DIR.mkdir(parents=True, exist_ok=True)

np.random.seed(SEED)


def setup_ax():
    fig, ax = plt.subplots(figsize=(SIZE / DPI, SIZE / DPI), dpi=DPI)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.set_facecolor("white")
    ax.set_xlim(-50, 50)
    ax.set_ylim(-50, 50)
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


def generate():
    """Ebbinghaus illusion arranged along a non-overlapping Archimedean spiral."""
    fig, ax = setup_ax()

    n_clusters = 15
    a_spiral = 4.5  # Skala pertumbuhan spiral
    
    # Penentuan nilai theta berbasis deret agar jarak fisik antar-kluster selalu aman
    thetas = []
    curr_theta = 2.2
    for _ in range(n_clusters):
        thetas.append(curr_theta)
        # Tambah theta secara proporsional agar tidak bertabrakan saat r membesar
        curr_theta += 0.85 / (curr_theta ** 0.5)

    thetas = np.array(thetas)
    r_vals = a_spiral * thetas

    for k in range(n_clusters):
        t = thetas[k]
        r = r_vals[k]

        cx = r * np.cos(t)
        cy = r * np.sin(t)

        # 1. Lingkaran Hitam Pusat (Ukuran sama)
        center_r = 1.6
        ax.add_patch(Circle((cx, cy), center_r, facecolor="black", zorder=3))

        # 2. Lingkaran Luar Penjelas (Besar vs Kecil bergantian)
        is_large = k % 2 == 0
        n_outer = 6 if is_large else 8
        
        # Batasi ukuran outer_r agar kluster tetap rapi
        outer_r = 2.1 + (k * 0.08) if is_large else 0.7 + (k * 0.02)
        ring_r = center_r + outer_r + 0.6

        for j in range(n_outer):
            angle = t + j * (2 * np.pi / n_outer)
            ox = cx + ring_r * np.cos(angle)
            oy = cy + ring_r * np.sin(angle)
            
            ax.add_patch(
                Circle(
                    (ox, oy),
                    outer_r,
                    fill=False,
                    edgecolor="black",
                    linewidth=1.2,
                    zorder=2,
                )
            )

    save(
        fig,
        "abstract optical ebbinghaus size illusion spiral path pattern black white texture",
    )


if __name__ == "__main__":
    generate()