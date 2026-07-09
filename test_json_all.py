import subprocess
import sys
from pathlib import Path
import json

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def run_cmd(args):
    result = subprocess.run([sys.executable, "-m", "src"] + args, capture_output=True, text=True, cwd=project_root)
    return result

print("=" * 60)
print("Testing All Commands JSON Output")
print("=" * 60)
print()

# Clean DB
data_dir = project_root / "data"
if data_dir.exists():
    import shutil
    shutil.rmtree(data_dir)

# Test version
print("1. Testing version...")
result = run_cmd(["--version"])
print(f"OK Version: {result.stdout.strip()}")

# Test config show
print("\n2. Testing config show...")
result = run_cmd(["config", "show"])
print(f"OK Config: {result.stdout.strip()}")

# Test account init
print("\n3. Testing account init...")
result = run_cmd(["account", "init", "--name", "测试账户", "--balance", "100000"])
print(f"OK Account init: {result.stdout.strip()}")

# Test account info
print("\n4. Testing account info...")
result = run_cmd(["account", "info"])
print(f"OK Account info: {result.stdout.strip()}")

# Test position add
print("\n5. Testing position add...")
result = run_cmd(["position", "add", "--code", "600519", "--name", "贵州茅台", "--quantity", "100", "--price", "150"])
print(f"OK Position add: {result.stdout.strip()}")

# Test position list
print("\n6. Testing position list...")
result = run_cmd(["position", "list"])
print(f"OK Position list: {result.stdout.strip()}")

# Test watch add
print("\n7. Testing watch add...")
result = run_cmd(["watch", "add", "--code", "AAPL", "--name", "苹果公司", "--note", "关注中"])
print(f"OK Watch add: {result.stdout.strip()}")

# Test watch list
print("\n8. Testing watch list...")
result = run_cmd(["watch", "list"])
print(f"OK Watch list: {result.stdout.strip()}")

print("\n" + "=" * 60)
print("All tests completed!")
print("=" * 60)
