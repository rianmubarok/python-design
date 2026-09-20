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


def lorenz_attractor(steps=10000, dt=0.01, sigma=10, rho=28, beta=8/3):
    """Simulasi attractor Lorenz (sistem chaos klasik)."""
    x = np.zeros(steps)
    y = np.zeros(steps)
    z = np.zeros(steps)
    
    # Kondisi awal
    x[0], y[0], z[0] = 0.1, 0.0, 0.0
    
    for i in range(steps - 1):
        dx = sigma * (y[i] - x[i])
        dy = x[i] * (rho - z[i]) - y[i]
        dz = x[i] * y[i] - beta * z[i]
        
        x[i+1] = x[i] + dx * dt
        y[i+1] = y[i] + dy * dt
        z[i+1] = z[i] + dz * dt
    
    # Normalisasi dan scaling
    x_norm = 50 + 25 * (x - x.mean()) / x.std()
    y_norm = 50 + 25 * (y - y.mean()) / y.std()
    
    return x_norm, y_norm


def rossler_attractor(steps=8000, dt=0.05, a=0.2, b=0.2, c=5.7):
    """Simulasi attractor Rössler."""
    x = np.zeros(steps)
    y = np.zeros(steps)
    z = np.zeros(steps)
    
    x[0], y[0], z[0] = 0.1, 0.0, 0.0
    
    for i in range(steps - 1):
        dx = -y[i] - z[i]
        dy = x[i] + a * y[i]
        dz = b + z[i] * (x[i] - c)
        
        x[i+1] = x[i] + dx * dt
        y[i+1] = y[i] + dy * dt
        z[i+1] = z[i] + dz * dt
    
    x_norm = 50 + 20 * (x - x.mean()) / x.std()
    y_norm = 50 + 20 * (y - y.mean()) / y.std()
    
    return x_norm, y_norm


def clifford_attractor(steps=20000, a=-1.7, b=1.8, c=-1.9, d=-0.4):
    """Simulasi attractor Clifford (map 2D)."""
    x = np.zeros(steps)
    y = np.zeros(steps)
    
    x[0], y[0] = 0.1, 0.1
    
    for i in range(steps - 1):
        x[i+1] = np.sin(a * y[i]) + c * np.cos(a * x[i])
        y[i+1] = np.sin(b * x[i]) + d * np.cos(b * y[i])
    
    x_norm = 50 + 30 * x
    y_norm = 50 + 30 * y
    
    return x_norm, y_norm


def chaotic_strange_attractor():
    """Sistem chaos dengan multiple strange attractors dan bifurkasi."""
    fig, ax = setup_ax()
    
    center_x, center_y = 50, 50
    
    min_x, max_x = float("inf"), float("-inf")
    min_y, max_y = float("inf"), float("-inf")
    
    # Layer 1: Lorenz attractor (sistem chaos 3D)
    print("Generating Lorenz attractor...")
    x_lorenz, y_lorenz = lorenz_attractor(steps=12000)
    
    # Plot Lorenz dengan density-based coloring
    n_lorenz = len(x_lorenz)
    for i in range(0, n_lorenz - 100, 50):
        segment_x = x_lorenz[i:i+100]
        segment_y = y_lorenz[i:i+100]
        
        # Alpha berdasarkan density lokal
        local_density = min(100, len(segment_x))
        alpha = 0.1 + 0.3 * (local_density / 100)
        lw = 0.3 + 0.4 * (i / n_lorenz)
        
        ax.plot(segment_x, segment_y, color="black", linewidth=lw, alpha=alpha)
        
        # Update bounding box
        min_x, max_x = min(min_x, segment_x.min()), max(max_x, segment_x.max())
        min_y, max_y = min(min_y, segment_y.min()), max(max_y, segment_y.max())
    
    # Layer 2: Rössler attractor
    print("Generating Rössler attractor...")
    x_rossler, y_rossler = rossler_attractor(steps=10000)
    
    # Transformasi untuk posisi berbeda
    x_rossler_trans = 50 + 0.8 * (x_rossler - 50) + 15
    y_rossler_trans = 50 + 0.8 * (y_rossler - 50) - 15
    
    n_rossler = len(x_rossler_trans)
    for i in range(0, n_rossler - 80, 40):
        segment_x = x_rossler_trans[i:i+80]
        segment_y = y_rossler_trans[i:i+80]
        
        alpha = 0.08 + 0.25 * (i / n_rossler)
        lw = 0.2 + 0.3 * (1 - i / n_rossler)
        
        ax.plot(segment_x, segment_y, color="black", linewidth=lw, alpha=alpha)
        
        min_x, max_x = min(min_x, segment_x.min()), max(max_x, segment_x.max())
        min_y, max_y = min(min_y, segment_y.min()), max(max_y, segment_y.max())
    
    # Layer 3: Clifford attractor
    print("Generating Clifford attractor...")
    x_clifford, y_clifford = clifford_attractor(steps=15000)
    
    x_clifford_trans = 50 + 0.7 * (x_clifford - 50) - 20
    y_clifford_trans = 50 + 0.7 * (y_clifford - 50) + 20
    
    n_clifford = len(x_clifford_trans)
    
    # Plot dengan pendekatan point-based untuk pola fractal
    for i in range(0, n_clifford, 10):
        x_val = x_clifford_trans[i]
        y_val = y_clifford_trans[i]
        
        # Ukuran titik berdasarkan posisi dalam sequence
        marker_size = 0.1 + 0.3 * (i / n_clifford)
        alpha = 0.05 + 0.15 * (1 - abs(i/n_clifford - 0.5))
        
        ax.plot(x_val, y_val, marker=".", markersize=marker_size, 
                color="black", alpha=alpha)
        
        min_x, max_x = min(min_x, x_val), max(max_x, x_val)
        min_y, max_y = min(min_y, y_val), max(max_y, y_val)
    
    # Layer 4: Bifurkasi diagram (simulasi logistic map)
    print("Generating bifurcation diagram...")
    n_bifurcation = 200
    r_values = np.linspace(2.5, 4.0, n_bifurcation)
    bif_x = []
    bif_y = []
    
    for r_idx, r in enumerate(r_values):
        # Logistic map: x_{n+1} = r * x_n * (1 - x_n)
        x = 0.5  # Nilai awal
        transient = 200  # Iterasi transient
        collect = 100    # Iterasi yang dikumpulkan
        
        for _ in range(transient):
            x = r * x * (1 - x)
        
        for _ in range(collect):
            x = r * x * (1 - x)
            bif_x.append(50 + 25 * (r_idx / n_bifurcation - 0.5))
            bif_y.append(50 + 40 * (x - 0.5))
    
    bif_x = np.array(bif_x)
    bif_y = np.array(bif_y)
    
    # Plot bifurkasi sebagai titik-titik
    for i in range(0, len(bif_x), 5):
        x_val = bif_x[i]
        y_val = bif_y[i]
        
        ax.plot(x_val, y_val, marker=".", markersize=0.2, 
                color="black", alpha=0.3)
        
        min_x, max_x = min(min_x, x_val), max(max_x, x_val)
        min_y, max_y = min(min_y, y_val), max(max_y, y_val)
    
    # Layer 5: Chaotic orbits (Poincaré sections)
    print("Generating chaotic orbits...")
    n_orbits = 8
    orbit_centers = []
    
    for orbit_idx in range(n_orbits):
        orbit_angle = orbit_idx * 2 * np.pi / n_orbits
        orbit_radius = 15 + np.random.uniform(-3, 3)
        orbit_cx = center_x + orbit_radius * np.cos(orbit_angle)
        orbit_cy = center_y + orbit_radius * np.sin(orbit_angle)
        orbit_centers.append((orbit_cx, orbit_cy))
        
        # Simulasi orbit chaotic
        n_orbit_points = 800
        orbit_points = []
        
        # Persamaan diferensial chaotic sederhana
        x, y = 0.1, 0.1
        for _ in range(n_orbit_points):
            dx = np.sin(y) + np.random.uniform(-0.1, 0.1)
            dy = np.cos(x) + np.random.uniform(-0.1, 0.1)
            
            x = (x + dx * 0.1) % (2*np.pi)
            y = (y + dy * 0.1) % (2*np.pi)
            
            # Transform ke koordinat lokal orbit
            local_x = orbit_cx + 6 * (x/np.pi - 1)
            local_y = orbit_cy + 6 * (y/np.pi - 1)
            orbit_points.append((local_x, local_y))
        
        # Plot orbit
        orbit_x = [p[0] for p in orbit_points]
        orbit_y = [p[1] for p in orbit_points]
        
        for i in range(0, len(orbit_points) - 20, 10):
            seg_x = orbit_x[i:i+20]
            seg_y = orbit_y[i:i+20]
            
            alpha = 0.1 + 0.2 * (i / len(orbit_points))
            lw = 0.2 + 0.3 * (1 - i / len(orbit_points))
            
            ax.plot(seg_x, seg_y, color="black", linewidth=lw, alpha=alpha)
            
            min_x, max_x = min(min_x, min(seg_x)), max(max_x, max(seg_x))
            min_y, max_y = min(min_y, min(seg_y)), max(max_y, max(seg_y))
    
    # Layer 6: Strange attractor basins
    print("Generating attractor basins...")
    n_basins = 6
    
    for basin_idx in range(n_basins):
        basin_angle = basin_idx * 2 * np.pi / n_basins + np.pi/6
        basin_radius = 25
        basin_cx = center_x + basin_radius * np.cos(basin_angle)
        basin_cy = center_y + basin_radius * np.sin(basin_angle)
        
        # Basin of attraction (daerah tarikan)
        n_basin_points = 300
        
        for _ in range(n_basin_points):
            # Titik awal acak
            start_x = basin_cx + np.random.uniform(-8, 8)
            start_y = basin_cy + np.random.uniform(-8, 8)
            
            # Simulasi iterasi menuju attractor
            x, y = start_x, start_y
            trajectory = []
            
            for step in range(50):
                # Persamaan yang menarik ke pusat basin
                dx = (basin_cx - x) * 0.1 + np.random.uniform(-0.3, 0.3)
                dy = (basin_cy - y) * 0.1 + np.random.uniform(-0.3, 0.3)
                
                x += dx
                y += dy
                trajectory.append((x, y))
            
            # Plot trajectory
            traj_x = [p[0] for p in trajectory]
            traj_y = [p[1] for p in trajectory]
            
            alpha = 0.05 + 0.1 * np.random.random()
            lw = 0.1 + 0.2 * np.random.random()
            
            ax.plot(traj_x, traj_y, color="black", linewidth=lw, alpha=alpha)
            
            min_x, max_x = min(min_x, min(traj_x)), max(max_x, max(traj_x))
            min_y, max_y = min(min_y, min(traj_y)), max(max_y, max(traj_y))
        
        # Pusat basin
        ax.plot(basin_cx, basin_cy, marker="o", markersize=1.5, 
                color="black", alpha=0.8)
    
    # Layer 7: Chaotic mixing dan transport
    print("Generating chaotic mixing...")
    n_mixing = 4
    
    for mix_idx in range(n_mixing):
        mix_angle = mix_idx * 2 * np.pi / n_mixing
        mix_radius = 35
        mix_cx = center_x + mix_radius * np.cos(mix_angle)
        mix_cy = center_y + mix_radius * np.sin(mix_angle)
        
        # Pola mixing chaotic (seperti adveksi)
        n_streamlines = 12
        
        for stream in range(n_streamlines):
            stream_angle = stream * 2 * np.pi / n_streamlines
            stream_length = 60
            
            streamline_x = []
            streamline_y = []
            
            x, y = mix_cx, mix_cy
            
            for _ in range(stream_length):
                # Velocity field chaotic
                u = np.sin(y/10) + 0.3 * np.cos(x/8)
                v = np.cos(x/10) + 0.3 * np.sin(y/8)
                
                x += u * 0.8
                y += v * 0.8
                
                streamline_x.append(x)
                streamline_y.append(y)
            
            # Plot streamline
            alpha = 0.06 + 0.12 * (stream / n_streamlines)
            lw = 0.2 + 0.3 * (stream / n_streamlines)
            
            ax.plot(streamline_x, streamline_y, color="black", 
                   linewidth=lw, alpha=alpha)
            
            min_x, max_x = min(min_x, min(streamline_x)), max(max_x, max(streamline_x))
            min_y, max_y = min(min_y, min(streamline_y)), max(max_y, max(streamline_y))
    
    # Framing dinamis
    cx_final = (min_x + max_x) / 2.0
    cy_final = (min_y + max_y) / 2.0
    w = max_x - min_x
    h = max_y - min_y
    pad = max(w, h) / 2.0 + 2.0
    
    ax.set_xlim(cx_final - pad, cx_final + pad)
    ax.set_ylim(cy_final - pad, cy_final + pad)
    
    save(fig, "chaotic strange attractor")


if __name__ == "__main__":
    chaotic_strange_attractor()