import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# ============================================================
# BATCH 05 — CONTOUR & TOPOGRAPHIC
# Pola kontur dan topografi
# Setting: 4000x4000 px, 300 DPI, 1:1
# Output: PNG + SVG
# ============================================================

SIZE = 4000
DPI = 300
SEED = 42
BATCH = "batch_05_contour"

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
# 1. TOPOGRAPHIC CONTOUR — Kontur topografi single peak
# ============================================================
def topographic_contour():
    fig, ax = setup_ax()

    cx, cy = 50, 50
    n_rings = 30
    for i in range(n_rings):
        r = 2 + i * 2
        theta = np.linspace(0, 2 * np.pi, 200)
        noise = 2.0 * np.sin(5 * theta) * np.cos(3 * theta + i * 0.3)
        x = cx + (r + noise) * np.cos(theta)
        y = cy + (r + noise) * np.sin(theta)
        lw = 1.5 + 1.5 * (i / n_rings)
        ax.plot(x, y, color="black", linewidth=lw)

    save(fig, "topographic_contour_lines_pattern_abstract_texture")


# ============================================================
# 2. MULTI-PEAK TOPOGRAPHIC — Kontur multi puncak
# ============================================================
def multi_peak_topographic():
    fig, ax = setup_ax()

    peaks = [(25, 30), (70, 60), (45, 75)]
    n_rings = 40

    for peak_x, peak_y in peaks:
        for i in range(n_rings):
            r = 1 + i * 1.5
            theta = np.linspace(0, 2 * np.pi, 200)
            noise = 1.5 * np.sin(4 * theta + i * 0.2)
            x = peak_x + (r + noise) * np.cos(theta)
            y = peak_y + (r + noise) * np.sin(theta)
            lw = 0.8 + 1.2 * (1 - i / n_rings)
            ax.plot(x, y, color="black", linewidth=lw)

    save(fig, "topographic_multi_peak_contour_lines_pattern")


# ============================================================
# 3. CONTOUR OVERLAP — Kontur tumpang tindih
# ============================================================
def contour_overlap():
    fig, ax = setup_ax()

    centers = [(30, 30), (70, 30), (50, 70)]
    n_rings = 25

    for cx, cy in centers:
        for i in range(n_rings):
            r = 1 + i * 2.5
            theta = np.linspace(0, 2 * np.pi, 200)
            noise = 1.0 * np.sin(6 * theta + i * 0.4)
            x = cx + (r + noise) * np.cos(theta)
            y = cy + (r + noise) * np.sin(theta)
            lw = 0.8 + 1.0 * (1 - i / n_rings)
            ax.plot(x, y, color="black", linewidth=lw)

    save(fig, "contour_overlap_topographic_pattern_multi_peak")


# ============================================================
# 4. INTERFERENCE WAVES — Kontur interferensi gelombang
# ============================================================
def interference_waves():
    fig, ax = setup_ax()

    x = np.linspace(-5, 105, 500)
    y = np.linspace(-5, 105, 500)
    X, Y = np.meshgrid(x, y)

    Z = np.sin(X * 0.5) * np.sin(Y * 0.5)
    Z = (Z - Z.min()) / (Z.max() - Z.min())

    n_levels = 30
    levels = np.linspace(0, 1, n_levels)
    ax.contour(X, Y, Z, levels=levels, colors='black', linewidths=0.8)

    save(fig, "interference_waves_contour_pattern_abstract_optical")


# ============================================================
# 5. WAVE INTERFERENCE GRID — Grid interferensi gelombang
# ============================================================
def wave_interference_grid():
    fig, ax = setup_ax()

    x = np.linspace(-5, 105, 400)
    y = np.linspace(-5, 105, 400)
    X, Y = np.meshgrid(x, y)

    Z1 = np.sin(X * 0.3) * np.cos(Y * 0.3)
    Z2 = np.cos(X * 0.3) * np.sin(Y * 0.3)
    Z = Z1 + Z2

    n_levels = 25
    levels = np.linspace(Z.min(), Z.max(), n_levels)
    ax.contour(X, Y, Z, levels=levels, colors='black', linewidths=0.7)

    save(fig, "wave_interference_grid_pattern_abstract_optical")


# ============================================================
# RUN
# ============================================================
if __name__ == "__main__":
    print("=== BATCH 05: CONTOUR & TOPOGRAPHIC ===")
    topographic_contour()
    multi_peak_topographic()
    contour_overlap()
    interference_waves()
    wave_interference_grid()
    print("Selesai!")
