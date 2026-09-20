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


def abstract_parallel_lines_chaotic_intersecting_bezier_loop_pattern_black_white_texture():
    fig, ax = setup_ax()

    n_lines = 50
    t = np.linspace(0, 2 * np.pi, 1000)  # Tingkatkan sampel agar garis lebih halus

    # Gunakan frekuensi tetap/bertahap agar antar garis tetap memiliki alur paralel
    freq1 = 4.0
    freq2 = 7.0

    for i in range(n_lines):
        r_base = 15 + i * 1.2

        # Amplitudo bertahap (smooth gradient)
        amp1 = 12 * np.sin(i * 0.08)
        amp2 = 6 * np.cos(i * 0.12)

        r = r_base + amp1 * np.sin(freq1 * t) + amp2 * np.cos(freq2 * t)

        drift_x = 50 + 8 * np.sin(i * 0.15)
        drift_y = 50 + 8 * np.cos(i * 0.15)

        x = drift_x + r * np.cos(t)
        y = drift_y + r * np.sin(t)

        ax.plot(
            x,
            y,
            color="black",
            linewidth=0.6,
            alpha=0.85,
            antialiased=True,  # Menghindari garis terlihat putus-putus
        )

    save(
        fig,
        "abstract parallel lines chaotic intersecting bezier loop pattern black white texture",
    )


if __name__ == "__main__":
    abstract_parallel_lines_chaotic_intersecting_bezier_loop_pattern_black_white_texture()
