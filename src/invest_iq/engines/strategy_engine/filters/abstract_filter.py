from abc import ABC, abstractmethod

from invest_iq.engines.strategy_engine.filters.metadata import FilterMetadata
from invest_iq.engines.strategy_engine.contracts import FilterOutput, FilterInput




class AbstractFilter(ABC):

    metadata: FilterMetadata

    @abstractmethod
    def apply_filter(
            self,
            input_: FilterInput
    ) -> FilterOutput:
        ...