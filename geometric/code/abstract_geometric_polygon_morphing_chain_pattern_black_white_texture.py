from datetime import datetime
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import matplotlib

matplotlib.use("Agg")

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


def draw_polygon(cx, cy, radius, sides, rotation=0):
    """Menghitung koordinat poligon dengan jumlah sisi tertentu."""
    angles = np.linspace(0, 2 * np.pi, sides + 1) + rotation
    x = cx + radius * np.cos(angles)
    y = cy + radius * np.sin(angles)
    return x, y


def polygon_morphing_chain():
    """Rantai poligon morphing yang tersusun rapi, padat, dan teratur."""
    fig, ax = setup_ax()

    # Tiga rantai sejajar dengan offset sinusoidal yang tidak saling bertabrakan
    chains_config = [
        {"y_base": 70.0, "freq": 2.0, "amp": 12.0, "start_sides": 3, "end_sides": 16},
        {"y_base": 50.0, "freq": 2.0, "amp": -12.0, "start_sides": 4, "end_sides": 18},
        {"y_base": 30.0, "freq": 2.0, "amp": 12.0, "start_sides": 3, "end_sides": 20},
    ]

    n_polygons = 22

    for config in chains_config:
        chain_points = []
        for i in range(n_polygons):
            t = i / (n_polygons - 1)
            x = 10.0 + t * 80.0
            y = config["y_base"] + config["amp"] * np.sin(t * np.pi * config["freq"])
            chain_points.append((x, y))

        for i, (cx, cy) in enumerate(chain_points):
            progress = i / (n_polygons - 1)
            sides = int(config["start_sides"] + progress * (config["end_sides"] - config["start_sides"]))
            radius = 3.2 + 2.5 * np.sin(progress * np.pi)
            rotation = progress * np.pi * 2.5

            x_poly, y_poly = draw_polygon(cx, cy, radius, sides, rotation)
            lw = 0.8 + 1.0 * progress

            ax.plot(
                x_poly,
                y_poly,
                color="black",
                linewidth=lw,
                solid_capstyle="round",
                zorder=2,
            )

            # Garis penghubung antar-pusat poligon
            if i < n_polygons - 1:
                next_cx, next_cy = chain_points[i + 1]
                ax.plot(
                    [cx, next_cx],
                    [cy, next_cy],
                    color="black",
                    linewidth=0.4,
                    linestyle=(0, (3, 3)),
                    zorder=1,
                )

    # Framing simetris terpusat
    pad = 42.0
    ax.set_xlim(50 - pad, 50 + pad)
    ax.set_ylim(50 - pad, 50 + pad)

    save(fig, "polygon morphing chain")


if __name__ == "__main__":
    polygon_morphing_chain()