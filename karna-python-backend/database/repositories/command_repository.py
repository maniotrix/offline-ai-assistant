from typing import Optional, List
from sqlalchemy.orm import Session
from .base_repository import BaseRepository
from ..models import CachedCommand
from domain.command import Command

class CommandRepository(BaseRepository[CachedCommand]):
    def __init__(self):
        super().__init__(CachedCommand)

    def find_by_name_and_domain(self, db: Session, name: str, domain: str) -> Optional[CachedCommand]:
        return (db.query(self.model)
               .filter(self.model.name == name.lower(),
                      self.model.domain == domain.lower())
               .first())

    def to_domain(self, db_command: CachedCommand) -> Command:
        """Convert database model to domain model"""
        return Command(
            name=db_command.name,
            domain=db_command.domain,
            uuid=db_command.uuid,
            is_in_cache=db_command.is_in_cache,
            created_at=db_command.created_at
        )

    def from_domain(self, command: Command) -> dict:
        """Convert domain model to database fields"""
        return {
            "name": command.name.lower(),
            "domain": command.domain.lower(),
            "uuid": str(command.uuid),
            "is_in_cache": command.is_in_cache,
            "created_at": command.created_at
        }