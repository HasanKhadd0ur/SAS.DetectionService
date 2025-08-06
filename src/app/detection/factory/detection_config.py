from app.detection.base import DetectionStrategy

class DetectionConfigManager:
    _current_strategy_name: str = "hdbscan"
    _strategy_instance: DetectionStrategy = None

    @classmethod
    def set_strategy(cls, name: str, strategy: DetectionStrategy):
        cls._current_strategy_name = name
        cls._strategy_instance = strategy

    @classmethod
    def get_current_strategy(cls) -> DetectionStrategy:
        return cls._strategy_instance

    @classmethod
    def get_current_strategy_name(cls) -> str:
        return cls._current_strategy_name
