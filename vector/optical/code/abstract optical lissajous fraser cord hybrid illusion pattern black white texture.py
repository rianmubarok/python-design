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


def generate():
    """Lissajous curves used as RAILS with dense Fraser cord illusion segments."""
    fig, ax = setup_ax()

    t_curve = np.linspace(0, 2 * np.pi, 4000)
    tilt_angle = np.radians(22)  # Sudut kemiringan khas Fraser Cord

    freq_pairs = [(3, 4), (5, 6), (2, 3), (7, 5)]
    scales = [42, 34, 26, 18]

    for idx, ((fa, fb), scale) in enumerate(zip(freq_pairs, scales)):
        delta = np.pi / 4
        x_liss = scale * np.sin(fa * t_curve + delta)
        y_liss = scale * np.cos(fb * t_curve)

        # 1. Gambar Garis Kurva Lissajous Utama sebagai Rail (Fondasi Ilusi)
        ax.plot(x_liss, y_liss, color="black", linewidth=1.5, alpha=0.85, zorder=1)

        # 2. Gambar Segmen Tali Fraser Rapat Sepanjang Kurva
        sample_step = 8  # Jarak diperketat agar membentuk pita tali kontinu
        for k in range(1, len(t_curve) - 1, sample_step):
            cx = x_liss[k]
            cy = y_liss[k]

            # Vektor Tangensial Lokal
            dx_tan = x_liss[k + 1] - x_liss[k - 1]
            dy_tan = y_liss[k + 1] - y_liss[k - 1]
            tangent = np.arctan2(dy_tan, dx_tan)

            # Kemiringan Segmen Fraser (Selang-seling arah tilt antar-layer)
            direction_tilt = tilt_angle if idx % 2 == 0 else -tilt_angle
            cord_dir = tangent + direction_tilt

            segment_len = 3.5
            ddx = (segment_len / 2) * np.cos(cord_dir)
            ddy = (segment_len / 2) * np.sin(cord_dir)

            # Segmen Hitam Utama
            ax.plot(
                [cx - ddx, cx + ddx],
                [cy - ddy, cy + ddy],
                color="black",
                linewidth=2.2,
                zorder=2,
            )
            # Garis Inti Putih di Tengah Segmen (Efek Tali Terpuntir)
            ax.plot(
                [cx - ddx * 0.45, cx + ddx * 0.45],
                [cy - ddy * 0.45, cy + ddy * 0.45],
                color="white",
                linewidth=0.8,
                zorder=3,
            )

    save(
        fig,
        "abstract optical lissajous fraser cord hybrid illusion pattern black white texture",
    )


if __name__ == "__main__":
    generate()