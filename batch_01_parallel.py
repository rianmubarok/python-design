import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# ============================================================
# BATCH 01 — PARALLEL LINES
# Garis paralel horizontal dengan variasi
# Setting: 4000x4000 px, 300 DPI, 1:1
# Output: PNG + SVG
# ============================================================

SIZE = 4000
DPI = 300
SEED = 42
BATCH = "batch_01_parallel"

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
# 1. PARALLEL RANDOM — Garis paralel acak ketebalan
# ============================================================
def parallel_random():
    fig, ax = setup_ax()

    y = -5
    while y < 105:
        lw = np.random.choice([1.5, 2.0, 3.0, 4.0, 5.0, 6.0])
        x_end = np.random.uniform(-5, 105)
        ax.plot([-5, x_end], [y, y], color="black", linewidth=lw, solid_capstyle="butt")
        y += np.random.uniform(2, 5)

    save(fig, "abstract_parallel_lines_pattern_black_white_texture")


# ============================================================
# 2. PARALLEL GRADIENT — Garis paralel gradiasi ketebalan
# ============================================================
def parallel_gradient():
    fig, ax = setup_ax()

    n_lines = 40
    for i in range(n_lines):
        y = -5 + i * 2.7
        lw = 0.5 + 5.0 * np.sin(i / n_lines * np.pi)
        ax.plot([-5, 105], [y, y], color="black", linewidth=lw)

    save(fig, "parallel_gradient_lines_pattern_abstract_thick_thin")


# ============================================================
# 3. DENSITY GRADIENT — Garis paralel kepadatan berubah
# ============================================================
def density_gradient():
    fig, ax = setup_ax()

    y = -5
    while y < 105:
        dist_from_center = abs(y - 50) / 50
        density = 0.5 + 2.0 * (1 - dist_from_center)
        n_segments = int(density * 15)

        x_segments = np.linspace(-5, 105, n_segments + 1)
        for j in range(n_segments):
            x1 = x_segments[j]
            x2 = x_segments[j + 1]
            lw = 1.0 + 2.0 * (1 - dist_from_center)
            ax.plot([x1, x2], [y, y], color="black", linewidth=lw)

        y += 1.5 + 1.5 * dist_from_center

    save(fig, "density_gradient_lines_pattern_abstract_minimalist")


# ============================================================
# RUN
# ============================================================
if __name__ == "__main__":
    print("=== BATCH 01: PARALLEL LINES ===")
    parallel_random()
    parallel_gradient()
    density_gradient()
    print("Selesai!")
