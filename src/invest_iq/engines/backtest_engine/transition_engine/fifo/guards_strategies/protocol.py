from typing import Protocol

from invest_iq.engines.backtest_engine.common.types import ResolveContext


class SafeGuardProtocol[E](Protocol):
    """
    Base of integrity guards_strategies executed before a fifo strategy.
    """
    def check(
        self,
        context: ResolveContext,
        expected : E
    ) -> None:
        ...