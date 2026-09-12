import shutil
from pathlib import Path

BASE = Path(r"D:\PEMROGRAMAN\PROJECT\2026\python-design")
CATEGORIES = ["parallel", "waves", "radial", "grid", "contour", "spiral", "optical", "geometric", "organic", "dynamic"]

for cat in CATEGORIES:
    code_output = BASE / cat / "code" / "output"
    real_output = BASE / cat / "output"
    
    if code_output.exists():
        for ext in ["jpg", "svg"]:
            src = code_output / ext
            dst = real_output / ext
            if src.exists():
                dst.mkdir(parents=True, exist_ok=True)
                for f in src.glob(f"*.{ext}"):
                    shutil.move(str(f), str(dst / f.name))
                print(f"Pindah: {cat}/code/output/{ext} -> {cat}/output/{ext}")
        
        # Hapus folder code/output
        shutil.rmtree(str(code_output))
        print(f"Hapus: {cat}/code/output/")

print("\nSelesai!")
