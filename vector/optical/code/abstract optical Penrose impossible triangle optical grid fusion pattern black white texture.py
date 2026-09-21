import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
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

# The three visible faces of a Penrose tribar (isometric), each an L-shaped
# hexagon. They tile the figure edge-to-edge with no overlap, which is what
# makes the impossible triangle read correctly in pure 2D.
PENROSE_FACES = [
    [(312.32408, 254.29303), (497.87767, 584.55178), (291.61277, 584.66663),
     (252.04899, 655.38029), (617.26698, 655.43727), (394.46457, 254.0866)],
    [(312.31392, 254.26591), (91.923882, 655.37223), (132.32998, 728.10322),
     (315.16759, 396.77318), (417.193, 584.66155), (498.0052, 584.66155)],
    [(315.20979, 396.83568), (355.50104, 471.05493), (251.87272, 655.43409),
     (617.28788, 655.62366), (578.81741, 730.12352), (132.3464, 728.07665)],
]


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


def fit_transform(faces, target=88.0):
    """Flip to screen coords, scale and centre the figure on the origin."""
    pts = [(x, -y) for poly in faces for (x, y) in poly]
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    scale = target / max(max(xs) - min(xs), max(ys) - min(ys))

    def transform(p):
        x, y = p
        return ((x - cx) * scale, (-y - cy) * scale)

    return transform


def grid_hatch(ax, poly, angle_deg, spacing, linewidth, alpha=1.0):
    """Fill a (possibly concave) polygon with parallel lines via scanline."""
    q = np.asarray(poly, dtype=float)
    a = np.radians(angle_deg)
    ca, sa = np.cos(a), np.sin(a)
    q = q @ np.array([[ca, sa], [-sa, ca]]).T
    ymin, ymax = q[:, 1].min(), q[:, 1].max()
    n = len(q)
    for y in np.arange(ymin + spacing * 0.5, ymax, spacing):
        xs = []
        for i in range(n):
            y1, y2 = q[i, 1], q[(i + 1) % n, 1]
            if (y1 <= y < y2) or (y2 <= y < y1):
                t = (y - y1) / (y2 - y1)
                xs.append(q[i, 0] + t * (q[(i + 1) % n, 0] - q[i, 0]))
        xs.sort()
        for j in range(0, len(xs) - 1, 2):
            x1, x2 = xs[j], xs[j + 1]
            if x2 - x1 < 1e-9:
                continue
            ax.plot(
                [ca * x1 - sa * y, ca * x2 - sa * y],
                [sa * x1 + ca * y, sa * x2 + ca * y],
                color="black",
                linewidth=linewidth,
                alpha=alpha,
                solid_capstyle="butt",
                zorder=3,
            )


def abstract_optical_Penrose_impossible_triangle_optical_grid_fusion_pattern_black_white_texture():
    """Penrose impossible triangle whose faces fuse with one shared isometric grid."""
    fig, ax = setup_ax()

    transform = fit_transform(PENROSE_FACES)
    faces = [[transform(p) for p in poly] for poly in PENROSE_FACES]

    # One isometric grid shared by every face -> the lines continue across the
    # beam edges, so the triangle appears "fused" into a single grid field.
    grid_angles = (0.0, 60.0, 120.0)
    spacing = 4.4
    for poly in faces:
        ax.add_patch(
            Polygon(poly, closed=True, facecolor="white", edgecolor="none", zorder=1)
        )
        for k, angle in enumerate(grid_angles):
            grid_hatch(ax, poly, angle, spacing, linewidth=0.55, alpha=0.9)

    # Beam boundaries on top keep the impossible-triangle structure readable.
    for poly in faces:
        ax.add_patch(
            Polygon(
                poly,
                closed=True,
                facecolor="none",
                edgecolor="black",
                linewidth=2.4,
                joinstyle="miter",
                zorder=4,
            )
        )

    save(
        fig,
        "abstract optical Penrose impossible triangle optical grid fusion pattern black white texture",
    )


if __name__ == "__main__":
    abstract_optical_Penrose_impossible_triangle_optical_grid_fusion_pattern_black_white_texture()
