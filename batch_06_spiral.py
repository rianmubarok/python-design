import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# ============================================================
# BATCH 06 — SPIRAL
# Pola spiral
# Setting: 4000x4000 px, 300 DPI, 1:1
# Output: PNG + SVG
# ============================================================

SIZE = 4000
DPI = 300
SEED = 42
BATCH = "batch_06_spiral"

PNG_DIR = Path(f"output/{BATCH}/png")
SVG_DIR = Path(f"output/{BATCH}/svg")
PNG_DIR.mkdir(parents=True, exist_ok=True)
SVG_DIR.mkdir(parents=True, exist_ok=True)

np.random.seed(SEED)


def setup_ax():
    fig, ax = plt.subplots(figsize=(SIZE/DPI, SIZE/DPI), dpi=DPI)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.set_facecolor("white")
    ax.set_xlim(-5, 105)
    ax.set_ylim(-5, 105)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def save(fig, name):
    png_path = PNG_DIR / f"{name}.png"
    svg_path = SVG_DIR / f"{name}.svg"
    fig.savefig(png_path, dpi=DPI, pad_inches=0, facecolor="white")
    fig.savefig(svg_path, format="svg", pad_inches=0, facecolor="white")
    plt.close(fig)
    print(f"Tersimpan: {png_path} | {svg_path}")


# ============================================================
# 1. SPIRAL — Spiral tunggal dengan gradiasi ketebalan
# ============================================================
def spiral():
    fig, ax = setup_ax()

    cx, cy = 50, 50
    theta = np.linspace(0, 12 * np.pi, 1000)
    r = 1 + theta * 1.5
    x = cx + r * np.cos(theta)
    y = cy + r * np.sin(theta)

    for i in range(len(x) - 1):
        dist = np.sqrt((x[i] - cx)**2 + (y[i] - cy)**2)
        lw = 1.0 + 3.0 * (1 - dist / 80)
        lw = max(0.5, min(lw, 4.0))
        ax.plot([x[i], x[i+1]], [y[i], y[i+1]], color="black", linewidth=lw)

    ax.plot(cx, cy, "o", color="black", markersize=15)
    save(fig, "spiral_lines_pattern_abstract_geometric_design")


# ============================================================
# 2. DOUBLE SPIRAL — Dua spiral berlawanan arah
# ============================================================
def double_spiral():
    fig, ax = setup_ax()

    cx, cy = 50, 50
    theta = np.linspace(0, 10 * np.pi, 800)

    r1 = 1 + theta * 1.5
    x1 = cx + r1 * np.cos(theta)
    y1 = cy + r1 * np.sin(theta)
    r2 = 1 + theta * 1.5
    x2 = cx + r2 * np.cos(theta + np.pi)
    y2 = cy + r2 * np.sin(theta + np.pi)

    for i in range(len(x1) - 1):
        dist = np.sqrt((x1[i] - cx)**2 + (y1[i] - cy)**2)
        lw = 1.0 + 2.5 * (1 - dist / 80)
        lw = max(0.5, min(lw, 3.5))
        ax.plot([x1[i], x1[i+1]], [y1[i], y1[i+1]], color="black", linewidth=lw)
        ax.plot([x2[i], x2[i+1]], [y2[i], y2[i+1]], color="black", linewidth=lw)

    ax.plot(cx, cy, "o", color="black", markersize=12)
    save(fig, "double_spiral_lines_pattern_symmetric_abstract")


# ============================================================
# RUN
# ============================================================
if __name__ == "__main__":
    print("=== BATCH 06: SPIRAL ===")
    spiral()
    double_spiral()
    print("Selesai!")
