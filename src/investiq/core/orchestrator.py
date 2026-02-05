from collections.abc import Sequence

from investiq.api.backtest import BacktestView
from investiq.api.execution import Decision
from investiq.api.filter import Filter
from investiq.api.strategy import Strategy


class StrategyOrchestrator:
    """
    - consumes a read-only view (BacktestView), never a mutable context
    - strategy + filters are pure transformations (no state mutation)
    - invariants are checked at the boundary
    - diagnostics are aggregated deterministically
    """
    def __init__(
            self,
            strategy: Strategy,
            filters: Sequence[Filter] | None = None
    ):
        self._strategy = strategy
        self._filters = list(filters) if filters else []

    def add_filter(self, fltr: Filter) -> None:
        self._filters.append(fltr)

    def run(
            self,
            view: BacktestView,
    ) -> Decision:

        decision = self._strategy.decide(view=view)

        diagnostics = {
            "strategy": {self._strategy.metadata.name: decision.diagnostics},
            "filters": []
        }

        for f in self._filters:
            decision = f.apply(view=view, decision=decision)
            diagnostics["filters"].append({f.metadata.name: decision.diagnostics})

        return Decision(
            timestamp=decision.timestamp,
            target_position=decision.target_position,
            execution_price=decision.execution_price,
            diagnostics=diagnostics,
        )