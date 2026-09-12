import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# ============================================================
# BATCH 02 — WAVES & ZIGZAG
# Gelombang dan zigzag dengan variasi
# Setting: 4000x4000 px, 300 DPI, 1:1
# Output: PNG + SVG
# ============================================================

SIZE = 4000
DPI = 300
SEED = 42
BATCH = "batch_02_waves"

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
# 1. ZIGZAG WAVE — Gelombang zigzag
# ============================================================
def zigzag_wave():
    fig, ax = setup_ax()

    n_zigzags = 10
    for i in range(n_zigzags):
        y_base = -5 + i * 11
        amp = np.random.uniform(3, 8)
        freq = np.random.randint(4, 10)
        lw = np.random.choice([1.5, 2.0, 3.0, 4.0])

        x = np.linspace(-5, 105, 200)
        y = y_base + amp * np.sin(freq * x * np.pi / 100)
        ax.plot(x, y, color="black", linewidth=lw)

    save(fig, "zigzag_wave_lines_pattern_abstract_minimalist")


# ============================================================
# 2. CURVED WAVES — Gelombang lengkung organik
# ============================================================
def curved_waves():
    fig, ax = setup_ax()

    n_waves = 14
    for i in range(n_waves):
        y_base = -5 + i * 8
        amp = np.random.uniform(1.5, 5)
        freq = np.random.uniform(0.03, 0.12)
        phase = np.random.uniform(0, 2 * np.pi)
        lw = np.random.choice([1.5, 2.0, 3.0, 4.0])

        x = np.linspace(-5, 105, 300)
        y = y_base + amp * np.sin(freq * x * 2 * np.pi + phase)
        ax.plot(x, y, color="black", linewidth=lw)

    save(fig, "curved_waves_lines_pattern_abstract_seamless")


# ============================================================
# 3. DOUBLE ZIGZAG — Dua zigzag berlawanan arah
# ============================================================
def double_zigzag():
    fig, ax = setup_ax()

    n_pairs = 8
    for i in range(n_pairs):
        y_base = -5 + i * 13
        amp = np.random.uniform(4, 7)
        freq = np.random.randint(5, 9)
        phase = np.random.uniform(0, np.pi)
        lw = np.random.choice([1.5, 2.0, 2.5])

        x = np.linspace(-5, 105, 300)
        y1 = y_base + amp * np.sin(freq * x * np.pi / 100 + phase)
        y2 = y_base + amp * np.sin(freq * x * np.pi / 100 + phase + np.pi)
        ax.plot(x, y1, color="black", linewidth=lw)
        ax.plot(x, y2, color="black", linewidth=lw)

    save(fig, "double_zigzag_wave_lines_pattern_mirror_abstract")


# ============================================================
# 4. OPTICAL ILLUSION WAVE — Gelombang ilusi optik
# ============================================================
def optical_illusion_wave():
    fig, ax = setup_ax()

    n_lines = 70
    for i in range(n_lines):
        y = -5 + i * 1.6
        x = np.linspace(-5, 105, 400)
        amp = 3 * np.sin(i * 0.2)
        freq = 0.08 + 0.02 * np.sin(i * 0.1)
        y_wave = y + amp * np.sin(freq * x * 2 * np.pi + i * 0.5)
        lw = 1.0 + 0.8 * np.abs(np.sin(i * 0.15))
        ax.plot(x, y_wave, color="black", linewidth=lw)

    save(fig, "optical_illusion_wave_lines_pattern_abstract_motion")


# ============================================================
# 5. PULSE WAVE — Gelombang pulse dinamis
# ============================================================
def pulse_wave():
    fig, ax = setup_ax()

    n_lines = 45
    for i in range(n_lines):
        x = -5 + i * 2.4
        y = np.linspace(-5, 105, 300)
        amp = 4 * np.sin(i * 0.4) * np.cos(i * 0.15)
        x_wave = x + amp * np.sin(y * 0.15 + i * 0.3)
        lw = 1.2 + 1.5 * np.abs(np.sin(i * 0.3))
        ax.plot(x_wave, y, color="black", linewidth=lw)

    save(fig, "pulse_wave_lines_pattern_abstract_dynamic_motion")


# ============================================================
# RUN
# ============================================================
if __name__ == "__main__":
    print("=== BATCH 02: WAVES & ZIGZAG ===")
    zigzag_wave()
    curved_waves()
    double_zigzag()
    optical_illusion_wave()
    pulse_wave()
    print("Selesai!")
