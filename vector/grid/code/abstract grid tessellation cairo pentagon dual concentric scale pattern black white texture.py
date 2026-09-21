from datetime import datetime
from pathlib import Path
from matplotlib.patches import Polygon
import matplotlib.pyplot as plt
import numpy as np
import matplotlib

matplotlib.use("Agg")

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


def scale_polygon_local(poly, factor):
    """Menghitung skala poligon secara lokal terhadap titik pusat geometri poligon itu sendiri."""
    centroid = poly.mean(axis=0)
    return (poly - centroid) * factor + centroid


def draw():
    """True interlocking Cairo pentagon tessellation with dual concentric outlines."""
    fig, ax = setup_ax()

    # Parameter Geometri Dasar
    s = 10.0  # Panjang rusuk dasar
    L1 = s
    L2 = s * (np.sqrt(3) - 1.0) / 2.0

    grid_width = 12
    grid_height = 12

    center_x = (grid_width - 1) * (L1 + L2) / 2.0
    center_y = (grid_height - 1) * (L1 + L2) / 2.0

    # Poligon Geometri Unit Cairo (2 Pentagons)
    p0 = np.array([
        [0, 0],
        [L1, 0],
        [L1 + L2, L2],
        [L1 / 2 + L2, L1 / 2 + L2],
        [-L1 / 2, L1 / 2],
    ])
    p1 = np.array([
        [0, 0],
        [0, L1],
        [L2, L1 + L2],
        [L1 / 2 + L2, L1 / 2 + L2],
        [L1 / 2, -L1 / 2],
    ])

    # Versi skala lokal (inner/outer concentric)
    p0_scaled = scale_polygon_local(p0, 0.85)
    p1_scaled = scale_polygon_local(p1, 0.85)

    p0_rot = np.column_stack([p0[:, 1], p0[:, 0]])
    p1_rot = np.column_stack([p1[:, 1], p1[:, 0]])
    p0_rot_scaled = scale_polygon_local(p0_rot, 0.85)
    p1_rot_scaled = scale_polygon_local(p1_rot, 0.85)

    for row in range(-1, grid_height + 1):
        for col in range(-1, grid_width + 1):
            cx = col * (L1 + L2)
            cy = row * (L1 + L2)

            tile_type = (row + col) % 2

            if tile_type == 0:
                # Type A: Pentagon Vertikal + Kontur Konsentris Lokal
                ax.add_patch(
                    Polygon(
                        p0 + [cx, cy],
                        closed=True,
                        fill=False,
                        edgecolor="black",
                        linewidth=1.2,
                        zorder=2,
                    )
                )
                ax.add_patch(
                    Polygon(
                        p0_scaled + [cx, cy],
                        closed=True,
                        fill=False,
                        edgecolor="black",
                        linewidth=0.8,
                        zorder=2,
                    )
                )

                ax.add_patch(
                    Polygon(
                        p1 + [cx, cy],
                        closed=True,
                        fill=False,
                        edgecolor="black",
                        linewidth=1.2,
                        zorder=2,
                    )
                )
                ax.add_patch(
                    Polygon(
                        p1_scaled + [cx, cy],
                        closed=True,
                        fill=False,
                        edgecolor="black",
                        linewidth=0.8,
                        zorder=2,
                    )
                )

            else:
                # Type B: Pentagon Horizontal + Kontur Konsentris Lokal
                ax.add_patch(
                    Polygon(
                        p1_rot + [cx, cy],
                        closed=True,
                        fill=False,
                        edgecolor="black",
                        linewidth=1.2,
                        zorder=2,
                    )
                )
                ax.add_patch(
                    Polygon(
                        p1_rot_scaled + [cx, cy],
                        closed=True,
                        fill=False,
                        edgecolor="black",
                        linewidth=0.8,
                        zorder=2,
                    )
                )

                ax.add_patch(
                    Polygon(
                        p0_rot + [cx, cy],
                        closed=True,
                        fill=False,
                        edgecolor="black",
                        linewidth=1.2,
                        zorder=2,
                    )
                )
                ax.add_patch(
                    Polygon(
                        p0_rot_scaled + [cx, cy],
                        closed=True,
                        fill=False,
                        edgecolor="black",
                        linewidth=0.8,
                        zorder=2,
                    )
                )

            # Aksen Garis Dalam (Inner Weave)
            acc_acc = np.array([
                [cx + L1 / 2, cy + L1 / 2],
                [cx + L1 / 2 + L2, cy + L1 / 2 + L2],
            ])
            ax.plot(
                acc_acc[:, 0],
                acc_acc[:, 1],
                color="black",
                linewidth=0.8,
                zorder=3,
            )

    # Tangkapan area tengah simetris penuh
    pad = 36.0
    ax.set_xlim(center_x - pad, center_x + pad)
    ax.set_ylim(center_y - pad, center_y + pad)

    save(
        fig,
        "abstract grid tessellation cairo pentagon dual concentric scale pattern black white texture",
    )


if __name__ == "__main__":
    draw()