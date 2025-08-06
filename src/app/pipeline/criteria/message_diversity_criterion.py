from app.pipeline.base.base_criterion import EventCriterion
import re

class MessageDiversityCriterion(EventCriterion):
    def __init__(self, min_distinct_words: int = 10):
        self.min_distinct_words = min_distinct_words

    def is_satisfied(self, event) -> bool:
        all_text = " ".join(getattr(m, 'text', '') for m in event.messages).lower()
        # Extract words using regex to handle punctuation, etc.
        words = re.findall(r'\b\w+\b', all_text)
        distinct_words = set(words)
        return len(distinct_words) >= self.min_distinct_words
