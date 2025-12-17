from typing import ClassVar

from engine.backtest_engine.common.enums import CurrentState, Event, TransitionType
from engine.backtest_engine.transition_engine.transition_rules.registry import register_transition_rule
from engine.backtest_engine.transition_engine.transition_rules.interface import TransitionRule


@register_transition_rule(CurrentState.LONG, Event.GO_LONG)
class AdjustLongFromLongRule(TransitionRule):

    RULE_NAME: ClassVar[str] = "AdjustLongFromLong"

    """
        Adjust an existing long position when already in a long state.

        Expected:
            - state must be LONG
            - event must be GO_LONG
            - current_position > 0
            - target_position > 0
            - transition depends on target vs current:
                - INCREASE_LONG if target_position > current_position
                - REDUCE_LONG if target_position < current_position

        Example:
            rule = AdjustLongFromLongRule()
            if rule.match(CurrentState.LONG, Event.GO_LONG):
                transition_type = rule.classify(
                    current_position=5,
                    target_position=8
                )
                # transition_type = TransitionType.INCREASE_LONG

        Invalid cases (raise ValueError):
            - target_position == current_position (no adjustment performed)
    """
    def match(self, state: CurrentState, event: Event) -> bool:
        return state == CurrentState.LONG and event == Event.GO_LONG

    def classify(self, current_position: float, target_position: float) -> TransitionType:
        if target_position > current_position:
            return TransitionType.INCREASE_LONG
        elif target_position < current_position:
            return TransitionType.REDUCE_LONG
        else:
            return TransitionType.NO_OP