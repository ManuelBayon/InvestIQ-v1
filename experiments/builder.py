from dataclasses import dataclass

from invest_iq.engines.backtest_engine.bootstrap import bootstrap_backtest_engine
from invest_iq.engines.backtest_engine.common.enums import FutureCME
from invest_iq.engines.backtest_engine.common.types import BacktestInput
from invest_iq.engines.backtest_engine.engine import BacktestEngine

from invest_iq.config.backtest_config import BacktestConfig

from invest_iq.engines.historical_data_engine.HistoricalDataEngine import HistoricalDataEngine
from invest_iq.engines.historical_data_engine.backtest_feed import DataFrameBacktestFeed
from invest_iq.engines.historical_data_engine.connection.TWSConnection import TWSConnection
from invest_iq.engines.historical_data_engine.enums import BarSize
from invest_iq.engines.historical_data_engine.instruments.ContFutureSettings import ContFutureSettings
from invest_iq.engines.historical_data_engine.instruments.InstrumentID import InstrumentID
from invest_iq.engines.historical_data_engine.request.IBKRRequestSettings import IBKRRequestSettings
from invest_iq.engines.historical_data_engine.source.IBKRDataSource import IBKRDataSource

from invest_iq.engines.strategy_engine.strategies.components.MovingAverageCrossStrategy import MovingAverageCrossStrategy

from invest_iq.engines.utilities.logger.factory import LoggerFactory

@dataclass
class BacktestBundle:
    engine: BacktestEngine
    bt_input: BacktestInput

def build_experiment(logger_factory: LoggerFactory) -> BacktestBundle:

    config = BacktestConfig(
        symbol=FutureCME.MNQ.value,
        asset_class="CONT_FUT",
        duration_setting="100 D",
        bar_size_setting=BarSize.ONE_HOUR,
        strategy=MovingAverageCrossStrategy(
            fast_window=10,
            slow_window=50,
        ),
        filters=None,
        initial_cash=100_000,
    )

    # 1. Configure and load historical data
    instrument_settings = ContFutureSettings(
        symbol=config.symbol,
        symbol_id=InstrumentID.from_symbol(config.symbol)
    )
    request_settings = IBKRRequestSettings(
        duration=config.duration_setting,
        bar_size_setting=config.bar_size_setting
    )
    tws_connection = TWSConnection(
        logger=logger_factory.child("TWS Connection").get(),
    )
    data_source = IBKRDataSource(
        logger=logger_factory.child("InteractiveBroker DataSource").get(),
        connection=tws_connection
    )
    hist_data_engine: HistoricalDataEngine = HistoricalDataEngine(
        logger=logger_factory.child("Historical Data Engine").get(),
        instrument_settings=instrument_settings,
        request_settings=request_settings,
        data_source=data_source
    )
    df = hist_data_engine.load_data()

    # 2. Bootstrap Backtest Engine
    backtest_engine: BacktestEngine = bootstrap_backtest_engine(
        logger_factory=logger_factory,
        strategy=config.strategy,
        filters=config.filters,
        initial_cash=config.initial_cash
    )

    # 3. Create event feed from data frame and initialize backtest input
    feed = DataFrameBacktestFeed(
        logger=logger_factory.child("BacktestFeed").get(),
        df=df,
        symbol=config.symbol,
        bar_size=config.bar_size_setting,
    )
    bt_input = BacktestInput(
        instrument=InstrumentSpec(
            symbol=config.symbol,
            asset_class=config.asset_class,
            bar_size=config.bar_size_setting,
        ),
        events=feed
    )

    # 5. Returns the Backtest Bundle
    return BacktestBundle(
        engine=backtest_engine,
        context=context,
        bt_input=bt_input,
    )