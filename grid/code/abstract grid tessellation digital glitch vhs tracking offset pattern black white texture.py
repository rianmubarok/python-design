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
    Digital Glitch VHS Tracking Offset.
    A rigid square grid that gets violently torn horizontally and vertically
    as if experiencing digital databending or VHS tracking errors.
    """
    fig, ax = setup_ax()
    rng = np.random.default_rng(42)

    n_lines = 50
    spacing = 120.0 / n_lines
    
    # Generate glitch bands (horizontal slices that are shifted left/right)
    n_h_glitches = 15
    h_bands = rng.uniform(-10, 110, n_h_glitches)
    h_widths = rng.uniform(1.0, 8.0, n_h_glitches)
    h_shifts = rng.uniform(-15.0, 15.0, n_h_glitches)
    
    # Generate glitch bands (vertical slices that are shifted up/down)
    n_v_glitches = 10
    v_bands = rng.uniform(-10, 110, n_v_glitches)
    v_widths = rng.uniform(1.0, 6.0, n_v_glitches)
    v_shifts = rng.uniform(-15.0, 15.0, n_v_glitches)

    def apply_glitch(x, y):
        x_out = np.copy(x)
        y_out = np.copy(y)
        
        # Apply horizontal shifts
        for band, width, shift in zip(h_bands, h_widths, h_shifts):
            mask = (y >= band) & (y <= band + width)
            x_out[mask] += shift
            
        # Apply vertical shifts
        for band, width, shift in zip(v_bands, v_widths, v_shifts):
            mask = (x_out >= band) & (x_out <= band + width)
            y_out[mask] += shift
            
        return x_out, y_out

    # Draw vertical lines
    for i in range(n_lines + 1):
        x_base = -10 + i * spacing
        y = np.linspace(-10, 110, 800)
        x = np.full_like(y, x_base)
        
        gx, gy = apply_glitch(x, y)
        
        # Insert NaNs at huge jumps to prevent drawing long connecting lines across glitches
        diffs = np.abs(np.diff(gx)) + np.abs(np.diff(gy))
        jump_indices = np.where(diffs > 2.0)[0] + 1
        
        gx = np.insert(gx, jump_indices, np.nan)
        gy = np.insert(gy, jump_indices, np.nan)
        
        lw = rng.choice([0.5, 1.0, 1.5, 2.0])
        ax.plot(gx, gy, color="black", linewidth=lw, solid_capstyle="butt")
        
    # Draw horizontal lines
    for i in range(n_lines + 1):
        y_base = -10 + i * spacing
        x = np.linspace(-10, 110, 800)
        y = np.full_like(x, y_base)
        
        gx, gy = apply_glitch(x, y)
        
        diffs = np.abs(np.diff(gx)) + np.abs(np.diff(gy))
        jump_indices = np.where(diffs > 2.0)[0] + 1
        
        gx = np.insert(gx, jump_indices, np.nan)
        gy = np.insert(gy, jump_indices, np.nan)
        
        lw = rng.choice([0.5, 1.0, 1.5, 2.0])
        ax.plot(gx, gy, color="black", linewidth=lw, solid_capstyle="butt")

    save(fig, "abstract grid tessellation digital glitch vhs tracking offset pattern black white texture")


if __name__ == "__main__":
    draw()
