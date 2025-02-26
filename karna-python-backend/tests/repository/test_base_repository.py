import pytest
from uuid import uuid4
from sqlalchemy.exc import IntegrityError
from database.repositories.base_repository import BaseRepository
from tests.repository.test_models import TestModel

def test_create_and_retrieve(test_db, test_repository_factory):
    repo = test_repository_factory(BaseRepository[TestModel], TestModel)
    
    # Test creation
    test_uuid = str(uuid4())
    obj = repo.create(test_db, uuid=test_uuid, name="test")
    assert obj.name == "test"
    assert obj.uuid == test_uuid
    
    # Test retrieval by id
    retrieved_by_id = repo.get_by_id(test_db, obj.id)
    assert retrieved_by_id is not None
    assert retrieved_by_id.name == "test"
    
    # Test retrieval by uuid
    retrieved_by_uuid = repo.get_by_uuid(test_db, test_uuid)
    assert retrieved_by_uuid is not None
    assert retrieved_by_uuid.name == "test"
    assert retrieved_by_uuid.id == obj.id

def test_update_operations(test_db, test_repository_factory):
    repo = test_repository_factory(BaseRepository[TestModel], TestModel)
    
    # Create initial object
    obj = repo.create(test_db, uuid=str(uuid4()), name="initial")
    
    # Test update
    updated = repo.update(test_db, obj, name="updated")
    assert updated.name == "updated"
    assert updated.id == obj.id
    assert updated.uuid == obj.uuid
    
    # Verify update persisted
    retrieved = repo.get_by_id(test_db, obj.id)
    assert retrieved.name == "updated"

def test_delete_operations(test_db, test_repository_factory):
    repo = test_repository_factory(BaseRepository[TestModel], TestModel)
    
    # Create and then delete
    obj = repo.create(test_db, uuid=str(uuid4()), name="to_delete")
    assert repo.delete(test_db, obj.id) is True
    
    # Verify deletion
    assert repo.get_by_id(test_db, obj.id) is None
    
    # Test deleting non-existent object
    assert repo.delete(test_db, 9999) is False

def test_get_all(test_db, test_repository_factory):
    repo = test_repository_factory(BaseRepository[TestModel], TestModel)
    
    # Create multiple objects
    uuids = [str(uuid4()) for _ in range(3)]
    objects = [
        repo.create(test_db, uuid=uuid, name=f"test_{i}")
        for i, uuid in enumerate(uuids)
    ]
    
    # Test get_all
    all_objects = repo.get_all(test_db)
    assert len(all_objects) >= 3  # Could be more if other tests left data
    assert all(obj.id is not None for obj in all_objects)

def test_duplicate_uuid(test_db, test_repository_factory):
    repo = test_repository_factory(BaseRepository[TestModel], TestModel)
    
    # Create first object
    test_uuid = str(uuid4())
    repo.create(test_db, uuid=test_uuid, name="first")
    
    # Attempt to create second object with same UUID
    with pytest.raises(IntegrityError):
        repo.create(test_db, uuid=test_uuid, name="second")