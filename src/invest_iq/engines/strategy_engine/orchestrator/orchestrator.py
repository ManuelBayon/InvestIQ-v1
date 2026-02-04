from collections.abc import Sequence

from invest_iq.engines.backtest_engine.common.errors import OrchestratorInvariantError
from invest_iq.engines.backtest_engine.common.types import BacktestView, OrchestratorOutput, StrategyInput, \
    StrategyOutput, FilterInput
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
    ) -> OrchestratorOutput:

        if view.market.snapshot is None:
            raise OrchestratorInvariantError("Market snapshot must be initialized before orchestrator.run()")

        """
        1. Executes the strategy. Returns strategy_output.
        """
        strat_input = StrategyInput(
            timestamp=view.market.timestamp,
            bar=view.market.bar,
            history=view.market.history,
        )
        strategy_output: StrategyOutput = self._strategy.generate_raw_signals(
            strategy_input=strat_input,
            view=view
        )
        strategy_diagnostics = {
            strategy_output.metadata.name: strategy_output.diagnostics,
        }

        """
        2. Applying sequentially all registered filters to this strategy.
        """
        filter_in = FilterInput(
            timestamp=strategy_output.timestamp,
            raw_target=strategy_output.raw_target,
            features=
        )
        filter_out = FilterOutput(
            timestamp=strategy_output.timestamp,
            target_position=strategy_output.raw_target,
            diagnostics={}
        )
        filter_diagnostics : list[
            dict[str, object] | None
        ] = []

        for filter_ in self._filters:
            filter_out = filter_.apply_filter(filter_in)
            filter_diagnostics.append({
                filter_.metadata.name: filter_out.diagnostics
            })
            filter_in = FilterInput(
                timestamp=filter_out.timestamp,
                raw_target=filter_out.target_position,
                features=filter_in.features
            )
        final_target = filter_out.target_position

        """
        3. Aggregate diagnostics.
        """
        all_diagnostics = {
            "strategy": strategy_diagnostics,
            "filters": filter_diagnostics,
        }

        """
        4. Return OrchestratorOutput.
        """
        return OrchestratorOutput(
            timestamp=filter_out.timestamp,
            target_position=final_target,
            price_type=strategy_output.price_type,
            price=strategy_output.price,
            diagnostics=all_diagnostics
        )