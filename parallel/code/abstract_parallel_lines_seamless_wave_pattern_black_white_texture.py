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


def parallel_seamless_wave():
    fig, ax = setup_ax()
    n_lines = 35
    for i in range(n_lines):
        y_base = -5 + i * (110 / n_lines)
        x = np.linspace(-5, 105, 500)
        amplitude = 3
        frequency = 2 * np.pi / 110
        y = y_base + amplitude * np.sin(x * frequency)
        ax.plot(x, y, color="black", linewidth=0.6)
    save(fig, "parallel_seamless_wave")


def parallel_seamless_wave_group():
    fig, ax = setup_ax()
    n_lines = 35
    for i in range(n_lines):
        y_base = -5 + i * (110 / n_lines)
        x = np.linspace(-5, 105, 500)
        amplitude = 3 + 2 * np.sin(i / n_lines * np.pi)
        frequency = 2 * np.pi / 110
        y = y_base + amplitude * np.sin(x * frequency)
        ax.plot(x, y, color="black", linewidth=0.6)
    save(fig, "parallel_seamless_wave_group")


def parallel_seamless_wave_multi():
    fig, ax = setup_ax()
    n_lines = 30
    for i in range(n_lines):
        y_base = -5 + i * (110 / n_lines)
        x = np.linspace(-5, 105, 500)
        y = y_base + 2 * np.sin(x * 2 * np.pi / 110) + 1.5 * np.sin(x * 4 * np.pi / 110)
        ax.plot(x, y, color="black", linewidth=0.5)
    save(fig, "parallel_seamless_wave_multi")


def parallel_seamless_gradient():
    fig, ax = setup_ax()
    n_lines = 40
    for i in range(n_lines):
        y = -5 + i * (110 / n_lines)
        lw = 0.5 + 4.0 * np.sin(i / n_lines * np.pi)
        ax.plot([-5, 105], [y, y], color="black", linewidth=lw)
    save(fig, "parallel_seamless_gradient")


def parallel_seamless_dashed():
    fig, ax = setup_ax()
    n_lines = 30
    dash_len = 8
    gap_len = 4
    for i in range(n_lines):
        y = -5 + i * (110 / n_lines)
        x = -5
        while x < 105:
            ax.plot([x, min(x + dash_len, 105)], [y, y], color="black", linewidth=0.6)
            x += dash_len + gap_len
    save(fig, "parallel_seamless_dashed")


def parallel_seamless_staggered():
    fig, ax = setup_ax()
    n_lines = 40
    for i in range(n_lines):
        y = -5 + i * (110 / n_lines)
        x_offset = 5 * np.sin(i * 2 * np.pi / n_lines)
        ax.plot([-5 + x_offset, 105 + x_offset], [y, y], color="black", linewidth=0.6)
    save(fig, "parallel_seamless_staggered")


def parallel_seamless_crosshatch():
    fig, ax = setup_ax()
    n_lines = 30
    spacing = 110 / n_lines
    for i in range(n_lines):
        y = -5 + i * spacing
        ax.plot([-5, 105], [y, y], color="black", linewidth=0.4, alpha=0.5)
    for i in range(n_lines):
        x = -5 + i * spacing
        ax.plot([x, x], [-5, 105], color="black", linewidth=0.4, alpha=0.5)
    save(fig, "parallel_seamless_crosshatch")


if __name__ == "__main__":
    parallel_seamless_wave()
    parallel_seamless_wave_group()
    parallel_seamless_wave_multi()
    parallel_seamless_gradient()
    parallel_seamless_dashed()
    parallel_seamless_staggered()
    parallel_seamless_crosshatch()
