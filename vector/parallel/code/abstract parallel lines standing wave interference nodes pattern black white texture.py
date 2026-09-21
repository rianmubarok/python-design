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


def abstract_parallel_lines_standing_wave_interference_nodes_pattern_black_white_texture():
    """Standing wave: two sine waves travelling in opposite directions create nodes and antinodes"""
    fig, ax = setup_ax()

    n_lines = 65
    n_pts = 800
    x = np.linspace(0, 100, n_pts)

    # Standing wave parameters
    k = 2 * np.pi / 22.0   # spatial frequency
    n_time_snapshots = 14    # draw multiple time snapshots faintly stacked

    for i in range(n_lines):
        y0 = i * (100.0 / (n_lines - 1))

        # Envelope: sine pattern across y axis (node positions)
        envelope = np.sin(np.pi * i / (n_lines - 1))

        for t_idx in range(n_time_snapshots):
            phase = t_idx * np.pi / n_time_snapshots
            # Standing wave: A * sin(kx) * cos(wt)
            displacement = 3.5 * envelope * np.sin(k * x) * np.cos(phase)
            y = y0 + displacement

            alpha = 0.18 if t_idx != n_time_snapshots // 2 else 0.75
            lw = 0.3 if t_idx != n_time_snapshots // 2 else 0.6
            ax.plot(x, y, color="black", linewidth=lw, alpha=alpha, solid_capstyle="round")

    save(fig, "abstract parallel lines standing wave interference nodes pattern black white texture")


if __name__ == "__main__":
    abstract_parallel_lines_standing_wave_interference_nodes_pattern_black_white_texture()
