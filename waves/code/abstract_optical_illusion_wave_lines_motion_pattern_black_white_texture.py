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
    save(fig, "optical_illusion_wave")


if __name__ == "__main__":
    optical_illusion_wave()
