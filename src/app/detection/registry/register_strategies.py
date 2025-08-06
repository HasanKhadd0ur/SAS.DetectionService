from app.core.configs.app_config import StrategyParamsConfig
from app.detection.strategies.hdbscan_detection_strategy import HDBSCANDetectionStrategy
from app.detection.strategies.simple_rule_based import SimpleRuleBased
from app.detection.registry.strategy_registry import StrategyRegistry

def register_strategies():
    hdbscan_params = StrategyParamsConfig.strategies["hdbscan"]

    # Register HDBSCAN with parameters
    StrategyRegistry.register("hdbscan", lambda: HDBSCANDetectionStrategy(
        window_size=hdbscan_params["window_size"],
        time_window_days=hdbscan_params["time_window_days"],
        min_cluster_size=hdbscan_params["min_cluster_size"],
        min_batch_size=hdbscan_params["min_batch_size"],
        min_samples=hdbscan_params["min_samples"],
    ))

    # Register simple rule-based strategy (no config needed)
    StrategyRegistry.register("rulebased", lambda: SimpleRuleBased())
