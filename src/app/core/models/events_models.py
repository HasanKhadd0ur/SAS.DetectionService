
from dataclasses import dataclass, field
from datetime import datetime
from typing import List
from app.core.models.message import Message

@dataclass 
class Location:
    latitude :float =0.0
    longitude:float=0.0

@dataclass
class Event:
    id :str
    location: Location=field(default_factory=lambda: Location(latitude=33.33, longitude=34.34))
    topic:str=""
    summary: str=""
    messages: List[Message]=field(default_factory=list)
    location_name:str=""
    mentioned_location:str="" 
    time: datetime =  field(default_factory=datetime.utcnow)
    
    
    @staticmethod
    def create_from_messages(messages: List[Message]) -> "Event":
        
        event_id = "event-" + messages[0].id  # Or generate UUID
        return Event(id=event_id, messages=messages)

@dataclass
class DetectionContext:
    messages: List[Message]
    detected_events: List[Event] = field(default_factory=list)
    updated_events: List[Event] = field(default_factory=list)
    
     # All active events that are still tracked (used for update/merge logic)
    current_events: List[Event] = field(default_factory=list)
    
    def ready_for_detection(self, min_batch_size: int) -> bool:
        return len(self.messages) >= min_batch_size
    