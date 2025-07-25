from abc import ABC, abstractmethod
from app.core.models.events_models import DetectionContext

class DetectionStrategy(ABC):

    @abstractmethod
    async def detect(self, context: DetectionContext) -> DetectionContext:
        pass