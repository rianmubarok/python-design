from datetime import datetime
from pathlib import Path
from matplotlib.patches import Arc, Circle
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
    """Seamless Wang-style pipe network grid tessellation with controlled pulsing thickness."""
    fig, ax = setup_ax()

    n = 18
    w = 100 / (n - 2)  # Diperluas agar menutupi tepi kanvas
    rng = np.random.default_rng(SEED)

    # Iterasi kisi melebihi batas tampilan agar tidak terpotong di tepi
    for row in range(-1, n + 1):
        for col in range(-1, n + 1):
            cx = col * w + w / 2
            cy = row * w + w / 2

            # Efek gelombang ketebalan (pulsing thickness)
            thick = 1.4 + 2.8 * (0.5 + 0.5 * np.sin(col * 0.7) * np.cos(row * 0.55))

            # Tipe ubin Truchet yang dijamin terhubung mulus di setiap batas
            # 0: Siku Kiri-Atas + Kanan-Bawah
            # 1: Siku Kiri-Bawah + Kanan-Atas
            # 2: Perempatan Pipa (Cross Joint + Circle Node)
            tile_type = rng.integers(0, 3)

            if tile_type == 0:
                # Siku Top-Left
                ax.add_patch(
                    Arc(
                        (cx - w / 2, cy + w / 2),
                        w,
                        w,
                        theta1=270,
                        theta2=360,
                        color="black",
                        linewidth=thick,
                        zorder=2,
                    )
                )
                # Siku Bottom-Right
                ax.add_patch(
                    Arc(
                        (cx + w / 2, cy - w / 2),
                        w,
                        w,
                        theta1=90,
                        theta2=180,
                        color="black",
                        linewidth=thick,
                        zorder=2,
                    )
                )

            elif tile_type == 1:
                # Siku Bottom-Left
                ax.add_patch(
                    Arc(
                        (cx - w / 2, cy - w / 2),
                        w,
                        w,
                        theta1=0,
                        theta2=90,
                        color="black",
                        linewidth=thick,
                        zorder=2,
                    )
                )
                # Siku Top-Right
                ax.add_patch(
                    Arc(
                        (cx + w / 2, cy + w / 2),
                        w,
                        w,
                        theta1=180,
                        theta2=270,
                        color="black",
                        linewidth=thick,
                        zorder=2,
                    )
                )

            elif tile_type == 2:
                # Pipa Lurus Horisontal & Vertikal (Cross)
                ax.plot(
                    [cx - w / 2, cx + w / 2],
                    [cy, cy],
                    color="black",
                    linewidth=thick,
                    solid_capstyle="butt",
                    zorder=1,
                )
                ax.plot(
                    [cx, cx],
                    [cy - w / 2, cy + w / 2],
                    color="black",
                    linewidth=thick,
                    solid_capstyle="butt",
                    zorder=1,
                )
                # Node lingkaran simpul di tengah
                ax.add_patch(
                    Circle(
                        (cx, cy),
                        w * 0.18,
                        fill=True,
                        facecolor="black",
                        zorder=3,
                    )
                )

    pad = 32.0
    # Fokus area tengah agar simetris penuh
    ax.set_xlim(50 - pad, 50 + pad)
    ax.set_ylim(50 - pad, 50 + pad)

    save(
        fig,
        "abstract grid tessellation wang pipe thickness checker pulse pattern black white texture",
    )


if __name__ == "__main__":
    draw()