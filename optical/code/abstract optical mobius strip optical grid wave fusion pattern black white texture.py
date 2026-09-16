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
    """Wild Optical Fusion: 3D Möbius strip surface mapped with an Op-Art checkerboard wave distortion."""
    fig, ax = setup_ax()

    u = np.linspace(0, 2 * np.pi, 240)
    v = np.linspace(-0.6, 0.6, 60)
    U, V = np.meshgrid(u, v)

    # Parametric Möbius strip coordinates
    X = (1 + (V / 2) * np.cos(U / 2)) * np.cos(U)
    Y = (1 + (V / 2) * np.cos(U / 2)) * np.sin(U)
    Z = (V / 2) * np.sin(U / 2)

    # Rotate 3D strip into 2D perspective projection
    angle_x = np.radians(35)
    angle_z = np.radians(45)

    # Z-rotation
    X_rot = X * np.cos(angle_z) - Y * np.sin(angle_z)
    Y_rot = X * np.sin(angle_z) + Y * np.cos(angle_z)
    Z_rot = Z

    # X-rotation
    Y_proj = Y_rot * np.cos(angle_x) - Z_rot * np.sin(angle_x)
    X_proj = X_rot

    # Render grid isolines with wave phase modulation creating optical illusion
    for i in range(V.shape[0]):
        # Modulate stroke width along u
        lw = 1.0 + 1.2 * np.sin(u * 3 + i * 0.2) ** 2
        ax.plot(
            X_proj[i, :], Y_proj[i, :], color="black", linewidth=1.2, alpha=0.85
        )

    for j in range(0, U.shape[1], 4):
        ax.plot(
            X_proj[:, j], Y_proj[:, j], color="black", linewidth=1.0, alpha=0.85
        )

    # Superimpose Op-Art concentric wave lines
    r_vals = np.linspace(0.2, 2.0, 18)
    theta_pts = np.linspace(0, 2 * np.pi, 300)
    for r in r_vals:
        wave_r = r + 0.08 * np.sin(8 * theta_pts)
        ax.plot(
            wave_r * np.cos(theta_pts),
            wave_r * np.sin(theta_pts),
            color="black",
            linewidth=0.9,
            linestyle="--",
        )

    save(
        fig,
        "abstract optical mobius strip optical grid wave fusion pattern black white texture",
    )


if __name__ == "__main__":
    abstract_optical_mobius_strip_optical_grid_wave_fusion_pattern_black_white_texture()
