import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc
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
    ax.set_xlim(-2, 18)
    ax.set_ylim(-2, 18)
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


def abstract_grid_tessellation_truchet_arc_radius_wave_oscillation_pattern_black_white_texture():
    """Tweak: Truchet arc grid where arc radii oscillate continuously using 2D sine waves."""
    fig, ax = setup_ax()
    
    n_grid = 15
    for row in range(n_grid):
        for col in range(n_grid):
            x0, y0 = col, row
            rot = np.random.choice([0, 1])
            
            # Radii oscillate with position
            r1 = 0.1 + 0.15 * (0.5 * (1 + np.sin(col * 0.5)))
            r2 = 0.3 + 0.15 * (0.5 * (1 + np.cos(row * 0.5)))
            
            for r in [r1, r2]:
                if rot == 0:
                    arc1 = Arc((x0, y0+1), 2*r, 2*r, angle=0, theta1=270, theta2=360, color="black", linewidth=1.0)
                    arc2 = Arc((x0+1, y0), 2*r, 2*r, angle=0, theta1=90, theta2=180, color="black", linewidth=1.0)
                else:
                    arc1 = Arc((x0, y0), 2*r, 2*r, angle=0, theta1=0, theta2=90, color="black", linewidth=1.0)
                    arc2 = Arc((x0+1, y0+1), 2*r, 2*r, angle=0, theta1=180, theta2=270, color="black", linewidth=1.0)
                ax.add_patch(arc1)
                ax.add_patch(arc2)

    save(fig, "abstract grid tessellation truchet arc radius wave oscillation pattern black white texture")


if __name__ == "__main__":
    abstract_grid_tessellation_truchet_arc_radius_wave_oscillation_pattern_black_white_texture()
