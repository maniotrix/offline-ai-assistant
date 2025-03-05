import pytest
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# This is a minimal conftest.py file that can be expanded as needed
# Currently, it doesn't contain any fixtures as we're directly testing the function

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """
    Setup function that runs once before all tests.
    Can be used to set up any necessary environment variables or configurations.
    """
    # Currently empty, but can be expanded as needed
    pass 