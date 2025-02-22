from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from uuid import uuid4
from .config import Base

class CachedCommand(Base):
    __tablename__ = "cached_commands"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String, unique=True, index=True, default=lambda: str(uuid4()))
    name = Column(String, index=True)
    domain = Column(String, index=True)
    is_in_cache = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    
    # Relationship with CachedIntent
    intents = relationship("CachedIntent", back_populates="command", cascade="all, delete-orphan")

class CachedIntent(Base):
    __tablename__ = "cached_intents"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String, unique=True, index=True, default=lambda: str(uuid4()))
    command_uuid = Column(String, ForeignKey("cached_commands.uuid"))
    confidence = Column(Float, default=1.0)
    meta_data = Column(JSON, default=dict)
    actions = Column(JSON, default=list)  # Store actions as JSON array
    created_at = Column(DateTime, default=datetime.now)

    # Relationship with CachedCommand
    command = relationship("CachedCommand", back_populates="intents")