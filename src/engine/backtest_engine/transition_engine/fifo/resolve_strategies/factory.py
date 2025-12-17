
from engine.backtest_engine.common.enums import AtomicActionType
from engine.backtest_engine.transition_engine.fifo.guards_strategies.factory import SafeGuardFactory
from engine.backtest_engine.transition_engine.fifo.resolve_strategies.registry import FIFOResolveRegistry
from engine.backtest_engine.transition_engine.fifo.resolve_strategies.interface import FIFOResolveStrategy
from engine.utilities.logger.factory import LoggerFactory

class FIFOResolveFactory:
    def __init__(
            self,
            logger_factory: LoggerFactory
    ):
        self._logger_factory = logger_factory

    def create(
            self,
            atomic_action_type: AtomicActionType
    ) -> FIFOResolveStrategy:

        safe_guard_factory = SafeGuardFactory(logger_factory=self._logger_factory)
        strategy_cls = FIFOResolveRegistry.get(key=atomic_action_type)
        strategy = strategy_cls(
            logger=self._logger_factory.child(f"{strategy_cls.STRATEGY_NAME}").get(),
            safe_guard_factory=safe_guard_factory
        )
        return strategy