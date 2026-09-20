import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import (
    Arc, Circle, Ellipse, FancyBboxPatch, Polygon, RegularPolygon, Rectangle, PathPatch,
)
from matplotlib.path import Path as MplPath
from matplotlib.transforms import Affine2D
from pathlib import Path
from datetime import datetime

# Konfigurasi Output
SIZE = 4000
DPI = 300
DATE = datetime.now().strftime("%d%m%Y")

# Manajemen Direktori
SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR.parent / "output"
JPG_DIR = OUTPUT_DIR / "jpg"
SVG_DIR = OUTPUT_DIR / "svg"
JPG_DIR.mkdir(parents=True, exist_ok=True)
SVG_DIR.mkdir(parents=True, exist_ok=True)


def setup_ax():
    """Inisialisasi koordinat axis (off, aspect equal, background putih)."""
    fig, ax = plt.subplots(figsize=(SIZE / DPI, SIZE / DPI), dpi=DPI)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.set_facecolor("white")
    # Rentang kanvas dasar (0-100), offset x/y agar simetris di tengah
    ax.set_xlim(-5, 105)
    ax.set_ylim(-5, 105)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def save(fig, name):
    """Menyimpan gambar dalam format JPG dan SVG."""
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


def squircle(cx, cy, rx, ry, p, n=80):
    """Menghitung koordinat poligon Superellipse/Squircle."""
    t = np.linspace(0, 2 * np.pi, n)
    ct, st = np.cos(t), np.sin(t)
    x = cx + rx * np.sign(ct) * (np.abs(ct) ** (2 / p))
    y = cy + ry * np.sign(st) * (np.abs(st) ** (2 / p))
    return x, y


def draw():
    """Generasi pola Squircle pada kisi Heksagonal dengan eksponen Checkerboard."""
    fig, ax = setup_ax()
    r0 = 6.4
    dx = r0 * np.sqrt(3)  # Jarak antar-kolom (jarak horizontal antar pusat heksagon)
    dy = r0 * 1.5  # Jarak antar-baris (jarak vertikal antar baris)

    # Rentang grid (13x13)
    rows, cols = 13, 13

    # Perhitungan offset untuk memposisikan grid simetris di tengah kanvas (50, 50)
    # Total lebar dan tinggi grid fisik
    total_w = (cols - 1) * dx + (dx / 2.0)  # Menghitung offset baris ganjil
    total_h = (rows - 1) * dy

    offset_x = 50.0 - (total_w / 2.0)
    offset_y = 50.0 - (total_h / 2.0)

    for row in range(rows):
        for col in range(cols):
            # Posisi x dengan offset baris heksagonal
            cx = col * dx + offset_x
            if row % 2:
                cx += dx / 2.0

            # Posisi y
            cy = row * dy + offset_y

            # Eksponen squircle (checkerboard pattern)
            p = 2.1 if (row + col) % 2 == 0 else 6.5

            # Radii squircle dengan variasi sinusoidal dinamis
            rx = r0 * (0.78 + 0.12 * np.sin(col * 0.4))
            ry = r0 * (0.78 + 0.12 * np.cos(row * 0.4))

            # Squircle Luar
            xs, ys = squircle(cx, cy, rx, ry, p, 120)
            ax.plot(xs, ys, color="black", linewidth=1.15)

            # Squircle Dalam
            xs2, ys2 = squircle(cx, cy, rx * 0.52, ry * 0.52, p, 80)
            ax.plot(xs2, ys2, color="black", linewidth=0.55)

    # Perhitungan ulang pad tampilan agar simetris penuh (jarak r0 eksternal)
    view_pad = (total_h / 2.0) + r0 * 0.6  # r0 * 0.6 memberikan margin kecil
    fit_view(ax, pad=view_pad)

    save(fig, "abstract grid tessellation hexagonal squircle exponent checkerboard pattern black white texture")


if __name__ == "__main__":
    draw()