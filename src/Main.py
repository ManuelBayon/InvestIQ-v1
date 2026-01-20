from datetime import datetime

from engine.backtest_engine.common.enums import FutureCME
from engine.backtest_engine.orchestrator import BacktestOrchestrator
from engine.export_engine.registries.config import ExportKey, ExportOptions
from engine.export_engine.runner import BacktestExportRunner
from engine.utilities.logger.factory import LoggerFactory
from engine.utilities.logger.setup import init_base_logger
from experiments.mnq_ma_cross import build_experiment


def main() -> None:

    # 1. Init base logger
    init_base_logger(debug=True)
    logger_factory = LoggerFactory(
        engine_type="Backtest",
        run_id="0841996",
    )

    # 2. Backtest configuration + build
    bundle = build_experiment(
        logger_factory=logger_factory
    )

    # 3. Instantiate and run backtest orchestrator
    orchestrator = BacktestOrchestrator(
        engine=bundle.engine,
        context=bundle.context,
    )

    for _ in orchestrator.stream_candles(bt_input=bundle.input):
        pass

    # 4. Export Execution logs
    export_runner = BacktestExportRunner(
        logger_factory=logger_factory,
        export_key=ExportKey.EXCEL,
        export_options=ExportOptions(
            sink={
                "filename": FutureCME.MNQ.value + datetime.now().strftime("_%Y-%m-%d_%Hh%M"),
            }
        )
    )
    export_runner.export_execution_log(
        bundle.engine.portfolio.execution_log
    )

if __name__ == "__main__":
    main()
