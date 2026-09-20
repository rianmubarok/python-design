from datetime import datetime
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon
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


def isometric_cube_stack_shadow():
    """Tumpukan kubus isometrik 3D presisi dengan shading 3-tonal yang bersih."""
    fig, ax = setup_ax()

    cols, rows = 14, 14
    S = 4.0
    cos30 = np.cos(np.pi / 6)
    sin30 = np.sin(np.pi / 6)

    def project(x, y, z=0.0):
        return (x - y) * cos30, (x + y) * sin30 + z

    # Kumpulkan seluruh kolom kubus
    columns = []
    for i in range(cols):
        for j in range(rows):
            dist = np.sqrt((i - cols / 2.0) ** 2 + (j - rows / 2.0) ** 2)
            H = 2.0 + 3.0 * (0.5 + 0.5 * np.sin(0.4 * dist))
            depth = i + j
            columns.append((depth, i, j, H))

    # Urutkan secara presisi dari belakang (depth terkecil) ke depan (depth terbesar)
    columns.sort(key=lambda c: (c[0], c[1], c[2]))

    all_2d_points = []

    for idx, (depth, i, j, H) in enumerate(columns):
        x0, y0 = i * S, j * S

        # Koordinat Proyeksi 3D Kubus
        P0 = project(x0, y0, 0.0)
        P1 = project(x0 + S, y0, 0.0)
        P2 = project(x0 + S, y0 + S, 0.0)
        P3 = project(x0, y0 + S, 0.0)

        T0 = project(x0, y0, H)
        T1 = project(x0 + S, y0, H)
        T2 = project(x0 + S, y0 + S, H)
        T3 = project(x0, y0 + S, H)

        all_2d_points.extend([P0, P1, P2, P3, T0, T1, T2, T3])

        z_base = idx * 5

        # 1. Sisi Kanan (Right Face) - Shadow Sedang
        right_poly = [P0, P1, T1, T0]
        ax.add_patch(
            Polygon(
                right_poly,
                closed=True,
                facecolor="#B0B0B0",
                edgecolor="black",
                linewidth=1.0,
                zorder=z_base + 1,
            )
        )

        # 2. Sisi Kiri (Left Face) - Terang Sedang
        left_poly = [P0, P3, T3, T0]
        ax.add_patch(
            Polygon(
                left_poly,
                closed=True,
                facecolor="#E0E0E0",
                edgecolor="black",
                linewidth=1.0,
                zorder=z_base + 2,
            )
        )

        # 3. Sisi Atas (Top Face) - Terang Murni
        top_poly = [T0, T1, T2, T3]
        ax.add_patch(
            Polygon(
                top_poly,
                closed=True,
                facecolor="#FFFFFF",
                edgecolor="black",
                linewidth=1.0,
                zorder=z_base + 3,
            )
        )

    # Framing simetris terpusat penuh
    pts = np.array(all_2d_points)
    min_x, max_x = pts[:, 0].min(), pts[:, 0].max()
    min_y, max_y = pts[:, 1].min(), pts[:, 1].max()

    center_x = (min_x + max_x) / 2.0
    center_y = (min_y + max_y) / 2.0
    w = max_x - min_x
    h_span = max_y - min_y
    pad = max(w, h_span) / 2.0 + 4.0

    ax.set_xlim(center_x - pad, center_x + pad)
    ax.set_ylim(center_y - pad, center_y + pad)

    save(fig, "isometric cube stack shadow")


if __name__ == "__main__":
    isometric_cube_stack_shadow()