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
    Pixel Sorting Digital Glitch Art.
    A high-resolution grid representing image pixels, where bands of pixels
    are algorithmically 'sorted' (stretched down) to create a famous glitch art effect.
    """
    fig, ax = setup_ax()
    rng = np.random.default_rng(42)

    import matplotlib.collections as collections

    n_cols = 120
    cell_w = 120.0 / n_cols
    
    # We will draw vertical strips (columns)
    # Each column has a "sorting threshold".
    
    segments = []
    linewidths = []
    
    for col in range(n_cols):
        cx = -10 + col * cell_w
        
        # A column consists of multiple vertical line segments
        y = 110.0
        while y > -10.0:
            # Decide if this chunk is "glitched" (long stretched line) or "noisy" (short dots)
            if rng.random() > 0.7:
                # Glitch stretch
                length = rng.uniform(5.0, 45.0)
                length = min(length, y + 10.0) # clamp to bottom
                
                segments.append([(cx, y), (cx, y - length)])
                # Stretched pixels look thicker/bolder sometimes
                linewidths.append(cell_w * rng.uniform(0.6, 1.0))
                
                y -= (length + rng.uniform(0.1, 1.0))
            else:
                # Noisy pixels
                length = rng.uniform(0.5, 2.0)
                segments.append([(cx, y), (cx, y - length)])
                linewidths.append(cell_w * 0.4)
                
                y -= (length + rng.uniform(0.5, 3.0))

    lc = collections.LineCollection(segments, linewidths=linewidths, colors="black", capstyle="butt")
    ax.add_collection(lc)

    save(fig, "abstract grid tessellation pixel sorting digital glitch art pattern black white texture")


if __name__ == "__main__":
    draw()
