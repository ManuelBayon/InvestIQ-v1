import datetime
from abc import ABC, abstractmethod
from dataclasses import dataclass

from strategy_engine.strategies.contracts import StrategyInput, StrategyOutput, ComponentType, MarketField


@dataclass(frozen=True)
class StrategyMetadata:
    strategy_uuid: str
    created_at: str
    name: str
    version: str
    description : str
    parameters: dict[str, object]
    price_type : MarketField
    required_fields : list[str]
    produced_features : list[str]
    component_type : ComponentType = ComponentType.STRATEGY

class AbstractStrategy(ABC):

    metadata: StrategyMetadata

    @abstractmethod
    def generate_raw_signals(
            self,
            input_ : StrategyInput
    ) -> StrategyOutput:
        pass