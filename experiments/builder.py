from dataclasses import dataclass
from datetime import datetime

from invest_iq.engines.backtest_engine.bootstrap import bootstrap_backtest_engine
from invest_iq.engines.backtest_engine.common.enums import FutureCME
from invest_iq.engines.backtest_engine.common.types import BacktestInput, InstrumentSpec
from invest_iq.engines.backtest_engine.engine import BacktestEngine

from invest_iq.config.backtest_config import BacktestConfig
from invest_iq.engines.export_engine.registries.config import ExportKey, ExportOptions
from invest_iq.engines.export_engine.runner import BacktestExportRunner

from invest_iq.engines.historical_data_engine.HistoricalDataEngine import HistoricalDataEngine
from invest_iq.engines.historical_data_engine.backtest_feed import DataFrameBacktestFeed
from invest_iq.engines.historical_data_engine.connection.TWSConnection import TWSConnection
from invest_iq.engines.historical_data_engine.instruments.ContFutureSettings import ContFutureSettings
from invest_iq.engines.historical_data_engine.instruments.InstrumentID import InstrumentID
from invest_iq.engines.historical_data_engine.request.IBKRRequestSettings import IBKRRequestSettings
from invest_iq.engines.historical_data_engine.source.IBKRDataSource import IBKRDataSource

from invest_iq.engines.utilities.logger.factory import LoggerFactory

@dataclass
class BacktestBundle:
    backtest_input: BacktestInput
    backtest_engine: BacktestEngine
    exporter: BacktestExportRunner

def build_experiment(
        logger_factory: LoggerFactory,
        config: BacktestConfig
) -> BacktestBundle:

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

    # 5. Exporter configuration
    export_runner = BacktestExportRunner(
        logger_factory=logger_factory,
        export_key=ExportKey.EXCEL,
        export_options=ExportOptions(
            sink={
                "filename": FutureCME.MNQ.value + datetime.now().strftime("_%Y-%m-%d_%Hh%M"),
            }
        )
    )

    # 6. Return BacktestBundle
    return BacktestBundle(
        backtest_input=bt_input,
        backtest_engine=backtest_engine,
        exporter=export_runner
    )