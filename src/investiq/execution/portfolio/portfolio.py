from collections import defaultdict

from investiq.utilities.logger.factory import LoggerFactory
from investiq.utilities.logger.protocol import LoggerProtocol
from investiq.execution.portfolio.execution.api import PortfolioExecutionStrategy
from investiq.execution.portfolio.execution.factory import PortfolioExecutionFactory
from investiq.execution.portfolio.types import Fill
from investiq.execution.transition.enums import FIFOSide
from investiq.execution.transition.types import FIFOPosition, FIFOOperation


class Portfolio:

    def __init__(
            self,
            logger_factory: LoggerFactory,
            initial_cash : float
    ):
        self._logger_factory = logger_factory
        self._logger : LoggerProtocol =self._logger_factory.child("Portfolio").get()

        self._fifo_exec_factory = PortfolioExecutionFactory()

        self.current_position: float = 0.0

        self.cash = initial_cash
        self.realized_pnl: float = 0.0
        self.unrealized_pnl: float = 0.0

        self.fifo_queues : dict[FIFOSide, list[FIFOPosition]] = defaultdict(list)
        self.execution_log : list[Fill] = []

    def append_log_entry(
            self,
            entry: Fill
    ) -> None:
        self.execution_log.append(entry)

    def apply_operations(
            self,
            operations: list[FIFOOperation]
    ) -> None:
        for op in operations:
            strategy: PortfolioExecutionStrategy = self._fifo_exec_factory.create(op_type=op.type)
            execution_log: Fill = strategy.apply(portfolio=self, operation=op)
            self.append_log_entry(execution_log)