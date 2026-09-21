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
    ax.set_xlim(-2.2, 2.2)
    ax.set_ylim(-2.2, 2.2)
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


def abstract_optical_mobius_strip_optical_grid_wave_fusion_pattern_black_white_texture():
    """3D Möbius strip surface mapped with clear grid structure and wave distortion."""
    fig, ax = setup_ax()

    # 1. Parameter Grid Pita Möbius (Diperjarang agar tidak menumpuk pekat)
    u = np.linspace(0, 2 * np.pi, 180)
    v = np.linspace(-0.55, 0.55, 20)
    U, V = np.meshgrid(u, v)

    # Koordinat Parametrik Möbius Strip
    X = (1 + (V / 2) * np.cos(U / 2)) * np.cos(U)
    Y = (1 + (V / 2) * np.cos(U / 2)) * np.sin(U)
    Z = (V / 2) * np.sin(U / 2)

    # 2. Sudut Rotasi Perspektif 3D yang Menampakkan Puntiran Möbius Tegas
    angle_x = np.radians(60)
    angle_z = np.radians(30)

    # Rotasi terhadap Sumbu Z
    X_rot = X * np.cos(angle_z) - Y * np.sin(angle_z)
    Y_rot = X * np.sin(angle_z) + Y * np.cos(angle_z)
    Z_rot = Z

    # Rotasi terhadap Sumbu X
    X_proj = X_rot
    Y_proj = Y_rot * np.cos(angle_x) - Z_rot * np.sin(angle_x)

    # 3. Render Garis-Garis Gelombang Latar Belakang Op-Art
    r_vals = np.linspace(0.15, 2.1, 24)
    theta_pts = np.linspace(0, 2 * np.pi, 400)
    for idx, r in enumerate(r_vals):
        wave_r = r + 0.06 * np.sin(10 * theta_pts + idx * 0.2)
        ax.plot(
            wave_r * np.cos(theta_pts),
            wave_r * np.sin(theta_pts),
            color="black",
            linewidth=0.6,
            linestyle="--" if idx % 2 == 0 else "-",
            alpha=0.45,
            zorder=1,
        )

    # 4. Render Grid Permukaan Möbius Strip (Panjang & Lebar)
    # Garis Memanjang (Longitudinal)
    for i in range(V.shape[0]):
        # Modulasi ketebalan garis secara dinamis
        lw = 0.5 + 0.6 * np.sin(i * 0.3) ** 2
        ax.plot(
            X_proj[i, :], Y_proj[i, :], color="black", linewidth=lw, alpha=0.9, zorder=3
        )

    # Garis Melintang (Transversal)
    for j in range(0, U.shape[1], 3):
        ax.plot(
            X_proj[:, j], Y_proj[:, j], color="black", linewidth=0.7, alpha=0.9, zorder=2
        )

    save(
        fig,
        "abstract optical mobius strip optical grid wave fusion pattern black white texture",
    )


if __name__ == "__main__":
    abstract_optical_mobius_strip_optical_grid_wave_fusion_pattern_black_white_texture()