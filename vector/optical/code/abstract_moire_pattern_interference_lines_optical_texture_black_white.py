import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime
SCRIPT_DIR = Path(__file__).resolve().parent

SIZE = 4000
DPI = 300
SEED = 42
DATE = datetime.now().strftime("%d%m%Y")

JPG_DIR = SCRIPT_DIR.parent / "output" / "jpg"
SVG_DIR = SCRIPT_DIR.parent / "output" / "svg"
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
    save(fig, "moire_interference")


if __name__ == "__main__":
    moire_interference()
