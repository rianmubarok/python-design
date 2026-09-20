import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime

SIZE = 4000
DPI = 300
SEED = 42
DATE = datetime.now().strftime("%d%m%Y")

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR.parent / "output"
JPG_DIR = OUTPUT_DIR / "jpg"
SVG_DIR = OUTPUT_DIR / "svg"
JPG_DIR.mkdir(parents=True, exist_ok=True)
SVG_DIR.mkdir(parents=True, exist_ok=True)

np.random.seed(SEED)


def setup_ax():
    fig, ax = plt.subplots(figsize=(SIZE/DPI, SIZE/DPI), dpi=DPI)
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


def draw_crease_pattern(cx, cy, module_size, fold_type='valley'):
    """
    Draw origami crease pattern module.
    Different fold types create different line patterns.
    """
    half_size = module_size / 2
    
    # Basic square boundary
    boundary = [
        (cx - half_size, cy - half_size),
        (cx + half_size, cy - half_size),
        (cx + half_size, cy + half_size),
        (cx - half_size, cy + half_size),
        (cx - half_size, cy - half_size)
    ]
    
    boundary_x = [p[0] for p in boundary]
    boundary_y = [p[1] for p in boundary]
    
    creases = []
    
    if fold_type == 'valley':
        # Valley fold pattern - diagonal creases
        creases.extend([
            [(cx - half_size, cy - half_size), (cx + half_size, cy + half_size)],
            [(cx + half_size, cy - half_size), (cx - half_size, cy + half_size)],
        ])
    
    elif fold_type == 'mountain':
        # Mountain fold pattern - perpendicular bisectors
        creases.extend([
            [(cx, cy - half_size), (cx, cy + half_size)],
            [(cx - half_size, cy), (cx + half_size, cy)],
        ])
    
    elif fold_type == 'waterbomb':
        # Waterbomb base pattern
        quarter_size = module_size / 4
        creases.extend([
            [(cx - quarter_size, cy - half_size), (cx, cy)],
            [(cx + quarter_size, cy - half_size), (cx, cy)],
            [(cx + half_size, cy - quarter_size), (cx, cy)],
            [(cx + half_size, cy + quarter_size), (cx, cy)],
            [(cx + quarter_size, cy + half_size), (cx, cy)],
            [(cx - quarter_size, cy + half_size), (cx, cy)],
            [(cx - half_size, cy + quarter_size), (cx, cy)],
            [(cx - half_size, cy - quarter_size), (cx, cy)],
        ])
    
    elif fold_type == 'bird_base':
        # Bird base preliminary creases
        creases.extend([
            # Main diagonals
            [(cx - half_size, cy - half_size), (cx + half_size, cy + half_size)],
            [(cx + half_size, cy - half_size), (cx - half_size, cy + half_size)],
            # Perpendicular bisectors
            [(cx, cy - half_size), (cx, cy + half_size)],
            [(cx - half_size, cy), (cx + half_size, cy)],
            # Additional creases for bird base
            [(cx - half_size, cy), (cx, cy - half_size)],
            [(cx, cy - half_size), (cx + half_size, cy)],
            [(cx + half_size, cy), (cx, cy + half_size)],
            [(cx, cy + half_size), (cx - half_size, cy)],
        ])
    
    elif fold_type == 'tessellation':
        # Complex tessellation pattern
        third_size = module_size / 3
        creases.extend([
            # Grid lines
            [(cx - third_size, cy - half_size), (cx - third_size, cy + half_size)],
            [(cx + third_size, cy - half_size), (cx + third_size, cy + half_size)],
            [(cx - half_size, cy - third_size), (cx + half_size, cy - third_size)],
            [(cx - half_size, cy + third_size), (cx + half_size, cy + third_size)],
            # Diagonal connections
            [(cx - third_size, cy - third_size), (cx + third_size, cy + third_size)],
            [(cx + third_size, cy - third_size), (cx - third_size, cy + third_size)],
        ])
    
    return boundary_x, boundary_y, creases


def modular_origami_crease_fold():
    """
    Modular origami crease and fold pattern.
    Shows different origami fold patterns in a tessellated arrangement.
    """
    fig, ax = setup_ax()
    
    module_size = 12
    grid_cols = 8
    grid_rows = 8
    
    fold_types = ['valley', 'mountain', 'waterbomb', 'bird_base', 'tessellation']
    
    for row in range(grid_rows):
        for col in range(grid_cols):
            # Module center position
            cx = 12.5 + col * module_size
            cy = 12.5 + row * module_size
            
            # Skip if outside canvas
            if cx > 95 or cy > 95:
                continue
            
            # Choose fold type based on position pattern
            fold_type_idx = (row + col) % len(fold_types)
            fold_type = fold_types[fold_type_idx]
            
            # Get crease pattern for this module
            boundary_x, boundary_y, creases = draw_crease_pattern(cx, cy, module_size, fold_type)
            
            # Draw module boundary
            boundary_lw = 1.5 if fold_type in ['waterbomb', 'bird_base'] else 1.0
            ax.plot(boundary_x, boundary_y, color="black", linewidth=boundary_lw, solid_capstyle="round")
            
            # Draw crease lines with different styles for different fold types
            for crease in creases:
                start, end = crease
                
                if fold_type == 'valley':
                    # Dashed lines for valley folds
                    ax.plot([start[0], end[0]], [start[1], end[1]], 
                           color="black", linewidth=0.8, linestyle=(0, (3, 2)))
                
                elif fold_type == 'mountain':
                    # Dash-dot lines for mountain folds
                    ax.plot([start[0], end[0]], [start[1], end[1]], 
                           color="black", linewidth=0.8, linestyle=(0, (5, 2, 1, 2)))
                
                elif fold_type == 'waterbomb':
                    # Alternating solid/dashed for complex pattern
                    line_idx = creases.index(crease)
                    if line_idx % 2 == 0:
                        ax.plot([start[0], end[0]], [start[1], end[1]], 
                               color="black", linewidth=0.6, linestyle='-')
                    else:
                        ax.plot([start[0], end[0]], [start[1], end[1]], 
                               color="black", linewidth=0.6, linestyle=(0, (2, 1)))
                
                elif fold_type == 'bird_base':
                    # Varied line weights for hierarchy
                    line_idx = creases.index(crease)
                    if line_idx < 4:  # Main creases
                        ax.plot([start[0], end[0]], [start[1], end[1]], 
                               color="black", linewidth=1.0, linestyle='-')
                    else:  # Secondary creases
                        ax.plot([start[0], end[0]], [start[1], end[1]], 
                               color="black", linewidth=0.6, linestyle=(0, (3, 1)))
                
                elif fold_type == 'tessellation':
                    # Dotted lines for tessellation pattern
                    ax.plot([start[0], end[0]], [start[1], end[1]], 
                           color="black", linewidth=0.5, linestyle=(0, (1, 1)))
    
    # Add connecting elements between modules
    # Valley and mountain fold connections
    for row in range(grid_rows - 1):
        for col in range(grid_cols - 1):
            cx1 = 12.5 + col * module_size
            cy1 = 12.5 + row * module_size
            cx2 = cx1 + module_size
            cy2 = cy1 + module_size
            
            if cx2 <= 95 and cy2 <= 95:
                # Connect adjacent modules with fold lines
                fold_type1 = fold_types[(row + col) % len(fold_types)]
                fold_type2 = fold_types[(row + col + 1) % len(fold_types)]
                
                # Horizontal connection
                if fold_type1 == fold_type2:
                    ax.plot([cx1 + module_size/2, cx2 + module_size/2], 
                           [cy1, cy1], color="black", linewidth=0.4, alpha=0.6)
                
                # Vertical connection  
                ax.plot([cx1, cx1], [cy1 + module_size/2, cy2 + module_size/2], 
                       color="black", linewidth=0.4, alpha=0.6)
    
    # Add corner reinforcement patterns
    corner_positions = [(18, 18), (82, 18), (18, 82), (82, 82), (50, 50)]
    
    for corner_x, corner_y in corner_positions:
        # Small decorative fold pattern at corners
        corner_size = 4
        corner_angles = [0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi]
        
        for i in range(len(corner_angles) - 1):
            start_angle = corner_angles[i]
            end_angle = corner_angles[i + 1]
            
            # Radial crease
            ax.plot([corner_x, corner_x + corner_size * np.cos(start_angle)], 
                   [corner_y, corner_y + corner_size * np.sin(start_angle)],
                   color="black", linewidth=0.6, alpha=0.8)
            
            # Arc between radial creases
            arc_angles = np.linspace(start_angle, end_angle, 8)
            arc_x = [corner_x + corner_size * 0.7 * np.cos(a) for a in arc_angles]
            arc_y = [corner_y + corner_size * 0.7 * np.sin(a) for a in arc_angles]
            
            ax.plot(arc_x, arc_y, color="black", linewidth=0.4, alpha=0.6)
    
    save(fig, "modular origami crease fold")


if __name__ == "__main__":
    modular_origami_crease_fold()