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
    fig, ax = plt.subplots(figsize=(SIZE / DPI, SIZE / DPI), dpi=DPI)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.set_facecolor("white")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
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

def generate():
    """Generates a Bridget Riley style wavy phase shift pattern."""
    fig, ax = setup_ax()
    
    n_lines = 150
    x = np.linspace(0, 10, 1000)
    
    for i in range(n_lines):
        y0 = (i / n_lines) * 10
        
        # Base wave
        wave = 0.5 * np.sin(2 * np.pi * (x / 3))
        
        # Phase shift based on x position to create folding illusion
        phase = np.sin(np.pi * x / 5) * 1.5
        y_wave = y0 + 0.15 * np.sin(2 * np.pi * (x / 2) + phase)
        
        ax.plot(x, y_wave, color="black", linewidth=1.5)

    save(fig, "abstract opart wavy phase shift lines Bridget pattern black white texture")

if __name__ == "__main__":
    generate()
