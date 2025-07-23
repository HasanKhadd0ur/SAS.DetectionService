import asyncio
from datetime import datetime
import uuid
from app.core.models.events_models import DetectionContext, Event, Location
from app.detection.base import DetectionStrategy


class SimpleRuleBased(DetectionStrategy):
    def __init__(self):
        pass
    
    async def detect(self, context: DetectionContext) -> DetectionContext:
        if not context.ready_for_detection(min_batch_size=3):
            # Not enough messages to detect
            return context
        
        # Simulate async delay
        await asyncio.sleep(0.05)

        # Create a simple event using the first message
        event = Event(
            id=str(uuid.uuid4()),
            topic="topic",
            mentioned_location="",
            summary=context.messages[0].content if context.messages else "",
            time=datetime.utcnow(),
            location=Location(latitude=33.5, longitude=36.3),
            messages=context.messages.copy()
        )

        context.detected_events = [event]
        context.updated_events = []
        
        # Append detected events to current_events
        context.current_events.extend(context.detected_events)

        return context