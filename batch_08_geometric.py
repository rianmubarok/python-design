import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# ============================================================
# BATCH 08 — GEOMETRIC SHAPES
# Pola bentuk geometris
# Setting: 4000x4000 px, 300 DPI, 1:1
# Output: PNG + SVG
# ============================================================

SIZE = 4000
DPI = 300
SEED = 42
BATCH = "batch_08_geometric"

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
# 1. NESTED ROTATING SQUARES — Persegi bersarang berputar
# ============================================================
def nested_rotating_squares():
    fig, ax = setup_ax()

    cx, cy = 50, 50
    n_squares = 30
    for i in range(n_squares):
        size = 2 + i * 2.5
        angle = i * 5
        rad = np.radians(angle)
        corners = [(-1, -1), (1, -1), (1, 1), (-1, 1)]
        xs = []
        ys = []
        for dx, dy in corners:
            rx = dx * size * np.cos(rad) - dy * size * np.sin(rad)
            ry = dx * size * np.sin(rad) + dy * size * np.cos(rad)
            xs.append(cx + rx)
            ys.append(cy + ry)
        xs.append(xs[0])
        ys.append(ys[0])
        lw = 1.0 + 2.0 * (i / n_squares)
        ax.plot(xs, ys, color="black", linewidth=lw)

    save(fig, "nested_rotating_squares_pattern_abstract_geometric")


# ============================================================
# 2. HERRINGBONE — Pola V berulang
# ============================================================
def herringbone():
    fig, ax = setup_ax()

    spacing = 4
    amp = 3
    for y in np.arange(-5, 105, spacing):
        for x in np.arange(-5, 105, spacing * 2):
            ax.plot([x, x + spacing], [y, y + amp], color="black", linewidth=1.2)
            ax.plot([x + spacing, x + spacing * 2], [y + amp, y], color="black", linewidth=1.2)

    save(fig, "herringbone_v_pattern_abstract_geometric_texture")


# ============================================================
# 3. LABYRINTH — Pola labirin
# ============================================================
def labyrinth():
    fig, ax = setup_ax()

    cell_size = 5
    rows = 20
    cols = 20
    np.random.seed(SEED)

    for r in range(rows):
        for c in range(cols):
            x = c * cell_size
            y = r * cell_size
            if np.random.random() > 0.5:
                ax.plot([x, x + cell_size], [y, y], color="black", linewidth=1.2)
            if np.random.random() > 0.5:
                ax.plot([x, x], [y, y + cell_size], color="black", linewidth=1.2)
            if np.random.random() > 0.3:
                ax.plot([x + cell_size, x + cell_size], [y, y + cell_size], color="black", linewidth=1.2)
            if np.random.random() > 0.3:
                ax.plot([x, x + cell_size], [y + cell_size, y + cell_size], color="black", linewidth=1.2)

    save(fig, "labyrinth_maze_pattern_abstract_geometric")


# ============================================================
# 4. TESSELLATION — Tessellation segitiga
# ============================================================
def tessellation():
    fig, ax = setup_ax()

    size = 8
    h = size * np.sqrt(3) / 2

    for row in range(-1, 15):
        for col in range(-1, 15):
            x = col * size + (row % 2) * size / 2
            y = row * h
            if (row + col) % 2 == 0:
                triangle = [(x, y), (x + size, y), (x + size / 2, y + h)]
            else:
                triangle = [(x, y + h), (x + size, y + h), (x + size / 2, y)]
            xs = [p[0] for p in triangle] + [triangle[0][0]]
            ys = [p[1] for p in triangle] + [triangle[0][1]]
            ax.plot(xs, ys, color="black", linewidth=0.8)

    save(fig, "tessellation_triangle_pattern_geometric_abstract")


# ============================================================
# RUN
# ============================================================
if __name__ == "__main__":
    print("=== BATCH 08: GEOMETRIC SHAPES ===")
    nested_rotating_squares()
    herringbone()
    labyrinth()
    tessellation()
    print("Selesai!")
