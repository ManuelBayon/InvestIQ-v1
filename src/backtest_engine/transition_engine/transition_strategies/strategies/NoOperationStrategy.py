from datetime import datetime
from typing import ClassVar

from backtest_engine.common.enums import TransitionType
from backtest_engine.common.types import AtomicAction
from backtest_engine.transition_engine.transition_strategies.registry import register_transition_strategy
from backtest_engine.transition_engine.transition_strategies.interface import TransitionStrategy

@register_transition_strategy(TransitionType.NO_OP)
class NoOpStrategy(TransitionStrategy):
    """
       Perform no operation when the current position already matches the target.

       Expected:
           - current_position must be exactly equal to target_position
           - no action should be generated

       Example:
           strategy = NoOpStrategy()
           strategy.resolve(current_position=3, target_position=3, timestamp=datetime(2025,1,1))
           []

       Invalid cases (raise ValueError):
           - current_position != target_position (inconsistency: nothing to change, so they must match)
    """
    STRATEGY_NAME: ClassVar[str] = "NoOperation"
    def resolve(
            self,
            current_position: float,
            target_position: float,
            timestamp: datetime
    ) -> list[AtomicAction]:
        if current_position != target_position:
            raise ValueError(
                f"[{self.STRATEGY_NAME}] invalid: current={current_position}, target={target_position},"
                f" expected current_position == target_position"
            )
        return []