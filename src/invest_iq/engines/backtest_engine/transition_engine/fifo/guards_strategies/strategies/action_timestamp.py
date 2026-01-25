from invest_iq.engines.backtest_engine.common.enums import GuardName
from invest_iq.engines.backtest_engine.transition_engine.fifo.guards_strategies.expectations import ActionTimestampExpectation
from invest_iq.engines.backtest_engine.transition_engine.fifo.guards_strategies.interface import SafeGuard
from invest_iq.engines.backtest_engine.transition_engine.fifo.guards_strategies.interface import ResolveContext
from invest_iq.engines.backtest_engine.transition_engine.fifo.guards_strategies.registry import register_safe_guard

@register_safe_guard(GuardName.ACTION_TIMESTAMP)
class ActionTimestampGuard(SafeGuard[ActionTimestampExpectation]):

    STRATEGY_NAME = "ActionTimestampGuard"

    def check(self, context: ResolveContext, expected: ActionTimestampExpectation) -> None:
        # nothing to validate: typing already guarantees a datetime
        return