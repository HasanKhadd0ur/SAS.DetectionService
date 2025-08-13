from app.pipeline.base.base_criterion import EventCriterion
import re

class MessageDiversityCriterion(EventCriterion):
    def __init__(self, min_ratio: float = 0.3):
        self.min_ratio = min_ratio

    def is_satisfied(self, event) -> bool:
        all_text = " ".join(getattr(m, 'text', '') for m in event.messages).lower()
        words = re.findall(r'\b\w+\b', all_text)
        total_words = len(words)
        if total_words == 0:
            return False
        distinct_words = set(words)
        ratio = len(distinct_words) / total_words
        return ratio >= self.min_ratio
