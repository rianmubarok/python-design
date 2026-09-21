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


def abstract_parallel_lines_fingerprint_whorl_triple_core_pattern_black_white_texture():
    """Wild combo: fingerprint whorl x multi focal -- three co-rotating cores in a triangle"""
    fig, ax = setup_ax()
    cores = np.array([[50.0, 62.0], [38.0, 42.0], [62.0, 42.0]])

    seeds = []
    for cx, cy in cores:
        for k in range(18):
            a = 2 * np.pi * k / 18
            seeds.append((cx + 1.5 * np.cos(a), cy + 1.5 * np.sin(a)))
    for rad in (26.0, 36.0):
        for k in range(22):
            a = 2 * np.pi * k / 22
            seeds.append((50.0 + rad * np.cos(a), 50.0 + rad * np.sin(a)))
    p = np.array(seeds)
    n = p.shape[0]

    max_steps = 9000
    h = 0.6
    xs = np.full((max_steps + 1, n), np.nan)
    ys = np.full((max_steps + 1, n), np.nan)
    xs[0] = p[:, 0]
    ys[0] = p[:, 1]
    x = p[:, 0].copy()
    y = p[:, 1].copy()
    active = np.ones(n, dtype=bool)

    for s in range(max_steps):
        if not active.any():
            break
        vx = np.zeros(n)
        vy = np.zeros(n)
        for qx, qy in cores:
            dx = x - qx
            dy = y - qy
            d2 = dx * dx + dy * dy + 2.0
            vx += -dy / d2
            vy += dx / d2
        norm = np.hypot(vx, vy)
        norm[norm < 1e-12] = 1.0
        x = x + h * vx / norm
        y = y + h * vy / norm
        active = active & ~((x < -170) | (x > 270) | (y < -170) | (y > 270))
        x = np.where(active, x, np.nan)
        y = np.where(active, y, np.nan)
        xs[s + 1] = x
        ys[s + 1] = y

    for j in range(n):
        xj = xs[:, j]
        yj = ys[:, j]
        m = ~np.isnan(xj)
        xj = xj[m]
        yj = yj[m]
        if xj.size > 380:
            idx = np.linspace(0, xj.size - 1, 380).astype(int)
            xj = xj[idx]
            yj = yj[idx]
        ax.plot(xj, yj, color="black", linewidth=0.7, solid_capstyle="round")

    save(fig, "abstract parallel lines fingerprint whorl triple core pattern black white texture")


if __name__ == "__main__":
    abstract_parallel_lines_fingerprint_whorl_triple_core_pattern_black_white_texture()
