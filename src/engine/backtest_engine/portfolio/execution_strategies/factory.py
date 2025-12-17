from engine.backtest_engine.common.enums import FIFOOperationType
from engine.backtest_engine.portfolio.execution_strategies.interface import PortfolioExecutionStrategy

from engine.backtest_engine.portfolio.execution_strategies.registry import FIFOExecutionRegistry
from engine.utilities.logger.factory import LoggerFactory
from engine.utilities.logger.protocol import LoggerProtocol


class FIFOExecutionFactory:
    def __init__(
            self,
            logger_factory: LoggerFactory
    ):
        self._logger_factory = logger_factory
        self._logger : LoggerProtocol = self._logger_factory.child("FIFOExecutionFactory").get()

    def create(
            self,
            fifo_op_type: FIFOOperationType
    ) -> PortfolioExecutionStrategy:
        strategy_cls: type[PortfolioExecutionStrategy] = FIFOExecutionRegistry.get(fifo_op_type)
        return strategy_cls(self._logger_factory.child(f"{strategy_cls.STRATEGY_NAME}").get())