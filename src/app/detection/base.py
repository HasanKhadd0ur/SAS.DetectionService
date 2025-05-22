from typing import AsyncGenerator, List
from app.core.models.message import Message
from app.core.models.events_models import Event

class DetectionStrategy:
    def detect_events(self, messages: AsyncGenerator[List[Message],None]) -> AsyncGenerator[List[Event],None]:
        """Detects events from a list of messages."""
        raise NotImplementedError("This method should be implemented by subclasses.")
