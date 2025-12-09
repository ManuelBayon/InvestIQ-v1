from backtest_engine.common.enums import FutureCME
from backtest_engine.engine import BacktestEngine
from backtest_engine.bootstrap import backtest_engine_bootstrap
from backtest_engine.transition_engine.engine import TransitionEngine

from export_engine.bootstrap import export_engine_bootstrap

from historical_data_engine.HistoricalDataEngine import HistoricalDataEngine
from historical_data_engine.connection.TWSConnection import TWSConnection
from historical_data_engine.enums import BarSize
from historical_data_engine.source.IBKRDataSource import IBKRDataSource
from historical_data_engine.instruments.ContFutureSettings import ContFutureSettings
from historical_data_engine.instruments.InstrumentID import InstrumentID
from historical_data_engine.request.IBKRRequestSettings import IBKRRequestSettings
from strategy_engine.strategies.components.MovingAverageCrossStrategy import MovingAverageCrossStrategy
from strategy_engine.strategy_orchestrator import StrategyOrchestrator

from utilities.logger.factory import LoggerFactory
from utilities.logger.setup import init_base_logger

def main() -> None:

    # 1. Logger initialisation
    init_base_logger(debug=True)
    logger_factory = LoggerFactory(
        engine_type="Backtest",
        run_id="0841996",
    )

    # 2. Bootstraps
    backtest_engine_bootstrap(logger=logger_factory.child("BacktestEngine Bootstrap").get())
    export_engine_bootstrap(logger=logger_factory.child("ExportEngine Bootstrap").get())

    # 3. Historical data engine configuration
    instrument_settings = ContFutureSettings(
        symbol=FutureCME.MNQ.value,
        symbol_id=InstrumentID.from_enum(FutureCME.MNQ)
    )
    request_settings = IBKRRequestSettings(
        duration="200 D",
        bar_size_setting=BarSize.ONE_HOUR
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

    # 4. Strategy engine configuration
    strategy = MovingAverageCrossStrategy()
    orchestrator = StrategyOrchestrator(strategy=strategy)

    # 5. Backtest engine configuration
    transition_engine: TransitionEngine = TransitionEngine(logger_factory=logger_factory)
    backtest_engine: BacktestEngine = BacktestEngine(
        logger_factory=logger_factory,
        hist_data_engine=hist_data_engine,
        orchestrator=orchestrator,
        transition_engine=transition_engine
    )

    # 6. Run backtest
    backtest_engine.run()

if __name__ == "__main__":
    main()