from datetime import datetime
from pathlib import Path
from matplotlib.patches import Arc
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


def draw_up_triangle_arcs(ax, v0, v1, v2, d_arc, st, lw):
    """Menggambar busur pada segitiga menghadap KE ATAS."""
    if st == 0:
        # Hubungkan titik tengah (v0-v1) & (v1-v2) & (v2-v0)
        ax.add_patch(Arc(v0, d_arc, d_arc, theta1=0, theta2=60, color="black", linewidth=lw))
        ax.add_patch(Arc(v1, d_arc, d_arc, theta1=120, theta2=180, color="black", linewidth=lw))
        ax.add_patch(Arc(v2, d_arc, d_arc, theta1=240, theta2=300, color="black", linewidth=lw))
    elif st == 1:
        ax.add_patch(Arc(v0, d_arc, d_arc, theta1=0, theta2=60, color="black", linewidth=lw))
        ax.add_patch(Arc(v1, d_arc, d_arc, theta1=120, theta2=180, color="black", linewidth=lw))
    else:
        ax.add_patch(Arc(v1, d_arc, d_arc, theta1=120, theta2=180, color="black", linewidth=lw))
        ax.add_patch(Arc(v2, d_arc, d_arc, theta1=240, theta2=300, color="black", linewidth=lw))


def draw_down_triangle_arcs(ax, v0, v1, v2_d, d_arc, st, lw):
    """Menggambar busur pada segitiga menghadap KE BAWAH."""
    if st == 0:
        ax.add_patch(Arc(v0, d_arc, d_arc, theta1=300, theta2=360, color="black", linewidth=lw))
        ax.add_patch(Arc(v1, d_arc, d_arc, theta1=180, theta2=240, color="black", linewidth=lw))
        ax.add_patch(Arc(v2_d, d_arc, d_arc, theta1=60, theta2=120, color="black", linewidth=lw))
    elif st == 1:
        ax.add_patch(Arc(v0, d_arc, d_arc, theta1=300, theta2=360, color="black", linewidth=lw))
        ax.add_patch(Arc(v1, d_arc, d_arc, theta1=180, theta2=240, color="black", linewidth=lw))
    else:
        ax.add_patch(Arc(v1, d_arc, d_arc, theta1=180, theta2=240, color="black", linewidth=lw))
        ax.add_patch(Arc(v2_d, d_arc, d_arc, theta1=60, theta2=120, color="black", linewidth=lw))


def draw():
    """True Seamless Interlocking Triangular Truchet Tile Maze Pattern."""
    fig, ax = setup_ax()

    a = 8.0  # Panjang sisi segitiga
    h = a * np.sqrt(3) / 2.0  # Tinggi kisi segitiga
    d_arc = a  # Diameter busur = panjang sisi agar menyambung di titik tengah rusuk
    lw = 1.5

    rows, cols = 16, 16
    center_x = (cols - 1) * a / 2.0
    center_y = (rows - 1) * h / 2.0

    rng = np.random.default_rng(42)

    # Render kisi yang cukup luas untuk menghindari pemotongan tepi
    for row in range(-2, rows + 3):
        for col in range(-2, cols + 3):
            cx = col * a + (a / 2.0 if row % 2 != 0 else 0.0)
            cy = row * h

            # 1. Segitiga Menghadap Atas
            v0 = (cx, cy)
            v1 = (cx + a, cy)
            v2 = (cx + a / 2.0, cy + h)
            st_up = int(rng.integers(0, 3))
            draw_up_triangle_arcs(ax, v0, v1, v2, d_arc, st_up, lw)

            # 2. Segitiga Menghadap Bawah (Mengisi celah dengan puncak v2_d yang benar di atas)
            v2_d = (cx + a / 2.0, cy + h)
            v1_next = (cx + a, cy)
            st_down = int(rng.integers(0, 3))
            draw_down_triangle_arcs(ax, v0, v1_next, v2_d, d_arc, st_down, lw)

    # Menentukan viewport simetris di tengah
    pad = 32.0
    ax.set_xlim(center_x - pad, center_x + pad)
    ax.set_ylim(center_y - pad, center_y + pad)

    save(
        fig,
        "abstract grid tessellation triangular truchet vertex arc maze pattern black white texture",
    )


if __name__ == "__main__":
    draw()