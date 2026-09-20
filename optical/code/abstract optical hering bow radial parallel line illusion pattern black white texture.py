import numpy as np
import matplotlib
matplotlib.use("Agg")
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
    """Wild: Hering illusion — radial fan plus apparently bowed parallel bars (not seamless)."""
    fig, ax = setup_ax()

    n_rays = 48
    for i in range(n_rays):
        a = i * np.pi / n_rays
        ax.plot(
            [-55 * np.cos(a), 55 * np.cos(a)],
            [-55 * np.sin(a), 55 * np.sin(a)],
            color="black",
            linewidth=0.7,
            alpha=0.9,
        )

    xs = np.linspace(-46, 46, 200)
    for k, y0 in enumerate(np.linspace(-28, 28, 9)):
        # True parallels; the rays make them look bowed.
        ax.plot(xs, np.full_like(xs, y0), color="black", linewidth=2.4 if k in (0, 8) else 1.7)

    save(
        fig,
        "abstract optical hering bow radial parallel line illusion pattern black white texture",
    )


if __name__ == "__main__":
    generate()
