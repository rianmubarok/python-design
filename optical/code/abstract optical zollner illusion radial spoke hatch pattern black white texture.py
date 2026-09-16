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
    """Tweak: Zollner using radiating lines as base, with hatch marks perpendicular to each ray."""
    fig, ax = setup_ax()

    n_rays = 36
    cx, cy = 0, 0

    for i in range(n_rays):
        angle = i * 2 * np.pi / n_rays
        # Draw main spoke
        r_vals = np.linspace(4, 46, 200)
        xr = cx + r_vals * np.cos(angle)
        yr = cy + r_vals * np.sin(angle)
        ax.plot(xr, yr, color="black", linewidth=2.2)

        # Perpendicular hatch marks along each spoke
        hatch_r_positions = np.linspace(8, 44, 18)
        perp_angle = angle + np.pi / 2 + (0.3 if i % 2 == 0 else -0.3)
        hatch_len = 2.5

        for r in hatch_r_positions:
            hx = cx + r * np.cos(angle)
            hy = cy + r * np.sin(angle)
            dx = (hatch_len / 2) * np.cos(perp_angle)
            dy = (hatch_len / 2) * np.sin(perp_angle)
            ax.plot([hx - dx, hx + dx], [hy - dy, hy + dy],
                    color="black", linewidth=1.5)

    save(fig, "abstract optical zollner illusion radial spoke hatch pattern black white texture")


if __name__ == "__main__":
    generate()
