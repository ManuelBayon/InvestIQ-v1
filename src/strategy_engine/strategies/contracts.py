from collections import defaultdict
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field

import pandas as pd

from strategy_engine.enums import MarketField
from strategy_engine.strategies.metadata import StrategyMetadata

@dataclass(frozen=True)
class StrategyInput:
    timestamp: pd.Timestamp
    bar: dict[str, float]
    history: Mapping[str, Sequence[float]]

@dataclass(frozen=True)
class FilterInput:
    timestamp: pd.Timestamp
    raw_target: float
    features: dict[str, object] | None = field(default_factory=dict)

@dataclass(frozen=True)
class StrategyOutput:
    timestamp: pd.Timestamp
    raw_target: float
    price_type: MarketField
    price: float
    metadata: StrategyMetadata
    features: dict[str, object] | None = field(default_factory=dict)
    diagnostics: dict[str, object] | None = field(default_factory=dict)

@dataclass(frozen=True)
class FilterOutput:
    timestamp: pd.Timestamp
    target_position: float
    diagnostics: dict[str, object] | None = field(default_factory=dict)

@dataclass(frozen=True)
class OrchestratorOutput:
    timestamp: pd.Timestamp
    target_position: float
    price_type: MarketField
    price: float
    diagnostics: dict[str, object] | None = field(default_factory=dict)