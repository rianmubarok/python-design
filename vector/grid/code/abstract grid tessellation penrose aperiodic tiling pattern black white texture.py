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
    Penrose Tiling (Rhombus based).
    A recursive substitution to generate a true aperiodic Penrose P3 tiling
    made of thick and thin rhombi.
    """
    fig, ax = setup_ax()

    golden_ratio = (1 + np.sqrt(5)) / 2

    # A recursive deflation algorithm for Penrose tiling
    # We represent a triangle by (color, A, B, C) where color is 0 (thick) or 1 (thin)
    
    def subdivide(triangles):
        result = []
        for color, A, B, C in triangles:
            if color == 0:
                # Subdivide thick triangle
                P = A + (B - A) / golden_ratio
                result.append((0, C, P, B))
                result.append((1, P, C, A))
            else:
                # Subdivide thin triangle
                Q = B + (A - B) / golden_ratio
                R = B + (C - B) / golden_ratio
                result.append((1, R, C, A))
                result.append((1, Q, R, B))
                result.append((0, R, Q, A))
        return result

    # Create initial "sun" layout (10 thick rhombi)
    triangles = []
    scale = 100.0
    cx, cy = 50.0, 50.0
    
    for i in range(10):
        B = np.array([cx + scale * np.cos((2 * i - 1) * np.pi / 10),
                      cy + scale * np.sin((2 * i - 1) * np.pi / 10)])
        C = np.array([cx + scale * np.cos((2 * i + 1) * np.pi / 10),
                      cy + scale * np.sin((2 * i + 1) * np.pi / 10)])
        
        if i % 2 == 0:
            B, C = C, B  # Mirror every second one
            
        triangles.append((0, np.array([cx, cy]), B, C))

    # Deflate (recurse) 5 times
    for _ in range(5):
        triangles = subdivide(triangles)
        
    # Draw edges
    import matplotlib.collections as collections
    
    segments = []
    for color, A, B, C in triangles:
        # Penrose triangles always come in pairs forming rhombi, but just drawing the outline of the triangles 
        # includes the inner diagonal. To draw rhombi perfectly requires pairing them, but drawing all edges 
        # and letting them overlap forms a beautifully dense and intricate grid anyway.
        segments.append([A, B])
        segments.append([B, C])
        segments.append([C, A])
        
    lc = collections.LineCollection(segments, linewidths=0.5, colors="black", capstyle="round")
    ax.add_collection(lc)

    save(fig, "abstract grid tessellation penrose aperiodic tiling pattern black white texture")


if __name__ == "__main__":
    draw()
