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


def draw diamond(cx, cy, w, h):
    """Menggambar belah ketupat (diamond) berpusat di (cx, cy)."""
    x = [cx, cx + w / 2.0, cx, cx - w / 2.0, cx]
    y = [cy + h / 2.0, cy, cy - h / 2.0, cy, cy + h / 2.0]
    return x, y


def diamond grid compressed density():
    """Teselasi belah ketupat dengan kepadatan tinggi dan dimensi terkompresi."""
    fig, ax = setup ax()

    # Dimensi belah ketupat yang lebih kecil untuk kepadatan tinggi
    w = 4.0  # Lebih sempit dari aslinya (6.0)
    h = 5.0  # Lebih pendek dari aslinya (8.0)

    cols = 30  # Lebih banyak kolom
    rows = 30  # Lebih banyak baris

    # Jarak kisi yang lebih rapat
    step x = w * 0.9  # 90% dari lebar untuk tumpang tindih minimal
    step y = h / 2.0 * 0.85  # 85% dari tinggi setengah untuk kompresi vertikal

    min x, max x = float("inf"), float("-inf")
    min y, max y = float("inf"), float("-inf")

    for r in range(rows):
        for c in range(cols):
            cx = c * step x
            if r % 2 != 0:
                cx += step x / 2.0
            cy = r * step y

            x pts, y pts = draw diamond(cx, cy, w, h)

            min x, max x = min(min x, min(x pts)), max(max x, max(x pts))
            min y, max y = min(min y, min(y pts)), max(max y, max(y pts))

            # Variasi ketebalan garis yang lebih halus untuk kepadatan tinggi
            lw = 0.6 + 0.2 * (r % 3)  # Variasi subtil berdasarkan modulo 3
            ax.plot(x pts, y pts, color="black", linewidth=lw, solid capstyle="round")

    # Framing simetris dengan padding yang lebih ketat
    cx final = (min x + max x) / 2.0
    cy final = (min y + max y) / 2.0
    span w = max x - min x
    span h = max y - min y
    pad = max(span w, span h) / 2.0 + 1.0  # Padding minimal

    ax.set xlim(cx final - pad, cx final + pad)
    ax.set ylim(cy final - pad, cy final + pad)

    save(fig, "diamond grid compressed density")


if   name   == "  main  ":
    diamond grid compressed density()