import subprocess
import sys
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def run_cmd(args):
    result = subprocess.run([sys.executable, "-m", "src"] + args, capture_output=True, text=True, cwd=project_root)
    print(f"Command: {' '.join(args)}")
    print(f"Return code: {result.returncode}")
    if result.stdout:
        print(f"Stdout:\n{result.stdout}")
    if result.stderr:
        print(f"Stderr:\n{result.stderr}")
    print()
    return result

print("=" * 60)
print("Testing JSON Output")
print("=" * 60)
print()

run_cmd(["--version"])
run_cmd(["config", "show"])
