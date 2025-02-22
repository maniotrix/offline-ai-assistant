from typing import Optional, List
from sqlalchemy.orm import Session
from .base_repository import BaseRepository
from ..models import CachedIntent, CachedAction
from domain.intent import Intent, IntentPrediction
from domain.action import Action, ActionCoordinates
from uuid import UUID

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
        for db_action in db_intent.actions:
            action = Action(
                type=db_action.type,
                coordinates=ActionCoordinates(
                    x=db_action.coordinates_x,
                    y=db_action.coordinates_y
                ),
                text=db_action.text,
                uuid=UUID(db_action.uuid)
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
        return {
            "uuid": str(prediction.intent.uuid),
            "command_uuid": str(prediction.intent.command_uuid),
            "confidence": prediction.confidence,
            "meta_data": prediction.metadata,
            "created_at": prediction.intent.created_at
        }

    def create_with_actions(self, db: Session, prediction: IntentPrediction) -> CachedIntent:
        """Create intent with its associated actions in a single transaction"""
        try:
            # Create intent
            intent_data = self.from_domain(prediction)
            db_intent = super().create(db, **intent_data)

            # Create associated actions
            for action in prediction.intent.actions:
                db_action = CachedAction(
                    uuid=str(action.uuid),
                    intent_id=db_intent.id,
                    type=action.type,
                    coordinates_x=action.coordinates.x,
                    coordinates_y=action.coordinates.y,
                    text=action.text
                )
                db.add(db_action)
            
            db.flush()  # Ensure all changes are ready but not committed
            db.refresh(db_intent)  # Refresh to get the actions relationship
            return db_intent
        except Exception as e:
            db.rollback()
            raise