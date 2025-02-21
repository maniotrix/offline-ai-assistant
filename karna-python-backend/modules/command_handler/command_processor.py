from base import SingletonMeta, GlobalLogger
from .command_keys import CommandKeys
import logging
import json
import os

_LOGTAG_ = "[Command-Module]" 
logger = GlobalLogger(_LOGTAG_, level=logging.DEBUG).logger  # <-- Use module name as tag

class _BaseCommandProcessor:

    def validate(self, data):
        """Validate the input data."""
        raise NotImplementedError("Subclasses should implement this method")

    def preprocess(self, data):
        """Preprocess the input data before processing."""
        raise NotImplementedError("Subclasses should implement this method")
    
    def process(self, data):
        raise NotImplementedError("Subclasses should implement this method")

    def postprocess(self, data):
        """Postprocess the data after processing."""
        raise NotImplementedError("Subclasses should implement this method")

class _CommandProcessor(_BaseCommandProcessor, metaclass=SingletonMeta):
    def __init__(self, *args, **kwargs):
        if not hasattr(self, '_initialized'):
            super(_CommandProcessor, self).__init__(*args, **kwargs)
            self._initialized = True
            # Load available commands
            self.commands_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                                            'data', 'available-commands.json')
    
    def preprocess(self, data):
        # Preprocess the input data before processing
        # Clean and extract relevant information from the string
        # Parse a string to dict without argparse using command_keys
        data_dict = {}
        parts = data.split(",")
        for part in parts:
            part = part.strip()
            if part.lower().startswith('domain'):
                # Extract domain value
                tokens = part.split(' ', 1)
                if len(tokens) > 1:
                    data_dict[CommandKeys.TASK_DOMAIN_ID.value] = tokens[1].strip()
            elif part.lower().startswith('use keys'):
                # Instruction segment to use keys from command_keys; can be ignored
                continue
            else:
                # Assume remaining part is the user command
                data_dict[CommandKeys.USER_COMMAND.value] = part
        return data_dict

    def validate(self, data):
        """Validate the input data against available commands"""
        try:
            with open(self.commands_file, 'r') as f:
                available_commands = json.load(f)
            
            command = data.get(CommandKeys.USER_COMMAND.value, '').lower()
            domain = data.get(CommandKeys.TASK_DOMAIN_ID.value, '').lower()
            
            # Check if command exists
            for cmd in available_commands['commands']:
                if cmd['name'].lower() == command and cmd['domain'].lower() == domain:
                    data[CommandKeys.IS_IN_CACHE.value] = True
                    return data
            
            data[CommandKeys.IS_IN_CACHE.value] = False
            return data
            
        except Exception as e:
            logger.error(f"Error validating command: {str(e)}")
            data[CommandKeys.IS_IN_CACHE.value] = False
            return data

    def process(self, data):
        """
        Gets the instance of the command processor.

        Receives:
            str: A string input (description of the string input can be added here).

        Returns:
            dict: A dictionary with keys from command keys.
        """
        logger.debug("Processing data: %s", data)
        preprocessed_data = self.preprocess(data)
        processed_data = self.validate(preprocessed_data)
        return processed_data

    def postprocess(self, data):
        # Postprocess the data after processing
        # Example: format the response
        raise NotImplementedError("Not implemented yet")

# Singleton instance of CommandProcessor
_command_processor_instance = _CommandProcessor()

def get_command_processor_instance():
    return _command_processor_instance

if __name__ == "__main__":
    # Test use case without argparse
    test_command = "Search cats on youtube, domain youtube.com , use keys from command_keys"
    command_processor = get_command_processor_instance()
    processed_command = command_processor.process(test_command)
    try:
        logger.info(command_processor.postprocess(processed_command))
    except Exception as e:
        logger.info(processed_command)

    # Example usage with argparse:
    # import argparse
    # parser = argparse.ArgumentParser(description="Command Processor for Offline AI Assistant")
    # parser.add_argument("--command", type=str, required=True, help="The command to process")
    # args = parser.parse_args()
    # processed_command = command_processor.process(args.command)
    # logger.debug(command_processor.postprocess(processed_command))

    # Example usage:
    # python command_processor.py --command "open browser"
    # Output: Processed command: Action triggered for intent: example_intent
