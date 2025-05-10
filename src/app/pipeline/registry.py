


# Define a postprcessing pipelie
from app.pipeline.pipeline import Pipeline
from app.pipeline.stages.events_locating_stage import EventsLocatingStage
from app.pipeline.stages.events_summerization_stage import EventsSummerizationStage
from app.pipeline.stages.events_publishing_stage import EventsPublishingStage


postprocessing_pipeline= Pipeline()
postprocessing_pipeline.add_stage(EventsSummerizationStage)
postprocessing_pipeline.add_stage(EventsLocatingStage)



# Define a publishing pipeline
publishing_pipeline= Pipeline()
publishing_pipeline.add_stage(EventsPublishingStage)

