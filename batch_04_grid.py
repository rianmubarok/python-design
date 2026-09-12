import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# ============================================================
# BATCH 04 — GRID & CROSSING
# Pola grid dan garis berpotongan
# Setting: 4000x4000 px, 300 DPI, 1:1
# Output: PNG + SVG
# ============================================================

SIZE = 4000
DPI = 300
SEED = 42
BATCH = "batch_04_grid"

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
# 1. CROSSING DIAGONAL — Grid diagonal berpotongan
# ============================================================
def crossing_diagonal():
    fig, ax = setup_ax()

    spacing = 8
    for offset in np.arange(-150, 250, spacing):
        lw = np.random.choice([1.5, 2.0, 3.0])
        ax.plot([offset, offset + 150], [-50, 150], color="black", linewidth=lw)
        ax.plot([offset, offset + 150], [150, -50], color="black", linewidth=lw * 0.7)

    save(fig, "crossing_diagonal_lines_pattern_geometric_texture")


# ============================================================
# 2. DIAMOND GRID — Grid diagonal berlian
# ============================================================
def diamond_grid():
    fig, ax = setup_ax()

    spacing = 6
    for offset in np.arange(-150, 250, spacing):
        lw = 0.8
        ax.plot([offset, offset + 150], [-50, 150], color="black", linewidth=lw)
        ax.plot([offset, offset + 150], [150, -50], color="black", linewidth=lw)

    cx, cy = 50, 50
    for r in np.arange(5, 80, 8):
        theta = np.linspace(0, 2 * np.pi, 5)
        x = cx + r * np.cos(theta)
        y = cy + r * np.sin(theta)
        ax.plot(x, y, color="black", linewidth=1.5)

    save(fig, "diamond_grid_lines_pattern_geometric_abstract")


# ============================================================
# 3. HEXAGONAL GRID — Grid heksagonal
# ============================================================
def hexagonal_grid():
    fig, ax = setup_ax()

    size = 5
    h = size * np.sqrt(3)
    for row in range(-2, 24):
        for col in range(-2, 22):
            x = col * size * 1.5
            y = row * h + (col % 2) * h / 2
            theta = np.linspace(0, 2 * np.pi, 7)
            hex_x = x + size * 0.9 * np.cos(theta)
            hex_y = y + size * 0.9 * np.sin(theta)
            ax.plot(hex_x, hex_y, color="black", linewidth=0.8)

    save(fig, "hexagonal_grid_pattern_geometric_abstract")


# ============================================================
# 4. WAVY GRID — Grid dengan distorsi gelombang
# ============================================================
def wavy_grid():
    fig, ax = setup_ax()

    n_lines = 20
    for i in range(n_lines):
        y_base = -5 + i * 5.5
        x = np.linspace(-5, 105, 300)
        amp = 2 * np.sin(i * 0.5)
        y = y_base + amp * np.sin(x * 0.1 + i * 0.3)
        ax.plot(x, y, color="black", linewidth=0.8)

    for i in range(n_lines):
        x_base = -5 + i * 5.5
        y = np.linspace(-5, 105, 300)
        amp = 2 * np.cos(i * 0.5)
        x = x_base + amp * np.sin(y * 0.1 + i * 0.3)
        ax.plot(x, y, color="black", linewidth=0.8)

    save(fig, "wavy_grid_distortion_pattern_abstract_seamless")


# ============================================================
# 5. SPIRAL GRID — Grid dengan distorsi spiral
# ============================================================
def spiral_grid():
    fig, ax = setup_ax()

    n_lines = 25
    cx, cy = 50, 50

    for i in range(n_lines):
        y_base = -5 + i * 4.5
        x = np.linspace(-5, 105, 400)
        dist_from_center = np.abs(x - cx) / 50
        spiral_factor = 3.0 * np.exp(-dist_from_center * 2)
        y = y_base + spiral_factor * np.sin(x * 0.2 + i * 0.5)
        ax.plot(x, y, color="black", linewidth=0.7)

    for i in range(n_lines):
        x_base = -5 + i * 4.5
        y = np.linspace(-5, 105, 400)
        dist_from_center = np.abs(y - cy) / 50
        spiral_factor = 3.0 * np.exp(-dist_from_center * 2)
        x = x_base + spiral_factor * np.cos(y * 0.2 + i * 0.5)
        ax.plot(x, y, color="black", linewidth=0.7)

    save(fig, "spiral_grid_distortion_pattern_abstract_geometric")


# ============================================================
# 6. PERSPECTIVE GRID — Grid perspektif titik hilang
# ============================================================
def perspective_grid():
    fig, ax = setup_ax()

    vx, vy = 50, 90
    n_lines_h = 15
    n_lines_v = 20

    for i in range(n_lines_h):
        y = -5 + i * 7
        ax.plot([-5, 105], [y, y], color="black", linewidth=0.8)

    for i in range(n_lines_v):
        x = -5 + i * 5.5
        ax.plot([x, vx], [-5, vy], color="black", linewidth=0.8)
        ax.plot([x, vx], [105, vy], color="black", linewidth=0.8)

    ax.plot(vx, vy, "o", color="black", markersize=10)
    save(fig, "perspective_grid_vanishing_point_abstract_depth")


# ============================================================
# 7. CROSSHATCH — Silang multi sudut
# ============================================================
def crosshatch():
    fig, ax = setup_ax()

    angles = [0, 30, 60, 90, 120, 150]
    for angle in angles:
        rad = np.radians(angle)
        cos_a = np.cos(rad)
        sin_a = np.sin(rad)
        for offset in np.arange(-150, 250, 6):
            if angle == 90:
                ax.plot([offset, offset], [-10, 110], color="black", linewidth=0.8)
            else:
                denom = sin_a if abs(sin_a) > 0.001 else 0.001
                t_vals = np.array([-10, 110])
                x_line = offset + t_vals * cos_a / denom
                y_line = t_vals
                ax.plot(x_line, y_line, color="black", linewidth=0.6, alpha=0.6)

    save(fig, "crosshatch_lines_pattern_abstract_texture_sketch")


# ============================================================
# 8. CROSSHATCH GRADIENT — Crosshatch gradiasi kepadatan
# ============================================================
def crosshatch_gradient():
    fig, ax = setup_ax()

    angles = [45, 135]
    for angle in angles:
        rad = np.radians(angle)
        cos_a = np.cos(rad)
        sin_a = np.sin(rad)
        for offset in np.arange(-150, 250, 5):
            x_line = np.array([-10, 110])
            y_line = (x_line - offset) * sin_a / cos_a if abs(cos_a) > 0.001 else np.array([offset, offset])
            if angle == 90:
                y_line = np.array([-10, 110])
                x_line = np.array([offset, offset])
            mask = (y_line >= -10) & (y_line <= 110)
            if mask.any():
                cx_mid = np.mean(x_line[mask])
                cy_mid = np.mean(y_line[mask])
                dist = np.sqrt((cx_mid - 50)**2 + (cy_mid - 50)**2)
                lw = 0.3 + 1.5 * (1 - dist / 80)
                ax.plot(x_line[mask], y_line[mask], color="black", linewidth=lw, alpha=0.7)

    save(fig, "crosshatch_gradient_density_pattern_abstract")


# ============================================================
# RUN
# ============================================================
if __name__ == "__main__":
    print("=== BATCH 04: GRID & CROSSING ===")
    crossing_diagonal()
    diamond_grid()
    hexagonal_grid()
    wavy_grid()
    spiral_grid()
    perspective_grid()
    crosshatch()
    crosshatch_gradient()
    print("Selesai!")
