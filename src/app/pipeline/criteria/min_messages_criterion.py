from app.pipeline.base.base_criterion import EventCriterion

class MinMessagesCriterion(EventCriterion):
    def __init__(self, min_messages: int):
        self.min_messages = min_messages

    def is_satisfied(self, event) -> bool:
        return len(event.messages) >= self.min_messages
