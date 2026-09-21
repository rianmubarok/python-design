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
    ax.set_xlim(-50, 50)
    ax.set_ylim(-50, 50)
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


def generate():
    """Wild: Phase-modulated Lissajous grid where grid spacing oscillates sinusoidally from center."""
    fig, ax = setup_ax()

    # Grid lines that breathe — spacing grows then shrinks as a sine function of position
    n_lines = 50
    y_pts = np.linspace(-48, 48, 400)

    for i in range(n_lines):
        # Normal linear spacing
        x_base_raw = -46 + (92 * i / (n_lines - 1))

        # Warp: compress/expand positions like an accordion
        x_base = 46 * np.tanh(x_base_raw / 25)

        # Phase-shift the column wave based on x position
        phase = np.pi * x_base / 25
        freq = 4 + 2 * np.sin(x_base / 20)
        x_vals = x_base + 3.5 * np.sin(freq * y_pts / 10 + phase)
        ax.plot(x_vals, y_pts, color="black", linewidth=1.0)

    x_pts = np.linspace(-48, 48, 400)
    for i in range(n_lines):
        y_base_raw = -46 + (92 * i / (n_lines - 1))
        y_base = 46 * np.tanh(y_base_raw / 25)

        phase = np.pi * y_base / 25
        freq = 4 + 2 * np.sin(y_base / 20)
        y_vals = y_base + 3.5 * np.sin(freq * x_pts / 10 + phase)
        ax.plot(x_pts, y_vals, color="black", linewidth=1.0)

    save(fig, "abstract optical lissajous accordion tanh warp grid pattern black white texture")


if __name__ == "__main__":
    generate()
