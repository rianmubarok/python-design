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
    """Wild: Fraser spiral cords arranged on an ELLIPSE, not a circle — creates bizarre tilted plane illusion."""
    fig, ax = setup_ax()

    num_rings = 22
    tilt_angle = np.radians(22)

    # Ellipse semi-axes: horizontal compressed, vertical stretched
    a_vals = np.linspace(4, 46, num_rings)
    b_scale = 0.55  # compress y-axis

    for idx, a in enumerate(a_vals):
        b = a * b_scale
        num_elements = int(20 + idx * 9)
        t_vals = np.linspace(0, 2 * np.pi, num_elements, endpoint=False)
        segment_len = 2.0 + idx * 0.16

        for t in t_vals:
            cx = a * np.cos(t)
            cy = b * np.sin(t)

            # Tangent of ellipse at t
            tx_tan = -a * np.sin(t)
            ty_tan = b * np.cos(t)
            tangent = np.arctan2(ty_tan, tx_tan)
            cord_dir = tangent + tilt_angle

            dx = (segment_len / 2) * np.cos(cord_dir)
            dy = (segment_len / 2) * np.sin(cord_dir)

            ax.plot([cx - dx, cx + dx], [cy - dy, cy + dy],
                    color="black", linewidth=2.6)
            ax.plot([cx - dx * 0.5, cx + dx * 0.5],
                    [cy - dy * 0.5, cy + dy * 0.5],
                    color="white", linewidth=1.0)

    save(fig, "abstract optical fraser spiral ellipse skew tilted plane pattern black white texture")


if __name__ == "__main__":
    generate()
