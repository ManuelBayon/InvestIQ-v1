from typing import Protocol

from engine.backtest_engine.common.types import ExecutionLogEntry, FIFOOperation


class PortfolioProtocol(Protocol):
    """
    HF-grade abstraction of a Portfolio.
    Strategies depend on this protocol, not on the concrete Portfolio implementation.
    """

    def append_log_entry(self, entry: ExecutionLogEntry) -> None:
        """
        Append an execution log entry (immutable audit trail).
        """
        ...

    def apply_operations(
            self,
            operations: list[FIFOOperation],
    ) -> None:
        ...