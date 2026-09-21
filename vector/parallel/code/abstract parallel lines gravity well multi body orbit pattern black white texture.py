import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime

SIZE = 4000
DPI = 300
DATE = datetime.now().strftime("%d%m%Y")

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR.parent / "output"
JPG_DIR = OUTPUT_DIR / "jpg"
SVG_DIR = OUTPUT_DIR / "svg"
JPG_DIR.mkdir(parents=True, exist_ok=True)
SVG_DIR.mkdir(parents=True, exist_ok=True)


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


def draw():
    """
    Three gravity wells placed in a triangle formation distort horizontal
    parallel lines. Each well pulls lines toward it with inverse-distance
    falloff, creating complex warped fields where the three influences overlap.
    """
    fig, ax = setup_ax()

    # Three gravity wells in a rough triangle
    wells = [
        (30.0, 70.0, 18.0),   # (x, y, strength)
        (75.0, 65.0, 15.0),
        (50.0, 25.0, 20.0),
    ]

    n_lines = 90
    n_pts = 600

    for i in range(n_lines):
        y0 = -5 + 110 * i / (n_lines - 1)
        x_base = np.linspace(-5, 105, n_pts)

        x_out = np.copy(x_base)
        y_out = np.full(n_pts, y0)

        for j in range(n_pts):
            total_dx = 0.0
            total_dy = 0.0
            for wx, wy, ws in wells:
                dx = x_out[j] - wx
                dy = y_out[j] - wy
                r = np.sqrt(dx * dx + dy * dy)
                r = max(r, 4.0)
                # Gravitational pull: toward the well
                force = ws / (r * 0.5)
                force = min(force, 8.0)
                total_dx -= force * dx / r
                total_dy -= force * dy / r
            x_out[j] += total_dx
            y_out[j] += total_dy

        ax.plot(x_out, y_out, color="black", linewidth=0.45, solid_capstyle="round")

    save(fig, "abstract parallel lines gravity well multi body orbit pattern black white texture")


if __name__ == "__main__":
    draw()
