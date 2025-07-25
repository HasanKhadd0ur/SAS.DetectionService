
from app.core.configs.env_config import EnvSettings
from app.pipeline.factory.pipeline_factory import PipelineFactory


settings = EnvSettings()

pipeline_config = settings.get_pipeline_config()

factory = PipelineFactory(pipeline_config)

postprocessing_pipeline = factory.build_pipeline("POSTPROCESSING_PIPELINE")
publishing_pipeline = factory.build_pipeline("PUBLISHING_PIPELINE")
