from abc import ABC, abstractmethod

from strategy_engine.strategies.contracts import StrategyInput, StrategyOutput
from strategy_engine.strategies.metadata import StrategyMetadata


class AbstractStrategy(ABC):

    metadata: StrategyMetadata

    @abstractmethod
    def generate_raw_signals(
            self,
            input_ : StrategyInput
    ) -> StrategyOutput:
        pass