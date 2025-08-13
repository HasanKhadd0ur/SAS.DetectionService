from app.core.models.events_models import DetectionContext

class ProcessingStage:
    async def process(self, detection_context : DetectionContext , nextStep: 'ProcessingStage' = None) -> DetectionContext:
        """
        This method should be implemented by each filter to process the events.
        If a next filter exists, the message should be passed to it.
        """
        raise NotImplementedError("Filter must implement `process()`")
