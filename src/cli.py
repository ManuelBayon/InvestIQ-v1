from datetime import datetime

from invest_iq.engines.backtest_engine.common.enums import FutureCME
from invest_iq.engines.backtest_engine.orchestrator import BacktestRunner
from invest_iq.engines.export_engine.registries.config import ExportKey, ExportOptions
from invest_iq.engines.export_engine.runner import BacktestExportRunner
from invest_iq.engines.utilities.logger.factory import LoggerFactory
from invest_iq.engines.utilities.logger.setup import init_base_logger
from experiments.mnq_ma_cross import build_experiment
from invest_iq.engines.backtest_engine.common.contracts import BacktestResult

def main() -> None:

    # 1. Init base logger
    init_base_logger()
    logger_factory = LoggerFactory(
        engine_type="Backtest",
        run_id="0841996",
    )

    # 2. Backtest configuration + build
    bundle = build_experiment(
        logger_factory=logger_factory
    )

    # 3. Instantiate and run backtest orchestrator
    runner = BacktestRunner(
        logger_factory=logger_factory,
        engine=bundle.engine,
        context=bundle.context,
    )
    result: BacktestResult= runner.run(bt_input=bundle.input)

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
        execution_log=result.execution_log,
        metrics={"Realized PnL":result.realized_pnl}
    )

if __name__ == "__main__":
    main()
