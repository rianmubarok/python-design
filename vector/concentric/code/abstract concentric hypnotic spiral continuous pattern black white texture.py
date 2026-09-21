import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime

SIZE = 4000
DPI = 300
DATE = datetime.now().strftime("%d%m%Y")

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR.parent / "output"
JPG_DIR = OUTPUT_DIR / "jpg"
SVG_DIR = OUTPUT_DIR / "svg"
EPS_DIR = OUTPUT_DIR / "eps"
JPG_DIR.mkdir(parents=True, exist_ok=True)
SVG_DIR.mkdir(parents=True, exist_ok=True)
EPS_DIR.mkdir(parents=True, exist_ok=True)


def setup_ax():
    fig, ax = plt.subplots(figsize=(SIZE / DPI, SIZE / DPI), dpi=DPI)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.set_facecolor("white")
    ax.set_xlim(-5, 105)
    ax.set_ylim(-5, 105)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def save(fig, name):
    jpg_path = JPG_DIR / f"{name} {DATE}.jpg"
    svg_path = SVG_DIR / f"{name} {DATE}.svg"
    eps_path = EPS_DIR / f"{name} {DATE}.eps"
    fig.savefig(jpg_path, dpi=DPI, pad_inches=0, facecolor="white")
    fig.savefig(svg_path, format="svg", pad_inches=0, facecolor="white")
    # Save EPS with larger figure size for 4MP+ bounding box
    orig_size = fig.get_size_inches()
    fig.set_size_inches(30, 30)
    fig.savefig(eps_path, format="eps", pad_inches=0, facecolor="white", dpi=DPI)
    fig.set_size_inches(orig_size[0], orig_size[1])
    plt.close(fig)
    print(f"Tersimpan: {jpg_path} | {svg_path} | {eps_path}")


def draw():
    """
    Hypnotic Continuous Spiral.
    Instead of discrete concentric circles, it's one continuous line that
    spirals outward, but is slightly perturbed by sine waves so it resembles
    a dense grouping of concentric rings playing optical tricks.
    """
    fig, ax = setup_ax()

    cx, cy = 50.0, 50.0
    n_revolutions = 40
    max_radius = 65.0
    
    n_pts = 4000
    
    # Continuous angle from 0 to 40 * 2pi
    t = np.linspace(0, n_revolutions * 2 * np.pi, n_pts)
    
    # Radius grows linearly
    r_base = max_radius * (t / (n_revolutions * 2 * np.pi))
    
    # Add an oscillating perturbation that depends on angle,
    # causing the spiral lines to pinch and swell together
    perturbation = np.sin(t * 8) * (1.5 + 0.05 * r_base)
    
    r = r_base + perturbation
    
    x = cx + r * np.cos(t)
    y = cy + r * np.sin(t)
    
    # Varying line thickness for hypnotic effect
    from matplotlib.collections import LineCollection
    lw = 1.0 + 1.5 * np.sin(t * 16)
    lw = np.clip(lw, 0.3, 3.0)
    
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    lc = LineCollection(segments, linewidths=lw[:-1], colors="black", capstyle="round")
    ax.add_collection(lc)

    save(fig, "abstract concentric hypnotic spiral continuous pattern black white texture")


if __name__ == "__main__":
    draw()
