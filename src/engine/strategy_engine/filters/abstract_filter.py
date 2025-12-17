from abc import ABC, abstractmethod

from engine.strategy_engine.filters.metadata import FilterMetadata
from engine.strategy_engine.contracts import FilterOutput, FilterInput




class AbstractFilter(ABC):

    metadata: FilterMetadata

    @abstractmethod
    def apply_filter(
            self,
            input_: FilterInput
    ) -> FilterOutput:
        ...