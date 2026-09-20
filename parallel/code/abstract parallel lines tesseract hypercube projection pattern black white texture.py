import numpy as np
import matplotlib.pyplot as plt
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
    ax.set_xlim(-5, 105)
    ax.set_ylim(-5, 105)
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


def fill_quad_with_lines(ax, p1, p2, p3, p4, n_lines=15, linewidth=0.2):
    """
    Mengisi bidang segi empat (quadrilateral) p1-p2-p3-p4 dengan garis paralel
    secara presisi dari garis (p1->p2) menuju garis (p4->p3).
    """
    for i in range(n_lines):
        t = i / (n_lines - 1) if n_lines > 1 else 0.5
        # Interpolasi titik awal dan akhir garis di dalam bidang
        start_pt = (1 - t) * p1 + t * p4
        end_pt = (1 - t) * p2 + t * p3
        ax.plot(
            [start_pt[0], end_pt[0]],
            [start_pt[1], end_pt[1]],
            color="black",
            linewidth=linewidth,
            solid_capstyle="round",
            alpha=0.6,
        )


def draw():
    """
    Proyeksi Tesseract (4D hypercube) presisi ke 2D menggunakan rotasi 4D 
    dengan isian garis-garis paralel rapi pada tiap sisi/wajah bidangnya.
    """
    fig, ax = setup_ax()

    # 1. Buat 16 titik sudut (vertices) dari Hiperkubus 4D
    vertices_4d = []
    for i in range(16):
        x = 1 if (i & 1) else -1
        y = 1 if (i & 2) else -1
        z = 1 if (i & 4) else -1
        w = 1 if (i & 8) else -1
        vertices_4d.append([x, y, z, w])
    vertices_4d = np.array(vertices_4d, dtype=float)

    # 2. Matriks Rotasi 4D untuk mendapatkan sudut pandang presisi & artistik
    angle = np.pi / 5
    rot_xz = np.array([
        [np.cos(angle), 0, -np.sin(angle), 0],
        [0, 1, 0, 0],
        [np.sin(angle), 0, np.cos(angle), 0],
        [0, 0, 0, 1]
    ])
    rot_yw = np.array([
        [1, 0, 0, 0],
        [0, np.cos(angle * 0.7), 0, -np.sin(angle * 0.7)],
        [0, 0, 1, 0],
        [0, np.sin(angle * 0.7), 0, np.cos(angle * 0.7)]
    ])

    rotated_4d = vertices_4d @ rot_xz @ rot_yw

    # 3. Proyeksi Perspektif 4D -> 3D -> 2D
    projected_2d = []
    distance_4d = 2.8
    distance_3d = 2.5

    for v in rotated_4d:
        # 4D -> 3D
        w_factor = 1 / (distance_4d - v[3])
        x3, y3, z3 = v[0] * w_factor, v[1] * w_factor, v[2] * w_factor

        # 3D -> 2D
        z_factor = 1 / (distance_3d - z3)
        x2, y2 = x3 * z_factor, y3 * z_factor
        projected_2d.append([x2, y2])

    projected_2d = np.array(projected_2d)

    # Normalisasi skala ke dalam ruang koordinat canvas (-5 sampai 105, pusat di 50,50)
    projected_2d = projected_2d * 60 + 50

    # 4. Gambar Arsir Garis Paralel pada Wajah-Wajah Kubus Outer & Inner
    # Pasangan wajah (faces) utama untuk tekstur paralel
    faces = [
        [0, 1, 3, 2],    # Depan
        [4, 5, 7, 6],    # Belakang
        [8, 9, 11, 10],  # Depan 4D
        [12, 13, 15, 14],# Belakang 4D
        [0, 1, 9, 8],    # Penghubung 4D bawah
        [2, 3, 11, 10],  # Penghubung 4D atas
    ]

    for face in faces:
        p1, p2, p3, p4 = (
            projected_2d[face[0]],
            projected_2d[face[1]],
            projected_2d[face[2]],
            projected_2d[face[3]],
        )
        fill_quad_with_lines(ax, p1, p2, p3, p4, n_lines=18, linewidth=0.25)

    # 5. Gambar Rusuk (Edges) Utama Tesseract (32 Rusuk)
    for i in range(16):
        for j in range(i + 1, 16):
            # Rusuk ada jika hanya 1 koordinat bernilai beda
            if np.sum(np.abs(vertices_4d[i] - vertices_4d[j]) == 2) == 1:
                p1, p2 = projected_2d[i], projected_2d[j]
                ax.plot(
                    [p1[0], p2[0]],
                    [p1[1], p2[1]],
                    color="black",
                    linewidth=0.8,
                    solid_capstyle="round",
                )

    save(fig, "abstract parallel lines tesseract hypercube projection pattern black white texture")


if __name__ == "__main__":
    draw()