import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import (
    Arc, Circle, Ellipse, FancyBboxPatch, Polygon, Rectangle,
)
from matplotlib.transforms import Affine2D
from pathlib import Path
from datetime import datetime

SIZE = 4000
DPI = 300
PERIOD = 100.0
DATE = datetime.now().strftime("%d%m%Y")
WRAPS = [(i * PERIOD, j * PERIOD) for i in (-1, 0, 1) for j in (-1, 0, 1)]

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR.parent / "output"
JPG_DIR = OUTPUT_DIR / "jpg"
SVG_DIR = OUTPUT_DIR / "svg"
EPS_DIR = OUTPUT_DIR / \"eps\"
JPG_DIR.mkdir(parents=True, exist_ok=True)
SVG_DIR.mkdir(parents=True, exist_ok=True)
EPS_DIR.mkdir(parents=True, exist_ok=True)


def setup_ax():
    fig, ax = plt.subplots(figsize=(SIZE / DPI, SIZE / DPI), dpi=DPI)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.set_facecolor("white")
    ax.set_xlim(0, PERIOD)
    ax.set_ylim(0, PERIOD)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_clip_on(True)
    return fig, ax


def save(fig, name):
    jpg_path = JPG_DIR / f"{name} {DATE}.jpg"
    svg_path = SVG_DIR / f"{name} {DATE}.svg"
    fig.savefig(jpg_path, dpi=DPI, pad_inches=0, facecolor="white")
    fig.savefig(svg_path, format="svg", pad_inches=0, facecolor="white")
    eps_path = EPS_DIR / f\"{name} {DATE}.eps\"
    orig_size = fig.get_size_inches()
    fig.set_size_inches(30, 30)
    fig.savefig(eps_path, format=\"eps\", pad_inches=0, facecolor=\"white\", dpi=DPI)
    fig.set_size_inches(orig_size[0], orig_size[1])
    plt.close(fig)
    print(f"Tersimpan: {jpg_path} | {svg_path}")

def gradient_candy_corn(ax, cx, cy, base_size, rotation, thickness_gradient):
    # Apply random rotation
    transform = Affine2D().rotate_deg(rotation).translate(cx, cy) + ax.transData
    
    # Base triangle with gradient thickness
    height = base_size
    base_width = base_size * 0.6 * thickness_gradient
    
    # Define triangle points (pointing up)
    tip = [0, height/2]
    left_base = [-base_width/2, -height/2]
    right_base = [base_width/2, -height/2]
    
    # Create candy corn with gradient sections
    sections = 3
    section_height = height / sections
    
    # Bottom section (widest)
    bottom_points = [
        left_base,
        [-base_width/2 * 0.8, -height/2 + section_height],
        [base_width/2 * 0.8, -height/2 + section_height],
        right_base
    ]
    bottom = Polygon(bottom_points, closed=True, 
                     facecolor="black", edgecolor="none", 
                     transform=transform)
    ax.add_patch(bottom)
    
    # Middle section (medium width)
    middle_width = base_width * 0.7
    middle_points = [
        [-middle_width/2, -height/2 + section_height],
        [-middle_width/2 * 0.6, -height/2 + 2*section_height],
        [middle_width/2 * 0.6, -height/2 + 2*section_height],
        [middle_width/2, -height/2 + section_height]
    ]
    middle = Polygon(middle_points, closed=True,
                     facecolor="black", edgecolor="none",
                     transform=transform)
    ax.add_patch(middle)
    
    # Top section (narrowest)
    top_width = base_width * 0.4
    top_points = [
        [-top_width/2, -height/2 + 2*section_height],
        [0, height/2],  # Tip
        [top_width/2, -height/2 + 2*section_height]
    ]
    top = Polygon(top_points, closed=True,
                  facecolor="black", edgecolor="none",
                  transform=transform)
    ax.add_patch(top)
    
    # Add gradient-like internal divisions with varying thickness
    division_thickness = base_size * 0.02 * thickness_gradient
    
    # Division between bottom and middle
    div1_y = -height/2 + section_height
    div1_width = base_width * 0.75
    div1 = Polygon([
        [-div1_width/2, div1_y - division_thickness/2],
        [-div1_width/2, div1_y + division_thickness/2],
        [div1_width/2, div1_y + division_thickness/2],
        [div1_width/2, div1_y - division_thickness/2]
    ], closed=True, facecolor="white", edgecolor="none", transform=transform)
    ax.add_patch(div1)
    
    # Division between middle and top (thinner)
    div2_y = -height/2 + 2*section_height
    div2_width = base_width * 0.55
    div2_thickness = division_thickness * 0.7
    div2 = Polygon([
        [-div2_width/2, div2_y - div2_thickness/2],
        [-div2_width/2, div2_y + div2_thickness/2],
        [div2_width/2, div2_y + div2_thickness/2],
        [div2_width/2, div2_y - div2_thickness/2]
    ], closed=True, facecolor="white", edgecolor="none", transform=transform)
    ax.add_patch(div2)
    
    # Add texture lines with gradient spacing
    line_count = int(6 * thickness_gradient)
    for i in range(line_count):
        line_y = -height/2 + (i + 0.5) * (height / (line_count + 1))
        
        # Calculate line width based on position (gradient)
        line_pos = (line_y + height/2) / height
        line_width = base_width * (0.3 + 0.5 * line_pos)  # Wider at bottom
        
        line = Polygon([
            [-line_width/2, line_y - division_thickness/4],
            [-line_width/2, line_y + division_thickness/4],
            [line_width/2, line_y + division_thickness/4],
            [line_width/2, line_y - division_thickness/4]
        ], closed=True, facecolor="white", edgecolor="none", transform=transform)
        ax.add_patch(line)


def draw():
    """Seamless candy corn pattern with gradient thickness and randomized orientation."""
    fig, ax = setup_ax()
    cols, rows = 8, 8
    dx, dy = PERIOD / cols, PERIOD / rows
    
    # Create staggered grid
    for row in range(rows):
        row_offset = (row % 2) * dx / 2
        
        for col in range(cols):
            cx = col * dx + row_offset
            cy = row * dy
            
            # Randomize parameters for each candy corn
            base_size = min(dx, dy) * np.random.uniform(0.4, 0.6)
            rotation = np.random.uniform(0, 360)
            thickness_gradient = np.random.uniform(0.7, 1.3)
            
            # Position adjustment for better tiling
            if row % 2 == 0:
                cy += dy / 2
            
            # Create candy corn with wrap-around
            for ox, oy in WRAPS:
                gradient_candy_corn(ax, cx + ox, cy + oy, 
                                   base_size, rotation, thickness_gradient)
    
    save(fig, "abstract halloween variation candy corn gradient thickness randomized orientation pattern black white texture")


if __name__ == "__main__":
    draw()