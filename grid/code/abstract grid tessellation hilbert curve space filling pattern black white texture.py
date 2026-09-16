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
    Hilbert Curve Space Filling.
    A continuous fractal curve that perfectly fills a grid.
    """
    fig, ax = setup_ax()

    # Iterative L-System string generation
    def hilbert(order):
        # A maps to -BF+AFA+FB-
        # B maps to +AF-BFB-FA+
        # F is draw forward, + is turn right, - is turn left
        rules = {
            "A": "-BF+AFA+FB-",
            "B": "+AF-BFB-FA+"
        }
        
        state = "A"
        for _ in range(order):
            new_state = ""
            for char in state:
                new_state += rules.get(char, char)
            state = new_state
        return state

    order = 6
    path = hilbert(order)
    
    # Grid size for order n is 2^n x 2^n
    n = 2 ** order
    step = 100.0 / (n - 1)
    
    x, y = 2.5, 2.5  # start position
    dir_angle = 90  # start pointing up
    
    points = [(x, y)]
    
    for char in path:
        if char == "F":
            rad = np.radians(dir_angle)
            x += np.cos(rad) * step
            y += np.sin(rad) * step
            points.append((x, y))
        elif char == "+":
            dir_angle += 90
        elif char == "-":
            dir_angle -= 90

    points = np.array(points)
    
    import matplotlib.collections as collections
    
    # We can draw the hilbert curve with varying thickness or colors
    segments = np.concatenate([points[:-1, np.newaxis, :], points[1:, np.newaxis, :]], axis=1)
    
    # Let's make the line thickness pulse based on position to make it abstract
    lw = 1.0 + 2.0 * np.sin(np.linspace(0, 50 * np.pi, len(segments)))
    lw = np.clip(lw, 0.5, 3.0)
    
    lc = collections.LineCollection(segments, linewidths=lw, colors="black", capstyle="projecting", joinstyle="miter")
    ax.add_collection(lc)


    all_x = []
    all_y = []
    for line in ax.lines:
        all_x.extend(line.get_xdata())
        all_y.extend(line.get_ydata())
    for patch in ax.patches:
        if hasattr(patch, 'get_path'):
            vertices = patch.get_path().vertices
            all_x.extend(vertices[:, 0])
            all_y.extend(vertices[:, 1])
            
    if all_x and all_y:
        cx = (min(all_x) + max(all_x)) / 2
        cy = (min(all_y) + max(all_y)) / 2
        ax.set_xlim(cx - 55, cx + 55)
        ax.set_ylim(cy - 55, cy + 55)
        
    save(fig, "abstract grid tessellation hilbert curve space filling pattern black white texture")


if __name__ == "__main__":
    draw()
