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
    """Wild: MacKay rays — dense fan spokes overlaid with concentric rings (scintillating moiré)."""
    fig, ax = setup_ax()

    n_rays = 120
    t = np.linspace(1.2, 70, 2)
    for i in range(n_rays):
        a = i * np.pi / n_rays
        ax.plot(
            [t[0] * np.cos(a), 55 * np.cos(a)],
            [t[0] * np.sin(a), 55 * np.sin(a)],
            color="black",
            linewidth=0.55,
        )
        ax.plot(
            [-t[0] * np.cos(a), -55 * np.cos(a)],
            [-t[0] * np.sin(a), -55 * np.sin(a)],
            color="black",
            linewidth=0.55,
        )

    theta = np.linspace(0, 2 * np.pi, 400)
    for i, r in enumerate(np.linspace(3.5, 48, 28)):
        lw = 1.35 if i % 2 == 0 else 0.55
        ax.plot(r * np.cos(theta), r * np.sin(theta), color="black", linewidth=lw)

    save(
        fig,
        "abstract optical mackay rays fan spoke scintillating moire pattern black white texture",
    )


if __name__ == "__main__":
    generate()
