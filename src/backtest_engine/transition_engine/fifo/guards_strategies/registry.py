from typing import TypeVar, Callable, Any

from backtest_engine.common.enums import GuardName
from backtest_engine.transition_engine.fifo.guards_strategies.expectations import GuardExpectation
from backtest_engine.transition_engine.fifo.guards_strategies.interface import SafeGuard

class SafeGuardRegistry:

    _registry: dict[GuardName, type[SafeGuard[GuardExpectation]]] = {}

    @classmethod
    def register(
            cls,
            key: GuardName,
            strategy_cls: type[SafeGuard[GuardExpectation]]
    ) -> None:
        if key in cls._registry:
            raise KeyError(f"{key} is already registered")
        cls._registry[key] = strategy_cls

    @classmethod
    def get(
            cls,
            key: GuardName
    ) -> type[SafeGuard[GuardExpectation]]:
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
    def available(cls) -> list[GuardName]:
        return list(cls._registry.keys())

T = TypeVar("T", bound=SafeGuard[Any])
def register_safe_guard(key: GuardName) -> Callable[[type[T]], type[T]]:
    def decorator(cls: type[T]) -> type[T]:
        SafeGuardRegistry.register(key, cls)
        return cls
    return decorator