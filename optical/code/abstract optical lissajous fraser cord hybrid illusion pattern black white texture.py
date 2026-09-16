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
    """Wild combo: Lissajous curves used as RAILS for Fraser cord illusion segments."""
    fig, ax = setup_ax()

    t_curve = np.linspace(0, 2 * np.pi, 3000)
    tilt_angle = np.radians(20)

    freq_pairs = [(3, 4), (5, 6), (2, 3), (7, 5)]
    scales = [40, 34, 28, 20]

    for (fa, fb), scale in zip(freq_pairs, scales):
        delta = np.pi / 4
        x_liss = scale * np.sin(fa * t_curve + delta)
        y_liss = scale * np.cos(fb * t_curve)

        # Sample sparse positions along curve for cord segments
        sample_step = 30
        for k in range(0, len(t_curve) - sample_step, sample_step):
            cx = x_liss[k]
            cy = y_liss[k]

            # Local tangent direction
            dx_tan = x_liss[k + 1] - x_liss[k - 1] if k > 0 else x_liss[1] - x_liss[0]
            dy_tan = y_liss[k + 1] - y_liss[k - 1] if k > 0 else y_liss[1] - y_liss[0]
            tangent = np.arctan2(dy_tan, dx_tan)
            cord_dir = tangent + tilt_angle

            segment_len = 3.0
            ddx = (segment_len / 2) * np.cos(cord_dir)
            ddy = (segment_len / 2) * np.sin(cord_dir)

            ax.plot([cx - ddx, cx + ddx], [cy - ddy, cy + ddy],
                    color="black", linewidth=2.4)
            ax.plot([cx - ddx * 0.5, cx + ddx * 0.5],
                    [cy - ddy * 0.5, cy + ddy * 0.5],
                    color="white", linewidth=0.9)

    save(fig, "abstract optical lissajous fraser cord hybrid illusion pattern black white texture")


if __name__ == "__main__":
    generate()
