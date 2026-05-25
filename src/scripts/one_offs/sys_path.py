# This file adds the project root to sys.path so that absolute imports
# (e.g. from src.utils.foo import bar) work regardless of which directory
# the script is run from.
#
# Usage: Add the following line at the top of any script that needs it,
# before any imports from the project:
#
#   import sys_path  # noqa: F401
#
# This file should be placed in the same directory as the script that
# imports it. A copy of this file should exist in every directory that
# has scripts needing project-level imports.
#
# The project root is identified by the presence of a .project-root file.
# Make sure to create it at the project root and commit it to Git:
#
#   touch .project-root

import sys
from pathlib import Path

# This module is imported for its side effect only — it exports nothing.
__all__ = []

def find_project_root(start: Path, landmark: str = ".project-root") -> Path:
    for parent in [start, *start.parents]:
        if (parent / landmark).exists():
            return parent
    raise FileNotFoundError(f"Could not find {landmark} above {start}")

project_root = str(find_project_root(Path(__file__).parent))
if project_root not in sys.path:
    sys.path.append(project_root)