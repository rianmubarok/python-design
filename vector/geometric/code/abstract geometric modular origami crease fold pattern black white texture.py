import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime

SIZE = 4000
DPI = 300
SEED = 42
DATE = datetime.now().strftime("%d%m%Y")

SCRIPT DIR = Path(  file  ).resolve().parent
OUTPUT DIR = SCRIPT DIR.parent / "output"
JPG DIR = OUTPUT DIR / "jpg"
SVG DIR = OUTPUT DIR / "svg"
JPG DIR.mkdir(parents=True, exist ok=True)
SVG DIR.mkdir(parents=True, exist ok=True)

np.random.seed(SEED)


def setup ax():
    fig, ax = plt.subplots(figsize=(SIZE/DPI, SIZE/DPI), dpi=DPI)
    fig.subplots adjust(left=0, right=1, top=1, bottom=0)
    ax.set facecolor("white")
    ax.set xlim(-5, 105)
    ax.set ylim(-5, 105)
    ax.set aspect("equal")
    ax.axis("off")
    return fig, ax


def save(fig, name):
    jpg path = JPG DIR / f"{name} {DATE}.jpg"
    svg path = SVG DIR / f"{name} {DATE}.svg"
    fig.savefig(jpg path, dpi=DPI, pad inches=0, facecolor="white")
    fig.savefig(svg path, format="svg", pad inches=0, facecolor="white")
    plt.close(fig)
    print(f"Tersimpan: {jpg path} | {svg path}")


def draw crease pattern(cx, cy, module size, fold type='valley'):
    """
    Draw origami crease pattern module.
    Different fold types create different line patterns.
    """
    half size = module size / 2
    
    # Basic square boundary
    boundary = [
        (cx - half size, cy - half size),
        (cx + half size, cy - half size),
        (cx + half size, cy + half size),
        (cx - half size, cy + half size),
        (cx - half size, cy - half size)
    ]
    
    boundary x = [p[0] for p in boundary]
    boundary y = [p[1] for p in boundary]
    
    creases = []
    
    if fold type == 'valley':
        # Valley fold pattern - diagonal creases
        creases.extend([
            [(cx - half size, cy - half size), (cx + half size, cy + half size)],
            [(cx + half size, cy - half size), (cx - half size, cy + half size)],
        ])
    
    elif fold type == 'mountain':
        # Mountain fold pattern - perpendicular bisectors
        creases.extend([
            [(cx, cy - half size), (cx, cy + half size)],
            [(cx - half size, cy), (cx + half size, cy)],
        ])
    
    elif fold type == 'waterbomb':
        # Waterbomb base pattern
        quarter size = module size / 4
        creases.extend([
            [(cx - quarter size, cy - half size), (cx, cy)],
            [(cx + quarter size, cy - half size), (cx, cy)],
            [(cx + half size, cy - quarter size), (cx, cy)],
            [(cx + half size, cy + quarter size), (cx, cy)],
            [(cx + quarter size, cy + half size), (cx, cy)],
            [(cx - quarter size, cy + half size), (cx, cy)],
            [(cx - half size, cy + quarter size), (cx, cy)],
            [(cx - half size, cy - quarter size), (cx, cy)],
        ])
    
    elif fold type == 'bird base':
        # Bird base preliminary creases
        creases.extend([
            # Main diagonals
            [(cx - half size, cy - half size), (cx + half size, cy + half size)],
            [(cx + half size, cy - half size), (cx - half size, cy + half size)],
            # Perpendicular bisectors
            [(cx, cy - half size), (cx, cy + half size)],
            [(cx - half size, cy), (cx + half size, cy)],
            # Additional creases for bird base
            [(cx - half size, cy), (cx, cy - half size)],
            [(cx, cy - half size), (cx + half size, cy)],
            [(cx + half size, cy), (cx, cy + half size)],
            [(cx, cy + half size), (cx - half size, cy)],
        ])
    
    elif fold type == 'tessellation':
        # Complex tessellation pattern
        third size = module size / 3
        creases.extend([
            # Grid lines
            [(cx - third size, cy - half size), (cx - third size, cy + half size)],
            [(cx + third size, cy - half size), (cx + third size, cy + half size)],
            [(cx - half size, cy - third size), (cx + half size, cy - third size)],
            [(cx - half size, cy + third size), (cx + half size, cy + third size)],
            # Diagonal connections
            [(cx - third size, cy - third size), (cx + third size, cy + third size)],
            [(cx + third size, cy - third size), (cx - third size, cy + third size)],
        ])
    
    return boundary x, boundary y, creases


def modular origami crease fold():
    """
    Modular origami crease and fold pattern.
    Shows different origami fold patterns in a tessellated arrangement.
    """
    fig, ax = setup ax()
    
    module size = 12
    grid cols = 8
    grid rows = 8
    
    fold types = ['valley', 'mountain', 'waterbomb', 'bird base', 'tessellation']
    
    for row in range(grid rows):
        for col in range(grid cols):
            # Module center position
            cx = 12.5 + col * module size
            cy = 12.5 + row * module size
            
            # Skip if outside canvas
            if cx > 95 or cy > 95:
                continue
            
            # Choose fold type based on position pattern
            fold type idx = (row + col) % len(fold types)
            fold type = fold types[fold type idx]
            
            # Get crease pattern for this module
            boundary x, boundary y, creases = draw crease pattern(cx, cy, module size, fold type)
            
            # Draw module boundary
            boundary lw = 1.5 if fold type in ['waterbomb', 'bird base'] else 1.0
            ax.plot(boundary x, boundary y, color="black", linewidth=boundary lw, solid capstyle="round")
            
            # Draw crease lines with different styles for different fold types
            for crease in creases:
                start, end = crease
                
                if fold type == 'valley':
                    # Dashed lines for valley folds
                    ax.plot([start[0], end[0]], [start[1], end[1]], 
                           color="black", linewidth=0.8, linestyle=(0, (3, 2)))
                
                elif fold type == 'mountain':
                    # Dash-dot lines for mountain folds
                    ax.plot([start[0], end[0]], [start[1], end[1]], 
                           color="black", linewidth=0.8, linestyle=(0, (5, 2, 1, 2)))
                
                elif fold type == 'waterbomb':
                    # Alternating solid/dashed for complex pattern
                    line idx = creases.index(crease)
                    if line idx % 2 == 0:
                        ax.plot([start[0], end[0]], [start[1], end[1]], 
                               color="black", linewidth=0.6, linestyle='-')
                    else:
                        ax.plot([start[0], end[0]], [start[1], end[1]], 
                               color="black", linewidth=0.6, linestyle=(0, (2, 1)))
                
                elif fold type == 'bird base':
                    # Varied line weights for hierarchy
                    line idx = creases.index(crease)
                    if line idx < 4:  # Main creases
                        ax.plot([start[0], end[0]], [start[1], end[1]], 
                               color="black", linewidth=1.0, linestyle='-')
                    else:  # Secondary creases
                        ax.plot([start[0], end[0]], [start[1], end[1]], 
                               color="black", linewidth=0.6, linestyle=(0, (3, 1)))
                
                elif fold type == 'tessellation':
                    # Dotted lines for tessellation pattern
                    ax.plot([start[0], end[0]], [start[1], end[1]], 
                           color="black", linewidth=0.5, linestyle=(0, (1, 1)))
    
    # Add connecting elements between modules
    # Valley and mountain fold connections
    for row in range(grid rows - 1):
        for col in range(grid cols - 1):
            cx1 = 12.5 + col * module size
            cy1 = 12.5 + row * module size
            cx2 = cx1 + module size
            cy2 = cy1 + module size
            
            if cx2 <= 95 and cy2 <= 95:
                # Connect adjacent modules with fold lines
                fold type1 = fold types[(row + col) % len(fold types)]
                fold type2 = fold types[(row + col + 1) % len(fold types)]
                
                # Horizontal connection
                if fold type1 == fold type2:
                    ax.plot([cx1 + module size/2, cx2 + module size/2], 
                           [cy1, cy1], color="black", linewidth=0.4, alpha=0.6)
                
                # Vertical connection  
                ax.plot([cx1, cx1], [cy1 + module size/2, cy2 + module size/2], 
                       color="black", linewidth=0.4, alpha=0.6)
    
    # Add corner reinforcement patterns
    corner positions = [(18, 18), (82, 18), (18, 82), (82, 82), (50, 50)]
    
    for corner x, corner y in corner positions:
        # Small decorative fold pattern at corners
        corner size = 4
        corner angles = [0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi]
        
        for i in range(len(corner angles) - 1):
            start angle = corner angles[i]
            end angle = corner angles[i + 1]
            
            # Radial crease
            ax.plot([corner x, corner x + corner size * np.cos(start angle)], 
                   [corner y, corner y + corner size * np.sin(start angle)],
                   color="black", linewidth=0.6, alpha=0.8)
            
            # Arc between radial creases
            arc angles = np.linspace(start angle, end angle, 8)
            arc x = [corner x + corner size * 0.7 * np.cos(a) for a in arc angles]
            arc y = [corner y + corner size * 0.7 * np.sin(a) for a in arc angles]
            
            ax.plot(arc x, arc y, color="black", linewidth=0.4, alpha=0.6)
    
    save(fig, "abstract geometric modular origami crease fold pattern black white texture"))


if   name   == "  main  ":
    modular origami crease fold()