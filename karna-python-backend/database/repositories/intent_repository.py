from typing import Optional, List
from sqlalchemy.orm import Session
from .base_repository import BaseRepository
from ..models import CachedIntent
from domain.intent import Intent, IntentPrediction
from domain.action import Action, ActionCoordinates
from uuid import UUID, uuid4

class IntentRepository(BaseRepository[CachedIntent]):
    def __init__(self):
        super().__init__(CachedIntent)

    def find_by_command_uuid(self, db: Session, command_uuid: str) -> Optional[CachedIntent]:
        return (db.query(self.model)
               .filter(self.model.command_uuid == command_uuid)
               .first())

    def to_domain(self, db_intent: CachedIntent) -> IntentPrediction:
        """Convert database model to domain model"""
        actions = []
        for action_data in db_intent.actions:
            action = Action(
                type=action_data['type'],
                coordinates=ActionCoordinates(
                    x=action_data['coordinates']['x'],
                    y=action_data['coordinates']['y']
                ),
                text=action_data.get('text'),
                uuid=UUID(action_data.get('uuid', str(uuid4())))
            )
            actions.append(action)

        intent = Intent(
            command_uuid=UUID(db_intent.command_uuid),
            actions=actions,
            uuid=UUID(db_intent.uuid),
            created_at=db_intent.created_at
        )
        
        return IntentPrediction(
            intent=intent,
            confidence=db_intent.confidence,
            metadata=db_intent.meta_data or {}
        )

    def from_domain(self, prediction: IntentPrediction) -> dict:
        """Convert domain model to database fields"""
        actions_json = []
        for action in prediction.intent.actions:
            action_data = {
                'type': action.type,
                'coordinates': {
                    'x': action.coordinates.x,
                    'y': action.coordinates.y
                },
                'uuid': str(action.uuid)
            }
            if action.text:
                action_data['text'] = action.text
            actions_json.append(action_data)

        return {
            "uuid": str(prediction.intent.uuid),
            "command_uuid": str(prediction.intent.command_uuid),
            "confidence": prediction.confidence,
            "meta_data": prediction.metadata,
            "actions": actions_json,
            "created_at": prediction.intent.created_at
        }

    def create_with_actions(self, db: Session, prediction: IntentPrediction) -> CachedIntent:
        """Create intent with its associated actions"""
        try:
            # Create intent with actions as JSON
            intent_data = self.from_domain(prediction)
            db_intent = super().create(db, **intent_data)
            db.flush()
            return db_intent
        except Exception as e:
            db.rollback()
            raise