from abc import ABC, abstractmethod

from backtest_engine.common.contracts import BacktestContext
from strategy_engine.contracts import StrategyInput, StrategyOutput
from strategy_engine.strategies.metadata import StrategyMetadata


class AbstractStrategy(ABC):

    metadata: StrategyMetadata

    @abstractmethod
    def generate_raw_signals(
            self,
            strategy_input: StrategyInput,
            context: BacktestContext | None = None
    ) -> StrategyOutput:
        ...