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


def draw_pumpkin(ax, cx, cy, s, fill="white"):
    """Pumpkin silhouette at 45-degree diamond orientation (rotated coords)."""
    inv = "black" if fill == "white" else "white"
    edge = "black" if fill == "white" else "none"
    elw = 0.5 if fill == "white" else 0.0

    # Three lobe ellipses rotated 45 deg — we rotate their centres
    for lx, ly in [(-s * 0.22, 0), (0, 0), (s * 0.22, 0)]:
        # rotate 45 deg
        rx = lx * np.cos(np.pi / 4) - ly * np.sin(np.pi / 4)
        ry = lx * np.sin(np.pi / 4) + ly * np.cos(np.pi / 4)
        # For diamond orientation the lobes run diagonally — use a rotated ellipse
        from matplotlib.patches import Ellipse
        from matplotlib.transforms import Affine2D
        e = Ellipse((cx + rx, cy + ry), s * 0.56, s * 0.74,
                    facecolor=fill, edgecolor=edge, linewidth=elw)
        t = Affine2D().rotate_deg_around(cx + rx, cy + ry, 45) + ax.transData
        e.set_transform(t)
        ax.add_patch(e)

    # Stem — rotated 45 deg offset from body top
    stem_ox = -s * 0.055 * np.cos(np.pi / 4) - s * 0.38 * np.sin(np.pi / 4)
    stem_oy = -s * 0.055 * np.sin(np.pi / 4) + s * 0.38 * np.cos(np.pi / 4)
    ax.add_patch(Ellipse((cx + stem_ox, cy + stem_oy), s * 0.10, s * 0.20,
                         angle=45, facecolor=fill, edgecolor=edge, linewidth=elw))

    # Triangle eyes — rotated 45 deg
    def rot45(pts, ocx, ocy):
        out = []
        for px, py in pts:
            dx, dy = px - ocx, py - ocy
            out.append((ocx + dx * np.cos(np.pi / 4) - dy * np.sin(np.pi / 4),
                        ocy + dx * np.sin(np.pi / 4) + dy * np.cos(np.pi / 4)))
        return out

    eye_l = [(cx - s * 0.24, cy + s * 0.14),
             (cx - s * 0.35, cy - s * 0.04),
             (cx - s * 0.13, cy - s * 0.04)]
    eye_r = [(cx + s * 0.24, cy + s * 0.14),
             (cx + s * 0.35, cy - s * 0.04),
             (cx + s * 0.13, cy - s * 0.04)]
    for eye in [eye_l, eye_r]:
        ax.add_patch(Polygon(rot45(eye, cx, cy), closed=True,
                             facecolor=inv, edgecolor="none"))

    # Mouth teeth
    teeth_x = np.linspace(cx - s * 0.26, cx + s * 0.26, 7)
    mouth_y_top = cy - s * 0.10
    mouth_y_bot = cy - s * 0.22
    raw_pts = [(teeth_x[0], mouth_y_top)]
    for k, x in enumerate(teeth_x):
        raw_pts.append((x, mouth_y_bot if k % 2 == 0 else mouth_y_top))
    raw_pts.append((teeth_x[-1], mouth_y_top))
    ax.add_patch(Polygon(rot45(raw_pts, cx, cy), closed=True,
                         facecolor=inv, edgecolor="none"))


def draw():
    """Pumpkins placed on a 45-degree rotated diamond (argyle) grid.
    The grid unit is a square rotated 45 deg → diamond cells."""
    fig, ax = setup_ax()

    # Diamond grid: tile along diagonals
    # Each cell diagonal = cell_d; centres at (i+j/2)*cell_d, j*cell_d*sin45
    n = 7          # number of diamonds across
    cell_d = PERIOD / n
    s = cell_d * 0.40

    rows_diag = int(np.ceil(PERIOD / (cell_d * np.sqrt(2) / 2))) + 4

    for row in range(-2, rows_diag):
        for col in range(-2, n + 3):
            # Diamond-grid centres: offset every other row by half a cell
            cx = (col + (row % 2) * 0.5) * cell_d
            cy = row * cell_d * 0.70   # vertical spacing = cell_d * cos45 ≈ 0.707
            fill = "white" if (row + col) % 2 == 0 else "black"
            edge_col = "white" if fill == "black" else "none"
            # Diamond clipping cell border
            diamond_pts = [
                (cx, cy + cell_d * 0.34),
                (cx + cell_d * 0.48, cy),
                (cx, cy - cell_d * 0.34),
                (cx - cell_d * 0.48, cy),
            ]
            for ox, oy in WRAPS:
                # cell fill diamond
                ax.add_patch(Polygon(
                    [(px + ox, py + oy) for px, py in diamond_pts],
                    closed=True, facecolor=fill, edgecolor="black",
                    linewidth=0.3, zorder=1))
                draw_pumpkin(ax, cx + ox, cy + oy, s,
                             fill="black" if fill == "white" else "white")

    save(fig, "abstract halloween variation pumpkin diamond rotated 45 degree tightly packed lattice pattern black white texture")


if __name__ == "__main__":
    draw()
