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
    """Tweak: Zöllner with much denser micro-hatches and gentler baseline curvature."""
    fig, ax = setup_ax()

    n_lines = 36
    y_coords = np.linspace(-46, 46, n_lines)
    x_pts = np.linspace(-48, 48, 240)

    for i, y_base in enumerate(y_coords):
        wave_y = y_base + 0.55 * np.sin(x_pts * 0.18 + i * 0.22)
        ax.plot(x_pts, wave_y, color="black", linewidth=1.35)
        hatch_angle = np.radians(28 if i % 2 == 0 else -28)
        hatch_len = 1.55
        hatch_x = np.linspace(-47, 47, 72)
        for hx in hatch_x:
            hy = y_base + 0.55 * np.sin(hx * 0.18 + i * 0.22)
            dx = (hatch_len / 2) * np.cos(hatch_angle)
            dy = (hatch_len / 2) * np.sin(hatch_angle)
            ax.plot([hx - dx, hx + dx], [hy - dy, hy + dy], color="black", linewidth=0.85)

    save(
        fig,
        "abstract optical zollner illusion dense micro hatch curved base pattern black white texture",
    )


if __name__ == "__main__":
    generate()
