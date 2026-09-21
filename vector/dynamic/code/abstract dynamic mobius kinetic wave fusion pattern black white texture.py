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
    ax.set_xlim(-2.5, 2.5)
    ax.set_ylim(-2.5, 2.5)
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


def abstract_dynamic_mobius_kinetic_wave_fusion_pattern_black_white_texture():
    """Wild Combination: Fusion of Möbius strip parametric twists with dynamic kinetic wave ripple oscillations."""
    fig, ax = setup_ax()
    
    u = np.linspace(0, 2 * np.pi, 250)
    v = np.linspace(-1, 1, 24)
    
    for v_val in v:
        # Dynamic kinetic wave modulation
        wave = 0.2 * np.sin(6 * u)
        
        x = (1 + (v_val/2 + wave) * np.cos(u/2)) * np.cos(u)
        y = (1 + (v_val/2 + wave) * np.cos(u/2)) * np.sin(u)
        z = (v_val/2 + wave) * np.sin(u/2)
        
        proj_x = x * np.cos(np.pi/6) - y * np.cos(np.pi/6)
        proj_y = x * np.sin(np.pi/6) + y * np.sin(np.pi/6) + z
        
        ax.plot(proj_x, proj_y, color="black", linewidth=0.9, alpha=0.85)

    save(fig, "abstract dynamic mobius kinetic wave fusion pattern black white texture")


if __name__ == "__main__":
    abstract_dynamic_mobius_kinetic_wave_fusion_pattern_black_white_texture()
