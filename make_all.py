"""Rebuild every figure and interactive page:  python make_all.py"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
scripts = sorted((ROOT / "charts").glob("[0-9][0-9]_*.py"))
for script in scripts:
    print(f"\n{script.name}")
    subprocess.run([sys.executable, str(script)], check=True)
print(f"\nDone: {len(scripts)} chart scripts.")
