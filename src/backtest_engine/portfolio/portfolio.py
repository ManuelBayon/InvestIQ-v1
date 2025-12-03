from collections import defaultdict

import pandas as pd

from backtest_engine.common.enums import FIFOSide
from backtest_engine.common.types import FIFOPosition, ExecutionLogEntry, FIFOOperation
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
        self.realized_pnl: float = 0.0
        self._unrealized_pnl: float = 0.0
        self.current_position: float = 0.0
        self.fifo_queues : dict[FIFOSide, list[FIFOPosition]] = defaultdict(list)
        self.execution_log : list[ExecutionLogEntry] = []
        self.fifo_execution_factory: FIFOExecutionFactory = FIFOExecutionFactory(logger_factory=self._logger_factory)

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
            fifo_execution_strategy: PortfolioExecutionStrategy = self.fifo_execution_factory.create(fifo_op_type=op.type)
            execution_log: ExecutionLogEntry = fifo_execution_strategy.apply(self, op)
            self.append_log_entry(execution_log)

    def generate_and_apply_fifo_operations_from_signals(
            self,
            signals : pd.DataFrame,
    ) -> None:
        for _, row in signals.iterrows():
            current_position = self.current_position
            timestamp = row.timestamp
            target_position = float(row.target_position)
            price = row.close
            fifo_operations : list[FIFOOperation] = self.transition_engine.process(
                current_position=current_position,
                target_position=target_position,
                timestamp=timestamp,
                fifo_queues=self.fifo_queues,
                price=price
            )
            self.apply_fifo_operations(fifo_operations)

    def get_realized_pnl(self) -> float:
        return self.realized_pnl