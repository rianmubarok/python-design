import subprocess

scripts = [
    'abstract concentric cellular mitosis division growth pattern black white texture.py',
    'abstract concentric fibonacci spiral golden ratio organic pattern black white texture.py',
    'abstract concentric geometric dual axis ellipse orbital dance pattern black white texture.py',
    'abstract concentric geometric octagon morph triangle transition pattern black white texture.py',
    'abstract concentric geometric star polygon recursive fractal pattern black white texture.py',
    'abstract concentric magnetic field twisted vortex pattern black white texture.py',
    'abstract concentric quantum interference hologram pattern black white texture.py',
    'abstract concentric ripple interference micro macro scale pattern black white texture.py',
    'abstract concentric seamless tiling modular wave pattern black white texture.py',
    'abstract concentric sonic boom shockwave propagation pattern black white texture.py',
    'abstract concentric time dilation relativistic space warp pattern black white texture.py',
    'abstract concentric torus knot topology hypersphere pattern black white texture.py',
]

for s in scripts:
    with open(s, 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace('DATE = datetime.now().strftime("%d%m%Y")', 'DATE = "19092026"')
    with open(s, 'w', encoding='utf-8') as f:
        f.write(content)
    subprocess.run(['python', s], capture_output=True)
    content = content.replace('DATE = "19092026"', 'DATE = datetime.now().strftime("%d%m%Y")')
    with open(s, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Generated 19092026: {s}')