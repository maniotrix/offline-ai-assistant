import sys
from pathlib import Path
import pytest # Import from new location

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))