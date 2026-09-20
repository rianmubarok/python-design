import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime

SIZE = 4000
DPI = 300
SEED = 42
DATE = datetime.now().strftime("%d%m%Y")

SCRIPT DIR = Path(  file  ).resolve().parent
OUTPUT DIR = SCRIPT DIR.parent / "output"
JPG DIR = OUTPUT DIR / "jpg"
SVG DIR = OUTPUT DIR / "svg"
JPG DIR.mkdir(parents=True, exist ok=True)
SVG DIR.mkdir(parents=True, exist ok=True)

np.random.seed(SEED)


def setup ax():
    fig, ax = plt.subplots(figsize=(SIZE / DPI, SIZE / DPI), dpi=DPI)
    fig.subplots adjust(left=0, right=1, top=1, bottom=0)
    ax.set facecolor("white")
    ax.set aspect("equal")
    ax.axis("off")
    return fig, ax


def save(fig, name):
    jpg path = JPG DIR / f"{name} {DATE}.jpg"
    svg path = SVG DIR / f"{name} {DATE}.svg"
    fig.savefig(jpg path, dpi=DPI, pad inches=0, facecolor="white")
    fig.savefig(svg path, format="svg", pad inches=0, facecolor="white")
    plt.close(fig)
    print(f"Tersimpan: {jpg path} | {svg path}")


def lorenz attractor(steps=10000, dt=0.01, sigma=10, rho=28, beta=8/3):
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
    x norm = 50 + 25 * (x - x.mean()) / x.std()
    y norm = 50 + 25 * (y - y.mean()) / y.std()
    
    return x norm, y norm


def rossler attractor(steps=8000, dt=0.05, a=0.2, b=0.2, c=5.7):
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
    
    x norm = 50 + 20 * (x - x.mean()) / x.std()
    y norm = 50 + 20 * (y - y.mean()) / y.std()
    
    return x norm, y norm


def clifford attractor(steps=20000, a=-1.7, b=1.8, c=-1.9, d=-0.4):
    """Simulasi attractor Clifford (map 2D)."""
    x = np.zeros(steps)
    y = np.zeros(steps)
    
    x[0], y[0] = 0.1, 0.1
    
    for i in range(steps - 1):
        x[i+1] = np.sin(a * y[i]) + c * np.cos(a * x[i])
        y[i+1] = np.sin(b * x[i]) + d * np.cos(b * y[i])
    
    x norm = 50 + 30 * x
    y norm = 50 + 30 * y
    
    return x norm, y norm


def chaotic strange attractor():
    """Sistem chaos dengan multiple strange attractors dan bifurkasi."""
    fig, ax = setup ax()
    
    center x, center y = 50, 50
    
    min x, max x = float("inf"), float("-inf")
    min y, max y = float("inf"), float("-inf")
    
    # Layer 1: Lorenz attractor (sistem chaos 3D)
    print("Generating Lorenz attractor...")
    x lorenz, y lorenz = lorenz attractor(steps=12000)
    
    # Plot Lorenz dengan density-based coloring
    n lorenz = len(x lorenz)
    for i in range(0, n lorenz - 100, 50):
        segment x = x lorenz[i:i+100]
        segment y = y lorenz[i:i+100]
        
        # Alpha berdasarkan density lokal
        local density = min(100, len(segment x))
        alpha = 0.1 + 0.3 * (local density / 100)
        lw = 0.3 + 0.4 * (i / n lorenz)
        
        ax.plot(segment x, segment y, color="black", linewidth=lw, alpha=alpha)
        
        # Update bounding box
        min x, max x = min(min x, segment x.min()), max(max x, segment x.max())
        min y, max y = min(min y, segment y.min()), max(max y, segment y.max())
    
    # Layer 2: Rössler attractor
    print("Generating Rössler attractor...")
    x rossler, y rossler = rossler attractor(steps=10000)
    
    # Transformasi untuk posisi berbeda
    x rossler trans = 50 + 0.8 * (x rossler - 50) + 15
    y rossler trans = 50 + 0.8 * (y rossler - 50) - 15
    
    n rossler = len(x rossler trans)
    for i in range(0, n rossler - 80, 40):
        segment x = x rossler trans[i:i+80]
        segment y = y rossler trans[i:i+80]
        
        alpha = 0.08 + 0.25 * (i / n rossler)
        lw = 0.2 + 0.3 * (1 - i / n rossler)
        
        ax.plot(segment x, segment y, color="black", linewidth=lw, alpha=alpha)
        
        min x, max x = min(min x, segment x.min()), max(max x, segment x.max())
        min y, max y = min(min y, segment y.min()), max(max y, segment y.max())
    
    # Layer 3: Clifford attractor
    print("Generating Clifford attractor...")
    x clifford, y clifford = clifford attractor(steps=15000)
    
    x clifford trans = 50 + 0.7 * (x clifford - 50) - 20
    y clifford trans = 50 + 0.7 * (y clifford - 50) + 20
    
    n clifford = len(x clifford trans)
    
    # Plot dengan pendekatan point-based untuk pola fractal
    for i in range(0, n clifford, 10):
        x val = x clifford trans[i]
        y val = y clifford trans[i]
        
        # Ukuran titik berdasarkan posisi dalam sequence
        marker size = 0.1 + 0.3 * (i / n clifford)
        alpha = 0.05 + 0.15 * (1 - abs(i/n clifford - 0.5))
        
        ax.plot(x val, y val, marker=".", markersize=marker size, 
                color="black", alpha=alpha)
        
        min x, max x = min(min x, x val), max(max x, x val)
        min y, max y = min(min y, y val), max(max y, y val)
    
    # Layer 4: Bifurkasi diagram (simulasi logistic map)
    print("Generating bifurcation diagram...")
    n bifurcation = 200
    r values = np.linspace(2.5, 4.0, n bifurcation)
    bif x = []
    bif y = []
    
    for r idx, r in enumerate(r values):
        # Logistic map: x {n+1} = r * x n * (1 - x n)
        x = 0.5  # Nilai awal
        transient = 200  # Iterasi transient
        collect = 100    # Iterasi yang dikumpulkan
        
        for   in range(transient):
            x = r * x * (1 - x)
        
        for   in range(collect):
            x = r * x * (1 - x)
            bif x.append(50 + 25 * (r idx / n bifurcation - 0.5))
            bif y.append(50 + 40 * (x - 0.5))
    
    bif x = np.array(bif x)
    bif y = np.array(bif y)
    
    # Plot bifurkasi sebagai titik-titik
    for i in range(0, len(bif x), 5):
        x val = bif x[i]
        y val = bif y[i]
        
        ax.plot(x val, y val, marker=".", markersize=0.2, 
                color="black", alpha=0.3)
        
        min x, max x = min(min x, x val), max(max x, x val)
        min y, max y = min(min y, y val), max(max y, y val)
    
    # Layer 5: Chaotic orbits (Poincaré sections)
    print("Generating chaotic orbits...")
    n orbits = 8
    orbit centers = []
    
    for orbit idx in range(n orbits):
        orbit angle = orbit idx * 2 * np.pi / n orbits
        orbit radius = 15 + np.random.uniform(-3, 3)
        orbit cx = center x + orbit radius * np.cos(orbit angle)
        orbit cy = center y + orbit radius * np.sin(orbit angle)
        orbit centers.append((orbit cx, orbit cy))
        
        # Simulasi orbit chaotic
        n orbit points = 800
        orbit points = []
        
        # Persamaan diferensial chaotic sederhana
        x, y = 0.1, 0.1
        for   in range(n orbit points):
            dx = np.sin(y) + np.random.uniform(-0.1, 0.1)
            dy = np.cos(x) + np.random.uniform(-0.1, 0.1)
            
            x = (x + dx * 0.1) % (2*np.pi)
            y = (y + dy * 0.1) % (2*np.pi)
            
            # Transform ke koordinat lokal orbit
            local x = orbit cx + 6 * (x/np.pi - 1)
            local y = orbit cy + 6 * (y/np.pi - 1)
            orbit points.append((local x, local y))
        
        # Plot orbit
        orbit x = [p[0] for p in orbit points]
        orbit y = [p[1] for p in orbit points]
        
        for i in range(0, len(orbit points) - 20, 10):
            seg x = orbit x[i:i+20]
            seg y = orbit y[i:i+20]
            
            alpha = 0.1 + 0.2 * (i / len(orbit points))
            lw = 0.2 + 0.3 * (1 - i / len(orbit points))
            
            ax.plot(seg x, seg y, color="black", linewidth=lw, alpha=alpha)
            
            min x, max x = min(min x, min(seg x)), max(max x, max(seg x))
            min y, max y = min(min y, min(seg y)), max(max y, max(seg y))
    
    # Layer 6: Strange attractor basins
    print("Generating attractor basins...")
    n basins = 6
    
    for basin idx in range(n basins):
        basin angle = basin idx * 2 * np.pi / n basins + np.pi/6
        basin radius = 25
        basin cx = center x + basin radius * np.cos(basin angle)
        basin cy = center y + basin radius * np.sin(basin angle)
        
        # Basin of attraction (daerah tarikan)
        n basin points = 300
        
        for   in range(n basin points):
            # Titik awal acak
            start x = basin cx + np.random.uniform(-8, 8)
            start y = basin cy + np.random.uniform(-8, 8)
            
            # Simulasi iterasi menuju attractor
            x, y = start x, start y
            trajectory = []
            
            for step in range(50):
                # Persamaan yang menarik ke pusat basin
                dx = (basin cx - x) * 0.1 + np.random.uniform(-0.3, 0.3)
                dy = (basin cy - y) * 0.1 + np.random.uniform(-0.3, 0.3)
                
                x += dx
                y += dy
                trajectory.append((x, y))
            
            # Plot trajectory
            traj x = [p[0] for p in trajectory]
            traj y = [p[1] for p in trajectory]
            
            alpha = 0.05 + 0.1 * np.random.random()
            lw = 0.1 + 0.2 * np.random.random()
            
            ax.plot(traj x, traj y, color="black", linewidth=lw, alpha=alpha)
            
            min x, max x = min(min x, min(traj x)), max(max x, max(traj x))
            min y, max y = min(min y, min(traj y)), max(max y, max(traj y))
        
        # Pusat basin
        ax.plot(basin cx, basin cy, marker="o", markersize=1.5, 
                color="black", alpha=0.8)
    
    # Layer 7: Chaotic mixing dan transport
    print("Generating chaotic mixing...")
    n mixing = 4
    
    for mix idx in range(n mixing):
        mix angle = mix idx * 2 * np.pi / n mixing
        mix radius = 35
        mix cx = center x + mix radius * np.cos(mix angle)
        mix cy = center y + mix radius * np.sin(mix angle)
        
        # Pola mixing chaotic (seperti adveksi)
        n streamlines = 12
        
        for stream in range(n streamlines):
            stream angle = stream * 2 * np.pi / n streamlines
            stream length = 60
            
            streamline x = []
            streamline y = []
            
            x, y = mix cx, mix cy
            
            for   in range(stream length):
                # Velocity field chaotic
                u = np.sin(y/10) + 0.3 * np.cos(x/8)
                v = np.cos(x/10) + 0.3 * np.sin(y/8)
                
                x += u * 0.8
                y += v * 0.8
                
                streamline x.append(x)
                streamline y.append(y)
            
            # Plot streamline
            alpha = 0.06 + 0.12 * (stream / n streamlines)
            lw = 0.2 + 0.3 * (stream / n streamlines)
            
            ax.plot(streamline x, streamline y, color="black", 
                   linewidth=lw, alpha=alpha)
            
            min x, max x = min(min x, min(streamline x)), max(max x, max(streamline x))
            min y, max y = min(min y, min(streamline y)), max(max y, max(streamline y))
    
    # Framing dinamis
    cx final = (min x + max x) / 2.0
    cy final = (min y + max y) / 2.0
    w = max x - min x
    h = max y - min y
    pad = max(w, h) / 2.0 + 2.0
    
    ax.set xlim(cx final - pad, cx final + pad)
    ax.set ylim(cy final - pad, cy final + pad)
    
    save(fig, "chaotic strange attractor")


if   name   == "  main  ":
    chaotic strange attractor()