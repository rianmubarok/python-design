import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from pathlib import Path
from datetime import datetime

SIZE = 4000
DPI = 300
PERIOD = 100.0
DATE = datetime.now().strftime("%d%m%Y")
WRAPS = [(i * PERIOD, j * PERIOD) for i in (-1, 0, 1) for j in (-1, 0, 1)]

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR.parent / "output"
JPG_DIR = OUTPUT_DIR / "jpg"
SVG_DIR = OUTPUT_DIR / "svg"
JPG_DIR.mkdir(parents=True, exist_ok=True)
SVG_DIR.mkdir(parents=True, exist_ok=True)


def setup_ax():
    fig, ax = plt.subplots(figsize=(SIZE / DPI, SIZE / DPI), dpi=DPI)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.set_facecolor("black")
    ax.set_xlim(0, PERIOD)
    ax.set_ylim(0, PERIOD)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def save(fig, name):
    jpg_path = JPG_DIR / f"{name} {DATE}.jpg"
    svg_path = SVG_DIR / f"{name} {DATE}.svg"
    fig.savefig(jpg_path, dpi=DPI, pad_inches=0, facecolor="black")
    fig.savefig(svg_path, format="svg", pad_inches=0, facecolor="black")
    plt.close(fig)
    print(f"Saved: {jpg_path} | {svg_path}")


def draw_crescent_shape(ax, cx, cy, r_outer, tilt):
    """Menggambar 1 bentuk bulan sabit murni dengan dua ujung runcing yang mulus."""
    n_pts = 200
    offset_dist = r_outer * 0.40
    
    # Busur Luar (lingkaran utama)
    theta_outer = np.linspace(-np.pi * 0.60, np.pi * 0.60, n_pts)
    outer_x = cx + r_outer * np.cos(theta_outer)
    outer_y = cy + r_outer * np.sin(theta_outer)
    
    # Titik pusat lingkaran dalam yang di-offset
    punch_cx = cx + offset_dist
    punch_cy = cy
    
    # Hitung sudut agar busur dalam menyambung tepat di ujung busur luar
    p1 = (outer_x[-1] - punch_cx, outer_y[-1] - punch_cy)
    p2 = (outer_x[0] - punch_cx, outer_y[0] - punch_cy)
    
    angle1 = np.arctan2(p1[1], p1[0])
    angle2 = np.arctan2(p2[1], p2[0])
    
    theta_inner = np.linspace(angle1, angle2, n_pts)
    r_inner_calc = np.hypot(p1[0], p1[1])
    
    inner_x = punch_cx + r_inner_calc * np.cos(theta_inner)
    inner_y = punch_cy + r_inner_calc * np.sin(theta_inner)
    
    # Gabungkan dan putar sesuai variabel tilt
    pts_x = np.concatenate([outer_x, inner_x]) - cx
    pts_y = np.concatenate([outer_y, inner_y]) - cy
    
    rot_x = pts_x * np.cos(tilt) - pts_y * np.sin(tilt) + cx
    rot_y = pts_x * np.sin(tilt) + pts_y * np.cos(tilt) + cy
    
    pts = np.column_stack([rot_x, rot_y])
    ax.add_patch(Polygon(pts, closed=True, facecolor="white", edgecolor="none"))


def concentric_crescents(ax, cx, cy, max_r, n=4, tilt=0.0):
    """Stack bulan sabit konsentris yang di-offset secara seimbang dari luar ke dalam."""
    for i in range(n):
        scale = (n - i) / n
        r_outer = max_r * scale
        
        # Geser titik pusat lapisan yang lebih kecil sedikit ke arah dalam agar seimbang
        shift = (max_r - r_outer) * 0.35
        shift_x = cx + shift * np.cos(tilt)
        shift_y = cy + shift * np.sin(tilt)
        
        draw_crescent_shape(ax, shift_x, shift_y, r_outer, tilt)


def draw():
    """3×4 grid of nested concentric crescent stack tiles."""
    fig, ax = setup_ax()
    cols, rows = 3, 4
    dx, dy = PERIOD / cols, PERIOD / rows
    max_r = min(dx, dy) * 0.38  # Dikurangi sedikit agar memberi ruang antar-ubin

    tilts = [np.radians(t) for t in [20, 340, 50, 310, 15, 345, 40, 320, 60, 300, 25, 335]]
    idx = 0
    for row in range(rows):
        for col in range(cols):
            cx = (col + 0.5) * dx + (dx * 0.5 if row % 2 else 0)
            cy = (row + 0.5) * dy
            tilt = tilts[idx % len(tilts)]
            idx += 1
            for ox, oy in WRAPS:
                concentric_crescents(ax, cx + ox, cy + oy, max_r, n=4, tilt=tilt)

    save(fig, "abstract halloween variation crescent moon nested concentric arcs shrinking pattern black white texture")


if __name__ == "__main__":
    draw()