import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon
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
    print(f"Saved: {jpg_path}")


def picket_post(ax, cx, base_y, post_w, post_h, fill="white"):
    """Pointed picket fence post."""
    # shaft
    ax.add_patch(FancyBboxPatch(
        (cx - post_w/2, base_y), post_w, post_h * 0.80,
        boxstyle=f"round,pad=0,rounding_size={post_w*0.12:.4f}",
        facecolor=fill, edgecolor="none"))
    # pointed top
    tip_pts = np.array([
        [cx - post_w/2, base_y + post_h*0.78],
        [cx,            base_y + post_h],
        [cx + post_w/2, base_y + post_h*0.78],
    ])
    ax.add_patch(Polygon(tip_pts, closed=True, facecolor=fill, edgecolor="none"))


def mini_web_corner(ax, x_post, y_top, r, side=1):
    """Quarter-circle web in the corner between post and rail."""
    a_start = np.radians(180) if side > 0 else np.radians(270)
    a_end   = np.radians(270) if side > 0 else np.radians(360)
    angles = np.linspace(a_start, a_end, 5)
    for a in angles:
        ax.plot([x_post, x_post + r*np.cos(a)], [y_top, y_top + r*np.sin(a)],
                color="white", linewidth=0.45, alpha=0.7)
    for sc in (0.3, 0.6, 0.9):
        pts = np.array([[x_post+r*sc*np.cos(a), y_top+r*sc*np.sin(a)]
                        for a in np.linspace(a_start, a_end, 24)])
        ax.plot(pts[:,0], pts[:,1], color="white", linewidth=0.35, alpha=0.6)


def draw():
    """Seamless haunted fence — rows of pointed picket posts with horizontal rails
    and cobwebs filling the space between posts. 3 rows of fence tiling vertically."""
    fig, ax = setup_ax()
    n_posts = 10
    post_w = PERIOD / n_posts * 0.55
    post_spacing = PERIOD / n_posts
    post_h = 22.0
    rail_h = 3.5
    n_fence_rows = 5
    row_spacing = PERIOD / n_fence_rows

    for fence_row in range(n_fence_rows):
        base_y = fence_row * row_spacing + row_spacing * 0.18
        # bottom rail
        rail_y = base_y + post_h * 0.25
        # top rail
        rail_y2 = base_y + post_h * 0.68
        for ox, oy in WRAPS:
            # rails
            ax.add_patch(FancyBboxPatch(
                (-2+ox, rail_y+oy), PERIOD+4, rail_h*0.7,
                boxstyle="square,pad=0", facecolor="white", edgecolor="none"))
            ax.add_patch(FancyBboxPatch(
                (-2+ox, rail_y2+oy), PERIOD+4, rail_h*0.6,
                boxstyle="square,pad=0", facecolor="white", edgecolor="none"))
            # posts
            for i in range(n_posts):
                cx = (i + 0.5) * post_spacing
                picket_post(ax, cx+ox, base_y+oy, post_w, post_h)
                # cobwebs between posts
                web_r = post_spacing * 0.38
                mini_web_corner(ax, cx + post_spacing*0.5+ox,
                                rail_y2 + rail_h*0.6+oy, web_r, side=1)
    save(fig, "abstract halloween tessellation haunted fence picket web posts pattern black white texture")


if __name__ == "__main__":
    draw()
