from collections.abc import Callable
from typing import TypeVar

from invest_iq.engines.backtest_engine.common.enums import (
    CurrentState, Event, TransitionType, AtomicActionType,
    GuardName, FIFOOperationType)
from invest_iq.engines.backtest_engine.engine import BacktestEngine
from invest_iq.engines.backtest_engine.portfolio.execution_strategies.registry import FIFOExecutionRegistry
from invest_iq.engines.backtest_engine.portfolio.portfolio import Portfolio
from invest_iq.engines.backtest_engine.transition_engine.engine import TransitionEngine
from invest_iq.engines.backtest_engine.transition_engine.fifo.guards_strategies.registry import SafeGuardRegistry
from invest_iq.engines.backtest_engine.transition_engine.fifo.resolve_strategies.registry import FIFOResolveRegistry
from invest_iq.engines.backtest_engine.transition_engine.transition_rules.registry import TransitionRuleRegistry
from invest_iq.engines.backtest_engine.transition_engine.transition_strategies.registry import TransitionStrategyRegistry
from invest_iq.engines.strategy_engine.filters.abstract_filter import AbstractFilter
from invest_iq.engines.strategy_engine.orchestrator.orchestrator import StrategyOrchestrator
from invest_iq.engines.strategy_engine.strategies.abstract_strategy import AbstractStrategy
from invest_iq.engines.utilities.import_tools import import_submodules
from invest_iq.engines.utilities.logger.factory import LoggerFactory
from invest_iq.engines.utilities.logger.protocol import LoggerProtocol


T = TypeVar("T")
def validate_registry(
        logger: LoggerProtocol,
        name: str,
        import_path: str,
        expected: set[T],
        available_fn: Callable[[], list[T]]
) -> None:
    """
    Generic validation for a registries:
    - Import modules from a path (to trigger registrations)
    - Check that available matches expected
    - Log summary, raises if mismatch
    """
    import_submodules(import_path)

    registered: set[T] = set(available_fn())
    missing = expected - registered
    extra = registered - expected

    if missing:
        raise RuntimeError(f"Missing {name}: {missing}")
    if extra:
        raise RuntimeError(f"Unexpected {name}: {extra}")

    logger.info(f"{name} registered: {len(registered)} / {len(expected)}")

def _validate_registries(logger: LoggerProtocol) -> None:
    """
    Verify that all expected rules and policies are recorded.
    Block if there is ever a gap in the configuration.
    """
    logger.info("Initializing backtest engines...")
    validate_registry(
        logger,
        "Transition rules",
        "invest_iq.engines.backtest_engine.transition_engine.transition_rules.rules",
        {(s, e) for s in CurrentState for e in Event},
        TransitionRuleRegistry.available,
    )
    validate_registry(
        logger,
        "Transition strategies",
        "invest_iq.engines.backtest_engine.transition_engine.transition_strategies.strategies",
        set(TransitionType),
        TransitionStrategyRegistry.available,
    )
    validate_registry(
        logger,
        "fifo resolve strategies",
        "invest_iq.engines.backtest_engine.transition_engine.fifo.resolve_strategies.strategies",
        set(AtomicActionType),
        FIFOResolveRegistry.available,
    )
    validate_registry(
        logger,
        "SafeGuard strategies",
        "invest_iq.engines.backtest_engine.transition_engine.fifo.guards_strategies.strategies",
        set(GuardName),
        SafeGuardRegistry.available,
    )
    validate_registry(
        logger,
        "fifo execution strategies",
        "invest_iq.engines.backtest_engine.portfolio.execution_strategies.strategies",
        set(FIFOOperationType),
        FIFOExecutionRegistry.available,
    )
    logger.info("Backtest engines initialized successfully.")



def bootstrap_backtest_engine(
        logger_factory: LoggerFactory,
        strategy: AbstractStrategy,
        initial_cash: float,
        filters: list[AbstractFilter] | None = None
) -> BacktestEngine:

    _validate_registries(
        logger=logger_factory.child("backtest_engine bootstrapper").get()
    )

    # 1. Build Strategy Orchestrator
    orchestrator = StrategyOrchestrator(
        strategy=strategy,
        filters=filters,
    )

    # 2. Build Transition Engine
    transition_engine = TransitionEngine(logger_factory=logger_factory)

    # 3. Build Portfolio
    portfolio = Portfolio(
        logger_factory=logger_factory,
        transition_engine=transition_engine,
        initial_cash=initial_cash
    )

    # 4. Build Backtest Engine
    return BacktestEngine(
        logger=logger_factory.child("backtest_engine").get(),
        orchestrator=orchestrator,
        transition_engine=transition_engine,
        portfolio=portfolio,
    )