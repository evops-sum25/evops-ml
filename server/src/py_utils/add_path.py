import sys
from pathlib import Path
path = Path(r"{}").resolve()
if str(path) not in sys.path:
    sys.path.insert(0, str(path))
