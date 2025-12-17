from typing import ClassVar, Callable

from engine.backtest_engine.common.enums import GuardName
from engine.backtest_engine.transition_engine.fifo.guards_strategies.expectations import GuardExpectation
from engine.backtest_engine.transition_engine.fifo.guards_strategies.factory import SafeGuardFactory
from engine.backtest_engine.transition_engine.fifo.guards_strategies.interface import ResolveContext, SafeGuard
from engine.utilities.logger.protocol import LoggerProtocol


class FIFOResolveStrategyBase:

    STRATEGY_NAME : ClassVar[str]
    REQUIRED_GUARDS: ClassVar[list[GuardName]] = []

    def __init__(
            self,
            logger: LoggerProtocol,
            safe_guard_factory: SafeGuardFactory
    ) -> None:
        self._logger = logger
        self._safe_guard_factory = safe_guard_factory

    def apply_guards(
            self,
            context: ResolveContext,
            factory: SafeGuardFactory,
            expectation_builders: dict[str, Callable[[], GuardExpectation]]
    ) -> None:
        safe_guards: list[SafeGuard[GuardExpectation]] = [
            factory.create(name) for name in self.REQUIRED_GUARDS
        ]
        for guard in safe_guards:
            builder = expectation_builders.get(guard.STRATEGY_NAME)
            if not builder:
                raise RuntimeError(
                    f"No expectation builder defined for {guard.STRATEGY_NAME}"
                )
            expectation = builder()
            guard.check(context, expectation)