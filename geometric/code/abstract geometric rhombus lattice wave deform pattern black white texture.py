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


def rhombus lattice wave deform():
    """Rhombus lattice pattern with seamless continuous sinusoidal wave deformation."""
    fig, ax = setup ax()

    # Parameter grid dasar
    rows, cols = 28, 28
    step x = 6.0
    step y = 5.0

    # 1. Buat matriks koordinat simpul (grid vertices)
    grid x = np.zeros((rows, cols))
    grid y = np.zeros((rows, cols))

    # Hitung posisi dasar dengan pergeseran selang-seling (staggered)
    for r in range(rows):
        for c in range(cols):
            bx = c * step x
            if r % 2 != 0:
                bx += step x * 0.5
            by = r * step y

            # 2. Terapkan deformasi gelombang global pada titik simpul
            wave x = 2.2 * np.sin(0.2 * by + 0.1 * bx)
            wave y = 1.8 * np.cos(0.25 * bx)

            grid x[r, c] = bx + wave x
            grid y[r, c] = by + wave y

    # Pusatkan grid ke titik (50, 50)
    center x = (grid x.min() + grid x.max()) / 2.0
    center y = (grid y.min() + grid y.max()) / 2.0
    grid x += 50.0 - center x
    grid y += 50.0 - center y

    # 3. Hubungkan titik simpul untuk membentuk belah ketupat tersambung (Interlocking)
    for r in range(rows - 1):
        for c in range(cols - 1):
            if r % 2 == 0:
                # Belah ketupat tipe A
                p1 = (grid x[r, c], grid y[r, c])
                p2 = (grid x[r, c + 1], grid y[r, c + 1])
                p3 = (grid x[r + 1, c], grid y[r + 1, c])
                p4 = (grid x[r + 1, c - 1], grid y[r + 1, c - 1]) if c > 0 else None
            else:
                # Belah ketupat tipe B
                p1 = (grid x[r, c], grid y[r, c])
                p2 = (grid x[r, c + 1], grid y[r, c + 1])
                p3 = (grid x[r + 1, c + 1], grid y[r + 1, c + 1])
                p4 = (grid x[r + 1, c], grid y[r + 1, c])

            # Gambar garis tepi belah ketupat
            if r % 2 == 0:
                poly x = [grid x[r, c], grid x[r, c + 1], grid x[r + 1, c + 1], grid x[r + 1, c], grid x[r, c]]
                poly y = [grid y[r, c], grid y[r, c + 1], grid y[r + 1, c + 1], grid y[r + 1, c], grid y[r, c]]
            else:
                poly x = [grid x[r, c], grid x[r, c + 1], grid x[r + 1, c + 1], grid x[r + 1, c], grid x[r, c]]
                poly y = [grid y[r, c], grid y[r, c + 1], grid y[r + 1, c + 1], grid y[r + 1, c], grid y[r, c]]

            ax.plot(poly x, poly y, color="black", linewidth=0.8, solid capstyle="round")

    # Framing simetris
    pad = 42.0
    ax.set xlim(50 - pad, 50 + pad)
    ax.set ylim(50 - pad, 50 + pad)

    save(fig, "rhombus lattice wave deform")


if   name   == "  main  ":
    rhombus lattice wave deform()