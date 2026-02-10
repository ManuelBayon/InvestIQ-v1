Voici une implémentation **desk-grade** d’une pipeline SMA “fast/slow” (atomique), qui :

- lit `MarketStore.history[MarketField.CLOSE]`
- calcule les deux SMAs **incrémentalement**
- écrit `ma_fast`, `ma_slow` dans le `FeatureStore`
- met `pipeline_ready=True` **uniquement quand les deux existent** (au tick courant)
- supporte `reset()`

> Je respecte ta signature actuelle : `update(market_store=..., feature_store=...)`.

```python
from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

from investiq.api.market import MarketField
from investiq.core.features.registry import register_feature_pipeline
from investiq.core.features.api import FeaturePipeline
from investiq.core.market_state_builder import MarketStore
from investiq.core.features.store import FeatureStore


@dataclass
class _SMAState:
    window: int
    value: float | None = None

    def reset(self) -> None:
        self.value = None

    def update(self, series: list[float]) -> float | None:
        """
        Incremental SMA update.

        - If len(series) < window: not ready -> None
        - If len(series) == window: compute full SMA
        - Else: update in O(1) using previous SMA
        """
        n = len(series)
        if n < self.window:
            self.value = None
            return None

        if n == self.window or self.value is None:
            self.value = sum(series[-self.window:]) / self.window
            return self.value

        x_t = series[-1]
        x_out = series[-self.window - 1]
        self.value = self.value + (x_t - x_out) / self.window
        return self.value


@register_feature_pipeline
class SMAPipeline(FeaturePipeline):
    """
    Produces:
      - ma_fast
      - ma_slow

    Readiness:
      - ready for the current tick iff both SMAs are defined.
    """

    NAME: ClassVar[str] = "SMA_FAST_SLOW"

    def __init__(self, fast_window: int = 20, slow_window: int = 100) -> None:
        if fast_window <= 0 or slow_window <= 0:
            raise ValueError("fast_window and slow_window must be positive")
        if fast_window >= slow_window:
            raise ValueError("fast_window must be < slow_window")

        self._fast = _SMAState(window=fast_window)
        self._slow = _SMAState(window=slow_window)

    def reset(self) -> None:
        self._fast.reset()
        self._slow.reset()

    def update(self, *, market_store: MarketStore, feature_store: FeatureStore) -> None:
        closes_seq = market_store.history.get(MarketField.CLOSE)
        if closes_seq is None:
            # Pas de données -> pas ready, pas d'écriture
            return

        closes = list(closes_seq)

        ma_fast = self._fast.update(closes)
        ma_slow = self._slow.update(closes)

        if ma_fast is None or ma_slow is None:
            # Warmup pas fini -> pas ready
            return

        # Écrire les features (atomiques)
        feature_store.set_value("ma_fast", ma_fast)
        feature_store.set_value("ma_slow", ma_slow)

        # Marquer ready pour ce tick
        feature_store.set_pipeline_ready(self.NAME)
```

### Notes pratiques

- Tu peux changer les noms de features (`"ma_fast"`, `"ma_slow"`) si tu veux un namespace (ex: `"trend.ma_fast"`), mais garde-les **stables**.
- Avec ton `FeatureStore.ingest()` qui reset `_pipelines_ready` à `False` à chaque tick, ce pipeline doit appeler `set_pipeline_ready()` **à chaque tick** où il est prêt (c’est ce qu’il fait).

Si tu me colles la structure exacte de `MarketStore.history` (type/structure) je peux enlever le `list(closes_seq)` si tu veux éviter une copie et rester purement streaming.