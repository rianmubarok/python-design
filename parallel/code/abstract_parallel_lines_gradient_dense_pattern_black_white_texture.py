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


def parallel_gradient_dense():
    fig, ax = setup_ax()
    n_lines = 60
    for i in range(n_lines):
        y = -5 + i * (110 / n_lines)
        lw = 0.3 + 3.0 * np.sin(i / n_lines * np.pi)
        ax.plot([-5, 105], [y, y], color="black", linewidth=lw)
    save(fig, "parallel_gradient_dense")


def parallel_gradient_sparse():
    fig, ax = setup_ax()
    n_lines = 20
    for i in range(n_lines):
        y = -5 + i * (110 / n_lines)
        lw = 1.0 + 8.0 * np.sin(i / n_lines * np.pi)
        ax.plot([-5, 105], [y, y], color="black", linewidth=lw)
    save(fig, "parallel_gradient_sparse")


def parallel_gradient_offset_top():
    fig, ax = setup_ax()
    n_lines = 40
    for i in range(n_lines):
        y = -5 + i * 2.7
        lw = 0.5 + 5.0 * np.sin((i / n_lines * np.pi) + 0.5)
        ax.plot([-5, 105], [y, y], color="black", linewidth=lw)
    save(fig, "parallel_gradient_offset_top")


def parallel_gradient_offset_bottom():
    fig, ax = setup_ax()
    n_lines = 40
    for i in range(n_lines):
        y = -5 + i * 2.7
        lw = 0.5 + 5.0 * np.sin((i / n_lines * np.pi) - 0.5)
        ax.plot([-5, 105], [y, y], color="black", linewidth=lw)
    save(fig, "parallel_gradient_offset_bottom")


def parallel_broken_dense():
    fig, ax = setup_ax()
    n_lines = 35
    n_segments = 15
    segment_width = 100 / n_segments
    for i in range(n_lines):
        y = -5 + i * (110 / n_lines)
        for j in range(n_segments):
            if (i + j) % 2 == 0:
                x_start = -5 + j * segment_width
                x_end = x_start + segment_width
                ax.plot([x_start, x_end], [y, y], color="black", linewidth=0.5)
    save(fig, "parallel_broken_dense")


def parallel_broken_sparse():
    fig, ax = setup_ax()
    n_lines = 25
    n_segments = 6
    segment_width = 100 / n_segments
    for i in range(n_lines):
        y = -5 + i * (110 / n_lines)
        for j in range(n_segments):
            if (i + j) % 2 == 0:
                x_start = -5 + j * segment_width
                x_end = x_start + segment_width
                ax.plot([x_start, x_end], [y, y], color="black", linewidth=0.8)
    save(fig, "parallel_broken_sparse")


def parallel_curved_wide():
    fig, ax = setup_ax()
    n_lines = 30
    for i in range(n_lines):
        y_base = -5 + i * (110 / n_lines)
        x = np.linspace(-5, 105, 500)
        amplitude = 8 + 4 * np.sin(i / n_lines * np.pi)
        frequency = 0.3
        y = y_base + amplitude * np.sin(x * frequency)
        ax.plot(x, y, color="black", linewidth=0.5)
    save(fig, "parallel_curved_wide")


def parallel_curved_tight():
    fig, ax = setup_ax()
    n_lines = 45
    for i in range(n_lines):
        y_base = -5 + i * (110 / n_lines)
        x = np.linspace(-5, 105, 500)
        amplitude = 1.5
        frequency = 1.5
        y = y_base + amplitude * np.sin(x * frequency)
        ax.plot(x, y, color="black", linewidth=0.4)
    save(fig, "parallel_curved_tight")


def parallel_dashed_dense():
    fig, ax = setup_ax()
    n_lines = 30
    dash_len = 3
    gap_len = 1
    for i in range(n_lines):
        y = -5 + i * (110 / n_lines)
        x = -5
        while x < 105:
            ax.plot([x, min(x + dash_len, 105)], [y, y], color="black", linewidth=0.6)
            x += dash_len + gap_len
    save(fig, "parallel_dashed_dense")


if __name__ == "__main__":
    parallel_gradient_dense()
    parallel_gradient_sparse()
    parallel_gradient_offset_top()
    parallel_gradient_offset_bottom()
    parallel_broken_dense()
    parallel_broken_sparse()
    parallel_curved_wide()
    parallel_curved_tight()
    parallel_dashed_dense()
    parallel_gradient_sparse()
    parallel_gradient_offset_top()
    parallel_gradient_offset_bottom()
    parallel_broken_dense()
    parallel_broken_sparse()
    parallel_curved_wide()
    parallel_curved_tight()
    parallel_dashed_dense()
