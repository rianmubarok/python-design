import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime

SIZE = 4000
DPI = 300
SEED = 42
DATE = datetime.now().strftime("%d%m%Y")

JPG_DIR = Path("output/jpg")
SVG_DIR = Path("output/svg")
JPG_DIR.mkdir(parents=True, exist_ok=True)
SVG_DIR.mkdir(parents=True, exist_ok=True)

np.random.seed(SEED)


def setup_ax():
    fig, ax = plt.subplots(figsize=(SIZE/DPI, SIZE/DPI), dpi=DPI)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.set_facecolor("white")
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def save(fig, name):
    jpg_path = JPG_DIR / f"{name}_{DATE}.jpg"
    svg_path = SVG_DIR / f"{name}_{DATE}.svg"
    fig.savefig(jpg_path, dpi=DPI, pad_inches=0, facecolor="white")
    fig.savefig(svg_path, format="svg", pad_inches=0, facecolor="white")
    plt.close(fig)
    print(f"Tersimpan: {jpg_path} | {svg_path}")


def nested_rotating_squares_offset_spiral():
    """Kotak bersarang dengan posisi berpindah secara spiral dari pusat."""
    fig, ax = setup_ax()
    
    n_squares = 35
    center_x, center_y = 50, 50
    
    min_x, max_x = float("inf"), float("-inf")
    min_y, max_y = float("inf"), float("-inf")
    
    for i in range(n_squares):
        # Ukuran bertambah secara progresif
        size = 1.5 + i * 2.0
        
        # Rotasi bertambah secara progresif
        angle = i * 7
        
        # Perpindahan posisi pusat secara spiral
        spiral_radius = i * 0.8
        spiral_angle = np.radians(i * 15)
        
        # Pusat yang berpindah
        cx = center_x + spiral_radius * np.cos(spiral_angle)
        cy = center_y + spiral_radius * np.sin(spiral_angle)
        
        rad = np.radians(angle)
        corners = [(-1, -1), (1, -1), (1, 1), (-1, 1)]
        xs = []
        ys = []
        
        for dx, dy in corners:
            rx = dx * size * np.cos(rad) - dy * size * np.sin(rad)
            ry = dx * size * np.sin(rad) + dy * size * np.cos(rad)
            xs.append(cx + rx)
            ys.append(cy + ry)
        
        xs.append(xs[0])
        ys.append(ys[0])
        
        # Melacak bounding box untuk framing
        min_x, max_x = min(min_x, min(xs)), max(max_x, max(xs))
        min_y, max_y = min(min_y, min(ys)), max(max_y, max(ys))
        
        # Ketebalan garis bervariasi
        lw = 0.8 + 1.8 * (i / n_squares)
        alpha = 0.9 - 0.3 * (i / n_squares)
        
        ax.plot(xs, ys, color="black", linewidth=lw, alpha=alpha)
        
        # Tambahkan titik pusat untuk setiap kotak
        ax.plot(cx, cy, marker="o", markersize=0.8, color="black", alpha=0.6)
    
    # Framing dinamis berdasarkan bounding box aktual
    cx_final = (min_x + max_x) / 2.0
    cy_final = (min_y + max_y) / 2.0
    w = max_x - min_x
    h = max_y - min_y
    pad = max(w, h) / 2.0 + 3.0
    
    ax.set_xlim(cx_final - pad, cx_final + pad)
    ax.set_ylim(cy_final - pad, cy_final + pad)
    
    save(fig, "nested_rotating_squares_offset_spiral")


if __name__ == "__main__":
    nested_rotating_squares_offset_spiral()