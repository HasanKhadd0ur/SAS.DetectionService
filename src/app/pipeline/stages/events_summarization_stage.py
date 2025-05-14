from typing import Optional
from app.pipeline.base import ProcessingStage
from app.core.models.events_models import DetectionContext

class EventsSummerizationStage(ProcessingStage):

    def process(self, detection_context : DetectionContext, nextStep: Optional[ProcessingStage] = None) -> DetectionContext:
        
        for event in detection_context.detected_events : 
            event.summary = event.messages[0] if event.messages else "No summary available"

        # If there's a next step, pass the events to it
        if nextStep:
            return nextStep.process(detection_context)

        return detection_context
