import sys

for f in sys.argv[1:]:
    with open(f, 'r') as file:
        content = file.read()
    
    if 'all_x = []' in content:
        print(f'{f} already patched')
        continue

    injection = '''
    all_x = []
    all_y = []
    for line in ax.lines:
        all_x.extend(line.get_xdata())
        all_y.extend(line.get_ydata())
    for patch in ax.patches:
        if hasattr(patch, 'get_path'):
            vertices = patch.get_path().vertices
            all_x.extend(vertices[:, 0])
            all_y.extend(vertices[:, 1])
            
    if all_x and all_y:
        cx = (min(all_x) + max(all_x)) / 2
        cy = (min(all_y) + max(all_y)) / 2
        ax.set_xlim(cx - 55, cx + 55)
        ax.set_ylim(cy - 55, cy + 55)
        
    save(fig,'''
    
    content = content.replace('    save(fig,', injection)
    
    with open(f, 'w') as file:
        file.write(content)
        
    print(f'Patched {f}')
