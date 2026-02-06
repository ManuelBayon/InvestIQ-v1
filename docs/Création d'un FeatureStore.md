Oui : **un FeatureStore “générique”** (qui peut contenir n’importe quelles features) est exactement l’analogue du `MarketStore`.

du `MarketStore`.  
Ce que je t’ai donné était un _MVP_ mono-indicateur. On va faire “desk-grade” :

- `FeatureStore` = **conteneur + orchestrateur** (il ne “connaît” pas SMA / RSI / etc.)
- Les calculs sont des **FeaturePipelines** (ou “FeatureComputers”) enregistrés (registry/factory comme tes rules/strategies)
- `FeatureView` = read-only snapshot (features scalaires + éventuellement history)
- Chaque pipeline lit le `MarketStore` et écrit dans le `FeatureStore`.

Je te donne une version **générique**, simple, et extensible, sans explosion de fichiers.

---
# 1) `src/investiq/api/feature.py` — **MODIF** (FeatureView plus riche)

```python
from __future__ import annotations

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
```

---
# 2) `src/investiq/core/features/api.py` — **NEUF** (Protocol pipeline)

```python
from __future__ import annotations

from typing import ClassVar, Protocol

from investiq.core.market_store import MarketStore


class FeaturePipeline(Protocol):
    """
    A feature pipeline reads MarketStore and writes into FeatureStore.

    It may keep internal state (allowed): determinism is ensured because
    the state is inside the engine, not inside strategies.
    """
    NAME: ClassVar[str]

    def reset(self) -> None: ...
    def update(self, *, market: MarketStore, store: "FeatureStore") -> None: ...
```

---
# 3) `src/investiq/core/features/registry.py` — **NEUF**

``` python
from __future__ import annotations

from collections.abc import Callable
from typing import TypeVar

from investiq.core.features.api import FeaturePipeline

T = TypeVar("T", bound=FeaturePipeline)


class FeaturePipelineRegistry:
    _registry: dict[str, type[FeaturePipeline]] = {}

    @classmethod
    def register(cls, *, name: str, pipeline_cls: type[FeaturePipeline]) -> None:
        if name in cls._registry:
            raise KeyError(f"Feature pipeline already registered: {name}")
        cls._registry[name] = pipeline_cls

    @classmethod
    def get(cls, name: str) -> type[FeaturePipeline]:
        try:
            return cls._registry[name]
        except KeyError:
            raise KeyError(f"Unknown feature pipeline: {name}. available={list(cls._registry)}")

    @classmethod
    def all(cls) -> list[type[FeaturePipeline]]:
        return list(cls._registry.values())


def register_feature_pipeline(name: str) -> Callable[[type[T]], type[T]]:
    def deco(cls_: type[T]) -> type[T]:
        FeaturePipelineRegistry.register(name=name, pipeline_cls=cls_)
        return cls_
    return deco
```

---
## 4) `src/investiq/core/features/store.py` — **NEUF** (FeatureStore générique)

Ici, le store :

- maintient `values` (dernier point)
- maintient `history` (liste append-only) optionnelle
- gère `ready` global (AND logique de readiness des pipelines)
- orchestre toutes les pipelines enregistrées (ou injectées)

```python
from __future__ import annotations

from collections import defaultdict
from collections.abc import Mapping, Sequence
from typing import Final

from investiq.api.feature import FeatureView
from investiq.core.features.api import FeaturePipeline
from investiq.core.features.registry import FeaturePipelineRegistry
from investiq.core.market_store import MarketStore


class FeatureStore:
    """
    Generic feature store:
      - holds latest values and optional history
      - runs pipelines to compute/update features
    """

    def __init__(self, *, keep_history: bool = True, pipelines: Sequence[FeaturePipeline] | None = None) -> None:
        self._keep_history: Final[bool] = keep_history

        self._values: dict[str, float] = {}
        self._history: dict[str, list[float]] = defaultdict(list)

        # Instantiate pipelines (default: everything registered)
        if pipelines is None:
            self._pipelines: list[FeaturePipeline] = [cls_() for cls_ in FeaturePipelineRegistry.all()]
        else:
            self._pipelines = list(pipelines)

        self._ready: bool = True  # can be flipped false by pipelines

    def reset(self) -> None:
        self._values.clear()
        self._history.clear()
        self._ready = True
        for p in self._pipelines:
            p.reset()

    # --- write API for pipelines ---

    def set(self, *, name: str, value: float, ready: bool = True) -> None:
        self._values[name] = float(value)
        if self._keep_history:
            self._history[name].append(float(value))
        # readiness is a global AND
        self._ready = self._ready and bool(ready)

    def mark_not_ready(self) -> None:
        self._ready = False

    # --- orchestration ---

    def ingest(self, *, market: MarketStore) -> None:
        # reset readiness each tick (pipelines recompute ready based on current history)
        self._ready = True
        for p in self._pipelines:
            p.update(market=market, store=self)

    def view(self) -> FeatureView:
        history_view: Mapping[str, Sequence[float]] = self._history
        return FeatureView(values=dict(self._values), history=history_view, ready=self._ready)
```

---
## 5) `src/investiq/core/features/implementations.py` — **NEUF** (ex: SMA pipeline)

Tu vois : **SMA devient une pipeline**, mais le store reste générique.

```python
from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

from investiq.api.market import MarketField
from investiq.core.features.api import FeaturePipeline
from investiq.core.features.registry import register_feature_pipeline
from investiq.core.market_store import MarketStore
from investiq.core.features.store import FeatureStore


@dataclass
class _SMAState:
    window: int
    value: float | None = None

    def reset(self) -> None:
        self.value = None

    def update(self, series: list[float]) -> float | None:
        n = len(series)
        if n < self.window:
            self.value = None
            return None
        if n == self.window:
            self.value = sum(series[-self.window:]) / self.window
            return self.value
        if self.value is None:
            self.value = sum(series[-self.window:]) / self.window
            return self.value
        x_t = series[-1]
        x_out = series[-self.window - 1]
        self.value = self.value + (x_t - x_out) / self.window
        return self.value


@register_feature_pipeline("SMA_FAST_SLOW")
class SMACrossFeatures(FeaturePipeline):
    NAME: ClassVar[str] = "SMA_FAST_SLOW"

    def __init__(self, fast_window: int = 20, slow_window: int = 100) -> None:
        if fast_window <= 0 or slow_window <= 0:
            raise ValueError("windows must be positive")
        if fast_window >= slow_window:
            raise ValueError("fast_window must be < slow_window")

        self._fast = _SMAState(window=fast_window)
        self._slow = _SMAState(window=slow_window)

    def reset(self) -> None:
        self._fast.reset()
        self._slow.reset()

    def update(self, *, market: MarketStore, store: FeatureStore) -> None:
        closes_seq = market.history.get(MarketField.CLOSE)
        if closes_seq is None:
            store.mark_not_ready()
            return

        closes = list(closes_seq)

        ma_fast = self._fast.update(closes)
        ma_slow = self._slow.update(closes)

        if ma_fast is None or ma_slow is None:
            # Not ready until both are available
            store.mark_not_ready()
            return

        store.set(name="ma_fast", value=ma_fast, ready=True)
        store.set(name="ma_slow", value=ma_slow, ready=True)
```

Plus tard tu mets RSI, ATR, VWAP, vol, etc. dans ce fichier (ou tu split si ça grossit).

---
## 6) `src/investiq/core/engine.py` — **MODIF** (comme avant)

Tu utilises le store générique.

```python
from investiq.core.features.store import FeatureStore

class BacktestEngine:
    def __init__(..., feature_store: FeatureStore | None = None, ...):
        ...
        self._features = feature_store or FeatureStore()

    def step(self, event):
        self._market.ingest(event)
        self._features.ingest(market=self._market)

        view = BacktestView(
            market=self._market.view(),
            execution=self._execution_view(),
            features=self._features.view(),
        )
        ...
```

---
## 7) Stratégie MA Cross — **MODIF** (pure, comme on voulait)

Elle lit `view.features.require("ma_fast")`, etc. Aucun état.

---
# Pourquoi c’est “desk-grade” et cohérent avec ton analogie

- `MarketStore` : état du marché + historique canonique
- `FeatureStore` : état des features + historique canonique (calculé)
- `BacktestView` : read-only snapshot `{market, execution, features}`
- Les stratégies sont des **fonctions pures** : `view -> decision`

Et tu n’exploses pas en fichiers : tu as un **petit sous-module `core/features/`** avec 4 fichiers stables.

---

# Point important : “n’importe quelle feature”

Oui, mais il faut décider **ce que tu stockes** :

- **scalars** (float) : ok pour 90% (MA, RSI, vol, beta, zscore…)
- si tu veux des structures (ex: order book), tu ajoutes plus tard `FeatureValue = float | int | ...` mais garde simple au début.