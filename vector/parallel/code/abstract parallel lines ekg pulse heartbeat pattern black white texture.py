import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime

SIZE = 4000
DPI = 300
SEED = 42
DATE = datetime.now().strftime("%d%m%Y")

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR.parent / "output"
JPG_DIR = OUTPUT_DIR / "jpg"
SVG_DIR = OUTPUT_DIR / "svg"
JPG_DIR.mkdir(parents=True, exist_ok=True)
SVG_DIR.mkdir(parents=True, exist_ok=True)

np.random.seed(SEED)


def setup_ax():
    fig, ax = plt.subplots(figsize=(SIZE / DPI, SIZE / DPI), dpi=DPI)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.set_facecolor("white")
    ax.set_xlim(-5, 105)
    ax.set_ylim(-5, 105)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def save(fig, name):
    jpg_path = JPG_DIR / f"{name} {DATE}.jpg"
    svg_path = SVG_DIR / f"{name} {DATE}.svg"
    fig.savefig(jpg_path, dpi=DPI, pad_inches=0, facecolor="white")
    fig.savefig(svg_path, format="svg", pad_inches=0, facecolor="white")
    plt.close(fig)
    print(f"Tersimpan: {jpg_path} | {svg_path}")


def abstract_parallel_lines_ekg_pulse_heartbeat_pattern_black_white_texture():
    """Wild: parallel raster lines each spiking like an EKG heartbeat at centre column"""
    fig, ax = setup_ax()
    n_lines = 72
    x = np.linspace(-5, 105, 1200)
    cx = 50.0
    # pulse shape: flat baseline + sharp PQRST-like spike
    # encode relative to cx
    dx = x - cx

    def pulse(dx, scale):
        # P wave
        p = 0.5 * np.exp(-((dx + 18) ** 2) / 18)
        # Q dip
        q = -0.4 * np.exp(-((dx + 6) ** 2) / 3)
        # R spike
        r = 3.5 * np.exp(-((dx) ** 2) / 1.8)
        # S dip
        s = -0.6 * np.exp(-((dx - 5) ** 2) / 2.5)
        # T wave
        t = 0.8 * np.exp(-((dx - 20) ** 2) / 28)
        return scale * (p + q + r + s + t)

    for i in range(n_lines):
        y0 = -5 + i * (110 / (n_lines - 1))
        # amplitude of the spike falls off toward top/bottom
        dist = abs(y0 - 50) / 55
        amp = 3.5 * (1 - dist ** 1.4)
        y = y0 + pulse(dx, amp)
        lw = 0.55 + 0.6 * (1 - dist)
        ax.plot(x, y, color="black", linewidth=lw, solid_capstyle="round")

    save(fig, "abstract parallel lines ekg pulse heartbeat pattern black white texture")


if __name__ == "__main__":
    abstract_parallel_lines_ekg_pulse_heartbeat_pattern_black_white_texture()
