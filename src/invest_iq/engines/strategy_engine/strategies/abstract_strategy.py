from abc import ABC, abstractmethod

from invest_iq.engines.backtest_engine.common.types import BacktestView, Decision
from invest_iq.engines.strategy_engine.strategies.metadata import StrategyMetadata


class AbstractStrategy(ABC):

    metadata: StrategyMetadata

    @abstractmethod
    def decide(
            self,
            view: BacktestView
    ) -> Decision:
        ...