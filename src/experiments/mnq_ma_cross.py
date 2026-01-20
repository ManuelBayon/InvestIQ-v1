from engine.backtest_engine.common.enums import FutureCME
from engine.backtest_engine.factory import BacktestBundle, build_backtest

from config.backtest import BacktestConfig
from engine.historical_data_engine.enums import BarSize

from engine.strategy_engine.strategies.components.MovingAverageCrossStrategy import MovingAverageCrossStrategy
from engine.utilities.logger.factory import LoggerFactory


def build_experiment(
        logger_factory: LoggerFactory,
) -> BacktestBundle:

    config = BacktestConfig(
        symbol=FutureCME.MNQ,
        duration_setting="100 D",
        bar_size_setting=BarSize.ONE_HOUR,
        strategy=MovingAverageCrossStrategy(
            fast_window=10,
            slow_window=50,
        ),
        filters=None,
        initial_cash=100_000,
    )

    return build_backtest(
    logger_factory=logger_factory,
    backtest_config=config
    )