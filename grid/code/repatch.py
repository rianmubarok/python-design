import sys
import re

for f in sys.argv[1:]:
    try:
        with open(f, 'r') as file:
            content = file.read()
            
        old_injection = '''    all_x = []
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
        ax.set_ylim(cy - 55, cy + 55)'''

        new_injection = '''    all_x = []
    all_y = []
    for line in ax.lines:
        all_x.extend(line.get_xdata())
        all_y.extend(line.get_ydata())
    for patch in ax.patches:
        if hasattr(patch, 'get_patch_transform') and hasattr(patch, 'get_path'):
            trans = patch.get_patch_transform()
            path = patch.get_path()
            vertices = trans.transform_path(path).vertices
            all_x.extend(vertices[:, 0])
            all_y.extend(vertices[:, 1])
        elif hasattr(patch, 'get_path'):
            vertices = patch.get_path().vertices
            all_x.extend(vertices[:, 0])
            all_y.extend(vertices[:, 1])
            
    if all_x and all_y:
        cx = (min(all_x) + max(all_x)) / 2
        cy = (min(all_y) + max(all_y)) / 2
        ax.set_xlim(cx - 55, cx + 55)
        ax.set_ylim(cy - 55, cy + 55)'''
        
        if old_injection in content:
            content = content.replace(old_injection, new_injection)
            with open(f, 'w') as file:
                file.write(content)
            print(f'Repatched {f}')
        else:
            print(f'Could not find old injection in {f}')
    except FileNotFoundError:
        print(f'File not found: {f}')
