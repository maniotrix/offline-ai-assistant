from base import SingletonMeta, BaseService
from domain.command import Command, CommandResult
from database.repositories.command_repository import CommandRepository
import logging
import asyncio
from uuid import UUID
from typing import Optional

class CommandService(BaseService, metaclass=SingletonMeta):
    def __init__(self, *args, **kwargs):
        if not hasattr(self, '_initialized'):
            super().__init__()
            self._request_queue = asyncio.Queue()
            self.command_repository = CommandRepository()
            self._initialized = True
            self.logger.info("CommandService instance created")

    async def initialize(self) -> None:
        """Initialize command service resources"""
        try:
            self.logger.info("Initializing CommandService...")
            # No need to load from file anymore as we use database
            self.logger.info("CommandService initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize CommandService: {str(e)}")
            raise

    async def shutdown(self) -> None:
        """Clean up resources"""
        self.logger.info("Shutting down CommandService...")
        self.logger.info("CommandService shutdown complete")

    async def preprocess(self, data: str) -> tuple[str, str]:
        """Preprocess the command data"""
        self.logger.debug(f"Preprocessing command data: {data}")
        command = ""
        domain = ""
        
        if isinstance(data, str):
            parts = data.split(",")
            for part in parts:
                part = part.strip()
                if part.lower().startswith('domain'):
                    tokens = part.split(' ', 1)
                    if len(tokens) > 1:
                        domain = tokens[1].strip()
                elif not part.lower().startswith('use keys'):
                    command = part
                    
        self.logger.debug(f"Preprocessed command: '{command}', domain: '{domain}'")
        return command, domain

    async def validate(self, command: str, domain: str) -> Optional[Command]:
        """Validate and store command if not already present"""
        try:
            self.logger.debug(f"Validating command: {command}, domain: {domain}")
            if not command or command == domain:
                self.logger.error("Invalid command: Command cannot be empty or equal to domain")
                return None

            # Try to find existing command in database
            with self.command_repository.get_db() as db:
                try:
                    existing_command = self.command_repository.find_by_name_and_domain(db, command, domain)
                    if existing_command:
                        self.logger.info(f"Found existing command: {command}")
                        return self.command_repository.to_domain(existing_command)

                    # Create new command
                    new_command = Command(
                        name=command,
                        domain=domain,
                        is_in_cache=False
                    )
                    
                    self.logger.info(f"Creating new command: {command}")
                    db_fields = self.command_repository.from_domain(new_command)
                    db_command = self.command_repository.create(db, **db_fields)
                    return self.command_repository.to_domain(db_command)
                except Exception as db_error:
                    self.logger.error(f"Database operation failed: {str(db_error)}")
                    raise

        except Exception as e:
            self.logger.error(f"Error validating command: {str(e)}")
            return None

    async def process_command(self, data: str) -> Optional[CommandResult]:
        """Process a command asynchronously"""
        self.logger.info(f"Processing command: {data}")
        try:
            command_text, domain = await self.preprocess(data)
            command = await self.validate(command_text, domain)
            if not command:
                return CommandResult(
                    command=Command(name=command_text, domain=domain),
                    success=False,
                    message="Invalid command"
                )
                
            result = CommandResult(
                command=command,
                success=True,
                message="Command processed successfully"
            )
            
            if command.is_in_cache:
                result = await self.postprocess(result)
            return result
            
        except Exception as e:
            self.logger.error(f"Error processing command: {str(e)}")
            raise

    async def postprocess(self, result: CommandResult) -> CommandResult:
        """Post process the command result"""
        self.logger.debug(f"Post-processing command result: {result}")
        return result
    
    def get_status(self) -> str:
        """Get service status"""
        if not self._initialized:
            return "not_initialized"

        return "running"

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
        print(f"Command: {result.command.name}")
        print(f"Success: {result.success}")
        print(f"Message: {result.message}")
        await command_service.shutdown()

    asyncio.run(test())
