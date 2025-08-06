from app.pipeline.criteria.message_diversity_criterion import MessageDiversityCriterion
from app.pipeline.criteria.min_engagement_criterion import MinEngagementCriterion
from app.pipeline.criteria.min_messages_criterion import MinMessagesCriterion


class HDBSCANConfig:
    WINDOW_SIZE = 1000
    TIME_WINDOW_DAYS = 3
    MIN_CLUSTER_SIZE = 6
    MIN_BATCH_SIZE =100
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
    "Min Cluster Size": {
        "type": int,
        "default": 5,
        "enabld":True,
        "description": "Minimum number of samples in a cluster"
    },
    "Min Distinct Words": {
        "type": int,
        "default": 10,
        "enabled": True,
        "description": "Minimum number of distinct words across all event messages"
    },
    "Min Engagement": {
        "type": int,
        "default": 2000,
        "enabled": True,
        "description": "Minimum total engagement score for event messages"
    }    
    # You can add more later: "min_samples", "topic_threshold", etc.
}


# New: Criteria registry mapping rule names to criterion classes or factory functions
CRITERIA_MAP = {
    "min_cluster_size": MinMessagesCriterion,
    "min_distinct_words": MessageDiversityCriterion,
     "min_engagement": MinEngagementCriterion,
    # Add more criteria mappings here
}