from typing import Optional
from app.core.services.location_inference_service import LocationInferenceService
from app.core.models.events_models import DetectionContext
from app.core.services.logging_service import LoggingService
from app.pipeline.base.base import ProcessingStage

logger = LoggingService("DetectionAgent").get_logger()

class EventsLocatingStage(ProcessingStage):
    def __init__(self, location_service: Optional[LocationInferenceService]):
        self.location_service = location_service

    def process(self, detection_context: DetectionContext, nextStep: Optional[ProcessingStage] = None) -> DetectionContext:
        for event in detection_context.detected_events:
            try:
                location_name = self.location_service.extract_event_location(event)
                event.location_name = location_name
                logger.info(f"Extracted location name '{location_name}' for event {getattr(event, 'id', 'unknown')}")

                geocoded_location = self.location_service.geocode(location_name)

                event.location = geocoded_location
                logger.info(f"Geocoded location for event {getattr(event, 'id', 'unknown')}: {geocoded_location}")

            except Exception as e:
                logger.error(f"Failed to extract or geocode location for event {getattr(event, 'id', 'unknown')}: {e}")
                event.location_name = None
                event.location = None

        if nextStep:
            return nextStep.process(detection_context)
        return detection_context
