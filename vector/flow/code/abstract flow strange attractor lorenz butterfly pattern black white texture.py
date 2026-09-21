import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime
from scipy.integrate import odeint

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
    ax.set_xlim(-25, 25)
    ax.set_ylim(-35, 35)
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


def lorenz(state, t):
    """Lorenz equations"""
    x, y, z = state
    sigma, rho, beta = 10.0, 28.0, 8.0/3.0
    
    dx_dt = sigma * (y - x)
    dy_dt = x * (rho - z) - y  
    dz_dt = x * y - beta * z
    
    return [dx_dt, dy_dt, dz_dt]


def draw():
    """Lorenz Attractor butterfly pattern projected to 2D."""
    fig, ax = setup_ax()
    
    # Time parameters
    t = np.linspace(0, 100, 50000)
    
    # Multiple trajectories with slightly different initial conditions
    trajectories = []
    initial_conditions = [
        [1.0, 1.0, 1.0],
        [1.01, 1.0, 1.0],
        [1.0, 1.01, 1.0], 
        [1.0, 1.0, 1.01],
        [0.99, 1.0, 1.0]
    ]
    
    for init in initial_conditions:
        trajectory = odeint(lorenz, init, t)
        trajectories.append(trajectory)
    
    # Plot XY projection (butterfly view)
    for i, traj in enumerate(trajectories):
        alpha = 0.3 - i * 0.05  # Varying transparency
        linewidth = 0.8 - i * 0.1
        ax.plot(traj[:, 0], traj[:, 1], color="black", alpha=alpha, linewidth=linewidth)
    
    save(fig, "abstract flow strange attractor lorenz butterfly pattern black white texture")


if __name__ == "__main__":
    draw()