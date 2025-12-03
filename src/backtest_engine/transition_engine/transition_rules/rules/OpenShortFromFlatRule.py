from typing import ClassVar

from backtest_engine.common.enums import CurrentState, Event, TransitionType
from backtest_engine.transition_engine.transition_rules.registry import register_transition_rule
from backtest_engine.transition_engine.transition_rules.interface import TransitionRule


@register_transition_rule(CurrentState.FLAT, Event.GO_SHORT)
class OpenShortFromFlatRule(TransitionRule):
    RULE_NAME: ClassVar[str] = "OpenShortFromShort"
    """
        Open a new short position when starting from a flat state.

        Expected:
            - state must be FLAT
            - event must be GO_SHORT
            - current_position must be exactly 0
            - target_position must be strictly less than 0
            - quantity opened = abs(target_position)
    
        Example:
            rule = OpenShortFromFlatRule()
            if rule.match(CurrentState.FLAT, Event.GO_SHORT):
                transition_type = rule.classify(
                    current_position=0,
                    target_position=-3
                )
                # transition_type = TransitionType.OPEN_SHORT
    
        Invalid cases (raise ValueError):
            - current_position != 0 (cannot open short if a position already exists)
            - target_position >= 0 (must be strictly negative to open short)
    """

    def match(self, state: CurrentState, event: Event) -> bool:
        return state == CurrentState.FLAT and event == Event.GO_SHORT

    def classify(self, current_position: float, target_position: float) -> TransitionType:
        if current_position != 0:
            self._logger.error(
                f"[{self.RULE_NAME}] invalid current_position=%s",
                current_position
            )
            raise ValueError(f"[{self.RULE_NAME}] current_position must be 0 to open short")
        if target_position >= 0:
            self._logger.error(
                f"[{self.RULE_NAME}] invalid target_position=%s",
                target_position
            )
            raise ValueError(f"[{self.RULE_NAME}] target_position must be < 0 to open short")
        return TransitionType.OPEN_SHORT