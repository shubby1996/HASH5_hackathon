from pathlib import Path
import os

# Check where we are
print(f"Current dir: {os.getcwd()}")

# Check where main.py thinks root is
main_file = Path("app/main.py")
root_from_main = main_file.parent.parent
print(f"Root from main.py: {root_from_main.absolute()}")

# Check if .env exists there
env_file = root_from_main / ".env"
print(f".env path: {env_file.absolute()}")
print(f".env exists: {env_file.exists()}")

# Check actual root
actual_root = Path(__file__).parent.parent
actual_env = actual_root / ".env"
print(f"\nActual root: {actual_root.absolute()}")
print(f"Actual .env: {actual_env.absolute()}")
print(f"Actual .env exists: {actual_env.exists()}")
