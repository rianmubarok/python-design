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


def abstract_parallel_lines_fabric_loom_weave_interlace_pattern_black_white_texture():
    """Fabric loom: horizontal weft lines that jump over/under evenly spaced vertical warp bands"""
    fig, ax = setup_ax()

    n_weft = 80          # horizontal threads
    n_warp = 40          # vertical bands
    gap = 100.0 / n_warp
    warp_width = gap * 0.38   # fraction of gap that is "above"
    lw_weft = 0.55
    lw_warp = 0.55

    # Draw warp (vertical) lines
    for k in range(n_warp + 1):
        x = k * gap
        ax.plot([x, x], [-5, 105], color="black", linewidth=lw_warp * 0.6, alpha=0.35)

    # Draw weft (horizontal) threads that go over/under warp bands
    for i in range(n_weft):
        y = -5 + i * (110.0 / (n_weft - 1))
        # Alternating rows shift the over/under phase
        phase = (i % 2)
        x_pts = []
        y_pts = []
        for k in range(n_warp + 2):
            x_start = (k - 1) * gap
            x_end = k * gap
            over = (k + phase) % 2 == 0

            # Segment before the warp band
            x_pts.append(x_start)
            y_pts.append(y)
            x_pts.append(x_start + gap * 0.3)
            y_pts.append(y)

            # Over warp band: stay at y; under: dip slightly (simulated by break)
            if over:
                x_pts.append(x_start + gap * 0.3)
                y_pts.append(y)
                x_pts.append(x_start + gap * 0.7)
                y_pts.append(y)
            else:
                # Break the line (NaN) so the vertical warp appears on top
                x_pts.append(x_start + gap * 0.32)
                y_pts.append(np.nan)
                x_pts.append(x_start + gap * 0.68)
                y_pts.append(np.nan)

            x_pts.append(x_start + gap * 0.7)
            y_pts.append(y)
            x_pts.append(x_end)
            y_pts.append(y)

        ax.plot(x_pts, y_pts, color="black", linewidth=lw_weft, solid_capstyle="round")

    save(fig, "abstract parallel lines fabric loom weave interlace pattern black white texture")


if __name__ == "__main__":
    abstract_parallel_lines_fabric_loom_weave_interlace_pattern_black_white_texture()
