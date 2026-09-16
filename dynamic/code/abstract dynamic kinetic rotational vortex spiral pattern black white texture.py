import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import matplotlib.transforms as transforms
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
    ax.set_xlim(-15, 115)
    ax.set_ylim(-15, 115)
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


def abstract_dynamic_kinetic_rotational_vortex_spiral_pattern_black_white_texture():
    """Tweak: Rotational spiral vortex where rects twist dynamically at varying speeds."""
    fig, ax = setup_ax()
    
    n_rects = 36
    for i in range(n_rects):
        w = 90 - i * 2.4
        if w <= 2:
            break
            
        r = 0.2 * w
        lw = 0.6 + 0.3 * (1 - i / n_rects)
        
        # Exponential twist angle speed
        angle = 8.0 * np.sqrt(i)
        
        box = FancyBboxPatch(
            (-w / 2, -w / 2),
            w,
            w,
            boxstyle=f"round,pad=0,rounding_size={r}",
            fill=False,
            edgecolor="black",
            linewidth=lw,
        )
        t = transforms.Affine2D().rotate_deg(angle).translate(50, 50) + ax.transData
        box.set_transform(t)
        ax.add_patch(box)

    save(fig, "abstract dynamic kinetic rotational vortex spiral pattern black white texture")


if __name__ == "__main__":
    abstract_dynamic_kinetic_rotational_vortex_spiral_pattern_black_white_texture()
