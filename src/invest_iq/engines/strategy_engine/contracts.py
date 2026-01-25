from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field

import pandas as pd

from invest_iq.common.market_types import OHLCV
from invest_iq.engines.strategy_engine.enums import MarketField
from invest_iq.engines.strategy_engine.strategies.metadata import StrategyMetadata

@dataclass(frozen=True)
class StrategyInput:
    timestamp: pd.Timestamp
    bar: OHLCV
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
    price: float
    price_type: MarketField
    metadata: StrategyMetadata
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