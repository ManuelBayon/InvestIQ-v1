from abc import ABC, abstractmethod

from strategy_engine.filters.metadata import FilterMetadata
from strategy_engine.strategies.contracts import FilterOutput, FilterInput




class AbstractFilter(ABC):

    metadata: FilterMetadata

    @abstractmethod
    def apply_filter(self, input_: FilterInput) -> FilterOutput:
        ...