


# Define a postprcessing pipelie
from app.pipeline.pipeline import Pipeline
from app.pipeline.stages.events_locating_stage import EventsLocatingStage
from app.pipeline.stages.events_summarization_stage import EventsSummerizationStage
from app.pipeline.stages.events_publishing_stage import EventsPublishingStage
from app.pipeline.stages.events_topic_classification import EventsTopicClassificationStage


postprocessing_pipeline= Pipeline()
postprocessing_pipeline.add_stage(EventsSummerizationStage)
postprocessing_pipeline.add_stage(EventsLocatingStage)
postprocessing_pipeline.add_stage(EventsTopicClassificationStage)




# Define a publishing pipeline
publishing_pipeline= Pipeline()
publishing_pipeline.add_stage(EventsPublishingStage)

