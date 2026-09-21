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
SEED = 42

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
    """Seamless Manhattan pipe network tessellation with controlled thickness wave."""
    fig, ax = setup_ax()

    n = 18
    w = 100 / (n - 2)  # Perluas sedikit agar menutupi tepi kanvas
    rng = np.random.default_rng(SEED)

    # Fungsi gelombang ketebalan berdasarkan koordinat absolut (x, y)
    def get_thick(x, y):
        return 1.5 + 3.0 * (0.5 + 0.5 * np.sin(x * 0.12) * np.cos(y * 0.1))

    for row in range(-1, n + 1):
        for col in range(-1, n + 1):
            cx = col * w + w / 2
            cy = row * w + w / 2

            # Ketebalan dihitung dari pusat tile agar garis konsisten
            thick = get_thick(cx, cy)

            # Tipe Ubin Truchet Manhattan (Menjamin 100% Seamless/Saling Mengunci)
            # Tipe 0: Siku Kiri-Atas & Kanan-Bawah
            # Tipe 1: Siku Kiri-Bawah & Kanan-Atas
            # Tipe 2: Pipa Lurus Horisontal & Vertikal (Cross)
            tile_type = rng.integers(0, 3)

            if tile_type == 0:
                # Arc 1: Top-Left (Pusat di Sudut Kiri-Atas)
                ax.add_patch(
                    Arc(
                        (cx - w / 2, cy + w / 2),
                        w,
                        w,
                        angle=0,
                        theta1=270,
                        theta2=360,
                        color="black",
                        linewidth=thick,
                        zorder=2,
                    )
                )
                # Arc 2: Bottom-Right (Pusat di Sudut Kanan-Bawah)
                ax.add_patch(
                    Arc(
                        (cx + w / 2, cy - w / 2),
                        w,
                        w,
                        angle=0,
                        theta1=90,
                        theta2=180,
                        color="black",
                        linewidth=thick,
                        zorder=2,
                    )
                )

            elif tile_type == 1:
                # Arc 1: Bottom-Left (Pusat di Sudut Kiri-Bawah)
                ax.add_patch(
                    Arc(
                        (cx - w / 2, cy - w / 2),
                        w,
                        w,
                        angle=0,
                        theta1=0,
                        theta2=90,
                        color="black",
                        linewidth=thick,
                        zorder=2,
                    )
                )
                # Arc 2: Top-Right (Pusat di Sudut Kanan-Atas)
                ax.add_patch(
                    Arc(
                        (cx + w / 2, cy + w / 2),
                        w,
                        w,
                        angle=0,
                        theta1=180,
                        theta2=270,
                        color="black",
                        linewidth=thick,
                        zorder=2,
                    )
                )

            else:
                # Straight Cross Pipe
                ax.plot(
                    [cx - w / 2, cx + w / 2],
                    [cy, cy],
                    color="black",
                    linewidth=thick,
                    solid_capstyle="butt",
                    zorder=2,
                )
                ax.plot(
                    [cx, cx],
                    [cy - w / 2, cy + w / 2],
                    color="black",
                    linewidth=thick,
                    solid_capstyle="butt",
                    zorder=2,
                )

    # Tangkapan area simetris di tengah kanvas
    pad = 36.0
    ax.set_xlim(50 - pad, 50 + pad)
    ax.set_ylim(50 - pad, 50 + pad)

    save(
        fig,
        "abstract grid tessellation manhattan pipe rounded elbow maze pattern black white texture",
    )


if __name__ == "__main__":
    draw()