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

def flame_effect(ax, cx, cy, size, intensity, rotation):
    # Apply rotation
    transform = Affine2D().rotate_deg(rotation).translate(cx, cy) + ax.transData
    
    # Base flame shape
    flame_height = size * (0.8 + intensity * 0.4)
    flame_width = size * (0.5 + intensity * 0.3)
    
    # Create flickering flame shape
    flame_points = []
    resolution = 20
    
    # Start at bottom center
    flame_points.append([0, -flame_height/2])
    
    # Right side with flicker
    for i in range(resolution + 1):
        t = i / resolution
        angle = np.pi * t  # 0 to pi
        
        # Flicker modulation
        flicker = np.sin(angle * 4 + intensity * 2) * 0.2
        
        x = flame_width/2 * np.sin(angle) * (1 + flicker)
        y = -flame_height/2 + flame_height * t
        
        flame_points.append([x, y])
    
    # Left side with different flicker
    for i in range(resolution, -1, -1):
        t = i / resolution
        angle = np.pi * t
        
        # Different flicker pattern
        flicker = np.cos(angle * 3 + intensity * 3) * 0.15
        
        x = -flame_width/2 * np.sin(angle) * (1 + flicker)
        y = -flame_height/2 + flame_height * t
        
        flame_points.append([x, y])
    
    # Close the shape
    flame_points.append([0, -flame_height/2])
    
    flame = Polygon(flame_points, closed=True,
                   facecolor="black", edgecolor="none",
                   transform=transform)
    ax.add_patch(flame)
    
    # Inner flame (lighter)
    inner_height = flame_height * 0.7
    inner_width = flame_width * 0.6
    
    inner_points = []
    inner_points.append([0, -inner_height/2])
    
    for i in range(resolution + 1):
        t = i / resolution
        angle = np.pi * t
        
        flicker = np.sin(angle * 5 + intensity * 4) * 0.1
        
        x = inner_width/2 * np.sin(angle) * (1 + flicker)
        y = -inner_height/2 + inner_height * t
        
        inner_points.append([x, y])
    
    for i in range(resolution, -1, -1):
        t = i / resolution
        angle = np.pi * t
        
        flicker = np.cos(angle * 4 + intensity * 5) * 0.12
        
        x = -inner_width/2 * np.sin(angle) * (1 + flicker)
        y = -inner_height/2 + inner_height * t
        
        inner_points.append([x, y])
    
    inner_points.append([0, -inner_height/2])
    
    inner_flame = Polygon(inner_points, closed=True,
                         facecolor="white", edgecolor="none",
                         transform=transform, alpha=0.8)
    ax.add_patch(inner_flame)
    
    # Flame tips/sparks
    spark_count = int(3 + intensity * 4)
    
    for _ in range(spark_count):
        spark_angle = np.random.uniform(0, 2*np.pi)
        spark_distance = flame_height * 0.4 + np.random.uniform(0, flame_height * 0.2)
        
        spark_x = spark_distance * np.cos(spark_angle)
        spark_y = spark_distance * np.sin(spark_angle) - flame_height/4
        
        spark_size = size * np.random.uniform(0.03, 0.08)
        
        # Transform spark position
        spark_pos = transform.transform([spark_x, spark_y])
        
        # Spark shape (small flame or circle)
        if np.random.random() > 0.5:
            spark = Circle(spark_pos, spark_size,
                          facecolor="black", edgecolor="none")
        else:
            # Tiny flame spark
            spark_points = [
                [spark_pos[0] - spark_size/2, spark_pos[1]],
                [spark_pos[0], spark_pos[1] + spark_size],
                [spark_pos[0] + spark_size/2, spark_pos[1]]
            ]
            spark = Polygon(spark_points, closed=True,
                           facecolor="black", edgecolor="none")
        
        ax.add_patch(spark)

def rotating_pentacle(ax, cx, cy, size, rotation, element_rotation):
    # Main pentacle circle
    circle_r = size * 0.45
    ax.add_patch(Circle((cx, cy), circle_r,
                       facecolor="black", edgecolor="none"))
    
    # Inner circle
    inner_r = circle_r * 0.7
    ax.add_patch(Circle((cx, cy), inner_r,
                       facecolor="white", edgecolor="none"))
    
    # Pentagram (5-pointed star)
    points = 5
    outer_r = size * 0.4
    inner_r_star = outer_r * 0.38
    
    star_points = []
    
    for i in range(points * 2):
        angle = 2 * np.pi * i / (points * 2) + np.radians(rotation)
        
        if i % 2 == 0:
            r = outer_r
        else:
            r = inner_r_star
        
        x = cx + r * np.cos(angle)
        y = cy + r * np.sin(angle)
        
        star_points.append([x, y])
    
    pentagram = Polygon(star_points, closed=True,
                       facecolor="black", edgecolor="none")
    ax.add_patch(pentagram)
    
    # Rotating elements at pentagram points
    element_count = points
    element_angles = [2 * np.pi * i / element_count + np.radians(rotation) for i in range(element_count)]
    
    for i, angle in enumerate(element_angles):
        element_distance = outer_r * 0.85
        element_x = cx + element_distance * np.cos(angle)
        element_y = cy + element_distance * np.sin(angle)
        
        # Element size and rotation
        element_size = size * 0.15
        element_rot = element_rotation + i * 72  # 72 degrees between elements
        
        # Create rotating element (gear-like)
        element_points = []
        gear_teeth = 8
        
        for j in range(gear_teeth * 2):
            gear_angle = 2 * np.pi * j / (gear_teeth * 2) + np.radians(element_rot)
            
            if j % 2 == 0:
                r = element_size * 0.9
            else:
                r = element_size * 0.6
            
            x = element_x + r * np.cos(gear_angle)
            y = element_y + r * np.sin(gear_angle)
            
            element_points.append([x, y])
        
        element = Polygon(element_points, closed=True,
                         facecolor="white", edgecolor="none")
        ax.add_patch(element)
        
        # Element center
        center_r = element_size * 0.3
        ax.add_patch(Circle((element_x, element_y), center_r,
                           facecolor="black", edgecolor="none"))
    
    # Connecting lines between rotating elements
    for i in range(element_count):
        angle1 = element_angles[i]
        angle2 = element_angles[(i + 2) % element_count]  # Skip one element
        
        x1 = cx + outer_r * 0.85 * np.cos(angle1)
        y1 = cy + outer_r * 0.85 * np.sin(angle1)
        x2 = cx + outer_r * 0.85 * np.cos(angle2)
        y2 = cy + outer_r * 0.85 * np.sin(angle2)
        
        # Curved connecting line
        mid_x = (x1 + x2) / 2 + (y2 - y1) * 0.2
        mid_y = (y1 + y2) / 2 - (x2 - x1) * 0.2
        
        t = np.linspace(0, 1, 30)
        curve_x = (1-t)**2 * x1 + 2*(1-t)*t * mid_x + t**2 * x2
        curve_y = (1-t)**2 * y1 + 2*(1-t)*t * mid_y + t**2 * y2
        
        ax.plot(curve_x, curve_y, color="black",
               linewidth=size * 0.01, alpha=0.7)
    
    # Runic symbols at inner circle
    rune_count = 5
    rune_angles = [2 * np.pi * i / rune_count + np.radians(rotation + 36) for i in range(rune_count)]
    
    for angle in rune_angles:
        rune_distance = inner_r * 0.8
        rune_x = cx + rune_distance * np.cos(angle)
        rune_y = cy + rune_distance * np.sin(angle)
        
        # Simple rune symbol (triangle based)
        rune_size = size * 0.08
        
        # Random rune type
        rune_type = np.random.choice(["triangle", "cross", "circle"])
        
        if rune_type == "triangle":
            rune_points = [
                [rune_x, rune_y + rune_size],
                [rune_x - rune_size * 0.866, rune_y - rune_size/2],
                [rune_x + rune_size * 0.866, rune_y - rune_size/2]
            ]
            rune = Polygon(rune_points, closed=True,
                          facecolor="black", edgecolor="none")
        elif rune_type == "cross":
            # Plus sign
            rune_width = rune_size * 0.2
            rune_height = rune_size * 0.6
            
            rune_points = []
            rune_points.append([rune_x - rune_width/2, rune_y - rune_height/2])
            rune_points.append([rune_x - rune_width/2, rune_y + rune_height/2])
            rune_points.append([rune_x + rune_width/2, rune_y + rune_height/2])
            rune_points.append([rune_x + rune_width/2, rune_y - rune_height/2])
            
            # Add crossbar
            rune_points.append([rune_x - rune_height/2, rune_y - rune_width/2])
            rune_points.append([rune_x - rune_height/2, rune_y + rune_width/2])
            rune_points.append([rune_x + rune_height/2, rune_y + rune_width/2])
            rune_points.append([rune_x + rune_height/2, rune_y - rune_width/2])
            
            rune = Polygon(rune_points, closed=True,
                          facecolor="black", edgecolor="none")
        else:  # circle
            rune = Circle((rune_x, rune_y), rune_size * 0.5,
                         facecolor="black", edgecolor="none")
        
        ax.add_patch(rune)

def pentacle_flame_composition(ax, cx, cy, base_size, seed):
    np.random.seed(seed)
    
    # Random parameters
    pentacle_rotation = np.random.uniform(0, 360)
    element_rotation = np.random.uniform(0, 360)
    flame_intensity = np.random.uniform(0.5, 1.0)
    
    # Create pentacle
    rotating_pentacle(ax, cx, cy, base_size, 
                     pentacle_rotation, element_rotation)
    
    # Create surrounding flames
    flame_count = np.random.randint(4, 7)
    flame_angles = np.linspace(0, 2*np.pi, flame_count, endpoint=False)
    
    # Add random offset and shuffle
    flame_offset = np.random.uniform(0, 2*np.pi)
    np.random.shuffle(flame_angles)
    
    for i, angle in enumerate(flame_angles):
        # Flame distance and size
        flame_distance = base_size * (0.6 + np.random.uniform(0, 0.3))
        flame_size = base_size * (0.25 + np.random.uniform(-0.05, 0.1))
        
        flame_x = cx + flame_distance * np.cos(angle + flame_offset)
        flame_y = cy + flame_distance * np.sin(angle + flame_offset)
        
        # Flame rotation (pointing outward from center)
        flame_rotation = np.degrees(angle + flame_offset) + 90
        
        flame_effect(ax, flame_x, flame_y, flame_size,
                    flame_intensity, flame_rotation)
    
    # Connecting energy lines
    if np.random.random() > 0.2:
        line_count = np.random.randint(3, 6)
        
        for _ in range(line_count):
            # Connect random flames
            idx1 = np.random.randint(0, flame_count)
            idx2 = np.random.randint(0, flame_count)
            
            if idx1 != idx2:
                angle1 = flame_angles[idx1] + flame_offset
                angle2 = flame_angles[idx2] + flame_offset
                
                distance1 = base_size * (0.6 + np.random.uniform(0, 0.2))
                distance2 = base_size * (0.6 + np.random.uniform(0, 0.2))
                
                x1 = cx + distance1 * np.cos(angle1)
                y1 = cy + distance1 * np.sin(angle1)
                x2 = cx + distance2 * np.cos(angle2)
                y2 = cy + distance2 * np.sin(angle2)
                
                # Draw energy line with glow effect
                line_width = base_size * 0.015
                
                # Main line
                ax.plot([x1, x2], [y1, y2],
                       color="black", linewidth=line_width,
                       solid_capstyle="round")
                
                # Glow effect
                ax.plot([x1, x2], [y1, y2],
                       color="white", linewidth=line_width * 0.5,
                       alpha=0.6, solid_capstyle="round")


def draw():
    """Seamless pentacle pattern with flame effects and rotating elements."""
    fig, ax = setup_ax()
    cols, rows = 4, 4
    dx, dy = PERIOD / cols, PERIOD / rows
    
    seed_offset = 700
    for row in range(rows):
        row_offset = (row % 2) * dx / 2
        
        for col in range(cols):
            # Vary position
            offset_x = np.random.uniform(-0.15, 0.15) * dx
            offset_y = np.random.uniform(-0.15, 0.15) * dy
            
            cx = col * dx + row_offset + offset_x + dx/2
            cy = row * dy + offset_y + dy/2
            
            # Base size with variation
            base_size = min(dx, dy) * np.random.uniform(0.5, 0.7)
            
            for ox, oy in WRAPS:
                pentacle_flame_composition(ax, cx + ox, cy + oy,
                                          base_size, seed_offset)
                seed_offset += 1
    
    save(fig, "abstract halloween variation pentacle flame effects rotating elements pattern black white texture")


if __name__ == "__main__":
    draw()