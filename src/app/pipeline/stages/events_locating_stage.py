from typing import Optional
from app.pipeline.base import ProcessingStage
from app.core.models.events_models import DetectionContext

class EventsLocatingStage(ProcessingStage):

    def process(self, detection_context : DetectionContext, nextStep: Optional[ProcessingStage] = None) -> DetectionContext:
    
        return detection_context
