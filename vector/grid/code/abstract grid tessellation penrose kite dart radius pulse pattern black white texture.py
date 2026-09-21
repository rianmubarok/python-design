import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from pathlib import Path
from datetime import datetime

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


def draw():
    """Connected Penrose Kite & Dart Star/Sun tiling with 5-fold radial symmetry."""
    fig, ax = setup_ax()

    golden = (1 + np.sqrt(5)) / 2  # Rasio Emas Phi (~1.618)
    scale = 8.0

    # Titik sudut dasar Kite dan Dart presisi berdasarkan Golden Ratio
    # Angle unit 36 deg = pi / 5
    def get_kite_vertices(center, r, angle_offset):
        # Vertex: tip, right, base, left
        angles = np.array([0, 1, 2, -1]) * (np.pi / 5) + angle_offset
        dists = np.array([r * golden, r, r / golden, r])
        pts = np.column_stack([dists * np.cos(angles), dists * np.sin(angles)])
        return pts + center

    def get_dart_vertices(center, r, angle_offset):
        # Vertex: tip, right, inner_indent, left
        angles = np.array([0, 1, 0, -1]) * (np.pi / 5) + angle_offset
        dists = np.array([r * golden, r, r * (golden - 0.618), r])
        pts = np.column_stack([dists * np.cos(angles), dists * np.sin(angles)])
        return pts + center

    # Generasi Bintang Penrose Terhubung (Radial Ring Extension)
    n_rings = 5
    center = np.array([0.0, 0.0])

    for ring in range(1, n_rings + 1):
        r_curr = ring * scale
        pulse = 1.0 + 0.12 * np.sin(ring * 0.8)  # Pulse modulasi radius
        
        n_sectors = 10 * ring
        for i in range(n_sectors):
            ang = i * (2 * np.pi / n_sectors)
            pos = center + np.array([np.cos(ang), np.sin(ang)]) * r_curr * pulse

            # Alternasi Kite dan Dart secara terstruktur untuk membentuk teselasi
            if (i + ring) % 2 == 0:
                pts = get_kite_vertices(pos, scale * 0.45 * pulse, ang)
                ax.add_patch(
                    Polygon(
                        pts,
                        closed=True,
                        facecolor="white",
                        edgecolor="black",
                        linewidth=0.9,
                        zorder=2,
                    )
                )
            else:
                pts = get_dart_vertices(pos, scale * 0.45 * pulse, ang + np.pi / 5)
                ax.add_patch(
                    Polygon(
                        pts,
                        closed=True,
                        facecolor="black",
                        edgecolor="black",
                        linewidth=0.5,
                        zorder=2,
                    )
                )

    # Tangkapan area tengah simetris penuh
    pad = 32.0
    ax.set_xlim(-pad, pad)
    ax.set_ylim(-pad, pad)

    save(
        fig,
        "abstract grid tessellation penrose kite dart radius pulse pattern black white texture",
    )


if __name__ == "__main__":
    draw()