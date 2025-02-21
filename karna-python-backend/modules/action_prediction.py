from base import BaseService, SingletonMeta
import torch
from typing import Dict, Optional, List
import json
from pathlib import Path
import asyncio
from dataclasses import dataclass
import os

@dataclass
class Action:
    type: str  # click, enter_text, etc.
    coordinates: Dict[str, int]  # x, y coordinates
    text: Optional[str] = None  # for enter_text actions

@dataclass
class ActionPrediction:
    uuid: str
    command_id: str
    actions: List[Action]

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
            self._batch_size = 4  # Configurable batch size for efficient processing
            # Add cache file path
            self.cache_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                                         'data', 'intents-cache.json')
            self._cache = {}
            self._load_cache()
            self._initialized = True
        
    async def initialize(self) -> None:
        """Initialize language model and tokenizer"""
        try:
            # Load config
            with open(self.config_path) as f:
                config = json.load(f)
                
            # Initialize tokenizer
            self.tokenizer = self._load_tokenizer()
            
            # Load model with quantization for efficiency
            self.model = torch.load(self.model_path)
            self.model.eval()
            
            if torch.cuda.is_available():
                self.model = self.model.cuda()
                
            self._resources['model'] = self.model
            self._resources['tokenizer'] = self.tokenizer
            
            # Start background task for batch processing
            self._batch_processor_task = asyncio.create_task(self._process_batch())
            
        except Exception as e:
            self.logger.error(f"Failed to initialize language model: {str(e)}")
            raise

    def _load_tokenizer(self):
        """Load and configure tokenizer"""
        vocab_path = Path(self.tokenizer_path) / "vocab.txt"
        if not vocab_path.exists():
            raise FileNotFoundError(f"Tokenizer vocab not found at {vocab_path}")
        # Initialize your tokenizer here based on the model requirements
        # This is a placeholder - replace with actual tokenizer initialization
        return None  # Replace with actual tokenizer

    def _load_cache(self):
        """Load cached commands and their actions from file"""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r') as f:
                    self._cache = json.load(f)
            else:
                self._cache = {}
        except Exception as e:
            self.logger.error(f"Failed to load intent cache: {str(e)}")
            self._cache = {}

    def _save_cache(self):
        """Save cache to file"""
        try:
            os.makedirs(os.path.dirname(self.cache_file), exist_ok=True)
            with open(self.cache_file, 'w') as f:
                json.dump(self._cache, f, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to save intent cache: {str(e)}")

    def _convert_cached_to_prediction(self, cached_data: Dict) -> ActionPrediction:
        """Convert cached JSON data to ActionPrediction object"""
        actions = []
        for action_data in cached_data.get('actions', []):
            actions.append(Action(
                type=action_data['type'],
                coordinates=action_data['coordinates'],
                text=action_data.get('text')
            ))
        
        return ActionPrediction(
            uuid=cached_data['uuid'],
            command_id=cached_data['command_id'],
            actions=actions
        )

    def _convert_prediction_to_json(self, prediction: ActionPrediction) -> Dict:
        """Convert ActionPrediction to JSON format"""
        return {
            "action_predictions": {
                "uuid": prediction.uuid,
                "command_id": prediction.command_id,
                "actions": [
                    {
                        "type": action.type,
                        "coordinates": action.coordinates,
                        **({"text": action.text} if action.text is not None else {})
                    }
                    for action in prediction.actions
                ]
            }
        }

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

    async def recognize_intent(self, command_id: str, uuid: str = None) -> ActionPrediction:
        """
        Recognize intent by first checking cache for the command_id.
        If found in cache, return cached actions, otherwise use model inference.
        """
        # Check cache first
        cache_key = command_id
        if cache_key in self._cache:
            self.logger.debug(f"Found cached actions for command {command_id}")
            cached_data = self._cache[cache_key]
            if uuid:  # Update UUID if provided
                cached_data['uuid'] = uuid
            return self._convert_cached_to_prediction(cached_data)

        # If not in cache, queue request for model inference
        future = asyncio.Future()
        await self._request_queue.put((command_id, uuid, future))
        result = await future
        
        # Cache the result
        self._cache[cache_key] = {
            'uuid': result.uuid,
            'command_id': result.command_id,
            'actions': [
                {
                    'type': action.type,
                    'coordinates': action.coordinates,
                    **({"text": action.text} if action.text is not None else {})
                }
                for action in result.actions
            ]
        }
        self._save_cache()
        
        return result

    async def _process_batch(self) -> None:
        """Background task to process requests in batches for efficiency"""
        while True:
            batch: List[tuple] = []
            try:
                # Collect batch_size requests or wait for timeout
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

                # Process batch
                texts = [item[0] for item in batch]
                futures = [item[2] for item in batch]
                
                try:
                    results = await self._batch_inference(batch)
                    # Set results for all futures
                    for future, result in zip(futures, results):
                        if not future.done():
                            future.set_result(result)
                except Exception as e:
                    # Handle errors
                    for future in futures:
                        if not future.done():
                            future.set_exception(e)
                            
            except asyncio.CancelledError:
                # Handle cancellation
                for _, _, future in batch:
                    if not future.done():
                        future.cancel()
                raise

    async def _batch_inference(self, requests: List[tuple]) -> List[ActionPrediction]:
        """Run batch inference on the model"""
        if self.model is None:
            raise RuntimeError("Language model not initialized")

        with torch.no_grad():
            # Unpack requests
            texts = [req[0] for req in requests]
            uuids = [req[1] for req in requests]
            
            # Tokenize
            inputs = self.tokenizer(
                texts,
                padding=True,
                truncation=True,
                return_tensors="pt"
            )
            
            if torch.cuda.is_available():
                inputs = {k: v.cuda() for k, v in inputs.items()}

            # Run inference
            outputs = self.model(**inputs)
            
            # Process outputs into ActionPrediction objects
            results = []
            for text, uuid, output in zip(texts, uuids, outputs):
                # Convert model output to ActionPrediction object
                # This is a placeholder - implement based on your model's output format
                prediction = ActionPrediction(
                    uuid=uuid or "generated_uuid",  # Use provided UUID or generate one
                    command_id=text,  # Use command_id from request
                    actions=[]  # Extract actions from model output
                )
                results.append(prediction)
                
            return results

# Singleton instance getter
_language_service_instance = None

def get_language_service_instance(model_path: str = None, config_path: str = None, tokenizer_path: str = None):
    global _language_service_instance
    if _language_service_instance is None:
        if model_path is None or config_path is None or tokenizer_path is None:
            raise ValueError("model_path, config_path and tokenizer_path are required for first initialization")
        _language_service_instance = LanguageService(model_path, config_path, tokenizer_path)
    return _language_service_instance