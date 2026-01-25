from dataclasses import dataclass, asdict

import pandas as pd

@dataclass(frozen=True)
class OHLCV:
    open: float
    high: float
    low: float
    close: float
    volume: float = 0.0

    def __getitem__(self, key: str) -> float:
        try:
            return getattr(self, key)
        except AttributeError as e:
            raise KeyError(key) from e

    def __contains__(self, key: object) -> bool:
        return isinstance(key, str) and hasattr(self, key)

    def items(self):
        for k in ("open","high","low","close","volume"):
            yield k, getattr(self, k)

@dataclass(frozen=True)
class MarketEvent:
    timestamp: pd.Timestamp
    bar: OHLCV
    symbol: str | None = None
    bar_size: str | None = None

