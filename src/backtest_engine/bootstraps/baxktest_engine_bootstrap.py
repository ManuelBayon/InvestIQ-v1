from backtest_engine.bootstraps.common import validate_registry
from backtest_engine.common.enums import (
    CurrentState, Event, TransitionType, AtomicActionType,
    GuardName, FIFOOperationType)
from backtest_engine.engine import BacktestEngine
from backtest_engine.portfolio.execution_strategies.registry import FIFOExecutionRegistry
from backtest_engine.portfolio.portfolio import Portfolio
from backtest_engine.transition_engine.engine import TransitionEngine
from backtest_engine.transition_engine.fifo.guards_strategies.registry import SafeGuardRegistry
from backtest_engine.transition_engine.fifo.resolve_strategies.registry import FIFOResolveRegistry
from backtest_engine.transition_engine.transition_rules.registry import TransitionRuleRegistry
from backtest_engine.transition_engine.transition_strategies.registry import TransitionStrategyRegistry
from strategy_engine.filters.abstract_filter import AbstractFilter
from strategy_engine.orchestrator.orchestrator import StrategyOrchestrator
from strategy_engine.strategies.abstract_strategy import AbstractStrategy
from utilities.logger.factory import LoggerFactory
from utilities.logger.protocol import LoggerProtocol


def _validate_registries(logger: LoggerProtocol) -> None:
    """
    Verify that all expected rules and policies are recorded.
    Block if there is ever a gap in the configuration.
    """
    logger.info("Initializing backtest engine...")
    validate_registry(
        logger,
        "Transition rules",
        "backtest_engine.transition_engine.transition_rules.rules",
        {(s, e) for s in CurrentState for e in Event},
        TransitionRuleRegistry.available,
    )
    validate_registry(
        logger,
        "Transition strategies",
        "backtest_engine.transition_engine.transition_strategies.strategies",
        set(TransitionType),
        TransitionStrategyRegistry.available,
    )
    validate_registry(
        logger,
        "fifo resolve strategies",
        "backtest_engine.transition_engine.fifo.resolve_strategies.strategies",
        set(AtomicActionType),
        FIFOResolveRegistry.available,
    )
    validate_registry(
        logger,
        "SafeGuard strategies",
        "backtest_engine.transition_engine.fifo.guards_strategies.strategies",
        set(GuardName),
        SafeGuardRegistry.available,
    )
    validate_registry(
        logger,
        "fifo execution strategies",
        "backtest_engine.portfolio.execution_strategies.strategies",
        set(FIFOOperationType),
        FIFOExecutionRegistry.available,
    )
    logger.info("Backtest engine initialized successfully.")

def bootstrap_backtest_engine(
        logger_factory: LoggerFactory,
        strategy: type[AbstractStrategy],
        initial_cash: float,
        filters: list[type[AbstractFilter]] | None = None
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