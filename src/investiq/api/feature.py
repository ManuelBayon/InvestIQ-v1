from dataclasses import dataclass
from typing import Mapping, Sequence


@dataclass(frozen=True)
class FeatureSnapshot:
    """
    Read-only snapshot of features at current timestamp.

    - values: latest scalar values (e.g. ma_fast, rsi, vol_20)
    - history: optional per-feature history (same order as market events ingested)
    - ready: global readiness flag (feature pipelines decide)
    """
    values: Mapping[str, float]
    history: Mapping[str, Sequence[float]]
    pipeline_ready: Mapping[str, bool]
    global_ready: bool

    def require(self, name: str) -> float:
        v = self.values.get(name)
        if v is None:
            raise KeyError(f"Missing feature: {name}")
        return v

    def __getitem__(self, name: str) -> float:
        return self.require(name)

    def series(self, name: str) -> Sequence[float]:
        s = self.history.get(name)
        if s is None:
            raise KeyError(f"Missing feature history: {name}")
        return s

    def pipeline_is_ready(self, pipeline: str) -> bool:
        v = self.pipeline_ready.get(pipeline)
        if v is None:
            raise KeyError(f"Unknown pipeline: {pipeline}")
        return bool(v)