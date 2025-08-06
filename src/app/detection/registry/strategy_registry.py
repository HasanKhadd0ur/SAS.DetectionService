# app/detection/registry/strategy_registry.py

from typing import Callable, Dict
from app.detection.base import DetectionStrategy

class StrategyRegistry:
    _registry: Dict[str, Callable[[], DetectionStrategy]] = {}

    @classmethod
    def register(cls, name: str, factory_func: Callable[[], DetectionStrategy]):
        cls._registry[name.lower()] = factory_func

    @classmethod
    def get(cls, name: str) -> Callable[[], DetectionStrategy]:
        return cls._registry.get(name.lower())

    @classmethod
    def available_strategies(cls):
        return list(cls._registry.keys())
