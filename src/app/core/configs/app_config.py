from app.pipeline.criteria.message_diversity_criterion import MessageDiversityCriterion
from app.pipeline.criteria.min_engagement_criterion import MinEngagementCriterion
from app.pipeline.criteria.min_messages_criterion import MinMessagesCriterion


class HDBSCANConfig:
    WINDOW_SIZE = 70
    TIME_WINDOW_DAYS = 3
    MIN_CLUSTER_SIZE = 5
    MIN_BATCH_SIZE = 50
    MIN_SAMPLES = 5


class StrategyParamsConfig:
    strategies = {
        "hdbscan": {
            "window_size": HDBSCANConfig.WINDOW_SIZE,
            "time_window_days": HDBSCANConfig.TIME_WINDOW_DAYS,
            "min_cluster_size": HDBSCANConfig.MIN_CLUSTER_SIZE,
            "min_batch_size": HDBSCANConfig.MIN_BATCH_SIZE,
            "min_samples": HDBSCANConfig.MIN_SAMPLES
        },
        "rulebased": {}  # No params needed for now
    }


ALLOWED_RULES = {
    "min_cluster_size": {
        "type": int,
        "default": 5,
        "enabled": True,
        "description": "Minimum number of samples in a cluster"
    },
    "min_distinct_words": {
        "type": float,
        "default": 0.3,
        "enabled": True,
        "description": "Minimum ratio of distinct words to total words in event messages"
},
    "min_engagement": {
        "type": int,
        "default": 2000,
        "enabled": True,
        "description": "Minimum total engagement score for event messages"
    }
    # Add more rules here if needed
}


# Criteria registry mapping rule names to corresponding criterion classes
CRITERIA_MAP = {
    "min_cluster_size": MinMessagesCriterion,
    "min_distinct_words": MessageDiversityCriterion,
    "min_engagement": MinEngagementCriterion,
    # Add more criteria mappings here
}
