from datetime import datetime
from pathlib import Path
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


def rotate_point(x, y, cx, cy, angle):
    """Menerapkan rotasi 2D pada titik (x, y) terhadap pusat (cx, cy)."""
    tx, ty = x - cx, y - cy
    rx = tx * np.cos(angle) - ty * np.sin(angle)
    ry = tx * np.sin(angle) + ty * np.cos(angle)
    return cx + rx, cy + ry


def kaleidoscope_triangle_reflection():
    """Simetri Kaleidoskop Presisi Berbasis Refleksi Cermin Sektor."""
    fig, ax = setup_ax()

    cx, cy = 50.0, 50.0
    n_sectors = 12  # Simetri 12-lipat (12 sektor cermin)
    sector_angle = 2 * np.pi / n_sectors

    # 1. Definisikan Elemen-Elemen Elegan di Dalam 1 Sektor Acuan (0 hingga sector_angle)
    # Segitiga & Poligon Motif
    motif_polygons = []
    for i in range(4):
        r = 12.0 + i * 8.0
        ang = sector_angle * (0.2 + 0.6 * (i % 2))
        s = 2.5 + i * 0.8

        # Poligon kecil di dalam sektor acuan
        pts = np.array([
            [r * np.cos(ang), r * np.sin(ang)],
            [(r + s) * np.cos(ang + 0.05), (r + s) * np.sin(ang + 0.05)],
            [(r + s * 0.5) * np.cos(ang - 0.08), (r + s * 0.5) * np.sin(ang - 0.08)],
            [r * np.cos(ang), r * np.sin(ang)],
        ])
        motif_polygons.append(pts)

    # Garis-garis lengkung aksen motif
    motif_lines = []
    t = np.linspace(0.05 * sector_angle, 0.95 * sector_angle, 30)
    for r in [10.0, 22.0, 34.0, 42.0]:
        lx = r * np.cos(t)
        ly = r * np.sin(t)
        motif_lines.append(np.column_stack((lx, ly)))

    # 2. Replikasi Refleksi Cermin Kaleidoskop di Seluruh Sektor
    for k in range(n_sectors):
        base_angle = k * sector_angle

        for pts in motif_polygons:
            # Bentuk Asli Sektor (Rotasi)
            x_rot, y_rot = rotate_point(cx + pts[:, 0], cy + pts[:, 1], cx, cy, base_angle)
            ax.plot(x_rot, y_rot, color="black", linewidth=1.1, solid_capstyle="round")

            # Bentuk Cermin Sektor (Flip Y lalu Rotasi)
            x_flip, y_flip = rotate_point(cx + pts[:, 0], cy - pts[:, 1], cx, cy, base_angle + sector_angle)
            ax.plot(x_flip, y_flip, color="black", linewidth=1.1, solid_capstyle="round")

        for line in motif_lines:
            # Garis Lengkung Asli
            lx_rot, ly_rot = rotate_point(cx + line[:, 0], cy + line[:, 1], cx, cy, base_angle)
            ax.plot(lx_rot, ly_rot, color="black", linewidth=0.8, solid_capstyle="round")

            # Garis Lengkung Cermin
            lx_flip, ly_flip = rotate_point(cx + line[:, 0], cy - line[:, 1], cx, cy, base_angle + sector_angle)
            ax.plot(lx_flip, ly_flip, color="black", linewidth=0.8, solid_capstyle="round")

    # Framing simetris penuh di tengah
    pad = 46.0
    ax.set_xlim(50.0 - pad, 50.0 + pad)
    ax.set_ylim(50.0 - pad, 50.0 + pad)

    save(fig, "kaleidoscope triangle reflection")


if __name__ == "__main__":
    kaleidoscope_triangle_reflection()