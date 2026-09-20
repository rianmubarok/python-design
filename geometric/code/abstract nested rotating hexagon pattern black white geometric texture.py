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


def nested rotating hexagon():
    """Wild combo: nested rotating squares x hexagonal tessellation, spun into a rosette"""
    fig, ax = setup ax()
    cx, cy = 50, 50
    n hex = 30
    for i in range(n hex):
        t = i / (n hex - 1)
        r = 3 + i * 1.7
        ang = np.radians(i * 4.0) + np.arange(7) * (2 * np.pi / 6)
        xs = cx + r * np.cos(ang)
        ys = cy + r * np.sin(ang)
        lw = 1.0 + 2.0 * t
        ax.plot(xs, ys, color="black", linewidth=lw)
    save(fig, "abstract nested rotating hexagon pattern black white geometric texture")


if   name   == "  main  ":
    nested rotating hexagon()
