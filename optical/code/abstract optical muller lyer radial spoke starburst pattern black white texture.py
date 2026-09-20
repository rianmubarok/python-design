import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime

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

np.random.seed(SEED)


def setup_ax():
    fig, ax = plt.subplots(figsize=(SIZE / DPI, SIZE / DPI), dpi=DPI)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.set_facecolor("white")
    ax.set_xlim(-50, 50)
    ax.set_ylim(-50, 50)
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


def draw_chevron(ax, x, y, ray_angle, is_inward, fin_len=4.5, fin_angle=np.radians(35)):
    """Menggambar sirip panah Müller-Lyer dengan sudut presisi."""
    # Arah dasar panah
    base_dir = ray_angle if is_inward else ray_angle + np.pi

    # Dua lengan sirip panah
    a1 = base_dir + fin_angle
    a2 = base_dir - fin_angle

    p1 = [x + fin_len * np.cos(a1), y + fin_len * np.sin(a1)]
    p2 = [x + fin_len * np.cos(a2), y + fin_len * np.sin(a2)]

    ax.plot([p1[0], x, p2[0]], [p1[1], y, p2[1]], color="black", linewidth=1.8, zorder=3)


def generate():
    """Radial Müller-Lyer optical illusion starburst pattern filling full canvas."""
    fig, ax = setup_ax()

    n_rays = 20
    inner_r = 12.0  # Diperbesar agar bagian dalam tidak saling menindih
    outer_r = 46.0  # Memenuhi canvas hingga mendekati tepi

    for i in range(n_rays):
        angle = i * 2 * np.pi / n_rays

        x1 = inner_r * np.cos(angle)
        y1 = inner_r * np.sin(angle)
        x2 = outer_r * np.cos(angle)
        y2 = outer_r * np.sin(angle)

        # 1. Gambar Garis Sinar Utama (Panjang sama persis untuk semua sinar)
        ax.plot([x1, x2], [y1, y2], color="black", linewidth=2.2, zorder=2)

        # 2. Gambar Sirip Panah (Berselang-seling: Inward vs Outward)
        inward = i % 2 == 0

        # Ujung Dalam
        draw_chevron(ax, x1, y1, angle, is_inward=inward)

        # Ujung Luar
        draw_chevron(ax, x2, y2, angle, is_inward=not inward)

    save(
        fig,
        "abstract optical muller lyer radial spoke starburst pattern black white texture",
    )


if __name__ == "__main__":
    generate()