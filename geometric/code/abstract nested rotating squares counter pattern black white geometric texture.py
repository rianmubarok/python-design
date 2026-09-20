import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime

SIZE = 4000
DPI = 300
SEED = 42
DATE = datetime.now().strftime("%d%m%Y")

SCRIPT DIR = Path(  file  ).resolve().parent
OUTPUT DIR = SCRIPT DIR.parent / "output"
JPG DIR = OUTPUT DIR / "jpg"
SVG DIR = OUTPUT DIR / "svg"
JPG DIR.mkdir(parents=True, exist ok=True)
SVG DIR.mkdir(parents=True, exist ok=True)

np.random.seed(SEED)


def setup ax():
    fig, ax = plt.subplots(figsize=(SIZE / DPI, SIZE / DPI), dpi=DPI)
    fig.subplots adjust(left=0, right=1, top=1, bottom=0)
    ax.set facecolor("white")
    ax.set xlim(-5, 105)
    ax.set ylim(-5, 105)
    ax.set aspect("equal")
    ax.axis("off")
    return fig, ax


def save(fig, name):
    jpg path = JPG DIR / f"{name} {DATE}.jpg"
    svg path = SVG DIR / f"{name} {DATE}.svg"
    fig.savefig(jpg path, dpi=DPI, pad inches=0, facecolor="white")
    fig.savefig(svg path, format="svg", pad inches=0, facecolor="white")
    plt.close(fig)
    print(f"Tersimpan: {jpg path} | {svg path}")


def nested rotating squares counter():
    """Tweak: rotation direction flips every ring, so squares cross instead of nest"""
    fig, ax = setup ax()
    cx, cy = 50, 50
    n squares = 30
    corners = [(-1, -1), (1, -1), (1, 1), (-1, 1)]
    for i in range(n squares):
        size = 2 + i * 1.3
        angle = (i * 5.0) * (1 if i % 2 == 0 else -1)
        rad = np.radians(angle)
        xs, ys = [], []
        for dx, dy in corners:
            rx = dx * size * np.cos(rad) - dy * size * np.sin(rad)
            ry = dx * size * np.sin(rad) + dy * size * np.cos(rad)
            xs.append(cx + rx)
            ys.append(cy + ry)
        xs.append(xs[0])
        ys.append(ys[0])
        lw = 1.0 + 2.0 * (i / n squares)
        ax.plot(xs, ys, color="black", linewidth=lw)
    save(fig, "abstract nested rotating squares counter pattern black white geometric texture")


if   name   == "  main  ":
    nested rotating squares counter()
