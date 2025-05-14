import asyncio
from typing import AsyncGenerator, List

from app.core.models.message import Message
from app.core.models.events_models import Event
from app.detection.strategies.simple_rule_based import SimpleRuleBased

class EventDetectionService:
    def __init__(self, batch_size: int = 5):
        # Initialize with the batch size
        self.detector = SimpleRuleBased(batch_size=batch_size)

    async def detect_events_from_messages(self, messages: AsyncGenerator[Message, None]) -> AsyncGenerator[List[Event], None]:
        """
        This method consumes a stream of messages and returns a stream of events in batches.
        """
        async for event_batch in self.detector.detect_events(messages):
            yield event_batch

