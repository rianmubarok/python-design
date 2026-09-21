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


def abstract_dynamic_strange_attractor_mobius_fusion_pattern_black_white_texture():
    """Wild Combination: Fusion of Lorenz chaotic strange attractor trajectories projected on a twisting Möbius surface!"""
    fig, ax = setup_ax()
    
    # Lorenz attractor integration
    dt = 0.01
    n_steps = 10000
    xs, ys, zs = np.empty(n_steps), np.empty(n_steps), np.empty(n_steps)
    xs[0], ys[0], zs[0] = (0.1, 0.0, 0.0)
    
    s, r_param, b = 10.0, 28.0, 8/3
    
    for i in range(n_steps - 1):
        xs[i + 1] = xs[i] + s * (ys[i] - xs[i]) * dt
        ys[i + 1] = ys[i] + (xs[i] * (r_param - zs[i]) - ys[i]) * dt
        zs[i + 1] = zs[i] + (xs[i] * ys[i] - b * zs[i]) * dt
        
    # Normalize Lorenz coordinates to [-1, 1]
    norm_x = (xs - np.min(xs)) / (np.max(xs) - np.min(xs)) * 2 - 1
    norm_y = (ys - np.min(ys)) / (np.max(ys) - np.min(ys)) * 2 - 1
    
    # Map onto Mobius surface projection
    u = norm_x * np.pi
    v = norm_y
    
    proj_x = (1 + (v/2) * np.cos(u/2)) * np.cos(u)
    proj_y = (1 + (v/2) * np.cos(u/2)) * np.sin(u)
    
    ax.plot(proj_x, proj_y, color="black", linewidth=0.5, alpha=0.6)

    save(fig, "abstract dynamic strange attractor mobius fusion pattern black white texture")


if __name__ == "__main__":
    abstract_dynamic_strange_attractor_mobius_fusion_pattern_black_white_texture()
