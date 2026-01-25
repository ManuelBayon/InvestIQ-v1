from typing import ClassVar

from invest_iq.engines.backtest_engine.common.enums import CurrentState, Event, TransitionType
from invest_iq.engines.backtest_engine.transition_engine.transition_rules.registry import register_transition_rule
from invest_iq.engines.backtest_engine.transition_engine.transition_rules.interface import TransitionRule


@register_transition_rule(CurrentState.LONG, Event.GO_SHORT)
class ReversalToShortFromLongRule(TransitionRule):
    RULE_NAME: ClassVar[str] = "ReversalToShortFromLong"
    """
        Reverse an existing long position into a short position.

        Expected:
            - state must be LONG
            - event must be GO_SHORT
            - current_position > 0
            - target_position < 0

        Example:
            rule = ReversalToShortFromLongRule()
            if rule.match(CurrentState.LONG, Event.GO_SHORT):
                transition_type = rule.classify(
                    current_position=5,
                    target_position=-4
                )
                # transition_type = TransitionType.REVERSAL_TO_SHORT

        Invalid cases (raise ValueError):
            - target_position >= 0 (must cross into negative territory)
    """

    def match(self, state: CurrentState, event: Event) -> bool:
        return state == CurrentState.LONG and event == Event.GO_SHORT

    def classify(self, current_position: float, target_position: float) -> TransitionType:
        if target_position >= 0:
            self._logger.error(
                f"[{self.RULE_NAME}] invalid target_position=%s (must be <0)",
                target_position
            )
            raise ValueError(f"[{self.RULE_NAME}] target_position must be < 0 for reversal to short")
        return TransitionType.REVERSAL_TO_SHORT