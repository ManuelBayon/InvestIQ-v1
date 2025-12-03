from abc import ABC, abstractmethod

from backtest_engine.portfolio.protocol import PortfolioProtocol
from backtest_engine.common.types import ExecutionLogEntry, FIFOOperation

from backtest_engine.portfolio.execution_strategies.base import FIFOExecutionStrategyBase
from backtest_engine.portfolio.execution_strategies.protocol import PortfolioExecutionStrategyProtocol


class PortfolioExecutionStrategy(PortfolioExecutionStrategyProtocol, FIFOExecutionStrategyBase, ABC):

    def __init_subclass__(
            cls,
            **kwargs: object
    ) -> None:
        super().__init_subclass__(**kwargs)
        if not isinstance(getattr(cls, "STRATEGY_NAME", None), str) or not cls.STRATEGY_NAME.strip():
            raise TypeError(f"{cls.__name__} must define a non-empty STRATEGY_NAME")

    @abstractmethod
    def apply(
            self,
            portfolio : PortfolioProtocol,
            operation: FIFOOperation
    ) -> ExecutionLogEntry:
        ...