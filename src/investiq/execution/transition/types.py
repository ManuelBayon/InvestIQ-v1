from dataclasses import dataclass
from datetime import datetime

from investiq.execution.transition.enums import AtomicActionType, FIFOOperationType, FIFOSide


@dataclass(frozen=True)
class AtomicAction:
    type : AtomicActionType
    quantity : float
    timestamp: datetime

@dataclass
class FIFOPosition:
    id : int
    is_active : bool
    timestamp : datetime
    type : FIFOOperationType
    side : FIFOSide
    quantity : float
    price : float

    _next_id = 0

    @classmethod
    def next_id(cls) -> int:
        id_ = cls._next_id
        cls._next_id += 1
        return id_

@dataclass
class FIFOOperation:
    id : int
    timestamp : datetime
    type : FIFOOperationType
    side : FIFOSide
    execution_price : float
    quantity : float
    linked_position_id: int | None = None
    _next_id = 0
    @classmethod
    def next_id(cls) -> int:
        id_ = cls._next_id
        cls._next_id += 1
        return id_

@dataclass(frozen=True)
class ResolveContext:
    """
    Unchanging context passed to SafeGuards strategies.
    Combines action, fifo status, and execution price for deterministic checks
    with no side effects.
    """
    action: AtomicAction
    fifo_queues: dict[FIFOSide, list[FIFOPosition]]
    execution_price: float
