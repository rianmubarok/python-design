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

def warped_witch_hat(ax, cx, cy, base_size, warp_factor, height_variation):
    # Calculate dimensions with variations
    brim_width = base_size * (1.0 + warp_factor * 0.4)
    brim_height = base_size * 0.15 * (1.0 + warp_factor * 0.3)
    cone_height = base_size * (0.8 + height_variation * 0.4)
    cone_base = base_size * 0.4 * (1.0 - warp_factor * 0.2)
    
    # Warped brim (asymmetric ellipse)
    brim_rx = brim_width / 2
    brim_ry = brim_height / 2
    
    # Create warped brim using distorted ellipse
    brim_points = []
    resolution = 36
    
    for i in range(resolution + 1):
        angle = 2 * np.pi * i / resolution
        
        # Apply warp to radius based on angle
        angle_warp = 1.0 + warp_factor * np.sin(angle * 3) * 0.3
        
        x = cx + brim_rx * np.cos(angle) * angle_warp
        y = cy + brim_ry * np.sin(angle) * (1.0 + warp_factor * np.cos(angle * 2) * 0.2)
        
        brim_points.append([x, y])
    
    brim = Polygon(brim_points, closed=True, 
                   facecolor="black", edgecolor="none")
    ax.add_patch(brim)
    
    # Warped cone
    cone_points = []
    
    # Left side of cone (warped)
    left_warp = 1.0 + warp_factor * 0.5
    cone_points.append([cx - cone_base/2 * left_warp, cy])
    
    # Tip (varied height)
    tip_y = cy + cone_height * (1.0 + height_variation * 0.2)
    cone_points.append([cx, tip_y])
    
    # Right side of cone (different warp)
    right_warp = 1.0 - warp_factor * 0.3
    cone_points.append([cx + cone_base/2 * right_warp, cy])
    
    cone = Polygon(cone_points, closed=True,
                   facecolor="black", edgecolor="none")
    ax.add_patch(cone)
    
    # Band with warped edges
    band_height = base_size * 0.08 * (1.0 - warp_factor * 0.1)
    band_y = cy + cone_height * 0.3
    
    # Create warped band
    band_points = []
    band_resolution = 24
    
    for i in range(band_resolution + 1):
        angle = 2 * np.pi * i / band_resolution
        
        # Band follows cone shape but warped
        if angle <= np.pi:  # Left half
            band_r = cone_base/2 * left_warp * (1.0 - (angle/np.pi) * 0.3)
        else:  # Right half
            band_r = cone_base/2 * right_warp * (1.0 - ((2*np.pi - angle)/np.pi) * 0.3)
        
        # Additional warp
        band_warp = 1.0 + warp_factor * np.sin(angle * 4) * 0.2
        
        x = cx + band_r * np.cos(angle) * band_warp
        y = band_y + band_height/2 * np.sin(angle * 2)
        
        band_points.append([x, y])
    
    band = Polygon(band_points, closed=True,
                   facecolor="white", edgecolor="none")
    ax.add_patch(band)
    
    # Decorative buckle (warped)
    buckle_size = base_size * 0.1 * (1.0 - warp_factor * 0.2)
    buckle_x = cx
    buckle_y = band_y
    
    # Warped rectangle buckle
    buckle_rx = buckle_size * (1.0 + warp_factor * 0.3)
    buckle_ry = buckle_size * 0.6 * (1.0 - warp_factor * 0.2)
    
    buckle_points = [
        [buckle_x - buckle_rx/2, buckle_y - buckle_ry/2],
        [buckle_x - buckle_rx/2 * 0.8, buckle_y + buckle_ry/2],
        [buckle_x + buckle_rx/2 * 0.8, buckle_y + buckle_ry/2],
        [buckle_x + buckle_rx/2, buckle_y - buckle_ry/2]
    ]
    
    buckle = Polygon(buckle_points, closed=True,
                     facecolor="black", edgecolor="none")
    ax.add_patch(buckle)
    
    # Buckle details (warped cross)
    cross_width = buckle_size * 0.15
    cross_height = buckle_size * 0.4
    
    # Vertical bar (warped)
    vert_points = [
        [buckle_x - cross_width/2, buckle_y - cross_height/2],
        [buckle_x - cross_width/2 * (1.0 + warp_factor * 0.2), buckle_y + cross_height/2],
        [buckle_x + cross_width/2 * (1.0 - warp_factor * 0.1), buckle_y + cross_height/2],
        [buckle_x + cross_width/2, buckle_y - cross_height/2]
    ]
    vert_bar = Polygon(vert_points, closed=True,
                       facecolor="white", edgecolor="none")
    ax.add_patch(vert_bar)
    
    # Horizontal bar (differently warped)
    horiz_width = buckle_size * 0.3
    horiz_height = cross_width
    
    horiz_points = [
        [buckle_x - horiz_width/2, buckle_y - horiz_height/2],
        [buckle_x - horiz_width/2 * 0.9, buckle_y + horiz_height/2],
        [buckle_x + horiz_width/2 * 0.9, buckle_y + horiz_height/2],
        [buckle_x + horiz_width/2, buckle_y - horiz_height/2]
    ]
    horiz_bar = Polygon(horiz_points, closed=True,
                        facecolor="white", edgecolor="none")
    ax.add_patch(horiz_bar)
    
    # Brim texture (warped lines)
    texture_count = int(8 * (1.0 + warp_factor))
    for i in range(texture_count):
        texture_angle = 2 * np.pi * i / texture_count
        
        # Vary texture length based on warp
        texture_length = brim_rx * (0.6 + warp_factor * 0.2 * np.sin(texture_angle * 2))
        
        start_x = cx + texture_length * 0.2 * np.cos(texture_angle)
        start_y = cy + texture_length * 0.2 * np.sin(texture_angle)
        end_x = cx + texture_length * np.cos(texture_angle)
        end_y = cy + texture_length * np.sin(texture_angle)
        
        # Warp texture line
        mid_x = (start_x + end_x) / 2 + warp_factor * 0.05 * base_size * np.sin(texture_angle * 3)
        mid_y = (start_y + end_y) / 2 + warp_factor * 0.05 * base_size * np.cos(texture_angle * 3)
        
        # Draw curved texture line
        t = np.linspace(0, 1, 20)
        curve_x = (1-t)**2 * start_x + 2*(1-t)*t * mid_x + t**2 * end_x
        curve_y = (1-t)**2 * start_y + 2*(1-t)*t * mid_y + t**2 * end_y
        
        ax.plot(curve_x, curve_y, color="white", 
                linewidth=np.random.uniform(0.6, 1.0))


def draw():
    """Seamless witch hat pattern with warped brims and varying heights."""
    fig, ax = setup_ax()
    cols, rows = 6, 6
    dx, dy = PERIOD / cols, PERIOD / rows
    
    seed_offset = 300
    for row in range(rows):
        row_offset = (row % 2) * dx / 3
        
        for col in range(cols):
            # Vary position
            offset_x = np.random.uniform(-0.1, 0.1) * dx
            offset_y = np.random.uniform(-0.1, 0.1) * dy
            
            cx = col * dx + row_offset + offset_x + dx/2
            cy = row * dy + offset_y + dy/2
            
            # Vary parameters
            base_size = min(dx, dy) * np.random.uniform(0.5, 0.7)
            warp_factor = np.random.uniform(-0.5, 0.5)
            height_variation = np.random.uniform(-0.3, 0.3)
            
            for ox, oy in WRAPS:
                warped_witch_hat(ax, cx + ox, cy + oy, 
                                base_size, warp_factor, height_variation)
                seed_offset += 1
    
    save(fig, "abstract halloween variation witch hat warped brims varying heights pattern black white texture")


if __name__ == "__main__":
    draw()