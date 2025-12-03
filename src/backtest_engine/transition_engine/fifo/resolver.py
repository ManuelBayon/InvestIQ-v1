from backtest_engine.common.enums import FIFOSide
from backtest_engine.common.types import AtomicAction, FIFOPosition, FIFOOperation
from backtest_engine.transition_engine.fifo.resolve_strategies.factory import FIFOResolveFactory
from utilities.logger.factory import LoggerFactory
from utilities.logger.protocol import LoggerProtocol


class FIFOResolver:
    """
    Orchestrator for resolving AtomicActions into FIFOOperations.

    The resolver delegates to the FIFOResolveFactory to get the
    appropriate FIFOResolveStrategy for each action type, executes the
    resolution, and aggregates the resulting FIFOOperations.

    Responsibilities:
      - Select the correct strategy for each action via the factory
      - Invoke the strategy's resolve() method
      - Collect and return all resulting FIFOOperations
      - Log resolution details for traceability

    Typical usage:
        resolver = FIFOResolver(logger_factory, fifo_resolve_factory)
        ops = resolver.resolve(actions, fifo_queues, execution_price)

    Methods:
        - resolve_action: resolve a single AtomicAction into FIFOOperations
        - resolve: resolve a list of AtomicActions into FIFOOperations
    """
    def __init__(
        self,
        logger_factory: LoggerFactory,

    ) -> None:
        self._logger_factory = logger_factory
        self._logger: LoggerProtocol = self._logger_factory.child("FIFOResolver").get()
        self._fifo_resolve_factory : FIFOResolveFactory= FIFOResolveFactory(self._logger_factory)

    def resolve_action(
        self,
        action: AtomicAction,
        fifo_queues: dict[FIFOSide, list[FIFOPosition]],
        execution_price: float,
    ) ->  list[FIFOOperation]:

        strategy = self._fifo_resolve_factory.create(atomic_action_type=action.type)

        ops: list[FIFOOperation] = strategy.resolve(
            action=action,
            fifo_queues=fifo_queues,
            execution_price=execution_price
        )
        return ops

    def resolve(
        self,
        actions: list[AtomicAction],
        fifo_queues: dict[FIFOSide, list[FIFOPosition]],
        execution_price: float,
    ) -> list[FIFOOperation]:

        list_operations: list[FIFOOperation] = []

        for action in actions:
            ops : list[FIFOOperation] = self.resolve_action(
                action=action,
                fifo_queues=fifo_queues,
                execution_price=execution_price
            )
            list_operations.extend(ops)

        return list_operations