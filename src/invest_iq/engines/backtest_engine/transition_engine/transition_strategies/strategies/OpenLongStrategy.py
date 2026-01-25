from datetime import datetime
from typing import ClassVar

from invest_iq.engines.backtest_engine.common.enums import AtomicActionType, TransitionType
from invest_iq.engines.backtest_engine.common.types import AtomicAction
from invest_iq.engines.backtest_engine.transition_engine.transition_strategies.interface import TransitionStrategy
from invest_iq.engines.backtest_engine.transition_engine.transition_strategies.registry import register_transition_strategy

@register_transition_strategy(TransitionType.OPEN_LONG)
class OpenLongStrategy(TransitionStrategy):
    """
       Open a new long position when no position is currently held.

       Expected:
           - current_position must be exactly 0
           - target_position must be strictly greater than 0

       Example:
           strategy = OpenLongStrategy()
           strategy.resolve(current_position=0, target_position=5, timestamp=datetime(2025,1,1))
           [AtomicAction(type=OPEN_LONG, quantity=5, timestamp=2025-01-01)]

       Invalid cases (raise ValueError):
           - current_position != 0 (cannot open if a position already exists)
           - target_position <= 0 (cannot open a non-positive position)
    """

    STRATEGY_NAME: ClassVar[str] = "OpenLong"

    def resolve(
            self,
            current_position: float,
            target_position: float,
            timestamp: datetime
    ) -> list[AtomicAction]:

        if current_position != 0:
            raise ValueError(
                f"[{self.STRATEGY_NAME}] invalid: target={target_position}, current={current_position}, current_position expected 0"
            )
        if target_position <= 0:
            raise ValueError(
                f"[{self.STRATEGY_NAME}] invalid: target={target_position}, current={current_position}, target_position <= 0, expected > 0"
            )
        actions = [
            AtomicAction(
                type= AtomicActionType.OPEN_LONG,
                quantity= target_position,
                timestamp=timestamp
            )
        ]
        return actions