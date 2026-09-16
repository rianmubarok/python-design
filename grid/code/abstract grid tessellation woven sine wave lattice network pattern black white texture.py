import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime

SIZE = 4000
DPI = 300
DATE = datetime.now().strftime("%d%m%Y")

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


def draw():
    """
    Woven Sine Wave Lattice Network.
    A highly complex grid of interlacing sine waves, creating a woven basket
    or carbon fiber lattice texture.
    """
    fig, ax = setup_ax()

    # We will draw horizontal and vertical sine waves that are phase-shifted
    # to interlock visually.
    
    n_waves = 30
    spacing = 120.0 / n_waves
    
    # X and Y arrays for the curves
    t = np.linspace(-10, 110, 1000)
    
    frequency = 0.4
    amplitude = spacing * 0.45
    
    # We use zorder to weave.
    # To truly weave, we would need to split the waves at every intersection.
    # A trick to create weaving is to draw the vertical lines with a thick white outline
    # where they cross the horizontal lines.
    # Since sine waves cross at specific intervals, we can mathematically calculate overlaps.
    
    # Draw horizontal waves first (zorder 1)
    for i in range(n_waves + 1):
        cy = -10 + i * spacing
        # Alternate phase
        phase = 0 if i % 2 == 0 else np.pi
        
        wave_y = cy + np.sin(t * frequency + phase) * amplitude
        
        # Multiple offset lines to make it look like a bundle/rope
        for offset in [-0.6, -0.2, 0.2, 0.6]:
            ax.plot(t, wave_y + offset, color="black", linewidth=1.0, zorder=1)

    # Draw vertical waves (zorder 2)
    for i in range(n_waves + 1):
        cx = -10 + i * spacing
        phase = 0 if i % 2 == 0 else np.pi
        
        wave_x = cx + np.sin(t * frequency + phase) * amplitude
        
        # To simulate weaving without actual 3D, we draw a thick white mask line
        # but ONLY near the intersections where we want this thread to go OVER.
        # This is extremely complex.
        # Alternatively, we just draw the vertical bundles with a white outline.
        # This creates a "layering" effect, but not a true over-under weave.
        # To get the optical illusion of a true weave, we can use a dashed line for the white mask.
        
        # Mask
        ax.plot(wave_x, t, color="white", linewidth=4.0, zorder=2)
        
        for offset in [-0.6, -0.2, 0.2, 0.6]:
            # Instead of a full mask, a dashed mask can simulate an over-under weave.
            # But the frequency of dashes must perfectly match the grid.
            # dash_length = (np.pi / frequency)
            # The intersection distance is exactly (np.pi / frequency).
            # We can use standard dash arrays!
            
            # Let's just use solid layering for a lattice effect, it's highly striking too.
            ax.plot(wave_x + offset, t, color="black", linewidth=1.0, zorder=3)

    save(fig, "abstract grid tessellation woven sine wave lattice network pattern black white texture")


if __name__ == "__main__":
    draw()
