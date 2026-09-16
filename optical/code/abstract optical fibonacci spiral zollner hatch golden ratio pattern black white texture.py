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
    """Wild: Fibonacci spiral combined with Zollner hatching — golden ratio vortex meets tilt illusion."""
    fig, ax = setup_ax()

    # Draw Fibonacci/golden spiral
    phi = (1 + np.sqrt(5)) / 2
    n_quarter_turns = 14
    hatch_len = 2.5

    for q in range(n_quarter_turns):
        t = np.linspace(q * np.pi / 2, (q + 1) * np.pi / 2, 100)
        r = phi ** (2 * t / np.pi)
        scale = 0.8
        x = scale * r * np.cos(t)
        y = scale * r * np.sin(t)
        ax.plot(x, y, color="black", linewidth=2.5)

        # Zollner hatch marks along the spiral curve
        hatch_indices = np.linspace(0, len(t) - 2, 8, dtype=int)
        hatch_tilt = 0.4 if q % 2 == 0 else -0.4

        for idx in hatch_indices:
            hx, hy = x[idx], y[idx]
            dx_tan = x[idx + 1] - x[idx]
            dy_tan = y[idx + 1] - y[idx]
            tangent = np.arctan2(dy_tan, dx_tan)
            perp = tangent + np.pi / 2 + hatch_tilt

            ddx = (hatch_len / 2) * np.cos(perp)
            ddy = (hatch_len / 2) * np.sin(perp)
            ax.plot([hx - ddx, hx + ddx], [hy - ddy, hy + ddy],
                    color="black", linewidth=1.6)

    save(fig, "abstract optical fibonacci spiral zollner hatch golden ratio pattern black white texture")


if __name__ == "__main__":
    generate()
