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

def cracked_tombstone(ax, cx, cy, width, height, tilt_angle, crack_intensity):
    # Apply tilt transformation
    transform = Affine2D().rotate_deg(tilt_angle).translate(cx, cy) + ax.transData
    
    # Tombstone base shape (rounded top, flat bottom)
    base_points = []
    resolution = 24
    
    # Bottom flat part
    base_points.append([-width/2, -height/2])
    
    # Rounded top
    for i in range(resolution + 1):
        angle = np.pi * i / resolution  # 0 to pi
        x = -width/2 * np.cos(angle)
        y = height/2 * np.sin(angle) - height/2
        base_points.append([x, y])
    
    # Other side
    base_points.append([width/2, -height/2])
    
    tombstone = Polygon(base_points, closed=True,
                       facecolor="black", edgecolor="none",
                       transform=transform)
    ax.add_patch(tombstone)
    
    # Cracks on surface
    crack_count = int(3 + crack_intensity * 5)
    
    for crack_idx in range(crack_count):
        # Random crack starting point
        start_x = np.random.uniform(-width/3, width/3)
        start_y = np.random.uniform(-height/3, height/4)
        
        # Crack path
        crack_points = [[start_x, start_y]]
        segments = np.random.randint(2, 6)
        
        current_x, current_y = start_x, start_y
        crack_length = 0
        
        for seg in range(segments):
            # Crack direction and length
            angle = np.random.uniform(0, 2*np.pi)
            seg_length = np.random.uniform(0.05, 0.2) * min(width, height) * (1 + crack_intensity)
            
            # Ensure crack stays within tombstone bounds
            next_x = current_x + seg_length * np.cos(angle)
            next_y = current_y + seg_length * np.sin(angle)
            
            # Boundary check
            if abs(next_x) > width/2 * 0.9:
                next_x = np.sign(next_x) * width/2 * 0.9
            if next_y > height/2 * 0.9 - height/2:
                next_y = height/2 * 0.9 - height/2
            if next_y < -height/2:
                next_y = -height/2 * 0.9
            
            crack_points.append([next_x, next_y])
            current_x, current_y = next_x, next_y
            crack_length += seg_length
        
        # Draw crack
        crack_arr = np.array(crack_points)
        
        # Transform crack points
        transformed_points = []
        for point in crack_arr:
            x, y = point
            # Apply same tilt transform
            transformed_points.append(transform.transform([x, y]))
        
        transformed_arr = np.array(transformed_points)
        
        # Vary crack width
        crack_width = np.random.uniform(0.8, 1.5) * (1 + crack_intensity * 0.5)
        
        ax.plot(transformed_arr[:, 0], transformed_arr[:, 1],
               color="white", linewidth=crack_width, solid_capstyle="round")
    
    # Moss/weathering effects
    moss_count = int(5 + crack_intensity * 8)
    
    for _ in range(moss_count):
        moss_x = np.random.uniform(-width/2.5, width/2.5)
        moss_y = np.random.uniform(-height/2, height/4 - height/2)
        
        moss_size = np.random.uniform(0.02, 0.08) * min(width, height)
        
        # Transform moss position
        moss_pos = transform.transform([moss_x, moss_y])
        
        # Moss patches (irregular shapes)
        if np.random.random() > 0.3:
            # Circular moss
            moss = Circle(moss_pos, moss_size,
                         facecolor="white", edgecolor="none", alpha=0.7)
            ax.add_patch(moss)
        else:
            # Irregular moss shape
            points = []
            moss_points = np.random.randint(5, 9)
            for i in range(moss_points):
                angle = 2 * np.pi * i / moss_points
                r = moss_size * np.random.uniform(0.7, 1.3)
                dx = r * np.cos(angle)
                dy = r * np.sin(angle)
                points.append([moss_pos[0] + dx, moss_pos[1] + dy])
            
            moss_patch = Polygon(points, closed=True,
                                facecolor="white", edgecolor="none", alpha=0.6)
            ax.add_patch(moss_patch)
    
    # Epitaph/RIP text (simplified as geometric shapes)
    text_height = height * 0.15
    text_y = -height/4
    
    # "R" shape
    r_x = -width/4
    r_points = [
        [r_x - text_height/3, text_y - text_height/2],
        [r_x - text_height/3, text_y + text_height/2],
        [r_x + text_height/3, text_y + text_height/2],
        [r_x + text_height/3, text_y],
        [r_x - text_height/3, text_y],
        [r_x, text_y - text_height/2]
    ]
    
    # Transform R points
    transformed_r = []
    for point in r_points:
        transformed_r.append(transform.transform(point))
    
    r_poly = Polygon(transformed_r, closed=True,
                    facecolor="white", edgecolor="none", alpha=0.9)
    ax.add_patch(r_poly)
    
    # "I" shape
    i_x = 0
    i_points = [
        [i_x - text_height/6, text_y - text_height/2],
        [i_x + text_height/6, text_y - text_height/2],
        [i_x + text_height/6, text_y + text_height/2],
        [i_x - text_height/6, text_y + text_height/2]
    ]
    
    transformed_i = []
    for point in i_points:
        transformed_i.append(transform.transform(point))
    
    i_poly = Polygon(transformed_i, closed=True,
                    facecolor="white", edgecolor="none", alpha=0.9)
    ax.add_patch(i_poly)
    
    # "P" shape
    p_x = width/4
    p_points = [
        [p_x - text_height/3, text_y - text_height/2],
        [p_x - text_height/3, text_y + text_height/2],
        [p_x + text_height/3, text_y + text_height/2],
        [p_x + text_height/3, text_y],
        [p_x - text_height/3, text_y]
    ]
    
    transformed_p = []
    for point in p_points:
        transformed_p.append(transform.transform(point))
    
    p_poly = Polygon(transformed_p, closed=True,
                    facecolor="white", edgecolor="none", alpha=0.9)
    ax.add_patch(p_poly)
    
    # Base/ground line
    ground_width = width * 1.2
    ground_y = -height/2 - height * 0.05
    
    ground_points = [
        [-ground_width/2, ground_y],
        [-ground_width/2, ground_y - height * 0.05],
        [ground_width/2, ground_y - height * 0.05],
        [ground_width/2, ground_y]
    ]
    
    transformed_ground = []
    for point in ground_points:
        transformed_ground.append(transform.transform(point))
    
    ground = Polygon(transformed_ground, closed=True,
                    facecolor="black", edgecolor="none")
    ax.add_patch(ground)


def draw():
    """Seamless tombstone pattern with cracked surfaces and tilted angles."""
    fig, ax = setup_ax()
    cols, rows = 5, 5
    dx, dy = PERIOD / cols, PERIOD / rows
    
    seed_offset = 400
    for row in range(rows):
        for col in range(cols):
            # Vary position
            offset_x = np.random.uniform(-0.15, 0.15) * dx
            offset_y = np.random.uniform(-0.15, 0.15) * dy
            
            cx = (col + 0.5) * dx + offset_x
            cy = (row + 0.5) * dy + offset_y
            
            # Vary dimensions and parameters
            width = dx * np.random.uniform(0.4, 0.6)
            height = dy * np.random.uniform(0.5, 0.7)
            tilt_angle = np.random.uniform(-15, 15)
            crack_intensity = np.random.uniform(0.3, 0.8)
            
            for ox, oy in WRAPS:
                cracked_tombstone(ax, cx + ox, cy + oy,
                                 width, height, tilt_angle, crack_intensity)
                seed_offset += 1
    
    save(fig, "abstract halloween variation tombstone cracked surfaces tilted angles pattern black white texture")


if __name__ == "__main__":
    draw()