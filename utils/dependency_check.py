import subprocess
import sys

def ensure_dependencies():
    try:
        import yaml
    except ImportError:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyyaml'])