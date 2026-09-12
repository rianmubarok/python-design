import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# ============================================================
# BATCH 03 — RADIAL & SUNBURST
# Pola radial dan memancar dari pusat
# Setting: 4000x4000 px, 300 DPI, 1:1
# Output: PNG + SVG
# ============================================================

SIZE = 4000
DPI = 300
SEED = 42
BATCH = "batch_03_radial"

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
# 1. RADIAL SUNBURST — Garis memancar dari pusat
# ============================================================
def radial_sunburst():
    fig, ax = setup_ax()

    cx, cy = 20, 50
    n_lines = 35
    for i in range(n_lines):
        angle = -80 + i * (160 / n_lines)
        rad = np.radians(angle)
        length = 100
        x2 = cx + length * np.cos(rad)
        y2 = cy + length * np.sin(rad)
        lw = np.random.choice([1.5, 2.0, 3.0, 4.0, 5.0])
        ax.plot([cx, x2], [cy, y2], color="black", linewidth=lw)

    ax.plot(cx, cy, "o", color="black", markersize=15)
    save(fig, "radial_lines_pattern_sunburst_abstract_design")


# ============================================================
# 2. CONVERGING PERSPECTIVE — Garis konvergen ke titik fokus
# ============================================================
def converging_perspective():
    fig, ax = setup_ax()

    focus_x, focus_y = 75, 50
    for i in range(24):
        angle = i * (360 / 24)
        rad = np.radians(angle)
        length = 100
        x1 = focus_x + length * np.cos(rad)
        y1 = focus_y + length * np.sin(rad)
        lw = np.random.choice([1.5, 2.0, 3.0, 4.0])
        ax.plot([focus_x, x1], [focus_y, y1], color="black", linewidth=lw)

    ax.plot(focus_x, focus_y, "o", color="black", markersize=15)
    save(fig, "converging_lines_pattern_perspective_abstract")


# ============================================================
# 3. RADIAL DENSITY — Radial dengan kepadatan bervariasi
# ============================================================
def radial_density():
    fig, ax = setup_ax()

    cx, cy = 50, 50
    n_lines = 72
    for i in range(n_lines):
        angle = i * (360 / n_lines)
        rad = np.radians(angle)
        length = 60
        x2 = cx + length * np.cos(rad)
        y2 = cy + length * np.sin(rad)
        lw = 0.5 + 3.0 * np.abs(np.sin(angle * np.pi / 180 * 3))
        ax.plot([cx, x2], [cy, y2], color="black", linewidth=lw)

    ax.plot(cx, cy, "o", color="black", markersize=10)
    save(fig, "radial_density_variation_lines_pattern_abstract")


# ============================================================
# 4. PINWHEEL — Kincir garis berputar
# ============================================================
def pinwheel():
    fig, ax = setup_ax()

    cx, cy = 50, 50
    n_arms = 12
    for i in range(n_arms):
        base_angle = i * (360 / n_arms)
        for j in range(40):
            angle = base_angle + j * 2
            rad = np.radians(angle)
            r_start = j * 1.2
            r_end = r_start + 2
            x1 = cx + r_start * np.cos(rad)
            y1 = cy + r_start * np.sin(rad)
            x2 = cx + r_end * np.cos(np.radians(angle + 3))
            y2 = cy + r_end * np.sin(np.radians(angle + 3))
            lw = 1.0 + 1.5 * (j / 40)
            ax.plot([x1, x2], [y1, y2], color="black", linewidth=lw)

    ax.plot(cx, cy, "o", color="black", markersize=12)
    save(fig, "pinwheel_rotating_lines_pattern_abstract_radial")


# ============================================================
# 5. MANDALA — Pola melingkar simetris
# ============================================================
def mandala():
    fig, ax = setup_ax()

    cx, cy = 50, 50
    n_petals = 12
    n_rings = 8

    for ring in range(n_rings):
        r = 5 + ring * 6
        theta = np.linspace(0, 2 * np.pi, 200)
        x = cx + r * np.cos(theta)
        y = cy + r * np.sin(theta)
        lw = 1.0 + 1.5 * (ring / n_rings)
        ax.plot(x, y, color="black", linewidth=lw)

    for i in range(n_petals):
        angle = i * (360 / n_petals)
        for j in range(1, n_rings + 1):
            r = 5 + j * 6
            petal_angle = np.linspace(-15, 15, 30) + angle
            rad = np.radians(petal_angle)
            x = cx + r * np.cos(rad)
            y = cy + r * np.sin(rad)
            lw = 0.8 + 1.0 * (j / n_rings)
            ax.plot(x, y, color="black", linewidth=lw)

    ax.plot(cx, cy, "o", color="black", markersize=10)
    save(fig, "mandala_circular_symmetric_pattern_abstract_spiritual")


# ============================================================
# RUN
# ============================================================
if __name__ == "__main__":
    print("=== BATCH 03: RADIAL & SUNBURST ===")
    radial_sunburst()
    converging_perspective()
    radial_density()
    pinwheel()
    mandala()
    print("Selesai!")
