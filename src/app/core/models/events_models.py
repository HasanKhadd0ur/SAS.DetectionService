
from dataclasses import dataclass
from datetime import datetime
from typing import List
from app.core.models.message import Message

@dataclass 
class Location:
    latitude :float 
    longtiude:float

@dataclass
class Event:
    id :str 
    topic:str
    summary: str=""
    time: datetime = datetime.utcnow()
    location: Location
    messages: List[Message]    
