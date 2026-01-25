from abc import ABC, abstractmethod
from datetime import datetime

from invest_iq.engines.backtest_engine.common.types import AtomicAction
from invest_iq.engines.backtest_engine.transition_engine.transition_strategies.base import TransitionStrategyBase
from invest_iq.engines.backtest_engine.transition_engine.transition_strategies.protocol import TransitionStrategyProtocol

class TransitionStrategy(TransitionStrategyProtocol, TransitionStrategyBase, ABC):

    def __init_subclass__(
            cls,
            **kwargs: object
    ) -> None:
        super().__init_subclass__(**kwargs)
        if not isinstance(getattr(cls, "STRATEGY_NAME", None), str) or not cls.STRATEGY_NAME.strip():
            raise TypeError(f"{cls.__name__} must define a non-empty STRATEGY_NAME")

    @abstractmethod
    def resolve(
            self,
            current_position: float,
            target_position: float,
            timestamp: datetime
    ) -> list[AtomicAction]:
        ...