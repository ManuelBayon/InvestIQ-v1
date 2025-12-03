from abc import ABC, abstractmethod

from backtest_engine.common.enums import FIFOSide
from backtest_engine.common.types import AtomicAction
from backtest_engine.common.types import FIFOOperation
from backtest_engine.common.types import FIFOPosition

from backtest_engine.transition_engine.fifo.resolve_strategies.base import FIFOResolveStrategyBase
from backtest_engine.transition_engine.fifo.resolve_strategies.protocol import FIFOResolveStrategyProtocol


class FIFOResolveStrategy(FIFOResolveStrategyProtocol, FIFOResolveStrategyBase, ABC):

    def __init_subclass__(
            cls,
            **kwargs: object
    ) -> None:
        super().__init_subclass__(**kwargs)
        if not cls.STRATEGY_NAME or not cls.STRATEGY_NAME.strip():
            raise TypeError(
                f"{cls.__name__} must define a non-empty STRATEGY_NAME"
            )

    @abstractmethod
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