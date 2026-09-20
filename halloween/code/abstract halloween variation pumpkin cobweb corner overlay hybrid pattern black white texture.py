import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, FancyBboxPatch, Polygon
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
EPS_DIR = OUTPUT_DIR / \"eps\"
JPG_DIR.mkdir(parents=True, exist_ok=True)
SVG_DIR.mkdir(parents=True, exist_ok=True)
EPS_DIR.mkdir(parents=True, exist_ok=True)


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
    eps_path = EPS_DIR / f\"{name} {DATE}.eps\"
    orig_size = fig.get_size_inches()
    fig.set_size_inches(30, 30)
    fig.savefig(eps_path, format=\"eps\", pad_inches=0, facecolor=\"white\", dpi=DPI)
    fig.set_size_inches(orig_size[0], orig_size[1])
    plt.close(fig)
    print(f"Saved: {jpg_path} | {svg_path} | {eps_path}")


def corner_web(ax, cx, cy, size, corner="tl"):
    """Quarter-circle web in a tile corner. corner = tl/tr/bl/br."""
    r = size
    if corner == "tl":
        ox, oy, angle_range = cx, cy + size, (270, 360)
    elif corner == "tr":
        ox, oy, angle_range = cx + size, cy + size, (180, 270)
    elif corner == "bl":
        ox, oy, angle_range = cx, cy, (0, 90)
    else:  # br
        ox, oy, angle_range = cx + size, cy, (90, 180)

    a_start, a_end = np.radians(angle_range[0]), np.radians(angle_range[1])
    angles = np.linspace(a_start, a_end, 6)

    for a in angles:
        ax.plot([ox, ox + r * np.cos(a)], [oy, oy + r * np.sin(a)],
                color="black", linewidth=0.55, alpha=0.7)
    for sc in (0.25, 0.50, 0.75, 1.00):
        pts = np.array([[ox + r * sc * np.cos(a), oy + r * sc * np.sin(a)]
                        for a in np.linspace(a_start, a_end, 24)])
        ax.plot(pts[:, 0], pts[:, 1], color="black", linewidth=0.45, alpha=0.65)


def pumpkin(ax, cx, cy, s, fill="black", inv="white"):
    for ox in (-s * 0.24, 0, s * 0.24):
        ax.add_patch(Ellipse((cx + ox, cy), s * 0.60, s * 0.76,
                             facecolor=fill, edgecolor="none"))
    for ox in (-s * 0.24, 0, s * 0.24):
        ax.plot([cx + ox, cx + ox], [cy - s * 0.37, cy + s * 0.37],
                color=inv, linewidth=0.7, solid_capstyle="round")
    ax.add_patch(FancyBboxPatch(
        (cx - s*0.06, cy + s*0.37), s*0.12, s*0.18,
        boxstyle=f"round,pad=0,rounding_size={s*0.04:.4f}",
        facecolor=fill, edgecolor="none"))
    # triangle eyes
    for ex in (-s*0.21, s*0.21):
        ax.add_patch(Polygon([[cx+ex, cy+s*0.16],
                               [cx+ex-s*0.10, cy-s*0.02],
                               [cx+ex+s*0.10, cy-s*0.02]],
                              closed=True, facecolor=inv, edgecolor="none"))
    # jagged mouth
    mx = np.linspace(cx-s*0.26, cx+s*0.26, 9)
    mpts = [(mx[0], cy-s*0.10)]
    for i, x in enumerate(mx):
        mpts.append((x, cy-s*0.22 if i%2==0 else cy-s*0.10))
    mpts.append((mx[-1], cy-s*0.10))
    ax.add_patch(Polygon(mpts, closed=True, facecolor=inv, edgecolor="none"))


def draw():
    """Pumpkin grid with cobwebs in tile corners — 4×5, alternating corner positions."""
    fig, ax = setup_ax()
    cols, rows = 4, 5
    dx, dy = PERIOD / cols, PERIOD / rows
    s = min(dx, dy) * 0.74
    corners = ["tl", "tr", "br", "bl"]
    for row in range(rows):
        for col in range(cols):
            cx = (col + 0.5) * dx
            cy = (row + 0.5) * dy
            fill = "black" if (row + col) % 2 == 0 else "white"
            inv = "white" if fill == "black" else "black"
            # tile background
            ax.add_patch(Polygon([
                [col * dx, row * dy], [(col+1)*dx, row*dy],
                [(col+1)*dx, (row+1)*dy], [col*dx, (row+1)*dy]
            ], closed=True, facecolor=inv, edgecolor="none"))
            # web corner
            corner = corners[(row * cols + col) % 4]
            web_size = min(dx, dy) * 0.30
            web_cx = col * dx
            web_cy = row * dy
            for ox, oy in WRAPS:
                corner_web(ax, web_cx + ox, web_cy + oy, web_size, corner)
                pumpkin(ax, cx + ox, cy + oy, s, fill=fill, inv=inv)
    save(fig, "abstract halloween variation pumpkin cobweb corner overlay hybrid pattern black white texture")


if __name__ == "__main__":
    draw()
