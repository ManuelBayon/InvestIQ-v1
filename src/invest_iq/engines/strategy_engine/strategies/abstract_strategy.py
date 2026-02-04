from abc import ABC, abstractmethod

from invest_iq.engines.backtest_engine.common.types import BacktestView, StrategyInput, StrategyOutput
from invest_iq.engines.strategy_engine.strategies.metadata import StrategyMetadata


class AbstractStrategy(ABC):

    metadata: StrategyMetadata

    @abstractmethod
    def generate_raw_signals(
            self,
            strategy_input: StrategyInput,
            view: BacktestView
    ) -> StrategyOutput:
        ...