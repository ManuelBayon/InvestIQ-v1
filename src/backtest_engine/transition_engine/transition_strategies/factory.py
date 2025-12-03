from backtest_engine.common.enums import TransitionType
from backtest_engine.transition_engine.transition_strategies.interface import TransitionStrategy
from backtest_engine.transition_engine.transition_strategies.registry import TransitionStrategyRegistry
from utilities.logger.factory import LoggerFactory

class TransitionStrategyFactory:
    def __init__(self, logger_factory: LoggerFactory) -> None:
        self._logger_factory = logger_factory

    def create(
            self,
            transition_type: TransitionType
    ) -> TransitionStrategy:

        strategy_cls: type[TransitionStrategy] = TransitionStrategyRegistry.get(key=transition_type)
        return strategy_cls(
            logger=self._logger_factory.child(f"{strategy_cls.STRATEGY_NAME}").get()
        )
