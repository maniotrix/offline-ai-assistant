from typing import Generic, TypeVar, Type, Optional, List, Union, Generator
from sqlalchemy.orm import Session, DeclarativeBase, mapped_column, Mapped
from sqlalchemy import select, Integer, String
from ..config import SessionLocal
from contextlib import contextmanager

class BaseModel(DeclarativeBase):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    uuid: Mapped[str] = mapped_column(String, unique=True, nullable=False)

ModelType = TypeVar("ModelType", bound=BaseModel)

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
        stmt = select(self.model).where(self.model.id == id)
        return db.scalars(stmt).first()

    def get_by_uuid(self, db: Session, uuid: str) -> Optional[ModelType]:
        stmt = select(self.model).where(self.model.uuid == uuid)
        return db.scalars(stmt).first()

    def get_all(self, db: Session) -> List[ModelType]:
        stmt = select(self.model)
        return list(db.scalars(stmt).all())

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
        stmt = select(self.model).where(
            self.model.id == id if isinstance(id, int) else self.model.uuid == id
        )
        db_obj = db.scalars(stmt).first()
        if db_obj:
            db.delete(db_obj)
            db.commit()
            return True
        return False