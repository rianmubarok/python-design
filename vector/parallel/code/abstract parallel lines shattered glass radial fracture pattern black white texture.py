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
    Horizontal parallel lines shattered by a radial impact point.
    Lines break and deflect outward from the impact center like cracked glass.
    Near the impact, radial fracture lines emanate; further out, the horizontal
    lines bend and resume with offsets.
    """
    fig, ax = setup_ax()
    rng = np.random.default_rng(42)

    # Impact point
    ix, iy = 55.0, 48.0
    shatter_radius = 35.0
    n_lines = 80
    n_pts = 600

    # Draw horizontal lines with shatter distortion
    for i in range(n_lines):
        y0 = -5 + (110) * i / (n_lines - 1)
        x = np.linspace(-5, 105, n_pts)
        y = np.full(n_pts, y0)

        x_out = np.zeros(n_pts)
        y_out = np.zeros(n_pts)

        for j in range(n_pts):
            dx = x[j] - ix
            dy = y[j] - iy
            r = np.sqrt(dx * dx + dy * dy)

            if r < shatter_radius:
                # Inside shatter zone: push outward radially
                t = r / shatter_radius  # 0 at center, 1 at edge
                push = (1 - t) ** 2 * 12.0
                angle = np.arctan2(dy, dx)
                # Add angular jitter for broken glass look
                angle += rng.normal(0, 0.15) * (1 - t)
                x_out[j] = x[j] + push * np.cos(angle)
                y_out[j] = y[j] + push * np.sin(angle)
                # Create gaps near center
                if r < shatter_radius * 0.2:
                    x_out[j] = np.nan
                    y_out[j] = np.nan
            else:
                # Outside: subtle residual displacement
                falloff = np.exp(-(r - shatter_radius) / 15.0)
                angle = np.arctan2(dy, dx)
                x_out[j] = x[j] + falloff * 1.5 * np.cos(angle)
                y_out[j] = y[j] + falloff * 1.5 * np.sin(angle)

        ax.plot(x_out, y_out, color="black", linewidth=0.5, solid_capstyle="round")

    # Draw radial fracture lines from impact center
    n_fractures = 24
    for k in range(n_fractures):
        angle = 2 * np.pi * k / n_fractures + rng.normal(0, 0.1)
        length = shatter_radius * rng.uniform(0.6, 1.3)
        n_seg = 60
        t_vals = np.linspace(0, 1, n_seg)
        fx = np.zeros(n_seg)
        fy = np.zeros(n_seg)
        for s in range(n_seg):
            t = t_vals[s]
            r = length * t
            # Jagged fracture: slight angular wobble
            a = angle + rng.normal(0, 0.08) * t
            fx[s] = ix + r * np.cos(a)
            fy[s] = iy + r * np.sin(a)
        ax.plot(fx, fy, color="black", linewidth=0.35, solid_capstyle="round")

    save(fig, "abstract parallel lines shattered glass radial fracture pattern black white texture")


if __name__ == "__main__":
    draw()
