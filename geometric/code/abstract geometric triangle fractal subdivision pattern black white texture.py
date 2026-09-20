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


def subdivide triangle(p1, p2, p3, depth, max depth, ax):
    """Subdivisi rekursif segitiga Sierpinski dengan bobot garis yang proporsional."""
    if depth >= max depth:
        return

    # Hitung titik tengah setiap sisi
    mid12 = ((p1[0] + p2[0]) / 2.0, (p1[1] + p2[1]) / 2.0)
    mid23 = ((p2[0] + p3[0]) / 2.0, (p2[1] + p3[1]) / 2.0)
    mid31 = ((p3[0] + p1[0]) / 2.0, (p3[1] + p1[1]) / 2.0)

    lw = max(0.4, 1.8 - depth * 0.3)

    # Plot segitiga tengah yang terbalik
    triangle x = [mid12[0], mid23[0], mid31[0], mid12[0]]
    triangle y = [mid12[1], mid23[1], mid31[1], mid12[1]]

    ax.plot(
        triangle x,
        triangle y,
        color="black",
        linewidth=lw,
        solid capstyle="round",
        zorder=2,
    )

    # Rekursi ke 3 segitiga di sudut
    subdivide triangle(p1, mid12, mid31, depth + 1, max depth, ax)
    subdivide triangle(mid12, p2, mid23, depth + 1, max depth, ax)
    subdivide triangle(mid31, mid23, p3, depth + 1, max depth, ax)


def triangle fractal subdivision():
    """Teselasi segitiga fraktal yang tersusun rapi, simetris, dan terpusat."""
    fig, ax = setup ax()

    # Struktur Hexagram / Triforce simetris yang saling menyambung tanpa tumpang tindih
    cx, cy = 50.0, 50.0
    side = 70.0
    h = side * np.sqrt(3) / 2.0

    # Segitiga Utama Besar (Hadap Atas)
    p1 = (cx, cy + (2 / 3) * h)
    p2 = (cx - side / 2.0, cy - (1 / 3) * h)
    p3 = (cx + side / 2.0, cy - (1 / 3) * h)

    # Garis tepi segitiga utama
    ax.plot(
        [p1[0], p2[0], p3[0], p1[0]],
        [p1[1], p2[1], p3[1], p1[1]],
        color="black",
        linewidth=2.2,
        solid capstyle="round",
        zorder=1,
    )

    # Jalankan subdivisi fraktal hingga kedalaman 5
    subdivide triangle(p1, p2, p3, 0, 5, ax)

    # Atur tampilan simetris tepat di tengah kanvas
    pad = 42.0
    ax.set xlim(50 - pad, 50 + pad)
    ax.set ylim(50 - pad, 50 + pad)

    save(fig, "abstract geometric triangle fractal subdivision pattern black white texture"))


if   name   == "  main  ":
    triangle fractal subdivision()