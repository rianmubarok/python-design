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

def broken_cobweb(ax, cx, cy, grid_size, seed, broken_factor=0.3):
    np.random.seed(seed)
    
    # Offset grid parameters
    grid_offset_x = np.random.uniform(-0.2, 0.2) * grid_size
    grid_offset_y = np.random.uniform(-0.2, 0.2) * grid_size
    
    # Web radius
    web_radius = grid_size * 0.4
    
    # Broken center
    if np.random.random() > broken_factor:
        center_r = web_radius * 0.15
        ax.add_patch(Circle((cx, cy), center_r, 
                           facecolor="black", edgecolor="none"))
    else:
        # Broken center - multiple small circles
        fragments = np.random.randint(2, 5)
        for _ in range(fragments):
            frag_r = web_radius * 0.05 * np.random.uniform(0.5, 1.5)
            frag_x = cx + np.random.uniform(-0.1, 0.1) * web_radius
            frag_y = cy + np.random.uniform(-0.1, 0.1) * web_radius
            ax.add_patch(Circle((frag_x, frag_y), frag_r,
                              facecolor="black", edgecolor="none"))
    
    # Radial spokes with breaks
    spoke_count = np.random.randint(6, 10)
    angles = np.linspace(0, 2*np.pi, spoke_count, endpoint=False)
    
    for i, angle in enumerate(angles):
        # Random chance to skip this spoke
        if np.random.random() < broken_factor * 0.5:
            continue
            
        # Vary spoke length
        spoke_length = web_radius * np.random.uniform(0.7, 1.0)
        
        # Create broken spoke segments
        segments = np.random.randint(2, 5)
        segment_length = spoke_length / segments
        
        for seg in range(segments):
            # Random chance to break this segment
            if np.random.random() < broken_factor:
                continue
                
            start_r = seg * segment_length
            end_r = (seg + 1) * segment_length
            
            # Add slight wobble to segments
            wobble_start = np.random.uniform(-0.05, 0.05) * segment_length
            wobble_end = np.random.uniform(-0.05, 0.05) * segment_length
            
            start_x = cx + (start_r + wobble_start) * np.cos(angle)
            start_y = cy + (start_r + wobble_start) * np.sin(angle)
            end_x = cx + (end_r + wobble_end) * np.cos(angle)
            end_y = cy + (end_r + wobble_end) * np.sin(angle)
            
            ax.plot([start_x, end_x], [start_y, end_y],
                   color="black", linewidth=np.random.uniform(0.4, 0.9))
    
    # Concentric rings with breaks and offset
    ring_count = np.random.randint(3, 6)
    ring_scales = np.sort(np.random.uniform(0.2, 0.9, ring_count))
    
    for ring_idx, scale in enumerate(ring_scales):
        ring_r = web_radius * scale
        
        # Apply grid offset to ring
        offset_ring_r = ring_r * (1 + np.random.uniform(-0.1, 0.1))
        
        # Determine ring completeness
        completeness = 1.0 - broken_factor * np.random.uniform(0.5, 1.0)
        segments_needed = int(spoke_count * completeness)
        
        if segments_needed < 3:  # Skip if too broken
            continue
            
        # Select which segments to draw
        segment_indices = np.random.choice(spoke_count, segments_needed, replace=False)
        segment_indices.sort()
        
        for seg_idx in segment_indices:
            angle1 = angles[seg_idx]
            angle2 = angles[(seg_idx + 1) % spoke_count]
            
            # Create arc segment
            arc_points = []
            seg_resolution = 10
            for j in range(seg_resolution + 1):
                t = j / seg_resolution
                current_angle = angle1 + t * (angle2 - angle1)
                
                # Add wobble to ring
                wobble = np.random.uniform(-0.05, 0.05) * offset_ring_r
                current_r = offset_ring_r + wobble
                
                arc_points.append([
                    cx + current_r * np.cos(current_angle),
                    cy + current_r * np.sin(current_angle)
                ])
            
            # Draw arc segment
            arc_arr = np.array(arc_points)
            ax.plot(arc_arr[:, 0], arc_arr[:, 1],
                   color="black", linewidth=np.random.uniform(0.3, 0.7))
    
    # Add random debris/spots
    debris_count = np.random.randint(3, 8)
    for _ in range(debris_count):
        if np.random.random() < broken_factor:
            debris_r = web_radius * np.random.uniform(0.02, 0.08)
            debris_x = cx + np.random.uniform(-0.8, 0.8) * web_radius
            debris_y = cy + np.random.uniform(-0.8, 0.8) * web_radius
            
            # Random debris shape
            if np.random.random() > 0.5:
                ax.add_patch(Circle((debris_x, debris_y), debris_r,
                                  facecolor="black", edgecolor="none"))
            else:
                rx = debris_r * np.random.uniform(0.7, 1.3)
                ry = debris_r * np.random.uniform(0.7, 1.3)
                angle = np.random.uniform(0, 180)
                ax.add_patch(Ellipse((debris_x, debris_y), rx, ry, angle=angle,
                                    facecolor="black", edgecolor="none"))


def draw():
    """Seamless cobweb pattern with broken segments and offset grid."""
    fig, ax = setup_ax()
    cols, rows = 7, 7
    dx, dy = PERIOD / cols, PERIOD / rows
    
    seed_offset = 200
    for row in range(rows):
        for col in range(cols):
            # Create offset grid
            col_offset = np.random.uniform(-0.15, 0.15) * dx
            row_offset = np.random.uniform(-0.15, 0.15) * dy
            
            cx = (col + 0.5) * dx + col_offset
            cy = (row + 0.5) * dy + row_offset
            
            # Vary broken factor
            broken_factor = np.random.uniform(0.1, 0.4)
            
            for ox, oy in WRAPS:
                broken_cobweb(ax, cx + ox, cy + oy, min(dx, dy) * 0.8, 
                             seed_offset, broken_factor)
                seed_offset += 1
    
    save(fig, "abstract halloween variation cobweb broken segments offset grid pattern black white texture")


if __name__ == "__main__":
    draw()