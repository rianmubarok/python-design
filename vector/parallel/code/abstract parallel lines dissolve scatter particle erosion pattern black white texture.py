import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime

SIZE = 4000
DPI = 300
DATE = datetime.now().strftime("%d%m%Y")

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR.parent / "output"
JPG_DIR = OUTPUT_DIR / "jpg"
SVG_DIR = OUTPUT_DIR / "svg"
JPG_DIR.mkdir(parents=True, exist_ok=True)
SVG_DIR.mkdir(parents=True, exist_ok=True)


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


def draw():
    """
    Lines dissolve from solid at the top to scattered particles at the bottom.
    Each horizontal line progressively breaks into shorter dashes, then dots,
    with random vertical displacement — simulating erosion / disintegration.
    """
    fig, ax = setup_ax()
    rng = np.random.default_rng(42)

    n_lines = 70

    for i in range(n_lines):
        y0 = 105 - 110 * i / (n_lines - 1)
        # Dissolution factor: 0 at top (solid), 1 at bottom (fully dissolved)
        dissolve = i / (n_lines - 1)

        if dissolve < 0.15:
            # Fully solid line
            ax.plot([-5, 105], [y0, y0], color="black", linewidth=0.6,
                    solid_capstyle="round")
        elif dissolve < 0.6:
            # Breaking into dashes with increasing gaps
            n_segs = int(30 + 80 * dissolve)
            x_starts = np.sort(rng.uniform(-5, 100, n_segs))
            for xs in x_starts:
                seg_len = rng.uniform(0.3, 4.0 * (1 - dissolve))
                dy = rng.normal(0, 0.5 * dissolve)
                ax.plot([xs, xs + seg_len], [y0 + dy, y0 + dy],
                        color="black", linewidth=0.5 * (1 - dissolve * 0.5),
                        solid_capstyle="round")
        else:
            # Particles / dots
            n_particles = int(60 + 120 * (1 - dissolve))
            px = rng.uniform(-5, 105, n_particles)
            py = y0 + rng.normal(0, 1.5 * dissolve, n_particles)
            sizes = rng.uniform(0.05, 0.6 * (1 - dissolve * 0.4), n_particles)
            for k in range(n_particles):
                circle = plt.Circle((px[k], py[k]), sizes[k], color="black",
                                     fill=True)
                ax.add_patch(circle)

    save(fig, "abstract parallel lines dissolve scatter particle erosion pattern black white texture")


if __name__ == "__main__":
    draw()
