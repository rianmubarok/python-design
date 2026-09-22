import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch, Ellipse, Circle
from matplotlib.path import Path as MPath
from pathlib import Path
from datetime import datetime

SIZE = 4000
DPI  = 300
PERIOD = 100.0
DATE = datetime.now().strftime("%d%m%Y")
WRAPS = [(i * PERIOD, j * PERIOD) for i in (-1, 0, 1) for j in (-1, 0, 1)]

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR  = SCRIPT_DIR.parent / "output"
JPG_DIR     = OUTPUT_DIR / "jpg"
SVG_DIR     = OUTPUT_DIR / "svg"
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


def draw_ghost_web(ax, cx, cy, s):
    """Ghost silhouette whose eye sockets are the hub centres of spider webs.
    The web radiates outward from each eye, filling the ghost's head.
    Ghost body is white; web lines are black drawn over the body.
    """
    # ── Ghost body silhouette ─────────────────────────────────────────────
    t_head = np.linspace(np.pi / 2, 0, 24)
    xh = cx + s * 0.30 * np.cos(t_head)
    yh = cy + s * 0.20 + s * 0.30 * np.sin(t_head)

    xbr = np.array([cx + s * 0.30, cx + s * 0.38, cx + s * 0.40])
    ybr = np.array([cy + s * 0.20, cy,             cy - s * 0.28])

    xw = np.linspace(cx + s * 0.40, cx - s * 0.40, 50)
    yw = (cy - s * 0.28) + s * 0.06 * np.sin((xw - cx) / (s * 0.40) * 2.5 * np.pi)

    xbl = np.array([cx - s * 0.40, cx - s * 0.38, cx - s * 0.30])
    ybl = np.array([cy - s * 0.28, cy,             cy + s * 0.20])

    t_head_l = np.linspace(np.pi, np.pi / 2, 24)
    xhl = cx + s * 0.30 * np.cos(t_head_l)
    yhl = cy + s * 0.20 + s * 0.30 * np.sin(t_head_l)

    pts_x = np.concatenate([xh, xbr, xw, xbl, xhl])
    pts_y = np.concatenate([yh, ybr, yw, ybl, yhl])
    pts   = np.column_stack([pts_x, pts_y])
    codes = [MPath.MOVETO] + [MPath.LINETO] * (len(pts) - 2) + [MPath.CLOSEPOLY]
    ax.add_patch(PathPatch(MPath(pts, codes), facecolor="white",
                           edgecolor="none", zorder=2))

    # ── Web from each eye socket ──────────────────────────────────────────
    eye_positions = [(cx - s * 0.115, cy + s * 0.255),
                     (cx + s * 0.115, cy + s * 0.255)]
    n_spokes  = 8
    n_rings   = 4
    web_r_max = s * 0.13

    for ex, ey in eye_positions:
        # spokes
        for k in range(n_spokes):
            ang = k * 2 * np.pi / n_spokes
            ax.plot([ex, ex + web_r_max * np.cos(ang)],
                    [ey, ey + web_r_max * np.sin(ang)],
                    color="black", linewidth=0.6, zorder=4)
        # concentric ring segments between spokes
        for ring in range(1, n_rings + 1):
            r = web_r_max * ring / n_rings
            for k in range(n_spokes):
                a0 = k * 2 * np.pi / n_spokes
                a1 = (k + 1) * 2 * np.pi / n_spokes
                theta = np.linspace(a0, a1, 12)
                ax.plot(ex + r * np.cos(theta), ey + r * np.sin(theta),
                        color="black", linewidth=0.6, zorder=4)

    # Small mouth dot
    ax.add_patch(Ellipse((cx, cy + s * 0.08), s * 0.07, s * 0.09,
                         facecolor="black", edgecolor="none", zorder=4))


def draw():
    """4×3 grid of ghost-web hybrid tiles, staggered rows. Black background."""
    fig, ax = setup_ax()
    cols, rows = 4, 3
    dx, dy = PERIOD / cols, PERIOD / rows
    s = min(dx, dy) * 0.80

    for row in range(rows):
        shift = dx * 0.5 if row % 2 else 0.0
        for col in range(cols):
            cx = (col + 0.5) * dx + shift
            cy = (row + 0.5) * dy
            for ox, oy in WRAPS:
                px, py = cx + ox, cy + oy
                if -20 <= px <= PERIOD + 20 and -20 <= py <= PERIOD + 20:
                    draw_ghost_web(ax, px, py, s)

    save(fig,
         "abstract halloween variation ghost face spider web radial hub "
         "eye socket combo pattern black white texture")


if __name__ == "__main__":
    draw()
