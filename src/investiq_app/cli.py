from investiq.market_data import BarSize
from investiq_app.experiments.builder import build_experiment
from investiq.api.instruments import AssetClass, FutureCME
from investiq_app.experiments.config import BacktestConfig
from investiq_research.execution_planners.fixed_pct_oco import FixedPctOCOPlanner

from investiq_research.strategies.MovingAverageCrossStrategy import MovingAverageCrossStrategy

def main() -> None:

    config = BacktestConfig(
        debug=False,
        symbol=FutureCME.MNQ,
        asset_class=AssetClass.CONT_FUT,
        duration_setting="100 D",
        bar_size_setting=BarSize.ONE_HOUR,
        strategy=MovingAverageCrossStrategy(
            fast_window=10,
            slow_window=50,
        ),
        execution_planner=FixedPctOCOPlanner(), #type: ignore
        filters=None,
        initial_cash=100_000,
    )
    bundle = build_experiment(config=config)
    result = bundle.backtest_engine.run(bt_input=bundle.backtest_input)
    bundle.exporter.export(
        execution_log=result.execution_log,
        metrics=result.metrics
    )

if __name__ == "__main__":
    main()
