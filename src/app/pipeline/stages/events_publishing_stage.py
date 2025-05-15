from typing import Optional
from app.pipeline.base import ProcessingStage
from app.core.models.events_models import DetectionContext

class EventsPublishingStage(ProcessingStage):

    def process(self, detection_context : DetectionContext, nextStep: Optional[ProcessingStage] = None) -> DetectionContext:
        """Process events by printing them and passing to the next step."""
        
        # Print the events to the console
        for event in  detection_context.detected_events:
            print(f"[+]  Topic: {event.topic}, Summary: {event.summary}, Time: {event.time}")

        # If there's a next step, pass the events to it
        if nextStep:
            return nextStep.process(detection_context)

        return detection_context
