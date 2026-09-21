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
def tessellation():
    fig, ax = setup ax()
    size = 8
    h = size * np.sqrt(3) / 2
    for row in range(-1, 15):
        for col in range(-1, 15):
            x = col * size + (row % 2) * size / 2
            y = row * h
            if (row + col) % 2 == 0:
                triangle = [(x, y), (x + size, y), (x + size / 2, y + h)]
            else:
                triangle = [(x, y + h), (x + size, y + h), (x + size / 2, y)]
            xs = [p[0] for p in triangle] + [triangle[0][0]]
            ys = [p[1] for p in triangle] + [triangle[0][1]]
            ax.plot(xs, ys, color="black", linewidth=0.8)
    save(fig, "abstract tessellation triangle pattern black white geometric texture"))


if   name   == "  main  ":
    tessellation()
