from base import SingletonMeta, GlobalLogger
from .command_keys import CommandKeys
import logging
import json
import os
import asyncio

_LOGTAG_ = "[Command-Module]" 
logger = GlobalLogger(_LOGTAG_, level=logging.DEBUG).logger

class _BaseCommandProcessor:
    async def validate(self, data):
        """Validate the input data."""
        raise NotImplementedError("Subclasses should implement this method")

    async def preprocess(self, data):
        """Preprocess the input data before processing."""
        raise NotImplementedError("Subclasses should implement this method")
    
    async def process_command(self, data):
        raise NotImplementedError("Subclasses should implement this method")

    async def postprocess(self, data):
        """Postprocess the data after processing."""
        raise NotImplementedError("Subclasses should implement this method")

class _CommandProcessor(_BaseCommandProcessor, metaclass=SingletonMeta):
    def __init__(self, *args, **kwargs):
        if not hasattr(self, '_initialized'):
            super(_CommandProcessor, self).__init__(*args, **kwargs)
            self._initialized = True
            self._request_queue = asyncio.Queue()
            self.commands_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                                            'data', 'commands-store.json')
            self._resources = {}

    async def initialize(self) -> None:
        """Initialize command processor resources"""
        try:
            # Load commands file
            if os.path.exists(self.commands_file):
                with open(self.commands_file, 'r') as f:
                    self._resources['commands'] = json.load(f)
            else:
                self._resources['commands'] = {'commands': []}
                
        except Exception as e:
            logger.error(f"Failed to initialize command processor: {str(e)}")
            raise

    async def shutdown(self) -> None:
        """Clean up resources"""
        self._resources.clear()
    
    async def preprocess(self, data):
        # Clean and extract relevant information from the string
        data_dict = {}
        if isinstance(data, str):
            parts = data.split(",")
            for part in parts:
                part = part.strip()
                if part.lower().startswith('domain'):
                    tokens = part.split(' ', 1)
                    if len(tokens) > 1:
                        data_dict[CommandKeys.TASK_DOMAIN_ID.value] = tokens[1].strip()
                elif part.lower().startswith('use keys'):
                    continue
                else:
                    data_dict[CommandKeys.USER_COMMAND.value] = part
        else:
            data_dict = data
        return data_dict

    async def validate(self, data):
        """Validate the input data against available commands"""
        try:
            available_commands = self._resources.get('commands', {'commands': []})
            
            command = data.get(CommandKeys.USER_COMMAND.value, '').lower()
            domain = data.get(CommandKeys.TASK_DOMAIN_ID.value, '').lower()
            
            # Check if command exists
            for cmd in available_commands['commands']:
                if cmd['name'].lower() == command and cmd['domain'].lower() == domain:
                    data[CommandKeys.IS_IN_CACHE.value] = cmd['is_in_cache']
                    data[CommandKeys.UUID.value] = cmd['uuid']
                    return data
            
            data[CommandKeys.IS_IN_CACHE.value] = False
            data[CommandKeys.UUID.value] = None
            return data
            
        except Exception as e:
            logger.error(f"Error validating command: {str(e)}")
            data[CommandKeys.IS_IN_CACHE.value] = False
            data[CommandKeys.UUID.value] = None
            return data

    async def process_command(self, data):
        """
        Process a command asynchronously.

        Args:
            data: String or dict containing command information

        Returns:
            dict: A dictionary with processed command data
        """
        logger.debug("Processing data: %s", data)
        preprocessed_data = await self.preprocess(data)
        processed_data = await self.validate(preprocessed_data)
        if processed_data[CommandKeys.IS_IN_CACHE.value]:
            processed_data = await self.postprocess(processed_data)
        return processed_data

    async def postprocess(self, data):
        """Post process the command data"""
        # Add any post-processing logic here
        return data

# Singleton instance management
_command_processor_instance = None

def get_command_processor_instance():
    global _command_processor_instance
    if _command_processor_instance is None:
        _command_processor_instance = _CommandProcessor()
    return _command_processor_instance

if __name__ == "__main__":
    async def test():
        command_processor = get_command_processor_instance()
        await command_processor.initialize()
        test_command = "Search cats on youtube, domain youtube.com , use keys from command_keys"
        result = await command_processor.process_command(test_command)
        logger.info(result)
        await command_processor.shutdown()

    asyncio.run(test())
