from typing import Protocol

from invest_iq.engines.backtest_engine.common.enums import FIFOSide
from invest_iq.engines.backtest_engine.common.types import AtomicAction
from invest_iq.engines.backtest_engine.common.types import FIFOPosition, FIFOOperation


class FIFOResolveStrategyProtocol(Protocol):
    """
    Base class for all fifo resolve resolve_strategies.

    Each subclass must define:
    - STRATEGY_NAME: unique non-empty identifier (used for logging and registries).
    - resolve(): how to turn an AtomicAction into one or more FIFOOperations.

    Logger is built from LoggerFactory with namespace:
        "BacktestEngine.{STRATEGY_NAME}"
    """
    def resolve(
        self,
        action: AtomicAction,
        fifo_queues: dict[FIFOSide, list[FIFOPosition]],
        execution_price: float
    ) -> list[FIFOOperation]:
        """
        Transform an AtomicAction into a list of FIFOOperations.

        Args:
            action: the atomic action to resolve
            fifo_queues: the current fifo queues (long/short)
            execution_price: price used for the operation

        Returns:
            A list of FIFOOperations ready to be applied to the Portfolio.
        """
        ...