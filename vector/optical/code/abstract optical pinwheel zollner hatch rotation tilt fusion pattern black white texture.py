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
    """Wild: Pinwheel where spokes carry Zollner hatch marks — combining rotation + tilt illusions."""
    fig, ax = setup_ax()

    n_spokes = 48
    t = np.linspace(0, 45, 200)
    hatch_len = 2.5

    for i in range(n_spokes):
        base_angle = i * 2 * np.pi / n_spokes
        angle = base_angle + 0.05 * t

        x = t * np.cos(angle)
        y = t * np.sin(angle)
        lw = 0.5 if i % 2 == 0 else 1.8
        ax.plot(x, y, color="black", linewidth=lw)

        # Zollner hatches along each spoke
        if i % 3 == 0:
            hatch_positions = np.linspace(8, 42, 10, dtype=int)
            tilt = 0.35 if i % 2 == 0 else -0.35
            for hi in hatch_positions:
                if hi < len(x) - 1:
                    hx, hy = x[hi], y[hi]
                    dx_tan = x[hi] - x[hi - 1]
                    dy_tan = y[hi] - y[hi - 1]
                    tangent = np.arctan2(dy_tan, dx_tan)
                    perp = tangent + np.pi / 2 + tilt
                    ddx = (hatch_len / 2) * np.cos(perp)
                    ddy = (hatch_len / 2) * np.sin(perp)
                    ax.plot([hx - ddx, hx + ddx], [hy - ddy, hy + ddy],
                            color="black", linewidth=1.3)

    save(fig, "abstract optical pinwheel zollner hatch rotation tilt fusion pattern black white texture")


if __name__ == "__main__":
    generate()
