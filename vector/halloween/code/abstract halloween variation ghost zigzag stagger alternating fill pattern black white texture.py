from datetime import datetime
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import PathPatch, Ellipse, Polygon
from matplotlib.path import Path as MPath
import matplotlib

matplotlib.use("Agg")

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


def draw_ghost(ax, cx, cy, s, fill="black", inv="white"):
    """Menggambar hantu mulus satu vektor tanpa garis celah di tengah."""
    # 1. Kontur Luar Badan Hantu
    t_head = np.linspace(np.pi / 2, 0, 20)
    x_head = cx + (s * 0.28) * np.cos(t_head)
    y_head = cy + (s * 0.25) + (s * 0.28) * np.sin(t_head)

    x_body_r = np.array([cx + s * 0.28, cx + s * 0.35, cx + s * 0.38])
    y_body_r = np.array([cy + s * 0.25, cy, cy - s * 0.30])

    x_wave = np.linspace(cx + s * 0.38, cx - s * 0.38, 50)
    y_wave = (cy - s * 0.30) + (s * 0.06) * np.sin((x_wave - cx) / (s * 0.38) * 2.5 * np.pi)

    x_body_l = np.array([cx - s * 0.38, cx - s * 0.35, cx - s * 0.28])
    y_body_l = np.array([cy - s * 0.30, cy, cy + s * 0.25])

    t_head_l = np.linspace(np.pi, np.pi / 2, 20)
    x_head_l = cx + (s * 0.28) * np.cos(t_head_l)
    y_head_l = cy + (s * 0.25) + (s * 0.28) * np.sin(t_head_l)

    pts_x = np.concatenate([x_head, x_body_r, x_wave, x_body_l, x_head_l])
    pts_y = np.concatenate([y_head, y_body_r, y_wave, y_body_l, y_head_l])
    pts = np.column_stack([pts_x, pts_y])

    codes = [MPath.MOVETO] + [MPath.LINETO] * (len(pts) - 2) + [MPath.CLOSEPOLY]
    path = MPath(pts, codes)

    # Render Badan Hantu
    edge_color = "black" if fill == "white" else "none"
    ax.add_patch(PathPatch(path, facecolor=fill, edgecolor=edge_color, linewidth=1.2, zorder=2))

    # 2. Mata & Mulut
    for ex in (-s * 0.10, s * 0.10):
        ax.add_patch(Ellipse((cx + ex, cy + s * 0.25), s * 0.08, s * 0.12,
                             facecolor=inv, edgecolor="none", zorder=3))
        
    ax.add_patch(Ellipse((cx, cy + s * 0.10), s * 0.07, s * 0.10,
                         facecolor=inv, edgecolor="none", zorder=3))


def draw():
    """Pola zig-zag hantu berselang-seling hitam-putih pada grid simetris."""
    fig, ax = setup_ax()
    cols, rows = 6, 8
    dx, dy = PERIOD / cols, PERIOD / rows
    s = min(dx, dy) * 0.75

    # 1. Latar Belakang Selang-Seling Baris (Stripes) agar Hantu Putih Kontras
    for row in range(rows):
        bg = "black" if row % 2 != 0 else "white"
        if bg == "black":
            rect = Polygon([[0, row * dy], [PERIOD, row * dy],
                            [PERIOD, (row + 1) * dy], [0, (row + 1) * dy]],
                           closed=True, facecolor="black", edgecolor="none", zorder=1)
            ax.add_patch(rect)

    # 2. Menggambar Hantu
    for row in range(rows):
        shift = (dx * 0.5) if row % 2 else 0.0
        fill = "black" if row % 2 == 0 else "white"
        inv = "white" if fill == "black" else "black"

        for col in range(cols):
            cx = (col + 0.5) * dx + shift
            cy = (row + 0.5) * dy

            for ox, oy in WRAPS:
                px, py = cx + ox, cy + oy
                if -15 <= px <= PERIOD + 15 and -15 <= py <= PERIOD + 15:
                    draw_ghost(ax, px, py, s, fill=fill, inv=inv)

    save(fig, "abstract halloween variation ghost zigzag stagger alternating fill pattern black white texture")


if __name__ == "__main__":
    draw()