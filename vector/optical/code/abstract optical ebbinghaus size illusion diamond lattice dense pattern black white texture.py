import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch
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
    """Tweak: Dense diamond-lattice Ebbinghaus clusters with identical inner discs."""
    fig, ax = setup_ax()
    inner_r = 2.15
    cols = np.linspace(-36, 36, 5)
    rows = np.linspace(-36, 36, 5)

    for i, cy in enumerate(rows):
        x_off = 0.0 if i % 2 == 0 else (cols[1] - cols[0]) * 0.5
        for j, cx0 in enumerate(cols):
            cx = cx0 + x_off
            if abs(cx) > 46 or abs(cy) > 46:
                continue
            ax.add_patch(Circle((cx, cy), inner_r, facecolor="black", edgecolor="none"))
            large = (i + j) % 2 == 0
            if large:
                n_outer, ring_r, outer_s, pad = 6, 10.2, 5.8, 1.7
            else:
                n_outer, ring_r, outer_s, pad = 8, 6.4, 1.7, 0.5
            for a in np.linspace(0, 2 * np.pi, n_outer, endpoint=False):
                ox = cx + ring_r * np.cos(a)
                oy = cy + ring_r * np.sin(a)
                ax.add_patch(
                    FancyBboxPatch(
                        (ox - outer_s / 2, oy - outer_s / 2),
                        outer_s,
                        outer_s,
                        boxstyle=f"round,pad=0,rounding_size={pad:.2f}",
                        facecolor="black",
                        edgecolor="none",
                    )
                )

    save(
        fig,
        "abstract optical ebbinghaus size illusion diamond lattice dense pattern black white texture",
    )


if __name__ == "__main__":
    generate()
