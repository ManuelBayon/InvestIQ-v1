from backtest_engine.common.enums import FIFOSide, FIFOOperationType
from backtest_engine.common.types import ExecutionLogEntry
from backtest_engine.common.types import FIFOPosition, FIFOOperation
from backtest_engine.portfolio.protocol import PortfolioProtocol
from backtest_engine.portfolio.execution_strategies.interface import PortfolioExecutionStrategy
from backtest_engine.portfolio.execution_strategies.registry import register_fifo_execution


@register_fifo_execution(FIFOOperationType.OPEN)
class OpenPositionExecution(PortfolioExecutionStrategy):

    STRATEGY_NAME = "OPEN_POSITION_EXECUTION"

    def apply(
            self,
            portfolio : PortfolioProtocol,
            operation: FIFOOperation
    ) -> ExecutionLogEntry:

        position = FIFOPosition(
            id=operation.id,
            is_active=True,
            timestamp=operation.timestamp,
            type=operation.type,
            side=operation.side,
            quantity=operation.quantity,
            price=operation.execution_price
        )

        direction = 1 if operation.side == FIFOSide.LONG else -1
        pos_before = portfolio.current_position
        pos_after = portfolio.current_position + operation.quantity * direction

        portfolio.fifo_queues[operation.side].append(position)
        portfolio.current_position = pos_after

        entry = ExecutionLogEntry(
            timestamp=operation.timestamp,
            operation_type=operation.type,
            side=operation.side,
            quantity=operation.quantity,
            entry_price=operation.execution_price,
            pos_before=pos_before,
            pos_after=pos_after,
            exit_price=None,
            realized_pnl=None,
            parent_id=None,
        )

        return entry