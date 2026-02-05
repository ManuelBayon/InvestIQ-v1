from __future__ import annotations

from typing import ClassVar, Protocol

from investiq.execution.transition.enums import AtomicActionType, FIFOSide
from investiq.execution.transition.types import AtomicAction, FIFOOperation, FIFOPosition


class FIFOResolveStrategy(Protocol):
    """
    Static contract for resolving one AtomicAction into FIFOOperations.
    Implementations must be duck-typed (do NOT inherit from this Protocol).
    """
    NAME: ClassVar[str]
    ACTION: ClassVar[AtomicActionType]

    def resolve(
        self,
        *,
        action: AtomicAction,
        fifo_queues: dict[FIFOSide, list[FIFOPosition]],
        execution_price: float,
    ) -> list[FIFOOperation]:
        ...