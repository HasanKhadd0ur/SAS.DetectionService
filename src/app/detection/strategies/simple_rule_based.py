import asyncio
from datetime import datetime
from typing import AsyncGenerator, List
import uuid
from app.core.models.message import Message
from app.core.models.events_models import Event, Location

class SimpleRuleBased:
    async def detect_events(self, messages: List[Message]) -> AsyncGenerator[List[Event], None]:
        """Detect events from the given batch of messages."""
        # Simulate processing messages and detecting events
        await asyncio.sleep(0.5)  # Simulating async processing delay

        # Example event detection (to be replaced with real logic)
        event =  Event(
                        id=str(uuid.uuid4()),
                        topic="topic",
                        mentioned_location="",
                        summary=messages[0].content,
                        time=datetime.utcnow(),
                        location=Location(latitude=33.5, longitude=36.3),  # Corrected spelling
                        messages=messages
                        )
        
        yield [event]  # Yield a list of events asynchronously
