import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, FancyBboxPatch, Polygon
from matplotlib.transforms import Affine2D
from pathlib import Path
from datetime import datetime

SIZE = 4000
DPI = 300
PERIOD = 100.0
DATE = datetime.now().strftime("%d%m%Y")
WRAPS = [(i * PERIOD, j * PERIOD) for i in (-1, 0, 1) for j in (-1, 0, 1)]

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR.parent / "output"
JPG_DIR = OUTPUT_DIR / "jpg"
SVG_DIR = OUTPUT_DIR / "svg"
JPG_DIR.mkdir(parents=True, exist_ok=True)
SVG_DIR.mkdir(parents=True, exist_ok=True)


def setup_ax():
    fig, ax = plt.subplots(figsize=(SIZE / DPI, SIZE / DPI), dpi=DPI)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.set_facecolor("white")
    ax.set_xlim(0, PERIOD)
    ax.set_ylim(0, PERIOD)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def save(fig, name):
    jpg_path = JPG_DIR / f"{name} {DATE}.jpg"
    svg_path = SVG_DIR / f"{name} {DATE}.svg"
    fig.savefig(jpg_path, dpi=DPI, pad_inches=0, facecolor="white")
    fig.savefig(svg_path, format="svg", pad_inches=0, facecolor="white")
    plt.close(fig)
    print(f"Saved: {jpg_path} | {svg_path}")


def eye_web(ax, ex, ey, eye_r, n_spokes=8, n_rings=5, col="black"):
    """Mini spider web filling the eye socket area."""
    angles = np.linspace(0, 2 * np.pi, n_spokes, endpoint=False)
    radii = np.linspace(eye_r * 0.18, eye_r * 0.92, n_rings)
    for a in angles:
        ax.plot([ex, ex + eye_r * np.cos(a)],
                [ey, ey + eye_r * np.sin(a)],
                color=col, linewidth=0.45, solid_capstyle="round")
    for r in radii:
        pts = np.array([[ex + r * np.cos(a), ey + r * np.sin(a)]
                        for a in angles])
        pts = np.vstack([pts, pts[0]])
        ax.plot(pts[:, 0], pts[:, 1], color=col, linewidth=0.35)


def web_strands_from_eye(ax, ex, ey, eye_r, s, col="black"):
    """Longer web strands radiating out from eye socket into surrounding area."""
    n_long = 6
    angles = np.linspace(np.pi * 0.3, np.pi * 1.9, n_long)
    for a in angles:
        length = s * np.random.uniform(0.25, 0.55)
        end_x = ex + length * np.cos(a)
        end_y = ey + length * np.sin(a)
        ax.plot([ex, end_x], [ey, end_y],
                color=col, linewidth=0.38, alpha=0.7)
        # small connecting arcs between strands at various distances
        for frac in (0.35, 0.65, 0.90):
            r = length * frac
            a2 = a + 2 * np.pi / n_long
            x2 = ex + length * frac * np.cos(a2)
            y2 = ey + length * frac * np.sin(a2)
            mx = ex + r * np.cos(a)
            my = ey + r * np.sin(a)
            ax.plot([mx, x2], [my, y2], color=col, linewidth=0.30, alpha=0.5)


def skull_with_webs(ax, cx, cy, s):
    """Skull silhouette (black on white) with web strands growing out of eye sockets."""
    np.random.seed(int((cx * 7 + cy * 13) % 1000))
    # crossbones
    for ang in (35, -35):
        tr = Affine2D().rotate_deg(ang).translate(cx, cy - 0.42 * s) + ax.transData
        ax.add_patch(FancyBboxPatch(
            (-0.58 * s, -0.05 * s), 1.16 * s, 0.10 * s,
            boxstyle=f"round,pad=0,rounding_size={0.046*s:.4f}",
            facecolor="black", edgecolor="none", transform=tr))
        for end in (-0.57 * s, 0.57 * s):
            ax.add_patch(Circle((end, 0), 0.08 * s, facecolor="black",
                                edgecolor="none", transform=tr))
    # cranium
    ax.add_patch(Ellipse((cx, cy + 0.14 * s), 0.80 * s, 0.72 * s,
                         facecolor="black", edgecolor="none"))
    # jaw
    ax.add_patch(FancyBboxPatch(
        (cx - 0.26 * s, cy - 0.22 * s), 0.52 * s, 0.23 * s,
        boxstyle=f"round,pad=0,rounding_size={0.04*s:.4f}",
        facecolor="black", edgecolor="none"))
    # eye socket positions
    eye_data = [(-0.17 * s, cy + 0.19 * s), (0.17 * s, cy + 0.19 * s)]
    eye_r = 0.10 * s
    for (ex_off, ey) in eye_data:
        ex = cx + ex_off
        # white socket
        ax.add_patch(Circle((ex, ey), eye_r * 1.55,
                            facecolor="white", edgecolor="none"))
        # web inside socket
        eye_web(ax, ex, ey, eye_r * 1.45, n_spokes=7, n_rings=4, col="black")
        # web strands radiating outward
        web_strands_from_eye(ax, ex, ey, eye_r * 1.45, s, col="black")
    # nose
    ax.add_patch(Polygon(
        np.array([[cx, cy + 0.02 * s],
                  [cx - 0.065 * s, cy - 0.075 * s],
                  [cx + 0.065 * s, cy - 0.075 * s]]),
        closed=True, facecolor="white", edgecolor="none"))
    # teeth
    for tx in (-0.12 * s, 0.0, 0.12 * s):
        ax.add_patch(FancyBboxPatch(
            (cx + tx - 0.026 * s, cy - 0.19 * s), 0.052 * s, 0.105 * s,
            boxstyle="round,pad=0,rounding_size=0.005",
            facecolor="white", edgecolor="none"))


def draw():
    """4×4 staggered grid — each skull has spider web strands
    growing from the eye sockets like an overgrown haunted skull."""
    fig, ax = setup_ax()
    cols, rows = 4, 4
    dx, dy = PERIOD / cols, PERIOD / rows
    s = min(dx, dy) * 0.74

    for row in range(rows):
        for col in range(cols):
            cx = (col + 0.5) * dx + (dx * 0.5 if row % 2 else 0)
            cy = (row + 0.5) * dy
            for ox, oy in WRAPS:
                skull_with_webs(ax, cx + ox, cy + oy, s)

    save(fig, "abstract halloween variation skull spider web overgrown eye socket strands pattern black white texture")


if __name__ == "__main__":
    draw()
