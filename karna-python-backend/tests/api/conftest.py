import pytest
from fastapi.testclient import TestClient
from config.db.settings import use_test_settings, use_default_settings
from main import app

import sys
from pathlib import Path
# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture
def test_client():
    """Create a test client instance with test database configuration"""
    use_test_settings()  # Ensure we're using test settings for the client
    with TestClient(app) as client:
        yield client
    use_default_settings()