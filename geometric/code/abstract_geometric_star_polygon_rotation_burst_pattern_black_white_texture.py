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


def draw_star_polygon(cx, cy, outer_radius, inner_radius, points, rotation=0):
    """Menghitung koordinat poligon bintang dengan sudut berselang-seling."""
    angles = []
    radii = []

    for i in range(points * 2):
        angle = rotation + i * np.pi / points
        radius = outer_radius if i % 2 == 0 else inner_radius
        angles.append(angle)
        radii.append(radius)

    angles.append(angles[0])
    radii.append(radii[0])

    x = [cx + r * np.cos(a) for r, a in zip(radii, angles)]
    y = [cy + r * np.sin(a) for r, a in zip(radii, angles)]

    return x, y


def star_polygon_rotation_burst():
    """Teselasi ledakan bintang terpusat yang rapat, simetris, dan proporsional."""
    fig, ax = setup_ax()

    cx, cy = 50.0, 50.0
    n_rings = 9
    stars_per_ring = [1, 6, 12, 18, 24, 30, 36, 42, 48]  # Ditingkatkan agar lebih rapat

    for ring in range(n_rings):
        n_stars = stars_per_ring[ring]
        ring_radius = ring * 5.2  # Dibuat lebih rapat dari 8.0

        for star_idx in range(n_stars):
            if ring == 0:
                star_x, star_y = cx, cy
                rotation = 0
                outer_radius = 4.2
                inner_radius = 2.1
                points = 8
            else:
                angle = 2 * np.pi * star_idx / n_stars
                star_x = cx + ring_radius * np.cos(angle)
                star_y = cy + ring_radius * np.sin(angle)
                rotation = angle + ring * np.pi / 6

                outer_radius = 1.8 + ring * 0.35
                inner_radius = outer_radius * 0.42
                points = 5 + (ring % 3)

            x_star, y_star = draw_star_polygon(
                star_x, star_y, outer_radius, inner_radius, points, rotation
            )

            lw = max(0.5, 1.8 - ring * 0.12)

            if ring % 2 == 0:
                ax.plot(
                    x_star,
                    y_star,
                    color="black",
                    linewidth=lw,
                    solid_capstyle="round",
                    zorder=2,
                )
            else:
                ax.plot(
                    x_star,
                    y_star,
                    color="black",
                    linewidth=lw,
                    linestyle=(0, (2, 1)),
                    solid_capstyle="round",
                    zorder=2,
                )

    # Memfokuskan tampilan agar simetris dan seluruh bintang luar muat
    pad = 48.0
    ax.set_xlim(50 - pad, 50 + pad)
    ax.set_ylim(50 - pad, 50 + pad)

    save(fig, "star polygon rotation burst")


if __name__ == "__main__":
    star_polygon_rotation_burst()