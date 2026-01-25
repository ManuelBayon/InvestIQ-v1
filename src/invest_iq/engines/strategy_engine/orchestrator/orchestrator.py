from collections.abc import Sequence

from invest_iq.engines.backtest_engine.common.backtest_context import BacktestContext
from invest_iq.engines.strategy_engine.strategies.abstract_strategy import AbstractStrategy
from invest_iq.engines.strategy_engine.filters.abstract_filter import AbstractFilter
from invest_iq.engines.strategy_engine.contracts import StrategyInput, OrchestratorOutput, StrategyOutput, FilterInput, \
    FilterOutput


class StrategyOrchestrator:

    def __init__(
            self,
            strategy: AbstractStrategy,
            filters: Sequence[AbstractFilter] | None = None
    ):
        self._strategy = strategy
        self._filters = list(filters) if filters else []

    def add_filter(
            self,
            filter_: AbstractFilter
    ) -> None:
        self._filters.append(filter_)

    def run(
            self,
            context: BacktestContext
    ) -> OrchestratorOutput:
        """
        1. Executes the strategy. Returns strategy_output.
        """
        strat_input = StrategyInput(
            timestamp=context.timestamp,
            bar=context.bar,
            history=context.history
        )

        strategy_output: StrategyOutput = self._strategy.generate_raw_signals(
            strategy_input=strat_input,
            context=context
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
            features=context.features_history
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