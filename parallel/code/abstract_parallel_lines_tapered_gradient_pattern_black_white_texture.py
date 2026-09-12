import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime

SIZE = 4000
DPI = 300
SEED = 42
DATE = datetime.now().strftime("%d%m%Y")

JPG_DIR = Path("output/jpg")
SVG_DIR = Path("output/svg")
JPG_DIR.mkdir(parents=True, exist_ok=True)
SVG_DIR.mkdir(parents=True, exist_ok=True)

np.random.seed(SEED)


def setup_ax():
    fig, ax = plt.subplots(figsize=(SIZE/DPI, SIZE/DPI), dpi=DPI)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.set_facecolor("white")
    ax.set_xlim(-5, 105)
    ax.set_ylim(-5, 105)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def save(fig, name):
    jpg_path = JPG_DIR / f"{name}_{DATE}.jpg"
    svg_path = SVG_DIR / f"{name}_{DATE}.svg"
    fig.savefig(jpg_path, dpi=DPI, pad_inches=0, facecolor="white")
    fig.savefig(svg_path, format="svg", pad_inches=0, facecolor="white")
    plt.close(fig)
    print(f"Tersimpan: {jpg_path} | {svg_path}")
def parallel_tapered_gradient():
    fig, ax = setup_ax()
    n_lines = 35
    for i in range(n_lines):
        y = -5 + i * (110 / n_lines)
        x = np.linspace(-5, 105, 500)
        thickness = 0.2 + 3.0 * np.abs(np.sin(x / 100 * np.pi))
        points = np.array([x, np.full_like(x, y)]).T
        from matplotlib.collections import LineCollection
        segments = np.array([[points[j], points[j+1]] for j in range(len(points)-1)])
        lc = LineCollection(segments, color="black", linewidths=thickness[:-1])
        ax.add_collection(lc)
    save(fig, "parallel_tapered_gradient")


if __name__ == "__main__":
    parallel_tapered_gradient()
