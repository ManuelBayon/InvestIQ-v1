from typing import Protocol

import pandas as pd

from backtest_engine.common.enums import FIFOSide
from backtest_engine.common.types import ExecutionLogEntry, FIFOPosition


class PortfolioProtocol(Protocol):
    """
    HF-grade abstraction of a Portfolio.
    Strategies depend on this protocol, not on the concrete Portfolio implementation.
    """
    fifo_queues: dict[FIFOSide, list[FIFOPosition]]
    current_position: float
    realized_pnl: float
    execution_log: list[ExecutionLogEntry]

    def append_log_entry(self, entry: ExecutionLogEntry) -> None:
        """
        Append an execution log entry (immutable audit trail).
        """
        ...

    def generate_and_apply_fifo_operations_from_signals(
            self,
            signals: pd.DataFrame,
    ) -> None:
        ...