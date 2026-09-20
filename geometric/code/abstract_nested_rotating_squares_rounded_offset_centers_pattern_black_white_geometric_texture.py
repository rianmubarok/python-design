import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib.transforms import Affine2D
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
    jpg_path = JPG_DIR / f"{name}_{DATE}.jpg"
    svg_path = SVG_DIR / f"{name}_{DATE}.svg"
    fig.savefig(jpg_path, dpi=DPI, pad_inches=0, facecolor="white")
    fig.savefig(svg_path, format="svg", pad_inches=0, facecolor="white")
    plt.close(fig)
    print(f"Tersimpan: {jpg_path} | {svg_path}")


def nested_rotating_squares_rounded_offset_centers():
    """Kotak bersarang dengan sudut membulat dan pusat yang berpindah secara dinamis."""
    fig, ax = setup_ax()
    
    n_squares = 28
    main_center_x, main_center_y = 50, 50
    
    min_x, max_x = float("inf"), float("-inf")
    min_y, max_y = float("inf"), float("-inf")
    
    for i in range(n_squares):
        t = i / (n_squares - 1)
        
        # Ukuran bertambah
        s = 1.5 + i * 1.4
        
        # Radius sudut membesar secara progresif
        r = 0.6 * s * t
        
        # Pusat yang berpindah secara sinusoidal
        offset_x = 8 * np.sin(i * 0.3) * (1 - t)
        offset_y = 6 * np.cos(i * 0.25) * (1 - t)
        
        cx = main_center_x + offset_x
        cy = main_center_y + offset_y
        
        # Rotasi bertambah
        rotation_angle = i * 6.5
        
        # Transformasi: translasi + rotasi
        tr = (Affine2D()
              .translate(cx - main_center_x, cy - main_center_y)
              .rotate_deg_around(main_center_x, main_center_y, rotation_angle)
              + ax.transData)
        
        # Buat kotak dengan sudut membulat
        box = FancyBboxPatch(
            (main_center_x - s, main_center_y - s),
            s * 2,
            s * 2,
            boxstyle=f"round,pad=0,rounding_size={r}",
            fill=False,
            edgecolor="black",
            linewidth=0.8 + 2.2 * t,
            transform=tr,
        )
        ax.add_patch(box)
        
        # Hitung bounding box untuk framing
        corners = [
            (main_center_x - s, main_center_y - s),
            (main_center_x + s, main_center_y - s),
            (main_center_x + s, main_center_y + s),
            (main_center_x - s, main_center_y + s)
        ]
        
        # Terapkan transformasi ke sudut
        for corner_x, corner_y in corners:
            # Terapkan rotasi
            rad = np.radians(rotation_angle)
            rx = (corner_x - main_center_x) * np.cos(rad) - (corner_y - main_center_y) * np.sin(rad)
            ry = (corner_x - main_center_x) * np.sin(rad) + (corner_y - main_center_y) * np.cos(rad)
            
            # Terapkan translasi
            final_x = main_center_x + rx + offset_x
            final_y = main_center_y + ry + offset_y
            
            min_x, max_x = min(min_x, final_x), max(max_x, final_x)
            min_y, max_y = min(min_y, final_y), max(max_y, final_y)
    
    # Framing dinamis berdasarkan bounding box aktual
    cx_final = (min_x + max_x) / 2.0
    cy_final = (min_y + max_y) / 2.0
    w = max_x - min_x
    h = max_y - min_y
    pad = max(w, h) / 2.0 + 4.0
    
    ax.set_xlim(cx_final - pad, cx_final + pad)
    ax.set_ylim(cy_final - pad, cy_final + pad)
    
    save(fig, "nested_rotating_squares_rounded_offset_centers")


if __name__ == "__main__":
    nested_rotating_squares_rounded_offset_centers()