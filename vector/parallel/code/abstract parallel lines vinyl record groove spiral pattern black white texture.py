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


def abstract_parallel_lines_vinyl_record_groove_spiral_pattern_black_white_texture():
    """Wild: a vinyl record — tight Archimedes spiral grooves that cover the whole disc area"""
    fig, ax = setup_ax()
    cx, cy = 50.0, 50.0

    # Spiral parameters
    r_label = 14.0     # centre label radius (no grooves)
    r_edge = 48.0      # outer groove edge
    groove_pitch = 0.95  # radial distance between grooves (tighter = more grooves)

    n_turns = (r_edge - r_label) / groove_pitch
    total_angle = n_turns * 2 * np.pi

    # Sample the spiral arc finely
    pts_per_turn = 500
    total_pts = int(n_turns * pts_per_turn)
    t = np.linspace(0, total_angle, total_pts)
    r = r_label + (r_edge - r_label) * t / total_angle

    x = cx + r * np.cos(t)
    y = cy + r * np.sin(t)

    # Draw as a single continuous line
    ax.plot(x, y, color="black", linewidth=0.4, solid_capstyle="round")

    # Centre label circle (filled white disc)
    label_circle = plt.Circle((cx, cy), r_label, color="white", zorder=2)
    ax.add_patch(label_circle)
    label_outline = plt.Circle((cx, cy), r_label, color="black", fill=False, linewidth=1.0, zorder=3)
    ax.add_patch(label_outline)

    # Spindle hole
    spindle = plt.Circle((cx, cy), 1.2, color="white", zorder=4)
    ax.add_patch(spindle)
    spindle_ring = plt.Circle((cx, cy), 1.2, color="black", fill=False, linewidth=0.8, zorder=5)
    ax.add_patch(spindle_ring)

    # Outer edge circle
    outer = plt.Circle((cx, cy), r_edge + 1.5, color="black", fill=False, linewidth=1.2)
    ax.add_patch(outer)

    save(fig, "abstract parallel lines vinyl record groove spiral pattern black white texture")


if __name__ == "__main__":
    abstract_parallel_lines_vinyl_record_groove_spiral_pattern_black_white_texture()
