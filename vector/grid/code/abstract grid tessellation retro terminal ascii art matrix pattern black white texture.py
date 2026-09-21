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
    Retro Terminal ASCII Art Matrix.
    A rigid grid where each cell is filled with a monospaced ASCII character
    simulating a retro computer terminal or the Matrix digital rain.
    """
    fig, ax = setup_ax()
    rng = np.random.default_rng(42)

    grid_size = 40
    cell_w = 120.0 / grid_size
    
    chars = ['+', '-', '/', '\\', '|', '*', '#', '=', ':', '.', ' ']
    
    # We will use noise to cluster the characters
    x = np.linspace(0, 10, grid_size)
    y = np.linspace(0, 10, grid_size)
    X, Y = np.meshgrid(x, y)
    
    noise = np.sin(X * 1.5) * np.cos(Y * 2.2) + np.sin(X * 0.5 + 2.0)
    noise = (noise - noise.min()) / (noise.max() - noise.min())
    
    import matplotlib.patches as patches
    
    for row in range(grid_size):
        for col in range(grid_size):
            cx = -10 + col * cell_w
            # Draw from top to bottom
            cy = 110 - row * cell_w
            
            # 20% chance to draw a solid block instead of text (glitch effect)
            if rng.random() > 0.8:
                if rng.random() > 0.5:
                    rect = patches.Rectangle((cx, cy - cell_w), cell_w, cell_w, facecolor='black')
                    ax.add_patch(rect)
                continue
                
            val = noise[row, col] + rng.uniform(-0.1, 0.1)
            
            # Map noise value to character list index
            idx = int(np.clip(val * len(chars), 0, len(chars) - 1))
            char = chars[idx]
            
            # We use matplotlib text. fontfamily='monospace' is critical.
            # fontdict controls the size perfectly.
            ax.text(cx + cell_w/2, cy - cell_w/2, char, 
                    fontsize=8, fontfamily='monospace', fontweight='bold', 
                    ha='center', va='center', color='black')
                    
            # Draw a faint grid line for the terminal aesthetic
            ax.plot([cx, cx + cell_w], [cy - cell_w, cy - cell_w], color="black", linewidth=0.2)
            ax.plot([cx + cell_w, cx + cell_w], [cy, cy - cell_w], color="black", linewidth=0.2)

    save(fig, "abstract grid tessellation retro terminal ascii art matrix pattern black white texture")


if __name__ == "__main__":
    draw()
