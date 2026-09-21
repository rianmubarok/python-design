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
    Fragmented Radial Scatter.
    Concentric circles broken into discrete dashed arcs that randomly scatter
    outward radially, simulating an explosion of orbital tracks.
    """
    fig, ax = setup_ax()
    rng = np.random.default_rng(42)

    cx, cy = 50.0, 50.0
    n_circles = 40
    max_radius = 65.0

    for i in range(1, n_circles + 1):
        r_base = max_radius * (i / n_circles)
        
        # Break circle into random angular segments
        n_segments = int(rng.uniform(4, 15))
        starts = np.sort(rng.uniform(0, 2*np.pi, n_segments))
        
        for j in range(n_segments):
            start_angle = starts[j]
            if j < n_segments - 1:
                end_angle = starts[j+1]
            else:
                end_angle = starts[0] + 2*np.pi
                
            # Leave a gap between segments
            arc_length = end_angle - start_angle
            gap = arc_length * rng.uniform(0.1, 0.4)
            end_angle -= gap
            
            if end_angle <= start_angle:
                continue
                
            # Random radial scatter for this specific arc segment
            # Outer rings scatter more
            scatter_amt = rng.uniform(-1.0, 2.5) * (i / n_circles) ** 1.5
            r = r_base + scatter_amt * 8.0
            
            angles = np.linspace(start_angle, end_angle, 50)
            x = cx + r * np.cos(angles)
            y = cy + r * np.sin(angles)
            
            ax.plot(x, y, color="black", linewidth=1.5, solid_capstyle="round")

    save(fig, "abstract concentric circles fragmented radial scatter pattern black white texture")


if __name__ == "__main__":
    draw()
