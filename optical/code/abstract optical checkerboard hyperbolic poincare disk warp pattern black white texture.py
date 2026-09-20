import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
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
    ax.set_xlim(-1.05, 1.05)
    ax.set_ylim(-1.05, 1.05)
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


def poincare(x, y):
    """Map Euclidean checker coords into a Poincaré-disk style radial warp."""
    r = np.hypot(x, y)
    if r < 1e-9:
        return 0.0, 0.0
    # Compress toward the rim: tanh radial map
    r_max = np.sqrt(2) * 1.05
    nr = np.tanh(r * 1.35) / np.tanh(r_max * 1.35)
    return x / r * nr, y / r * nr


def generate():
    """Wild: Checkerboard pulled into a hyperbolic Poincaré-disk warp (not seamless)."""
    fig, ax = setup_ax()

    n = 28
    vals = np.linspace(-1.08, 1.08, n + 1)
    for i in range(n):
        for j in range(n):
            if (i + j) % 2:
                continue
            corners = [
                (vals[j], vals[i]),
                (vals[j + 1], vals[i]),
                (vals[j + 1], vals[i + 1]),
                (vals[j], vals[i + 1]),
            ]
            # Subdivide edges so the warp stays curved
            pts = []
            for k in range(4):
                p0 = np.array(corners[k])
                p1 = np.array(corners[(k + 1) % 4])
                for t in np.linspace(0, 1, 6, endpoint=False):
                    p = (1 - t) * p0 + t * p1
                    pts.append(poincare(*p))
            ax.add_patch(Polygon(pts, closed=True, facecolor="black", edgecolor="none"))

    rim = np.linspace(0, 2 * np.pi, 400)
    ax.plot(np.cos(rim), np.sin(rim), color="black", linewidth=1.4)

    save(
        fig,
        "abstract optical checkerboard hyperbolic poincare disk warp pattern black white texture",
    )


if __name__ == "__main__":
    generate()
