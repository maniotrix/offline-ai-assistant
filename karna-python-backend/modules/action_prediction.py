from base import BaseService, SingletonMeta
import torch
from typing import Dict, Optional, List
import json
from pathlib import Path
import asyncio
from dataclasses import dataclass

@dataclass
class Intent:
    action_type: str
    confidence: float
    parameters: Dict
    raw_output: Dict

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

    async def recognize_intent(self, text: str) -> Intent:
        """Queue the intent recognition request and return result"""
        future = asyncio.Future()
        await self._request_queue.put((text, future))
        return await future

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
                futures = [item[1] for item in batch]
                
                try:
                    results = await self._batch_inference(texts)
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
                for _, future in batch:
                    if not future.done():
                        future.cancel()
                raise

    async def _batch_inference(self, texts: List[str]) -> List[Intent]:
        """Run batch inference on the model"""
        if self.model is None:
            raise RuntimeError("Language model not initialized")

        with torch.no_grad():
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
            
            # Process outputs into Intent objects
            results = []
            for output in outputs:
                # Convert model output to Intent object
                # This is a placeholder - implement based on your model's output format
                intent = Intent(
                    action_type="",  # Extract from output
                    confidence=0.0,  # Extract from output
                    parameters={},   # Extract from output
                    raw_output={}    # Store raw output
                )
                results.append(intent)
                
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