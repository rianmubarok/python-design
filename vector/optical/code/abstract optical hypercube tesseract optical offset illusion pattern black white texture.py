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


def get_tesseract_edges():
    # 16 vertices of a 4D unit hypercube
    vertices = []
    for x in [-1, 1]:
        for y in [-1, 1]:
            for z in [-1, 1]:
                for w in [-1, 1]:
                    vertices.append([x, y, z, w])
    vertices = np.array(vertices, dtype=float)

    # 32 edges connecting vertices differing by 1 coordinate
    edges = []
    for i in range(16):
        for j in range(i + 1, 16):
            if np.sum(np.abs(vertices[i] - vertices[j]) > 1e-4) == 1:
                edges.append((i, j))
    return vertices, edges


def project_4d_to_2d(vertices, rx, ry, rw, d4=3.0, scale=12.0):
    # 4D rotations (X-W and Y-Z)
    c_w, s_w = np.cos(rw), np.sin(rw)
    R_xw = np.array([[c_w, 0, 0, -s_w], [0, 1, 0, 0], [0, 0, 1, 0], [s_w, 0, 0, c_w]])

    c_x, s_x = np.cos(rx), np.sin(rx)
    R_yz = np.array([[1, 0, 0, 0], [0, c_x, -s_x, 0], [0, s_x, c_x, 0], [0, 0, 0, 1]])

    rotated = vertices @ R_xw.T @ R_yz.T

    # 4D perspective projection to 3D
    w_factor = 1.0 / (d4 - rotated[:, 3])
    proj_3d = rotated[:, :3] * w_factor[:, np.newaxis]

    # 3D to 2D isometric projection
    proj_2d = proj_3d[:, :2] * scale
    return proj_2d


def abstract_optical_hypercube_tesseract_optical_offset_illusion_pattern_black_white_texture():
    """Optical experiment: 4D Hypercube wireframe projection with optical line offset hatches."""
    fig, ax = setup_ax()

    vertices, edges = get_tesseract_edges()

    # Draw 3x3 grid of hypercube projections with progressive rotation angles
    grid_coords = np.linspace(-30, 30, 3)

    for i, cx in enumerate(grid_coords):
        for j, cy in enumerate(grid_coords):
            rx = 0.4 + i * 0.35
            rw = 0.6 + j * 0.45

            proj_2d = project_4d_to_2d(vertices, rx, 0.3, rw, scale=14.0)
            proj_2d[:, 0] += cx
            proj_2d[:, 1] += cy

            # Render 32 hypercube edges
            for e1, e2 in edges:
                p1 = proj_2d[e1]
                p2 = proj_2d[e2]

                ax.plot(
                    [p1[0], p2[0]],
                    [p1[1], p2[1]],
                    color="black",
                    linewidth=1.8,
                )

                # Add optical Zöllner hatch ticks along edges
                mid_x = (p1[0] + p2[0]) / 2.0
                mid_y = (p1[1] + p2[1]) / 2.0
                dx = p2[0] - p1[0]
                dy = p2[1] - p1[1]
                angle = np.arctan2(dy, dx) + np.radians(45)

                tick_len = 1.8
                tx = (tick_len / 2) * np.cos(angle)
                ty = (tick_len / 2) * np.sin(angle)

                ax.plot(
                    [mid_x - tx, mid_x + tx],
                    [mid_y - ty, mid_y + ty],
                    color="black",
                    linewidth=1.2,
                )

    save(
        fig,
        "abstract optical hypercube tesseract optical offset illusion pattern black white texture",
    )


if __name__ == "__main__":
    abstract_optical_hypercube_tesseract_optical_offset_illusion_pattern_black_white_texture()
