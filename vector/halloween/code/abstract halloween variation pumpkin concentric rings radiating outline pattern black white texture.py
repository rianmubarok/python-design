import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, FancyBboxPatch, Polygon
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


def draw_pumpkin_core(ax, cx, cy, s):
    """Labu padat dengan mata dan mulut jack-o'-lantern hitam tegas."""
    # Badan labu (3 lobe putih)
    for lobe_ox in (-s * 0.22, 0, s * 0.22):
        ax.add_patch(Ellipse((cx + lobe_ox, cy), s * 0.56, s * 0.74,
                             facecolor="white", edgecolor="none"))
                             
    # Tangkai labu
    ax.add_patch(FancyBboxPatch(
        (cx - s * 0.055, cy + s * 0.35), s * 0.11, s * 0.17,
        boxstyle=f"round,pad=0,rounding_size={s*0.03:.4f}",
        facecolor="white", edgecolor="none"))

    # Mata segitiga hitam
    eye_l = np.array([
        [cx - s * 0.24, cy + s * 0.14],
        [cx - s * 0.35, cy - s * 0.04],
        [cx - s * 0.13, cy - s * 0.04],
    ])
    ax.add_patch(Polygon(eye_l, closed=True, facecolor="black", edgecolor="none"))
    
    eye_r = eye_l.copy()
    eye_r[:, 0] = cx + (eye_l[:, 0] - cx) * -1
    ax.add_patch(Polygon(eye_r, closed=True, facecolor="black", edgecolor="none"))

    # Mulut bergerigi hitam
    teeth_x = np.linspace(cx - s * 0.28, cx + s * 0.28, 7)
    mouth_y_top = cy - s * 0.10
    mouth_y_bot = cy - s * 0.25
    mouth_pts = [(teeth_x[0], mouth_y_top)]
    for k, x in enumerate(teeth_x):
        mouth_pts.append((x, mouth_y_bot if k % 2 == 0 else mouth_y_top))
    mouth_pts.append((teeth_x[-1], mouth_y_top))
    ax.add_patch(Polygon(mouth_pts, closed=True, facecolor="black", edgecolor="none"))


def draw_pumpkin_radiating_ring(ax, cx, cy, s, lw=0.8, alpha=0.5):
    """Garis luar kontur labu tunggal untuk efek gelombang/aura."""
    # Kontur badan
    for lobe_ox in (-s * 0.22, 0, s * 0.22):
        ax.add_patch(Ellipse((cx + lobe_ox, cy), s * 0.56, s * 0.74,
                             facecolor="none", edgecolor="white",
                             linewidth=lw, alpha=alpha))


def draw():
    """Pola grid labu jack-o'-lantern dengan gelombang aura konsentris yang bersih."""
    fig, ax = setup_ax()
    cols, rows = 4, 4
    dx, dy = PERIOD / cols, PERIOD / rows
    s_core = min(dx, dy) * 0.38

    for row in range(rows):
        for col in range(cols):
            cx = (col + 0.5) * dx
            cy = (row + 0.5) * dy
            for ox, oy in WRAPS:
                # 1. Gambar 5 garis aura gelombang konsentris secara bersih
                for i in range(5, 0, -1):
                    scale = 1.0 + i * 0.25
                    alpha_val = max(0.8 - i * 0.12, 0.2)
                    draw_pumpkin_radiating_ring(ax, cx + ox, cy + oy,
                                               s_core * scale, lw=1.0, alpha=alpha_val)

                # 2. Gambar labu utama berwajah tegas di bagian tengah
                draw_pumpkin_core(ax, cx + ox, cy + oy, s_core)

    save(fig, "abstract halloween variation pumpkin concentric rings radiating outline pattern black white texture")


if __name__ == "__main__":
    draw()