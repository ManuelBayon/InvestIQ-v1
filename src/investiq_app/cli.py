from investiq_app.experiments.builder import build_experiment
from investiq.api.instruments import AssetClass, FutureCME
from investiq.data.legagy_data_engine.enums import BarSize
from investiq_app.experiments.config import BacktestConfig
from investiq_research.strategies.MovingAverageCrossStrategy import MovingAverageCrossStrategy

def main() -> None:
    bundle = build_experiment(
        config=BacktestConfig(
            symbol=FutureCME.MNQ,
            asset_class=AssetClass.CONT_FUT,
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
    result = bundle.backtest_engine.run(bt_input=bundle.backtest_input)
    bundle.exporter.export(
        execution_log=result.execution_log,
        metrics=result.metrics
    )

if __name__ == "__main__":
    main()
