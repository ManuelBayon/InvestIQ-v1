from typing import ClassVar

from engine.backtest_engine.common.enums import CurrentState, Event, TransitionType
from engine.backtest_engine.transition_engine.transition_rules.registry import register_transition_rule
from engine.backtest_engine.transition_engine.transition_rules.interface import TransitionRule


@register_transition_rule(CurrentState.LONG, Event.GO_FLAT)
class CloseLongFromLongRule(TransitionRule):
    RULE_NAME: ClassVar[str] = "CloseLongFromLong"
    """
       Close an existing long position, returning to flat.

       Expected:
           - state must be LONG
           - event must be GO_FLAT
           - current_position > 0
           - target_position == 0

       Example:
           rule = CloseLongFromLongRule()
           if rule.match(CurrentState.LONG, Event.GO_FLAT):
               transition_type = rule.classify(
                   current_position=5,
                   target_position=0
               )
               # transition_type = TransitionType.CLOSE_LONG

       Invalid cases (raise ValueError):
           - target_position != 0 (must be zero to close long)
    """
    def match(self, state: CurrentState, event: Event) -> bool:
        return state == CurrentState.LONG and event == Event.GO_FLAT

    def classify(self, current_position: float, target_position: float) -> TransitionType:
        if target_position != 0:
            self._logger.error(
                f"[{self.RULE_NAME}] invalid target_position=%s (must be 0)",
                target_position
            )
            raise ValueError(f"[{self.RULE_NAME}] target_position must be 0 to close long")
        return TransitionType.CLOSE_LONG