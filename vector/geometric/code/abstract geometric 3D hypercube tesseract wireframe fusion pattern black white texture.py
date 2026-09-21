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
    ax.set_xlim(-5, 105)
    ax.set_ylim(-5, 105)
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


def abstract_geometric_3D_hypercube_tesseract_wireframe_fusion_pattern_black_white_texture():
    """Wild Combination: Fusion of 4D Hypercube / Tesseract perspective projection with geometric line hatchings."""
    fig, ax = setup_ax()
    
    # 4D Hypercube 16 vertices: (+-1, +-1, +-1, +-1)
    vertices_4d = np.array([[i, j, k, l] for i in [-1, 1] for j in [-1, 1] for k in [-1, 1] for l in [-1, 1]], dtype=float)
    
    # 4D Rotation matrix (X-W plane)
    theta = np.pi / 5
    rot_4d = np.array([
        [np.cos(theta), 0, 0, -np.sin(theta)],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [np.sin(theta), 0, 0, np.cos(theta)]
    ])
    
    rot_vertices = vertices_4d @ rot_4d.T
    
    # Perspective projection 4D -> 3D -> 2D (diperbesar maksimal)
    d4 = 3.0
    pts_3d = rot_vertices[:, :3] / (d4 - rot_vertices[:, 3:])
    
    d3 = 3.0
    pts_2d = pts_3d[:, :2] / (d3 - pts_3d[:, 2:]) * 200.0 + 50.0  # Perbesar dari 120 ke 200, memenuhi canvas
    
    # Connect edges (vertices differing by 1 coordinate)
    for i in range(16):
        for j in range(i + 1, 16):
            if np.sum(np.abs(vertices_4d[i] - vertices_4d[j])) == 2.0:
                ax.plot([pts_2d[i, 0], pts_2d[j, 0]], [pts_2d[i, 1], pts_2d[j, 1]], color="black", linewidth=1.2)

    save(fig, "abstract geometric 3D hypercube tesseract wireframe fusion pattern black white texture")


if __name__ == "__main__":
    abstract_geometric_3D_hypercube_tesseract_wireframe_fusion_pattern_black_white_texture()
