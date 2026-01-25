from datetime import datetime
from typing import ClassVar

from invest_iq.engines.backtest_engine.common.types import AtomicAction
from invest_iq.engines.backtest_engine.common.enums import AtomicActionType, TransitionType
from invest_iq.engines.backtest_engine.transition_engine.transition_strategies.interface import TransitionStrategy
from invest_iq.engines.backtest_engine.transition_engine.transition_strategies.registry import register_transition_strategy

@register_transition_strategy(TransitionType.CLOSE_SHORT)
class CloseShortStrategy(TransitionStrategy):
    """
       Fully close an existing short position.

       Expected:
           - current_position must be strictly less than 0
           - target_position must be exactly 0
           - quantity closed = abs(current_position)

       Example:
           strategy = CloseShortStrategy()
           strategy.resolve(current_position=-4, target_position=0, timestamp=datetime(2025,1,1))
           [AtomicAction(type=CLOSE_SHORT, quantity=4, timestamp=2025-01-01)]

       Invalid cases (raise ValueError):
           - current_position >= 0 (no short position to close)
           - target_position != 0 (closing requires target=0)
    """
    STRATEGY_NAME: ClassVar[str] = "CloseShort"
    def resolve(
            self,
            current_position: float,
            target_position: float,
            timestamp: datetime
    ) -> list[AtomicAction]:
        if current_position >= 0:
            raise ValueError(
                f"[{self.STRATEGY_NAME}] invalid: target={target_position}, current={current_position}, current_position >= 0, expected < 0"
            )
        if target_position != 0:
            raise ValueError(
                f"[{self.STRATEGY_NAME}] invalid: target={target_position}, current={current_position}, target position != 0, expected == 0"
            )
        actions = [
            AtomicAction(
                type=AtomicActionType.CLOSE_SHORT,
                quantity=abs(current_position),
                timestamp=timestamp
            )
        ]
        #self.log_transition("[CloseShortStrategy]", current_position, target_position, timestamp, actions)
        return actions