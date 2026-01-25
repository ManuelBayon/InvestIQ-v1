from abc import abstractmethod, ABC
from invest_iq.engines.backtest_engine.transition_engine.fifo.guards_strategies.base import SafeGuardBase
from invest_iq.engines.backtest_engine.transition_engine.fifo.guards_strategies.protocol import SafeGuardProtocol
from invest_iq.engines.backtest_engine.common.types import ResolveContext


class SafeGuard[E](SafeGuardProtocol[E], SafeGuardBase, ABC):
    """
    Hybrid interface: combines Protocol + base class (logger, STRATEGY_NAME).
    """
    def __init_subclass__(cls, **kwargs: object) -> None:
        super().__init_subclass__(**kwargs)
        if bool(getattr(cls, "__abstractmethods__", False)):
            return
        if not isinstance(getattr(cls, "STRATEGY_NAME", None), str) or not cls.STRATEGY_NAME.strip():
            raise TypeError(f"{cls.__name__} must define a non-empty STRATEGY_NAME")

    @abstractmethod
    def check(
        self,
        context: ResolveContext,
        expected : E
    ) -> None:
        ...