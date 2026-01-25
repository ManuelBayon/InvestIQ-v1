from collections import defaultdict

from invest_iq.engines.backtest_engine.common.enums import FIFOSide
from invest_iq.engines.backtest_engine.common.types import FIFOPosition, ExecutionLogEntry, FIFOOperation
from invest_iq.engines.backtest_engine.portfolio.protocol import PortfolioProtocol
from invest_iq.engines.backtest_engine.portfolio.execution_strategies.factory import FIFOExecutionFactory
from invest_iq.engines.backtest_engine.transition_engine.engine import TransitionEngine
from invest_iq.engines.backtest_engine.portfolio.execution_strategies.interface import PortfolioExecutionStrategy
from invest_iq.engines.utilities.logger.factory import LoggerFactory

from invest_iq.engines.utilities.logger.protocol import LoggerProtocol


class Portfolio(PortfolioProtocol):

    def __init__(
            self,
            logger_factory: LoggerFactory,
            transition_engine: TransitionEngine,
            initial_cash : float
    ):
        self._logger_factory = logger_factory
        self._logger : LoggerProtocol =self._logger_factory.child("Portfolio").get()

        self._fifo_exec_factory = FIFOExecutionFactory(
            logger_factory=self._logger_factory
        )
        self.transition_engine = transition_engine

        self.current_position: float = 0.0

        self.cash = initial_cash
        self.realized_pnl: float = 0.0
        self.unrealized_pnl: float = 0.0

        self.fifo_queues : dict[FIFOSide, list[FIFOPosition]] = defaultdict(list)
        self.execution_log : list[ExecutionLogEntry] = []

    def append_log_entry(
            self,
            entry: ExecutionLogEntry
    ) -> None:
        self.execution_log.append(entry)

    def apply_operations(
            self,
            operations: list[FIFOOperation]
    ) -> None:
        for op in operations:
            strategy: PortfolioExecutionStrategy = self._fifo_exec_factory.create(fifo_op_type=op.type)
            execution_log: ExecutionLogEntry = strategy.apply(self, operation=op)
            self.append_log_entry(execution_log)