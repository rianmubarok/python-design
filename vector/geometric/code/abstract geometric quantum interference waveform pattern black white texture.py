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


def quantum interference waveform():
    """Pola interferensi kuantum dengan gelombang probabilistik dan kolaps fungsi gelombang."""
    fig, ax = setup ax()
    
    center x, center y = 50, 50
    
    min x, max x = float("inf"), float("-inf")
    min y, max y = float("inf"), float("-inf")
    
    # Parameter sistem kuantum
    n energy levels = 8
    n wave points = 200
    
    # Layer 1: Orbital elektron (fungsi gelombang probabilistik)
    for level in range(n energy levels):
        energy = level + 1
        orbital radius = 5 + energy * 4.5
        
        # Fungsi gelombang radial (probabilitas)
        theta = np.linspace(0, 2 * np.pi, n wave points)
        
        for harmonic in range(1, 4):  # Harmonik orbital
            # Fungsi gelombang dengan interferensi
            wave function = np.sin(energy * theta * harmonic) * np.cos(harmonic * theta * 2)
            probability density = np.abs(wave function) ** 2
            
            # Radius orbital dengan modulasi gelombang
            modulated radius = orbital radius * (1 + 0.15 * probability density)
            
            x orbital = center x + modulated radius * np.cos(theta)
            y orbital = center y + modulated radius * np.sin(theta)
            
            # Ketebalan berdasarkan probabilitas
            lw = 0.4 + 0.8 * (probability density.max() / 2)
            alpha = 0.3 + 0.4 * (level / n energy levels)
            
            ax.plot(x orbital, y orbital, color="black", linewidth=lw, alpha=alpha)
            
            # Update bounding box
            min x, max x = min(min x, x orbital.min()), max(max x, x orbital.max())
            min y, max y = min(min y, y orbital.min()), max(max y, y orbital.max())
            
            # Titik kuantum (partikel teramati)
            if np.random.random() < 0.3:  # Probabilitas observasi
                obs theta = np.random.choice(theta)
                obs radius = orbital radius * (1 + 0.15 * np.abs(np.sin(energy * obs theta * harmonic)))
                obs x = center x + obs radius * np.cos(obs theta)
                obs y = center y + obs radius * np.sin(obs theta)
                
                # Ukuran titik berdasarkan tingkat energi
                marker size = 0.5 + 0.8 * (energy / n energy levels)
                ax.plot(obs x, obs y, marker="o", markersize=marker size, 
                        color="black", alpha=0.7)
    
    # Layer 2: Interferensi gelombang de Broglie
    n interference sources = 5
    source positions = []
    
    for i in range(n interference sources):
        angle = i * 2 * np.pi / n interference sources
        distance = 15 + np.random.uniform(-3, 3)
        source x = center x + distance * np.cos(angle)
        source y = center y + distance * np.sin(angle)
        source positions.append((source x, source y))
        
        # Sumber gelombang
        ax.plot(source x, source y, marker="*", markersize=3, 
                color="black", alpha=0.9)
    
    # Pola interferensi
    grid size = 80
    x grid = np.linspace(center x - 25, center x + 25, grid size)
    y grid = np.linspace(center y - 25, center y + 25, grid size)
    
    interference intensity = np.zeros((grid size, grid size))
    
    for i, sx in enumerate(x grid):
        for j, sy in enumerate(y grid):
            total wave = 0
            for source x, source y in source positions:
                distance = np.sqrt((sx - source x)**2 + (sy - source y)**2)
                wavelength = 3.0 + np.random.uniform(0.5, 1.5)
                phase = 2 * np.pi * distance / wavelength
                total wave += np.cos(phase)
            
            interference intensity[j, i] = np.abs(total wave) / n interference sources
    
    # Kontur interferensi
    levels = np.linspace(0.1, 0.9, 8)
    contour = ax.contour(x grid, y grid, interference intensity, levels=levels,
                        colors="black", linewidths=0.6, alpha=0.5)
    
    # Update bounding box dari grid (simpler approach)
    min x, max x = min(min x, x grid.min()), max(max x, x grid.max())
    min y, max y = min(min y, y grid.min()), max(max y, y grid.max())
    
    # Layer 3: Kolaps fungsi gelombang (pengukuran kuantum)
    n measurements = 12
    measurement angles = np.linspace(0, 2 * np.pi, n measurements, endpoint=False)
    
    for i, angle in enumerate(measurement angles):
        measurement radius = 32
        measurement x = center x + measurement radius * np.cos(angle)
        measurement y = center y + measurement radius * np.sin(angle)
        
        # "Pengukuran" menyebabkan kolaps
        collapse lines = 8
        for line in range(collapse lines):
            line angle = angle + line * (2 * np.pi / collapse lines)
            line length = 6 + np.random.uniform(0, 3)
            
            end x = measurement x + line length * np.cos(line angle)
            end y = measurement y + line length * np.sin(line angle)
            
            ax.plot([measurement x, end x], [measurement y, end y], 
                   color="black", linewidth=0.5, alpha=0.6)
        
        # Efek kolaps (gelombang berhenti)
        collapse waves = 5
        for wave in range(collapse waves):
            wave radius = 2 + wave * 1.5
            wave x = measurement x + wave radius * np.cos(angle + np.pi/2)
            wave y = measurement y + wave radius * np.sin(angle + np.pi/2)
            
            # Garis gelombang terputus
            ax.plot(wave x, wave y, marker="x", markersize=1.2, 
                    color="black", alpha=0.5)
    
    # Layer 4: Superposisi kuantum
    n superpositions = 6
    superposition radius = 18
    
    for i in range(n superpositions):
        super angle = i * 2 * np.pi / n superpositions
        super x = center x + superposition radius * np.cos(super angle)
        super y = center y + superposition radius * np.sin(super angle)
        
        # State superposisi (multiple states overlapping)
        n states = 3
        for state in range(n states):
            state angle = super angle + state * (2 * np.pi / n states)
            state radius = 4
            
            # State yang tumpang tindih
            state points = []
            for t in np.linspace(0, 2 * np.pi, 50):
                x state = super x + state radius * np.cos(t + state angle)
                y state = super y + state radius * np.sin(t + state angle)
                state points.append((x state, y state))
            
            state points.append(state points[0])  # Tutup loop
            x state = [p[0] for p in state points]
            y state = [p[1] for p in state points]
            
            ax.plot(x state, y state, color="black", linewidth=0.4, 
                    alpha=0.4, linestyle="--")
            
            # Update bounding box
            min x, max x = min(min x, min(x state)), max(max x, max(x state))
            min y, max y = min(min y, min(y state)), max(max y, max(y state))
    
    # Layer 5: Entanglement kuantum (keterkaitan)
    n entangled pairs = 4
    entanglement radius = 22
    
    for pair in range(n entangled pairs):
        angle1 = pair * 2 * np.pi / n entangled pairs
        angle2 = angle1 + np.pi / 2  # Partner entangled
        
        # Partikel entangled
        ent1 x = center x + entanglement radius * np.cos(angle1)
        ent1 y = center y + entanglement radius * np.sin(angle1)
        ent2 x = center x + entanglement radius * np.cos(angle2)
        ent2 y = center y + entanglement radius * np.sin(angle2)
        
        # Garis entanglement (keterkaitan)
        n ent lines = 15
        for line in range(n ent lines):
            t = line / (n ent lines - 1)
            
            # Kurva entanglement
            ent x = (1-t)**3 * ent1 x + 3*(1-t)**2*t*(ent1 x+3) + \
                   3*(1-t)*t**2*(ent2 x-3) + t**3*ent2 x
            ent y = (1-t)**3 * ent1 y + 3*(1-t)**2*t*(ent1 y+3) + \
                   3*(1-t)*t**2*(ent2 y-3) + t**3*ent2 y
            
            ax.plot(ent x, ent y, marker=".", markersize=0.3, 
                    color="black", alpha=0.3)
        
        # Partikel entangled
        ax.plot(ent1 x, ent1 y, marker="o", markersize=1.5, 
                color="black", alpha=0.8)
        ax.plot(ent2 x, ent2 y, marker="o", markersize=1.5, 
                color="black", alpha=0.8)
        
        # Update bounding box
        min x, max x = min(min x, ent1 x, ent2 x), max(max x, ent1 x, ent2 x)
        min y, max y = min(min y, ent1 y, ent2 y), max(max y, ent1 y, ent2 y)
    
    # Framing dinamis
    cx final = (min x + max x) / 2.0
    cy final = (min y + max y) / 2.0
    w = max x - min x
    h = max y - min y
    pad = max(w, h) / 2.0 + 3.0
    
    ax.set xlim(cx final - pad, cx final + pad)
    ax.set ylim(cy final - pad, cy final + pad)
    
    save(fig, "abstract geometric quantum interference waveform pattern black white texture"))


if   name   == "  main  ":
    quantum interference waveform()