from datetime import datetime

from experiments.builder import build_experiment
from invest_iq.config.backtest_config import BacktestConfig

from invest_iq.engines.backtest_engine.common.enums import FutureCME
from invest_iq.engines.export_engine.registries.config import ExportKey, ExportOptions
from invest_iq.engines.export_engine.runner import BacktestExportRunner
from invest_iq.engines.historical_data_engine.enums import BarSize
from invest_iq.engines.strategy_engine.strategies.components.MovingAverageCrossStrategy import \
    MovingAverageCrossStrategy
from invest_iq.engines.utilities.logger.factory import LoggerFactory
from invest_iq.engines.utilities.logger.setup import init_base_logger

def main() -> None:

    # 1. Init base logger
    init_base_logger(debug=True)
    logger_factory = LoggerFactory(
        engine_type="Backtest",
        run_id="0841996",
    )

    # 2. Backtest configuration
    bundle = build_experiment(
        logger_factory=logger_factory,
        config=BacktestConfig(
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
    )

    # 3. Run backtest engine
    result = bundle.engine.run(bt_input=bundle.bt_input)

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
        metrics={"Realized PnL":bundle.engine.portfolio.realized_pnl}
    )

if __name__ == "__main__":
    main()
