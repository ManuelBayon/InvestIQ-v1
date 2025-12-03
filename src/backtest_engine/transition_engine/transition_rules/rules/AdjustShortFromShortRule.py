from typing import ClassVar

from backtest_engine.common.enums  import CurrentState, Event, TransitionType
from backtest_engine.transition_engine.transition_rules.registry import register_transition_rule
from backtest_engine.transition_engine.transition_rules.interface import TransitionRule


@register_transition_rule(CurrentState.SHORT, Event.GO_SHORT)
class AdjustShortFromShortRule(TransitionRule):
    RULE_NAME: ClassVar[str] = "AdjustShortFromShort"
    """
        Adjust an existing short position when already in a short state.

        Expected:
            - state must be SHORT
            - event must be GO_SHORT
            - current_position < 0
            - target_position < 0
            - transition depends on target vs current:
                - INCREASE_SHORT if target_position < current_position
                - REDUCE_SHORT if target_position > current_position

        Example:
            rule = AdjustShortFromShortRule()
            if rule.match(CurrentState.SHORT, Event.GO_SHORT):
                transition_type = rule.classify(
                    current_position=-3,
                    target_position=-6
                )
                # transition_type = TransitionType.INCREASE_SHORT

        Invalid cases (raise ValueError):
            - target_position == current_position (no adjustment performed)
    """

    def match(self, state: CurrentState, event: Event) -> bool:
        return state == CurrentState.SHORT and event == Event.GO_SHORT

    def classify(self, current_position: float, target_position: float) -> TransitionType:
        if target_position < current_position:
            return TransitionType.INCREASE_SHORT
        if target_position > current_position:
            return TransitionType.REDUCE_SHORT
        else:
            return TransitionType.NO_OP
