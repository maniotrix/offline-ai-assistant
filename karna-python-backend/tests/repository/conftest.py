import sys
from pathlib import Path
import pytest
from database.config import create_db_engine, get_session_factory, Base
from config.db.settings import use_test_settings, use_default_settings
from tests.repository.test_models import TestModel  # Import from new location

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

@pytest.fixture(scope="session")
def test_engine():
    """Create a test database engine that uses an in-memory SQLite database"""
    use_test_settings()
    engine = create_db_engine()
    Base.metadata.create_all(bind=engine)  # This will now create TestModel table too
    yield engine
    Base.metadata.drop_all(bind=engine)
    use_default_settings()

@pytest.fixture(scope="session")
def test_session_factory(test_engine):
    """Create a test session factory"""
    return get_session_factory(test_engine)

@pytest.fixture
def test_db(test_session_factory):
    """Get a test database session"""
    session = test_session_factory()
    try:
        yield session
    finally:
        session.rollback()
        session.close()

@pytest.fixture
def test_repository_factory(test_session_factory):
    """Factory for creating repositories with test database session"""
    def _factory(repository_class, model_class):
        return repository_class(model_class, session_factory=test_session_factory)
    return _factory