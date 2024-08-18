# run.py
import sys
from pathlib import Path

# This fixes the issue with module not found error
# Add the project root to the Python path
project_root = Path(__file__).parent.absolute()
sys.path.append(str(project_root))


