import re
from pathlib import Path

files = list(Path('.').glob('*.py'))
for f in files:
    if f.name in ('fix_eps_size.py', 'fix_eps_size2.py', 'fix_eps_size3.py', 'update_eps.py', 'restore_19092026.py', 'update_eps2.py'):
        continue
    content = f.read_text(encoding='utf-8')

    # Use regex to find and replace save function
    def replace_save(match):
        func = match.group(0)
        if 'fig.set_size_inches(30, 30)' in func:
            return func
        # Add the EPS size fix before fig.savefig(eps_path...
        func = func.replace(
            'fig.savefig(eps_path, format="eps", pad_inches=0, facecolor="white")',
            '# Save EPS with larger figure size for 4MP+ bounding box\n    orig_size = fig.get_size_inches()\n    fig.set_size_inches(30, 30)\n    fig.savefig(eps_path, format="eps", pad_inches=0, facecolor="white", dpi=DPI)\n    fig.set_size_inches(orig_size[0], orig_size[1])'
        )
        return func

    # Find save function
    new_content = re.sub(
        r'def save\(fig, name\):.*?(?=\n\ndef |\nif __name__|$)',
        replace_save,
        content,
        flags=re.DOTALL
    )

    if new_content != content:
        f.write_text(new_content, encoding='utf-8')
        print('Updated:', f.name)

print('Done!')