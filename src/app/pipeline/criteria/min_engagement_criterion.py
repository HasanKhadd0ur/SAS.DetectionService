from app.pipeline.base.base_criterion import EventCriterion
from app.core.models.events_models import Event

class MinEngagementCriterion(EventCriterion):
    def __init__(self, min_engagement: int):
        self.min_engagement = min_engagement

    def is_satisfied(self, event: Event) -> bool:
        # Sum engagement scores across all messages of the event
        total_engagement = sum(getattr(msg, "engagement_score", 0) for msg in event.messages)
        return total_engagement >= self.min_engagement
