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

def distorted_crescent_moon(ax, cx, cy, base_size, distortion_factor, phase):
    # Calculate moon dimensions
    outer_r = base_size * 0.4
    inner_r = outer_r * (0.6 + phase * 0.2)  # Phase affects crescent thickness
    
    # Apply distortion to radii
    outer_r *= (1.0 + distortion_factor * 0.3)
    inner_r *= (1.0 + distortion_factor * 0.2)
    
    # Create distorted crescent using two circles with offset centers
    offset = inner_r * (0.8 + distortion_factor * 0.4)
    
    # Outer circle (full moon outline)
    outer_circle = Circle((cx, cy), outer_r,
                         facecolor="black", edgecolor="none")
    
    # Inner circle (cutout for crescent) - distorted position
    inner_cx = cx + offset * (1.0 + distortion_factor * 0.2)
    inner_cy = cy + offset * distortion_factor * 0.1
    
    # Apply additional distortion to inner circle
    inner_rx = inner_r * (1.0 + distortion_factor * 0.1)
    inner_ry = inner_r * (1.0 - distortion_factor * 0.05)
    inner_rotation = distortion_factor * 15
    
    inner_circle = Ellipse((inner_cx, inner_cy), inner_rx*2, inner_ry*2,
                          angle=inner_rotation,
                          facecolor="white", edgecolor="none")
    
    # Combine to create crescent
    ax.add_patch(outer_circle)
    ax.add_patch(inner_circle)
    
    # Add surface texture (craters)
    crater_count = int(4 + abs(distortion_factor) * 3)
    
    for i in range(crater_count):
        # Random position within moon
        angle = np.random.uniform(0, 2*np.pi)
        distance = np.random.uniform(0.1, 0.7) * outer_r
        
        crater_x = cx + distance * np.cos(angle)
        crater_y = cy + distance * np.sin(angle)
        
        # Crater size with modulation
        crater_size = outer_r * np.random.uniform(0.05, 0.15) * (1.0 - abs(distortion_factor) * 0.3)
        
        # Crater shape (distorted circle)
        crater_rx = crater_size * (1.0 + distortion_factor * 0.2)
        crater_ry = crater_size * (1.0 - distortion_factor * 0.1)
        crater_angle = np.random.uniform(0, 180)
        
        crater = Ellipse((crater_x, crater_y), crater_rx, crater_ry,
                        angle=crater_angle,
                        facecolor="white", edgecolor="none", alpha=0.7)
        ax.add_patch(crater)
    
    return outer_r

def modulated_star(ax, cx, cy, base_size, size_modulation, spike_variation):
    # Calculate star dimensions with modulation
    outer_r = base_size * 0.15 * (1.0 + size_modulation * 0.5)
    inner_r = outer_r * 0.4 * (1.0 - size_modulation * 0.2)
    
    points = 5 + int(spike_variation * 3)  # 5 to 8 points
    
    # Create star points
    star_points = []
    
    for i in range(points * 2):
        angle = np.pi * i / points
        
        if i % 2 == 0:
            # Outer point
            r = outer_r * (1.0 + spike_variation * np.sin(angle * 2) * 0.2)
        else:
            # Inner point
            r = inner_r * (1.0 - spike_variation * np.cos(angle * 2) * 0.3)
        
        x = cx + r * np.cos(angle)
        y = cy + r * np.sin(angle)
        
        star_points.append([x, y])
    
    star = Polygon(star_points, closed=True,
                  facecolor="black", edgecolor="none")
    ax.add_patch(star)
    
    # Add star glow/effect
    glow_layers = int(2 + size_modulation * 2)
    
    for layer in range(glow_layers):
        glow_scale = 1.0 + (layer + 1) * 0.1
        
        glow_points = []
        for i in range(points * 2):
            angle = np.pi * i / points
            
            if i % 2 == 0:
                r = outer_r * glow_scale * (1.0 + spike_variation * np.sin(angle * 2) * 0.15)
            else:
                r = inner_r * glow_scale * (1.0 - spike_variation * np.cos(angle * 2) * 0.25)
            
            x = cx + r * np.cos(angle)
            y = cy + r * np.sin(angle)
            
            glow_points.append([x, y])
        
        glow = Polygon(glow_points, closed=True,
                      facecolor="white", edgecolor="none",
                      alpha=0.2 / (layer + 1))
        ax.add_patch(glow)
    
    return outer_r

def moon_star_composition(ax, cx, cy, base_size, seed):
    np.random.seed(seed)
    
    # Random parameters for this composition
    moon_distortion = np.random.uniform(-0.5, 0.5)
    moon_phase = np.random.uniform(0, 1)
    
    # Create distorted moon
    moon_r = distorted_crescent_moon(ax, cx, cy, base_size, 
                                    moon_distortion, moon_phase)
    
    # Create surrounding stars with modulated sizes
    star_count = np.random.randint(4, 8)
    star_angles = np.linspace(0, 2*np.pi, star_count, endpoint=False)
    
    # Shuffle and add random offset
    np.random.shuffle(star_angles)
    angle_offset = np.random.uniform(0, 2*np.pi)
    
    for i, angle in enumerate(star_angles):
        # Calculate star position (orbiting the moon)
        distance = moon_r * (1.5 + np.random.uniform(0, 0.5))
        star_angle = angle + angle_offset + np.random.uniform(-0.2, 0.2)
        
        star_x = cx + distance * np.cos(star_angle)
        star_y = cy + distance * np.sin(star_angle)
        
        # Modulate star size based on position
        size_modulation = np.random.uniform(-0.3, 0.3)
        spike_variation = np.random.uniform(0, 0.5)
        
        modulated_star(ax, star_x, star_y, base_size,
                      size_modulation, spike_variation)
    
    # Add connecting lines/constellation lines
    if np.random.random() > 0.3:
        line_count = np.random.randint(2, 4)
        
        # Select random stars to connect
        for _ in range(line_count):
            angle1 = np.random.choice(star_angles) + angle_offset
            angle2 = np.random.choice(star_angles) + angle_offset
            
            if angle1 != angle2:
                distance1 = moon_r * (1.5 + np.random.uniform(0, 0.3))
                distance2 = moon_r * (1.5 + np.random.uniform(0, 0.3))
                
                x1 = cx + distance1 * np.cos(angle1)
                y1 = cy + distance1 * np.sin(angle1)
                x2 = cx + distance2 * np.cos(angle2)
                y2 = cy + distance2 * np.sin(angle2)
                
                # Draw constellation line
                ax.plot([x1, x2], [y1, y2],
                       color="black", linewidth=np.random.uniform(0.4, 0.8),
                       alpha=0.7)


def draw():
    """Seamless moon and star pattern with crescent distortion and size modulation."""
    fig, ax = setup_ax()
    cols, rows = 6, 6
    dx, dy = PERIOD / cols, PERIOD / rows
    
    seed_offset = 500
    for row in range(rows):
        row_offset = (row % 2) * dx / 2
        
        for col in range(cols):
            # Vary position
            offset_x = np.random.uniform(-0.1, 0.1) * dx
            offset_y = np.random.uniform(-0.1, 0.1) * dy
            
            cx = col * dx + row_offset + offset_x + dx/2
            cy = row * dy + offset_y + dy/2
            
            # Base size with variation
            base_size = min(dx, dy) * np.random.uniform(0.6, 0.8)
            
            for ox, oy in WRAPS:
                moon_star_composition(ax, cx + ox, cy + oy, 
                                     base_size, seed_offset)
                seed_offset += 1
    
    save(fig, "abstract halloween variation moon star crescent distortion size modulation pattern black white texture")


if __name__ == "__main__":
    draw()