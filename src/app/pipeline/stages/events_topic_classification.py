from typing import Optional
from app.pipeline.base.base import ProcessingStage
from app.core.models.events_models import DetectionContext
from app.core.services.topic_classification_service import TopicClassificationService
from app.core.services.logging_service import LoggingService  

class EventsTopicClassificationStage(ProcessingStage):
    """
    Pipeline stage responsible for assigning a topic to each detected event
    using a keyword-based topic classification service.
    """

    def __init__(self, classification_service: TopicClassificationService):
        """
        Initialize the stage with a topic classification service and a logger.

        Args:
            classification_service (TopicClassificationService): Service that classifies text into predefined topics.
        """
        self.classification_service = classification_service

        # Initialize logging
        self.logger = LoggingService(name="EventsTopicClassificationStage").get_logger()

    async def process(self, detection_context: DetectionContext, nextStep: Optional[ProcessingStage] = None) -> DetectionContext:
        """
        Process the detection context by classifying the topic of each detected event.

        Args:
            detection_context (DetectionContext): The current context containing detected events.
            nextStep (Optional[ProcessingStage]): The next processing stage in the pipeline.

        Returns:
            DetectionContext: Updated context with topics assigned to events.
        """

        self.logger.info("Starting topic classification for detected events.")

        for idx, event in enumerate(detection_context.detected_events, start=1):
            if event.summary:
                topic = self.classification_service.predict_topic(event.summary)
                event.topic = topic
                self.logger.debug(f"[Event {idx}] Classified topic: {topic}")
            else:
                event.topic = "أخبار المحافظات"
                self.logger.warning(f"[Event {idx}] Missing content. Assigned default topic: غير معروف")

        self.logger.info("Completed topic classification.")

        # Pass to the next stage if it exists
        if nextStep:
            self.logger.debug("Passing detection context to the next pipeline stage.")
            return nextStep.process(detection_context)

        return detection_context
