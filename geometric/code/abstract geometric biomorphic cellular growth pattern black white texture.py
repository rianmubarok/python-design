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


def grow cell(cx, cy, generation, max generations, parent angle=None):
    """Simulasi pertumbuhan sel biomorfik."""
    cells = []
    
    # Ukuran sel berdasarkan generasi
    cell size = 2.0 + 1.5 * (max generations - generation)
    
    # Bentuk sel (tidak sempurna, organik)
    n points = 12 + generation * 2
    theta = np.linspace(0, 2 * np.pi, n points)
    
    # Variasi bentuk organik
    radius variation = np.random.uniform(0.8, 1.2, n points)
    modulated radius = cell size * radius variation
    
    x cell = cx + modulated radius * np.cos(theta)
    y cell = cy + modulated radius * np.sin(theta)
    
    cells.append((x cell, y cell, cx, cy, cell size, generation))
    
    # Pembelahan sel (mitosis)
    if generation < max generations:
        # Arah pembelahan
        if parent angle is None:
            mitosis angle = np.random.uniform(0, 2 * np.pi)
        else:
            mitosis angle = parent angle + np.random.uniform(-np.pi/4, np.pi/4)
        
        # Posisi sel anak
        child distance = cell size * 2.5
        
        for i in range(2):  # Dua sel anak
            child angle = mitosis angle + i * np.pi
            child cx = cx + child distance * np.cos(child angle)
            child cy = cy + child distance * np.sin(child angle)
            
            # Pertumbuhan rekursif
            child cells = grow cell(child cx, child cy, generation + 1, 
                                   max generations, child angle)
            cells.extend(child cells)
    
    return cells


def biomorphic cellular growth():
    """Pola pertumbuhan sel biomorfik dengan pembelahan mitosis dan diferensiasi."""
    fig, ax = setup ax()
    
    center x, center y = 50, 50
    
    min x, max x = float("inf"), float("-inf")
    min y, max y = float("inf"), float("-inf")
    
    # Layer 1: Sel induk (stem cells)
    n stem cells = 5
    stem cells = []
    
    for i in range(n stem cells):
        angle = i * 2 * np.pi / n stem cells
        distance = 8
        stem x = center x + distance * np.cos(angle)
        stem y = center y + distance * np.sin(angle)
        
        # Sel induk (besar, kompleks)
        stem size = 4.0
        n stem points = 20
        theta stem = np.linspace(0, 2 * np.pi, n stem points)
        
        # Bentuk tidak beraturan organik
        stem modulation = 1 + 0.3 * np.sin(5 * theta stem + i)
        x stem = stem x + stem size * stem modulation * np.cos(theta stem)
        y stem = stem y + stem size * stem modulation * np.sin(theta stem)
        
        ax.plot(x stem, y stem, color="black", linewidth=1.5, alpha=0.9)
        
        # Update bounding box
        min x, max x = min(min x, x stem.min()), max(max x, x stem.max())
        min y, max y = min(min y, y stem.min()), max(max y, y stem.max())
        
        # Nukleus (inti sel)
        nucleus size = stem size * 0.4
        x nucleus = stem x + nucleus size * np.cos(theta stem)
        y nucleus = stem y + nucleus size * np.sin(theta stem)
        
        ax.plot(x nucleus, y nucleus, color="black", linewidth=0.8, alpha=0.7)
        
        stem cells.append((stem x, stem y, stem size))
    
    # Layer 2: Pertumbuhan sel diferensiasi
    all cells = []
    
    for stem x, stem y, stem size in stem cells:
        # Pertumbuhan dari sel induk
        max generations = 4
        cells from stem = grow cell(stem x, stem y, 0, max generations)
        all cells.extend(cells from stem)
    
    # Gambar semua sel
    for x cell, y cell, cx, cy, cell size, generation in all cells:
        # Ketebalan berdasarkan generasi (sel lebih tua lebih tebal)
        lw = 0.6 + 0.4 * (max generations - generation) / max generations
        alpha = 0.5 + 0.3 * (max generations - generation) / max generations
        
        ax.plot(x cell, y cell, color="black", linewidth=lw, alpha=alpha)
        
        # Update bounding box
        min x, max x = min(min x, x cell.min()), max(max x, x cell.max())
        min y, max y = min(min y, y cell.min()), max(max y, y cell.max())
        
        # Organel dalam sel (berdasarkan jenis sel)
        if generation % 3 == 0:
            # Mitokondria (organel energi)
            n mito = 3
            for m in range(n mito):
                mito angle = m * 2 * np.pi / n mito
                mito distance = cell size * 0.6
                mito x = cx + mito distance * np.cos(mito angle)
                mito y = cy + mito distance * np.sin(mito angle)
                
                # Bentuk mitokondria (lonjong)
                mito size = cell size * 0.2
                mito points = 8
                theta mito = np.linspace(0, 2 * np.pi, mito points)
                
                x mito = mito x + mito size * (1 + 0.3 * np.cos(2*theta mito)) * np.cos(theta mito)
                y mito = mito y + mito size * (1 + 0.3 * np.cos(2*theta mito)) * np.sin(theta mito)
                
                ax.plot(x mito, y mito, color="black", linewidth=0.3, alpha=0.6)
        
        if generation % 4 == 1:
            # Retikulum endoplasma
            n er = 4
            for e in range(n er):
                er angle = e * 2 * np.pi / n er
                er distance = cell size * 0.4
                er x = cx + er distance * np.cos(er angle)
                er y = cy + er distance * np.sin(er angle)
                
                # Bentuk retikulum (berliku-liku)
                er size = cell size * 0.15
                er points = 20
                theta er = np.linspace(0, 2 * np.pi, er points)
                
                # Modulasi untuk bentuk berliku
                er mod = 1 + 0.2 * np.sin(8 * theta er)
                x er = er x + er size * er mod * np.cos(theta er)
                y er = er y + er size * er mod * np.sin(theta er)
                
                ax.plot(x er, y er, color="black", linewidth=0.2, alpha=0.5, linestyle="--")
    
    # Layer 3: Jaringan penghubung (extracellular matrix)
    n connections = 80
    
    for   in range(n connections):
        # Pilih dua sel acak untuk dihubungkan
        if len(all cells) < 2:
            continue
            
        idx1, idx2 = np.random.choice(len(all cells), 2, replace=False)
        cell1 = all cells[idx1]
        cell2 = all cells[idx2]
        
        cx1, cy1 = cell1[2], cell1[3]
        cx2, cy2 = cell2[2], cell2[3]
        
        # Jarak antara sel
        distance = np.sqrt((cx1 - cx2)**2 + (cy1 - cy2)**2)
        
        # Hanya hubungkan sel yang cukup dekat
        if distance < 25:
            # Garis penghubung dengan pola organik
            n connect points = 15
            t connect = np.linspace(0, 1, n connect points)
            
            # Kurva dengan variasi sinusoidal
            wave freq = np.random.uniform(2, 5)
            wave amp = np.random.uniform(0.5, 2.0)
            
            connect x = []
            connect y = []
            
            for t in t connect:
                # Posisi linear
                base x = cx1 + (cx2 - cx1) * t
                base y = cy1 + (cy2 - cy1) * t
                
                # Offset sinusoidal
                perp x = (cy2 - cy1) / distance
                perp y = -(cx2 - cx1) / distance
                
                wave = wave amp * np.sin(wave freq * t * np.pi)
                
                connect x.append(base x + perp x * wave)
                connect y.append(base y + perp y * wave)
            
            ax.plot(connect x, connect y, color="black", linewidth=0.3, alpha=0.4)
    
    # Layer 4: Pembelahan mitosis aktif
    n active mitosis = 6
    
    for i in range(n active mitosis):
        mitosis angle = i * 2 * np.pi / n active mitosis
        mitosis radius = 30
        mitosis x = center x + mitosis radius * np.cos(mitosis angle)
        mitosis y = center y + mitosis radius * np.sin(mitosis angle)
        
        # Sel yang sedang membelah
        parent size = 3.0
        n parent points = 16
        theta parent = np.linspace(0, 2 * np.pi, n parent points)
        
        # Bentuk sel yang memanjang sebelum pembelahan
        elongation = 1 + 0.5 * np.cos(2 * theta parent)
        x parent = mitosis x + parent size * elongation * np.cos(theta parent + mitosis angle)
        y parent = mitosis y + parent size * elongation * np.sin(theta parent + mitosis angle)
        
        ax.plot(x parent, y parent, color="black", linewidth=1.0, alpha=0.8)
        
        # Garis pembelahan
        cleavage length = parent size * 1.8
        cleavage x = [mitosis x - cleavage length * np.cos(mitosis angle),
                     mitosis x + cleavage length * np.cos(mitosis angle)]
        cleavage y = [mitosis y - cleavage length * np.sin(mitosis angle),
                     mitosis y + cleavage length * np.sin(mitosis angle)]
        
        ax.plot(cleavage x, cleavage y, color="black", linewidth=0.6, alpha=0.7, linestyle=":")
        
        # Sel anak yang baru terbentuk
        for child in range(2):
            child angle = mitosis angle + child * np.pi
            child distance = parent size * 1.2
            child x = mitosis x + child distance * np.cos(child angle)
            child y = mitosis y + child distance * np.sin(child angle)
            
            child size = parent size * 0.6
            n child points = 12
            theta child = np.linspace(0, 2 * np.pi, n child points)
            
            x child = child x + child size * np.cos(theta child)
            y child = child y + child size * np.sin(theta child)
            
            ax.plot(x child, y child, color="black", linewidth=0.5, alpha=0.6)
            
            # Update bounding box
            min x, max x = min(min x, x child.min()), max(max x, x child.max())
            min y, max y = min(min y, y child.min()), max(max y, y child.max())
    
    # Layer 5: Apoptosis (kematian sel terprogram)
    n apoptosis = 4
    
    for i in range(n apoptosis):
        apo angle = i * 2 * np.pi / n apoptosis + np.pi/4
        apo radius = 35
        apo x = center x + apo radius * np.cos(apo angle)
        apo y = center y + apo radius * np.sin(apo angle)
        
        # Sel yang mengalami apoptosis
        apo size = 2.5
        n apo points = 20
        theta apo = np.linspace(0, 2 * np.pi, n apo points)
        
        # Bentuk tidak beraturan (sel sekarat)
        apo modulation = 1 + 0.4 * np.random.uniform(-1, 1, n apo points)
        x apo = apo x + apo size * apo modulation * np.cos(theta apo)
        y apo = apo y + apo size * apo modulation * np.sin(theta apo)
        
        ax.plot(x apo, y apo, color="black", linewidth=0.7, alpha=0.6, linestyle="--")
        
        # Fragmen sel (apoptotic bodies)
        n fragments = 5
        for f in range(n fragments):
            frag angle = apo angle + f * 2 * np.pi / n fragments
            frag distance = apo size * 1.5
            frag x = apo x + frag distance * np.cos(frag angle)
            frag y = apo y + frag distance * np.sin(frag angle)
            
            frag size = apo size * 0.3
            n frag points = 8
            theta frag = np.linspace(0, 2 * np.pi, n frag points)
            
            x frag = frag x + frag size * np.cos(theta frag)
            y frag = frag y + frag size * np.sin(theta frag)
            
            ax.plot(x frag, y frag, color="black", linewidth=0.3, alpha=0.4)
            
            # Update bounding box
            min x, max x = min(min x, x frag.min()), max(max x, x frag.max())
            min y, max y = min(min y, y frag.min()), max(max y, y frag.max())
    
    # Framing dinamis
    cx final = (min x + max x) / 2.0
    cy final = (min y + max y) / 2.0
    w = max x - min x
    h = max y - min y
    pad = max(w, h) / 2.0 + 3.0
    
    ax.set xlim(cx final - pad, cx final + pad)
    ax.set ylim(cy final - pad, cy final + pad)
    
    save(fig, "abstract geometric biomorphic cellular growth pattern black white texture"))


if   name   == "  main  ":
    biomorphic cellular growth()