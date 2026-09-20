from datetime import datetime
from pathlib import Path
import matplotlib.patches as patches
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


def draw():
    """Wang Tiles Pipe Network Maze (Seamless Interlocking Implementation)."""
    fig, ax = setup_ax()
    rng = np.random.default_rng(42)

    grid_size = 22
    cell_w = 120.0 / grid_size

    # Lebar garis luar (hitam) dan dalam (putih)
    lw_black = 7.0
    lw_white = 3.5

    def draw_pipe_segment(x1, y1, x2, y2):
        """Menggambar potongan pipa lurus berongga."""
        ax.plot(
            [x1, x2],
            [y1, y2],
            color="black",
            linewidth=lw_black,
            solid_capstyle="butt",
            zorder=2,
        )
        ax.plot(
            [x1, x2],
            [y1, y2],
            color="white",
            linewidth=lw_white,
            solid_capstyle="butt",
            zorder=3,
        )

    def draw_arc_segment(center_x, center_y, angle1, angle2):
        """Menggambar potongan pipa melengkung (siku) berongga."""
        arc_b = patches.Arc(
            (center_x, center_y),
            cell_w,
            cell_w,
            angle=0,
            theta1=angle1,
            theta2=angle2,
            linewidth=lw_black,
            color="black",
            capstyle="butt",
            zorder=2,
        )
        arc_w = patches.Arc(
            (center_x, center_y),
            cell_w,
            cell_w,
            angle=0,
            theta1=angle1,
            theta2=angle2,
            linewidth=lw_white,
            color="white",
            capstyle="butt",
            zorder=3,
        )
        ax.add_patch(arc_b)
        ax.add_patch(arc_w)

    for row in range(-2, grid_size + 2):
        for col in range(-2, grid_size + 2):
            cx = -10 + col * cell_w
            cy = -10 + row * cell_w
            mid_x = cx + cell_w / 2
            mid_y = cy + cell_w / 2

            # Pilih tipe konfigurasi ubin Truchet/Wang yang menjamin keterhubungan
            # 1: Dual Siku (Kiri-Atas & Kanan-Bawah)
            # 2: Dual Siku (Kiri-Bawah & Kanan-Atas)
            # 3: Perempatan (Cross Joint)
            tile = rng.choice([1, 2, 3])

            if tile == 1:
                draw_arc_segment(cx, cy + cell_w, 270, 360)  # Top-Left
                draw_arc_segment(cx + cell_w, cy, 90, 180)  # Bottom-Right

            elif tile == 2:
                draw_arc_segment(cx, cy, 0, 90)  # Bottom-Left
                draw_arc_segment(cx + cell_w, cy + cell_w, 180, 270)  # Top-Right

            elif tile == 3:
                # Perempatan Pipa Lurus
                draw_pipe_segment(cx, mid_y, cx + cell_w, mid_y)
                draw_pipe_segment(mid_x, cy, mid_x, cy + cell_w)

                # Sambungan Lingkaran Tengah (Joint Circle)
                joint_b = patches.Circle(
                    (mid_x, mid_y), cell_w * 0.22, color="black", zorder=4
                )
                joint_w = patches.Circle(
                    (mid_x, mid_y), cell_w * 0.14, color="white", zorder=5
                )
                joint_d = patches.Circle(
                    (mid_x, mid_y), cell_w * 0.05, color="black", zorder=6
                )
                ax.add_patch(joint_b)
                ax.add_patch(joint_w)
                ax.add_patch(joint_d)

    # Memfokuskan tampilan di area tengah kanvas
    ax.set_xlim(50 - 45, 50 + 45)
    ax.set_ylim(50 - 45, 50 + 45)

    save(
        fig,
        "abstract grid tessellation wang tiles pipe network maze pattern black white texture",
    )


if __name__ == "__main__":
    draw()