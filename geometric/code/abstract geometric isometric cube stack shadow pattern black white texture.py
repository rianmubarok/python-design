from datetime import datetime
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon
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


def isometric cube stack shadow():
    """Tumpukan kubus isometrik 3D presisi dengan shading 3-tonal yang bersih."""
    fig, ax = setup ax()

    cols, rows = 14, 14
    S = 4.0
    cos30 = np.cos(np.pi / 6)
    sin30 = np.sin(np.pi / 6)

    def project(x, y, z=0.0):
        return (x - y) * cos30, (x + y) * sin30 + z

    # Kumpulkan seluruh kolom kubus
    columns = []
    for i in range(cols):
        for j in range(rows):
            dist = np.sqrt((i - cols / 2.0) ** 2 + (j - rows / 2.0) ** 2)
            H = 2.0 + 3.0 * (0.5 + 0.5 * np.sin(0.4 * dist))
            depth = i + j
            columns.append((depth, i, j, H))

    # Urutkan secara presisi dari belakang (depth terkecil) ke depan (depth terbesar)
    columns.sort(key=lambda c: (c[0], c[1], c[2]))

    all 2d points = []

    for idx, (depth, i, j, H) in enumerate(columns):
        x0, y0 = i * S, j * S

        # Koordinat Proyeksi 3D Kubus
        P0 = project(x0, y0, 0.0)
        P1 = project(x0 + S, y0, 0.0)
        P2 = project(x0 + S, y0 + S, 0.0)
        P3 = project(x0, y0 + S, 0.0)

        T0 = project(x0, y0, H)
        T1 = project(x0 + S, y0, H)
        T2 = project(x0 + S, y0 + S, H)
        T3 = project(x0, y0 + S, H)

        all 2d points.extend([P0, P1, P2, P3, T0, T1, T2, T3])

        z base = idx * 5

        # 1. Sisi Kanan (Right Face) - Shadow Sedang
        right poly = [P0, P1, T1, T0]
        ax.add patch(
            Polygon(
                right poly,
                closed=True,
                facecolor="#B0B0B0",
                edgecolor="black",
                linewidth=1.0,
                zorder=z base + 1,
            )
        )

        # 2. Sisi Kiri (Left Face) - Terang Sedang
        left poly = [P0, P3, T3, T0]
        ax.add patch(
            Polygon(
                left poly,
                closed=True,
                facecolor="#E0E0E0",
                edgecolor="black",
                linewidth=1.0,
                zorder=z base + 2,
            )
        )

        # 3. Sisi Atas (Top Face) - Terang Murni
        top poly = [T0, T1, T2, T3]
        ax.add patch(
            Polygon(
                top poly,
                closed=True,
                facecolor="#FFFFFF",
                edgecolor="black",
                linewidth=1.0,
                zorder=z base + 3,
            )
        )

    # Framing simetris terpusat penuh
    pts = np.array(all 2d points)
    min x, max x = pts[:, 0].min(), pts[:, 0].max()
    min y, max y = pts[:, 1].min(), pts[:, 1].max()

    center x = (min x + max x) / 2.0
    center y = (min y + max y) / 2.0
    w = max x - min x
    h span = max y - min y
    pad = max(w, h span) / 2.0 + 4.0

    ax.set xlim(center x - pad, center x + pad)
    ax.set ylim(center y - pad, center y + pad)

    save(fig, "isometric cube stack shadow")


if   name   == "  main  ":
    isometric cube stack shadow()