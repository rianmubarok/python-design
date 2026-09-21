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


def fit_view(ax, pad=50):
    """Memfokuskan tampilan simetris tepat di tengah kanvas (50, 50)."""
    ax.set_xlim(50 - pad, 50 + pad)
    ax.set_ylim(50 - pad, 50 + pad)


def draw():
    """Cairo pentagons with rounded vertices and a size pulse across the lattice."""
    fig, ax = setup_ax()
    a = 11.0
    rows, cols = 12, 12

    # Menghitung offset kisi agar pusat pola berada tepat di (50, 50)
    grid_w = (cols - 1) * a
    grid_h = (rows - 1) * a
    offset_x = 50.0 - (grid_w / 2.0)
    offset_y = 50.0 - (grid_h / 2.0)

    for r in range(-1, rows + 1):
        for c in range(-1, cols + 1):
            pulse = 0.78 + 0.22 * np.sin(c * 0.55) * np.cos(r * 0.45)
            s = a * pulse
            cx = c * a + offset_x
            cy = r * a + offset_y

            pts = np.array([
                [cx, cy],
                [cx + s * 0.52, cy - s * 0.22],
                [cx + s, cy],
                [cx + s * 0.74, cy + s * 0.92],
                [cx + s * 0.26, cy + s * 0.92],
            ])
            mid = pts.mean(axis=0)
            pts = mid + (pts - mid)

            # Pembulatan sudut via interpolasi fillet
            n = len(pts)
            curve = []
            for i in range(n):
                p0, p1, p2 = pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
                a0 = p0 * 0.25 + p1 * 0.75
                a1 = p1 * 0.75 + p2 * 0.25
                for t in np.linspace(0, 1, 8, endpoint=False):
                    curve.append((1 - t) * a0 + t * a1)

            poly = np.array(curve)

            # Outset / Garis Luar
            ax.add_patch(
                Polygon(
                    poly,
                    fill=False,
                    edgecolor="black",
                    linewidth=1.15,
                    zorder=1,
                )
            )

            # Inner Contour / Garis Dalam
            inner = mid + (poly - mid) * 0.55
            ax.add_patch(
                Polygon(
                    inner,
                    fill=False,
                    edgecolor="black",
                    linewidth=0.55,
                    zorder=2,
                )
            )

    fit_view(ax, pad=50)
    save(
        fig,
        "abstract grid tessellation cairo pentagonal rounded fillet pulse pattern black white texture",
    )


if __name__ == "__main__":
    draw()