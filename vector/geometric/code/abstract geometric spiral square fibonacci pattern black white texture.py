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


def spiral square fibonacci():
    """Spiral Fibonacci dengan susunan persegi presisi dan kurva spiral emas kontinu yang menyatu sempurna."""
    fig, ax = setup ax()

    # Urutan Fibonacci
    fib = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]

    min x, max x = 0.0, 1.0
    min y, max y = 0.0, 1.0

    # S0: Persegi Pertama (1x1)
    squares = [(0.0, 0.0, 1.0, 1.0, 1.0, np.pi, 1.5 * np.pi)]

    # Penempelan berurutan: RIGHT -> TOP -> LEFT -> BOTTOM
    for i in range(1, len(fib)):
        s = float(fib[i])
        mod = i % 4
        if mod == 1:  # RIGHT
            bx, by = max x, min y
            arc cx, arc cy = max x, max y
            t1, t2 = 1.5 * np.pi, 2.0 * np.pi
            max x += s
        elif mod == 2:  # TOP
            bx, by = min x, max y
            arc cx, arc cy = min x, max y
            t1, t2 = 0.0, 0.5 * np.pi
            max y += s
        elif mod == 3:  # LEFT
            bx, by = min x - s, min y
            arc cx, arc cy = min x, min y
            t1, t2 = 0.5 * np.pi, np.pi
            min x -= s
        elif mod == 0:  # BOTTOM
            bx, by = min x, min y - s
            arc cx, arc cy = max x, min y
            t1, t2 = np.pi, 1.5 * np.pi
            min y -= s
        squares.append((bx, by, s, arc cx, arc cy, t1, t2))

    # 1. Gambar Kotak-Kotak Persegi Fibonacci
    for idx, (bx, by, s, arc cx, arc cy, t1, t2) in enumerate(squares):
        square x = [bx, bx + s, bx + s, bx, bx]
        square y = [by, by, by + s, by + s, by]
        ax.plot(
            square x,
            square y,
            color="black",
            linewidth=1.2,
            solid capstyle="round",
            zorder=1,
        )

    # 2. Gambar Kurva Busur Spiral Emas Kontinu
    for idx, (bx, by, s, arc cx, arc cy, t1, t2) in enumerate(squares):
        t = np.linspace(t1, t2, 100)
        arc x = arc cx + s * np.cos(t)
        arc y = arc cy + s * np.sin(t)
        ax.plot(
            arc x,
            arc y,
            color="black",
            linewidth=2.8,
            solid capstyle="round",
            zorder=2,
        )

    # Memfokuskan tampilan simetris tepat di tengah kanvas
    center x = (min x + max x) / 2.0
    center y = (min y + max y) / 2.0
    width = max x - min x
    height = max y - min y
    pad = max(width, height) / 2.0 * 1.08

    ax.set xlim(center x - pad, center x + pad)
    ax.set ylim(center y - pad, center y + pad)

    save(fig, "abstract geometric spiral square fibonacci pattern black white texture"))


if   name   == "  main  ":
    spiral square fibonacci()