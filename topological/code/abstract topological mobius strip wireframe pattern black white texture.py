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
    ax.set_xlim(-2.2, 2.2)
    ax.set_ylim(-2.2, 2.2)
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


def abstract_topological_mobius_strip_wireframe_pattern_black_white_texture():
    """Generates a 3D Mobius Strip wireframe projected onto 2D."""
    fig, ax = setup_ax()
    
    u = np.linspace(0, 2 * np.pi, 200)
    v = np.linspace(-1, 1, 20)
    
    # Plot the wireframe lines along 'u' (around the loop)
    for v_val in v:
        # Mobius strip parametric equations
        x = (1 + (v_val/2) * np.cos(u/2)) * np.cos(u)
        y = (1 + (v_val/2) * np.cos(u/2)) * np.sin(u)
        z = (v_val/2) * np.sin(u/2)
        
        # Simple orthographic projection with a slight isometric angle
        proj_x = x * np.cos(np.pi/6) - y * np.cos(np.pi/6)
        proj_y = x * np.sin(np.pi/6) + y * np.sin(np.pi/6) + z
        
        ax.plot(proj_x, proj_y, color="black", linewidth=1.2, alpha=0.8)

    # Plot the wireframe lines along 'v' (across the strip)
    u_cross = np.linspace(0, 2 * np.pi, 60)
    for u_val in u_cross:
        x = (1 + (v/2) * np.cos(u_val/2)) * np.cos(u_val)
        y = (1 + (v/2) * np.cos(u_val/2)) * np.sin(u_val)
        z = (v/2) * np.sin(u_val/2)
        
        proj_x = x * np.cos(np.pi/6) - y * np.cos(np.pi/6)
        proj_y = x * np.sin(np.pi/6) + y * np.sin(np.pi/6) + z
        
        ax.plot(proj_x, proj_y, color="black", linewidth=0.6, alpha=0.5)
        
    save(fig, "abstract topological mobius strip wireframe pattern black white texture")


if __name__ == "__main__":
    abstract_topological_mobius_strip_wireframe_pattern_black_white_texture()
