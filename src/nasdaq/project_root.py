import os
import sys

cur_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(cur_dir, "../.."))
# print(project_root)
if project_root not in sys.path:
    sys.path.append(project_root)
