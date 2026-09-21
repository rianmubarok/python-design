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
    ax.set_xlim(-50, 50)
    ax.set_ylim(-50, 50)
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


def generate():
    """Tweak: Café-wall polar rings with variable tile height and rounded ends."""
    fig, ax = setup_ax()

    n_rings = 14
    radii = np.linspace(6, 47, n_rings)
    for i, r in enumerate(radii[:-1]):
        r1 = radii[i + 1]
        r_mid = 0.5 * (r + r1)
        h = r1 - r
        n_tiles = max(12, int(2 * np.pi * r_mid / 7.2))
        shift = 0.5 if i % 2 == 0 else 0.0
        for k in range(n_tiles):
            if k % 2:
                continue
            a0 = (k + shift) * 360.0 / n_tiles
            a1 = (k + 1 + shift) * 360.0 / n_tiles
            theta = np.linspace(np.radians(a0), np.radians(a1), 18)
            inner = np.column_stack([(r + 0.25) * np.cos(theta), (r + 0.25) * np.sin(theta)])
            outer = np.column_stack([(r1 - 0.25) * np.cos(theta[::-1]), (r1 - 0.25) * np.sin(theta[::-1])])
            pts = np.vstack([inner, outer])
            ax.add_patch(Polygon(pts, closed=True, facecolor="black", edgecolor="none"))
        # gray mortar ring
        t = np.linspace(0, 2 * np.pi, 360)
        ax.plot(r * np.cos(t), r * np.sin(t), color="#7a7a7a", linewidth=1.4)
    t = np.linspace(0, 2 * np.pi, 360)
    ax.plot(radii[-1] * np.cos(t), radii[-1] * np.sin(t), color="#7a7a7a", linewidth=1.4)

    save(
        fig,
        "abstract optical cafe wall polar ring rounded tile shift pattern black white texture",
    )


if __name__ == "__main__":
    generate()
