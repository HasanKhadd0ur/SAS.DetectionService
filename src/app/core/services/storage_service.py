from typing import Dict, List, Optional
from app.core.models.events_models import Event
from app.core.models.message import Message

class StorageService:
    def __init__(self):
        self._events: Dict[str, Event] = {}

    def store_event(self, event: Event) -> None:
        """Store a new event in memory."""
        self._events[event.id] = event
        print(f"[StorageService] Stored event with ID: {event.id}")

    def add_message_to_event(self, event_id: str, message: Message) -> bool:
        """Append a message to an existing event."""
        event = self._events.get(event_id)
        if event:
            event.messages.append(message)
            print(f"[StorageService] Added message to event ID: {event_id}")
            return True
        print(f"[StorageService] Event with ID {event_id} not found")
        return False

    def get_event(self, event_id: str) -> Event:
        """Retrieve an event by ID."""
        return self._events.get(event_id)

    def list_events(self) -> List[Event]:
        """Return all stored events."""
        return list(self._events.values())
