from app.core.models.events_models import DetectionContext
from app.pipeline.base.base import ProcessingStage

class Pipeline:
    def __init__(self):
        self.filters = []

    def add_stage(self, filter_stage_class :ProcessingStage,*args):
        """Add a processing stage class (that extends ProcessingStage) to the pipeline."""
        # Instantiate the filter class and add it to the pipeline
        self.filters.append(filter_stage_class(*args))
        return self  # Allow method chaining


    def process(self, detection_context : DetectionContext) -> DetectionContext:
        """Process the events through all the filters in the pipeline."""
        for stage in self.filters:
            context = stage.process(detection_context)
        return context