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


def fit_view(ax, pad=48):
    """Memfokuskan tampilan simetris tepat di tengah kanvas (50, 50)."""
    ax.set_xlim(50 - pad, 50 + pad)
    ax.set_ylim(50 - pad, 50 + pad)


def draw():
    """Cairo pentagon cells fused with inner 8-point stars and a scale checker."""
    fig, ax = setup_ax()

    a = 12.0
    rows, cols = 12, 12

    # Menghitung offset kisi agar pusat pola berada tepat di (50, 50)
    grid_w = cols * a
    grid_h = rows * a
    offset_x = 50.0 - (grid_w / 2.0)
    offset_y = 50.0 - (grid_h / 2.0)

    for r in range(-1, rows + 1):
        for c in range(-1, cols + 1):
            s = a * (0.9 if (r + c) % 2 else 1.05)
            cx = c * a + offset_x
            cy = r * a + offset_y

            # Poligon Pentagon Cairo
            pts = np.array([
                [cx, cy + s * 0.08],
                [cx + s * 0.5, cy - s * 0.18],
                [cx + s, cy + s * 0.08],
                [cx + s * 0.72, cy + s * 0.95],
                [cx + s * 0.28, cy + s * 0.95],
            ])
            ax.add_patch(
                Polygon(
                    pts,
                    fill=False,
                    edgecolor="black",
                    linewidth=1.15,
                    zorder=1,
                )
            )

            # Bintang 8 Sudut di Dalam
            mid = pts.mean(axis=0)
            rr = s * 0.22
            angs = np.deg2rad(np.arange(0, 360, 45) + 10 * (r - c))

            # Lapisan Bintang Luar
            star_outer = np.column_stack([
                mid[0] + rr * np.cos(angs),
                mid[1] + rr * np.sin(angs),
            ])
            ax.add_patch(
                Polygon(
                    star_outer,
                    closed=True,
                    fill=False,
                    edgecolor="black",
                    linewidth=0.7,
                    zorder=2,
                )
            )

            # Lapisan Bintang Dalam
            star_inner = np.column_stack([
                mid[0] + rr * 0.55 * np.cos(angs + np.pi / 8),
                mid[1] + rr * 0.55 * np.sin(angs + np.pi / 8),
            ])
            ax.add_patch(
                Polygon(
                    star_inner,
                    closed=True,
                    fill=False,
                    edgecolor="black",
                    linewidth=0.45,
                    zorder=2,
                )
            )

    fit_view(ax, pad=48)
    save(
        fig,
        "abstract grid tessellation cairo pentagon islamic star fusion pattern black white texture",
    )


if __name__ == "__main__":
    draw()