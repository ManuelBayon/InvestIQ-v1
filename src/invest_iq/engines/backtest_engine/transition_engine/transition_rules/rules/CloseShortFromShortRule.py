from typing import ClassVar

from invest_iq.engines.backtest_engine.common.enums import CurrentState, Event, TransitionType
from invest_iq.engines.backtest_engine.transition_engine.transition_rules.registry import register_transition_rule
from invest_iq.engines.backtest_engine.transition_engine.transition_rules.interface import TransitionRule


@register_transition_rule(CurrentState.SHORT, Event.GO_FLAT)
class CloseShortFromShortRule(TransitionRule):
    RULE_NAME: ClassVar[str] = "CloseShortFromShort"
    """
       Close an existing short position, returning to flat.

       Expected:
           - state must be SHORT
           - event must be GO_FLAT
           - current_position < 0
           - target_position == 0

       Example:
           rule = CloseShortFromShortRule()
           if rule.match(CurrentState.SHORT, Event.GO_FLAT):
               transition_type = rule.classify(
                   current_position=-5,
                   target_position=0
               )
               # transition_type = TransitionType.CLOSE_SHORT

       Invalid cases (raise ValueError):
           - target_position != 0 (must be zero to close short)
    """

    def match(self, state: CurrentState, event: Event) -> bool:
        return state == CurrentState.SHORT and event == Event.GO_FLAT

    def classify(self, current_position: float, target_position: float) -> TransitionType:
        if target_position != 0:
            self._logger.error(
                f"[{self.RULE_NAME}] invalid target_position=%s (must be 0)",
                target_position
            )
            raise ValueError(f"[{self.RULE_NAME}] target_position must be 0 to close short")
        return TransitionType.CLOSE_SHORT