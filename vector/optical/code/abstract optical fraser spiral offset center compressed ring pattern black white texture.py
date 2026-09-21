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
    """Tweak: Fraser spiral with shifted origin and compressed ring spacing (not a seamless tile)."""
    fig, ax = setup_ax()

    ox, oy = 7.5, -5.0
    num_rings = 34
    radii = np.linspace(1.4, 62, num_rings)
    tilt = np.radians(22)

    for r in radii:
        circle = plt.Circle((ox, oy), r, fill=False, edgecolor="black", linewidth=0.35, alpha=0.28)
        ax.add_patch(circle)

    for idx, r in enumerate(radii):
        num_elements = int(14 + idx * 7)
        angles = np.linspace(0, 2 * np.pi, num_elements, endpoint=False)
        segment_len = 1.15 + idx * 0.11
        for a in angles:
            cx = ox + r * np.cos(a)
            cy = oy + r * np.sin(a)
            cord_dir = a + np.pi / 2 + tilt
            dx = (segment_len / 2) * np.cos(cord_dir)
            dy = (segment_len / 2) * np.sin(cord_dir)
            ax.plot([cx - dx, cx + dx], [cy - dy, cy + dy], color="black", linewidth=2.2)
            ax.plot(
                [cx - dx * 0.42, cx + dx * 0.42],
                [cy - dy * 0.42, cy + dy * 0.42],
                color="white",
                linewidth=0.9,
            )

    save(
        fig,
        "abstract optical fraser spiral offset center compressed ring pattern black white texture",
    )


if __name__ == "__main__":
    generate()
