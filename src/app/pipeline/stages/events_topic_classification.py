from typing import Optional
from app.pipeline.base import ProcessingStage
from app.core.models.events_models import DetectionContext
# from transformers import pipeline

class EventsTopicClassificationStage(ProcessingStage):
    
    def __init__(self):
        """Initialize the Arabic classification model."""
        # Use a pre-trained Arabic text classification model (e.g., BERT)
        # This is a general classification pipeline; customize if necessary
        # self.classifier = pipeline(
        #     'text-classification',
        #     model='asafaya/bert-base-arabic',
        #     tokenizer='asafaya/bert-base-arabic'
        # )
    def process(self, detection_context : DetectionContext, nextStep: Optional[ProcessingStage] = None) -> DetectionContext:
        """Process the events by classifying their topics using the Arabic model."""
        
        # for event in events:
        #     if event.content:  # Assuming the content of the event holds the relevant text
        #         # Predict the topic using the model
        #         prediction = self.classifier(event.content)
        #         # Extract the predicted topic (assumed to be the 'label' field from the prediction)
        #         event.topic = prediction[0]['label']
        #     else:
        #         event.topic = "Unknown"  # If no content available, set topic to 'Unknown'
        for event in detection_context.detected_events:
            event.topic="أخبار دمشق"
        # If there's a next step, pass the events to it
        if nextStep:
            return nextStep.process(detection_context)

        return detection_context
