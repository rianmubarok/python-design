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


def draw star polygon(cx, cy, outer radius, inner radius, points, rotation=0):
    """Menghitung koordinat poligon bintang dengan sudut berselang-seling."""
    angles = []
    radii = []

    for i in range(points * 2):
        angle = rotation + i * np.pi / points
        radius = outer radius if i % 2 == 0 else inner radius
        angles.append(angle)
        radii.append(radius)

    angles.append(angles[0])
    radii.append(radii[0])

    x = [cx + r * np.cos(a) for r, a in zip(radii, angles)]
    y = [cy + r * np.sin(a) for r, a in zip(radii, angles)]

    return x, y


def star polygon rotation burst():
    """Teselasi ledakan bintang terpusat yang rapat, simetris, dan proporsional."""
    fig, ax = setup ax()

    cx, cy = 50.0, 50.0
    n rings = 9
    stars per ring = [1, 6, 12, 18, 24, 30, 36, 42, 48]  # Ditingkatkan agar lebih rapat

    for ring in range(n rings):
        n stars = stars per ring[ring]
        ring radius = ring * 5.2  # Dibuat lebih rapat dari 8.0

        for star idx in range(n stars):
            if ring == 0:
                star x, star y = cx, cy
                rotation = 0
                outer radius = 4.2
                inner radius = 2.1
                points = 8
            else:
                angle = 2 * np.pi * star idx / n stars
                star x = cx + ring radius * np.cos(angle)
                star y = cy + ring radius * np.sin(angle)
                rotation = angle + ring * np.pi / 6

                outer radius = 1.8 + ring * 0.35
                inner radius = outer radius * 0.42
                points = 5 + (ring % 3)

            x star, y star = draw star polygon(
                star x, star y, outer radius, inner radius, points, rotation
            )

            lw = max(0.5, 1.8 - ring * 0.12)

            if ring % 2 == 0:
                ax.plot(
                    x star,
                    y star,
                    color="black",
                    linewidth=lw,
                    solid capstyle="round",
                    zorder=2,
                )
            else:
                ax.plot(
                    x star,
                    y star,
                    color="black",
                    linewidth=lw,
                    linestyle=(0, (2, 1)),
                    solid capstyle="round",
                    zorder=2,
                )

    # Memfokuskan tampilan agar simetris dan seluruh bintang luar muat
    pad = 48.0
    ax.set xlim(50 - pad, 50 + pad)
    ax.set ylim(50 - pad, 50 + pad)

    save(fig, "star polygon rotation burst")


if   name   == "  main  ":
    star polygon rotation burst()