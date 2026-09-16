import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime

SIZE = 4000
DPI = 300
SEED = 42
DATE = datetime.now().strftime("%d%m%Y")

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR.parent / "output"
JPG_DIR = OUTPUT_DIR / "jpg"
SVG_DIR = OUTPUT_DIR / "svg"
JPG_DIR.mkdir(parents=True, exist_ok=True)
SVG_DIR.mkdir(parents=True, exist_ok=True)

np.random.seed(SEED)


def setup_ax():
    fig, ax = plt.subplots(figsize=(SIZE / DPI, SIZE / DPI), dpi=DPI)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.set_facecolor("white")
    ax.set_xlim(-5, 105)
    ax.set_ylim(-5, 105)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def save(fig, name):
    jpg_path = JPG_DIR / f"{name} {DATE}.jpg"
    svg_path = SVG_DIR / f"{name} {DATE}.svg"
    fig.savefig(jpg_path, dpi=DPI, pad_inches=0, facecolor="white")
    fig.savefig(svg_path, format="svg", pad_inches=0, facecolor="white")
    plt.close(fig)
    print(f"Tersimpan: {jpg_path} | {svg_path}")


def abstract_parallel_lines_wormhole_tunnel_radial_compression_pattern_black_white_texture():
    """Wormhole tunnel: parallel lines pinch into a central tunnel throat then expand back out"""
    fig, ax = setup_ax()

    n_lines = 72
    n_pts = 900
    cx = 50.0   # horizontal centre of the throat
    throat_r = 4.0   # min radius at the throat
    throat_w = 12.0  # half-width of the compression zone in x

    x_full = np.linspace(-5, 105, n_pts)

    for i in range(n_lines):
        t = i / (n_lines - 1)        # 0..1
        y0 = -5 + t * 110.0
        dist_from_mid = abs(y0 - 50.0)  # 0 at centre, 55 at edge

        y_pts = []
        for xi in x_full:
            dx = xi - cx
            # Compression factor: 1 far from throat, < 1 near throat
            zone = np.exp(-(dx * dx) / (2 * throat_w ** 2))
            # Map lines toward centre as they enter the throat
            compress = 1 - zone * (1 - throat_r / 55.0)
            y = 50.0 + (y0 - 50.0) * compress
            y_pts.append(y)

        # Lineweight: thicker far from centre (more spread), thinner at throat
        lw = 0.25 + 0.65 * (dist_from_mid / 55.0)
        ax.plot(x_full, y_pts, color="black", linewidth=lw, solid_capstyle="round")

    save(fig, "abstract parallel lines wormhole tunnel radial compression pattern black white texture")


if __name__ == "__main__":
    abstract_parallel_lines_wormhole_tunnel_radial_compression_pattern_black_white_texture()
