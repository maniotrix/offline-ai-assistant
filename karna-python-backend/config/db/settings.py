from pathlib import Path
from typing import Optional
from dataclasses import dataclass

@dataclass
class DatabaseSettings:
    url: str
    pool_size: int = 5
    max_overflow: int = 10
    pool_timeout: int = 30
    pool_recycle: int = 1800
    echo: bool = False

@dataclass
class Settings:
    database: DatabaseSettings
    
    @classmethod
    def get_default(cls) -> 'Settings':
        # Get the karna-python-backend root directory
        base_dir = Path(__file__).parent.parent.parent
        return cls(
            database=DatabaseSettings(
                url=f"sqlite:///{base_dir / 'data' / 'cache.db'}"
            )
        )
    
    @classmethod
    def get_test(cls) -> 'Settings':
        return cls(
            database=DatabaseSettings(
                url="sqlite:///:memory:",
                pool_size=1,
                max_overflow=0
            )
        )

_current_settings: Optional[Settings] = None

def get_settings() -> Settings:
    global _current_settings
    if _current_settings is None:
        _current_settings = Settings.get_default()
    return _current_settings

def use_test_settings():
    global _current_settings
    _current_settings = Settings.get_test()

def use_default_settings():
    global _current_settings
    _current_settings = Settings.get_default()