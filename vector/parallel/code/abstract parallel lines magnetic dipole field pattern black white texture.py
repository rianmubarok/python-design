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


def abstract_parallel_lines_magnetic_dipole_field_pattern_black_white_texture():
    """Wild: parallel lines replaced by streamlines of an opposite-pole field"""
    fig, ax = setup_ax()
    poles = [(28.0, 50.0, 1.0), (72.0, 50.0, -1.0)]

    def unit_field(x, y):
        vx = vy = 0.0
        for qx, qy, q in poles:
            dx, dy = x - qx, y - qy
            d2 = dx * dx + dy * dy
            if d2 < 1e-9:
                continue
            inv = q / (d2 * np.sqrt(d2))
            vx += dx * inv
            vy += dy * inv
        n = np.hypot(vx, vy)
        if n < 1e-12:
            return 0.0, 0.0
        return vx / n, vy / n

    h = 0.4
    r_seed = 2.0
    n_seeds = 30
    for a in np.linspace(0.0, 2 * np.pi, n_seeds, endpoint=False):
        x = 28.0 + r_seed * np.cos(a)
        y = 50.0 + r_seed * np.sin(a)
        xs, ys = [x], [y]
        for _ in range(16000):
            k1x, k1y = unit_field(x, y)
            k2x, k2y = unit_field(x + 0.5 * h * k1x, y + 0.5 * h * k1y)
            k3x, k3y = unit_field(x + 0.5 * h * k2x, y + 0.5 * h * k2y)
            k4x, k4y = unit_field(x + h * k3x, y + h * k3y)
            x += h / 6 * (k1x + 2 * k2x + 2 * k3x + k4x)
            y += h / 6 * (k1y + 2 * k2y + 2 * k3y + k4y)
            xs.append(x)
            ys.append(y)
            if np.hypot(x - 72.0, y - 50.0) < 1.0:
                xs.append(72.0)
                ys.append(50.0)
                break
            if x < -260 or x > 360 or y < -260 or y > 360:
                break
        if len(xs) > 900:
            idx = np.linspace(0, len(xs) - 1, 900).astype(int)
            xs = [xs[j] for j in idx]
            ys = [ys[j] for j in idx]
        ax.plot(xs, ys, color="black", linewidth=0.7, solid_capstyle="round")

    save(fig, "abstract parallel lines magnetic dipole field pattern black white texture")


if __name__ == "__main__":
    abstract_parallel_lines_magnetic_dipole_field_pattern_black_white_texture()
