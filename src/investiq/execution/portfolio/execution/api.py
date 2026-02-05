from __future__ import annotations

from typing import ClassVar, Protocol

from investiq.execution.portfolio.types import Fill
from investiq.execution.transition.enums import FIFOSide
from investiq.execution.transition.types import FIFOOperation, FIFOPosition


class PortfolioProtocol(Protocol):
    current_position: float
    cash: float
    realized_pnl: float
    fifo_queues: dict[FIFOSide, list[FIFOPosition]]


class PortfolioExecutionStrategy(Protocol):
    NAME: ClassVar[str]

    def apply(
        self,
        *,
        portfolio: PortfolioProtocol,
        operation: FIFOOperation,
    ) -> Fill:
        ...
