from abc import ABC, abstractmethod
from dataclasses import dataclass

from strategy_engine.strategies.contracts import FilterOutput, FilterInput, ComponentType, MarketField


@dataclass(frozen=True)
class FilterMetadata:
    component_type: ComponentType.FILTER
    name: str
    version: str
    description: str
    parameters: dict[str, object]
    required_fields : list[str]
    produced_features: list[str]
    diagnostics_schema: list[str]

class AbstractFilter(ABC):

    metadata: FilterMetadata

    @abstractmethod
    def apply_filter(self, input_: FilterInput) -> FilterOutput:
        ...