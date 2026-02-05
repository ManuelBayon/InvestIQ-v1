from __future__ import annotations

from typing import ClassVar

from investiq.execution.portfolio.types import Fill
from investiq.execution.transition.enums import FIFOSide, FIFOOperationType
from investiq.execution.transition.types import FIFOOperation, FIFOPosition
from .api import PortfolioProtocol
from .registry import register_execution_strategy


def _require(cond: bool, msg: str) -> None:
    if not cond:
        raise ValueError(msg)


@register_execution_strategy(FIFOOperationType.OPEN)
class OpenPosition:
    NAME: ClassVar[str] = "OpenPosition"

    def apply(self, *, portfolio: PortfolioProtocol, operation: FIFOOperation) -> Fill:
        _require(operation.quantity > 0, f"[{self.NAME}] quantity must be > 0, got {operation.quantity}")

        direction = 1.0 if operation.side == FIFOSide.LONG else -1.0

        pos_before = portfolio.current_position
        pos_after = pos_before + operation.quantity * direction

        cash_before = portfolio.cash
        notional = operation.quantity * operation.execution_price
        cash_after = cash_before - direction * notional

        # Create FIFOPosition (open creates a new position)
        position = FIFOPosition(
            id=operation.id,
            is_active=True,
            timestamp=operation.timestamp,
            type=operation.type,
            side=operation.side,
            quantity=operation.quantity,
            price=operation.execution_price,
        )
        portfolio.fifo_queues[operation.side].append(position)
        portfolio.current_position = pos_after
        portfolio.cash = cash_after

        return Fill.from_operation(
            operation=operation,
            position_before=pos_before,
            position_after=pos_after,
            cash_before=cash_before,
            cash_after=cash_after,
            realized_pnl=None,
            entry_price=operation.execution_price,
            exit_price=None,
        )


@register_execution_strategy(FIFOOperationType.CLOSE)
class ClosePosition:
    NAME: ClassVar[str] = "ClosePosition"

    def apply(self, *, portfolio: PortfolioProtocol, operation: FIFOOperation) -> Fill:
        _require(operation.quantity > 0, f"[{self.NAME}] quantity must be > 0, got {operation.quantity}")
        _require(operation.linked_position_id is not None, f"[{self.NAME}] linked_position_id required for CLOSE")

        fifo = portfolio.fifo_queues[operation.side]
        matched = next((p for p in fifo if p.id == operation.linked_position_id), None)

        _require(matched is not None, f"[{self.NAME}] no FIFOPosition with id={operation.linked_position_id}")
        _require(matched.is_active, f"[{self.NAME}] position {matched.id} already closed")
        _require(operation.quantity <= matched.quantity, f"[{self.NAME}] close qty {operation.quantity} > available {matched.quantity}")

        # Mutate FIFOPosition
        if operation.quantity == matched.quantity:
            matched.is_active = False
        else:
            matched.quantity -= operation.quantity

        direction = 1.0 if operation.side == FIFOSide.LONG else -1.0
        pnl = (operation.execution_price - matched.price) * operation.quantity * direction

        pos_before = portfolio.current_position
        pos_after = pos_before - operation.quantity * direction

        cash_before = portfolio.cash
        notional = operation.quantity * operation.execution_price
        cash_after = cash_before + direction * notional

        portfolio.current_position = pos_after
        portfolio.cash = cash_after
        portfolio.realized_pnl += pnl

        return Fill.from_operation(
            operation=operation,
            position_before=pos_before,
            position_after=pos_after,
            cash_before=cash_before,
            cash_after=cash_after,
            realized_pnl=pnl,
            entry_price=matched.price,
            exit_price=operation.execution_price,
        )
