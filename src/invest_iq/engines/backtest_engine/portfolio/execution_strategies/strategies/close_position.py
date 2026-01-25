from invest_iq.engines.backtest_engine.common.enums import FIFOSide, FIFOOperationType
from invest_iq.engines.backtest_engine.common.types import ExecutionLogEntry

from invest_iq.engines.backtest_engine.common.types import FIFOOperation
from invest_iq.engines.backtest_engine.portfolio.protocol import PortfolioProtocol
from invest_iq.engines.backtest_engine.portfolio.execution_strategies.interface import PortfolioExecutionStrategy
from invest_iq.engines.backtest_engine.portfolio.execution_strategies.registry import register_fifo_execution


@register_fifo_execution(FIFOOperationType.CLOSE)
class ClosePositionExecution(PortfolioExecutionStrategy):

    STRATEGY_NAME = "CLOSE_POSITION_EXECUTION"

    def apply(
            self,
            portfolio: PortfolioProtocol,
            operation: FIFOOperation
    ) -> ExecutionLogEntry:

        fifo = portfolio.fifo_queues[operation.side]
        direction = 1 if operation.side == FIFOSide.LONG else -1
        matched_position = next(
            (pos for pos in fifo if pos.id == operation.linked_position_id),
            None
        )
        if matched_position is None:
            raise ValueError(
                f"[{self.STRATEGY_NAME}] No FIFOPosition with id={operation.linked_position_id}"
            )
        if not matched_position.is_active:
            raise ValueError(
                f"[{self.STRATEGY_NAME}] Position {matched_position.id} already closed"
            )
        if operation.quantity == matched_position.quantity:
            matched_position.is_active = False
        elif operation.quantity < matched_position.quantity:
            matched_position.quantity -= operation.quantity
        else:
            raise ValueError(
                f"[{self.STRATEGY_NAME}] Close quantity {operation.quantity} "
                f"> available {matched_position.quantity}"
            )
        pnl = (operation.execution_price - matched_position.price) * operation.quantity * direction
        pos_before = portfolio.current_position
        pos_after = portfolio.current_position - operation.quantity * direction
        portfolio.current_position = pos_after
        portfolio.realized_pnl += pnl
        entry = ExecutionLogEntry(
            timestamp=operation.timestamp,
            operation_type=operation.type,
            side=operation.side,
            quantity=operation.quantity,
            entry_price=matched_position.price,
            pos_before=pos_before,
            pos_after=pos_after,
            exit_price=operation.execution_price,
            realized_pnl=pnl,
            parent_id=matched_position.id,
        )
        return entry