from typing import List, Optional
from app.core.models.message import Message
from app.core.models.events_models import Event, Location

class LocationInferenceService:
    def __init__(self, *args, **kwargs):
        pass  # Dummy version, no real model loading

    def extract_message_location_mentions(self, message: Message) -> List[str]:
        """Always return a constant location name."""
        return ["Damascus"]
    
    def extract_message_location(self, message: Message) -> List[str]:
        """Always return a constant location name."""
        return ["Damascus"]
    
    def extract_event_location(self, event: Event) -> str:
        
        return "Jableh, Syria"

    def geocode(self, location_name: str) -> Location:
        """Always return a constant location for any input."""
        return Location(latitude=33.5138, longtiude=36.2765)
