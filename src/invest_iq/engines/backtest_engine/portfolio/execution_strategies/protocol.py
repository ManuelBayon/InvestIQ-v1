from typing import Protocol

from invest_iq.engines.backtest_engine.common.types import ExecutionLogEntry, FIFOOperation
from invest_iq.engines.backtest_engine.portfolio.protocol import PortfolioProtocol


class PortfolioExecutionStrategyProtocol(Protocol):

    def apply(
            self,
            portfolio : PortfolioProtocol,
            operation: FIFOOperation
    ) -> ExecutionLogEntry:
        ...