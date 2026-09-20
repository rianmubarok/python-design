import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon
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
    eps_path = EPS_DIR / f\"{name} {DATE}.eps\"
    orig_size = fig.get_size_inches()
    fig.set_size_inches(30, 30)
    fig.savefig(eps_path, format=\"eps\", pad_inches=0, facecolor=\"white\", dpi=DPI)
    fig.set_size_inches(orig_size[0], orig_size[1])
    plt.close(fig)
    print(f"Saved: {jpg_path} | {svg_path} | {eps_path}")


def candy_corn_at(ax, cx, cy, h, angle_deg):
    a = np.radians(angle_deg)
    hw_base = h*0.38; hw_mid = h*0.20
    tip = np.array([0, h*0.50])
    mid_l = np.array([-hw_mid, h*0.10]); mid_r = np.array([hw_mid, h*0.10])
    base_l = np.array([-hw_base, -h*0.50]); base_r = np.array([hw_base, -h*0.50])
    def rot(pt):
        c,s_=np.cos(a),np.sin(a)
        return np.array([c*pt[0]-s_*pt[1]+cx, s_*pt[0]+c*pt[1]+cy])
    full = [rot(tip),rot(mid_l),rot(base_l),rot(base_r),rot(mid_r)]
    ax.add_patch(Polygon(full, closed=True, facecolor="white", edgecolor="none"))
    base_band = [rot(np.array([-hw_mid,-h*0.08])),rot(np.array([hw_mid,-h*0.08])),
                 rot(base_r),rot(base_l)]
    ax.add_patch(Polygon(base_band, closed=True, facecolor="black", edgecolor="none"))
    ax.add_patch(Polygon(full, closed=True, facecolor="none",
                         edgecolor="white", linewidth=0.35))


def web_with_candy(ax, cx, cy, r):
    spokes = 8
    angles = [k*np.pi/4 for k in range(spokes)]
    for a in angles:
        ax.plot([cx, cx+r*np.cos(a)],[cy, cy+r*np.sin(a)],
                color="white", linewidth=0.55)
    ring_scales = [0.30, 0.55, 0.80]
    for sc in ring_scales:
        pts = np.array([[cx+r*sc*np.cos(a), cy+r*sc*np.sin(a)] for a in angles])
        pts = np.vstack([pts, pts[0]])
        ax.plot(pts[:,0], pts[:,1], color="white", linewidth=0.45)
        # place candy corn at each spoke intersection on this ring
        for a in angles:
            ix = cx + r*sc*np.cos(a)
            iy = cy + r*sc*np.sin(a)
            # tip points outward along spoke
            candy_corn_at(ax, ix, iy, r*0.18, np.degrees(a)-90)
    # centre dot
    ax.add_patch(Circle((cx,cy), r*0.04, facecolor="white", edgecolor="none"))


def draw():
    """Spider webs with candy corns at each ring-spoke intersection, 6×6."""
    fig, ax = setup_ax()
    cols, rows = 6, 6
    dx, dy = PERIOD/cols, PERIOD/rows
    r = min(dx, dy) * 0.56
    for row in range(rows):
        for col in range(cols):
            cx = (col+0.5)*dx + (dx*0.5 if row%2 else 0)
            cy = (row+0.5)*dy
            for ox, oy in WRAPS:
                web_with_candy(ax, cx+ox, cy+oy, r)
    save(fig, "abstract halloween variation candy corn web spoke intersection placement pattern black white texture")


if __name__ == "__main__":
    draw()
