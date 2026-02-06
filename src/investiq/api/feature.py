from dataclasses import dataclass
from typing import Mapping, Sequence


@dataclass(frozen=True)
class FeatureView:
    """
    Read-only snapshot of features at current timestamp.

    - values: latest scalar values (e.g. ma_fast, rsi, vol_20)
    - history: optional per-feature history (same order as market events ingested)
    - ready: global readiness flag (feature pipelines decide)
    """
    values: Mapping[str, float]
    history: Mapping[str, Sequence[float]]
    ready: bool

    def get(self, name: str) -> float | None:
        return self.values.get(name)

    def require(self, name: str) -> float:
        v = self.values.get(name)
        if v is None:
            raise KeyError(f"Missing feature: {name}")
        return v

    def series(self, name: str) -> Sequence[float]:
        s = self.history.get(name)
        if s is None:
            raise KeyError(f"Missing feature history: {name}")
        return s