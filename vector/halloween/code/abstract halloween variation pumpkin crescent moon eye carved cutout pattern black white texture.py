import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, FancyBboxPatch, Circle, Polygon
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
    ax.set_facecolor("white")
    ax.set_xlim(0, PERIOD)
    ax.set_ylim(0, PERIOD)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def save(fig, name):
    jpg_path = JPG_DIR / f"{name} {DATE}.jpg"
    svg_path = SVG_DIR / f"{name} {DATE}.svg"
    fig.savefig(jpg_path, dpi=DPI, pad_inches=0, facecolor="white")
    fig.savefig(svg_path, format="svg", pad_inches=0, facecolor="white")
    plt.close(fig)
    print(f"Saved: {jpg_path} | {svg_path}")


def pumpkin_moon_eyes(ax, cx, cy, s, fill="black"):
    """Pumpkin where each eye is a crescent moon cutout shape."""
    inv = "white" if fill == "black" else "black"
    edge = "black" if fill == "white" else "none"
    lw = 1.2 if fill == "white" else 0.0

    # 1a. Gambar 2 elips samping (kiri & kanan) terlebih dahulu
    for lox in (-s * 0.25, s * 0.25):
        ax.add_patch(Ellipse((cx + lox, cy), s * 0.62, s * 0.80,
                             facecolor=fill, edgecolor=edge, linewidth=lw))

    # 1b. Gambar elips tengah PALING ATAS agar garis batasnya tidak tertutup
    ax.add_patch(Ellipse((cx, cy), s * 0.62, s * 0.80,
                         facecolor=fill, edgecolor=edge, linewidth=lw))

    # 2. Tangkai labu
    ax.add_patch(FancyBboxPatch(
        (cx - s * 0.06, cy + s * 0.38), s * 0.12, s * 0.20,
        boxstyle=f"round,pad=0,rounding_size={s*0.04:.4f}",
        facecolor=fill, edgecolor=edge, linewidth=lw))

    # 3. Mata bulan sabit (Crescent Moon Eyes)
    eye_r = s * 0.13
    for ex in (-s * 0.24, s * 0.24):
        # Lingkaran luar mata
        ax.add_patch(Circle((cx + ex, cy + s * 0.18), eye_r,
                            facecolor=inv, edgecolor="none"))
        # Pemotong lingkaran dalam untuk membentuk bulan sabit
        ax.add_patch(Circle((cx + ex + eye_r * 0.45, cy + s * 0.18),
                            eye_r * 0.75, facecolor=fill, edgecolor="none"))

    # 4. Hidung segitiga
    ax.add_patch(Polygon(
        np.array([[cx, cy + s * 0.02],
                  [cx - s * 0.07, cy - s * 0.09],
                  [cx + s * 0.07, cy - s * 0.09]]),
        closed=True, facecolor=inv, edgecolor="none"))

    # 5. Mulut bergerigi
    teeth_x = np.linspace(cx - s * 0.28, cx + s * 0.28, 9)
    mouth_y_top = cy - s * 0.12
    mouth_y_bot = cy - s * 0.26
    m_pts = [(teeth_x[0], mouth_y_top)]
    for i, x in enumerate(teeth_x):
        m_pts.append((x, mouth_y_bot if i % 2 == 0 else mouth_y_top))
    m_pts.append((teeth_x[-1], mouth_y_top))
    ax.add_patch(Polygon(m_pts, closed=True, facecolor=inv, edgecolor="none"))


def draw():
    """5×5 staggered grid of pumpkins with crescent-moon-shaped eye cutouts."""
    fig, ax = setup_ax()
    cols, rows = 5, 5
    dx, dy = PERIOD / cols, PERIOD / rows
    s = min(dx, dy) * 0.78

    for row in range(rows):
        for col in range(cols):
            cx = (col + 0.5) * dx + (dx * 0.5 if row % 2 else 0)
            cy = (row + 0.5) * dy
            fill = "black" if (row + col) % 2 == 0 else "white"
            for ox, oy in WRAPS:
                pumpkin_moon_eyes(ax, cx + ox, cy + oy, s, fill=fill)

    save(fig, "abstract halloween variation pumpkin crescent moon eye carved cutout pattern black white texture")


if __name__ == "__main__":
    draw()