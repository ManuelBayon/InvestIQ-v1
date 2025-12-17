from datetime import datetime
from typing import ClassVar

from engine.backtest_engine.common.types import AtomicAction
from engine.backtest_engine.common.enums import AtomicActionType, TransitionType
from engine.backtest_engine.transition_engine.transition_strategies.interface import TransitionStrategy
from engine.backtest_engine.transition_engine.transition_strategies.registry import register_transition_strategy

@register_transition_strategy(TransitionType.CLOSE_LONG)
class CloseLongStrategy(TransitionStrategy):
    """
       Fully close an existing long position.

       Expected:
           - current_position must be strictly greater than 0
           - target_position must be exactly 0
           - quantity closed = current_position

       Example:
           strategy = CloseLongStrategy()
           strategy.resolve(current_position=4, target_position=0, timestamp=datetime(2025,1,1))
           [AtomicAction(type=CLOSE_LONG, quantity=4, timestamp=2025-01-01)]

       Invalid cases (raise ValueError):
           - current_position <= 0 (nothing to close)
           - target_position != 0 (closing requires target=0)
    """
    STRATEGY_NAME : ClassVar[str] = "CloseLong"
    def resolve(
            self,
            current_position: float,
            target_position: float,
            timestamp: datetime
    ) -> list[AtomicAction]:
        if current_position <= 0:
            raise ValueError(
                f"[{self.STRATEGY_NAME}] invalid: target={target_position}, current={current_position}, current_position <= 0, expected > 0"
            )
        if target_position != 0:
            raise ValueError(
                f"[{self.STRATEGY_NAME}] invalid: target={target_position}, current={current_position}, target position != 0, expected == 0"
            )
        actions = [
            AtomicAction(
                type=AtomicActionType.CLOSE_LONG,
                quantity=current_position,
                timestamp=timestamp
            )
        ]
        return actions