import numpy as np
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
    """Wild: Zollner wave lines drawn on concentric ring paths (polar Zollner)."""
    fig, ax = setup_ax()

    # Use concentric rings as the "lines" for Zollner hatching
    n_rings = 26
    radii = np.linspace(4, 47, n_rings)
    theta = np.linspace(0, 2 * np.pi, 600)
    hatch_len = 2.8

    for i, r in enumerate(radii):
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        ax.plot(x, y, color="black", linewidth=2.2)

        # Hatch marks along each ring, tilted alternately inward/outward
        n_hatches = int(14 + i * 3)
        hatch_angles = np.linspace(0, 2 * np.pi, n_hatches, endpoint=False)
        tilt = 0.35 if i % 2 == 0 else -0.35  # radial tilt offset

        for ha in hatch_angles:
            hx = r * np.cos(ha)
            hy = r * np.sin(ha)
            # Perpendicular to ring + tilt
            perp = ha + np.pi / 2 + tilt
            dx = (hatch_len / 2) * np.cos(perp)
            dy = (hatch_len / 2) * np.sin(perp)
            ax.plot([hx - dx, hx + dx], [hy - dy, hy + dy],
                    color="black", linewidth=1.6)

    save(fig, "abstract optical zollner illusion polar concentric ring pattern black white texture")


if __name__ == "__main__":
    generate()
