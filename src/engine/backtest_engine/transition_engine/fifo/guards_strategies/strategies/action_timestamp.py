from engine.backtest_engine.common.enums import GuardName
from engine.backtest_engine.transition_engine.fifo.guards_strategies.expectations import ActionTimestampExpectation
from engine.backtest_engine.transition_engine.fifo.guards_strategies.interface import SafeGuard
from engine.backtest_engine.transition_engine.fifo.guards_strategies.interface import ResolveContext
from engine.backtest_engine.transition_engine.fifo.guards_strategies.registry import register_safe_guard

@register_safe_guard(GuardName.ACTION_TIMESTAMP)
class ActionTimestampGuard(SafeGuard[ActionTimestampExpectation]):

    STRATEGY_NAME = "ActionTimestampGuard"

    def check(self, context: ResolveContext, expected: ActionTimestampExpectation) -> None:
        # nothing to validate: typing already guarantees a datetime
        return