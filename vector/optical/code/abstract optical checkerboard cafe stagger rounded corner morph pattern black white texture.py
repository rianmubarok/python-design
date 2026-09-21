import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
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
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
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
    """Tweak: Checkerboard with café-wall row stagger and corner radius that morphs across the tile."""
    fig, ax = setup_ax()

    n_rows = 16
    n_cols = 16
    cell = 100.0 / n_cols
    row_h = 100.0 / n_rows
    offsets = [0.0, 0.22, 0.44, 0.22]

    for r in range(n_rows):
        y = r * row_h
        shift = offsets[r % len(offsets)] * cell
        for c in range(-1, n_cols + 2):
            if (c + r) % 2 != 0:
                continue
            x = c * cell + shift
            morph = 0.5 + 0.5 * np.sin((c + r) * 0.4)
            rounding = 0.15 + morph * (min(cell, row_h) * 0.48)
            ax.add_patch(
                FancyBboxPatch(
                    (x + 0.15, y + 0.15),
                    cell - 0.3,
                    row_h - 0.3,
                    boxstyle=f"round,pad=0,rounding_size={rounding:.3f}",
                    facecolor="black",
                    edgecolor="none",
                )
            )

    save(
        fig,
        "abstract optical checkerboard cafe stagger rounded corner morph pattern black white texture",
    )


if __name__ == "__main__":
    generate()
