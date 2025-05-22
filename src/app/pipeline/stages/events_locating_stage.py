from typing import Optional
from app.core.services.location_inference_service import LocationInferenceService
from app.pipeline.base import ProcessingStage
from app.core.models.events_models import DetectionContext

class EventsLocatingStage(ProcessingStage):
    def __init__(self, location_service: Optional[LocationInferenceService] ):
        self.location_service = location_service

    def process(self, detection_context: DetectionContext, nextStep: Optional[ProcessingStage] = None) -> DetectionContext:
        for event in detection_context.detected_events:
            # Extract location from event title
            # location_name = self.location_service.extract_message_location(event.messages[0])
          
            location_name = self.location_service.extract_event_location(event)
            event.location_name=location_name
            geocoded_location = self.location_service.geocode(location_name)
            # print(geocoded_location)
            # Set it on the event
            event.location = geocoded_location

        # Continue to next step if provided
        if nextStep:
            return nextStep.process(detection_context)
        return detection_context
