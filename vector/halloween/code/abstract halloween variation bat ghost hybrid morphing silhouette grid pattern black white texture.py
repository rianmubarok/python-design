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


def bat_ghost_morph(ax, cx, cy, w, h, t=0.5, fill="white"):
    """Morphed silhouette: t=0 → pure ghost, t=1 → pure bat.
    Interpolates between ghost body (rounded dome + wavy hem) and bat wings."""
    inv = "black" if fill == "white" else "white"

    # ── Ghost shape points (local coords centred at 0,0) ──
    t_r = np.linspace(np.pi/2, 0, 16)
    gx_r = w * 0.28 * np.cos(t_r)
    gy_r = h * 0.24 + w * 0.28 * np.sin(t_r)
    gbr_x = np.array([w*0.28, w*0.35, w*0.37])
    gbr_y = np.array([h*0.24, 0.0, -h*0.26])
    x_wv = np.linspace(w*0.37, -w*0.37, 30)
    y_wv = -h*0.26 + h*0.055 * np.sin(x_wv / (w*0.37) * 2.5*np.pi)
    gbl_x = np.array([-w*0.37, -w*0.35, -w*0.28])
    gbl_y = np.array([-h*0.26, 0.0, h*0.24])
    t_l = np.linspace(np.pi, np.pi/2, 16)
    gx_l = w * 0.28 * np.cos(t_l)
    gy_l = h * 0.24 + w * 0.28 * np.sin(t_l)
    ghost_x = np.concatenate([gx_r, gbr_x, x_wv, gbl_x, gx_l])
    ghost_y = np.concatenate([gy_r, gbr_y, y_wv, gbl_y, gy_l])
    n_pts = len(ghost_x)

    # ── Bat shape points (same count as ghost, resampled) ──
    bat_raw_x = np.array([0, w*0.22, w*0.50, w*0.42, w*0.20, w*0.08,
                           -w*0.08, -w*0.20, -w*0.42, -w*0.50, -w*0.22, 0])
    bat_raw_y = np.array([0, h*0.28, h*0.14, -h*0.22, -h*0.08, 0,
                           0, -h*0.08, -h*0.22, h*0.14, h*0.28, 0])
    # Resample bat shape to n_pts
    from scipy.interpolate import interp1d
    t_bat = np.linspace(0, 1, len(bat_raw_x))
    t_new = np.linspace(0, 1, n_pts)
    bat_x = interp1d(t_bat, bat_raw_x, kind="linear")(t_new)
    bat_y = interp1d(t_bat, bat_raw_y, kind="linear")(t_new)

    # ── Interpolate ──
    mix_x = (1 - t) * ghost_x + t * bat_x + cx
    mix_y = (1 - t) * ghost_y + t * bat_y + cy

    pts = np.column_stack([mix_x, mix_y])
    codes = [MPath.MOVETO] + [MPath.LINETO]*(len(pts)-2) + [MPath.CLOSEPOLY]
    ax.add_patch(PathPatch(MPath(pts, codes),
                           facecolor=fill, edgecolor="none", zorder=2))

    # Eyes
    for ex in (-w*0.09, w*0.09):
        ax.add_patch(Ellipse((cx+ex, cy + h*0.20*(1-t) + h*0.10*t),
                             w*0.07*(1-t) + w*0.04*t,
                             h*0.10*(1-t) + h*0.06*t,
                             facecolor=inv, edgecolor="none", zorder=3))


def draw():
    """4×5 grid with morph parameter t increasing left→right, top→bottom.
    Top rows look ghost-like; bottom rows look bat-like. Creates a visual
    metamorphosis across the tile. Diagonal morph gradient."""
    fig, ax = setup_ax()

    cols, rows = 5, 5
    dx, dy = PERIOD / cols, PERIOD / rows
    w = dx * 0.70
    h = dy * 0.70

    for row in range(-1, rows + 1):
        shift = (dx * 0.5) if row % 2 else 0.0
        for col in range(-1, cols + 2):
            # morph t: 0=ghost (top-left) … 1=bat (bottom-right)
            t_val = ((col % cols) + (row % rows)) / (cols + rows - 2.0)
            t_val = np.clip(t_val, 0.0, 1.0)
            cx = (col + 0.5) * dx + shift
            cy = (row + 0.5) * dy
            for ox, oy in WRAPS:
                px, py = cx + ox, cy + oy
                if -15 <= px <= PERIOD + 15 and -15 <= py <= PERIOD + 15:
                    bat_ghost_morph(ax, px, py, w, h, t=t_val, fill="white")

    save(fig, "abstract halloween variation bat ghost hybrid morphing silhouette grid pattern black white texture")


if __name__ == "__main__":
    draw()
