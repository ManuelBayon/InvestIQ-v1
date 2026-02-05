from abc import ABC, abstractmethod

from invest_iq.engines.backtest_engine.common.types import BacktestView, Decision
from invest_iq.engines.strategy_engine.filters.metadata import FilterMetadata


class AbstractFilter(ABC):
    metadata: FilterMetadata
    @abstractmethod
    def apply(
            self,
            view: BacktestView,
            decision: Decision,
    ) -> Decision:
        ...