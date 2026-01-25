from typing import Protocol

from invest_iq.engines.backtest_engine.common.enums import CurrentState, Event, TransitionType

class TransitionRuleProtocol(Protocol):

    def match(
            self,
            current_state : CurrentState,
            event : Event
    ) -> bool:
        ...

    def classify(
            self,
            current_position : float,
            target_position: float
    ) -> TransitionType:
        ...