from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime
from typing import Protocol, FrozenSet

from investiq.api.backtest import BacktestView
from investiq.api.execution import Decision
from investiq.api.market import MarketField

@dataclass(frozen=True)
class StrategyMetadata:
    name: str
    version: str
    description: str

    parameters: Mapping[str, object]

    price_type: MarketField
    required_fields: FrozenSet[MarketField]
    produced_features: FrozenSet[str]

    component_type: str = "STRATEGY"
    created_at: datetime = datetime.now()

class Strategy(Protocol):
    metadata: StrategyMetadata
    def decide(self, view: BacktestView) -> Decision:
        ...