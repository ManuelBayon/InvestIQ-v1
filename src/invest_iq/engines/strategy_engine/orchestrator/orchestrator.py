from collections.abc import Sequence

from invest_iq.engines.backtest_engine.common.types import BacktestView, Decision
from invest_iq.engines.strategy_engine.strategies.abstract_strategy import AbstractStrategy
from invest_iq.engines.strategy_engine.filters.abstract_filter import AbstractFilter

class StrategyOrchestrator:
    """
    - consumes a read-only view (BacktestView), never a mutable context
    - strategy + filters are pure transformations (no state mutation)
    - invariants are checked at the boundary
    - diagnostics are aggregated deterministically
    """
    def __init__(
            self,
            strategy: AbstractStrategy,
            filters: Sequence[AbstractFilter] | None = None
    ):
        self._strategy = strategy
        self._filters = list(filters) if filters else []

    def add_filter(self, filter_: AbstractFilter) -> None:
        self._filters.append(filter_)

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
            price_ref=decision.price_ref,
            diagnostics=diagnostics,
        )