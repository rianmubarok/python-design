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
    Folded Origami Paper.
    A square grid divided into diagonal and straight triangles, shaded
    with hatches to simulate the geometric creases of a folded origami sheet.
    """
    fig, ax = setup_ax()
    rng = np.random.default_rng(42)

    import matplotlib.patches as patches

    grid_size = 15
    cell_size = 120.0 / grid_size
    
    for row in range(-1, grid_size + 1):
        for col in range(-1, grid_size + 1):
            cx = -10 + col * cell_size
            cy = -10 + row * cell_size
            
            # Each cell is divided into 4 triangles by an X
            center_x = cx + cell_size / 2
            center_y = cy + cell_size / 2
            
            tl = [cx, cy + cell_size]
            tr = [cx + cell_size, cy + cell_size]
            bl = [cx, cy]
            br = [cx + cell_size, cy]
            c = [center_x, center_y]
            
            triangles = [
                ([tl, tr, c], rng.choice(['', '////', '....', 'solid'])), # Top
                ([tr, br, c], rng.choice(['', '////', '....', 'solid'])), # Right
                ([br, bl, c], rng.choice(['', '////', '....', 'solid'])), # Bottom
                ([bl, tl, c], rng.choice(['', '////', '....', 'solid']))  # Left
            ]
            
            for pts, style in triangles:
                if style == 'solid':
                    poly = patches.Polygon(pts, closed=True, facecolor='black', edgecolor='black', linewidth=1.5)
                elif style == '':
                    poly = patches.Polygon(pts, closed=True, facecolor='white', edgecolor='black', linewidth=1.5)
                elif style == '....':
                    # Emulate dots by hatching
                    poly = patches.Polygon(pts, closed=True, facecolor='none', edgecolor='black', linewidth=1.5, hatch='..')
                else:
                    poly = patches.Polygon(pts, closed=True, facecolor='none', edgecolor='black', linewidth=1.5, hatch=style)
                ax.add_patch(poly)

    save(fig, "abstract grid tessellation folded origami paper crinkled surface pattern black white texture")


if __name__ == "__main__":
    draw()
