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


def abstract_parallel_lines_concentric_rounded_rect_multi_lobe_clover_morph_pattern_black_white_texture():
    """Tweak: Concentric squircle-like shapes morphing into a 4-lobe clover pattern."""
    fig, ax = setup_ax()
    
    n_shapes = 36
    t_vals = np.linspace(0, 2 * np.pi, 400)
    
    for i in range(n_shapes):
        r_base = 48 - i * 1.25
        if r_base <= 2:
            break
            
        # 4-lobe clover modulation
        k = i / n_shapes
        clover_amp = 8.0 * np.sin(k * np.pi)
        
        r = r_base + clover_amp * np.cos(4 * t_vals)
        
        x = 50 + r * np.cos(t_vals)
        y = 50 + r * np.sin(t_vals)
        
        lw = 0.5 + 0.4 * (1 - i / n_shapes)
        ax.plot(x, y, color="black", linewidth=lw)

    save(fig, "abstract parallel lines concentric rounded rect multi lobe clover morph pattern black white texture")


if __name__ == "__main__":
    abstract_parallel_lines_concentric_rounded_rect_multi_lobe_clover_morph_pattern_black_white_texture()
