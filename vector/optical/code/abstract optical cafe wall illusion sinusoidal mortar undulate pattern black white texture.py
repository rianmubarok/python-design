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


def generate():
    """Café wall optical illusion with wavy mortar lines integrated seamlessly into tile boundaries."""
    fig, ax = setup_ax()

    n_rows = 14
    n_cols = 14
    row_h = 100.0 / n_rows
    col_w = 100.0 / n_cols

    # Pergeseran pola café wall berselang-seling (staggered shifts)
    offsets = [0, 0.25, 0.5, 0.25, 0, -0.25, -0.5, -0.25]

    def wave_y(x, base_y, r):
        """Fungsi deformasi gelombang sinusoidal untuk mortar & batas ubin."""
        return base_y + 0.8 * np.sin(x * 0.2 + r * 1.2)

    # 1. Gambar ubin persegi hitam yang terdeformasi gelombang
    for r in range(n_rows):
        y_bottom_base = r * row_h
        y_top_base = (r + 1) * row_h
        shift = offsets[r % len(offsets)] * col_w

        for c in range(-2, n_cols + 2):
            if (c + r) % 2 == 0:
                x_left = c * col_w + shift
                x_right = x_left + col_w

                # Titik-titik sampel sepanjang batas horizontal atas dan bawah
                x_samples = np.linspace(x_left, x_right, 20)
                y_bottom = wave_y(x_samples, y_bottom_base, r)
                y_top = wave_y(np.flip(x_samples), y_top_base, r + 1)

                # Gabungkan membentuk poligon ubin yang menyatu dengan mortar
                poly_x = np.concatenate([x_samples, np.flip(x_samples)])
                poly_y = np.concatenate([y_bottom, y_top])

                polygon = Polygon(
                    np.column_stack([poly_x, poly_y]),
                    closed=True,
                    facecolor="black",
                    edgecolor="none",
                    zorder=1,
                )
                ax.add_patch(polygon)

    # 2. Gambar garis mortar sinusoidal melintasi batas baris
    x_mortar = np.linspace(-10, 110, 600)
    for r in range(n_rows + 1):
        y_mortar = wave_y(x_mortar, r * row_h, r)
        ax.plot(
            x_mortar,
            y_mortar,
            color="#808080",
            linewidth=2.5,
            solid_capstyle="round",
            zorder=2,
        )

    # Framing simetris presisi di dalam batas (0, 100)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)

    save(
        fig,
        "abstract optical cafe wall illusion sinusoidal mortar undulate pattern black white texture",
    )


if __name__ == "__main__":
    generate()