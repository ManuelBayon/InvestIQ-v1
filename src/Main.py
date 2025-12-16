from datetime import datetime

from backtest_engine.factory import build_backtest
from backtest_engine.orchestrator import BacktestOrchestrator
from backtest_engine.common.enums import FutureCME

from export_engine.bootstrap import export_engine_bootstrap
from export_engine.factory import ExportServiceFactory
from export_engine.registries.config import ExportOptions, ExportKey

from historical_data_engine.enums import BarSize

from strategy_engine.strategies.components.MovingAverageCrossStrategy import MovingAverageCrossStrategy

from utilities.logger.factory import LoggerFactory
from utilities.logger.setup import init_base_logger

def main() -> None:

    init_base_logger(debug=True)
    logger_factory = LoggerFactory(
        engine_type="Backtest",
        run_id="0841996",
    )
    # 2. Bootstraps
    export_engine_bootstrap(logger=logger_factory.child("ExportEngine Bootstrap").get())

    export_service_factory = ExportServiceFactory(
        logger_factory=logger_factory,
        options=ExportOptions(
            sink={
                "filename": FutureCME.MNQ.value + datetime.now().strftime("_%Y-%m-%d_%Hh%M"),
            }
        )
    )

    bundle = build_backtest(
        logger_factory=logger_factory,
        symbol=FutureCME.MNQ,
        duration_setting="100 D",
        bar_size_setting=BarSize.ONE_HOUR,
        strategy=MovingAverageCrossStrategy,
        filters=None,
        initial_cash=100_000,
    )

    orchestrator = BacktestOrchestrator(
        engine=bundle.engine,
        context=bundle.context,
    )

    for _ in orchestrator.stream_candles(bt_input=bundle.input):
        pass

    export_service = export_service_factory.create_backtest_batch_export_service(
        key=ExportKey.EXCEL
    )
    export_service.export(
        raw_data=bundle.engine.portfolio.execution_log
    )

    print("Backtest finished.")

if __name__ == "__main__":
    main()
