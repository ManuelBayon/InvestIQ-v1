from typing import ClassVar

from backtest_engine.common.enums import CurrentState, Event, TransitionType
from backtest_engine.transition_engine.transition_rules.registry import register_transition_rule
from backtest_engine.transition_engine.transition_rules.interface import TransitionRule


@register_transition_rule(CurrentState.SHORT, Event.GO_LONG)
class ReversalToLongFromShortRule(TransitionRule):
    RULE_NAME: ClassVar[str] = "ReversalToLongFromShort"
    """
        Reverse an existing short position into a long position.

        Expected:
            - state must be SHORT
            - event must be GO_LONG
            - current_position < 0
            - target_position > 0

        Example:
            rule = ReversalToLongFromShortRule()
            if rule.match(CurrentState.SHORT, Event.GO_LONG):
                transition_type = rule.classify(
                    current_position=-4,
                    target_position=7
                )
                # transition_type = TransitionType.REVERSAL_TO_LONG

        Invalid cases (raise ValueError):
            - target_position <= 0 (must cross into positive territory)
    """

    def match(self, state: CurrentState, event: Event) -> bool:
        return state == CurrentState.SHORT and event == Event.GO_LONG

    def classify(self, current_position: float, target_position: float) -> TransitionType:
        if target_position <= 0:
            self._logger.error(
                f"[{self.RULE_NAME}] invalid target_position=%s (must be >0)",
                target_position
            )
            raise ValueError(f"[{self.RULE_NAME}] target_position must be > 0 for reversal to long")
        return TransitionType.REVERSAL_TO_LONG