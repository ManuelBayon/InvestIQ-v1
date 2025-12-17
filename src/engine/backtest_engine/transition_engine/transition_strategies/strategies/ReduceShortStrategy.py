from datetime import datetime
from typing import ClassVar

from engine.backtest_engine.common.types import AtomicAction
from engine.backtest_engine.common.enums import AtomicActionType, TransitionType
from engine.backtest_engine.transition_engine.transition_strategies.registry import register_transition_strategy
from engine.backtest_engine.transition_engine.transition_strategies.interface import TransitionStrategy

@register_transition_strategy(TransitionType.REDUCE_SHORT)
class ReduceShortStrategy(TransitionStrategy):
    """
       Reduce the size of an existing short position without fully closing it.

       Expected:
           - current_position must be strictly less than 0
           - target_position must be strictly less than 0
           - target_position must be strictly greater than current_position
             (i.e. closer to zero, less negative)
           - quantity closed = abs(current_position - target_position)

       Example:
           strategy = ReduceShortStrategy()
           strategy.resolve(current_position=-5, target_position=-2, timestamp=datetime(2025,1,1))
           [AtomicAction(type=CLOSE_SHORT, quantity=3, timestamp=2025-01-01)]

       Invalid cases (raise ValueError):
           - current_position >= 0 (no short to reduce)
           - target_position >= 0 (reduction must leave a short position)
           - target_position <= current_position (not a reduction)
    """
    STRATEGY_NAME: ClassVar[str] = "ReduceShort"
    def resolve(
            self,
            current_position: float,
            target_position: float,
            timestamp: datetime
    ) -> list[AtomicAction]:
        delta: float = abs(current_position - target_position)
        if current_position >= 0:
            raise ValueError(
                f"[{self.STRATEGY_NAME}] invalid: target={target_position}, current={current_position}, current_position >= 0, expected < 0"
            )
        if target_position >= 0:
            raise ValueError(
                f"[{self.STRATEGY_NAME}] invalid: target={target_position}, current={current_position}, target_position >= 0, expected < 0"
            )
        if target_position <= current_position:
            raise ValueError(
                f"[{self.STRATEGY_NAME}] invalid: target={target_position}, current={current_position}, target_position <= current_position, expected > current_position"
            )
        actions = [
            AtomicAction(
                type=AtomicActionType.CLOSE_SHORT,
                quantity=delta,
                timestamp=timestamp
            )
        ]
        #self.log_transition("[ReduceShortStrategy]", current_position, target_position, timestamp, actions)
        return actions