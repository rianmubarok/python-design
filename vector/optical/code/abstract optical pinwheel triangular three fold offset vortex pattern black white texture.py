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
    """Wild: Three-fold pinwheel vortex with an off-center origin and breathing spoke width."""
    fig, ax = setup_ax()
    ox, oy = 6.0, 4.5
    n_spokes = 72
    n_pts = 260
    t = np.linspace(0, 70, n_pts)

    for i in range(n_spokes):
        fold = i % 3
        twist = 0.035 + 0.018 * fold
        base = i * 2 * np.pi / n_spokes
        angle = base + twist * t
        x = ox + t * np.cos(angle)
        y = oy + t * np.sin(angle)
        envelope = 0.35 + 1.8 * (np.sin(t * 0.14 + fold) ** 2)
        for seg in range(0, n_pts - 1, 4):
            ax.plot(
                x[seg : seg + 5],
                y[seg : seg + 5],
                color="black",
                linewidth=float(envelope[seg]),
                solid_capstyle="round",
            )

    save(
        fig,
        "abstract optical pinwheel triangular three fold offset vortex pattern black white texture",
    )


if __name__ == "__main__":
    generate()
