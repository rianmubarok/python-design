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


def nested pentagon starburst():
    """
    Geometric nested pentagons with starburst lines radiating from vertices.
    Each layer has progressively larger pentagons with rotation offset.
    """
    fig, ax = setup ax()
    
    cx, cy = 50, 50
    n layers = 15
    
    for i in range(n layers):
        radius = 3 + i * 2.8
        rotation = i * 12  # Progressive rotation
        
        # Pentagon vertices
        angles = np.array([2 * np.pi * k / 5 + np.radians(rotation) for k in range(6)])  # 6 to close
        
        x points = cx + radius * np.cos(angles)
        y points = cy + radius * np.sin(angles)
        
        # Draw pentagon
        lw = 0.8 + 1.5 * (i / n layers)
        ax.plot(x points, y points, color="black", linewidth=lw, solid capstyle="round")
        
        # Draw starburst lines from vertices (every 3rd layer)
        if i % 3 == 0 and i > 0:
            for j in range(5):  # 5 vertices
                start x = x points[j]
                start y = y points[j]
                
                # Radiate outward from vertex
                line length = radius * 0.4
                end x = start x + line length * np.cos(angles[j])
                end y = start y + line length * np.sin(angles[j])
                
                ax.plot([start x, end x], [start y, end y], 
                       color="black", linewidth=0.6, alpha=0.7)
    
    save(fig, "nested pentagon starburst")


if   name   == "  main  ":
    nested pentagon starburst()