from datetime import datetime
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import matplotlib

matplotlib.use("Agg")

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


def draw polygon(cx, cy, radius, sides, rotation=0):
    """Menghitung koordinat poligon dengan jumlah sisi tertentu."""
    angles = np.linspace(0, 2 * np.pi, sides + 1) + rotation
    x = cx + radius * np.cos(angles)
    y = cy + radius * np.sin(angles)
    return x, y


def polygon morphing chain():
    """Rantai poligon morphing yang tersusun rapi, padat, dan teratur."""
    fig, ax = setup ax()

    # Tiga rantai sejajar dengan offset sinusoidal yang tidak saling bertabrakan
    chains config = [
        {"y base": 70.0, "freq": 2.0, "amp": 12.0, "start sides": 3, "end sides": 16},
        {"y base": 50.0, "freq": 2.0, "amp": -12.0, "start sides": 4, "end sides": 18},
        {"y base": 30.0, "freq": 2.0, "amp": 12.0, "start sides": 3, "end sides": 20},
    ]

    n polygons = 22

    for config in chains config:
        chain points = []
        for i in range(n polygons):
            t = i / (n polygons - 1)
            x = 10.0 + t * 80.0
            y = config["y base"] + config["amp"] * np.sin(t * np.pi * config["freq"])
            chain points.append((x, y))

        for i, (cx, cy) in enumerate(chain points):
            progress = i / (n polygons - 1)
            sides = int(config["start sides"] + progress * (config["end sides"] - config["start sides"]))
            radius = 3.2 + 2.5 * np.sin(progress * np.pi)
            rotation = progress * np.pi * 2.5

            x poly, y poly = draw polygon(cx, cy, radius, sides, rotation)
            lw = 0.8 + 1.0 * progress

            ax.plot(
                x poly,
                y poly,
                color="black",
                linewidth=lw,
                solid capstyle="round",
                zorder=2,
            )

            # Garis penghubung antar-pusat poligon
            if i < n polygons - 1:
                next cx, next cy = chain points[i + 1]
                ax.plot(
                    [cx, next cx],
                    [cy, next cy],
                    color="black",
                    linewidth=0.4,
                    linestyle=(0, (3, 3)),
                    zorder=1,
                )

    # Framing simetris terpusat
    pad = 42.0
    ax.set xlim(50 - pad, 50 + pad)
    ax.set ylim(50 - pad, 50 + pad)

    save(fig, "polygon morphing chain")


if   name   == "  main  ":
    polygon morphing chain()