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
def labyrinth():
    fig, ax = setup ax()
    cell size = 5
    rows = 20
    cols = 20
    np.random.seed(SEED)
    for r in range(rows):
        for c in range(cols):
            x = c * cell size
            y = r * cell size
            if np.random.random() > 0.5:
                ax.plot([x, x + cell size], [y, y], color="black", linewidth=1.2)
            if np.random.random() > 0.5:
                ax.plot([x, x], [y, y + cell size], color="black", linewidth=1.2)
            if np.random.random() > 0.3:
                ax.plot([x + cell size, x + cell size], [y, y + cell size], color="black", linewidth=1.2)
            if np.random.random() > 0.3:
                ax.plot([x, x + cell size], [y + cell size, y + cell size], color="black", linewidth=1.2)
    save(fig, "labyrinth")


if   name   == "  main  ":
    labyrinth()
