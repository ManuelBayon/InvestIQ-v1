from dataclasses import dataclass
from datetime import datetime

from investiq.api.backtest import BacktestInput
from investiq.api.instruments import InstrumentSpec
from investiq.core.engine import BacktestEngine
from investiq.data.legagy_data_engine.HistoricalDataEngine import HistoricalDataEngine
from investiq.data.legagy_data_engine.backtest_feed import DataFrameBacktestFeed
from investiq.data.legagy_data_engine.instruments.ContFutureSettings import ContFutureSettings
from investiq.data.legagy_data_engine.instruments.InstrumentID import InstrumentID
from investiq.export_engine.registries.config import ExportKey, ExportOptions
from investiq.export_engine.runner import BacktestExportRunner

from investiq.data.legagy_data_engine.connection.TWSConnection import TWSConnection

from investiq.data.legagy_data_engine.request.IBKRRequestSettings import IBKRRequestSettings
from investiq.data.legagy_data_engine.source.IBKRDataSource import IBKRDataSource

from investiq.utilities.logger.factory import LoggerFactory
from investiq.utilities.logger.setup import init_base_logger
from investiq.runs.builder import bootstrap_backtest_engine
from investiq_app.experiments.config import BacktestConfig

import investiq_research.features.SMA

@dataclass
class BacktestBundle:
    logger_factory: LoggerFactory
    backtest_input: BacktestInput
    backtest_engine: BacktestEngine
    exporter: BacktestExportRunner


class FutureCME:
    pass


def build_experiment(config: BacktestConfig) -> BacktestBundle:

    # 0. Init base logger
    init_base_logger(debug=config.debug)
    logger_factory = LoggerFactory(
        engine_type="Backtest",
        run_id="0841996",
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

    # 4. Exporter configuration
    export_runner = BacktestExportRunner(
        logger_factory=logger_factory,
        export_key=ExportKey.EXCEL,
        export_options=ExportOptions(
            sink={
                "filename": "MNQ" + datetime.now().strftime("_%Y-%m-%d_%Hh%M"),
            }
        )
    )

    # 5. Return BacktestBundle
    return BacktestBundle(
        logger_factory=logger_factory,
        backtest_input=bt_input,
        backtest_engine=backtest_engine,
        exporter=export_runner
    )