import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# ============================================================
# BATCH 07 — OPTICAL ILLUSION
# Pola ilusi optik
# Setting: 4000x4000 px, 300 DPI, 1:1
# Output: PNG + SVG
# ============================================================

SIZE = 4000
DPI = 300
SEED = 42
BATCH = "batch_07_optical"

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
# 1. MOIRE INTERFERENCE — Efek moire interferensi
# ============================================================
def moire_interference():
    fig, ax = setup_ax()

    spacing = 3
    for offset in np.arange(-200, 300, spacing):
        lw = 0.8
        ax.plot([offset, offset + 200], [-50, 150], color="black", linewidth=lw, alpha=0.7)

    theta = np.linspace(0, 2 * np.pi, 360)
    for i in range(60):
        r = 2 + i * 1.5
        x = 50 + r * np.cos(theta)
        y = 50 + r * np.sin(theta)
        ax.plot(x, y, color="black", linewidth=0.6, alpha=0.5)

    save(fig, "moire_pattern_interference_lines_abstract_optical")


# ============================================================
# 2. OP ART CHECKERBOARD — Ilusi optik checkerboard
# ============================================================
def op_art_checkerboard():
    fig, ax = setup_ax()

    size = 5
    for i, x in enumerate(np.arange(-5, 105, size)):
        for j, y in enumerate(np.arange(-5, 105, size)):
            if (i + j) % 2 == 0:
                cx_sq = x + size / 2
                cy_sq = y + size / 2
                dist = np.sqrt((cx_sq - 50)**2 + (cy_sq - 50)**2)
                wave = 0.3 * np.sin(dist * 0.3)
                corners = [
                    (x + wave, y - wave),
                    (x + size - wave, y + wave),
                    (x + size + wave, y + size - wave),
                    (x - wave, y + size + wave),
                ]
                xs = [c[0] for c in corners] + [corners[0][0]]
                ys = [c[1] for c in corners] + [corners[0][1]]
                ax.fill(xs, ys, color="black")

    save(fig, "op_art_optical_illusion_checkerboard_pattern")


# ============================================================
# 3. CHECKERBOARD WAVE — Checkerboard distorsi gelombang
# ============================================================
def checkerboard_wave():
    fig, ax = setup_ax()

    size = 5
    for i, x in enumerate(np.arange(-5, 105, size)):
        for j, y in enumerate(np.arange(-5, 105, size)):
            if (i + j) % 2 == 0:
                cx_sq = x + size / 2
                cy_sq = y + size / 2
                wave_x = 1.5 * np.sin(cy_sq * 0.2)
                wave_y = 1.5 * np.sin(cx_sq * 0.2)
                rect = plt.Rectangle((x + wave_x, y + wave_y), size, size, color="black")
                ax.add_patch(rect)

    save(fig, "checkerboard_wave_distortion_pattern_optical")


# ============================================================
# RUN
# ============================================================
if __name__ == "__main__":
    print("=== BATCH 07: OPTICAL ILLUSION ===")
    moire_interference()
    op_art_checkerboard()
    checkerboard_wave()
    print("Selesai!")
