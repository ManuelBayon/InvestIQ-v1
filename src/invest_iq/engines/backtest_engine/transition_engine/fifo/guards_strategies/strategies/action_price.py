import math

from invest_iq.engines.backtest_engine.common.enums import GuardName
from invest_iq.engines.backtest_engine.transition_engine.fifo.guards_strategies.expectations import ActionPriceExpectation
from invest_iq.engines.backtest_engine.transition_engine.fifo.guards_strategies.interface import SafeGuard
from invest_iq.engines.backtest_engine.transition_engine.fifo.guards_strategies.interface import ResolveContext
from invest_iq.engines.backtest_engine.transition_engine.fifo.guards_strategies.registry import register_safe_guard

@register_safe_guard(GuardName.ACTION_PRICE)
class ActionPriceGuard(SafeGuard[ActionPriceExpectation]):
    STRATEGY_NAME = "ActionPriceGuard"

    def check(self, context: ResolveContext, expected: ActionPriceExpectation) -> None:
        if expected.must_be_positive and (context.execution_price <= 0 or math.isnan(context.execution_price)):
            self._logger.error(
                "[%s] Invalid execution price: %s",
                self.STRATEGY_NAME, context.execution_price
            )
            raise ValueError(
                f"[{self.STRATEGY_NAME}] Invalid execution price: {context.execution_price}"
            )