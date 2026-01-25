from invest_iq.engines.backtest_engine.common.enums import GuardName
from invest_iq.engines.backtest_engine.transition_engine.fifo.guards_strategies.expectations import ActionTypeExpectation
from invest_iq.engines.backtest_engine.transition_engine.fifo.guards_strategies.interface import SafeGuard
from invest_iq.engines.backtest_engine.transition_engine.fifo.guards_strategies.interface import ResolveContext
from invest_iq.engines.backtest_engine.transition_engine.fifo.guards_strategies.registry import register_safe_guard

@register_safe_guard(GuardName.ACTION_TYPE)
class ActionTypeGuard(SafeGuard[ActionTypeExpectation]):

    STRATEGY_NAME = "ActionTypeGuard"

    def check(
        self,
        context: ResolveContext,
        expected : ActionTypeExpectation
    ) -> None:
        if context.action.type != expected.action_type:
            self._logger.error(
                "[%s] Invalid action type: expected=%s, got=%s",
                self.STRATEGY_NAME, expected.action_type, context.action.type
            )
            raise ValueError(
                f"[{self.STRATEGY_NAME}] Invalid action type: "
                f"expected {expected.action_type}, got {context.action.type}"
            )