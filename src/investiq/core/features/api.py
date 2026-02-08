from typing import ClassVar, Protocol, TYPE_CHECKING

from investiq.core.market_store import MarketStore

if TYPE_CHECKING:
    from investiq.core.features.store import FeatureStore

class FeaturePipeline(Protocol):
    """
    A feature pipeline reads MarketStore and writes into FeatureStore.

    It may keep internal state (allowed): determinism is ensured because
    the state is inside the engine, not inside the strategies.
    """
    NAME: ClassVar[str]

    def reset(self) -> None:
        ...
    def update(
            self,
            market_store: MarketStore,
            feature_store: "FeatureStore"
    ) -> None:
        ...