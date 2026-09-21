import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon
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


def maple_leaf(ax, cx, cy, size, angle_deg, fill="black"):
    """Stylised 5-lobe maple leaf."""
    a = np.radians(angle_deg)
    n_lobes = 5
    pts = []
    for i in range(n_lobes*2+1):
        t = i / (n_lobes*2) * np.pi * 2 - np.pi/2
        # alternate between lobe tip and notch
        r = size if i % 2 == 0 else size*0.50
        pts.append([cx + r*np.cos(t), cy + r*np.sin(t)])
    # rotate
    c, s_ = np.cos(a), np.sin(a)
    R = np.array([[c,-s_],[s_,c]])
    pts = np.array(pts) - [cx, cy]
    pts = (R @ pts.T).T + [cx, cy]
    ax.add_patch(Polygon(pts, closed=True, facecolor=fill, edgecolor="none"))
    # stem
    stem_len = size*0.35
    ax.plot([cx, cx+stem_len*np.sin(a)],
            [cy, cy-stem_len*np.cos(a)],
            color=fill, linewidth=0.8)


def bat_poly(cx, cy, s):
    pts = np.array([
        [0.00,0.08],[0.12,0.18],[0.10,0.05],[0.42,0.22],[0.78,0.38],
        [0.62,0.08],[0.95,0.12],[0.55,-0.08],[0.72,-0.28],[0.28,-0.10],
        [0.18,-0.22],[0.08,-0.08],[0.00,-0.18],
        [-0.08,-0.08],[-0.18,-0.22],[-0.28,-0.10],[-0.72,-0.28],
        [-0.55,-0.08],[-0.95,0.12],[-0.62,0.08],[-0.78,0.38],
        [-0.42,0.22],[-0.10,0.05],[-0.12,0.18],
    ]) * s + [cx, cy]
    return pts


def draw():
    """Seamless scatter of falling maple leaves mixed with bat silhouettes."""
    fig, ax = setup_ax()
    rng = np.random.default_rng(27)
    n_items = 120
    for _ in range(n_items):
        cx = rng.uniform(0, PERIOD)
        cy = rng.uniform(0, PERIOD)
        is_bat = rng.random() < 0.35
        angle = rng.uniform(0, 360)
        if is_bat:
            s = rng.uniform(2.2, 5.5)
            for ox, oy in WRAPS:
                ax.add_patch(Polygon(bat_poly(cx+ox, cy+oy, s),
                                     closed=True, facecolor="black", edgecolor="none"))
        else:
            s = rng.uniform(2.5, 6.0)
            for ox, oy in WRAPS:
                maple_leaf(ax, cx+ox, cy+oy, s, angle)
    save(fig, "abstract halloween variation falling leaves bat scatter organic mix pattern black white texture")


if __name__ == "__main__":
    draw()
