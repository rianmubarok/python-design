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
    """Tweak: Fraser spiral with LARGE tilt angle (45 deg) and compressed ring spacing."""
    fig, ax = setup_ax()

    num_rings = 28
    radii = np.linspace(2, 47, num_rings)
    tilt_angle = np.radians(45)

    for r in radii:
        circle = plt.Circle((0, 0), r, fill=False, edgecolor="black", linewidth=0.5, alpha=0.35)
        ax.add_patch(circle)

    for idx, r in enumerate(radii):
        num_elements = int(18 + idx * 10)
        angles = np.linspace(0, 2 * np.pi, num_elements, endpoint=False)
        segment_len = 1.8 + idx * 0.18

        for a in angles:
            cx = r * np.cos(a)
            cy = r * np.sin(a)
            tangent = a + np.pi / 2
            cord_dir = tangent + tilt_angle

            dx = (segment_len / 2) * np.cos(cord_dir)
            dy = (segment_len / 2) * np.sin(cord_dir)

            ax.plot([cx - dx, cx + dx], [cy - dy, cy + dy],
                    color="black", linewidth=3.0)
            ax.plot([cx - dx * 0.45, cx + dx * 0.45],
                    [cy - dy * 0.45, cy + dy * 0.45],
                    color="white", linewidth=1.2)

    save(fig, "abstract optical fraser spiral large tilt dense cord pattern black white texture")


if __name__ == "__main__":
    generate()
