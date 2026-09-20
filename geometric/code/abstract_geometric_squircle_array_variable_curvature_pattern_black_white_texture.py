import numpy as np
import matplotlib.pyplot as plt
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


def squircle_array_variable_curvature():
    """Array squircles dengan kelengkungan variabel dari kotak hingga lingkaran."""
    fig, ax = setup_ax()
    
    n_cols = 8
    n_rows = 8
    dx = 100 / n_cols
    dy = 100 / n_rows
    t_vals = np.linspace(0, 2 * np.pi, 200)
    
    min_x, max_x = float("inf"), float("-inf")
    min_y, max_y = float("inf"), float("-inf")
    
    for r in range(n_rows):
        for c in range(n_cols):
            cx = (c + 0.5) * dx
            cy = (r + 0.5) * dy
            
            # Ukuran dasar
            r_base = dx * 0.4
            
            # Eksponen squircle bervariasi dari baris ke baris
            # Baris atas: hampir kotak (p tinggi)
            # Baris bawah: hampir lingkaran (p mendekati 2)
            p = 8.0 - 6.0 * (r / (n_rows - 1))
            p = max(2.1, min(8.0, p))
            
            cos_t = np.cos(t_vals)
            sin_t = np.sin(t_vals)
            
            x = cx + r_base * np.sign(cos_t) * (np.abs(cos_t) ** (2 / p))
            y = cy + r_base * np.sign(sin_t) * (np.abs(sin_t) ** (2 / p))
            
            # Ketebalan garis berdasarkan kelengkungan
            # Lebih tebal untuk bentuk lebih kotak
            lw = 0.8 + 1.2 * ((p - 2.0) / 6.0)
            
            # Alpha berdasarkan posisi grid
            alpha = 0.7 + 0.2 * ((c + r) % 2)
            
            ax.plot(x, y, color="black", linewidth=lw, alpha=alpha)
            
            # Melacak bounding box
            min_x, max_x = min(min_x, x.min()), max(max_x, x.max())
            min_y, max_y = min(min_y, y.min()), max(max_y, y.max())
            
            # Tambahkan titik pusat dengan ukuran berdasarkan kelengkungan
            marker_size = 1.0 if p > 5 else 1.5
            ax.plot(cx, cy, marker="o", markersize=marker_size, 
                    color="black", alpha=0.6)
    
    # Framing dinamis berdasarkan bounding box
    cx_final = (min_x + max_x) / 2.0
    cy_final = (min_y + max_y) / 2.0
    w = max_x - min_x
    h = max_y - min_y
    pad = max(w, h) / 2.0 + 3.0
    
    ax.set_xlim(cx_final - pad, cx_final + pad)
    ax.set_ylim(cy_final - pad, cy_final + pad)
    
    save(fig, "squircle array variable curvature")


if __name__ == "__main__":
    squircle_array_variable_curvature()