from datetime import datetime
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import matplotlib

matplotlib.use("Agg")

SIZE = 4000
DPI = 300
DATE = datetime.now().strftime("%d%m%Y")

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR.parent / "output"
JPG_DIR = OUTPUT_DIR / "jpg"
SVG_DIR = OUTPUT_DIR / "svg"
EPS_DIR = OUTPUT_DIR / "eps"
JPG_DIR.mkdir(parents=True, exist_ok=True)
SVG_DIR.mkdir(parents=True, exist_ok=True)
EPS_DIR.mkdir(parents=True, exist_ok=True)


def setup_ax():
    fig, ax = plt.subplots(figsize=(SIZE / DPI, SIZE / DPI), dpi=DPI)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.set_facecolor("white")
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def save(fig, name):
    jpg_path = JPG_DIR / f"{name} {DATE}.jpg"
    svg_path = SVG_DIR / f"{name} {DATE}.svg"
    eps_path = EPS_DIR / f"{name} {DATE}.eps"
    fig.savefig(jpg_path, dpi=DPI, pad_inches=0, facecolor="white")
    fig.savefig(svg_path, format="svg", pad_inches=0, facecolor="white")
    # Save EPS with larger figure size for 4MP+ bounding box
    orig_size = fig.get_size_inches()
    fig.set_size_inches(30, 30)
    fig.savefig(eps_path, format="eps", pad_inches=0, facecolor="white", dpi=DPI)
    fig.set_size_inches(orig_size[0], orig_size[1])
    plt.close(fig)
    print(f"Tersimpan: {jpg_path} | {svg_path} | {eps_path}")


def draw():
    """Concentric nested triangles pointing upwards with automatic symmetric framing."""
    fig, ax = setup_ax()

    cx, cy = 50.0, 48.0
    n_shapes = 35
    max_radius = 50.0  # Disesuaikan agar proporsional di dalam kanvas

    all_x = []
    all_y = []

    for i in range(1, n_shapes + 1):
        r = max_radius * (i / n_shapes)

        # Vertices of an equilateral triangle
        angles = np.array([np.pi / 2, np.pi / 2 + 2 * np.pi / 3, np.pi / 2 + 4 * np.pi / 3, np.pi / 2])
        x = cx + r * np.cos(angles)
        y = cy + r * np.sin(angles)

        all_x.extend(x)
        all_y.extend(y)

        ax.plot(
            x,
            y,
            color="black",
            linewidth=1.5,
            solid_capstyle="round",
            solid_joinstyle="round",
        )

    # Hitung Framing Simetris Terpusat
    min_x, max_x = min(all_x), max(all_x)
    min_y, max_y = min(all_y), max(all_y)

    center_x = (min_x + max_x) / 2.0
    center_y = (min_y + max_y) / 2.0
    w = max_x - min_x
    h = max_y - min_y
    pad = max(w, h) / 2.0 + 4.0  # Margin aman sekeliling kanvas

    ax.set_xlim(center_x - pad, center_x + pad)
    ax.set_ylim(center_y - pad, center_y + pad)

    save(fig, "abstract concentric triangles nested pattern black white texture")


if __name__ == "__main__":
    draw()