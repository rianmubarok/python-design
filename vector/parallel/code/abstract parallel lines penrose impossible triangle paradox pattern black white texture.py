import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime

SIZE = 4000
DPI = 300
DATE = datetime.now().strftime("%d%m%Y")

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR.parent / "output"
JPG_DIR = OUTPUT_DIR / "jpg"
SVG_DIR = OUTPUT_DIR / "svg"
JPG_DIR.mkdir(parents=True, exist_ok=True)
SVG_DIR.mkdir(parents=True, exist_ok=True)

# The three visible faces of a Penrose tribar (isometric), each an L-shaped
# hexagon. They tile the figure edge-to-edge with no overlap. Angle = hatch
# direction, aligned with the long arm of each face.
PENROSE_FACES = [
    ([(312.32408, 254.29303), (497.87767, 584.55178), (291.61277, 584.66663),
      (252.04899, 655.38029), (617.26698, 655.43727), (394.46457, 254.0866)], 120.0),
    ([(312.31392, 254.26591), (91.923882, 655.37223), (132.32998, 728.10322),
      (315.16759, 396.77318), (417.193, 584.66155), (498.0052, 584.66155)], 60.0),
    ([(315.20979, 396.83568), (355.50104, 471.05493), (251.87272, 655.43409),
      (617.28788, 655.62366), (578.81741, 730.12352), (132.3464, 728.07665)], 0.0),
]


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


def make_transform(faces):
    """Fit/flip the raw figure onto the 0-100 drawing area, centred in canvas."""
    pts = [(x, -y) for poly, _ in faces for (x, y) in poly]
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    minx, maxx, miny, maxy = min(xs), max(xs), min(ys), max(ys)
    cx, cy = (minx + maxx) / 2, (miny + maxy) / 2
    scale = 100.0 / max(maxx - minx, maxy - miny)

    def transform(p):
        x, y = p
        return (50 + (x - cx) * scale, 50 + (-y - cy) * scale)

    return transform


def hatch_polygon(ax, poly, angle_deg, spacing, linewidth):
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
                solid_capstyle="butt",
            )


def draw():
    """Penrose impossible triangle paradox pattern built from parallel lines."""
    fig, ax = setup_ax()
    transform = make_transform(PENROSE_FACES)

    for poly, angle in PENROSE_FACES:
        transformed = [transform(p) for p in poly]
        hatch_polygon(ax, transformed, angle, spacing=0.45, linewidth=0.3)
        outline = np.array(transformed + [transformed[0]])
        ax.plot(
            outline[:, 0],
            outline[:, 1],
            color="black",
            linewidth=1.1,
            solid_capstyle="round",
        )

    save(fig, "abstract parallel lines penrose impossible triangle paradox pattern black white texture")


if __name__ == "__main__":
    draw()
