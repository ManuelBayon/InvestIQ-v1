from datetime import datetime
from typing import ClassVar

from invest_iq.engines.backtest_engine.common.types import AtomicAction
from invest_iq.engines.backtest_engine.common.enums import AtomicActionType, TransitionType
from invest_iq.engines.backtest_engine.transition_engine.transition_strategies.interface import TransitionStrategy
from invest_iq.engines.backtest_engine.transition_engine.transition_strategies.registry import register_transition_strategy

@register_transition_strategy(TransitionType.INCREASE_LONG)
class IncreaseLongStrategy(TransitionStrategy):
    """
       Increase the size of an existing long position.

       Expected:
           - current_position must be strictly greater than 0
           - target_position must be strictly greater than current_position
           - quantity opened = target_position - current_position

       Example:
           strategy = IncreaseLongStrategy()
           strategy.resolve(current_position=2, target_position=5, timestamp=datetime(2025,1,1))
           [AtomicAction(type=OPEN_LONG, quantity=3, timestamp=2025-01-01)]

       Invalid cases (raise ValueError):
           - current_position <= 0 (cannot increase if no position exists)
           - target_position <= current_position (no increase to apply)
    """
    STRATEGY_NAME: ClassVar[str] = "IncreaseLong"
    def resolve(
            self,
            current_position: float,
            target_position: float,
            timestamp: datetime
    ) -> list[AtomicAction]:
        delta : float = target_position - current_position
        if current_position <= 0:
            raise ValueError(
                f"[{self.STRATEGY_NAME}] invalid: target={target_position}, current={current_position}, current_position<=0, expected > 0"
            )
        if target_position <= current_position:
            raise ValueError(
                f"[{self.STRATEGY_NAME}] invalid: target={target_position}, current={current_position}, target position <= current position"
            )
        actions = [
            AtomicAction(
                type=AtomicActionType.OPEN_LONG,
                quantity=delta,
                timestamp=timestamp
            )
        ]
        #self.log_transition("[IncreaseLongStrategy]", current_position, target_position, timestamp, actions)
        return actions