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
    save(fig, "pulse_wave")


if __name__ == "__main__":
    pulse_wave()
