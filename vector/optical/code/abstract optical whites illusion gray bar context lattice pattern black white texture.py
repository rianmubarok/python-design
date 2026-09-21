import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
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
    """Wild: White's illusion lattice — identical mid-gray bars look different on black vs white stripes."""
    fig, ax = setup_ax()

    n_stripes = 16
    stripe_w = 100.0 / n_stripes
    for i in range(n_stripes):
        color = "black" if i % 2 == 0 else "white"
        ax.add_patch(Rectangle((i * stripe_w, 0), stripe_w, 100, facecolor=color, edgecolor="none"))

    n_rows = 10
    bar_h = 3.4
    gray = "#808080"
    ys = np.linspace(8, 92, n_rows)
    for r, y in enumerate(ys):
        # Place gray rectangles that sit half on black, half on white context
        start = 1 if r % 2 == 0 else 0
        for i in range(start, n_stripes - 1, 4):
            ax.add_patch(
                Rectangle(
                    (i * stripe_w + stripe_w * 0.15, y - bar_h / 2),
                    stripe_w * 1.7,
                    bar_h,
                    facecolor=gray,
                    edgecolor="none",
                )
            )

    save(
        fig,
        "abstract optical whites illusion gray bar context lattice pattern black white texture",
    )


if __name__ == "__main__":
    generate()
