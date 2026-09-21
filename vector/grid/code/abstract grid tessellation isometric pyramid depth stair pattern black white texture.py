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
    ax.set_xlim(-10, 110)
    ax.set_ylim(-10, 110)
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


def abstract_grid_tessellation_isometric_pyramid_depth_stair_pattern_black_white_texture():
    """Tweak: Isometric pyramid grid with stepped depth levels on faces."""
    fig, ax = setup_ax()
    
    a = 12.0
    h = a * np.sqrt(3) / 2
    
    n_cols = 10
    n_rows = 10
    
    for r in range(n_rows):
        for c in range(n_cols):
            x0 = c * a
            if r % 2 != 0:
                x0 += a / 2
            y0 = r * h
            
            p1 = (x0, y0)
            p2 = (x0 + a, y0)
            p3 = (x0 + a/2, y0 + h)
            apex = (x0 + a/2, y0 + h/3)
            
            # Draw outer pyramid ridges
            ax.plot([p1[0], p2[0], p3[0], p1[0]], [p1[1], p2[1], p3[1], p1[1]], color="black", linewidth=1.2)
            ax.plot([p1[0], apex[0]], [p1[1], apex[1]], color="black", linewidth=1.0)
            ax.plot([p2[0], apex[0]], [p2[1], apex[1]], color="black", linewidth=1.0)
            ax.plot([p3[0], apex[0]], [p3[1], apex[1]], color="black", linewidth=1.0)
            
            # Stepped inner depth triangles
            for scale in [0.75, 0.5, 0.25]:
                sp1 = (apex[0] + scale * (p1[0] - apex[0]), apex[1] + scale * (p1[1] - apex[1]))
                sp2 = (apex[0] + scale * (p2[0] - apex[0]), apex[1] + scale * (p2[1] - apex[1]))
                sp3 = (apex[0] + scale * (p3[0] - apex[0]), apex[1] + scale * (p3[1] - apex[1]))
                ax.plot([sp1[0], sp2[0], sp3[0], sp1[0]], [sp1[1], sp2[1], sp3[1], sp1[1]], color="black", linewidth=0.6)


    all_x = []
    all_y = []
    for line in ax.lines:
        all_x.extend(line.get_xdata())
        all_y.extend(line.get_ydata())
    for patch in ax.patches:
        if hasattr(patch, 'get_patch_transform') and hasattr(patch, 'get_path'):
            trans = patch.get_patch_transform()
            path = patch.get_path()
            vertices = trans.transform_path(path).vertices
            all_x.extend(vertices[:, 0])
            all_y.extend(vertices[:, 1])
        elif hasattr(patch, 'get_path'):
            vertices = patch.get_path().vertices
            all_x.extend(vertices[:, 0])
            all_y.extend(vertices[:, 1])
            
    if all_x and all_y:
        cx = (min(all_x) + max(all_x)) / 2
        cy = (min(all_y) + max(all_y)) / 2
        ax.set_xlim(cx - 55, cx + 55)
        ax.set_ylim(cy - 55, cy + 55)
        
    save(fig, "abstract grid tessellation isometric pyramid depth stair pattern black white texture")


if __name__ == "__main__":
    abstract_grid_tessellation_isometric_pyramid_depth_stair_pattern_black_white_texture()
