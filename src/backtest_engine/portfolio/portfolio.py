from collections import defaultdict

from backtest_engine.common.enums import FIFOSide
from backtest_engine.common.types import FIFOPosition, ExecutionLogEntry, FIFOOperation
from backtest_engine.portfolio.contracts import PortfolioSignal
from backtest_engine.portfolio.protocol import PortfolioProtocol
from backtest_engine.portfolio.execution_strategies.factory import FIFOExecutionFactory
from backtest_engine.transition_engine.engine import TransitionEngine
from backtest_engine.portfolio.execution_strategies.interface import PortfolioExecutionStrategy
from utilities.logger.factory import LoggerFactory

from utilities.logger.protocol import LoggerProtocol


class Portfolio(PortfolioProtocol):

    def __init__(
            self,
            logger_factory: LoggerFactory,
            transition_engine: TransitionEngine,
            initial_cash : float
    ):
        self._logger_factory = logger_factory
        self._logger : LoggerProtocol =self._logger_factory.get()
        self._cash = initial_cash
        self.transition_engine = transition_engine
        self._realized_pnl: float = 0.0
        self._unrealized_pnl: float = 0.0
        self._current_position: float = 0.0
        self._fifo_queues : dict[FIFOSide, list[FIFOPosition]] = defaultdict(list)
        self._execution_log : list[ExecutionLogEntry] = []
        self._fifo_exec_factory: FIFOExecutionFactory = FIFOExecutionFactory(logger_factory=self._logger_factory)

    def append_log_entry(
            self,
            entry: ExecutionLogEntry
    ) -> None:
        self.execution_log.append(entry)

    def apply_fifo_operations(
            self,
            operations: list[FIFOOperation]
    ) -> None:
        for op in operations:
            strategy: PortfolioExecutionStrategy = self._fifo_exec_factory.create(fifo_op_type=op.type)
            execution_log: ExecutionLogEntry = strategy.apply(self, operation=op)
            self.append_log_entry(execution_log)

    def apply_signals(
            self,
            signals : list[PortfolioSignal]
    ) -> None:
        for signal in signals:
            fifo_operations : list[FIFOOperation] = self.transition_engine.process(
                current_position=self._current_position,
                timestamp=signal.timestamp,
                target_position=signal.target_position,
                price=signal.price,
                fifo_queues=self.fifo_queues
            )
            self.apply_fifo_operations(fifo_operations)

    def get_realized_pnl(self) -> float:
        return self._realized_pnl