from typing import AsyncGenerator, List
from app.core.models.message import Message
from app.core.models.events_models import DetectionContext, Event
from app.detection.base import DetectionStrategy
from app.pipeline.base.pipeline import Pipeline
from app.pipeline.factory.default_pipelines import postprocessing_pipeline as post, publishing_pipeline as pub
from app.core.services.logging_service import LoggingService

logger = LoggingService("DetectionAgent").get_logger()


class DetectionAgent:
    def __init__(self,
            strategy: DetectionStrategy,
            min_batch_size: int = 10,
            postprocessing_pipeline: Pipeline = post, 
            publishing_pipeline: Pipeline = pub):
        self.strategy = strategy
        self.context = DetectionContext(messages=[])
        self.min_batch_size = min_batch_size
        self.postprocessing_pipeline = postprocessing_pipeline
        self.publishing_pipeline = publishing_pipeline

    def set_detection_strategy(self, strategy: DetectionStrategy):
        self.strategy = strategy

    def set_postprocessing_pipeline(self, pipeline: Pipeline):
        self.postprocessing_pipeline = pipeline

    def set_publishing_pipeline(self, pipeline: Pipeline):
        self.publishing_pipeline = pipeline

    async def handel_messages(self, new_messages: AsyncGenerator[List[Message], None]) -> List[Event]:
        """Process messages using the detection strategy and pipelines."""

        # self.context.messages.extend(new_messages)
        
        async for batch in new_messages:  # batch is List[Message]
            self.context.messages.extend(batch)
            logger.info(f"Added {len(batch)} messages to buffer. Total now: {len(self.context.messages)}")

            if len(self.context.messages) >= self.min_batch_size:
                logger.info("Running detection strategy...")

                # Strategy handles detection + cleanup logic (e.g., clustering window, cutoff)
                self.context = await self.strategy.detect(self.context)

                # Run post-detection pipeline
                self.context =await  self.postprocessing_pipeline.process(self.context)
                self.context = await self.publishing_pipeline.process(self.context)
                logger.info(f"Detected {len(self.context.detected_events)} new events.")
                logger.info(f"Updated {len(self.context.updated_events)} events.")

                self.context.detected_events =[]
                self.context.updated_events=[]
                