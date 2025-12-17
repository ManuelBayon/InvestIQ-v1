from abc import ABC, abstractmethod

from engine.backtest_engine.common.enums import CurrentState, Event, TransitionType
from engine.backtest_engine.transition_engine.transition_rules.base import TransitionRuleBase
from engine.backtest_engine.transition_engine.transition_rules.protocol import TransitionRuleProtocol

class TransitionRule(TransitionRuleProtocol, TransitionRuleBase, ABC):

    def __init_subclass__(cls, **kwargs: object) -> None:
        super().__init_subclass__(**kwargs)
        if not cls.RULE_NAME :
            raise TypeError(
                f"{cls.__name__} must define a valid STRATEGY_NAME (got {cls.RULE_NAME!r})"
            )

    @abstractmethod
    def match(
            self,
            current_state : CurrentState,
            event : Event
    ) -> bool:
        ...

    @abstractmethod
    def classify(
            self,
            current_position : float,
            target_position: float
    ) -> TransitionType:
        ...