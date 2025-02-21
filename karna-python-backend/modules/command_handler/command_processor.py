from base import SingletonMeta, BaseService
from .command_keys import CommandKeys
import logging
import json
import os
import asyncio
import uuid

class CommandService(BaseService, metaclass=SingletonMeta):
    def __init__(self, *args, **kwargs):
        if not hasattr(self, '_initialized'):
            super().__init__()
            self._request_queue = asyncio.Queue()
            self.commands_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                                            'data', 'commands-store.json')
            self._resources = {} # TODO use sqlite and always query instead of validating from object memory
            self._initialized = True
            self.logger.info("CommandService instance created")

    async def initialize(self) -> None:
        """Initialize command service resources"""
        try:
            self.logger.info("Initializing CommandService...")
            # Load commands file
            if os.path.exists(self.commands_file):
                with open(self.commands_file, 'r') as f:
                    self._resources['commands'] = json.load(f)
                    self.logger.debug(f"Loaded {len(self._resources['commands'].get('commands', []))} commands from storage")
            else:
                self._resources['commands'] = {'commands': []}
                self.logger.info("Created new commands storage")
            
            print("Store Resources: ", self._resources)
            self.logger.info("CommandService initialized successfully")
                
        except Exception as e:
            self.logger.error(f"Failed to initialize CommandService: {str(e)}")
            raise

    async def shutdown(self) -> None:
        """Clean up resources"""
        self.logger.info("Shutting down CommandService...")
        self._resources.clear()
        self.logger.info("CommandService shutdown complete")

    async def preprocess(self, data):
        """Preprocess the command data"""
        self.logger.debug(f"Preprocessing command data: {data}")
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
            
        self.logger.debug(f"Preprocessed data: {data_dict}")
        return data_dict

    async def validate(self, data):
        """Validate and store command data if not already present"""
        try:
            self.logger.debug(f"Validating command data: {data}")
            command = data.get(CommandKeys.USER_COMMAND.value, '').lower()
            domain = data.get(CommandKeys.TASK_DOMAIN_ID.value, '').lower()
            uuid_value = data.get(CommandKeys.UUID.value)

            if not command or command == domain:
                self.logger.error("Invalid command: Command cannot be empty or equal to domain")
                return None

            available_commands = self._resources.get('commands', {'commands': []})
            
            # Try to find existing command
            existing_command = next(
                (cmd for cmd in available_commands['commands'] 
                 if (uuid_value and cmd['uuid'] == uuid_value) or 
                    (cmd['name'].lower() == command and cmd['domain'].lower() == domain)
                ), None)

            if existing_command:
                self.logger.info(f"Found existing command: {command}")
                return {
                    CommandKeys.USER_COMMAND.value: command,
                    CommandKeys.TASK_DOMAIN_ID.value: domain,
                    CommandKeys.IS_IN_CACHE.value: existing_command['is_in_cache'],
                    CommandKeys.UUID.value: existing_command['uuid']
                }

            # Create new command
            new_command = {
                'name': command,
                'domain': domain,
                'is_in_cache': False,
                'uuid': str(uuid.uuid4())
            }
            
            self.logger.info(f"Creating new command: {command}")
            available_commands['commands'].append(new_command)
            with open(self.commands_file, 'w') as f:
                json.dump(available_commands, f, indent=4)

            return {
                CommandKeys.USER_COMMAND.value: command,
                CommandKeys.TASK_DOMAIN_ID.value: domain,
                CommandKeys.IS_IN_CACHE.value: False,
                CommandKeys.UUID.value: new_command['uuid']
            }

        except Exception as e:
            self.logger.error(f"Error validating command: {str(e)}")
            return None

    async def process_command(self, data):
        """Process a command asynchronously"""
        self.logger.info(f"Processing command: {data}")
        try:
            preprocessed_data = await self.preprocess(data)
            processed_data = await self.validate(preprocessed_data)
            if processed_data and processed_data[CommandKeys.IS_IN_CACHE.value]:
                processed_data = await self.postprocess(processed_data)
            return processed_data
        except Exception as e:
            self.logger.error(f"Error processing command: {str(e)}")
            raise

    async def postprocess(self, data):
        """Post process the command data"""
        self.logger.debug(f"Post-processing command data: {data}")
        return data

# Singleton instance management
_command_service_instance = None

def get_command_service_instance():
    global _command_service_instance
    if _command_service_instance is None:
        _command_service_instance = CommandService()
    return _command_service_instance

if __name__ == "__main__":
    async def test():
        command_service = get_command_service_instance()
        await command_service.initialize()
        test_command = "Search cats on youtube, domain youtube.com"
        result = await command_service.process_command(test_command)
        print(result)
        await command_service.shutdown()

    asyncio.run(test())
