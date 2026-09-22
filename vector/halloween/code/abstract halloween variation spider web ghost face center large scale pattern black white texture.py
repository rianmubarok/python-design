import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch, Ellipse
from matplotlib.path import Path as MPath
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


def draw_ghost_face_web(ax, cx, cy, tile_w, tile_h, n_spokes=10, n_rings=7):
    """Giant spider web centred at (cx, cy).
    Spokes extend to the full tile-half-diagonal so they always reach the corners,
    ensuring seamless connection between adjacent tiles.
    Ghost-face silhouette sits at the hub."""

    # Reach far enough to cover the tile corner
    half_diag = 0.5 * np.hypot(tile_w, tile_h)
    max_r = half_diag   # spokes reach corners — seamless coverage

    lw_spoke = 0.9
    lw_ring = 0.70

    spoke_angles = [k * 2 * np.pi / n_spokes for k in range(n_spokes)]
    ring_radii = [max_r * (k + 1) / n_rings for k in range(n_rings)]

    # ── Web structure ──
    for a in spoke_angles:
        ax.plot([cx, cx + max_r * np.cos(a)],
                [cy, cy + max_r * np.sin(a)],
                color="white", linewidth=lw_spoke, zorder=2)

    for r in ring_radii:
        for k in range(n_spokes):
            a1, a2 = spoke_angles[k], spoke_angles[(k + 1) % n_spokes]
            t = np.linspace(a1, a2, 20)
            ax.plot(cx + r * np.cos(t), cy + r * np.sin(t),
                    color="white", linewidth=lw_ring, zorder=2)

    # ── Ghost face at hub ──
    head_r = max_r * 0.13   # slightly smaller relative to the larger max_r

    t_r = np.linspace(np.pi / 2, 0, 14)
    xr = cx + head_r * np.cos(t_r)
    yr = cy + head_r * 0.24 + head_r * np.sin(t_r)

    xbr = np.array([cx + head_r, cx + head_r * 1.28, cx + head_r * 1.30])
    ybr = np.array([cy + head_r * 0.24, cy, cy - head_r * 0.88])

    x_wv = np.linspace(cx + head_r * 1.30, cx - head_r * 1.30, 24)
    y_wv = cy - head_r * 0.88 + head_r * 0.20 * np.sin(
        (x_wv - cx) / (head_r * 1.30) * 2.5 * np.pi)

    xbl = np.array([cx - head_r * 1.30, cx - head_r * 1.28, cx - head_r])
    ybl = np.array([cy - head_r * 0.88, cy, cy + head_r * 0.24])

    t_l = np.linspace(np.pi, np.pi / 2, 14)
    xl = cx + head_r * np.cos(t_l)
    yl = cy + head_r * 0.24 + head_r * np.sin(t_l)

    pts_x = np.concatenate([xr, xbr, x_wv, xbl, xl])
    pts_y = np.concatenate([yr, ybr, y_wv, ybl, yl])
    codes = [MPath.MOVETO] + [MPath.LINETO] * (len(pts_x) - 2) + [MPath.CLOSEPOLY]
    ax.add_patch(PathPatch(MPath(np.column_stack([pts_x, pts_y]), codes),
                           facecolor="white", edgecolor="none", zorder=3))

    # Eyes
    for ex in (-head_r * 0.38, head_r * 0.38):
        ax.add_patch(Ellipse((cx + ex, cy + head_r * 0.24),
                             head_r * 0.28, head_r * 0.36,
                             facecolor="black", edgecolor="none", zorder=4))
    # Mouth
    ax.add_patch(Ellipse((cx, cy - head_r * 0.10),
                         head_r * 0.22, head_r * 0.26,
                         facecolor="black", edgecolor="none", zorder=4))


def draw():
    """2×2 large tiles. Each tile = full ghost-face-web filling the entire cell.
    Spokes extend to the tile corner (half-diagonal) so they connect seamlessly
    with adjacent tiles at the edges — no dark gaps."""
    fig, ax = setup_ax()

    cols, rows = 2, 2
    dx, dy = PERIOD / cols, PERIOD / rows

    for row in range(-1, rows + 1):
        for col in range(-1, cols + 1):
            cx = (col + 0.5) * dx
            cy = (row + 0.5) * dy
            for ox, oy in WRAPS:
                px, py = cx + ox, cy + oy
                if -30 <= px <= PERIOD + 30 and -30 <= py <= PERIOD + 30:
                    draw_ghost_face_web(ax, px, py, dx, dy,
                                       n_spokes=10, n_rings=7)

    save(fig, "abstract halloween variation spider web ghost face center large scale pattern black white texture")


if __name__ == "__main__":
    draw()
