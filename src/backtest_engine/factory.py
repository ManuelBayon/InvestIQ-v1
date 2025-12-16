from dataclasses import dataclass

from backtest_engine.bootstraps.baxktest_engine_bootstrap import bootstrap_backtest_engine
from backtest_engine.common.contracts import BacktestInput, BacktestContext, ModelState, ExecutionState
from backtest_engine.common.enums import FutureCME
from backtest_engine.engine import BacktestEngine

from historical_data_engine.HistoricalDataEngine import HistoricalDataEngine
from historical_data_engine.connection.TWSConnection import TWSConnection
from historical_data_engine.enums import BarSize
from historical_data_engine.source.IBKRDataSource import IBKRDataSource
from historical_data_engine.instruments.ContFutureSettings import ContFutureSettings
from historical_data_engine.instruments.InstrumentID import InstrumentID
from historical_data_engine.request.IBKRRequestSettings import IBKRRequestSettings
from strategy_engine.filters.abstract_filter import AbstractFilter
from strategy_engine.strategies.abstract_strategy import AbstractStrategy

from utilities.logger.factory import LoggerFactory

@dataclass(frozen=True)
class BacktestBundle:
    engine: BacktestEngine
    context: BacktestContext
    input: BacktestInput

def build_backtest(
        logger_factory: LoggerFactory,
        symbol: FutureCME,
        duration_setting: str,
        bar_size_setting: BarSize,
        strategy: type[AbstractStrategy],
        filters: list[type[AbstractFilter]] | None = None,
        initial_cash: float = 100_000,
) -> BacktestBundle:

    # 3. Historical data
    instrument_settings = ContFutureSettings(
        symbol=symbol.value,
        symbol_id=InstrumentID.from_enum(symbol)
    )
    request_settings = IBKRRequestSettings(
        duration=duration_setting,
        bar_size_setting=bar_size_setting
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

    # 5. Backtest engine configuration
    backtest_engine: BacktestEngine = bootstrap_backtest_engine(
        logger_factory=logger_factory,
        strategy=strategy,
        filters=filters,
        initial_cash=initial_cash
    )

    # 6. Prepare backtest input once
    bt_input = BacktestInput(
        timestamp=df.timestamp,
        data={
            "open": df.open,
            "high": df.high,
            "low": df.low,
            "close": df.close
        }
    )

    # 7. Initialize Backtest context
    context = BacktestContext(
        timestamp=df.timestamp.iloc[0],
        bar={},
        history={"open": [], "high": [], "low": [], "close": []},
        model=ModelState(),
        execution=ExecutionState()
    )

    return BacktestBundle(
        engine=backtest_engine,
        context=context,
        input=bt_input
    )