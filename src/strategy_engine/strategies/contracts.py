from dataclasses import dataclass
from enum import Enum

import pandas as pd

class StrategyVersion(str, Enum):
    V1= "v1"

class SignalPrice(str, Enum):
    OPEN = "OPEN"
    HIGH = "HIGH"
    LOW = "LOW"
    CLOSE = "CLOSE"

@dataclass(frozen=True)
class StrategyInput:
    timestamp: pd.Series
    open: pd.Series | None = None
    high: pd.Series | None = None
    low: pd.Series | None = None
    close: pd.Series | None = None
    volume: pd.Series | None = None
    extra: dict | None = None

@dataclass(frozen=True)
class StrategyOutput:
    timestamp: pd.Series
    raw_target: pd.Series
    signal_price: SignalPrice
    signal_price_series: pd.Series
    diagnostics: pd.DataFrame | None = None
    strategy_version: StrategyVersion = StrategyVersion.V1