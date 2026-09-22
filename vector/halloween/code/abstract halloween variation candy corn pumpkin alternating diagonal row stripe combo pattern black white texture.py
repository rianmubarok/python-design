import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch, Ellipse, FancyBboxPatch, Polygon
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


def draw_candy_corn(ax, cx, cy, h, w_base, fill="white", mid="#777777"):
    tip_y = cy + h * 0.5
    base_y = cy - h * 0.5
    mid_y1 = cy - h * 0.10
    mid_y2 = cy - h * 0.38
    w_mid = w_base * 0.60
    base_pts = [[cx-w_base/2, base_y],[cx+w_base/2, base_y],
                [cx+w_mid/2, mid_y1],[cx-w_mid/2, mid_y1]]
    mid_pts  = [[cx-w_mid/2, mid_y1],[cx+w_mid/2, mid_y1],
                [cx+w_base*0.18, mid_y2],[cx-w_base*0.18, mid_y2]]
    tip_pts  = [[cx-w_base*0.18, mid_y2],[cx+w_base*0.18, mid_y2],[cx, tip_y]]
    ax.add_patch(Polygon(base_pts, closed=True, facecolor=fill, edgecolor="none"))
    ax.add_patch(Polygon(mid_pts,  closed=True, facecolor=mid,  edgecolor="none"))
    ax.add_patch(Polygon(tip_pts,  closed=True, facecolor=fill, edgecolor="none"))


def draw_pumpkin(ax, cx, cy, s, fill="white"):
    inv = "black" if fill == "white" else "white"
    for ddx in (-s*0.22, 0.0, s*0.22):
        ax.add_patch(Ellipse((cx+ddx, cy), s*0.30, s*0.48,
                             facecolor=fill, edgecolor="none"))
    ax.add_patch(FancyBboxPatch(
        (cx-s*0.04, cy+s*0.24), s*0.08, s*0.13,
        boxstyle=f"round,pad=0,rounding_size={s*0.015:.4f}",
        facecolor=fill, edgecolor="none"))
    for ex in (-s*0.13, s*0.13):
        ax.add_patch(Polygon([[cx+ex,cy+s*0.12],[cx+ex-s*0.07,cy-s*0.01],
                               [cx+ex+s*0.07,cy-s*0.01]],
                             closed=True, facecolor=inv, edgecolor="none"))
    x_m = np.array([-0.16,-0.10,-0.04,0.04,0.10,0.16])*s+cx
    y_m = np.array([-0.13,-0.07,-0.13,-0.07,-0.13,-0.07])*s+cy
    x_c = np.array([0.16,0.16,-0.16,-0.16])*s+cx
    y_c = np.array([-0.07,-0.17,-0.17,-0.13])*s+cy
    mx = np.concatenate([x_m,x_c]); my = np.concatenate([y_m,y_c])
    codes = [MPath.MOVETO]+[MPath.LINETO]*(len(mx)-2)+[MPath.CLOSEPOLY]
    ax.add_patch(PathPatch(MPath(np.column_stack([mx,my]),codes),
                           facecolor=inv, edgecolor="none"))


def draw():
    """Diagonal stripe combo: (col-row)%2==0 → candy corn column, else → pumpkin.
    Both motifs share the same grid spacing. Diagonal stripe rhythm on black bg.
    Candy corns are upright white; pumpkins are white — two distinct silhouettes alternating."""
    fig, ax = setup_ax()

    cols, rows = 5, 7
    dx, dy = PERIOD / cols, PERIOD / rows
    h_cc = dy * 0.82; w_cc = dx * 0.58
    s_pk = min(dx, dy) * 0.66

    for row in range(-1, rows + 1):
        shift = (dx * 0.5) if row % 2 else 0.0
        for col in range(-1, cols + 2):
            cx = (col + 0.5) * dx + shift
            cy = (row + 0.5) * dy
            motif = (col - row) % 2
            for ox, oy in WRAPS:
                px, py = cx + ox, cy + oy
                if -15 <= px <= PERIOD + 15 and -15 <= py <= PERIOD + 15:
                    if motif == 0:
                        draw_candy_corn(ax, px, py, h_cc, w_cc)
                    else:
                        draw_pumpkin(ax, px, py, s_pk)

    save(fig, "abstract halloween variation candy corn pumpkin alternating diagonal row stripe combo pattern black white texture")


if __name__ == "__main__":
    draw()
