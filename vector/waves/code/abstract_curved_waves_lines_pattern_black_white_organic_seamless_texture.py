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
    save(fig, "curved_waves")


if __name__ == "__main__":
    curved_waves()
