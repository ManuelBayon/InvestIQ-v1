from abc import ABC, abstractmethod

from invest_iq.engines.backtest_engine.common.backtest_context import FilterInput, FilterOutput
from invest_iq.engines.strategy_engine.filters.metadata import FilterMetadata


class AbstractFilter(ABC):
    metadata: FilterMetadata
    @abstractmethod
    def apply_filter(
            self,
            input_: FilterInput
    ) -> FilterOutput:
        ...