
from modules.action_prediction import get_language_service_instance
from modules.command_handler.command_processor import get_command_service_instance
from services.base_service import BaseService
from domain.status import StatusContext

class StatusService(BaseService[StatusContext]):
    async def update_system_status(self) -> None:
        context = StatusContext(
            language=get_language_service_instance().get_status(),
            command=get_command_service_instance().get_status(),
        )
        self.notify_observers(context)