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
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
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


def abstract_parallel_lines_sine_wave_rounded_rect_fusion_pattern_black_white_texture():
    """Wild Combination: Parallel sine waves passing through a rounded rectangle lens that magnifies wave frequency."""
    fig, ax = setup_ax()
    
    n_lines = 60
    y_starts = np.linspace(5, 95, n_lines)
    x_vals = np.linspace(0, 100, 600)
    
    # Rounded rect lens region (centered at 50, 50, width 50, height 50)
    cx, cy = 50, 50
    rw, rh = 25, 25
    r_corner = 8.0
    
    for y0 in y_starts:
        y_vals = []
        for x in x_vals:
            # Distance metric for rounded rectangle
            dx = max(0, abs(x - cx) - (rw - r_corner))
            dy = max(0, abs(y0 - cy) - (rh - r_corner))
            dist = np.sqrt(dx**2 + dy**2)
            
            is_inside = (abs(x - cx) <= rw and abs(y0 - cy) <= rh) and (dist <= r_corner or (dx == 0 or dy == 0))
            
            if is_inside:
                # Inside the rounded rect lens: higher frequency & larger amplitude sine wave
                amp = 3.0
                freq = 0.4
            else:
                # Outside: gentle wave
                amp = 1.0
                freq = 0.1
                
            y = y0 + amp * np.sin(freq * x)
            y_vals.append(y)
            
        ax.plot(x_vals, y_vals, color="black", linewidth=1.0)
        
    save(fig, "abstract parallel lines sine wave rounded rect fusion pattern black white texture")


if __name__ == "__main__":
    abstract_parallel_lines_sine_wave_rounded_rect_fusion_pattern_black_white_texture()
