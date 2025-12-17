from datetime import datetime
from typing import ClassVar

from engine.backtest_engine.common.types import AtomicAction
from engine.backtest_engine.common.enums import AtomicActionType, TransitionType
from engine.backtest_engine.transition_engine.transition_strategies.registry import register_transition_strategy
from engine.backtest_engine.transition_engine.transition_strategies.interface import TransitionStrategy

@register_transition_strategy(TransitionType.REDUCE_LONG)
class ReduceLongStrategy(TransitionStrategy):
    """
       Reduce the size of an existing long position without fully closing it.

       Expected:
           - current_position must be strictly greater than target_position
           - target_position must be strictly greater than 0
           - quantity closed = current_position - target_position

       Example:
           strategy = ReduceLongStrategy()
           strategy.resolve(current_position=5, target_position=2, timestamp=datetime(2025,1,1))
           [AtomicAction(type=CLOSE_LONG, quantity=3, timestamp=2025-01-01)]

       Invalid cases (raise ValueError):
           - current_position <= target_position (no reduction possible)
           - target_position <= 0 (reduction must leave a strictly positive position)
    """
    STRATEGY_NAME: ClassVar[str] = "ReduceLong"
    def resolve(
            self,
            current_position: float,
            target_position: float,
            timestamp: datetime
    ) -> list[AtomicAction]:
        delta : float = current_position - target_position
        if current_position <= target_position:
            raise ValueError(
                f"[{self.STRATEGY_NAME}] invalid: target={target_position}, current={current_position},"
                "current position < target position, expected current_position > target_position"
            )
        if target_position <= 0:
            raise ValueError(
                f"[{self.STRATEGY_NAME}] invalid: target={target_position}, current={current_position}, target_position <= 0, expected > 0"
            )
        actions = [
            AtomicAction(
                type=AtomicActionType.CLOSE_LONG,
                quantity=delta,
                timestamp=timestamp
            )
        ]
        #self.log_transition("[ReduceLongStrategy]", current_position, target_position, timestamp, actions)
        return actions