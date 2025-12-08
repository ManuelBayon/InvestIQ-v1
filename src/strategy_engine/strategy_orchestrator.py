from strategy_engine.strategies.abstract_strategy import AbstractStrategy
from strategy_engine.filters.abstract_filter import AbstractFilter
from strategy_engine.strategies.contracts import StrategyInput, OrchestratorOutput, OrchestratorInput, MarketField, \
    StrategyOutput, FilterOutput, FilterInput


class StrategyOrchestrator:

    def __init__(self, strategy: AbstractStrategy):
        self._strategy: AbstractStrategy = strategy
        self._filters: list[AbstractFilter] = []

    def add_filter(self, filter_: AbstractFilter):
        self._filters.append(filter_)

    def run(self, input_: OrchestratorInput) -> OrchestratorOutput:

        """
        1. Executes the strategy. Returns raw signals.
        """

        strategy_output: StrategyOutput = self._strategy.generate_raw_signals(
            StrategyInput(
                timestamp=input_.timestamp,
                data=input_.data,
                extra=input_.extra
            )
        )

        strategy_diagnostics = {
            strategy_output.metadata.name : strategy_output.diagnostics
        }

        """ 
        2. Applies sequentially all the filters, 
        the inputs of the filters are the output of the previous ones.
        """

        # Initialize input before filter loop
        filter_input = FilterInput(
            timestamp = strategy_output.timestamp,
            raw_target=strategy_output.raw_target,
            features=strategy_output.features
        )

        # Initialize output before filter loop
        filter_output = FilterOutput(
            timestamp=strategy_output.timestamp,
            target_position=strategy_output.raw_target

        )

        # Initialize filter_diagnostics
        filter_diagnostics = []

        # Applying filters
        for f in self._filters:
            filter_output: FilterOutput = f.apply_filter(filter_input)
            filter_diagnostics.append({
                f.metadata.name: filter_output.diagnostics
            })
            filter_input = FilterInput(
                timestamp=filter_output.timestamp,
                raw_target=filter_output.target_position,
                features = filter_input.features
            )
        """
        3. Returns the target positions.
        """
        all_diagnostics = {
            "strategy": strategy_diagnostics,
            "filters": filter_diagnostics
        }
        return OrchestratorOutput(
            timestamp= filter_output.timestamp,
            target_position = filter_output.target_position,
            price_type = strategy_output.price_type,
            price_serie = strategy_output.price_serie,
            diagnostics=all_diagnostics
        )