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


def draw octagon(cx, cy, r):
    """Menggambar oktagon beraturan dengan jari-jari luar r."""
    angles = np.linspace(np.pi / 8, 2 * np.pi + np.pi / 8, 9)
    x = cx + r * np.cos(angles)
    y = cy + r * np.sin(angles)
    return x, y


def draw square(cx, cy, side):
    """Menggambar persegi sejajar sumbu dengan panjang sisi side."""
    h = side / 2.0
    x = [cx - h, cx + h, cx + h, cx - h, cx - h]
    y = [cy - h, cy - h, cy + h, cy + h, cy - h]
    return x, y


def octagon tessellation seamless():
    """Teselasi presisi segi delapan dan persegi yang saling mengunci (Truncated Square Tiling)."""
    fig, ax = setup ax()

    # Panjang sisi bersama antara oktagon dan persegi
    s = 6.0
    # Jarak antar-pusat oktagon yang presisi
    D = s * (1.0 + np.sqrt(2.0))
    # Jari-jari luar oktagon
    r oct = s / (2.0 * np.sin(np.pi / 8.0))

    cols, rows = 8, 8

    # Perhitungan offset untuk memposisikan teselasi simetris di tengah kanvas (50, 50)
    total w = (cols - 1) * D
    total h = (rows - 1) * D
    offset x = 50.0 - total w / 2.0
    offset y = 50.0 - total h / 2.0

    # 1. Gambar Oktagon pada setiap simpul kisi
    for r in range(rows):
        for c in range(cols):
            cx = offset x + c * D
            cy = offset y + r * D

            x oct, y oct = draw octagon(cx, cy, r oct)
            ax.plot(
                x oct,
                y oct,
                color="black",
                linewidth=1.2,
                solid capstyle="round",
                zorder=2,
            )

    # 2. Gambar Persegi pada persimpangan antar-oktagon
    for r in range(rows - 1):
        for c in range(cols - 1):
            sq cx = offset x + c * D + D / 2.0
            sq cy = offset y + r * D + D / 2.0

            x sq, y sq = draw square(sq cx, sq cy, s)
            ax.plot(
                x sq,
                y sq,
                color="black",
                linewidth=1.2,
                solid capstyle="round",
                zorder=2,
            )

    # Framing simetris terpusat penuh
    pad = (total w / 2.0) + r oct + 2.0
    ax.set xlim(50.0 - pad, 50.0 + pad)
    ax.set ylim(50.0 - pad, 50.0 + pad)

    save(fig, "octagon tessellation seamless")


if   name   == "  main  ":
    octagon tessellation seamless()