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
    ax.set xlim(0, 100)
    ax.set ylim(0, 100)
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


def draw star 8(cx, cy, outer radius, inner radius):
    """Draw an 8-pointed star (khatam)"""
    angles = []
    radii = []
    
    for i in range(16):  # 8 points × 2 (outer/inner)
        angle = i * np.pi / 8
        if i % 2 == 0:
            radius = outer radius
        else:
            radius = inner radius
        angles.append(angle)
        radii.append(radius)
    
    # Close the shape
    angles.append(angles[0])
    radii.append(radii[0])
    
    x = [cx + r * np.cos(a) for r, a in zip(radii, angles)]
    y = [cy + r * np.sin(a) for r, a in zip(radii, angles)]
    
    return x, y


def draw interlaced square(cx, cy, size, rotation=0):
    """Draw interlaced square pattern"""
    # Outer square
    angles1 = [np.pi/4 + i*np.pi/2 + rotation for i in range(5)]  # 5 to close
    x1 = [cx + size * np.cos(a) for a in angles1]
    y1 = [cy + size * np.sin(a) for a in angles1]
    
    # Inner rotated square
    angles2 = [np.pi/4 + i*np.pi/2 + rotation + np.pi/4 for i in range(5)]
    x2 = [cx + size * 0.7 * np.cos(a) for a in angles2]
    y2 = [cy + size * 0.7 * np.sin(a) for a in angles2]
    
    return (x1, y1), (x2, y2)


def arabesque islamic geometric():
    """
    Arabesque Islamic geometric pattern.
    Traditional Islamic geometric motifs with interlacing stars and polygons.
    """
    fig, ax = setup ax()
    
    # Grid parameters for seamless tiling
    grid size = 16
    cell size = 100 / 6  # Divide canvas into 6×6 grid
    
    # Main pattern: 8-pointed stars with interlacing squares
    for row in range(-1, 8):
        for col in range(-1, 8):
            cx = col * cell size + cell size/2
            cy = row * cell size + cell size/2
            
            # Skip if outside extended canvas
            if cx < -10 or cx > 110 or cy < -10 or cy > 110:
                continue
            
            # Draw 8-pointed star
            star outer = cell size * 0.3
            star inner = star outer * 0.4
            
            x star, y star = draw star 8(cx, cy, star outer, star inner)
            ax.plot(x star, y star, color="black", linewidth=1.5, solid capstyle="round")
            
            # Draw interlaced squares around star
            square size = cell size * 0.25
            rotation offset = (row + col) * np.pi / 8
            
            (x1, y1), (x2, y2) = draw interlaced square(cx, cy, square size, rotation offset)
            
            ax.plot(x1, y1, color="black", linewidth=1.2, solid capstyle="round")
            ax.plot(x2, y2, color="black", linewidth=1.0, solid capstyle="round")
    
    # Secondary pattern: connecting geometric elements
    # Rhombuses at intersection points
    for row in range(-1, 7):
        for col in range(-1, 7):
            # Intersection points between main grid
            int x = (col + 0.5) * cell size + cell size/2
            int y = (row + 0.5) * cell size + cell size/2
            
            if int x < -5 or int x > 105 or int y < -5 or int y > 105:
                continue
            
            # Draw small rhombus
            rhomb size = cell size * 0.15
            rhomb angles = [0, np.pi/2, np.pi, 3*np.pi/2, 0]  # Diamond orientation
            
            x rhomb = [int x + rhomb size * np.cos(a) for a in rhomb angles]
            y rhomb = [int y + rhomb size * np.sin(a) for a in rhomb angles]
            
            ax.plot(x rhomb, y rhomb, color="black", linewidth=0.8, solid capstyle="round")
    
    # Tertiary pattern: connecting lines and arabesques
    # Curved connecting elements
    for row in range(6):
        for col in range(6):
            cx = col * cell size + cell size/2
            cy = row * cell size + cell size/2
            
            # Draw connecting arcs to adjacent cells
            if col < 5:  # Right connection
                arc start x = cx + cell size * 0.3
                arc end x = cx + cell size * 0.7
                arc y = cy
                
                # Create curved connection
                n points = 10
                arc x = np.linspace(arc start x, arc end x, n points)
                arc curve y = arc y + cell size * 0.1 * np.sin(np.pi * np.linspace(0, 1, n points))
                
                ax.plot(arc x, arc curve y, color="black", linewidth=0.6, alpha=0.7)
            
            if row < 5:  # Down connection
                arc start y = cy + cell size * 0.3
                arc end y = cy + cell size * 0.7
                arc x = cx
                
                # Create curved connection
                n points = 10
                arc y = np.linspace(arc start y, arc end y, n points)
                arc curve x = arc x + cell size * 0.1 * np.sin(np.pi * np.linspace(0, 1, n points))
                
                ax.plot(arc curve x, arc y, color="black", linewidth=0.6, alpha=0.7)
    
    # Border decorative elements
    border elements = [
        # Corner stars
        (cell size * 0.5, cell size * 0.5),
        (100 - cell size * 0.5, cell size * 0.5),
        (cell size * 0.5, 100 - cell size * 0.5),
        (100 - cell size * 0.5, 100 - cell size * 0.5)
    ]
    
    for bx, by in border elements:
        # Small decorative 6-pointed stars
        star 6 outer = cell size * 0.2
        star 6 inner = star 6 outer * 0.5
        
        angles 6 = []
        radii 6 = []
        
        for i in range(12):  # 6 points × 2
            angle = i * np.pi / 6
            if i % 2 == 0:
                radius = star 6 outer
            else:
                radius = star 6 inner
            angles 6.append(angle)
            radii 6.append(radius)
        
        angles 6.append(angles 6[0])
        radii 6.append(radii 6[0])
        
        x 6 = [bx + r * np.cos(a) for r, a in zip(radii 6, angles 6)]
        y 6 = [by + r * np.sin(a) for r, a in zip(radii 6, angles 6)]
        
        ax.plot(x 6, y 6, color="black", linewidth=1.0, solid capstyle="round", alpha=0.8)
    
    save(fig, "arabesque islamic geometric")


if   name   == "  main  ":
    arabesque islamic geometric()