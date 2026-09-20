import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime

SIZE = 4000
DPI = 300
SEED = 42
DATE = datetime.now().strftime("%d%m%Y")

JPG DIR = Path("output/jpg")
SVG DIR = Path("output/svg")
JPG DIR.mkdir(parents=True, exist ok=True)
SVG DIR.mkdir(parents=True, exist ok=True)

np.random.seed(SEED)


def setup ax():
    fig, ax = plt.subplots(figsize=(SIZE/DPI, SIZE/DPI), dpi=DPI)
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
def nested rotating squares():
    fig, ax = setup ax()
    cx, cy = 50, 50
    n squares = 30
    for i in range(n squares):
        size = 2 + i * 2.5
        angle = i * 5
        rad = np.radians(angle)
        corners = [(-1, -1), (1, -1), (1, 1), (-1, 1)]
        xs = []
        ys = []
        for dx, dy in corners:
            rx = dx * size * np.cos(rad) - dy * size * np.sin(rad)
            ry = dx * size * np.sin(rad) + dy * size * np.cos(rad)
            xs.append(cx + rx)
            ys.append(cy + ry)
        xs.append(xs[0])
        ys.append(ys[0])
        lw = 1.0 + 2.0 * (i / n squares)
        ax.plot(xs, ys, color="black", linewidth=lw)
    save(fig, "nested rotating squares")


if   name   == "  main  ":
    nested rotating squares()
