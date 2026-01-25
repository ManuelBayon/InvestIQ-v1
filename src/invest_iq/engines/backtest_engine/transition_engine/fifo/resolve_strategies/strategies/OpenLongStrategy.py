
from typing import ClassVar

from invest_iq.engines.backtest_engine.common.enums import GuardName
from invest_iq.engines.backtest_engine.common.types import AtomicAction
from invest_iq.engines.backtest_engine.common.enums import FIFOSide, FIFOOperationType, AtomicActionType
from invest_iq.engines.backtest_engine.common.types import FIFOPosition, FIFOOperation
from invest_iq.engines.backtest_engine.transition_engine.fifo.guards_strategies.expectations import ActionPriceExpectation, \
    ActionQuantityExpectation, ActionTypeExpectation, ActionTimestampExpectation
from invest_iq.engines.backtest_engine.transition_engine.fifo.guards_strategies.interface import ResolveContext
from invest_iq.engines.backtest_engine.transition_engine.fifo.resolve_strategies.interface import FIFOResolveStrategy
from invest_iq.engines.backtest_engine.transition_engine.fifo.resolve_strategies.registry import register_fifo_resolve_strategy

@register_fifo_resolve_strategy(AtomicActionType.OPEN_LONG)
class OpenLongStrategy(FIFOResolveStrategy):
    """
        Strategy for opening long positions in fifo.

        Responsibilities:
          - Create a new FIFOOperation of type OPEN with side LONG.
          - Use the action's quantity and timestamp, and the provided execution price.
          - Append the new position to the LONG side of the fifo queue.

        Invariants enforced:
          - Action type must be OPEN_LONG.
          - Quantity must be strictly positive.
          - Execution price must be > 0 and not NaN.

        This strategy is stateless and idempotent: repeated calls with the same
        inputs produce identical FIFOOperations.
    """

    STRATEGY_NAME: ClassVar[str] = "OpenLong"
    EXPECTED_TYPE: ClassVar[AtomicActionType] = AtomicActionType.OPEN_LONG

    REQUIRED_GUARDS = [
        GuardName.ACTION_PRICE,
        GuardName.ACTION_QUANTITY,
        GuardName.ACTION_TYPE,
        GuardName.ACTION_TIMESTAMP
    ]

    def resolve(
        self,
        action: AtomicAction,
        fifo_queues: dict[FIFOSide, list[FIFOPosition]],
        execution_price: float
    ) -> list[FIFOOperation]:

        context = ResolveContext(
            action=action,
            fifo_queues=fifo_queues,
            execution_price=execution_price
        )
        expectation_builders = {
            "ActionPriceGuard": lambda: ActionPriceExpectation(must_be_positive=True),
            "ActionQuantityGuard": lambda: ActionQuantityExpectation(min_qty=0.0),
            "ActionTypeGuard": lambda: ActionTypeExpectation(action_type=self.EXPECTED_TYPE),
            "ActionTimestampGuard": lambda : ActionTimestampExpectation()
        }

        self.apply_guards(context, self._safe_guard_factory, expectation_builders)

        # Process
        op = FIFOOperation(
            id=FIFOOperation.next_id(),
            timestamp=action.timestamp,
            type=FIFOOperationType.OPEN,
            side=FIFOSide.LONG,
            execution_price=execution_price,
            quantity=action.quantity
        )
        return [op]