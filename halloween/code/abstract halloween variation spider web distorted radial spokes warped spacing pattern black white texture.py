import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import (
    Arc, Circle, Ellipse, FancyBboxPatch, Polygon, Rectangle,
)
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
EPS_DIR = OUTPUT_DIR / \"eps\"
JPG_DIR.mkdir(parents=True, exist_ok=True)
SVG_DIR.mkdir(parents=True, exist_ok=True)
EPS_DIR.mkdir(parents=True, exist_ok=True)


def setup_ax():
    fig, ax = plt.subplots(figsize=(SIZE / DPI, SIZE / DPI), dpi=DPI)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.set_facecolor("white")
    ax.set_xlim(0, PERIOD)
    ax.set_ylim(0, PERIOD)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_clip_on(True)
    return fig, ax


def save(fig, name):
    jpg_path = JPG_DIR / f"{name} {DATE}.jpg"
    svg_path = SVG_DIR / f"{name} {DATE}.svg"
    fig.savefig(jpg_path, dpi=DPI, pad_inches=0, facecolor="white")
    fig.savefig(svg_path, format="svg", pad_inches=0, facecolor="white")
    eps_path = EPS_DIR / f\"{name} {DATE}.eps\"
    orig_size = fig.get_size_inches()
    fig.set_size_inches(30, 30)
    fig.savefig(eps_path, format=\"eps\", pad_inches=0, facecolor=\"white\", dpi=DPI)
    fig.set_size_inches(orig_size[0], orig_size[1])
    plt.close(fig)
    print(f"Tersimpan: {jpg_path} | {svg_path}")

def distorted_web(ax, cx, cy, r, seed):
    np.random.seed(seed)
    spokes = np.random.randint(6, 12)
    angles = np.linspace(0, 2*np.pi, spokes, endpoint=False)
    
    # Add distortion to angles
    angles += np.random.uniform(-0.3, 0.3, spokes)
    
    # Distorted radial spokes
    for i, a in enumerate(angles):
        spoke_r = r * np.random.uniform(0.7, 1.0)
        ax.plot([cx, cx + spoke_r * np.cos(a)], 
                [cy, cy + spoke_r * np.sin(a)], 
                color="black", linewidth=np.random.uniform(0.5, 1.2))
    
    # Warped rings with varying spacing
    ring_counts = np.random.randint(3, 7)
    ring_scales = np.sort(np.random.uniform(0.15, 0.95, ring_counts))
    
    for scale in ring_scales:
        pts = []
        for a in angles:
            # Add wobble to ring points
            wobble = np.random.uniform(-0.1, 0.1)
            actual_scale = scale * (1 + wobble)
            pts.append([cx + r * actual_scale * np.cos(a), 
                       cy + r * actual_scale * np.sin(a)])
        pts.append(pts[0])
        arr = np.array(pts)
        
        # Vary line width
        line_width = np.random.uniform(0.4, 0.9)
        ax.plot(arr[:, 0], arr[:, 1], color="black", linewidth=line_width)
    
    # Distorted center
    center_r = r * 0.25 * np.random.uniform(0.8, 1.2)
    center_shape = np.random.choice(["circle", "ellipse"])
    if center_shape == "circle":
        ax.add_patch(Circle((cx, cy), center_r, 
                           facecolor="black", edgecolor="none"))
    else:
        rx = center_r * np.random.uniform(0.7, 1.3)
        ry = center_r * np.random.uniform(0.7, 1.3)
        angle = np.random.uniform(0, 180)
        ax.add_patch(Ellipse((cx, cy), rx, ry, angle=angle,
                            facecolor="black", edgecolor="none"))


def draw():
    """Seamless distorted spider-web lattice with warped spacing."""
    fig, ax = setup_ax()
    cols, rows = 7, 7
    dx, dy = PERIOD / cols, PERIOD / rows
    
    seed_offset = 0
    for row in range(rows):
        for col in range(cols):
            # Add slight offset to grid positions
            offset_x = np.random.uniform(-0.1, 0.1) * dx
            offset_y = np.random.uniform(-0.1, 0.1) * dy
            
            cx = (col + 0.5) * dx + offset_x
            cy = (row + 0.5) * dy + offset_y
            
            # Vary size randomly
            r = min(dx, dy) * np.random.uniform(0.5, 0.7)
            
            for ox, oy in WRAPS:
                distorted_web(ax, cx + ox, cy + oy, r, seed_offset)
                seed_offset += 1
    
    save(fig, "abstract halloween variation spider web distorted radial spokes warped spacing pattern black white texture")


if __name__ == "__main__":
    draw()