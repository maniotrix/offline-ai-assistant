import os
import sys
import json
import logging
from pathlib import Path
from sqlalchemy import inspect
from typing import Dict, List, Any

# Add parent directory to path to import from database
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.config import engine, SessionLocal
from database.models import CachedCommand, CachedIntent, CachedAction
from database.repositories.command_repository import CommandRepository
from database.repositories.intent_repository import IntentRepository
from alembic import command
from alembic.config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BATCH_SIZE = 100  # Number of records to process in a batch

def validate_command(cmd: Dict[str, Any]) -> bool:
    """Validate command data before insertion"""
    required_fields = ['name', 'domain', 'uuid']
    return all(field in cmd and cmd[field] for field in required_fields)

def validate_intent(intent: Dict[str, Any]) -> bool:
    """Validate intent data before insertion"""
    if not all(k in intent for k in ['uuid', 'command_id']):
        return False
    if 'actions' not in intent or not isinstance(intent['actions'], list):
        return False
    for action in intent['actions']:
        if not all(k in action for k in ['type', 'coordinates']):
            return False
        if not isinstance(action['coordinates'], dict) or not all(k in action['coordinates'] for k in ['x', 'y']):
            return False
    return True

def init_db():
    """Initialize the database and run migrations"""
    try:
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        if not tables:
            logger.info("No tables found. Running migrations...")
            alembic_cfg = Config("alembic.ini")
            command.upgrade(alembic_cfg, "head")
            logger.info("Migrations completed successfully")
        else:
            logger.info("Database tables already exist, skipping migrations")
            
    except Exception as e:
        logger.error(f"Database initialization failed: {str(e)}")
        raise

def migrate_json_to_db():
    """Migrate existing JSON data to SQLite database with batch processing"""
    base_dir = Path(__file__).parent.parent
    commands_file = base_dir / 'data' / 'commands-store.json'
    intents_file = base_dir / 'data' / 'intents-cache.json'
    
    command_repo = CommandRepository()
    intent_repo = IntentRepository()
    
    # Migrate commands
    if commands_file.exists():
        try:
            with open(commands_file) as f:
                commands_data = json.load(f)
                commands = commands_data.get('commands', [])
                
                for i in range(0, len(commands), BATCH_SIZE):
                    batch = commands[i:i + BATCH_SIZE]
                    with command_repo.get_db() as db:
                        try:
                            for cmd in batch:
                                if not validate_command(cmd):
                                    logger.warning(f"Skipping invalid command: {cmd}")
                                    continue
                                    
                                existing = command_repo.find_by_name_and_domain(
                                    db, cmd['name'], cmd['domain']
                                )
                                if not existing:
                                    command_repo.create(
                                        db,
                                        name=cmd['name'],
                                        domain=cmd['domain'],
                                        uuid=cmd['uuid'],
                                        is_in_cache=cmd.get('is_in_cache', False)
                                    )
                            db.commit()
                            logger.info(f"Migrated commands batch {i//BATCH_SIZE + 1}")
                        except Exception as e:
                            db.rollback()
                            logger.error(f"Error in command batch {i//BATCH_SIZE + 1}: {str(e)}")
                            
        except Exception as e:
            logger.error(f"Failed to migrate commands: {str(e)}")
    
    # Migrate intents
    if intents_file.exists():
        try:
            with open(intents_file) as f:
                intents_data = json.load(f)
                intents = intents_data.get('action_predictions', [])
                
                for i in range(0, len(intents), BATCH_SIZE):
                    batch = intents[i:i + BATCH_SIZE]
                    with intent_repo.get_db() as db:
                        try:
                            for intent in batch:
                                if not validate_intent(intent):
                                    logger.warning(f"Skipping invalid intent: {intent}")
                                    continue
                                    
                                existing = intent_repo.find_by_command_uuid(
                                    db, intent['command_id']
                                )
                                if not existing:
                                    db_intent = CachedIntent(
                                        uuid=intent['uuid'],
                                        command_uuid=intent['command_id'],
                                        confidence=1.0
                                    )
                                    db.add(db_intent)
                                    db.flush()
                                    
                                    for action in intent.get('actions', []):
                                        db_action = CachedAction(
                                            intent_id=db_intent.id,
                                            type=action['type'],
                                            coordinates_x=action['coordinates']['x'],
                                            coordinates_y=action['coordinates']['y'],
                                            text=action.get('text')
                                        )
                                        db.add(db_action)
                                    
                            db.commit()
                            logger.info(f"Migrated intents batch {i//BATCH_SIZE + 1}")
                        except Exception as e:
                            db.rollback()
                            logger.error(f"Error in intent batch {i//BATCH_SIZE + 1}: {str(e)}")
                            
        except Exception as e:
            logger.error(f"Failed to migrate intents: {str(e)}")

if __name__ == "__main__":
    logger.info("Initializing database...")
    init_db()
    logger.info("Database initialized successfully!")
    
    logger.info("Migrating existing JSON data...")
    migrate_json_to_db()
    logger.info("Data migration completed!")