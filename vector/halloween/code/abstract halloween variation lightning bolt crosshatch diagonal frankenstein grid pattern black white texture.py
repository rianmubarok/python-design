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


def lightning_bolt(ax, cx, cy, h, w, angle_deg=45.0, fill="white", stroke="black"):
    """Bentuk kilat petir zig-zag klasik tanpa potongan melintang."""
    a = np.radians(angle_deg)
    c, s_ = np.cos(a), np.sin(a)
    
    # Urutan titik searah jarum jam agar poligon solid dan tidak menyilang
    pts_local = np.array([
        [ 0.10 * w,   0.50 * h],  # 1. Puncak atas
        [ 0.00 * w,   0.05 * h],  # 2. Siku dalam kanan
        [ 0.35 * w,   0.05 * h],  # 3. Siku luar kanan
        [-0.10 * w,  -0.50 * h],  # 4. Ujung bawah runcing
        [ 0.00 * w,  -0.05 * h],  # 5. Siku dalam kiri
        [-0.35 * w,  -0.05 * h],  # 6. Siku luar kiri
    ])
    
    R = np.array([[c, -s_], [s_, c]])
    pts = (R @ pts_local.T).T + [cx, cy]
    
    ax.add_patch(Polygon(pts, closed=True, facecolor=fill, 
                         edgecolor=stroke if stroke else "none", 
                         linewidth=1.2 if stroke else 0))


def draw():
    """Crosshatch petir yang padat, proporsional, dan tegas."""
    fig, ax = setup_ax()

    cols = 5
    rows = 5
    dx = PERIOD / cols
    dy = PERIOD / rows
    
    bh = min(dx, dy) * 1.10
    bw = min(dx, dy) * 0.50

    # Grid Utama
    for row in range(rows):
        for col in range(cols):
            cx = (col + 0.5) * dx
            cy = (row + 0.5) * dy
            for ox, oy in WRAPS:
                # Petir +45°
                lightning_bolt(ax, cx + ox, cy + oy, bh, bw,
                               angle_deg=45, fill="white", stroke="black")
                # Petir -45° bersilangan
                lightning_bolt(ax, cx + ox, cy + oy, bh * 0.85, bw * 0.85,
                               angle_deg=-45, fill="white", stroke="black")

    # Grid Sekunder Offset (Di tengah antar sel)
    for row in range(rows):
        for col in range(cols):
            cx = (col + 1.0) * dx
            cy = (row + 1.0) * dy
            for ox, oy in WRAPS:
                lightning_bolt(ax, cx + ox, cy + oy, bh * 0.65, bw * 0.65,
                               angle_deg=45, fill="white", stroke="black")
                lightning_bolt(ax, cx + ox, cy + oy, bh * 0.65, bw * 0.65,
                               angle_deg=-45, fill="white", stroke="black")

    save(fig, "abstract halloween variation lightning bolt crosshatch diagonal frankenstein grid pattern black white texture")


if __name__ == "__main__":
    draw()