from datetime import datetime
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import matplotlib

matplotlib.use("Agg")

SIZE = 4000
DPI = 300
DATE = datetime.now().strftime("%d%m%Y")

SCRIPT DIR = Path(  file  ).resolve().parent
OUTPUT DIR = SCRIPT DIR.parent / "output"
JPG DIR = OUTPUT DIR / "jpg"
SVG DIR = OUTPUT DIR / "svg"
JPG DIR.mkdir(parents=True, exist ok=True)
SVG DIR.mkdir(parents=True, exist ok=True)


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


def draw hexagon(cx, cy, size, rotation=0.0):
    """Menggambar heksagon beraturan presisi."""
    angles = np.linspace(0, 2 * np.pi, 7) + rotation
    x = cx + size * np.cos(angles)
    y = cy + size * np.sin(angles)
    return x, y


def hexagon spiral twist morph():
    """Heksagon spiral dengan rotasi bertahap, ukuran melipat, dan framing terpusat."""
    fig, ax = setup ax()

    cx, cy = 50.0, 50.0
    n hexagons = 90
    spiral turns = 4.5

    min x, max x = cx, cx
    min y, max y = cy, cy

    for i in range(n hexagons):
        t = i / n hexagons
        angle = t * spiral turns * 2 * np.pi
        radius = 1.5 + 38.0 * (t ** 1.1)

        hex x = cx + radius * np.cos(angle)
        hex y = cy + radius * np.sin(angle)

        # Ukuran heksagon membesar dari pusat ke luar
        hex size = 1.2 + 4.5 * t

        # Rotasi (twist) berdasarkan posisi spiral
        twist = angle * 0.75 + t * np.pi

        x hex, y hex = draw hexagon(hex x, hex y, hex size, rotation=twist)

        # Melacak area bounding box untuk framing
        min x, max x = min(min x, x hex.min()), max(max x, x hex.max())
        min y, max y = min(min y, y hex.min()), max(max y, y hex.max())

        # Ketebalan garis menyesuaikan posisi spiral
        lw = max(0.5, 2.0 - 1.2 * t)
        ax.plot(x hex, y hex, color="black", linewidth=lw, solid capstyle="round", zorder=2)

    # Framing simetris terpusat di tengah kanvas
    cx final = (min x + max x) / 2.0
    cy final = (min y + max y) / 2.0
    w = max x - min x
    h = max y - min y
    pad = max(w, h) / 2.0 + 3.0

    ax.set xlim(cx final - pad, cx final + pad)
    ax.set ylim(cy final - pad, cy final + pad)

    save(fig, "hexagon spiral twist morph")


if   name   == "  main  ":
    hexagon spiral twist morph()