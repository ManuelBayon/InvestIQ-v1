from investiq.api.filter import Filter
from investiq.api.strategy import Strategy
from investiq.core.engine import BacktestEngine
from investiq.core.features.registry import FeaturePipelineRegistry
from investiq.core.features.store import FeatureStore

from investiq.execution.portfolio.portfolio import Portfolio
from investiq.execution.transition.engine import TransitionEngine
from investiq.core.orchestrator import StrategyOrchestrator
from investiq.utilities.logger.factory import LoggerFactory


def bootstrap_backtest_engine(
        logger_factory: LoggerFactory,
        strategy: Strategy,
        initial_cash: float,
        filters: list[Filter] | None = None
) -> BacktestEngine:

    feature_store = FeatureStore(logger=logger_factory.child("Feature store").get())

    # 1. Build Strategy Orchestrator
    strategy_orchestrator = StrategyOrchestrator(
        available_pipelines=feature_store.pipeline_names(),
        strategy=strategy,
        filters=filters,
    )

    # 2. Build Transition Engine
    transition_engine = TransitionEngine(logger_factory=logger_factory)

    # 3. Build Portfolio
    portfolio = Portfolio(
        logger_factory=logger_factory,
        initial_cash=initial_cash
    )

    # 4. Build Backtest Engine
    return BacktestEngine(
        logger_factory=logger_factory,
        strategy_orchestrator=strategy_orchestrator,
        transition_engine=transition_engine,
        portfolio=portfolio,
    )