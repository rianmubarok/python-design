import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d
from matplotlib.patches import Wedge, Polygon
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


def abstract_optical_kanizsa_triangle_voronoi_negative_space_pattern_black_white_texture():
    """Optical experiment: Kanizsa negative space illusion built from a Voronoi cell lattice and Pac-Man notches."""
    fig, ax = setup_ax()

    # Generate relaxed Voronoi points
    n_points = 35
    points = np.random.uniform(-40, 40, (n_points, 2))

    # Lloyd relaxation step
    vor = Voronoi(points)
    centroids = []
    for region_idx in vor.point_region:
        region = vor.regions[region_idx]
        if not region or -1 in region:
            continue
        polygon = vor.vertices[region]
        centroids.append(polygon.mean(axis=0))
    if len(centroids) > 0:
        points = np.array(centroids)
        vor = Voronoi(points)

    # Plot Voronoi edges with bold black lines
    for line in vor.ridge_vertices:
        if -1 not in line:
            p1 = vor.vertices[line[0]]
            p2 = vor.vertices[line[1]]
            if (
                np.all(np.abs(p1) < 48)
                and np.all(np.abs(p2) < 48)
            ):
                ax.plot(
                    [p1[0], p2[0]], [p1[1], p2[1]], color="black", linewidth=1.5
                )

    # Place Kanizsa Pac-Man discs at triangle vertices to induce subjective white triangles in negative space
    triangle_centers = [(-22, -10), (22, -10), (0, 26)]
    triangle_orientations = [60, 180, 300]  # Cut angles towards triangle center

    for (cx, cy), notch_angle in zip(triangle_centers, triangle_orientations):
        # Draw Pac-Man disc with missing 60-degree wedge
        r = 9.5
        w = Wedge(
            (cx, cy),
            r,
            notch_angle + 30,
            notch_angle + 330,
            facecolor="black",
            edgecolor="black",
        )
        ax.add_patch(w)

    # Secondary smaller inverted subjective triangle Pac-Mans
    sub_centers = [(-11, 12), (11, 12), (0, -7)]
    sub_orientations = [240, 0, 120]

    for (cx, cy), notch_angle in zip(sub_centers, sub_orientations):
        r = 5.0
        w = Wedge(
            (cx, cy),
            r,
            notch_angle + 30,
            notch_angle + 330,
            facecolor="black",
            edgecolor="black",
        )
        ax.add_patch(w)

    save(
        fig,
        "abstract optical kanizsa triangle voronoi negative space pattern black white texture",
    )


if __name__ == "__main__":
    abstract_optical_kanizsa_triangle_voronoi_negative_space_pattern_black_white_texture()
