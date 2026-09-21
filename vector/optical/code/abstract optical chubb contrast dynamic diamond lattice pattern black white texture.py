import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
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
    ax.set_xlim(-50, 50)
    ax.set_ylim(-50, 50)
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


def abstract_optical_chubb_contrast_dynamic_diamond_lattice_pattern_black_white_texture():
    """Optical experiment: Chubb contrast illusion using nested diamond lattices over variable density hatching."""
    fig, ax = setup_ax()

    # Background fine diagonal hatching across the canvas
    hatch_y = np.linspace(-60, 60, 120)
    for y in hatch_y:
        ax.plot(
            [-60, 60], [y - 30, y + 30], color="black", linewidth=0.7, alpha=0.35
        )

    # Grid of nested diamond units
    n_rows = 6
    n_cols = 6
    xs = np.linspace(-35, 35, n_cols)
    ys = np.linspace(-35, 35, n_rows)

    d_size = 11.0

    for i, cx in enumerate(xs):
        for j, cy in enumerate(ys):
            # Outer diamond points
            pts = np.array(
                [
                    [cx, cy + d_size],
                    [cx + d_size, cy],
                    [cx, cy - d_size],
                    [cx - d_size, cy],
                ]
            )

            # High contrast solid / hatched fill
            is_black_fill = (i + j) % 2 == 0

            poly = Polygon(
                pts,
                closed=True,
                facecolor="black" if is_black_fill else "white",
                edgecolor="black",
                linewidth=2.0,
            )
            ax.add_patch(poly)

            # Inner concentric diamonds with varying stroke density
            for scale in [0.7, 0.45, 0.2]:
                inner_pts = np.array(
                    [
                        [cx, cy + d_size * scale],
                        [cx + d_size * scale, cy],
                        [cx, cy - d_size * scale],
                        [cx - d_size * scale, cy],
                    ]
                )
                inner_poly = Polygon(
                    inner_pts,
                    closed=True,
                    facecolor="white" if is_black_fill else "black",
                    edgecolor="black",
                    linewidth=1.4,
                )
                ax.add_patch(inner_poly)

    save(
        fig,
        "abstract optical chubb contrast dynamic diamond lattice pattern black white texture",
    )


if __name__ == "__main__":
    abstract_optical_chubb_contrast_dynamic_diamond_lattice_pattern_black_white_texture()
