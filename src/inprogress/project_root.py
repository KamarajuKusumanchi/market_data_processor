import sys
from pathlib import Path

project_root = Path(__file__).parents[2]
if project_root not in sys.path:
    sys.path.insert(0, str(project_root))
