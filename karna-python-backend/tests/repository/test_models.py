from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String, Integer
from database.config import Base

class TestModel(Base):
    __tablename__ = 'test_model'
    __table_args__ = {'extend_existing': True}
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    uuid: Mapped[str] = mapped_column(String, unique=True)