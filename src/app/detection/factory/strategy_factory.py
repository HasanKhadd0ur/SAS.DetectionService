from app.detection.registry.strategy_registry import StrategyRegistry
from app.detection.base import DetectionStrategy

class StrategyFactory:
    @staticmethod
    def create_strategy(name: str) -> DetectionStrategy:
        strategy_creator = StrategyRegistry.get(name)
        if not strategy_creator:
            raise ValueError(f"Strategy '{name}' is not registered.")
        return strategy_creator()
