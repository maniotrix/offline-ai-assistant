import pytest
from uuid import uuid4
from database.repositories.base_repository import BaseRepository, BaseModel
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String

class TestModel(BaseModel):
    name: Mapped[str] = mapped_column(String)

def test_repository_operations(test_db, test_repository_factory):
    # Create a repository instance with test database
    repo = test_repository_factory(BaseRepository[TestModel], TestModel)
    
    # Create a test record
    test_uuid = str(uuid4())
    obj = repo.create(test_db, uuid=test_uuid, name="test")
    assert obj.name == "test"
    assert obj.uuid == test_uuid
    
    # Get by id
    retrieved = repo.get_by_id(test_db, obj.id)
    assert retrieved is not None
    assert retrieved.name == "test"
    
    # Update
    updated = repo.update(test_db, retrieved, name="updated")
    assert updated.name == "updated"
    
    # Delete
    assert repo.delete(test_db, obj.id) is True
    assert repo.get_by_id(test_db, obj.id) is None