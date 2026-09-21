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


def abstract_grid_tessellation_isometric_cube_face_hatch_rotation_pattern_black_white_texture():
    """Tweak: Isometric cubes with rotating line hatchings across the 3 faces."""
    fig, ax = setup_ax()
    
    a = 10.0
    dx = a * np.sqrt(3)
    dy = a * 1.5
    
    n_rows = 10
    n_cols = 10
    
    for row in range(n_rows):
        for col in range(n_cols):
            cx = col * dx
            if row % 2 != 0:
                cx += dx / 2
            cy = row * dy
            
            v_top = (cx, cy + a)
            v_center = (cx, cy)
            v_left = (cx - a * np.sqrt(3)/2, cy + a/2)
            v_right = (cx + a * np.sqrt(3)/2, cy + a/2)
            v_bot_left = (cx - a * np.sqrt(3)/2, cy - a/2)
            v_bot_right = (cx + a * np.sqrt(3)/2, cy - a/2)
            v_bottom = (cx, cy - a)
            
            # Cube edges
            ax.plot([v_center[0], v_top[0]], [v_center[1], v_top[1]], color="black", linewidth=1.0)
            ax.plot([v_center[0], v_bot_left[0]], [v_center[1], v_bot_left[1]], color="black", linewidth=1.0)
            ax.plot([v_center[0], v_bot_right[0]], [v_center[1], v_bot_right[1]], color="black", linewidth=1.0)
            
            ax.plot([v_top[0], v_right[0], v_bot_right[0], v_bottom[0], v_bot_left[0], v_left[0], v_top[0]],
                    [v_top[1], v_right[1], v_bot_right[1], v_bottom[1], v_bot_left[1], v_left[1], v_top[1]],
                    color="black", linewidth=1.0)
                    
            # Hatching on top face
            for t in np.linspace(0.25, 0.75, 3):
                h1 = (v_left[0] + t * (v_top[0] - v_left[0]), v_left[1] + t * (v_top[1] - v_left[1]))
                h2 = (v_center[0] + t * (v_right[0] - v_center[0]), v_center[1] + t * (v_right[1] - v_center[1]))
                ax.plot([h1[0], h2[0]], [h1[1], h2[1]], color="black", linewidth=0.5)


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
        
    save(fig, "abstract grid tessellation isometric cube face hatch rotation pattern black white texture")


if __name__ == "__main__":
    abstract_grid_tessellation_isometric_cube_face_hatch_rotation_pattern_black_white_texture()
