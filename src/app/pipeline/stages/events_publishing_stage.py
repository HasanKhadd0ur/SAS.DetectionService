from typing import List, Optional
from app.pipeline.base import ProcessingStage
from app.core.models.events_models import Event

class EventsPublishingStage(ProcessingStage):

    def process(self, events: List[Event], nextStep: Optional[ProcessingStage] = None) -> List[Event]:
    
        return events
