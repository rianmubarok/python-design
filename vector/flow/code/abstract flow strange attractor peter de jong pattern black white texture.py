import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime

SIZE = 4000
DPI = 300
SEED = 42
DATE = datetime.now().strftime("%d%m%Y")

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR.parent / "output"
JPG_DIR = OUTPUT_DIR / "jpg"
SVG_DIR = OUTPUT_DIR / "svg"
JPG_DIR.mkdir(parents=True, exist_ok=True)
SVG_DIR.mkdir(parents=True, exist_ok=True)

np.random.seed(SEED)


def setup_ax():
    fig, ax = plt.subplots(figsize=(SIZE / DPI, SIZE / DPI), dpi=DPI)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.set_facecolor("white")
    ax.set_xlim(-2.5, 2.5)
    ax.set_ylim(-2.5, 2.5)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def save(fig, name):
    jpg_path = JPG_DIR / f"{name} {DATE}.jpg"
    svg_path = SVG_DIR / f"{name} {DATE}.svg"
    fig.savefig(jpg_path, dpi=DPI, pad_inches=0, facecolor="white")
    fig.savefig(svg_path, format="svg", pad_inches=0, facecolor="white")
    plt.close(fig)
    print(f"Tersimpan: {jpg_path} | {svg_path}")


def abstract_flow_strange_attractor_peter_de_jong_pattern_black_white_texture():
    """Generates a Peter de Jong Attractor."""
    fig, ax = setup_ax()
    
    # Peter de Jong Attractor parameters
    a, b, c, d = 1.641, 1.902, 0.316, 1.525
    
    n_points = 500000
    x, y = np.zeros(n_points), np.zeros(n_points)
    
    x[0], y[0] = 0.1, 0.1
    
    for i in range(1, n_points):
        x[i] = np.sin(a * y[i-1]) - np.cos(b * x[i-1])
        y[i] = np.sin(c * x[i-1]) - np.cos(d * y[i-1])
        
    ax.plot(x, y, ',', color="black", alpha=0.1, markersize=0.5)
    
    save(fig, "abstract flow strange attractor peter de jong pattern black white texture")


if __name__ == "__main__":
    abstract_flow_strange_attractor_peter_de_jong_pattern_black_white_texture()
