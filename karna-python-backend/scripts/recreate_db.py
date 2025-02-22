import json
import sys
import os
from pathlib import Path
import sqlite3
from datetime import datetime

# Add the parent directory to sys path to import database modules
sys.path.append(str(Path(__file__).parent.parent))

def read_json_file(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def main():
    # Connect to the database
    db_path = Path(__file__).parent.parent / 'data' / 'cache.db'
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    # Temporarily disable foreign key constraints
    cursor.execute("PRAGMA foreign_keys = OFF")

    try:
        # Drop existing tables
        cursor.execute("DROP TABLE IF EXISTS cached_actions")
        cursor.execute("DROP TABLE IF EXISTS cached_intents")
        cursor.execute("DROP TABLE IF EXISTS cached_commands")

        # Recreate tables
        cursor.execute("""
        CREATE TABLE cached_commands (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uuid TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            domain TEXT NOT NULL,
            is_in_cache BOOLEAN NOT NULL DEFAULT 0,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """)

        cursor.execute("""
        CREATE TABLE cached_intents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uuid TEXT NOT NULL UNIQUE,
            command_uuid TEXT NOT NULL,
            confidence REAL NOT NULL DEFAULT 1.0,
            meta_data JSON,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (command_uuid) REFERENCES cached_commands(uuid)
        )
        """)

        cursor.execute("""
        CREATE TABLE cached_actions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uuid TEXT NOT NULL UNIQUE,
            intent_id INTEGER NOT NULL,
            type TEXT NOT NULL,
            coordinates_x INTEGER NOT NULL,
            coordinates_y INTEGER NOT NULL,
            text TEXT,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (intent_id) REFERENCES cached_intents(id)
        )
        """)

        # Create indexes
        cursor.execute("CREATE INDEX ix_cached_commands_uuid ON cached_commands(uuid)")
        cursor.execute("CREATE INDEX ix_cached_commands_name ON cached_commands(name)")
        cursor.execute("CREATE INDEX ix_cached_commands_domain ON cached_commands(domain)")
        cursor.execute("CREATE INDEX ix_cached_intents_uuid ON cached_intents(uuid)")
        cursor.execute("CREATE INDEX ix_cached_actions_uuid ON cached_actions(uuid)")

        # Read JSON files
        commands_file = Path(__file__).parent.parent / 'data' / 'commands-store.json'
        intents_file = Path(__file__).parent.parent / 'data' / 'intents-cache.json'

        commands_data = read_json_file(commands_file)
        intents_data = read_json_file(intents_file)

        # Insert commands
        for cmd in commands_data.get('commands', []):
            cursor.execute(
                "INSERT INTO cached_commands (uuid, name, domain, is_in_cache) VALUES (?, ?, ?, ?)",
                (cmd['uuid'], cmd['name'], cmd['domain'], cmd.get('is_in_cache', False))
            )

        # Insert intents and actions
        for prediction in intents_data.get('action_predictions', []):
            # Insert intent
            cursor.execute(
                "INSERT INTO cached_intents (uuid, command_uuid, confidence) VALUES (?, ?, ?)",
                (prediction['uuid'], prediction['command_id'], 1.0)
            )
            intent_id = cursor.lastrowid

            # Insert actions
            for action in prediction.get('actions', []):
                cursor.execute(
                    """INSERT INTO cached_actions 
                    (uuid, intent_id, type, coordinates_x, coordinates_y, text) 
                    VALUES (?, ?, ?, ?, ?, ?)""",
                    (
                        str(os.urandom(16).hex()),  # Generate a new UUID for actions
                        intent_id,
                        action['type'],
                        action['coordinates']['x'],
                        action['coordinates']['y'],
                        action.get('text')
                    )
                )

        # Re-enable foreign key constraints
        cursor.execute("PRAGMA foreign_keys = ON")
        
        # Commit the transaction
        conn.commit()
        print("Database tables recreated successfully!")

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    main()