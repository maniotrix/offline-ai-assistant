from typing import Generic, TypeVar, Type, Optional, List, Union, Generator
from sqlalchemy.orm import Session, DeclarativeBase
from ..config import Base, SessionLocal
from contextlib import contextmanager

ModelType = TypeVar("ModelType", bound=DeclarativeBase)

class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    @contextmanager
    def get_db(self) -> Generator[Session, None, None]:
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    def get_by_id(self, db: Session, id: int) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_by_uuid(self, db: Session, uuid: str) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.uuid == uuid).first()

    def get_all(self, db: Session) -> List[ModelType]:
        return db.query(self.model).all()

    def create(self, db: Session, **kwargs) -> ModelType:
        db_obj = self.model(**kwargs)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: ModelType, **kwargs) -> ModelType:
        for key, value in kwargs.items():
            setattr(db_obj, key, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, id: Union[int, str]) -> bool:
        db_obj = (db.query(self.model)
                 .filter(self.model.id == id if isinstance(id, int) else self.model.uuid == id)
                 .first())
        if db_obj:
            db.delete(db_obj)
            db.commit()
            return True
        return False