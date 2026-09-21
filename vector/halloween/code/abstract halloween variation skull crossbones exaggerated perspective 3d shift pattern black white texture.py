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

def exaggerated_skull(ax, cx, cy, s, perspective):
    # Perspective scaling
    front_scale = 1.0 + perspective * 0.3
    back_scale = 1.0 - perspective * 0.2
    
    # Exaggerated skull head
    head_rx = 0.45 * s * front_scale
    head_ry = 0.4 * s * front_scale
    ax.add_patch(Ellipse((cx, cy + 0.2 * s * front_scale), 
                         head_rx, head_ry, 
                         facecolor="black", edgecolor="none"))
    
    # Exaggerated jaw with 3D effect
    jaw_width = 0.6 * s * back_scale
    jaw_height = 0.3 * s * back_scale
    jaw_y = cy - 0.1 * s * back_scale
    
    # Create perspective effect by shifting jaw downward
    jaw_shift = perspective * 0.15 * s
    ax.add_patch(FancyBboxPatch((cx - jaw_width/2, jaw_y + jaw_shift), 
                                jaw_width, jaw_height,
                                boxstyle="round,pad=0,rounding_size=" + str(0.06 * s),
                                facecolor="black", edgecolor="none"))
    
    # Exaggerated eye sockets
    eye_rx = 0.12 * s * front_scale
    eye_ry = 0.15 * s * front_scale
    eye_offset = 0.18 * s * front_scale
    
    # Left eye (slightly larger for perspective)
    left_eye_rx = eye_rx * (1 + perspective * 0.2)
    ax.add_patch(Ellipse((cx - eye_offset, cy + 0.22 * s * front_scale), 
                         left_eye_rx, eye_ry, 
                         facecolor="white", edgecolor="none"))
    
    # Right eye
    right_eye_rx = eye_rx * (1 - perspective * 0.1)
    ax.add_patch(Ellipse((cx + eye_offset, cy + 0.22 * s * front_scale), 
                         right_eye_rx, eye_ry, 
                         facecolor="white", edgecolor="none"))
    
    # Exaggerated nose
    nose_size = 0.08 * s * front_scale
    nose = Polygon(np.array([[cx, cy + 0.05 * s], 
                            [cx - nose_size, cy - 0.03 * s], 
                            [cx + nose_size, cy - 0.03 * s]]),
                   closed=True, facecolor="white", edgecolor="none")
    ax.add_patch(nose)
    
    # Exaggerated teeth with perspective distortion
    tooth_count = 5
    tooth_width = 0.06 * s * back_scale
    tooth_height = 0.12 * s * back_scale
    start_x = cx - (tooth_count - 1) * tooth_width / 2
    
    for i in range(tooth_count):
        tooth_x = start_x + i * tooth_width
        # Vary tooth height for perspective
        tooth_h = tooth_height * (1 - abs(i - (tooth_count-1)/2) * 0.3)
        tooth_y = jaw_y + jaw_shift - tooth_h * 0.8
        
        # Alternate tooth shapes
        if i % 2 == 0:
            # Pointed tooth
            points = [(tooth_x - tooth_width/2, tooth_y),
                     (tooth_x, tooth_y + tooth_h),
                     (tooth_x + tooth_width/2, tooth_y)]
            ax.add_patch(Polygon(points, facecolor="white", edgecolor="none"))
        else:
            # Square tooth with rounded top
            ax.add_patch(FancyBboxPatch((tooth_x - tooth_width/2, tooth_y), 
                                        tooth_width, tooth_h,
                                        boxstyle="round,pad=0,rounding_size=" + str(tooth_width/4),
                                        facecolor="white", edgecolor="none"))
    
    # Exaggerated crossbones
    bone_length = 0.8 * s * front_scale
    bone_width = 0.12 * s * back_scale
    
    # First bone (angled)
    angle1 = 45 + perspective * 10
    tr1 = Affine2D().rotate_deg(angle1).translate(cx, cy) + ax.transData
    bone1 = FancyBboxPatch((-bone_length/2, -bone_width/2), 
                          bone_length, bone_width,
                          boxstyle="round,pad=0,rounding_size=" + str(bone_width/2),
                          facecolor="black", edgecolor="none", 
                          transform=tr1)
    ax.add_patch(bone1)
    
    # Second bone (angled oppositely with perspective)
    angle2 = -45 - perspective * 5
    tr2 = Affine2D().rotate_deg(angle2).translate(cx, cy) + ax.transData
    bone2 = FancyBboxPatch((-bone_length/2, -bone_width/2), 
                          bone_length, bone_width,
                          boxstyle="round,pad=0,rounding_size=" + str(bone_width/2),
                          facecolor="black", edgecolor="none", 
                          transform=tr2)
    ax.add_patch(bone2)


def draw():
    """Seamless exaggerated skull-and-crossbones with 3D perspective shift."""
    fig, ax = setup_ax()
    n = 5
    step = PERIOD / n
    s = step * 0.65
    
    for row in range(n):
        for col in range(n):
            cx = (col + 0.5) * step
            cy = (row + 0.5) * step
            
            # Create perspective effect based on position
            perspective = (col + row) / (2 * (n - 1))
            
            for ox, oy in WRAPS:
                exaggerated_skull(ax, cx + ox, cy + oy, s, perspective)
    
    save(fig, "abstract halloween variation skull crossbones exaggerated perspective 3d shift pattern black white texture")


if __name__ == "__main__":
    draw()