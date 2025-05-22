
from dataclasses import dataclass
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
    topic:str
    summary: str
    location: Location
    messages: List[Message]   
    location_name:str=""
    mentioned_location:str="" 
    time: datetime = datetime.utcnow()

@dataclass
class DetectionContext:
    detected_events : List[Event]
    updated_events : List[Event]=None
    