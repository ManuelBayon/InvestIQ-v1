from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from investiq.execution.transition.enums import FIFOOperationType, FIFOSide
from investiq.execution.transition.types import FIFOOperation


@dataclass(frozen=True)
class PortfolioSignal:
    timestamp: datetime
    price: float
    target_position: float

@dataclass(frozen=True)
class Fill:

    timestamp: datetime
    operation_type : FIFOOperationType
    side : FIFOSide

    quantity : float
    execution_price : float

    operation_id: int
    linked_position_id: Optional[int]

    position_before : float
    position_after: float
    cash_before: float
    cash_after: float

    entry_price: Optional[float]
    exit_price: Optional[float]
    realized_pnl: Optional[float]

    instrument_id: Optional[str] = None

    @staticmethod
    def from_operation(
        *,
        operation: FIFOOperation,
        position_before: float,
        position_after: float,
        cash_before: float,
        cash_after: float,
        realized_pnl: Optional[float],
        entry_price: Optional[float],
        exit_price: Optional[float],
        instrument_id: Optional[str] = None,
    ) -> "Fill":
        """
        Convenience constructor: build a Fill from a FIFOOperation plus computed accounting.
        """
        return Fill(
            timestamp=operation.timestamp,
            operation_type=operation.type,
            side=operation.side,
            quantity=operation.quantity,
            execution_price=operation.execution_price,
            operation_id=operation.id,
            linked_position_id=operation.linked_position_id,
            position_before=position_before,
            position_after=position_after,
            cash_before=cash_before,
            cash_after=cash_after,
            realized_pnl=realized_pnl,
            entry_price=entry_price,
            exit_price=exit_price,
            instrument_id=instrument_id,
        )