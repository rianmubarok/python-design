import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime
from matplotlib.collections import LineCollection

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
    Woven Ribbon Overlapping Sine Waves.
    Lines are drawn as interlocking sine waves that shift in phase,
    creating a braided or woven ribbon illusion. The line thickness
    varies as if the ribbons are twisting in 3D space.
    """
    fig, ax = setup_ax()

    n_ribbons = 25
    lines_per_ribbon = 5
    n_pts = 800

    for i in range(n_ribbons):
        base_y = 5 + 90 * i / (n_ribbons - 1)
        
        # Each ribbon oscillates
        freq = 0.08
        phase_offset = i * 0.4
        
        x = np.linspace(-5, 105, n_pts)
        
        # The main path of the ribbon
        wave = np.sin(x * freq + phase_offset) * 4.0
        
        # Draw the parallel strands within the ribbon
        for j in range(lines_per_ribbon):
            # Offset inside the ribbon
            local_offset = (j - (lines_per_ribbon - 1) / 2) * 0.4
            
            y_path = base_y + wave + local_offset
            
            # Simulate a 3D twist by varying thickness
            # When cosine is near 1, the ribbon is flat to the camera (wide lines)
            # When cosine is near 0, the ribbon is edge-on (thin lines)
            twist = np.cos(x * freq + phase_offset)
            
            lw = 0.15 + 0.6 * np.abs(twist)
            
            points = np.array([x, y_path]).T.reshape(-1, 1, 2)
            segments = np.concatenate([points[:-1], points[1:]], axis=1)
            lc = LineCollection(segments, linewidths=lw[:-1], colors="black", capstyle="round")
            ax.add_collection(lc)

    save(fig, "abstract parallel lines woven ribbon overlapping sine wave pattern black white texture")


if __name__ == "__main__":
    draw()
