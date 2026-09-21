import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
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


def draw_squircle(ax, x, y, width, height, pad=0.8, fill=True, color="black"):
    patch = FancyBboxPatch(
        (x - width / 2, y - height / 2),
        width,
        height,
        boxstyle=f"round,pad=0,rounding_size={pad}",
        facecolor=color if fill else "none",
        edgecolor=color,
        linewidth=1.8 if not fill else 0,
    )
    ax.add_patch(patch)


def abstract_optical_ebbinghaus_size_illusion_squircle_array_pattern_black_white_texture():
    """Optical experiment: Ebbinghaus size-contrast illusion arranged in a patterned squircle matrix."""
    fig, ax = setup_ax()

    # 4x4 grid of target clusters
    grid_size = 4
    centers = np.linspace(-33, 33, grid_size)

    # Identical center squircle diameter for ALL clusters
    center_size = 6.0

    for i, cx in enumerate(centers):
        for j, cy in enumerate(centers):
            # Draw identical central squircle
            draw_squircle(
                ax, cx, cy, center_size, center_size, pad=1.5, fill=True
            )

            # Alternate surrounding ring context: small vs large outer elements
            is_large_surround = (i + j) % 2 == 0

            if is_large_surround:
                # Large outer elements (makes center look smaller)
                n_outer = 6
                ring_r = 13.5
                outer_size = 7.5
            else:
                # Small outer elements (makes center look larger)
                n_outer = 8
                ring_r = 8.5
                outer_size = 2.2

            angles = np.linspace(0, 2 * np.pi, n_outer, endpoint=False)
            for a in angles:
                ox = cx + ring_r * np.cos(a)
                oy = cy + ring_r * np.sin(a)
                draw_squircle(
                    ax,
                    ox,
                    oy,
                    outer_size,
                    outer_size,
                    pad=outer_size * 0.25,
                    fill=False,
                )

    save(
        fig,
        "abstract optical ebbinghaus size illusion squircle array pattern black white texture",
    )


if __name__ == "__main__":
    abstract_optical_ebbinghaus_size_illusion_squircle_array_pattern_black_white_texture()
