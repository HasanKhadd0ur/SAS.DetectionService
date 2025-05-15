from typing import AsyncGenerator, List
from app.core.models.message import Message
from app.core.models.events_models import DetectionContext, Event
from app.detection.base import DetectionStrategy
from app.pipeline.pipeline import Pipeline
from app.pipeline.registry import postprocessing_pipeline as post, publishing_pipeline as pub

class DetectionAgent:
    def __init__(
        self, 
        detection_strategy: DetectionStrategy, 
        postprocessing_pipeline: Pipeline = post, 
        publishing_pipeline: Pipeline = pub
    ):
        self.detection_strategy = detection_strategy
        self.postprocessing_pipeline = postprocessing_pipeline
        self.publishing_pipeline = publishing_pipeline

    def set_detection_strategy(self, strategy: DetectionStrategy):
        self.detection_strategy = strategy

    def set_postprocessing_pipeline(self, pipeline: Pipeline):
        self.postprocessing_pipeline = pipeline

    def set_publishing_pipeline(self, pipeline: Pipeline):
        self.publishing_pipeline = pipeline

    async def run(self, messages: AsyncGenerator[List[Message], None]) -> List[Event]:
        """Process messages using the detection strategy and pipelines."""
        events = []

        # Iterate over the messages in the asynchronous generator
        async for msg_batch in messages:
            # Detect events from the message batch
            async for event_batch in self.detection_strategy.detect_events(msg_batch):
                context= DetectionContext(detected_events=event_batch)
                 # Process the detected events through the postprocessing and publishing pipelines
                context = self.postprocessing_pipeline.process(context) 
                context=self.publishing_pipeline.process(context)
                events.extend(context.detected_events)

       
        return events
