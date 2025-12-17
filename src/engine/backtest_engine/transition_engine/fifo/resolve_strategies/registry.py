from typing import Callable, TypeVar
from engine.backtest_engine.transition_engine.fifo.resolve_strategies.interface import FIFOResolveStrategy
from engine.backtest_engine.common.enums import AtomicActionType

R = TypeVar("R", bound=FIFOResolveStrategy)

class FIFOResolveRegistry:
    _registry: dict[AtomicActionType, type[FIFOResolveStrategy]] = {}

    @classmethod
    def register(
            cls,
            key: AtomicActionType,
            strategy_cls: type[FIFOResolveStrategy]
    ) -> None:
        if key in cls._registry:
            raise KeyError(f"{key} already registered")
        if not issubclass(strategy_cls, FIFOResolveStrategy):
            raise TypeError(f"{strategy_cls.__name__} must subclass FIFOResolveStrategy")
        cls._registry[key] = strategy_cls

    @classmethod
    def get(
            cls,
            key: AtomicActionType
    ) -> type[FIFOResolveStrategy]:
        try:
            return cls._registry[key]
        except KeyError:
            raise KeyError(f"{key} not registered; available={list(cls._registry.keys())}")

    @classmethod
    def available(cls) -> list[AtomicActionType]:
        return list(cls._registry.keys())

    @classmethod
    def clear(cls) -> None:
        return cls._registry.clear()

def register_fifo_resolve_strategy(key: AtomicActionType) -> Callable[[type[R]], type[R]]:
    def decorator(cls: type[R]) -> type[R]:
        FIFOResolveRegistry.register(key, cls)
        return cls
    return decorator