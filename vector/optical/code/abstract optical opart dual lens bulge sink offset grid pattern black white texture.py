import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
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


def warp(x, y, cx, cy, radius, strength):
    dx = x - cx
    dy = y - cy
    dist = np.hypot(dx, dy) + 1e-9
    if dist >= radius:
        return x, y
    t = dist / radius
    factor = 1.0 + strength * (np.cos(t * np.pi / 2) ** 2)
    return cx + dx * factor, cy + dy * factor


def generate():
    """Wild: Squircle checker grid warped by an offset bulge lens and a sink lens."""
    fig, ax = setup_ax()
    n = 24
    xs = np.linspace(-44, 44, n)
    ys = np.linspace(-44, 44, n)
    bulge = (-16.0, 12.0, 32.0, 0.48)
    sink = (18.0, -14.0, 28.0, -0.42)

    for i, x in enumerate(xs):
        for j, y in enumerate(ys):
            wx, wy = warp(x, y, *bulge)
            wx, wy = warp(wx, wy, *sink)
            dist = np.hypot(wx, wy)
            base = 2.55 * (0.88 + 0.18 * np.clip(1.2 - dist / 55.0, 0.4, 1.2))
            corner = min(base * 0.48, 0.25 + 1.55 * (1.0 - dist / 70.0))
            fill = (i + j) % 2 == 0
            ax.add_patch(
                FancyBboxPatch(
                    (wx - base / 2, wy - base / 2),
                    base,
                    base,
                    boxstyle=f"round,pad=0,rounding_size={max(0.12, corner):.2f}",
                    facecolor="black" if fill else "white",
                    edgecolor="black",
                    linewidth=0.7,
                )
            )

    save(
        fig,
        "abstract optical opart dual lens bulge sink offset grid pattern black white texture",
    )


if __name__ == "__main__":
    generate()
