from datetime import datetime

from experiments.builder import build_experiment

from invest_iq.engines.backtest_engine.common.enums import FutureCME
from invest_iq.engines.export_engine.registries.config import ExportKey, ExportOptions
from invest_iq.engines.export_engine.runner import BacktestExportRunner
from invest_iq.engines.utilities.logger.factory import LoggerFactory
from invest_iq.engines.utilities.logger.setup import init_base_logger
from invest_iq.engines.backtest_engine.common.contracts import BacktestResult

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
    for event in bundle.bt_input.events:
        bundle.engine.step(
            event=event,
            context=bundle.context,
        )

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
    export_runner.export(
        execution_log=bundle.engine.portfolio.execution_log,
        metrics={"Realized PnL":bundle.engine.portfolio.realized_pnl}
    )

if __name__ == "__main__":
    main()
