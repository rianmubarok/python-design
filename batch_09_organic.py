import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# ============================================================
# BATCH 09 — ORGANIC & FLOW
# Pola organik dan aliran
# Setting: 4000x4000 px, 300 DPI, 1:1
# Output: PNG + SVG
# ============================================================

SIZE = 4000
DPI = 300
SEED = 42
BATCH = "batch_09_organic"

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
# 1. FLOW FIELD — Garis mengikuti vektor field
# ============================================================
def flow_field():
    fig, ax = setup_ax()

    def angle_field(x, y):
        return np.sin(x * 0.1) * np.cos(y * 0.1) * np.pi

    for start_x in np.arange(-5, 105, 5):
        for start_y in np.arange(-5, 105, 5):
            x, y = start_x, start_y
            xs, ys = [x], [y]
            for _ in range(100):
                angle = angle_field(x, y)
                x += 0.5 * np.cos(angle)
                y += 0.5 * np.sin(angle)
                if x < -10 or x > 110 or y < -10 or y > 110:
                    break
                xs.append(x)
                ys.append(y)
            if len(xs) > 5:
                lw = 0.8 + 0.5 * np.sin(start_x * 0.2)
                ax.plot(xs, ys, color="black", linewidth=lw, alpha=0.7)

    save(fig, "flow_field_lines_pattern_organic_abstract")


# ============================================================
# 2. FRACTAL TREE — Pohon fraktal
# ============================================================
def fractal_tree():
    fig, ax = setup_ax()

    def draw_branch(x, y, angle, length, depth, lw):
        if depth == 0 or length < 1:
            return
        x2 = x + length * np.cos(np.radians(angle))
        y2 = y + length * np.sin(np.radians(angle))
        ax.plot([x, x2], [y, y2], color="black", linewidth=lw)
        draw_branch(x2, y2, angle - 25, length * 0.7, depth - 1, lw * 0.8)
        draw_branch(x2, y2, angle + 25, length * 0.7, depth - 1, lw * 0.8)

    draw_branch(50, 5, 90, 25, 8, 3.0)
    save(fig, "fractal_tree_branches_pattern_abstract_organic")


# ============================================================
# RUN
# ============================================================
if __name__ == "__main__":
    print("=== BATCH 09: ORGANIC & FLOW ===")
    flow_field()
    fractal_tree()
    print("Selesai!")
