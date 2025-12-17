from engine.backtest_engine.common.enums import GuardName
from engine.backtest_engine.transition_engine.fifo.guards_strategies.expectations import ActionQuantityExpectation
from engine.backtest_engine.transition_engine.fifo.guards_strategies.interface import SafeGuard
from engine.backtest_engine.transition_engine.fifo.guards_strategies.interface import ResolveContext
from engine.backtest_engine.transition_engine.fifo.guards_strategies.registry import register_safe_guard

@register_safe_guard(GuardName.ACTION_QUANTITY)
class ActionQuantityGuard(SafeGuard[ActionQuantityExpectation]):

    STRATEGY_NAME = "ActionQuantityGuard"

    def check(self, context: ResolveContext, expected: ActionQuantityExpectation) -> None:
        if context.action.quantity <= expected.min_qty:
            self._logger.error(
                "[%s] Invalid quantity: %s",
                self.STRATEGY_NAME, context.action.quantity
            )
            raise ValueError(
                f"[{self.STRATEGY_NAME}] Invalid quantity: {context.action.quantity}"
            )