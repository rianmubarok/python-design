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
    """True Woven Sine Lattice Tessellation with Integrated Node Rings."""
    fig, ax = setup_ax()

    scale = 8.5
    h_nodes = 14
    v_nodes = 14
    
    # Grid offset agar simetris di tengah
    ox = - (h_nodes - 1) * scale / 2.0
    oy = - (v_nodes - 1) * scale / 2.0

    # 1. Plot Anyaman Jaring Sinus Terintegrasi
    # Transformasi gelombang sinus untuk menyatukan kisi di setiap node persimpangan
    def warp(x, y):
        w = 1.4 * np.sin(x * 0.16) + 1.1 * np.cos(y * 0.2)
        return x, y + w

    for i in range(h_nodes):
        for j in range(v_nodes):
            # Posisi kisi dasar
            cx = i * scale + ox
            cy = j * scale + oy

            # 6 Sudut Heksagon Isometrik (Tessellation Grid)
            v = [
                warp(cx, cy + scale),
                warp(cx + scale * np.sqrt(3)/2, cy + scale/2),
                warp(cx + scale * np.sqrt(3)/2, cy - scale/2),
                warp(cx, cy - scale),
                warp(cx - scale * np.sqrt(3)/2, cy - scale/2),
                warp(cx - scale * np.sqrt(3)/2, cy + scale/2),
            ]
            
            # Pusat Gelombang Anyaman yang Menyatu
            pcx, pcy = warp(cx, cy)

            # Gambar 3 Lengan Anyaman Sinus Utama
            # Lengan Horizontal
            if i < h_nodes - 1:
                ax.plot([pcx, warp(cx+scale, cy)[0]], [pcy, warp(cx+scale, cy)[1]], color="black", linewidth=0.9, zorder=1)

            # Lengan Diagonal Kanan & Kiri
            if j < v_nodes - 1:
                ax.plot([pcx, warp(cx, cy+scale)[0]], [pcy, warp(cx, cy+scale)[1]], color="black", linewidth=0.9, zorder=1)
                if i < h_nodes - 1:
                   # Sambungan antar kolom gelombang
                   ax.plot([warp(cx+scale, cy)[0], warp(cx, cy+scale)[0]], [warp(cx+scale, cy)[1], warp(cx, cy+scale)[1]], color="black", linewidth=0.9, zorder=1)


    # 2. Plot Lingkaran Node Ring Terintegrasi di Pusat Anyaman
    # Digambar di pusat gelombanganyaman 'warp'
    for i in range(h_nodes):
        for j in range(v_nodes):
            cx = i * scale + ox
            cy = j * scale + oy
            
            # Pusat anyaman terdistorsi
            pcx, pcy = warp(cx, cy)

            # Modulasi radius node berdasarkan gelombang sine lapangan
            rad = 1.6 + 0.9 * (0.5 + 0.5 * np.sin(cx * 0.12) * np.cos(cy * 0.15))
            
            # Node Ring Utama & Inti (Nested Circles)
            ax.add_patch(Circle((pcx, pcy), rad, fill=False, edgecolor="black", linewidth=1.1, zorder=2))
            ax.add_patch(Circle((pcx, pcy), rad * 0.5, fill=False, edgecolor="black", linewidth=0.6, zorder=3))

    # Fokus area tengah simetris penuh
    pad = 38.0
    ax.set_xlim(-pad, pad)
    ax.set_ylim(-pad, pad)

    save(
        fig,
        "abstract grid tessellation woven sine lattice node ring pattern black white texture",
    )


if __name__ == "__main__":
    draw()