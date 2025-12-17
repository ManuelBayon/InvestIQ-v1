from typing import ClassVar

from engine.backtest_engine.common.enums import CurrentState, Event, TransitionType
from engine.backtest_engine.transition_engine.transition_rules.registry import register_transition_rule
from engine.backtest_engine.transition_engine.transition_rules.interface import TransitionRule


@register_transition_rule(CurrentState.FLAT, Event.GO_FLAT)
class NoOperationRule(TransitionRule):

    RULE_NAME : ClassVar[str] = "NoOperation"

    """
        Handle cases where the current_position == target_position.
        This represents a 'no operation' transition.

        Expected:
            - Any state (FLAT, LONG, SHORT)
            - Any event (GO_LONG, GO_SHORT, GO_FLAT)
            - current_position == target_position

        Example:
            rule = NoOpRule()
            if rule.match(CurrentState.LONG, Event.GO_LONG):
                transition_type = rule.classify(
                    current_position=5,
                    target_position=5
                )
                # transition_type = TransitionType.NO_OP

        Invalid cases (raise ValueError):
            - current_position != target_position
    """

    def match(
            self,
            state : CurrentState,
            event : Event
    ) -> bool:
        return state == CurrentState.FLAT and event == Event.GO_FLAT

    def classify(self, current_position: float, target_position: float) -> TransitionType:
        if current_position == target_position:
            return TransitionType.NO_OP
        self._logger.error(
            "[NoOpRule] invalid case: current=%s target=%s (must be equal)",
            current_position, target_position
        )
        raise ValueError("NoOpRule requires current_position == target_position")