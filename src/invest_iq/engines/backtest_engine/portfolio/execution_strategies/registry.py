from typing import Callable, TypeVar

from invest_iq.engines.backtest_engine.common.enums import FIFOOperationType
from invest_iq.engines.backtest_engine.portfolio.execution_strategies.interface import PortfolioExecutionStrategy


class FIFOExecutionRegistry:

    _registry: dict[FIFOOperationType, type[PortfolioExecutionStrategy]] = {}

    @classmethod
    def register(
            cls,
            key: FIFOOperationType,
            strategy_cls: type[PortfolioExecutionStrategy]
    ) -> None:
        if key in cls._registry:
            raise KeyError(f"{key} is already registered")
        cls._registry[key] = strategy_cls

    @classmethod
    def get(
            cls,
            key: FIFOOperationType
    ) -> type[PortfolioExecutionStrategy]:
        try:
            return cls._registry[key]
        except KeyError:
            raise KeyError(
                f"Transition: {key} is not supported"
                f"Available transitions: {cls.available()}"
            )

    @classmethod
    def clear(cls) -> None:
        cls._registry.clear()

    @classmethod
    def available(cls) -> list[FIFOOperationType]:
        return list(cls._registry.keys())

T = TypeVar("T", bound=PortfolioExecutionStrategy)
def register_fifo_execution(key: FIFOOperationType) -> Callable[[type[T]], type[T]]:
    def decorator(cls: type[T]) -> type[T]:
        FIFOExecutionRegistry.register(key, cls)
        return cls
    return decorator