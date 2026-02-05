from __future__ import annotations

from investiq.execution.transition.enums import FIFOSide
from investiq.execution.transition.types import AtomicAction, FIFOOperation, FIFOPosition
from investiq.execution.transition.fifo.factory import FIFOResolveFactory


class FIFOResolver:
    """
    Orchestrator: AtomicAction -> FIFOOperation(s).
    Delegates per-action resolution to registered FIFO resolve strategies.
    """

    def __init__(self) -> None:
        self._factory = FIFOResolveFactory()

    def resolve_action(
        self,
        *,
        action: AtomicAction,
        fifo_queues: dict[FIFOSide, list[FIFOPosition]],
        execution_price: float,
    ) -> list[FIFOOperation]:
        strategy = self._factory.create(action_type=action.type)
        return strategy.resolve(action=action, fifo_queues=fifo_queues, execution_price=execution_price)

    def resolve(
        self,
        *,
        actions: list[AtomicAction],
        fifo_queues: dict[FIFOSide, list[FIFOPosition]],
        execution_price: float,
    ) -> list[FIFOOperation]:
        ops: list[FIFOOperation] = []
        for a in actions:
            ops.extend(self.resolve_action(action=a, fifo_queues=fifo_queues, execution_price=execution_price))
        return ops
