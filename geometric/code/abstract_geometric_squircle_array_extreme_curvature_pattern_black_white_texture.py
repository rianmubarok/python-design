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


def squircle_array_extreme_curvature():
    """Array squircles dengan kelengkungan ekstrem dari sangat tajam hingga sangat bulat."""
    fig, ax = setup_ax()
    
    n_cols = 10
    n_rows = 10
    dx = 100 / n_cols
    dy = 100 / n_rows
    t_vals = np.linspace(0, 2 * np.pi, 300)  # Lebih banyak titik untuk presisi
    
    min_x, max_x = float("inf"), float("-inf")
    min_y, max_y = float("inf"), float("-inf")
    
    for r in range(n_rows):
        for c in range(n_cols):
            cx = (c + 0.5) * dx
            cy = (r + 0.5) * dy
            
            # Ukuran dengan variasi diagonal
            size_factor = 0.35 + 0.1 * np.sin((c + r) * 0.3)
            r_base = dx * 0.35 * size_factor
            
            # Eksponen squircle bervariasi secara diagonal
            # Dari kiri atas (sangat kotak) ke kanan bawah (sangat bulat)
            diagonal_progress = (c + r) / (n_cols + n_rows - 2)
            
            # Rentang eksponen yang ekstrem: 20 (sangat kotak) hingga 2.01 (sangat bulat)
            p = 20.0 - 18.0 * diagonal_progress
            p = max(2.01, min(20.0, p))
            
            # Faktor penguatan kurva untuk efek yang lebih dramatis
            curve_intensity = 1.0 + 2.0 * diagonal_progress
            
            cos_t = np.cos(t_vals)
            sin_t = np.sin(t_vals)
            
            # Rumus squircle dengan modifikasi untuk efek ekstrem
            x_power = (2 / p) * curve_intensity
            y_power = (2 / p) * curve_intensity
            
            x = cx + r_base * np.sign(cos_t) * (np.abs(cos_t) ** x_power)
            y = cy + r_base * np.sign(sin_t) * (np.abs(sin_t) ** y_power)
            
            # Ketebalan garis berdasarkan kelengkungan
            # Garis lebih tebal untuk bentuk lebih kotak
            lw = 0.6 + 1.8 * (1.0 - diagonal_progress)
            
            # Warna dengan variasi alpha untuk efek kedalaman
            alpha = 0.6 + 0.3 * (1.0 - abs(diagonal_progress - 0.5))
            
            ax.plot(x, y, color="black", linewidth=lw, alpha=alpha)
            
            # Melacak bounding box
            min_x, max_x = min(min_x, x.min()), max(max_x, x.max())
            min_y, max_y = min(min_y, y.min()), max(max_y, y.max())
            
            # Tambahkan detail interior berdasarkan kelengkungan
            if diagonal_progress < 0.3:  # Bentuk kotak
                # Tambahkan garis diagonal untuk kotak
                inner_size = r_base * 0.4
                ax.plot([cx - inner_size, cx + inner_size], 
                        [cy - inner_size, cy + inner_size], 
                        color="black", linewidth=0.3, alpha=0.5)
                ax.plot([cx - inner_size, cx + inner_size], 
                        [cy + inner_size, cy - inner_size], 
                        color="black", linewidth=0.3, alpha=0.5)
            elif diagonal_progress > 0.7:  # Bentuk bulat
                # Tambahkan lingkaran dalam untuk bentuk bulat
                inner_circle = plt.Circle((cx, cy), r_base * 0.3, 
                                         fill=False, linewidth=0.4, 
                                         edgecolor="black", alpha=0.4)
                ax.add_patch(inner_circle)
    
    # Framing dengan padding yang sesuai
    cx_final = (min_x + max_x) / 2.0
    cy_final = (min_y + max_y) / 2.0
    w = max_x - min_x
    h = max_y - min_y
    pad = max(w, h) / 2.0 + 2.0
    
    ax.set_xlim(cx_final - pad, cx_final + pad)
    ax.set_ylim(cy_final - pad, cy_final + pad)
    
    save(fig, "squircle array extreme curvature")


if __name__ == "__main__":
    squircle_array_extreme_curvature()