import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch, Ellipse, Circle, Polygon
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


def draw_ghost_mini(ax, cx, cy, s, fill="white"):
    inv = "black" if fill == "white" else "white"
    t_r = np.linspace(np.pi/2, 0, 14)
    x_r = cx + s*0.26 * np.cos(t_r); y_r = cy + s*0.22 + s*0.26 * np.sin(t_r)
    x_br = np.array([cx+s*0.26, cx+s*0.33, cx+s*0.34])
    y_br = np.array([cy+s*0.22, cy, cy-s*0.24])
    x_wv = np.linspace(cx+s*0.34, cx-s*0.34, 30)
    y_wv = cy-s*0.24 + s*0.05*np.sin((x_wv-cx)/(s*0.34)*2.5*np.pi)
    x_bl = np.array([cx-s*0.34, cx-s*0.33, cx-s*0.26])
    y_bl = np.array([cy-s*0.24, cy, cy+s*0.22])
    t_l = np.linspace(np.pi, np.pi/2, 14)
    x_l = cx + s*0.26*np.cos(t_l); y_l = cy+s*0.22+s*0.26*np.sin(t_l)
    pts_x = np.concatenate([x_r, x_br, x_wv, x_bl, x_l])
    pts_y = np.concatenate([y_r, y_br, y_wv, y_bl, y_l])
    codes = [MPath.MOVETO]+[MPath.LINETO]*(len(pts_x)-2)+[MPath.CLOSEPOLY]
    ax.add_patch(PathPatch(MPath(np.column_stack([pts_x, pts_y]), codes),
                           facecolor=fill, edgecolor="none", zorder=3))
    for ex in (-s*0.085, s*0.085):
        ax.add_patch(Ellipse((cx+ex, cy+s*0.20), s*0.065, s*0.09,
                             facecolor=inv, edgecolor="none", zorder=4))


def draw_bat_mini(ax, cx, cy, w, h, fill="white"):
    pts = np.array([
        [cx,       cy],
        [cx+w*0.22, cy+h*0.26],
        [cx+w*0.48, cy+h*0.12],
        [cx+w*0.40, cy-h*0.20],
        [cx+w*0.18, cy-h*0.07],
        [cx+w*0.07, cy],
        [cx-w*0.07, cy],
        [cx-w*0.18, cy-h*0.07],
        [cx-w*0.40, cy-h*0.20],
        [cx-w*0.48, cy+h*0.12],
        [cx-w*0.22, cy+h*0.26],
        [cx,       cy],
    ])
    codes = [MPath.MOVETO]+[MPath.LINETO]*(len(pts)-2)+[MPath.CLOSEPOLY]
    ax.add_patch(PathPatch(MPath(pts, codes), facecolor=fill, edgecolor="none", zorder=3))
    ax.add_patch(Circle((cx, cy+h*0.12), w*0.06,
                        facecolor=fill, edgecolor="none", zorder=4))


def draw():
    """3×3 hub tiles. Each hub has:
    - A small ghost orbiting at radius r1 (at 60° position)
    - A small bat orbiting at radius r1 (at 240° position, opposite)
    - A faint crescent arc trail connecting their orbit path
    The duo spins around a small white hub dot."""
    fig, ax = setup_ax()

    cols, rows = 3, 3
    dx, dy = PERIOD / cols, PERIOD / rows
    orbit_r = min(dx, dy) * 0.30
    ghost_s = min(dx, dy) * 0.14
    bat_w   = min(dx, dy) * 0.22
    bat_h   = min(dx, dy) * 0.16

    for row in range(-1, rows + 1):
        shift = (dx * 0.5) if row % 2 else 0.0
        for col in range(-1, cols + 2):
            hub_x = (col + 0.5) * dx + shift
            hub_y = (row + 0.5) * dy
            base_a = np.radians(60) if (row + col) % 2 == 0 else np.radians(30)

            for ox, oy in WRAPS:
                px, py = hub_x + ox, hub_y + oy
                if -20 <= px <= PERIOD + 20 and -20 <= py <= PERIOD + 20:
                    # Orbit arc (faint dotted trail)
                    t_arc = np.linspace(0, 2*np.pi, 120)
                    ax.plot(px + orbit_r * np.cos(t_arc),
                            py + orbit_r * np.sin(t_arc),
                            color="white", linewidth=0.5, alpha=0.30, zorder=1)

                    # Ghost at base_a angle
                    gx = px + orbit_r * np.cos(base_a)
                    gy = py + orbit_r * np.sin(base_a)
                    draw_ghost_mini(ax, gx, gy, ghost_s, fill="white")

                    # Bat at opposite angle
                    bx = px + orbit_r * np.cos(base_a + np.pi)
                    by = py + orbit_r * np.sin(base_a + np.pi)
                    draw_bat_mini(ax, bx, by, bat_w, bat_h, fill="white")

                    # Hub dot
                    ax.add_patch(Circle((px, py), orbit_r * 0.06,
                                       facecolor="white", edgecolor="none", zorder=5))

    save(fig, "abstract halloween variation ghost bat orbit duo crescent arc trail pattern black white texture")


if __name__ == "__main__":
    draw()
