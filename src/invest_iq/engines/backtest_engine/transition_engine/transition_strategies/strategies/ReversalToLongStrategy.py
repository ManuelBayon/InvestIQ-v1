from datetime import datetime
from typing import ClassVar

from invest_iq.engines.backtest_engine.common.types import AtomicAction
from invest_iq.engines.backtest_engine.common.enums import AtomicActionType, TransitionType
from invest_iq.engines.backtest_engine.transition_engine.transition_strategies.registry import register_transition_strategy
from invest_iq.engines.backtest_engine.transition_engine.transition_strategies.interface import TransitionStrategy

@register_transition_strategy(TransitionType.REVERSAL_TO_LONG)
class ReversalToLongStrategy(TransitionStrategy):
    """
       Reverse an existing short position into a new long position.

       Expected:
           - current_position must be strictly < 0 (you must hold a short)
           - target_position must be strictly > 0 (the new long position)
           - Actions:
                1. CLOSE_SHORT with quantity = abs(current_position)
                2. OPEN_LONG with quantity = target_position

       Example:
           strategy = ReversalToLongStrategy()
           strategy.resolve(current_position=-3, target_position=4, timestamp=datetime(2025,1,1))
           [
               AtomicAction(type=CLOSE_SHORT, quantity=3, timestamp=2025-01-01),
               AtomicAction(type=OPEN_LONG, quantity=4, timestamp=2025-01-01)
           ]

       Invalid cases (raise ValueError):
           - current_position >= 0 (no short to reverse)
           - target_position <= 0 (must reverse into a long)
    """
    STRATEGY_NAME: ClassVar[str] = "ReversalToLong"
    def resolve(
            self,
            current_position: float,
            target_position: float,
            timestamp: datetime
    ) -> list[AtomicAction]:
        if current_position >= 0:
            raise ValueError(
                f"[{self.STRATEGY_NAME}] invalid: current={current_position}, expected < 0"
            )
        if target_position <= 0:
            raise ValueError(
                f"[{self.STRATEGY_NAME}] invalid: target={target_position}, expected > 0"
            )
        actions = [
            AtomicAction(
                type=AtomicActionType.CLOSE_SHORT,
                quantity=abs(current_position),
                timestamp=timestamp
            ),
            AtomicAction(
                type=AtomicActionType.OPEN_LONG,
                quantity=target_position,
                timestamp=timestamp
            )
        ]
        #self.log_transition("[ReversalToLongStrategy]", current_position, target_position, timestamp, actions)
        return actions