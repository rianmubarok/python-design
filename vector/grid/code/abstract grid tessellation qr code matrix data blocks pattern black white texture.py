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
    QR Code Matrix Data Blocks.
    A highly dense, abstract matrix of varying square blocks,
    mimicking a digital QR code, barcode hash, or game of life grid.
    """
    fig, ax = setup_ax()
    rng = np.random.default_rng(42)

    import matplotlib.patches as patches

    # Create a 40x40 matrix
    grid_size = 45
    cell_w = 120.0 / grid_size
    
    # We simulate a "Game of Life" or Perlin threshold to cluster the blocks naturally
    
    x = np.linspace(0, 10, grid_size)
    y = np.linspace(0, 10, grid_size)
    X, Y = np.meshgrid(x, y)
    
    # Simple sine wave interference to act as fake noise
    noise = np.sin(X * 2.5) * np.cos(Y * 1.5) + np.sin(X * 0.8 + 2.0) * np.cos(Y * 3.3)
    
    # Normalize noise 0 to 1
    noise = (noise - noise.min()) / (noise.max() - noise.min())
    
    # Add high frequency random jitter
    noise += rng.uniform(-0.3, 0.3, (grid_size, grid_size))
    
    for row in range(grid_size):
        for col in range(grid_size):
            cx = -10 + col * cell_w
            cy = -10 + row * cell_w
            
            val = noise[row, col]
            
            # Thresholding creates the binary blocks
            if val > 0.55:
                # Solid black block
                rect = patches.Rectangle((cx, cy), cell_w * 0.95, cell_w * 0.95, 
                                         linewidth=0, facecolor='black')
                ax.add_patch(rect)
            elif val > 0.45:
                # Outlined block
                rect = patches.Rectangle((cx + cell_w*0.1, cy + cell_w*0.1), cell_w * 0.75, cell_w * 0.75, 
                                         linewidth=1.0, edgecolor='black', facecolor='none')
                ax.add_patch(rect)
                
            # Draw standard QR code positioning squares in the corners
            if (row < 8 and col < 8) or (row > grid_size-9 and col < 8) or (row < 8 and col > grid_size-9):
                # We overwrite the corner with a massive QR block
                pass 
                
    # Function to draw a massive QR anchor
    def draw_anchor(anchor_c, anchor_r):
        sx = -10 + anchor_c * cell_w
        sy = -10 + anchor_r * cell_w
        aw = cell_w * 7
        
        # Outer thick box
        ax.add_patch(patches.Rectangle((sx, sy), aw, aw, linewidth=4.0, edgecolor='black', facecolor='white', zorder=2))
        # Inner solid box
        ax.add_patch(patches.Rectangle((sx + cell_w*2, sy + cell_w*2), aw - cell_w*4, aw - cell_w*4, linewidth=0, facecolor='black', zorder=2))

    draw_anchor(2, 2)
    draw_anchor(2, grid_size - 9)
    draw_anchor(grid_size - 9, 2)

    save(fig, "abstract grid tessellation qr code matrix data blocks pattern black white texture")


if __name__ == "__main__":
    draw()
