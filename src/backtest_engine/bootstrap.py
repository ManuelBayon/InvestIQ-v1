from typing import TypeVar, Callable

from backtest_engine.common.enums import CurrentState, Event, TransitionType, AtomicActionType, FIFOOperationType
from backtest_engine.common.enums import GuardName
from backtest_engine.portfolio.execution_strategies.registry import FIFOExecutionRegistry
from backtest_engine.transition_engine.fifo.guards_strategies.registry import SafeGuardRegistry
from backtest_engine.transition_engine.fifo.resolve_strategies.registry import FIFOResolveRegistry
from backtest_engine.transition_engine.transition_rules.registry import TransitionRuleRegistry
from backtest_engine.transition_engine.transition_strategies.registry import TransitionStrategyRegistry
from utilities.import_tools import import_submodules
from utilities.logger.factory import LoggerFactory
from utilities.logger.protocol import LoggerProtocol

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

def backtest_engine_bootstrap(logger : LoggerProtocol) -> None:
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