import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime

SIZE = 4000
DPI = 300
SEED = 42
DATE = datetime.now().strftime("%d%m%Y")

JPG_DIR = Path("output/jpg")
SVG_DIR = Path("output/svg")
JPG_DIR.mkdir(parents=True, exist_ok=True)
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
    jpg_path = JPG_DIR / f"{name}_{DATE}.jpg"
    svg_path = SVG_DIR / f"{name}_{DATE}.svg"
    fig.savefig(jpg_path, dpi=DPI, pad_inches=0, facecolor="white")
    fig.savefig(svg_path, format="svg", pad_inches=0, facecolor="white")
    plt.close(fig)
    print(f"Tersimpan: {jpg_path} | {svg_path}")


def parallel_curved_wider():
    fig, ax = setup_ax()
    n_lines = 40
    for i in range(n_lines):
        y_base = -5 + i * 2.8
        x = np.linspace(-5, 105, 300)
        curve = 25 * np.sin(x * np.pi / 100) * (1 - i / n_lines)
        y = y_base + curve
        lw = 1.5 + 2.0 * (i / n_lines)
        ax.plot(x, y, color="black", linewidth=lw)
    save(fig, "parallel_curved_wider")


def parallel_curved_tighter():
    fig, ax = setup_ax()
    n_lines = 50
    for i in range(n_lines):
        y_base = -5 + i * 2.2
        x = np.linspace(-5, 105, 300)
        curve = 8 * np.sin(x * np.pi / 100) * (1 - i / n_lines)
        y = y_base + curve
        lw = 1.0 + 1.5 * (i / n_lines)
        ax.plot(x, y, color="black", linewidth=lw)
    save(fig, "parallel_curved_tighter")


def parallel_sine_high_freq():
    fig, ax = setup_ax()
    n_lines = 35
    for i in range(n_lines):
        y_base = -5 + i * (110 / n_lines)
        x = np.linspace(-5, 105, 500)
        amplitude = 3 + 2 * np.sin(i / n_lines * np.pi)
        frequency = 1.2
        y = y_base + amplitude * np.sin(x * frequency)
        ax.plot(x, y, color="black", linewidth=0.6)
    save(fig, "parallel_sine_high_freq")


def parallel_sine_low_freq():
    fig, ax = setup_ax()
    n_lines = 35
    for i in range(n_lines):
        y_base = -5 + i * (110 / n_lines)
        x = np.linspace(-5, 105, 500)
        amplitude = 3 + 2 * np.sin(i / n_lines * np.pi)
        frequency = 0.2
        y = y_base + amplitude * np.sin(x * frequency)
        ax.plot(x, y, color="black", linewidth=0.6)
    save(fig, "parallel_sine_low_freq")


def parallel_staggered_wide():
    fig, ax = setup_ax()
    n_lines = 40
    stagger_amp = 15
    for i in range(n_lines):
        y = -5 + i * 2.8
        x_offset = stagger_amp * np.sin(i * 0.8)
        lw = 2.0 + 1.5 * np.abs(np.sin(i * 0.4))
        ax.plot([-5 + x_offset, 105 + x_offset], [y, y], color="black", linewidth=lw)
    save(fig, "parallel_staggered_wide")


def parallel_staggered_narrow():
    fig, ax = setup_ax()
    n_lines = 50
    stagger_amp = 4
    for i in range(n_lines):
        y = -5 + i * 2.2
        x_offset = stagger_amp * np.sin(i * 0.8)
        lw = 1.5 + 1.0 * np.abs(np.sin(i * 0.4))
        ax.plot([-5 + x_offset, 105 + x_offset], [y, y], color="black", linewidth=lw)
    save(fig, "parallel_staggered_narrow")


def parallel_wave_modulated_strong():
    fig, ax = setup_ax()
    n_lines = 35
    for i in range(n_lines):
        y_base = -5 + i * (110 / n_lines)
        x = np.linspace(-5, 105, 500)
        modulation = 1.5 + 1.0 * np.sin(i / n_lines * np.pi)
        y = y_base + modulation * np.sin(x * 0.8 + i * 0.5)
        ax.plot(x, y, color="black", linewidth=0.6)
    save(fig, "parallel_wave_modulated_strong")


def parallel_wave_modulated_weak():
    fig, ax = setup_ax()
    n_lines = 45
    for i in range(n_lines):
        y_base = -5 + i * (110 / n_lines)
        x = np.linspace(-5, 105, 500)
        modulation = 0.5 + 0.3 * np.sin(i / n_lines * np.pi)
        y = y_base + modulation * np.sin(x * 0.8 + i * 0.5)
        ax.plot(x, y, color="black", linewidth=0.5)
    save(fig, "parallel_wave_modulated_weak")


def parallel_density_center():
    fig, ax = setup_ax()
    n_lines = 40
    center_y = 50
    for i in range(n_lines):
        y = -5 + i * (110 / n_lines)
        dist = abs(y - center_y)
        max_dist = 55
        density_factor = 1 - dist / max_dist
        lw = 0.3 + 3.0 * density_factor
        ax.plot([-5, 105], [y, y], color="black", linewidth=lw)
    save(fig, "parallel_density_center")


def parallel_density_edges():
    fig, ax = setup_ax()
    n_lines = 40
    for i in range(n_lines):
        y = -5 + i * (110 / n_lines)
        dist_from_edge = min(abs(y - (-5)), abs(y - 105))
        max_dist = 55
        density_factor = 1 - dist_from_edge / max_dist
        lw = 0.3 + 3.0 * density_factor
        ax.plot([-5, 105], [y, y], color="black", linewidth=lw)
    save(fig, "parallel_density_edges")


def parallel_rhythmic_fast():
    fig, ax = setup_ax()
    n_lines = 40
    for i in range(n_lines):
        y = -5 + i * 2.8
        phase = np.sin(i * 1.5) * 0.5
        lw = 1.0 + 3.0 * np.abs(np.sin(i * 1.5 + phase))
        ax.plot([-5, 105], [y, y], color="black", linewidth=lw)
    save(fig, "parallel_rhythmic_fast")


def parallel_rhythmic_slow():
    fig, ax = setup_ax()
    n_lines = 40
    for i in range(n_lines):
        y = -5 + i * 2.8
        phase = np.sin(i * 0.3) * 0.5
        lw = 1.0 + 3.0 * np.abs(np.sin(i * 0.3 + phase))
        ax.plot([-5, 105], [y, y], color="black", linewidth=lw)
    save(fig, "parallel_rhythmic_slow")


if __name__ == "__main__":
    parallel_curved_wider()
    parallel_curved_tighter()
    parallel_sine_high_freq()
    parallel_sine_low_freq()
    parallel_staggered_wide()
    parallel_staggered_narrow()
    parallel_wave_modulated_strong()
    parallel_wave_modulated_weak()
    parallel_density_center()
    parallel_density_edges()
    parallel_rhythmic_fast()
    parallel_rhythmic_slow()
