import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, FancyBboxPatch, Polygon
from scipy.spatial import Voronoi
from pathlib import Path
from datetime import datetime

SIZE = 4000
DPI = 300
PERIOD = 100.0
DATE = datetime.now().strftime("%d%m%Y")

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR.parent / "output"
JPG_DIR = OUTPUT_DIR / "jpg"
SVG_DIR = OUTPUT_DIR / "svg"
JPG_DIR.mkdir(parents=True, exist_ok=True)
SVG_DIR.mkdir(parents=True, exist_ok=True)


def setup_ax():
    fig, ax = plt.subplots(figsize=(SIZE / DPI, SIZE / DPI), dpi=DPI)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.set_facecolor("black")
    ax.set_xlim(0, PERIOD)
    ax.set_ylim(0, PERIOD)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def save(fig, name):
    jpg_path = JPG_DIR / f"{name} {DATE}.jpg"
    svg_path = SVG_DIR / f"{name} {DATE}.svg"
    fig.savefig(jpg_path, dpi=DPI, pad_inches=0, facecolor="black")
    fig.savefig(svg_path, format="svg", pad_inches=0, facecolor="black")
    plt.close(fig)
    print(f"Saved: {jpg_path} | {svg_path}")


def mini_skull(ax, cx, cy, s, fill="white", inv="black"):
    """Compact skull — cranium + jaw + eyes + nose + 3 teeth."""
    ax.add_patch(Ellipse((cx, cy + 0.16*s), 0.78*s, 0.70*s, facecolor=fill, edgecolor="none"))
    ax.add_patch(FancyBboxPatch((cx-0.24*s, cy-0.22*s), 0.48*s, 0.24*s,
                                boxstyle=f"round,pad=0,rounding_size={0.04*s:.4f}",
                                facecolor=fill, edgecolor="none"))
    for sx in (-0.16*s, 0.16*s):
        ax.add_patch(Ellipse((cx+sx, cy+0.18*s), 0.20*s, 0.22*s, facecolor=inv, edgecolor="none"))
    ax.add_patch(Polygon([[cx,cy+0.03*s],[cx-0.065*s,cy-0.07*s],[cx+0.065*s,cy-0.07*s]],
                          closed=True, facecolor=inv, edgecolor="none"))
    for x in (-0.12*s, 0.0, 0.12*s):
        ax.add_patch(FancyBboxPatch((cx+x-0.026*s,cy-0.19*s),0.050*s,0.105*s,
                                    facecolor=inv, edgecolor="none"))


def clip_polygon_to_box(pts, x0, y0, x1, y1):
    """Sutherland-Hodgman clip polygon to axis-aligned box."""
    def clip_edge(pts, a, b):
        result = []
        n = len(pts)
        if n == 0:
            return result
        def inside(p):
            return (b[0]-a[0])*(p[1]-a[1]) - (b[1]-a[1])*(p[0]-a[0]) >= 0
        def intersect(p, q):
            dx,dy = b[0]-a[0],b[1]-a[1]
            ex,ey = q[0]-p[0],q[1]-p[1]
            denom = dx*ey-dy*ex
            if abs(denom) < 1e-10:
                return p
            t = ((a[0]-p[0])*ey-(a[1]-p[1])*ex)/denom
            return (p[0]+t*dx, p[1]+t*dy)
        for i in range(n):
            cur, nxt = pts[i], pts[(i+1)%n]
            if inside(nxt):
                if not inside(cur):
                    result.append(intersect(cur, nxt))
                result.append(nxt)
            elif inside(cur):
                result.append(intersect(cur, nxt))
        return result

    edges = [
        ((x0,y0),(x1,y0)),
        ((x1,y0),(x1,y1)),
        ((x1,y1),(x0,y1)),
        ((x0,y1),(x0,y0)),
    ]
    clipped = list(map(tuple, pts))
    for a, b in edges:
        clipped = clip_edge(clipped, a, b)
        if not clipped:
            return []
    return clipped


def draw():
    """Voronoi cell layout — each cell is filled alternating black/white and gets
    a skull face sized to fit inside the cell's bounding region."""
    fig, ax = setup_ax()
    rng = np.random.default_rng(42)
    n_seeds = 40

    # tile with 3×3 mirrored seeds for seamless Voronoi
    base_pts = rng.uniform(0, PERIOD, (n_seeds, 2))
    # replicate 3×3
    all_pts = []
    for di in (-1, 0, 1):
        for dj in (-1, 0, 1):
            all_pts.append(base_pts + [di*PERIOD, dj*PERIOD])
    all_pts = np.vstack(all_pts)

    vor = Voronoi(all_pts)

    # for each base seed (the n_seeds in tile (0,0)), draw its cell
    offset_idx = 4 * n_seeds   # index of (0,0) tile seeds: (1*3+1)*n_seeds
    for i in range(n_seeds):
        seed_idx = offset_idx + i
        region_idx = vor.point_region[seed_idx]
        region = vor.regions[region_idx]
        if -1 in region or len(region) == 0:
            continue
        verts = vor.vertices[region]
        # clip to [0,PERIOD]
        clipped = clip_polygon_to_box(verts.tolist(), 0, 0, PERIOD, PERIOD)
        if len(clipped) < 3:
            continue
        clipped_arr = np.array(clipped)
        fill = "white" if i % 2 == 0 else "none"
        ec = "white"
        ax.add_patch(Polygon(clipped_arr, closed=True,
                             facecolor=fill, edgecolor=ec, linewidth=0.6))

        # compute centroid and bounding radius of clipped cell
        cx_c = np.mean(clipped_arr[:, 0])
        cy_c = np.mean(clipped_arr[:, 1])
        dists = np.hypot(clipped_arr[:, 0]-cx_c, clipped_arr[:, 1]-cy_c)
        cell_r = np.min(dists) * 0.72

        sk_fill = "black" if fill == "white" else "white"
        sk_inv  = "white" if sk_fill == "black" else "black"
        mini_skull(ax, cx_c, cy_c, cell_r, fill=sk_fill, inv=sk_inv)

    save(fig, "abstract halloween variation voronoi cell skull face per region halloween pattern black white texture")


if __name__ == "__main__":
    draw()
