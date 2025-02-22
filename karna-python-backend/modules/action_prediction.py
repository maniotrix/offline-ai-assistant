from base import BaseService, SingletonMeta
import torch
from typing import Dict, Optional, List, Tuple
import json
from pathlib import Path
import asyncio
from uuid import UUID
import numpy as np
from transformers import AutoTokenizer, AutoModel
from domain.action import Action, ActionCoordinates
from domain.intent import Intent, IntentPrediction
from database.repositories.intent_repository import IntentRepository
from database.models import CachedCommand

class LanguageService(BaseService, metaclass=SingletonMeta):
    def __init__(self, model_path: str, config_path: str, tokenizer_path: str):
        if not hasattr(self, '_initialized'):
            super().__init__()
            self.model_path = model_path
            self.config_path = config_path
            self.tokenizer_path = tokenizer_path
            self.model = None
            self.tokenizer = None
            self._request_queue = asyncio.Queue()
            self._batch_size = 4
            self.intent_repository = IntentRepository()
            self._initialized = True

    async def initialize(self) -> None:
        """Initialize language model and tokenizer"""
        try:
            # Load config
            with open(self.config_path) as f:
                self.config = json.load(f)
            
            # Load model config
            self.max_length = self.config.get('max_length', 512)
            self.action_types = self.config.get('action_types', ['click', 'type', 'scroll'])
            
            # Initialize tokenizer
            self.tokenizer = self._load_tokenizer()
            
            # Load model with optimization
            self.model = self._load_model()
            
            # Start background task for batch processing
            self._batch_processor_task = asyncio.create_task(self._process_batch())
            
            self._resources['model'] = self.model
            self._resources['tokenizer'] = self.tokenizer
            self.logger.info("Language model initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize language model: {str(e)}")
            raise

    def _load_tokenizer(self):
        """Load and configure the tokenizer"""
        try:
            tokenizer = AutoTokenizer.from_pretrained(
                self.tokenizer_path,
                model_max_length=self.max_length
            )
            self.logger.info("Tokenizer loaded successfully")
            return tokenizer
        except Exception as e:
            self.logger.error(f"Failed to load tokenizer: {str(e)}")
            raise

    def _load_model(self) -> torch.nn.Module:
        """Load and optimize the model for inference"""
        try:
            model = AutoModel.from_pretrained(self.model_path)
            model.eval()
            
            if torch.cuda.is_available():
                model = model.cuda()
                # Enable TorchScript optimization
                model = torch.jit.script(model)
            
            return model
        except Exception as e:
            self.logger.error(f"Failed to load model: {str(e)}")
            raise

    async def shutdown(self) -> None:
        """Clean up resources"""
        if hasattr(self, '_batch_processor_task'):
            self._batch_processor_task.cancel()
            try:
                await self._batch_processor_task
            except asyncio.CancelledError:
                pass
        
        self.model = None
        self.tokenizer = None
        self._resources.clear()

    async def recognize_intent(self, command_uuid: str) -> Optional[IntentPrediction]:
        """
        Recognize intent by first checking cache for the command_uuid.
        If found in cache, return cached actions, otherwise use model inference.
        """
        try:
            # Check cache in database
            with self.intent_repository.get_db() as db:
                cached_intent = self.intent_repository.find_by_command_uuid(db, command_uuid)
                if cached_intent:
                    self.logger.debug(f"Found cached intent for command {command_uuid}")
                    return self.intent_repository.to_domain(cached_intent)

            # If not in cache, queue request for model inference
            future = asyncio.Future()
            await self._request_queue.put((command_uuid, future))
            result = await future
            
            if result:
                # Cache the result in database
                with self.intent_repository.get_db() as db:
                    self.intent_repository.create_with_actions(db, result)
            
            return result
        except Exception as e:
            self.logger.error(f"Error recognizing intent: {str(e)}")
            return None

    async def _process_batch(self) -> None:
        """Background task to process requests in batches for efficiency"""
        while True:
            batch: List[Tuple[str, asyncio.Future]] = []
            try:
                while len(batch) < self._batch_size:
                    try:
                        request = await asyncio.wait_for(
                            self._request_queue.get(),
                            timeout=0.1
                        )
                        batch.append(request)
                    except asyncio.TimeoutError:
                        break

                if not batch:
                    continue

                command_uuids = [item[0] for item in batch]
                futures = [item[1] for item in batch]
                
                try:
                    results = await self._batch_inference(command_uuids)
                    for future, result in zip(futures, results):
                        if not future.done():
                            future.set_result(result)
                except Exception as e:
                    self.logger.error(f"Batch inference error: {str(e)}")
                    for future in futures:
                        if not future.done():
                            future.set_exception(e)
                            
            except asyncio.CancelledError:
                for _, future in batch:
                    if not future.done():
                        future.cancel()
                raise
            except Exception as e:
                self.logger.error(f"Error in batch processing: {str(e)}")

    async def _batch_inference(self, command_uuids: List[str]) -> List[IntentPrediction]:
        """Run batch inference on the model"""
        if self.model is None or self.tokenizer is None:
            raise RuntimeError("Language model or tokenizer not initialized")

        try:
            with torch.no_grad():
                # Get commands from database
                commands = []
                with self.intent_repository.get_db() as db:
                    for uuid in command_uuids:
                        cmd = db.query(CachedCommand).filter_by(uuid=uuid).first()
                        if cmd:
                            commands.append(cmd.name)
                        else:
                            commands.append("")

                # Tokenize commands
                inputs = self.tokenizer(
                    commands,
                    padding=True,
                    truncation=True,
                    max_length=self.max_length,
                    return_tensors="pt"
                )
                
                if torch.cuda.is_available():
                    inputs = {k: v.cuda() for k, v in inputs.items()}

                # Run model inference
                outputs = self.model(**inputs)
                logits = outputs.logits if hasattr(outputs, 'logits') else outputs[0]
                
                # Process model outputs
                predictions = []
                for uuid, logit in zip(command_uuids, logits):
                    # Extract action predictions from logits
                    action_probs = torch.softmax(logit, dim=-1)
                    predicted_actions = self._decode_actions(action_probs)
                    
                    # Create IntentPrediction object
                    intent = Intent(
                        command_uuid=UUID(uuid),
                        actions=predicted_actions
                    )
                    prediction = IntentPrediction(
                        intent=intent,
                        confidence=float(action_probs.max()),
                        metadata={"action_probabilities": action_probs.tolist()}
                    )
                    predictions.append(prediction)

                return predictions

        except Exception as e:
            self.logger.error(f"Inference error: {str(e)}")
            raise

    def _decode_actions(self, action_probs: torch.Tensor) -> List[Action]:
        """Decode model outputs into action objects"""
        actions = []
        # Get top K action predictions
        top_k = min(3, len(self.action_types))
        values, indices = torch.topk(action_probs, k=top_k)
        
        for prob, idx in zip(values, indices):
            if prob < 0.3:  # Confidence threshold
                continue
                
            action_type = self.action_types[idx]
            # Extract coordinate predictions (implementation depends on model output format)
            x, y = self._predict_coordinates(action_probs)
            
            action = Action(
                type=action_type,
                coordinates=ActionCoordinates(x=x, y=y)
            )
            actions.append(action)
            
        return actions

    def _predict_coordinates(self, probs: torch.Tensor) -> Tuple[int, int]:
        """Predict screen coordinates from model output"""
        # This is a simplified implementation
        # In practice, this would depend on your model's output format
        # and how coordinates are encoded
        x = int(torch.argmax(probs[:self.config.get('screen_width', 1920)]))
        y = int(torch.argmax(probs[self.config.get('screen_width', 1920):]))
        return x, y

    def get_status(self) -> str:
        """Get service status"""
        if not self._initialized:
            return "not_initialized"
        if self.model is None or self.tokenizer is None:
            return "not_ready"
        return "running"

# Singleton instance getter
_language_service_instance = None

def get_language_service_instance(model_path: str = None, config_path: str = None, tokenizer_path: str = None):
    global _language_service_instance
    if _language_service_instance is None:
        if model_path is None or config_path is None or tokenizer_path is None:
            raise ValueError("model_path, config_path and tokenizer_path are required for first initialization")
        _language_service_instance = LanguageService(model_path, config_path, tokenizer_path)
    return _language_service_instance