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

def modulated_bat(ax, cx, cy, base_size, seed):
    np.random.seed(seed)
    
    # Modulated parameters
    wing_asymmetry = np.random.uniform(-0.3, 0.3)  # Left/right asymmetry
    wingspan_mod = np.random.uniform(0.8, 1.2)     # Overall wingspan modulation
    body_scale = np.random.uniform(0.9, 1.1)       # Body size variation
    
    s = base_size * 0.7
    
    # Asymmetric body
    body_width = 0.3 * s * body_scale
    body_height = 0.4 * s * body_scale
    ax.add_patch(Ellipse((cx, cy), body_width, body_height, 
                        facecolor="black", edgecolor="none"))
    
    # Head
    head_r = 0.15 * s * body_scale
    ax.add_patch(Circle((cx, cy + body_height/2 + head_r*0.5), head_r,
                       facecolor="black", edgecolor="none"))
    
    # Ears
    ear_height = head_r * 0.8
    ear_width = head_r * 0.4
    
    # Left ear (modulated)
    left_ear = Polygon([(cx - head_r*0.7, cy + body_height/2 + head_r*0.5 + head_r),
                       (cx - head_r*0.7 - ear_width/2, cy + body_height/2 + head_r*0.5 + head_r + ear_height),
                       (cx - head_r*0.7 + ear_width/2, cy + body_height/2 + head_r*0.5 + head_r + ear_height)],
                      facecolor="black", edgecolor="none")
    ax.add_patch(left_ear)
    
    # Right ear (asymmetric)
    right_ear_height = ear_height * (1 + wing_asymmetry * 0.2)
    right_ear = Polygon([(cx + head_r*0.7, cy + body_height/2 + head_r*0.5 + head_r),
                        (cx + head_r*0.7 - ear_width/2, cy + body_height/2 + head_r*0.5 + head_r + right_ear_height),
                        (cx + head_r*0.7 + ear_width/2, cy + body_height/2 + head_r*0.5 + head_r + right_ear_height)],
                       facecolor="black", edgecolor="none")
    ax.add_patch(right_ear)
    
    # Wings with modulated spans and asymmetry
    wing_points_left = []
    wing_points_right = []
    
    # Left wing (modulated)
    left_wing_span = 0.8 * s * wingspan_mod * (1 + abs(wing_asymmetry) * 0.5)
    left_wing_height = 0.6 * s * wingspan_mod
    
    wing_points_left = [
        (cx - body_width/2, cy - body_height/3),  # Wing root
        (cx - left_wing_span, cy - left_wing_height * 0.7),  # Outer tip
        (cx - left_wing_span * 0.6, cy - left_wing_height),  # Bottom middle
        (cx - left_wing_span * 0.3, cy - left_wing_height * 0.8),  # Inner curve
        (cx - body_width/2, cy - body_height/3)  # Back to root
    ]
    
    left_wing = Polygon(wing_points_left, facecolor="black", edgecolor="none")
    ax.add_patch(left_wing)
    
    # Right wing (asymmetric)
    right_wing_span = 0.8 * s * wingspan_mod * (1 - abs(wing_asymmetry) * 0.3)
    right_wing_height = 0.6 * s * wingspan_mod * (1 + wing_asymmetry * 0.2)
    
    wing_points_right = [
        (cx + body_width/2, cy - body_height/3),  # Wing root
        (cx + right_wing_span, cy - right_wing_height * 0.7),  # Outer tip
        (cx + right_wing_span * 0.6, cy - right_wing_height),  # Bottom middle
        (cx + right_wing_span * 0.3, cy - right_wing_height * 0.8),  # Inner curve
        (cx + body_width/2, cy - body_height/3)  # Back to root
    ]
    
    right_wing = Polygon(wing_points_right, facecolor="black", edgecolor="none")
    ax.add_patch(right_wing)
    
    # Wing details - finger bones (asymmetric)
    finger_count = np.random.randint(2, 4)
    
    # Left wing fingers
    for i in range(finger_count):
        finger_length = left_wing_span * np.random.uniform(0.3, 0.5)
        start_x = cx - body_width/2 - i * 0.05 * s
        start_y = cy - body_height/3
        
        end_x = cx - left_wing_span * (0.8 - i * 0.15)
        end_y = cy - left_wing_height * (0.5 + i * 0.1)
        
        ax.plot([start_x, end_x], [start_y, end_y], 
               color="black", linewidth=np.random.uniform(0.8, 1.5))
    
    # Right wing fingers (different count for asymmetry)
    right_finger_count = finger_count + np.random.choice([-1, 0, 1])
    right_finger_count = max(2, min(4, right_finger_count))
    
    for i in range(right_finger_count):
        finger_length = right_wing_span * np.random.uniform(0.3, 0.5)
        start_x = cx + body_width/2 + i * 0.05 * s
        start_y = cy - body_height/3
        
        end_x = cx + right_wing_span * (0.8 - i * 0.15)
        end_y = cy - right_wing_height * (0.5 + i * 0.1)
        
        ax.plot([start_x, end_x], [start_y, end_y], 
               color="black", linewidth=np.random.uniform(0.8, 1.5))
    
    # Feet (asymmetric)
    foot_size = 0.08 * s
    
    # Left foot
    left_foot = Ellipse((cx - body_width/3, cy + body_height/2 - foot_size/2),
                       foot_size * 0.8, foot_size,
                       angle=30, facecolor="black", edgecolor="none")
    ax.add_patch(left_foot)
    
    # Right foot (different size/angle)
    right_foot_size = foot_size * np.random.uniform(0.9, 1.2)
    right_foot = Ellipse((cx + body_width/3, cy + body_height/2 - foot_size/2),
                        right_foot_size * 0.8, right_foot_size,
                        angle=-30, facecolor="black", edgecolor="none")
    ax.add_patch(right_foot)


def draw():
    """Seamless bat silhouette pattern with modulated wingspans and asymmetric forms."""
    fig, ax = setup_ax()
    cols, rows = 6, 6
    dx, dy = PERIOD / cols, PERIOD / rows
    
    seed_offset = 100
    for row in range(rows):
        for col in range(cols):
            # Vary position slightly
            offset_x = np.random.uniform(-0.15, 0.15) * dx
            offset_y = np.random.uniform(-0.15, 0.15) * dy
            
            cx = (col + 0.5) * dx + offset_x
            cy = (row + 0.5) * dy + offset_y
            
            # Base size with variation
            base_size = min(dx, dy) * np.random.uniform(0.6, 0.8)
            
            for ox, oy in WRAPS:
                modulated_bat(ax, cx + ox, cy + oy, base_size, seed_offset)
                seed_offset += 1
    
    save(fig, "abstract halloween variation bat silhouette modulated wingspan asymmetric forms pattern black white texture")


if __name__ == "__main__":
    draw()