from engine.backtest_engine.common.types import FIFOPosition
from engine.backtest_engine.common.enums import GuardName
from engine.backtest_engine.transition_engine.fifo.guards_strategies.expectations import FIFOCapacityExpectation
from engine.backtest_engine.transition_engine.fifo.guards_strategies.interface import SafeGuard
from engine.backtest_engine.transition_engine.fifo.guards_strategies.interface import ResolveContext
from engine.backtest_engine.transition_engine.fifo.guards_strategies.registry import register_safe_guard

@register_safe_guard(GuardName.FIFO_CAPACITY)
class FIFOCapacityGuard(SafeGuard[FIFOCapacityExpectation]):

    STRATEGY_NAME = "FIFOCapacityGuard"

    def check(self, context: ResolveContext, expected: FIFOCapacityExpectation) -> None:
        fifo_positions: list[FIFOPosition] = context.fifo_queues[expected.side]
        active_qty = sum(p.quantity for p in fifo_positions if p.is_active)

        if active_qty < expected.required_qty:
            self._logger.error(
                "[%s] Not enough fifo capacity: requested=%s, available=%s",
                self.STRATEGY_NAME, expected.required_qty, active_qty
            )
            raise ValueError(
                f"[{self.STRATEGY_NAME}] Not enough active quantity in fifo "
                f"(requested={expected.required_qty}, available={active_qty})"
            )