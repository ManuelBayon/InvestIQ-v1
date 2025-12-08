from dataclasses import dataclass
from enum import Enum

import pandas as pd

from strategy_engine.strategies.abstract_strategy import StrategyMetadata

class Version(str, Enum):
    V1= "1.0"

class MarketField(str, Enum):
    OPEN = "open"
    HIGH = "high"
    LOW = "low"
    CLOSE = "close"

class ComponentType(str, Enum):
    STRATEGY = "strategy"
    FILTER = "filter"

@dataclass(frozen=True)
class OrchestratorInput:
    timestamp: pd.Series
    data: dict[str, pd.Series]
    extra: dict[str, object] | None = None

@dataclass(frozen=True)
class StrategyInput:
    timestamp: pd.Series
    data: dict[str, pd.Series]
    extra: dict [str, object]| None = None

@dataclass(frozen=True)
class FilterInput:
    timestamp: pd.Series
    raw_target: pd.Series
    features: dict[str, object] | None = None

@dataclass(frozen=True)
class StrategyOutput:
    timestamp: pd.Series
    raw_target: pd.Series
    price_type: MarketField
    price_serie: pd.Series
    metadata: StrategyMetadata
    features: dict[str, object] | None = None
    diagnostics: dict[str, object] | None = None

@dataclass(frozen=True)
class FilterOutput:
    timestamp: pd.Series
    target_position: pd.Series
    diagnostics: dict[str, object] | None = None
    version: Version = Version.V1

@dataclass(frozen=True)
class OrchestratorOutput:
    timestamp: pd.Series
    target_position: pd.Series
    price_type: MarketField
    price_serie: pd.Series
    version: Version = Version.V1
    diagnostics : dict[str, object] | None = None