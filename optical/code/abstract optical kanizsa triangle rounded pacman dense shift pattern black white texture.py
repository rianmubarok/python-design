import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge
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
    """Tweak: Denser Kanizsa pac-men with rounded mouths and a half-cell shift (tiled)."""
    fig, ax = setup_ax()
    spacing = 11.5
    pac_r = 2.85
    rows, cols = 9, 9
    mouth = 52  # wider rounded-looking bite

    for r in range(rows):
        for c in range(cols):
            cx = (c - cols / 2 + 0.5) * spacing + (spacing * 0.28 if r % 2 else 0)
            cy = (r - rows / 2 + 0.5) * spacing
            if (r + c) % 2 == 0:
                positions = [(cx - 3.6, cy - 2.1, 28), (cx + 3.6, cy - 2.1, 152), (cx, cy + 4.2, 270)]
            else:
                positions = [(cx - 3.6, cy + 2.1, 332), (cx + 3.6, cy + 2.1, 208), (cx, cy - 4.2, 90)]
            for px, py, mouth_angle in positions:
                ax.add_patch(
                    Wedge(
                        (px, py),
                        pac_r,
                        mouth_angle + mouth / 2,
                        mouth_angle + 360 - mouth / 2,
                        facecolor="black",
                        edgecolor="black",
                        linewidth=0.2,
                    )
                )

    save(
        fig,
        "abstract optical kanizsa triangle rounded pacman dense shift pattern black white texture",
    )


if __name__ == "__main__":
    generate()
