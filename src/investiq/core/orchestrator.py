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
            available_pipelines: frozenset[str],
            strategy: Strategy,
            filters: Sequence[Filter] | None = None
    ):
        # --- CONFIG VALIDATION  ---
        required = strategy.metadata.required_pipelines
        missing = required - available_pipelines
        if missing:
            raise ValueError(
                f"Strategy '{strategy.metadata.name}' requires unknown pipelines: {sorted(missing)}."
                f"Available pipelines: {sorted(available_pipelines)}"
            )
        self._strategy = strategy
        self._filters = list(filters) if filters else []

    def run(self, *, view: BacktestView) -> Decision:

        d0 = self._strategy.decide(view=view)

        diagnostics = {
            "strategy": {self._strategy.metadata.name: d0.diagnostics},
            "filters": []
        }

        d = d0
        for f in self._filters:
            d = f.apply(view=view, decision=d)
            diagnostics["filters"].append({f.metadata.name: d.diagnostics})

        return Decision(
            timestamp=d.timestamp,
            target_position=d.target_position,
            execution_price=d.execution_price,
            diagnostics=diagnostics,
        )