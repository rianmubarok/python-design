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
    """Tweak: Zollner with angular escalation — hatch angle increases progressively per row."""
    fig, ax = setup_ax()

    n_lines = 30
    y_coords = np.linspace(-46, 46, n_lines)

    for i, y_base in enumerate(y_coords):
        x_pts = np.linspace(-48, 48, 200)
        ax.plot(x_pts, np.full_like(x_pts, y_base), color="black", linewidth=2.5)

        # Progressive hatch angle: starts small, escalates dramatically
        hatch_angle = np.radians(10 + (i / n_lines) * 70)
        if i % 2 == 1:
            hatch_angle = -hatch_angle

        hatch_length = 3.5
        num_hatches = 40
        hatch_x_centers = np.linspace(-46, 46, num_hatches)

        for hx in hatch_x_centers:
            dx = (hatch_length / 2) * np.cos(hatch_angle)
            dy = (hatch_length / 2) * np.sin(hatch_angle)
            ax.plot([hx - dx, hx + dx], [y_base - dy, y_base + dy],
                    color="black", linewidth=1.8)

    save(fig, "abstract optical zollner illusion progressive angle escalation pattern black white texture")


if __name__ == "__main__":
    generate()
