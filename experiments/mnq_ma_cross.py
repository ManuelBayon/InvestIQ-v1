from invest_iq.engines.backtest_engine.common.enums import FutureCME
from invest_iq.engines.backtest_engine.factory import BacktestBundle, build_backtest

from invest_iq.config.backtest_config import BacktestConfig
from invest_iq.engines.historical_data_engine.enums import BarSize

from invest_iq.engines.strategy_engine.strategies.components.MovingAverageCrossStrategy import MovingAverageCrossStrategy
from invest_iq.engines.utilities.logger.factory import LoggerFactory


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

    bundle = build_backtest(
    logger_factory=logger_factory,
    backtest_config=config
    )

    return bundle