from app.core.models.events_models import Event

class ProcessingStage:
    def process(self, events: list[Event], nextStep: 'ProcessingStage' = None) -> list[Event]:
        """
        This method should be implemented by each filter to process the events.
        If a next filter exists, the message should be passed to it.
        """
        raise NotImplementedError("Filter must implement `process()`")
