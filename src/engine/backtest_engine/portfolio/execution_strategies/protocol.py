from typing import Protocol

from engine.backtest_engine.common.types import ExecutionLogEntry, FIFOOperation
from engine.backtest_engine.portfolio.protocol import PortfolioProtocol


class PortfolioExecutionStrategyProtocol(Protocol):

    def apply(
            self,
            portfolio : PortfolioProtocol,
            operation: FIFOOperation
    ) -> ExecutionLogEntry:
        ...