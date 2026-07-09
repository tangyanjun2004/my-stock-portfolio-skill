import shutil
from pathlib import Path

data_dir = Path(__file__).parent / "data"
if data_dir.exists():
    shutil.rmtree(data_dir)
    print("Database cleaned")
