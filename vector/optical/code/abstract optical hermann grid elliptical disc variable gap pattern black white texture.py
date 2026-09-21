import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
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
    """Tweak: Hermann scintillating grid using stretched ellipses whose gap breathes across the field."""
    fig, ax = setup_ax()

    n = 12
    spacing = 100.0 / n
    for r in range(n):
        for c in range(n):
            x = (c + 0.5) * spacing
            y = (r + 0.5) * spacing
            breathe = 0.55 + 0.45 * np.sin((c + r) * 0.55)
            w = spacing * (0.58 + 0.18 * breathe)
            h = spacing * (0.42 + 0.12 * (1.0 - breathe))
            ax.add_patch(Ellipse((x, y), w, h, facecolor="black", edgecolor="none"))

    save(
        fig,
        "abstract optical hermann grid elliptical disc variable gap pattern black white texture",
    )


if __name__ == "__main__":
    generate()
