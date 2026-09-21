from datetime import datetime
from pathlib import Path
import matplotlib.collections as collections
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np

SIZE = 4000
DPI = 300
DATE = datetime.now().strftime("%d%m%Y")

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR.parent / "output"
JPG_DIR = OUTPUT_DIR / "jpg"
SVG_DIR = OUTPUT_DIR / "svg"
JPG_DIR.mkdir(parents=True, exist_ok=True)
SVG_DIR.mkdir(parents=True, exist_ok=True)


def setup_ax():
    fig, ax = plt.subplots(figsize=(SIZE / DPI, SIZE / DPI), dpi=DPI)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.set_facecolor("white")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def save(fig, name):
    jpg_path = JPG_DIR / f"{name} {DATE}.jpg"
    svg_path = SVG_DIR / f"{name} {DATE}.svg"
    fig.savefig(jpg_path, dpi=DPI, pad_inches=0, facecolor="white")
    fig.savefig(svg_path, format="svg", pad_inches=0, facecolor="white")
    plt.close(fig)
    print(f"Tersimpan: {jpg_path} | {svg_path}")


def draw():
    """Printed Circuit Board Trace Routing.

    A grid of horizontal, vertical, and 45-degree traces connecting
    randomly placed square 'chips' and circular 'vias', simulating PCB
    routing.
    """
    fig, ax = setup_ax()
    rng = np.random.default_rng(42)

    grid_size = 20
    # Penyesuaian skala & offset agar seluruh elemen berada dalam batas koordinat (0-100)
    cell_size = 90.0 / grid_size
    offset = 5.0

    # Menempatkan node (chips/vias/pads)
    nodes = []
    for _ in range(30):
        r = rng.integers(1, grid_size - 1)
        c = rng.integers(1, grid_size - 1)
        if (r, c) not in nodes:
            nodes.append((r, c))

    segments = []
    for i in range(len(nodes) - 1):
        r1, c1 = nodes[i]
        # Menghubungkan ke node berikutnya secara berurutan agar alur jalur lebih teratur
        r2, c2 = nodes[i + 1]

        x1 = offset + c1 * cell_size
        y1 = offset + r1 * cell_size
        x2 = offset + c2 * cell_size
        y2 = offset + r2 * cell_size

        dx = x2 - x1
        dy = y2 - y1

        # Tracing 45/90 derajat yang presisi:
        # Garis bergerak secara diagonal terlebih dahulu, lalu disambung garis lurus tegak lurus
        if abs(dx) > abs(dy):
            x_mid = x1 + np.sign(dx) * abs(dy)
            y_mid = y2
        else:
            x_mid = x2
            y_mid = y1 + np.sign(dy) * abs(dx)

        segments.append([(x1, y1), (x_mid, y_mid)])
        segments.append([(x_mid, y_mid), (x2, y2)])

    # Menggambar garis jalur (traces)
    lc = collections.LineCollection(
        segments,
        linewidths=2.0,
        colors="black",
        capstyle="round",
        joinstyle="round",
    )
    ax.add_collection(lc)

    # Menggambar komponen (chips, vias, dan pads)
    for r, c in nodes:
        x = offset + c * cell_size
        y = offset + r * cell_size

        node_type = rng.choice(["via", "chip", "pad"])

        if node_type == "via":
            c1 = patches.Circle(
                (x, y),
                cell_size * 0.3,
                facecolor="white",
                edgecolor="black",
                linewidth=2.0,
                zorder=3,
            )
            ax.add_patch(c1)
        elif node_type == "chip":
            rect = patches.Rectangle(
                (x - cell_size * 0.4, y - cell_size * 0.4),
                cell_size * 0.8,
                cell_size * 0.8,
                facecolor="black",
                zorder=3,
            )
            ax.add_patch(rect)
        elif node_type == "pad":
            rect = patches.Rectangle(
                (x - cell_size * 0.3, y - cell_size * 0.3),
                cell_size * 0.6,
                cell_size * 0.6,
                facecolor="white",
                edgecolor="black",
                linewidth=2.0,
                zorder=3,
            )
            ax.add_patch(rect)

    save(
        fig,
        "abstract grid tessellation printed circuit board trace routing pattern black white texture",
    )


if __name__ == "__main__":
    draw()