import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi
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


def draw_pacman_towards_center(ax, center_pt, target_pt, radius=10.0, f_angle=60):
    dx = target_pt[0] - center_pt[0]
    dy = target_pt[1] - center_pt[1]
    angle_to_target = np.degrees(np.arctan2(dy, dx))

    theta1 = angle_to_target + (f_angle / 2)
    theta2 = angle_to_target + 360 - (f_angle / 2)

    w = Wedge(
        center_pt,
        radius,
        theta1,
        theta2,
        facecolor="black",
        edgecolor="black",
        linewidth=0.5,
        zorder=3,
    )
    ax.add_patch(w)


def abstract_optical_kanizsa_triangle_voronoi_negative_space_pattern_black_white_texture():
    fig, ax = setup_ax()

    # 1. Generate Voronoi Grid Background
    n_points = 180
    points = np.random.uniform(-55, 55, (n_points, 2))
    vor = Voronoi(points)

    for line in vor.ridge_vertices:
        if -1 not in line:
            p1 = vor.vertices[line[0]]
            p2 = vor.vertices[line[1]]
            if np.all(np.abs(p1) < 52) and np.all(np.abs(p2) < 52):
                ax.plot(
                    [p1[0], p2[0]], [p1[1], p2[1]], color="black", linewidth=0.8, alpha=0.75, zorder=1
                )

    # 2. Koordinat Segitiga Utama
    side_len = 50.0
    h = side_len * np.sqrt(3) / 2
    cy_offset = -4.0

    A = np.array([0.0, cy_offset + h * (2 / 3)])
    B = np.array([-side_len / 2, cy_offset - h * (1 / 3)])
    C = np.array([side_len / 2, cy_offset - h * (1 / 3)])
    tri_center = (A + B + C) / 3.0

    # 3. Menutupi area segitiga dengan warna putih polos (Masking) agar ilusi timbul
    triangle_patch = Polygon([A, B, C], facecolor="white", edgecolor="none", zorder=2)
    ax.add_patch(triangle_patch)

    # 4. Gambar Pac-Man Utama (Besar)
    r_main = 11.5
    draw_pacman_towards_center(ax, A, tri_center, radius=r_main, f_angle=60)
    draw_pacman_towards_center(ax, B, tri_center, radius=r_main, f_angle=60)
    draw_pacman_towards_center(ax, C, tri_center, radius=r_main, f_angle=60)

    # 5. Segitiga Sekunder Kecil Terbalik
    A_sub = np.array([0.0, cy_offset - h * (1 / 3)])
    B_sub = np.array([-side_len / 4, cy_offset + h * (1 / 6)])
    C_sub = np.array([side_len / 4, cy_offset + h * (1 / 6)])
    sub_center = (A_sub + B_sub + C_sub) / 3.0

    r_sub = 5.5
    draw_pacman_towards_center(ax, A_sub, sub_center, radius=r_sub, f_angle=60)
    draw_pacman_towards_center(ax, B_sub, sub_center, radius=r_sub, f_angle=60)
    draw_pacman_towards_center(ax, C_sub, sub_center, radius=r_sub, f_angle=60)

    save(
        fig,
        "abstract optical kanizsa triangle voronoi negative space pattern black white texture",
    )


if __name__ == "__main__":
    abstract_optical_kanizsa_triangle_voronoi_negative_space_pattern_black_white_texture()