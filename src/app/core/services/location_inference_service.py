import requests
from typing import List
from app.core.models.message import Message
from app.core.models.events_models import Event, Location

def serialize_message(message: Message) -> dict:
    data = message.__dict__.copy()
    data["created_at"] = message.created_at.isoformat()  # Serialize datetime
    return data

class LocationInferenceService:
    def __init__(self, base_url: str ):
        self.base_url = base_url

    def extract_message_location(self, message: Message) -> List[str]:
        response = requests.post(f"{self.base_url}/recognition/extract-message-location", json={"message":message.r})
        response.raise_for_status()
        print(response.json())
        return response.json()  

    def extract_event_location(self, event: Event) -> str:
            serialized_messages = [m.serialize_message() for m in event.messages]
            response = requests.post(
                f"{self.base_url}/resolution/extract-event-location",
                json=serialized_messages
            )
            response.raise_for_status()
            return response.json()
    def geocode(self, location_name: str) -> Location:
        response = requests.get(f"{self.base_url}/resolution/geocode", params={"location": location_name})
        response.raise_for_status()
        data = response.json()
        return Location(**data)  # Should match your Location model format
