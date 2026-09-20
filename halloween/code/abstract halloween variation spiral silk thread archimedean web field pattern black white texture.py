import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
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


def archimedean_web(ax, cx, cy, max_r, n_coils=5, n_spokes=12, lw_base=0.8):
    """Archimedean spiral web — the capture thread follows a true outward spiral
    rather than concentric rings, more closely resembling real spider silk."""
    # Archimedean: r = a * theta
    total_angle = n_coils * 2 * np.pi
    n_pts = int(total_angle / (2 * np.pi) * 360)   # 360 pts per coil
    theta = np.linspace(0, total_angle, n_pts)
    r = max_r * theta / total_angle
    xs = cx + r * np.cos(theta)
    ys = cy + r * np.sin(theta)
    # draw spiral as single polyline (fast)
    ax.plot(xs, ys, color="white", linewidth=lw_base * 0.7, alpha=0.82,
            solid_capstyle="round")

    # spokes (radial threads)
    for k in range(n_spokes):
        a = k * 2 * np.pi / n_spokes
        ax.plot([cx, cx + max_r * np.cos(a)], [cy, cy + max_r * np.sin(a)],
                color="white", linewidth=0.5, alpha=0.55)

    # dew drop dots along spiral
    drop_every = max(1, n_pts // 60)
    for i in range(0, n_pts, drop_every):
        ax.add_patch(Circle((xs[i], ys[i]), max_r * 0.008,
                            facecolor="white", edgecolor="none", alpha=0.55))

    # centre anchor
    ax.add_patch(Circle((cx, cy), max_r * 0.022, facecolor="white", edgecolor="none"))


def draw():
    """Field of Archimedean spiral webs — 4×4 staggered, varying coil counts."""
    fig, ax = setup_ax()
    cols, rows = 4, 4
    dx, dy = PERIOD / cols, PERIOD / rows
    r = min(dx, dy) * 0.52
    coil_counts = [4, 6, 5, 7]
    for row in range(rows):
        for col in range(cols):
            cx = (col + 0.5) * dx + (dx * 0.5 if row % 2 else 0)
            cy = (row + 0.5) * dy
            nc = coil_counts[(row * cols + col) % len(coil_counts)]
            ns = 10 if nc < 6 else 14
            for ox, oy in WRAPS:
                archimedean_web(ax, cx + ox, cy + oy, r, n_coils=nc, n_spokes=ns)
    save(fig, "abstract halloween variation spiral silk thread archimedean web field pattern black white texture")


if __name__ == "__main__":
    draw()
