from typing import ClassVar

from invest_iq.engines.backtest_engine.common.enums import CurrentState, Event, TransitionType
from invest_iq.engines.backtest_engine.transition_engine.transition_rules.registry import register_transition_rule
from invest_iq.engines.backtest_engine.transition_engine.transition_rules.interface import TransitionRule


@register_transition_rule(CurrentState.FLAT, Event.GO_LONG)
class OpenLongFromFlatRule(TransitionRule):
    """
       Open a new long position when starting from a flat state.

       Expected:
           - state must be FLAT
           - event must be GO_LONG
           - current_position must be exactly 0
           - target_position must be strictly greater than 0
           - quantity opened = target_position

       Example:
           rule = OpenLongFromFlatRule()
           if rule.match(CurrentState.FLAT, Event.GO_LONG):
               transition_type = rule.classify(
                   current_position=0,
                   target_position=5
               )
               # transition_type = TransitionType.OPEN_LONG

       Invalid cases (raise ValueError):
           - current_position != 0 (cannot open long if a position already exists)
           - target_position <= 0 (cannot open a non-positive position)
    """
    RULE_NAME: ClassVar[str] = "OpenLongFromFlat"

    def match(self, state: CurrentState, event: Event) -> bool:
        match = state == CurrentState.FLAT and event == Event.GO_LONG
        return match

    def classify(self, current_position: float, target_position: float) -> TransitionType:
        if current_position != 0:
            self._logger.error(
                f"[{self.RULE_NAME}] invalid current_position=%s (must be 0)",
                current_position
            )
            raise ValueError("current_position must be 0 to open long")
        if target_position <= 0:
            self._logger.error(
                f"[{self.RULE_NAME}] invalid target_position=%s (must be >0)",
                target_position
            )
            raise ValueError(f"{self.RULE_NAME} must be > 0 to open long")
        return TransitionType.OPEN_LONG