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


def herringbone amplitude gradient():
    """Tweak: chevron amplitude ramps left to right, flat ridges rising into tall peaks"""
    fig, ax = setup ax()
    spacing = 4.0
    for y in np.arange(-6, 106, spacing):
        for x in np.arange(-6, 106, spacing * 2):
            amp = 0.8 + 6.0 * ((x + 6) / 112)
            lw = 0.9 + 0.5 * ((x + 6) / 112)
            ax.plot([x, x + spacing], [y, y + amp], color="black", linewidth=lw)
            ax.plot([x + spacing, x + spacing * 2], [y + amp, y], color="black", linewidth=lw)
    save(fig, "abstract herringbone amplitude gradient pattern black white geometric texture")


if   name   == "  main  ":
    herringbone amplitude gradient()
