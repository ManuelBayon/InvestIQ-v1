from datetime import datetime
from typing import Protocol

from backtest_engine.common.types import AtomicAction

class TransitionStrategyProtocol(Protocol):

    def resolve(
            self,
            current_position: float,
            target_position: float,
            timestamp: datetime
    ) -> list[AtomicAction]:
        ...