import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch, FancyBboxPatch, Ellipse, Polygon
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


def draw_tombstone(ax, cx, cy, w, h, fill="white", zorder=2):
    r = w * 0.5
    ax.add_patch(FancyBboxPatch(
        (cx - w/2, cy - h/2), w, h * 0.62,
        boxstyle="square,pad=0",
        facecolor=fill, edgecolor="none", zorder=zorder))
    t = np.linspace(0, np.pi, 40)
    arch = np.column_stack([cx + r*np.cos(t), cy + h*0.12 + r*np.sin(t)])
    arch = np.vstack([[cx-r, cy+h*0.12], arch, [cx+r, cy+h*0.12]])
    ax.add_patch(Polygon(arch, closed=True, facecolor=fill, edgecolor="none", zorder=zorder))


def draw_ghost_rising(ax, cx, cy, s, fill="white"):
    """Ghost with fading trail — body + shorter wispy tail, no wave."""
    inv = "black" if fill == "white" else "white"
    t_r = np.linspace(np.pi/2, 0, 16)
    xr = cx + s*0.24*np.cos(t_r); yr = cy + s*0.20 + s*0.24*np.sin(t_r)
    xbr = np.array([cx+s*0.24, cx+s*0.28, cx+s*0.22])
    ybr = np.array([cy+s*0.20, cy+s*0.05, cy-s*0.20])
    xbl = np.array([cx-s*0.22, cx-s*0.28, cx-s*0.24])
    ybl = np.array([cy-s*0.20, cy+s*0.05, cy+s*0.20])
    t_l = np.linspace(np.pi, np.pi/2, 16)
    xl = cx + s*0.24*np.cos(t_l); yl = cy+s*0.20+s*0.24*np.sin(t_l)
    pts_x = np.concatenate([xr, xbr, xbl[::-1], xl])
    pts_y = np.concatenate([yr, ybr, ybl[::-1], yl])
    codes = [MPath.MOVETO]+[MPath.LINETO]*(len(pts_x)-2)+[MPath.CLOSEPOLY]
    ax.add_patch(PathPatch(MPath(np.column_stack([pts_x, pts_y]), codes),
                           facecolor=fill, edgecolor="none", zorder=4))
    for ex in (-s*0.08, s*0.08):
        ax.add_patch(Ellipse((cx+ex, cy+s*0.18), s*0.065, s*0.085,
                             facecolor=inv, edgecolor="none", zorder=5))


def draw_crescent_moon(ax, cx, cy, r, tilt, fill="white"):
    n = 120
    od = r * 0.42
    t_o = np.linspace(-np.pi*0.60, np.pi*0.60, n)
    ox = cx + r*np.cos(t_o); oy = cy + r*np.sin(t_o)
    pcx = cx + od
    p1 = (ox[-1]-pcx, oy[-1]-cy); p2 = (ox[0]-pcx, oy[0]-cy)
    a1 = np.arctan2(p1[1], p1[0]); a2 = np.arctan2(p2[1], p2[0])
    ri = np.hypot(p1[0], p1[1])
    t_i = np.linspace(a1, a2, n)
    ix = pcx + ri*np.cos(t_i); iy = cy + ri*np.sin(t_i)
    px = np.concatenate([ox, ix])-cx; py = np.concatenate([oy, iy])-cy
    rx = px*np.cos(tilt)-py*np.sin(tilt)+cx
    ry = px*np.sin(tilt)+py*np.cos(tilt)+cy
    ax.add_patch(Polygon(np.column_stack([rx, ry]),
                         closed=True, facecolor=fill, edgecolor="none", zorder=3))


def draw():
    """Repeating landscape stripe: bottom third = tombstone row, middle = ghosts rising,
    top = scattered crescents. Horizontally repeating seamless band tile.
    Tile is 1 wide × 3 rows tall, stacked vertically."""
    fig, ax = setup_ax()

    tile_w = PERIOD / 3   # 3 column tiles
    tile_h = PERIOD / 2   # 2 row tiles

    rng = np.random.default_rng(17)

    for tile_col in range(-1, 3 + 1):
        for tile_row in range(-1, 2 + 1):
            tx = tile_col * tile_w
            ty = tile_row * tile_h

            for ox, oy in WRAPS:
                bx = tx + ox
                by = ty + oy
                if bx < -tile_w or bx > PERIOD + tile_w:
                    continue
                if by < -tile_h or by > PERIOD + tile_h:
                    continue

                # ── Tombstones (bottom band) ──
                n_t = 3
                for i in range(n_t):
                    xf = (i + 0.5) / n_t
                    stone_cx = bx + xf * tile_w
                    stone_cy = by + tile_h * 0.20
                    w = tile_w * 0.18
                    h = tile_h * 0.32
                    draw_tombstone(ax, stone_cx, stone_cy, w, h)

                # ── Ghosts rising ──
                n_g = 2
                for i in range(n_g):
                    xf = (i + 0.5) / n_g
                    ghost_cx = bx + xf * tile_w + rng.uniform(-0.05, 0.05)*tile_w
                    ghost_cy = by + tile_h * 0.52
                    draw_ghost_rising(ax, ghost_cx, ghost_cy, tile_h * 0.14)

                # ── Crescent moons (top band) ──
                moon_cx = bx + tile_w * rng.uniform(0.2, 0.8)
                moon_cy = by + tile_h * 0.82
                draw_crescent_moon(ax, moon_cx, moon_cy, tile_h*0.10,
                                   tilt=np.radians(30))

    save(fig, "abstract halloween variation tombstone ghost rising crescent arc scattered landscape pattern black white texture")


if __name__ == "__main__":
    draw()
