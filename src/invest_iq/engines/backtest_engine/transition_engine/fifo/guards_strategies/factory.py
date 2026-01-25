from invest_iq.engines.backtest_engine.common.enums import GuardName
from invest_iq.engines.backtest_engine.transition_engine.fifo.guards_strategies.expectations import GuardExpectation
from invest_iq.engines.backtest_engine.transition_engine.fifo.guards_strategies.interface import SafeGuard
from invest_iq.engines.backtest_engine.transition_engine.fifo.guards_strategies.registry import SafeGuardRegistry
from invest_iq.engines.utilities.logger.factory import LoggerFactory

class SafeGuardFactory:

    def __init__(
            self,
            logger_factory : LoggerFactory,
    ):
        self._logger_factory = logger_factory

    def create(
            self,
            key : GuardName
    ) -> SafeGuard[GuardExpectation]:
        strategy_cls: type[SafeGuard[GuardExpectation]] =SafeGuardRegistry.get(key)
        return strategy_cls(logger=self._logger_factory.child(f"{strategy_cls.STRATEGY_NAME}").get())

    def create_all(
            self
    ) -> list[SafeGuard[GuardExpectation]]:
        return [self.create(key) for key in SafeGuardRegistry.available()]