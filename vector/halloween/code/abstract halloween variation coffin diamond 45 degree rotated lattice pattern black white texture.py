import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.transforms import Affine2D
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


def coffin_pts_local(w, h):
    hw = w / 2
    return np.array([
        [-hw * 0.40, -h * 0.50],
        [ hw * 0.40, -h * 0.50],
        [ hw * 1.00, -h * 0.18],
        [ hw * 0.78,  h * 0.50],
        [-hw * 0.78,  h * 0.50],
        [-hw * 1.00, -h * 0.18],
    ])


def draw():
    """Coffins rotated 45°, arranged on a diamond (rotated square) grid.
    Alternating black/white fill so neighbours contrast each other."""
    fig, ax = setup_ax()
    # Diamond grid step — use 45° rotated coordinates
    step = PERIOD / 7.0
    cw = step * 0.82
    ch = step * 0.86
    pts_local = coffin_pts_local(cw, ch)
    # Rotate pts 45°
    angle = np.radians(45)
    R = np.array([[np.cos(angle), -np.sin(angle)],
                  [np.sin(angle),  np.cos(angle)]])
    pts_rotated = (R @ pts_local.T).T

    cols, rows = 9, 9
    dx = PERIOD / cols
    dy = PERIOD / rows
    for row in range(rows):
        for col in range(cols):
            cx = (col + 0.5) * dx + (dx * 0.5 if row % 2 else 0)
            cy = (row + 0.5) * dy
            fill = "black" if (row + col) % 2 == 0 else "white"
            edge = "none" if fill == "black" else "black"
            inv = "white" if fill == "black" else "black"
            for ox, oy in WRAPS:
                translated = pts_rotated + [cx + ox, cy + oy]
                ax.add_patch(Polygon(translated, closed=True,
                                     facecolor=fill, edgecolor=edge, linewidth=0.6))
                # cross detail (also rotated)
                cross_len = ch * 0.22
                cross_arm = cw * 0.14
                for angle_c, lx, ly in [(45, 0, ch*0.10), (45, 0, ch*0.10)]:
                    # vertical arm of cross
                    v0 = R @ np.array([0, cross_len])
                    v1 = R @ np.array([0, -cross_len * 0.2])
                    # horizontal arm
                    h0 = R @ np.array([-cross_arm, cross_len * 0.35])
                    h1 = R @ np.array([cross_arm, cross_len * 0.35])
                ax.plot([cx+ox + v0[0], cx+ox + v1[0]],
                        [cy+oy + v0[1], cy+oy + v1[1]],
                        color=inv, linewidth=0.9)
                ax.plot([cx+ox + h0[0], cx+ox + h1[0]],
                        [cy+oy + h0[1], cy+oy + h1[1]],
                        color=inv, linewidth=0.9)
    save(fig, "abstract halloween variation coffin diamond 45 degree rotated lattice pattern black white texture")


if __name__ == "__main__":
    draw()
