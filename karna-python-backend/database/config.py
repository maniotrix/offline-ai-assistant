from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import QueuePool
from config.settings import get_settings

def create_db_engine(database_url=None):
    settings = get_settings()
    db_settings = settings.database
    
    if database_url is None:
        database_url = db_settings.url
    
    return create_engine(
        database_url,
        connect_args={"check_same_thread": False},
        poolclass=QueuePool,
        pool_size=db_settings.pool_size,
        max_overflow=db_settings.max_overflow,
        pool_timeout=db_settings.pool_timeout,
        pool_recycle=db_settings.pool_recycle,
        echo=db_settings.echo
    )

def get_session_factory(engine=None):
    if engine is None:
        engine = create_db_engine()
    
    return sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
        expire_on_commit=False
    )

# Default instances for backward compatibility
engine = create_db_engine()
SessionLocal = get_session_factory(engine)
Base = declarative_base()