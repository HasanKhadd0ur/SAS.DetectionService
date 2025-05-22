from app.core.models.message import Message
from app.core.models.events_models import Event, Location
from typing import List
import uuid
from datetime import datetime

class EventsService:
    def __init__(self):
        pass  # No real model used here

    def classify_event_topic(self, messages: List[Message]) -> str:
        """Dummy topic classifier. In real case, use NLP classifier."""
        return "dummy-topic"

    def summarize_event(self, messages: List[Message]) -> str:
        """Dummy summarization. In real case, use text summarizer."""
        return "This is a dummy summary of the event."

    def create_event(self, messages: List[Message], location: Location) -> Event:
        """Creates a dummy Event from messages and location."""
        return Event(
            id=str(uuid.uuid4()),
            topic=self.classify_event_topic(messages),
            summary=self.summarize_event(messages),
            time=datetime.utcnow(),
            location=location,
            messages=messages,
            mentioned_location= ""
        )
