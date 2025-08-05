from abc import ABC, abstractmethod
from app.core.models.events_models import Event

class EventCriterion(ABC):
    @abstractmethod
    def is_satisfied(self, event: Event) -> bool:
        pass
