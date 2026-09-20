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


def poincare_transform(x, y, R=40.0):
    """Memetakan titik koordinat ke dalam Poincaré Disk Model secara presisi."""
    r = np.hypot(x, y)
    if r == 0:
        return 0.0, 0.0
    r_transformed = R * (r / (R + r))
    theta = np.arctan2(y, x)
    return r_transformed * np.cos(theta), r_transformed * np.sin(theta)


def hyperbolic_tessellation_escher():
    """Teselasi Hiperbolik Escher tanpa garis batas lingkaran luar."""
    fig, ax = setup_ax()

    cx, cy = 50.0, 50.0
    disk_radius = 42.0

    # (Perintah gambar lingkaran batas luar telah dihapus dari sini)

    # Buat Kisi dasar bersarang (Nested Hexagonal / Star Lattice)
    n_rings = 10
    n_pts_per_ring = 6

    for ring in range(1, n_rings + 1):
        r_base = ring * 8.0
        n_polygons = ring * n_pts_per_ring

        for i in range(n_polygons):
            angle = 2 * np.pi * i / n_polygons
            bx = r_base * np.cos(angle)
            by = r_base * np.sin(angle)

            # Poligon lokal
            poly_sides = 6
            poly_size = 5.0 / (1.0 + 0.08 * r_base)
            poly_angles = np.linspace(0, 2 * np.pi, poly_sides + 1) + angle

            px = bx + poly_size * np.cos(poly_angles)
            py = by + poly_size * np.sin(poly_angles)

            # Peta setiap titik ke Poincaré Disk
            tx, ty = [], []
            for x_val, y_val in zip(px, py):
                hx, hy = poincare_transform(x_val, y_val, R=disk_radius)
                tx.append(cx + hx)
                ty.append(cy + hy)

            # Ketebalan garis menyesuaikan kedalaman kisi
            lw = max(0.4, 1.2 - ring * 0.08)
            ax.plot(tx, ty, color="black", linewidth=lw, solid_capstyle="round", zorder=2)

    # Framing simetris terpusat
    pad = disk_radius + 4.0
    ax.set_xlim(cx - pad, cx + pad)
    ax.set_ylim(cy - pad, cy + pad)

    save(fig, "hyperbolic tessellation escher")


if __name__ == "__main__":
    hyperbolic_tessellation_escher()