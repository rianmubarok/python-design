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


def diamond grid expanded sparse():
    """Teselasi belah ketupat dengan dimensi besar dan spasi lebar."""
    fig, ax = setup ax()

    # Dimensi belah ketupat yang diperbesar
    w = 12.0  # 2x lebih lebar dari aslinya (6.0)
    h = 16.0  # 2x lebih tinggi dari aslinya (8.0)

    cols = 12  # Lebih sedikit kolom
    rows = 12  # Lebih sedikit baris

    # Jarak kisi yang lebih longgar
    step x = w * 1.2  # 120% dari lebar untuk spasi ekstra
    step y = h / 2.0 * 1.3  # 130% dari tinggi setengah untuk spasi vertikal ekstra

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

            # Garis yang lebih tebal untuk bentuk yang diperbesar
            lw = 2.0 if r % 2 == 0 else 1.5
            ax.plot(x pts, y pts, color="black", linewidth=lw, solid capstyle="round")

            # Tambahkan titik pusat untuk aksen
            ax.plot(cx, cy, marker="o", markersize=1.5, color="black")

    # Framing simetris dengan padding lebih besar
    cx final = (min x + max x) / 2.0
    cy final = (min y + max y) / 2.0
    span w = max x - min x
    span h = max y - min y
    pad = max(span w, span h) / 2.0 + 5.0  # Padding lebih besar

    ax.set xlim(cx final - pad, cx final + pad)
    ax.set ylim(cy final - pad, cy final + pad)

    save(fig, "abstract geometric diamond grid expanded sparse pattern black white texture"))


if   name   == "  main  ":
    diamond grid expanded sparse()