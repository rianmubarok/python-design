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
JPG_DIR.mkdir(parents=True, exist_ok=True)
SVG_DIR.mkdir(parents=True, exist_ok=True)


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
    plt.close(fig)
    print(f"Tersimpan: {jpg_path} | {svg_path}")

def randomized_broomstick(ax, cx, cy, base_size, curvature, seed):
    np.random.seed(seed)
    
    # Broom dimensions
    handle_length = base_size * 1.2
    bristle_width = base_size * 0.8
    bristle_length = base_size * 0.5
    
    # Curved handle using Bézier curve
    handle_start = [cx, cy]
    handle_end = [cx, cy + handle_length]
    
    # Control points for curvature
    if curvature > 0:
        # Curve to the right
        cp1 = [cx + curvature * 0.3 * handle_length, cy + handle_length * 0.3]
        cp2 = [cx + curvature * 0.4 * handle_length, cy + handle_length * 0.7]
    else:
        # Curve to the left
        cp1 = [cx + curvature * 0.3 * handle_length, cy + handle_length * 0.3]
        cp2 = [cx + curvature * 0.4 * handle_length, cy + handle_length * 0.7]
    
    # Draw curved handle
    t = np.linspace(0, 1, 50)
    handle_x = (1-t)**3 * handle_start[0] + 3*(1-t)**2*t * cp1[0] + 3*(1-t)*t**2 * cp2[0] + t**3 * handle_end[0]
    handle_y = (1-t)**3 * handle_start[1] + 3*(1-t)**2*t * cp1[1] + 3*(1-t)*t**2 * cp2[1] + t**3 * handle_end[1]
    
    # Handle width variation along curve
    handle_width_start = base_size * 0.08
    handle_width_end = base_size * 0.05
    
    # Create handle as thickened curve
    for i in range(len(t)-1):
        segment_width = handle_width_start + (handle_width_end - handle_width_start) * t[i]
        
        # Calculate perpendicular direction
        dx = handle_x[i+1] - handle_x[i]
        dy = handle_y[i+1] - handle_y[i]
        length = np.sqrt(dx*dx + dy*dy)
        
        if length > 0:
            perp_x = -dy / length * segment_width/2
            perp_y = dx / length * segment_width/2
            
            # Create segment polygon
            segment_points = [
                [handle_x[i] + perp_x, handle_y[i] + perp_y],
                [handle_x[i] - perp_x, handle_y[i] - perp_y],
                [handle_x[i+1] - perp_x, handle_y[i+1] - perp_y],
                [handle_x[i+1] + perp_x, handle_y[i+1] + perp_y]
            ]
            
            segment = Polygon(segment_points, closed=True,
                            facecolor="black", edgecolor="none")
            ax.add_patch(segment)
    
    # Bristle base (where bristles attach to handle)
    bristle_base_x = handle_end[0]
    bristle_base_y = handle_end[1]
    
    # Randomized bristles
    bristle_count = np.random.randint(20, 35)
    bristle_angles = np.linspace(-np.pi/2, np.pi/2, bristle_count)
    
    # Add random variation to angles
    bristle_angles += np.random.uniform(-0.2, 0.2, bristle_count)
    
    for i, angle in enumerate(bristle_angles):
        # Bristle parameters with randomization
        bristle_len_variation = np.random.uniform(0.7, 1.3)
        bristle_width_variation = np.random.uniform(0.8, 1.2)
        
        actual_length = bristle_length * bristle_len_variation
        actual_width = base_size * 0.02 * bristle_width_variation
        
        # Bristle shape (tapered)
        start_x = bristle_base_x
        start_y = bristle_base_y
        
        end_x = bristle_base_x + actual_length * np.cos(angle)
        end_y = bristle_base_y + actual_length * np.sin(angle)
        
        # Create tapered bristle
        mid_t = np.random.uniform(0.3, 0.7)
        mid_x = start_x + mid_t * (end_x - start_x)
        mid_y = start_y + mid_t * (end_y - start_y)
        
        # Control points for curved bristle
        bristle_curve = np.random.uniform(-0.3, 0.3)
        cp1_x = start_x + (mid_x - start_x) * 0.3 + bristle_curve * actual_length * 0.2
        cp1_y = start_y + (mid_y - start_y) * 0.3
        cp2_x = mid_x + (end_x - mid_x) * 0.3 - bristle_curve * actual_length * 0.2
        cp2_y = mid_y + (end_y - mid_y) * 0.3
        
        # Draw curved bristle with varying width
        t_bristle = np.linspace(0, 1, 20)
        
        # Bézier curve for bristle center
        center_x = (1-t_bristle)**3 * start_x + 3*(1-t_bristle)**2*t_bristle * cp1_x + 3*(1-t_bristle)*t_bristle**2 * cp2_x + t_bristle**3 * end_x
        center_y = (1-t_bristle)**3 * start_y + 3*(1-t_bristle)**2*t_bristle * cp1_y + 3*(1-t_bristle)*t_bristle**2 * cp2_y + t_bristle**3 * end_y
        
        # Calculate tangents for width
        dx_dt = -3*(1-t_bristle)**2 * start_x + 3*(1-4*t_bristle+3*t_bristle**2) * cp1_x + 3*(2*t_bristle-3*t_bristle**2) * cp2_x + 3*t_bristle**2 * end_x
        dy_dt = -3*(1-t_bristle)**2 * start_y + 3*(1-4*t_bristle+3*t_bristle**2) * cp1_y + 3*(2*t_bristle-3*t_bristle**2) * cp2_y + 3*t_bristle**2 * end_y
        
        # Tapered width
        widths = actual_width * (1 - t_bristle * 0.7)
        
        # Create bristle as series of segments
        for j in range(len(t_bristle)-1):
            seg_length = np.sqrt((center_x[j+1]-center_x[j])**2 + (center_y[j+1]-center_y[j])**2)
            
            if seg_length > 0:
                # Perpendicular direction
                perp_x = -dy_dt[j] / np.sqrt(dx_dt[j]**2 + dy_dt[j]**2) * widths[j]/2
                perp_y = dx_dt[j] / np.sqrt(dx_dt[j]**2 + dy_dt[j]**2) * widths[j]/2
                
                seg_points = [
                    [center_x[j] + perp_x, center_y[j] + perp_y],
                    [center_x[j] - perp_x, center_y[j] - perp_y],
                    [center_x[j+1] - perp_x, center_y[j+1] - perp_y],
                    [center_x[j+1] + perp_x, center_y[j+1] + perp_y]
                ]
                
                seg_poly = Polygon(seg_points, closed=True,
                                 facecolor="black", edgecolor="none")
                ax.add_patch(seg_poly)
    
    # Bristle binding/band
    band_width = base_size * 0.1
    band_height = base_size * 0.05
    
    band_points = [
        [bristle_base_x - band_width/2, bristle_base_y - band_height/2],
        [bristle_base_x - band_width/2 * 0.9, bristle_base_y + band_height/2],
        [bristle_base_x + band_width/2 * 0.9, bristle_base_y + band_height/2],
        [bristle_base_x + band_width/2, bristle_base_y - band_height/2]
    ]
    
    band = Polygon(band_points, closed=True,
                  facecolor="black", edgecolor="none")
    ax.add_patch(band)
    
    # Band details
    detail_count = np.random.randint(3, 6)
    for i in range(detail_count):
        detail_x = bristle_base_x + np.random.uniform(-band_width/3, band_width/3)
        detail_y = bristle_base_y + np.random.uniform(-band_height/3, band_height/3)
        
        detail_size = band_height * 0.3
        
        if np.random.random() > 0.5:
            # Circular detail
            detail = Circle((detail_x, detail_y), detail_size,
                           facecolor="white", edgecolor="none")
        else:
            # Rectangular detail
            detail = Rectangle((detail_x - detail_size/2, detail_y - detail_size/4),
                              detail_size, detail_size/2,
                              facecolor="white", edgecolor="none")
        
        ax.add_patch(detail)
    
    # Loose bristles/stragglers
    straggler_count = np.random.randint(5, 10)
    
    for _ in range(straggler_count):
        # Random position near bristles
        straggler_angle = np.random.uniform(-np.pi/2, np.pi/2) * 1.5
        straggler_length = bristle_length * np.random.uniform(0.3, 0.8)
        
        start_x = bristle_base_x + np.random.uniform(-band_width/4, band_width/4)
        start_y = bristle_base_y + np.random.uniform(-band_height/2, band_height/2)
        
        end_x = start_x + straggler_length * np.cos(straggler_angle)
        end_y = start_y + straggler_length * np.sin(straggler_angle)
        
        # Draw straggler
        ax.plot([start_x, end_x], [start_y, end_y],
               color="black", linewidth=np.random.uniform(0.5, 1.0))


def draw():
    """Seamless broomstick pattern with randomized bristles and curved handles."""
    fig, ax = setup_ax()
    cols, rows = 5, 5
    dx, dy = PERIOD / cols, PERIOD / rows
    
    seed_offset = 600
    for row in range(rows):
        row_offset = (row % 2) * dx / 3
        
        for col in range(cols):
            # Vary position
            offset_x = np.random.uniform(-0.2, 0.2) * dx
            offset_y = np.random.uniform(-0.2, 0.2) * dy
            
            cx = col * dx + row_offset + offset_x + dx/2
            cy = row * dy + offset_y + dy/3  # Start lower for handle
            
            # Vary parameters
            base_size = min(dx, dy) * np.random.uniform(0.4, 0.6)
            curvature = np.random.uniform(-0.5, 0.5)
            
            for ox, oy in WRAPS:
                randomized_broomstick(ax, cx + ox, cy + oy,
                                     base_size, curvature, seed_offset)
                seed_offset += 1
    
    save(fig, "abstract halloween variation broomstick randomized bristles curved handle pattern black white texture")


if __name__ == "__main__":
    draw()