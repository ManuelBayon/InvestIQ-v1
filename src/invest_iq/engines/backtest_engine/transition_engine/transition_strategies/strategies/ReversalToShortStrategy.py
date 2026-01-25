from datetime import datetime
from typing import ClassVar

from invest_iq.engines.backtest_engine.common.types import AtomicAction
from invest_iq.engines.backtest_engine.common.enums import AtomicActionType, TransitionType
from invest_iq.engines.backtest_engine.transition_engine.transition_strategies.registry import register_transition_strategy
from invest_iq.engines.backtest_engine.transition_engine.transition_strategies.interface import TransitionStrategy

@register_transition_strategy(TransitionType.REVERSAL_TO_SHORT)
class ReversalToShortStrategy(TransitionStrategy):
    """
       Reverse an existing long position into a new short position.
    
       Expected:
           - current_position must be strictly > 0 (you must hold a long)
           - target_position must be strictly < 0 (the new short position)
           - Actions:
                1. CLOSE_LONG with quantity = current_position
                2. OPEN_SHORT with quantity = abs(target_position)
    
       Example:
           strategy = ReversalToShortStrategy()
           strategy.resolve(current_position=3, target_position=-2, timestamp=datetime(2025,1,1))
           [
               AtomicAction(type=CLOSE_LONG, quantity=3, timestamp=2025-01-01),
               AtomicAction(type=OPEN_SHORT, quantity=2, timestamp=2025-01-01)
           ]
    
       Invalid cases (raise ValueError):
           - current_position <= 0 (no long to reverse)
           - target_position >= 0 (must reverse into a short)
    """
    STRATEGY_NAME: ClassVar[str] = "ReversalToShort"
    def resolve(
            self,
            current_position: float,
            target_position: float,
            timestamp: datetime
    ) -> list[AtomicAction]:
        if current_position <= 0:
            raise ValueError(
                f"[{self.STRATEGY_NAME}] invalid: current={current_position}, expected > 0"
            )
        if target_position >= 0:
            raise ValueError(
                f"[{self.STRATEGY_NAME}] invalid: target={target_position}, expected < 0"
            )
        actions = [
            AtomicAction(
                type=AtomicActionType.CLOSE_LONG,
                quantity=current_position,
                timestamp=timestamp
            ),
            AtomicAction(
                type=AtomicActionType.OPEN_SHORT,
                quantity=abs(target_position),
                timestamp=timestamp
            )
        ]
        return actions