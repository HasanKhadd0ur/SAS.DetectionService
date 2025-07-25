


# Define a postprcessing pipelie
from app.core.configs.env_config import EnvConfig
from app.core.services.location_inference_service import LocationInferenceService
from app.pipeline.base.pipeline import Pipeline
from app.pipeline.stages.events_locating_stage import EventsLocatingStage
from app.pipeline.stages.events_summarization_stage import EventsSummerizationStage
from app.pipeline.stages.events_publishing_stage import EventsPublishingStage
from app.pipeline.stages.events_topic_classification import EventsTopicClassificationStage

location_service =LocationInferenceService("http://127.0.0.1:5000")

postprocessing_pipeline= Pipeline()
postprocessing_pipeline.add_stage(EventsSummerizationStage,EnvConfig())
postprocessing_pipeline.add_stage(EventsLocatingStage,location_service)
postprocessing_pipeline.add_stage(EventsTopicClassificationStage)




# Define a publishing pipeline
publishing_pipeline= Pipeline()
publishing_pipeline.add_stage(EventsPublishingStage)


# Shared dependency instances (singletons or factories)
shared_dependencies = {
    "LOCATION_SERVICE": location_service,
    "EnvConfig":EnvConfig()
    # Add more shared dependencies here if needed
}

STAGE_CLASS_MAP = {
    "EventsSummerizationStage": {
        "class": EventsSummerizationStage,
        "dependencies": []
    },
    "EventsLocatingStage": {
        "class": EventsLocatingStage,
        "dependencies": ['LOCATION_SERVICE']
    },
    "EventsTopicClassificationStage": {
        "class": EventsTopicClassificationStage,
        "dependencies": []
    },
    "EventsPublishingStage":{
        "class":EventsPublishingStage,
        "dependencies":[]
    }
}
