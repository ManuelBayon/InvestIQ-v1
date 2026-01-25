from dataclasses import dataclass

from invest_iq.engines.backtest_engine.bootstraps.backtest_engine_bootstrap import bootstrap_backtest_engine
from invest_iq.engines.backtest_engine.common.backtest_context import BacktestContext
from invest_iq.engines.backtest_engine.common.contracts import BacktestInput, ModelState, ExecutionState
from invest_iq.engines.backtest_engine.engine import BacktestEngine

from invest_iq.config.backtest_config import BacktestConfig

from invest_iq.engines.historical_data_engine.HistoricalDataEngine import HistoricalDataEngine
from invest_iq.engines.historical_data_engine.connection.TWSConnection import TWSConnection
from invest_iq.engines.historical_data_engine.source.IBKRDataSource import IBKRDataSource
from invest_iq.engines.historical_data_engine.instruments.ContFutureSettings import ContFutureSettings
from invest_iq.engines.historical_data_engine.instruments.InstrumentID import InstrumentID
from invest_iq.engines.historical_data_engine.request.IBKRRequestSettings import IBKRRequestSettings

from invest_iq.engines.utilities.logger.factory import LoggerFactory

@dataclass(frozen=True)
class BacktestBundle:
    engine: BacktestEngine
    context: BacktestContext
    input: BacktestInput

def build_backtest(
        logger_factory: LoggerFactory,
        backtest_config: BacktestConfig,
) -> BacktestBundle:

    # 1. Configure and load historical data
    instrument_settings = ContFutureSettings(
        symbol=backtest_config.symbol.value,
        symbol_id=InstrumentID.from_enum(backtest_config.symbol)
    )
    request_settings = IBKRRequestSettings(
        duration=backtest_config.duration_setting,
        bar_size_setting=backtest_config.bar_size_setting
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

    # 2. Backtest engines configuration
    backtest_engine: BacktestEngine = bootstrap_backtest_engine(
        logger_factory=logger_factory,
        strategy=backtest_config.strategy,
        filters=backtest_config.filters,
        initial_cash=backtest_config.initial_cash
    )

    # 3. Create backtest input
    bt_input = BacktestInput(
        timestamp=df.timestamp,
        data={
            "open": df.open,
            "high": df.high,
            "low": df.low,
            "close": df.close
        }
    )

    # 4. Initialize Backtest context
    context = BacktestContext()

    # 5. Returns the Backtest Bundle
    return BacktestBundle(
        engine=backtest_engine,
        context=context,
        input=bt_input,
    )