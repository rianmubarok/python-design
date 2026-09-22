import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, FancyBboxPatch
from pathlib import Path
from datetime import datetime

SIZE = 4000
DPI = 300
PERIOD = 100.0
DATE = datetime.now().strftime("%d%m%Y")
WRAPS = [(i * PERIOD, j * PERIOD) for i in (-1, 0, 1) for j in (-1, 0, 1)]

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR.parent / "output"
JPG_DIR = OUTPUT_DIR / "jpg"
SVG_DIR = OUTPUT_DIR / "svg"
JPG_DIR.mkdir(parents=True, exist_ok=True)
SVG_DIR.mkdir(parents=True, exist_ok=True)


def setup_ax():
    fig, ax = plt.subplots(figsize=(SIZE / DPI, SIZE / DPI), dpi=DPI)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.set_facecolor("black")
    ax.set_xlim(0, PERIOD)
    ax.set_ylim(0, PERIOD)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def save(fig, name):
    jpg_path = JPG_DIR / f"{name} {DATE}.jpg"
    svg_path = SVG_DIR / f"{name} {DATE}.svg"
    fig.savefig(jpg_path, dpi=DPI, pad_inches=0, facecolor="black")
    fig.savefig(svg_path, format="svg", pad_inches=0, facecolor="black")
    plt.close(fig)
    print(f"Saved: {jpg_path} | {svg_path}")


def potion_bottle(ax, cx, cy, s, fill="white"):
    """Botol ramuan bundar dengan batas leher dan simbol tengkorak yang diperjelas."""
    inv = "black" if fill == "white" else "white"
    body_r = s * 0.34
    
    # Badan botol
    ax.add_patch(Circle((cx, cy - s * 0.08), body_r, facecolor=fill, edgecolor="none"))
    
    # Leher botol (diberi stroke tipis agar terpisah visual dari badan)
    ax.add_patch(FancyBboxPatch(
        (cx - s * 0.08, cy + s * 0.22), s * 0.16, s * 0.22,
        boxstyle="square,pad=0",
        facecolor=fill, edgecolor=inv, linewidth=1.0))
        
    # Bibir/Gabus botol
    ax.add_patch(FancyBboxPatch(
        (cx - s * 0.10, cy + s * 0.42), s * 0.20, s * 0.08,
        boxstyle=f"round,pad=0,rounding_size={s*0.02:.4f}",
        facecolor=fill, edgecolor=inv, linewidth=1.0))
        
    # Label persegi di badan botol
    ax.add_patch(FancyBboxPatch(
        (cx - s * 0.16, cy - s * 0.20), s * 0.32, s * 0.20,
        boxstyle=f"round,pad=0,rounding_size={s*0.02:.4f}",
        facecolor=inv, edgecolor="none"))
        
    # Simbol tengkorak pada label
    skull_r = s * 0.045
    # Kepala
    ax.add_patch(Circle((cx, cy - s * 0.08), skull_r, facecolor=fill, edgecolor="none"))
    # Rahang
    ax.add_patch(FancyBboxPatch(
        (cx - skull_r * 0.55, cy - s * 0.14), skull_r * 1.1, skull_r * 0.8,
        boxstyle="square,pad=0", facecolor=fill, edgecolor="none"))
    # Mata (Dua titik hitam)
    ax.add_patch(Circle((cx - skull_r * 0.4, cy - s * 0.08), skull_r * 0.3, facecolor=inv, edgecolor="none"))
    ax.add_patch(Circle((cx + skull_r * 0.4, cy - s * 0.08), skull_r * 0.3, facecolor=inv, edgecolor="none"))

    # Gelembung dalam cairan
    for (bx, by, br) in [(-0.12, -0.01, 0.035), (0.10, 0.06, 0.03), (-0.04, 0.10, 0.025)]:
        ax.add_patch(Circle((cx + bx * s, cy + by * s), br * s,
                            facecolor="none", edgecolor=inv, linewidth=0.8))


def potion_with_aura(ax, cx, cy, s, n_rings=5):
    """Botol ramuan dikelilingi lingkaran aura gelembung konsentris yang kontras."""
    body_r = s * 0.34
    for i in range(n_rings, 0, -1):
        r = body_r + i * s * 0.11
        alpha = 0.85 - i * 0.10
        
        # Garis lingkaran aura lebih tebal dan jelas
        ax.add_patch(Circle((cx, cy - s * 0.08), r,
                            facecolor="none", edgecolor="white",
                            linewidth=1.0, alpha=max(alpha, 0.2)))
                            
        # Titik-titik gelembung pada aura
        n_dots = 6 + i * 2
        for k in range(n_dots):
            ang = k * 2 * np.pi / n_dots + i * 0.4
            bx = cx + r * np.cos(ang)
            by = cy - s * 0.08 + r * np.sin(ang)
            dot_r = s * 0.016
            ax.add_patch(Circle((bx, by), dot_r,
                                facecolor="white", edgecolor="none",
                                alpha=max(alpha, 0.2)))
                                
    potion_bottle(ax, cx, cy, s, fill="white")


def draw():
    """Pola grid 4x3 botol ramuan dengan aura konsentris."""
    fig, ax = setup_ax()
    cols, rows = 4, 3
    dx, dy = PERIOD / cols, PERIOD / rows
    s = min(dx, dy) * 0.50

    for row in range(rows):
        for col in range(cols):
            cx = (col + 0.5) * dx + (dx * 0.5 if row % 2 else 0)
            cy = (row + 0.5) * dy
            for ox, oy in WRAPS:
                potion_with_aura(ax, cx + ox, cy + oy, s, n_rings=5)

    save(fig, "abstract halloween variation potion bottle bubble aura concentric rings pattern black white texture")


if __name__ == "__main__":
    draw()