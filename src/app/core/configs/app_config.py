class HDBSCANConfig:
    WINDOW_SIZE = 1000
    TIME_WINDOW_DAYS = 3
    MIN_CLUSTER_SIZE = 15
    MIN_BATCH_SIZE = 100
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
