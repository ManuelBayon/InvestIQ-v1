
from typing import ClassVar

from engine.backtest_engine.common.enums import GuardName
from engine.backtest_engine.common.types import AtomicAction
from engine.backtest_engine.common.enums import FIFOSide, FIFOOperationType, AtomicActionType
from engine.backtest_engine.common.types import FIFOPosition, FIFOOperation
from engine.backtest_engine.transition_engine.fifo.guards_strategies.expectations import ActionPriceExpectation, \
    ActionQuantityExpectation, ActionTypeExpectation, ActionTimestampExpectation, FIFOCapacityExpectation
from engine.backtest_engine.transition_engine.fifo.guards_strategies.interface import ResolveContext
from engine.backtest_engine.transition_engine.fifo.resolve_strategies.interface import FIFOResolveStrategy
from engine.backtest_engine.transition_engine.fifo.resolve_strategies.registry import register_fifo_resolve_strategy

@register_fifo_resolve_strategy(AtomicActionType.CLOSE_SHORT)
class CloseShortStrategy(FIFOResolveStrategy):

    """
        Strategy for closing short positions in fifo.

        Responsibilities:
          - Match the action's quantity against existing active SHORT positions.
          - Generate one or more FIFOOperations of type CLOSE with side SHORT.
          - Link each close operation to its originating fifo position.

        Invariants enforced:
          - Action type must be CLOSE_SHORT.
          - Quantity must be strictly positive.
          - Execution price must be > 0 and not NaN.
          - Active fifo capacity must be sufficient to cover the requested quantity.

        Raises ValueError if the requested quantity exceeds available fifo capacity.
    """

    STRATEGY_NAME: ClassVar[str] = "CloseShort"
    EXPECTED_TYPE: ClassVar[AtomicActionType] = AtomicActionType.CLOSE_SHORT
    REQUIRED_GUARDS = [
        GuardName.ACTION_PRICE,
        GuardName.ACTION_QUANTITY,
        GuardName.ACTION_TYPE,
        GuardName.ACTION_TIMESTAMP,
        GuardName.FIFO_CAPACITY
    ]

    def resolve(
            self,
            action: AtomicAction,
            fifo_queues: dict[FIFOSide, list[FIFOPosition]],
            execution_price: float
    ) -> list[FIFOOperation]:

        # SafeGuards
        context = ResolveContext(
            action=action,
            fifo_queues=fifo_queues,
            execution_price=execution_price
        )
        expectation_builders = {
            "ActionPriceGuard": lambda: ActionPriceExpectation(must_be_positive=True),
            "ActionQuantityGuard": lambda: ActionQuantityExpectation(min_qty=0.0),
            "ActionTypeGuard": lambda: ActionTypeExpectation(action_type=self.EXPECTED_TYPE),
            "ActionTimestampGuard": lambda: ActionTimestampExpectation(),
            "FIFOCapacityGuard": lambda: FIFOCapacityExpectation(
                side=FIFOSide.SHORT,
                required_qty=action.quantity
            )
        }
        self.apply_guards(context, self._safe_guard_factory, expectation_builders)

        # Process
        fifo_operation_list: list[FIFOOperation] = []
        remaining_qty = action.quantity
        fifo = fifo_queues[FIFOSide.SHORT]

        for position in fifo:
            if not position.is_active:
                continue
            available_qty = position.quantity
            close_qty = min(remaining_qty, available_qty)
            op = FIFOOperation(
                id=FIFOOperation.next_id(),
                timestamp=action.timestamp,
                type=FIFOOperationType.CLOSE,
                side=FIFOSide.SHORT,
                quantity=close_qty,
                execution_price=execution_price,
                linked_position_id=position.id
            )
            fifo_operation_list.append(op)
            remaining_qty -= close_qty
            if remaining_qty <= 0:
                break
        if remaining_qty > 0:
            raise ValueError(
                f"[CloseShortStrategy] Quantity to close ({action.quantity}) exceeds available fifo positions ({action.quantity - remaining_qty})."
            )
        return fifo_operation_list