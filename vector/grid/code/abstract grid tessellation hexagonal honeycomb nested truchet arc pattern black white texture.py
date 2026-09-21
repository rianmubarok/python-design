from datetime import datetime
from pathlib import Path
from matplotlib.patches import Arc, RegularPolygon
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


def draw():
    """Hex honeycomb cells filled with nested Truchet arcs centered and seamless."""
    fig, ax = setup_ax()

    r_hex = 6.0  # Jari-jari segi enam
    dx = r_hex * np.sqrt(3)  # Jarak antar-kolom
    dy = r_hex * 1.5  # Jarak antar-baris

    rows, cols = 18, 18

    # Menghitung titik pusat geometris kisi agar pas di tengah kanvas (50, 50)
    grid_center_x = (cols - 1) * dx / 2.0
    grid_center_y = (rows - 1) * dy / 2.0
    offset_x = 50.0 - grid_center_x
    offset_y = 50.0 - grid_center_y

    # Jarak titik sudut segi enam ke tengah rusuk (apothem)
    r_inc = r_hex * np.sqrt(3) / 2.0

    for row in range(-2, rows + 2):
        for col in range(-2, cols + 2):
            cx = col * dx + offset_x
            if row % 2 != 0:
                cx += dx / 2.0
            cy = row * dy + offset_y

            # 1. Segi enam (Honeycomb Grid)
            ax.add_patch(
                RegularPolygon(
                    (cx, cy),
                    numVertices=6,
                    radius=r_hex,
                    orientation=0,
                    fill=False,
                    edgecolor="black",
                    linewidth=0.8,
                    zorder=1,
                )
            )

            # Rotasi selang-seling untuk variasi pola Truchet
            rot = (row + col) % 2

            # 2. Busur Truchet bersarang (Nested Arcs)
            # Menggunakan radius apothem (r_inc / 2) agar bertemu tepat di titik tengah rusuk
            base_r = r_inc / 2.0
            offsets = (-1.2, 0.0, 1.2)  # Penggeser untuk busur bersarang
            lws = (0.6, 1.0, 0.6)

            for delta, lw in zip(offsets, lws):
                r_arc = base_r + delta
                d_arc = 2 * r_arc

                if rot == 0:
                    # Busur kiri dan kanan berpusat di titik sudut vertikal
                    v_left = (cx - r_hex * np.sqrt(3) / 2.0, cy)
                    v_right = (cx + r_hex * np.sqrt(3) / 2.0, cy)

                    ax.add_patch(
                        Arc(
                            v_left,
                            d_arc,
                            d_arc,
                            angle=0,
                            theta1=300,
                            theta2=60,
                            color="black",
                            linewidth=lw,
                            zorder=2,
                        )
                    )
                    ax.add_patch(
                        Arc(
                            v_right,
                            d_arc,
                            d_arc,
                            angle=0,
                            theta1=120,
                            theta2=240,
                            color="black",
                            linewidth=lw,
                            zorder=2,
                        )
                    )
                else:
                    # Busur atas dan bawah berpusat di titik sudut horizontal
                    v_top = (cx, cy + r_hex)
                    v_bottom = (cx, cy - r_hex)

                    ax.add_patch(
                        Arc(
                            v_top,
                            d_arc,
                            d_arc,
                            angle=0,
                            theta1=210,
                            theta2=330,
                            color="black",
                            linewidth=lw,
                            zorder=2,
                        )
                    )
                    ax.add_patch(
                        Arc(
                            v_bottom,
                            d_arc,
                            d_arc,
                            angle=0,
                            theta1=30,
                            theta2=150,
                            color="black",
                            linewidth=lw,
                            zorder=2,
                        )
                    )

    # Tangkapan area simetris di tengah
    pad = 38.0
    ax.set_xlim(50 - pad, 50 + pad)
    ax.set_ylim(50 - pad, 50 + pad)

    save(
        fig,
        "abstract grid tessellation hexagonal honeycomb nested truchet arc pattern black white texture",
    )


if __name__ == "__main__":
    draw()