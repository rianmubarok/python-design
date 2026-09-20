"""
Jalankan semua file Python halloween untuk generate ulang EPS dari Python langsung.
"""
import subprocess
import sys
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parent / "code"
py_files = sorted([f for f in CODE_DIR.glob("*.py") if f.name != "vector_icon.py"])

print(f"Total: {len(py_files)} file\n")

success = 0
errors = []

for i, fpath in enumerate(py_files, 1):
    print(f"[{i}/{len(py_files)}] {fpath.name[:70]}...")
    result = subprocess.run(
        [sys.executable, str(fpath)],
        capture_output=True, text=True, timeout=120
    )
    if result.returncode == 0:
        print(f"  OK")
        success += 1
    else:
        print(f"  ERROR: {result.stderr.strip()[-200:]}")
        errors.append((fpath.name, result.stderr.strip()[-200:]))

print(f"\n=== DONE: {success}/{len(py_files)} berhasil, {len(errors)} error ===")
if errors:
    for name, err in errors:
        print(f"\n  - {name}")
        print(f"    {err}")
