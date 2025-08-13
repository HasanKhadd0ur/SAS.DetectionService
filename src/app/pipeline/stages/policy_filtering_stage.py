from app.core.configs.app_config import CRITERIA_MAP
from app.pipeline.base.base import ProcessingStage
from app.core.models.events_models import DetectionContext
from app.pipeline.base.base_criterion import EventCriterion
from app.core.services.policy_service import policy_service

class PolicyFilteringStage(ProcessingStage):
    def __init__(self):
        self.criteria: list[EventCriterion] = []

    def load_criteria(self):
        self.criteria.clear()
        for rule in policy_service.rules.values():
            if not getattr(rule, 'enabled', True):
                continue
            criterion_class = CRITERIA_MAP.get(rule.name)
            if criterion_class:
                # Instantiate criterion with the rule value; adjust if constructor differs
                self.criteria.append(criterion_class(rule.value))
            else:
                print(f"[WARN] No criterion mapped for rule '{rule.name}'")

    async def process(self, detection_context: DetectionContext, nextStep=None) -> DetectionContext:
        self.load_criteria()

        filtered_events = [
            event for event in detection_context.detected_events
            if all(c.is_satisfied(event) for c in self.criteria)
        ]

        removed_count = len(detection_context.detected_events) - len(filtered_events)
        print(f"[INFO] PolicyFilteringStage: Removed {removed_count} events.")

        detection_context.detected_events = filtered_events

        if nextStep:
            return nextStep.process(detection_context)
        return detection_context
